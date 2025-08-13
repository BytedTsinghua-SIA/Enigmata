import random
import string
import json
from collections import Counter, defaultdict
import numpy as np
from tqdm import tqdm
import os
import hashlib
import time
from .template import PROMPT_TEMPLATE

PUZZLE_TYPE = "sequence_puzzle"
SOURCE_URL = "auto-generated"
DATASET_NAME = "car_painting"

CONFIGS = {
    "easy": {
        'N_range': (8, 15),
        'M_range': (2, 4),
        'K_range': (2, 4),
        'skew_range': (0.6, 0.8)  # Skewness degree of color distribution
    },
    "medium": {
        'N_range': (15, 25),
        'M_range': (3, 6),
        'K_range': (3, 5),
        'skew_range': (0.3, 0.5)
    },
    "hard": {
        'N_range': (25, 40),
        'M_range': (5, 9),
        'K_range': (2, 4),  # Smaller K makes the problem harder
        'skew_range': (0.1, 0.3)
    }
}

def string_to_md5(s):
    encoded_string = s.encode('utf-8')
    md5_hash = hashlib.md5()
    md5_hash.update(encoded_string)
    return md5_hash.hexdigest()

def generate_skewed_distribution(M, skew=0.5):
    """Generate skewed color distribution"""
    # Use power-law distribution to generate skewed probabilities
    raw_distribution = np.random.power(skew, M)
    # Normalize
    return raw_distribution / np.sum(raw_distribution)

def calculate_switches(arrangement, colors):
    """Calculate the number of color switches in a given arrangement"""
    switches = 0
    for i in range(1, len(arrangement)):
        if colors[arrangement[i]-1] != colors[arrangement[i-1]-1]:
            switches += 1
    return switches

def find_optimal_solution(car_ids, colors, K):
    """Find optimal solution using simulated annealing algorithm"""
    N = len(car_ids)
    
    # Initial solution is the original order
    current_solution = car_ids.copy()
    current_switches = calculate_switches(current_solution, colors)
    
    # Best solution
    best_solution = current_solution.copy()
    best_switches = current_switches
    
    # Simulated annealing parameters
    temperature = 100.0
    cooling_rate = 0.995
    iterations = 10000
    
    # Simulated annealing process
    for i in range(iterations):
        # Randomly select a car
        car_idx = random.randint(0, N-1)
        car_id = current_solution[car_idx]
        original_position = car_ids.index(car_id) + 1  # Original position (1-indexed)
        
        # Calculate movable range
        min_pos = max(0, car_idx - 1)  # At least stay within array bounds
        max_pos = min(N-1, car_idx + 1)  # At least stay within array bounds
        
        # Further restrict to K range
        min_allowed = max(0, original_position - 1 - K)  # Original position can move K positions forward
        max_allowed = min(N-1, original_position - 1 + K)  # Original position can move K positions backward
        
        # Find indices in the current solution that are within the allowed range
        valid_positions = []
        for pos in range(N):
            if min_allowed <= car_ids.index(current_solution[pos]) <= max_allowed:
                valid_positions.append(pos)
        
        # Randomly select a valid position for swapping
        if len(valid_positions) > 1:  # Ensure there are multiple positions to choose from
            new_idx = random.choice([p for p in valid_positions if p != car_idx])
            
            # Create new solution
            new_solution = current_solution.copy()
            
            # Move the car (by swapping)
            if new_idx > car_idx:
                # Move backward
                new_solution[car_idx:new_idx+1] = new_solution[car_idx+1:new_idx+1] + [new_solution[car_idx]]
            else:
                # Move forward
                new_solution[new_idx:car_idx+1] = [new_solution[car_idx]] + new_solution[new_idx:car_idx]
            
            # Check if the new solution satisfies constraints
            valid = True
            for j, car in enumerate(new_solution):
                original_pos = car_ids.index(car) + 1
                if not (original_pos - K <= j + 1 <= original_pos + K):
                    valid = False
                    break
            
            if valid:
                # Calculate color switches for the new solution
                new_switches = calculate_switches(new_solution, colors)
                
                # Calculate energy difference
                delta_e = new_switches - current_switches
                
                # Accept better solutions or worse solutions with a certain probability
                if delta_e < 0 or random.random() < np.exp(-delta_e / temperature):
                    current_solution = new_solution
                    current_switches = new_switches
                    
                    # Update best solution
                    if current_switches < best_switches:
                        best_solution = current_solution.copy()
                        best_switches = current_switches
        
        # Cool down
        temperature *= cooling_rate
    
    # Use local search to further optimize
    best_solution, best_switches = local_search(best_solution, colors, car_ids, K, best_switches)
    
    return best_solution, best_switches

def local_search(solution, colors, car_ids, K, current_best_switches):
    """Further optimize solution using local search"""
    improved = True
    best_solution = solution.copy()
    best_switches = current_best_switches
    
    while improved:
        improved = False
        N = len(solution)
        
        # Try all possible swaps
        for i in range(N):
            for j in range(i+1, N):
                # Check if swap is within K range
                car_i = best_solution[i]
                car_j = best_solution[j]
                original_pos_i = car_ids.index(car_i) + 1
                original_pos_j = car_ids.index(car_j) + 1
                
                if abs((j+1) - original_pos_i) <= K and abs((i+1) - original_pos_j) <= K:
                    # Create new solution
                    new_solution = best_solution.copy()
                    new_solution[i], new_solution[j] = new_solution[j], new_solution[i]
                    
                    # Calculate color switches for the new solution
                    new_switches = calculate_switches(new_solution, colors)
                    
                    # If a better solution is found
                    if new_switches < best_switches:
                        best_solution = new_solution
                        best_switches = new_switches
                        improved = True
                        break
            
            if improved:
                break
    
    return best_solution, best_switches

