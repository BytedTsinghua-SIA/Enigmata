import json
import random
import hashlib
import time
from copy import deepcopy
from tqdm import tqdm
from .template import PROMPT_TEMPLATE

CONFIGS = {
    "easy": [
        {"size": 4, "mask_rate": 0.2, "min_filled_cells": 12},  # Configuration 1
        {"size": 6, "mask_rate": 0.1, "min_filled_cells": 24},  # Configuration 2
    ],
    "medium": [
        {"size": 4, "mask_rate": 0.3, "min_filled_cells": 10},  # Configuration 1
        {"size": 6, "mask_rate": 0.2, "min_filled_cells": 20},  # Configuration 2
    ],
    "hard": [
        {"size": 6, "mask_rate": 0.3, "min_filled_cells": 24},  # Configuration 1
        {"size": 8, "mask_rate": 0.2, "min_filled_cells": 40},  # Configuration 2
    ],
}

PUZZLE_TYPE = "PUZZLE"
SOURCE_URL = "auto-generated"
DATASET_NAME = "binario"

def string_to_md5(s):
    encoded_string = s.encode('utf-8')
    md5_hash = hashlib.md5()
    md5_hash.update(encoded_string)
    return md5_hash.hexdigest()

def is_valid_puzzle(grid):
    size = len(grid)
    half_size = size // 2

    for i in range(size):
        row = grid[i]
        col = [grid[j][i] for j in range(size)]

        if row.count(0) > half_size or row.count(1) > half_size:
            return False
        if col.count(0) > half_size or col.count(1) > half_size:
            return False

        for j in range(size - 2):
            if row[j] == row[j+1] == row[j+2]:
                return False
            if col[j] == col[j+1] == col[j+2]:
                return False

    return True

def is_valid_puzzle_partial(grid, row, col):
    size = len(grid)
    half_size = size // 2

    current_row = grid[row]
    current_col = [grid[r][col] for r in range(size)]

    row_counts = {0: 0, 1: 0}
    col_counts = {0: 0, 1: 0}
    for cell in current_row:
        if cell is not None:
            row_counts[cell] += 1
    for cell in current_col:
        if cell is not None:
            col_counts[cell] += 1

    if row_counts[0] > half_size or row_counts[1] > half_size:
        return False
    if col_counts[0] > half_size or col_counts[1] > half_size:
        return False

    for j in range(max(0, col - 2), min(col + 1, size - 2)):
        window = current_row[j:j+3]
        if window.count(window[0]) == 3 and window[0] is not None:
            return False

    for j in range(max(0, row - 2), min(row + 1, size - 2)):
        window = [grid[j+k][col] for k in range(3)]
        if window.count(window[0]) == 3 and window[0] is not None:
            return False

    return True

def has_unique_solution(grid):
    solutions = []
    size = len(grid)
    max_solutions = 2  

    def solve(current_grid, row, col):
        if len(solutions) >= max_solutions:
            return
        if row == size:
            solutions.append(deepcopy(current_grid))
            return
        next_row, next_col = (row, col + 1) if col + 1 < size else (row + 1, 0)
        if current_grid[row][col] is not None:
            solve(current_grid, next_row, next_col)
        else:
            for value in [0, 1]:
                current_grid[row][col] = value
                if is_valid_puzzle_partial(current_grid, row, col):
                    solve(current_grid, next_row, next_col)
                if len(solutions) >= max_solutions:
                    break
            current_grid[row][col] = None

    solve(deepcopy(grid), 0, 0)
    return len(solutions) == 1

def generate_complete_grid(size):
    grid = [[None for _ in range(size)] for _ in range(size)]
    half_size = size // 2

    def backtrack(r, c):
        if r == size:
            return True
        next_r, next_c = (r, c + 1) if c + 1 < size else (r + 1, 0)
        for val in [0, 1]:
            grid[r][c] = val

            row = grid[r]
            col = [grid[i][c] for i in range(size)]
            if row.count(val) > half_size or col.count(val) > half_size:
                grid[r][c] = None
                continue

            valid = True
            for j in range(max(0, c - 2), min(c + 1, size - 2)):
                window = row[j:j+3]
                if window.count(val) == 3:
                    valid = False
                    break
            if not valid:
                grid[r][c] = None
                continue

            for i in range(max(0, r - 2), min(r + 1, size - 2)):
                window = [grid[i+k][c] for k in range(3)]
                if window.count(val) == 3:
                    valid = False
                    break
            if not valid:
                grid[r][c] = None
                continue

            if backtrack(next_r, next_c):
                return True

            grid[r][c] = None

        return False

    if backtrack(0, 0):
        return grid
    else:
        return None
    
def get_random_config(difficulty):
    config_options = CONFIGS[difficulty]  
    return random.choice(config_options)  

def generate_binario_problem(language, difficulty):
    config = get_random_config(difficulty)
    size, mask_rate, min_filled_cells = config["size"], config["mask_rate"], config["min_filled_cells"]

    attempts = 0
    max_attempts = 1000
    while attempts < max_attempts:
        grid = generate_complete_grid(size)
        if grid and is_valid_puzzle(grid) and has_unique_solution(grid):
            break
        attempts += 1
    else:
        raise ValueError("Unable to generate a complete solution that meets the criteria. Please check the rules or adjust the configuration.")

    attempts = 0
    while attempts < max_attempts:
        masked_grid = [[cell if random.random() > mask_rate else None for cell in row] for row in grid]
        filled_cells = sum(cell is not None for row in masked_grid for cell in row)
        if filled_cells >= min_filled_cells and has_unique_solution(masked_grid):
            break
        attempts += 1
    else:
        raise ValueError("Unable to generate a puzzle with holes that meets the criteria. Please check the rules or adjust the configuration.")

    question = '\n'.join([' '.join(['_' if cell is None else str(cell) for cell in row]) for row in masked_grid])
    answer = '\n'.join([' '.join(map(str, row)) for row in grid])

    return {
        "question": question,
        "answer": answer,
        "difficulty_level": difficulty,
    }

def transform_problem_to_meta(problem, idx, language, split):
    timestamp = str(time.time())
    random_suffix = random.randint(0, int(1e6))
    id_string = f"binario_{idx}_{timestamp}_{random_suffix}"
    hash_id_string = string_to_md5(id_string)
    return {
        "id": hash_id_string,
        "question": problem["question"],
        "answer": problem["answer"],
        "rationale": "",
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
            while True:
                problem = generate_binario_problem(language, difficulty)
                if problem: break
            meta = transform_problem_to_meta(problem, generated, language, split)
            meta["task_name"] = DATASET_NAME
            yield {
                "prompt": prompt_template.format(question=meta["question"]),
                "answer": meta["answer"],
                "task_name": DATASET_NAME,
                "ability": PUZZLE_TYPE,
                "language": language,
                "meta": json.dumps(meta, ensure_ascii=False),
            }
            generated += 1
        except ValueError as e:
            print(f"Generation error: {e}")
        attempts += 1

    if attempts >= max_attempts:
        print(f"Warning: Maximum attempt count reached, generated {generated} / {count} puzzles.")

def save_to_jsonl(output_file, count, language, split):
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
            print(f"Generating {difficulty} puzzles: {num} puzzles")
            for item in tqdm(generate(num, difficulty=difficulty, language=language, split=split), desc=f"Generating {difficulty} puzzles"):
                f.write(json.dumps(item, ensure_ascii=False) + '\n')

if __name__ == "__main__":
    save_to_jsonl("train_en.jsonl", 20000, language="en", split="train")
    save_to_jsonl("test_en.jsonl", 1500, language="en", split="eval")
