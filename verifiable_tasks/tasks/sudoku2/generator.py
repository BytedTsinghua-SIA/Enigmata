import random
import collections
import json
from tqdm import tqdm
import copy
from .template import PROMPT_TEMPLATE


# Generate complete Sudoku
def generate_full_sudoku():
    base  = 2
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

# Remove numbers from the board to create a puzzle
def remove_numbers_from_board(board, holes=40):
    side = len(board)
    out = copy.deepcopy(board)
    squares = side * side
    empties = set(random.sample(range(squares), holes))
    
    for i in range(side):
        for j in range(side):
            if i * side + j in empties:
                out[i][j] = 0  # 0 represents an empty cell

    return out

# Print Sudoku
def sudoku_to_string(board):
    sudoku_str = ""
    for row in board:
        sudoku_str += " ".join(str(num) if num != 0 else "." for num in row) + "\n"
    return sudoku_str


# Example: Generate a Sudoku and display it
def generate(count, difficulty='medium', language='en', split="train"):
    prompt_template = PROMPT_TEMPLATE
    
    dif_level = {"easy" : [4,5], "medium" : [6,7], "hard" : [8,9]}
    lo, hi = dif_level[difficulty][0], dif_level[difficulty][1]

    for i in tqdm(range(count)):
        board = generate_full_sudoku()
        holes = random.randint(lo, hi)
        puzzle = remove_numbers_from_board(board, holes)
        puzzle_str = sudoku_to_string(puzzle)
        yield {
            "prompt": prompt_template.format(question=puzzle_str),
            "answer":  board,
            "task_name": "sudoku2",    
            "ability": "logic_puzzle", 
            "language": language,
            "meta": {
                "id":"sudoku2_"+difficulty+'_'+str(i),
                "question": puzzle,
                "holes":holes,
                "answer": board,
                "rationale": "", 
                "split": split,
                "type": "sudoku_puzzle", 
                "source_url": "auto-generated", 
                "dataset_name": "sudoku2", 
                "difficulty_level": difficulty,
                "language": language,
            },
        }

def save_to_jsonl(of1, of2, count, lange='en'):
    with open(of1, 'w', encoding='utf-8') as f1, open(of2, 'w', encoding='utf-8') as f2:
        for item in generate(count//3, 'easy', lange):
            f1.write(json.dumps(item, ensure_ascii=False) + '\n')
            f2.write(json.dumps(item["meta"], ensure_ascii=False) + '\n')
        for item in generate(count//3, 'medium', lange):
            f1.write(json.dumps(item, ensure_ascii=False) + '\n')
            f2.write(json.dumps(item["meta"], ensure_ascii=False) + '\n')
        for item in generate(count//3, 'hard', lange):
            f1.write(json.dumps(item, ensure_ascii=False) + '\n')
            f2.write(json.dumps(item["meta"], ensure_ascii=False) + '\n')

# Call functions to generate and save
#save_to_jsonl('training/sudoku2/en/train.jsonl', 'raw/sudoku2/en/train.jsonl', 24000, 'en')
#save_to_jsonl('eval/sudoku2/en/test.jsonl', 'raw/sudoku2/en/test.jsonl', 1500, 'en')