def is_solution_unique(car_ids, colors, K, solution, min_switches):
    """Check if the solution is unique"""
    # Run the algorithm again with different initial solutions
    for _ in range(3):  # Try a few different initial solutions
        random_start = car_ids.copy()
        random.shuffle(random_start)
        
        # Ensure the random initial solution satisfies K constraints
        valid = True
        for i, car in enumerate(random_start):
            original_pos = car_ids.index(car) + 1
            if abs((i+1) - original_pos) > K:
                valid = False
                break
        
        if not valid:
            continue
            
        alt_solution, alt_switches = find_optimal_solution(car_ids, colors, K)
        
        # If a different solution is found but has the same number of switches, the solution is not unique
        if alt_switches == min_switches and alt_solution != solution:
            return False
    
    return True

def generate_unique_car_painting_problem(difficulty="medium", max_tries=100):
    """Generate a unique solution car painting problem"""
    # Select parameters based on difficulty
    params = CONFIGS[difficulty]
    
    for _ in range(max_tries):
        # Randomly select parameter values
        N = random.randint(*params['N_range'])
        M = random.randint(*params['M_range'])
        K = random.randint(*params['K_range'])
        skew = random.uniform(*params['skew_range'])
        
        # Generate color distribution
        color_distribution = generate_skewed_distribution(M, skew=skew)
        
        # Generate colors
        available_colors = list(string.ascii_uppercase[:M])
        colors = []
        for i in range(M):
            color = available_colors[i]
            count = max(1, int(N * color_distribution[i]))
            colors.extend([color] * count)
        
        # Ensure color count is N
        while len(colors) < N:
            colors.append(random.choice(available_colors))
        while len(colors) > N:
            colors.pop()
        
        # Shuffle colors
        random.shuffle(colors)
        
        # Generate vehicle IDs
        car_ids = list(range(1, N+1))
        
        # Calculate optimal solution
        solution, min_switches = find_optimal_solution(car_ids, colors, K)
        
        # Ensure solution is unique
        if is_solution_unique(car_ids, colors, K, solution, min_switches):
            return {
                "N": N, 
                "M": M, 
                "K": K,
                "car_ids": car_ids,
                "colors": colors,
                "solution": solution,
                "min_switches": min_switches,
                "difficulty_level": difficulty
            }
    
    return None

def transform_problem_to_meta(problem, idx, language, split):
    """Convert problem to meta data format"""
    timestamp = str(time.time())
    random_suffix = random.randint(0, int(1e6))
    id_string = f"car_painting_{idx}_{timestamp}_{random_suffix}"
    hash_id_string = string_to_md5(id_string)
    
    return {
        "id": hash_id_string,
        "N": problem["N"],
        "M": problem["M"],
        "K": problem["K"],
        "car_ids": problem["car_ids"],
        "colors": problem["colors"],
        "solution": problem["solution"],
        "min_switches": problem["min_switches"],
        "split": split,
        "type": PUZZLE_TYPE,
        "source_url": SOURCE_URL,
        "dataset_name": DATASET_NAME,
        "difficulty_level": problem["difficulty_level"],
        "language": language,
    }

def generate(count=100, difficulty="medium", language="en", split="train"):
    prompt_template = PROMPT_TEMPLATE
    generated = 0
    attempts = 0
    max_attempts = count * 10  

    while generated < count and attempts < max_attempts:
        try:
            problem = generate_unique_car_painting_problem(difficulty)
            if problem:
                meta = transform_problem_to_meta(problem, generated, language, split)
                
                # Format prompt
                formatted_prompt = prompt_template.format(
                    n=meta["N"],
                    m=meta["M"],
                    k=meta["K"],
                    car_ids=meta["car_ids"],
                    colors=meta["colors"]
                )
                
                yield {
                    "prompt": formatted_prompt,
                    "answer": meta["solution"],
                    "task_name": DATASET_NAME,
                    "ability": PUZZLE_TYPE,
                    "language": language,
                    "meta": json.dumps(meta),
                }
                generated += 1
        except Exception as e:
            print(f"Generation error: {e}")
        attempts += 1

    if attempts >= max_attempts:
        print(f"Warning: Maximum attempt count reached, generated {generated} / {count} problems.")

def save_to_jsonl(output_file, count, language, split):
    """Save generated problems to jsonl file"""
    difficulties = ["easy", "medium", "hard"]
    per_difficulty = count // len(difficulties)
    remainder = count % len(difficulties)
    difficulty_counts = {d: per_difficulty for d in difficulties}
    for i in range(remainder):
        difficulty_counts[difficulties[i]] += 1


    with open(output_file, 'w', encoding='utf-8') as f:
        for difficulty in difficulties:
            num = difficulty_counts[difficulty]
            if num == 0:
                continue
            print(f"Generating {difficulty} problems: {num} problems")
            for item in tqdm(generate(num, difficulty=difficulty, language=language, split=split), desc=f"Generating {difficulty} problems"):
                f.write(json.dumps(item, ensure_ascii=False) + '\n')

