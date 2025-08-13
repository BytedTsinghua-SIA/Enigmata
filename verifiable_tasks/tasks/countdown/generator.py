import random
from .template import PROMPT_TEMPLATE
from itertools import permutations, product
import json
from tqdm import tqdm

def generate_numbers(num_count, min_val=1, max_val=20):
    """Generate specified number of random digits"""
    return [random.randint(min_val, max_val) for _ in range(num_count)]

def generate_target(min_val=50, max_val=999):
    """Generate target number"""
    return random.randint(min_val, max_val)

operations = ['+', '-', '*', '/']

# Define error tolerance
EPSILON = 1e-6

# Try to calculate the value of an expression, avoiding division by zero and non-integer results
def safe_eval(exp): 
    try:
        result = eval(exp)
        # Check if it's an integer
        if result <= 0 or result != int(result):
            return None
        return int(result)
    except (ZeroDivisionError, ValueError):
        return None

def can_form_target(nums, target, lang='en'):
    """Check if the target number can be formed using the given numbers"""
    answer_cue = 'The answer is: '
    refuse_cue = f'cannot form {target}'
    
    # Try all possible number permutations
    for perm in permutations(nums):
        # Try all possible operator combinations
        for ops in product(operations, repeat=len(nums)-1):
            # Build expression elements
            elements = []
            for i in range(len(perm)-1):
                elements.append(str(perm[i]))
                elements.append(ops[i])
            elements.append(str(perm[-1]))
            
            # Generate all possible bracket combinations
            # Here we use a simplified method: try adding brackets before and after each operator
            expressions = [(''.join(elements), None)]  # Basic expression, no brackets
            
            for i in range(1, len(elements), 2):  # Iterate through all operator positions
                # Add left bracket before operator
                for j in range(i+2, len(elements), 2):  # Add right bracket after subsequent operators
                    if j < len(elements):
                        new_elements = elements.copy()
                        new_elements.insert(i-1, '(')
                        new_elements.insert(j+1, ')')
                        expressions.append((''.join(new_elements), None))
            
            # Evaluate all generated expressions
            for expr, _ in expressions:
                result = safe_eval(expr)
                if result == target:
                    return f"{answer_cue}{expr} = {target}"
    
    # If no solution is found, return cannot form
    return refuse_cue

def generate(count=100, difficulty='medium', language='en', split='train'):
    """Generate specified number of game instances with specified difficulty"""
    dic = {'easy': 5, 'medium': 6, 'hard': 7}
    num_count = dic[difficulty]
    prompt_template = PROMPT_TEMPLATE
    
    # Adjust number and target range based on difficulty
    if difficulty == 'easy':
        min_val, max_val = 1, 15
        target_min, target_max = 30, 100
    elif difficulty == 'medium':
        min_val, max_val = 1, 20
        target_min, target_max = 50, 200
    else:  # hard
        min_val, max_val = 1, 25
        target_min, target_max = 100, 500
    
    generated = 0
    attempts = 0
    max_attempts = count * 10  # Set maximum number of attempts
    
    with tqdm(total=count) as pbar:
        while generated < count and attempts < max_attempts:
            attempts += 1
            
            # Generate random numbers and target
            numbers = generate_numbers(num_count, min_val, max_val)
            target = generate_target(target_min, target_max)
            
            # Check if there is a solution
            answer = can_form_target(numbers, target, language)
            
            # Only keep instances with solutions
            if "cannot form" not in answer:
                numbers_str = ", ".join(map(str, numbers))
                
                yield {
                    "prompt": prompt_template.format(
                        num_count=num_count,
                        numbers=numbers_str,
                        target=target
                    ), 
                    "answer": answer,
                    "task_name": "countdown",    
                    "ability": "logic_puzzle", 
                    "language": language,
                    "meta": json.dumps({
                        "id": f"countdown_{difficulty}_{generated}", 
                        "question": numbers,
                        "target": target,
                        "answer": answer,
                        "rationale": "", 
                        "split": split,
                        "type": "code_puzzle", 
                        "source_url": "auto-generated", 
                        "dataset_name": "countdown", 
                        "difficulty_level": difficulty,
                        "language": language,
                    }),            
                }
                generated += 1
                pbar.update(1)
                pbar.set_description(f"Generated {generated}/{count} ({difficulty})")

def save_to_jsonl(output_file, count, language='en'):
    """
    Save generated instances to a jsonl file
    
    Parameters:
    - output_file: Output file path
    - count: Total number of instances to generate
    - language: Language ('en' or 'zh')
    """
    # Calculate number of instances to generate for each difficulty level
    per_difficulty = count // 3
    total_generated = 0
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # Generate and save easy difficulty
        print(f"Generating {per_difficulty} easy instances...")
        easy_count = 0
        for item in generate(per_difficulty, 'easy', language):
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
            easy_count += 1
            total_generated += 1
            if easy_count >= per_difficulty:
                break
                
        # Generate and save medium difficulty
        print(f"Generating {per_difficulty} medium instances...")
        medium_count = 0
        for item in generate(per_difficulty, 'medium', language):
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
            medium_count += 1
            total_generated += 1
            if medium_count >= per_difficulty:
                break
                
        # Generate and save hard difficulty
        print(f"Generating {per_difficulty} hard instances...")
        hard_count = 0
        for item in generate(per_difficulty, 'hard', language):
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
            hard_count += 1
            total_generated += 1
            if hard_count >= per_difficulty:
                break
        
        print(f"Generated: {easy_count} easy, {medium_count} medium, {hard_count} hard")
        print(f"Total generated: {total_generated}")

# Generate training and test data
def generate_train_test_data(train_count=24000, test_count=1500, languages=['en']):
    """
    Generate training and test data
    
    Parameters:
    - train_count: Number of training data
    - test_count: Number of test data
    - languages: List of languages
    """
    for lang in languages:
        # Create directories
        import os
        os.makedirs(f'training/countdown/{lang}', exist_ok=True)
        os.makedirs(f'eval/countdown/{lang}', exist_ok=True)
        
        # Generate training data
        print(f"Generating {train_count} training instances for {lang}...")
        save_to_jsonl(f'training/countdown/{lang}/train.jsonl', train_count, lang)
        
        # Generate test data
        print(f"Generating {test_count} test instances for {lang}...")
        save_to_jsonl(f'eval/countdown/{lang}/test.jsonl', test_count, lang)

if __name__ == "__main__":
    # Generate English data
    generate_train_test_data(train_count=24000, test_count=1500, languages=['en']) 