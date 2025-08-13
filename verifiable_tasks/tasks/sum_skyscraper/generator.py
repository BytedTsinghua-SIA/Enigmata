import numpy as np
import random
from tqdm import tqdm
import json
from .template import PROMPT_TEMPLATE

# Function to generate random skyscraper grid and compute its clues
def generate_random_latin_square(N):
    def is_safe(matrix, row, col, num):
        # Check row
        if num in matrix[row]:
            return False
        # Check column
        if num in [matrix[i][col] for i in range(N)]:
            return False
        return True

    def backtrack(matrix, row, col):
        if col == N:
            row += 1
            col = 0
        
        if row == N:
            return True
        
        # Create a list of numbers in random order
        nums = list(range(1, N+1))
        random.shuffle(nums)
        
        for num in nums:
            if is_safe(matrix, row, col, num):
                matrix[row][col] = num
                if backtrack(matrix, row, col + 1):
                    return True
                matrix[row][col] = 0
        
        return False

    matrix = [[0 for _ in range(N)] for _ in range(N)]
    if backtrack(matrix, 0, 0):
        return matrix
    else:
        raise ValueError("No solution exists")

def generate_valid_skyscraper_data(n):
    # Generate a random n x n grid with unique numbers in each row and column
    grid = generate_random_latin_square(n)
    # grid = grid.tolist()
    # Function to calculate the clues for a single direction
    def calculate_clues(grid):
        clues = []
        for line in grid:
            max_seen = 0
            count = 0
            for height in line:
                if height > max_seen:
                    count += height
                    max_seen = height
            clues.append(int(count))
        return clues
    grid = np.array(grid)
    # Top clues (look from top to bottom)
    top_clues = calculate_clues(grid.T)
    
    # Bottom clues (look from bottom to top)
    bottom_clues = calculate_clues(np.flipud(grid).T)
    
    # Left clues (look from left to right)
    left_clues = calculate_clues(grid)
    
    # Right clues (look from right to left)
    right_clues = calculate_clues(np.fliplr(grid))
    
    # Combine all clues into a single array
    clues = {
        'top': top_clues,
        'left': left_clues,
        'right': right_clues,
        'bottom': bottom_clues
    }
    
    return grid, clues


def generate(count, difficulty='medium', language='en', split="train"):
    prompt_template = PROMPT_TEMPLATE
    for i in tqdm(range(count)):
        dif_level = {"easy" : [3,4], "medium" : [5,6], "hard" : [7,8]}
        n_size = random.randint(dif_level[difficulty][0], dif_level[difficulty][1])
        grid, clues = generate_valid_skyscraper_data(n_size)
        grid = grid.tolist()
        clue_str = "\n".join([" ".join(map(str, clues["top"])), " ".join(map(str, clues["left"])), " ".join(map(str, clues["right"])), " ".join(map(str, clues["bottom"]))])
        prompt = prompt_template.format(question=clue_str)
        yield {
            "prompt": prompt,
            "answer":  grid,
            "task_name": "sum_skyscraper",    
            "ability": "logic_puzzle", 
            "language": language,
            "meta": json.dumps({
                "id":"sum_skyscraper_"+difficulty+str(i),
                "grid": grid,
                "grid_size":n_size,
                "question": clues,
                "answer": grid,
                "rationale": "", 
                "split": split,
                "type": "sequential_puzzle", 
                "source_url": "auto-generated", 
                "dataset_name": "sum_skyscraper", 
                "difficulty_level": difficulty,
                "language": language,
            }),
        }

def save_to_jsonl(output_file, count, lange='en'):
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in generate(count//3, 'easy', lange):
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
        for item in generate(count//3, 'medium', lange):
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
        for item in generate(count//3, 'hard', lange):
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

# Call functions to generate and save
#save_to_jsonl('../ss_en.jsonl', 31500, 'en')
#save_to_jsonl('../ss_zh.jsonl', 31500, 'zh')



