import random
import collections
import json
from tqdm import tqdm
import copy
from .template import PROMPT_TEMPLATE


# Generate complete sudoku
def generate_full_sudoku():
    base  = 3
    side  = base * base

    # pattern for a baseline valid solution
    def pattern(r, c): return (base*(r%base)+r//base+c)%side

    # randomize rows, columns and numbers (1-9)
    def shuffle(s): return random.sample(s, len(s))
    rBase = range(base)
    rows  = [g*base + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols  = [g*base + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums  = shuffle(range(1, base*base+1))

    # produce board using randomized baseline pattern
    board = [[nums[pattern(r, c)] for c in cols] for r in rows]

    return board

# Remove some numbers from the complete sudoku to create a puzzle
def remove_numbers_from_board(board, holes=40):
    side = len(board)
    out = copy.deepcopy(board)
    squares = side * side
    empties = set(random.sample(range(squares), holes))
    
    for i in range(side):
        for j in range(side):
            if i * side + j in empties:
                out[i][j] = 0  # Use 0 to represent empty cells

    return out

# Print sudoku
def sudoku_to_string(board):
    sudoku_str = ""
    for row in board:
        sudoku_str += " ".join(str(num) if num != 0 else "." for num in row) + "\n"
    return sudoku_str


# Example: Generate a sudoku and display it
def generate(count, difficulty='medium', language='en', split="train"):
    prompt_template = PROMPT_TEMPLATE
    
    dif_level = {"easy" : [10,20], "medium" : [20,35], "hard" : [35,50]}
    lo, hi = dif_level[difficulty][0], dif_level[difficulty][1]

    for i in tqdm(range(count)):
        board = generate_full_sudoku()
        holes = random.randint(lo, hi)
        puzzle = remove_numbers_from_board(board, holes)
        puzzle_str = sudoku_to_string(puzzle)
        yield {
            "prompt": prompt_template.format(question=puzzle_str),
            "answer":  board,
            "task_name": "sudoku",    
            "ability": "logic_puzzle", 
            "language": language,
            "meta": json.dumps({
                "id":"sudoku_"+difficulty+'_'+str(i),
                "question": puzzle,
                "holes":holes,
                "answer": board,
                "rationale": "", 
                "split": split,
                "type": "sudoku_puzzle", 
                "source_url": "auto-generated", 
                "dataset_name": "sudoku", 
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
#save_to_jsonl('../sudoku_en.jsonl', 31500, 'en')
#save_to_jsonl('../sudoku_zh.jsonl', 31500, 'zh')