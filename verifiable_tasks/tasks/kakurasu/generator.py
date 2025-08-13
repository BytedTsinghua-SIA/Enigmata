import random
import json
import hashlib
import random
import time
from tqdm import tqdm
from .template import PROMPT_TEMPLATE

CONFIGS = {
    "easy": [
        {"grid": 4, "black_rate": 0.3},
        {"grid": 5, "black_rate": 0.2}
    ],
    "medium": [
        {"grid": 5, "black_rate": 0.3},
        {"grid": 6, "black_rate": 0.2}
    ],
    "hard": [
        {"grid": 5, "black_rate": 0.4},
        {"grid": 6, "black_rate": 0.3}
    ]
}


PUZZLE_TYPE = "search_puzzle"
SOURCE_URL = "auto-generated"
DATASET_NAME = "kakurasu"


def string_to_md5(s):
    encoded_string = s.encode('utf-8')
    md5_hash = hashlib.md5()
    md5_hash.update(encoded_string)
    return md5_hash.hexdigest()


def solve_kakurasu(row_sums, col_sums, R, C, max_solutions=2):
    """
    Solve Kakurasu using backtracking and return all solutions that meet the conditions.
    If the number of solutions exceeds max_solutions, it can stop early (used to determine if solution is unique).
    
    Parameters:
    row_sums: list[int], length R, representing the target sum for each row
    col_sums: list[int], length C, representing the target sum for each column
    R, C: number of rows and columns in the board
    max_solutions: return early if more than this number of solutions are found, used to determine uniqueness
    
    Returns:
    solutions: list of solutions, where each solution is an R x C 2D boolean list,
               True indicates the cell is filled black, False indicates it's not filled.
    """
    solutions = []
    # board[r][c] = True/False indicates whether the cell is filled black
    board = [[False]*C for _ in range(R)]
    
    # Pre-calculate possible position weights for each row/column
    row_values = [[c+1 for c in range(C)] for _ in range(R)]
    col_values = [[r+1 for r in range(R)] for _ in range(C)]
    
    # For backtracking, keep track of current row/column sums
    current_row_sum = [0]*R
    current_col_sum = [0]*C
    
    def backtrack(cell_index=0):
        # If we've found too many solutions, stop early
        if len(solutions) >= max_solutions:
            return
        
        # If cell_index == R*C, we've traversed all cells
        if cell_index == R*C:
            # Check if all rows and columns meet target sums
            if all(current_row_sum[r] == row_sums[r] for r in range(R)) and \
               all(current_col_sum[c] == col_sums[c] for c in range(C)):
                # Make a copy of the solution
                solution = [row[:] for row in board]
                solutions.append(solution)
            return
        
        r = cell_index // C
        c = cell_index % C
        
        # Make two choices for the current cell: (1) not filled (False) (2) filled (True)
        
        # 1. Not filled
        board[r][c] = False
        backtrack(cell_index + 1)
        if len(solutions) >= max_solutions:
            return
        
        # 2. Filled (need to update row/column sums, then backtrack, and restore after backtracking)
        value_for_row = row_values[r][c]  # In row r, the column weight of the black cell
        value_for_col = col_values[c][r]  # In column c, the row weight of the black cell
        
        # Only try if adding this black cell won't exceed the expected row/column sums
        if current_row_sum[r] + value_for_row <= row_sums[r] and \
           current_col_sum[c] + value_for_col <= col_sums[c]:
            board[r][c] = True
            current_row_sum[r] += value_for_row
            current_col_sum[c] += value_for_col
            
            backtrack(cell_index + 1)
            
            # Backtrack
            board[r][c] = False
            current_row_sum[r] -= value_for_row
            current_col_sum[c] -= value_for_col
    
    backtrack(0)
    return solutions


def generate_question(row_sums, col_sums, language="en"):
    """
    Return generated row and column target sums and corresponding solutions based on input language.
    
    Returns:
    - Returns a string containing the board description, target sums, and black cell coordinates.
    """
    if row_sums is None:
        return "No valid solution exists within the given range, please increase max_tries or decrease difficulty."
    
    R = len(row_sums)
    C = len(col_sums)
    
    # Initialize return string
    result = ""


    result += f"Board size: {R} X {C}\n"
    result += f"Row sums: {row_sums}\n"
    result += f"Column sums: {col_sums}\n"
    return result

def generate_kakurasu_problem(language = "en", difficulty='easy', max_tries=500, ):
    """
    Automatically generate an R x C Kakurasu board and solution.
    
    Parameters:
    R, C: board size
    max_tries: maximum number of attempts to generate and verify a unique solution to avoid infinite loops
    difficulty: for example only, simply controls the random distribution based on number of black cells
    
    Returns:
    row_sums: list[int], target sum for each row
    col_sums: list[int], target sum for each column
    solution: R x C 2D boolean list (True indicates the cell is filled black)
    """
    # Based on difficulty, limit the "expected" number of black cells (for demonstration only, can be improved)
    
    # Based on difficulty, choose board configuration
    selected_config = random.choice(CONFIGS[difficulty])
    R = C = selected_config["grid"]
    black_rate = selected_config["black_rate"]
    
    for _ in range(max_tries):
        # Randomly generate a solution (boolean matrix)
        solution = []
        for r in range(R):
            row = []
            for c in range(C):
                # Choose whether to fill the cell with black_rate probability
                if random.random() < black_rate:
                    row.append(True)
                else:
                    row.append(False)
            solution.append(row)
        
        # Calculate row and column sums
        row_sums = [0]*R
        col_sums = [0]*C
        for r in range(R):
            for c in range(C):
                if solution[r][c]:
                    # In row r, column c is filled black, its weight in that row is c+1
                    row_sums[r] += (c+1)
                    # In column c, row r is filled black, its weight in that column is r+1
                    col_sums[c] += (r+1)
        
        # Verify uniqueness using backtracking
        solutions = solve_kakurasu(row_sums, col_sums, R, C, max_solutions=2)
        
        if len(solutions) == 1:
            # Unique solution, return result
            question = generate_question(row_sums, col_sums,language)
            black_cells = []
            for r in range(R):
                row_str = []
                for c in range(C):
                    if solution[r][c]:
                        black_cells.append((r+1, c+1))
            
            answer = list(black_cells)
            return {
                "question": question,
                "answer": answer,
                "difficulty_level": difficulty
            }
    # If max_tries is reached without finding a unique solution, return None
    return None

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
                problem = generate_kakurasu_problem(language, difficulty, max_tries=500)
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
