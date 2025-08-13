import random
import copy
import collections
import json
import numpy as np
from tqdm import tqdm
from .template import PROMPT_TEMPLATE


def siamese_method_magic_square(n=3):
    if n % 2 == 0:
        raise ValueError("Siamese method only works for odd n")
    
    magic_square = np.zeros((n, n), dtype=int)

    num = 1
    i, j = 0, n // 2  # Start from the middle column of the first row

    while num <= n**2:
        magic_square[i, j] = num
        num += 1
        new_i, new_j = (i - 1) % n, (j + 1) % n  # Move to the upper right cell

        if magic_square[new_i, new_j]:  # If the cell is already filled, move to the cell below the current one
            i = (i + 1) % n
        else:
            i, j = new_i, new_j

    return magic_square

def shuffle_magic_square(square):
    n = square.shape[0]

    # Randomly rotate 90, 180, or 270 degrees
    if random.choice([True, True, True, False]):
        k = random.choice([1, 2, 3])
        square = np.rot90(square, k=k)
    
    # Randomly flip along the main diagonal or anti-diagonal
    if random.choice([True, False]):
        if random.choice([True, False]):
            square = np.transpose(square)  # Flip along the main diagonal
        else:
            square = np.fliplr(np.transpose(np.fliplr(square)))  # Flip along the anti-diagonal

    return square

def siamese_method_magic_square(n=3):
    if n % 2 == 0:
        raise ValueError("Siamese method only works for odd n")
    
    magic_square = np.zeros((n, n), dtype=int)

    num = 1
    i, j = 0, n // 2  # Start from the middle column of the first row

    while num <= n**2:
        magic_square[i, j] = num
        num += 1
        new_i, new_j = (i - 1) % n, (j + 1) % n  # Move to the upper right cell

        if magic_square[new_i, new_j]:  # If the cell is already filled, move to the cell below the current one
            i = (i + 1) % n
        else:
            i, j = new_i, new_j

    return magic_square

def apply_arithmetic_sequence(square, a, d):
    """
    Map the magic square values to an arithmetic sequence, where a is the first term and d is the common difference.
    """
    n = square.shape[0]
    # Apply linear transformation to map 1-9 to an arithmetic sequence
    new_square = a + (square - 1) * d
    return new_square

def puzzle_to_string(board):
    puzzle_str = ""
    for row in board:
        puzzle_str += " ".join(str(num) if num != None else "." for num in row) + "\n"
    return puzzle_str


def shuffle_magic_square(square):
    n = square.shape[0]

    # Randomly rotate 90, 180, or 270 degrees
    if random.choice([True, False]):
        k = random.choice([1, 2, 3])
        square = np.rot90(square, k=k)
    
    # Randomly flip along the main diagonal or anti-diagonal
    if random.choice([True, False]):
        if random.choice([True, False]):
            square = np.transpose(square)  # Flip along the main diagonal
        else:
            square = np.fliplr(np.transpose(np.fliplr(square)))  # Flip along the anti-diagonal
    
    return square


def generate(count , difficulty='naive', language='en', split="train"):
    prompt_template = PROMPT_TEMPLATE
    
    for i in tqdm(range(count)):

        # Generate standard 3x3 magic square
        magic_square = siamese_method_magic_square(3)

        # Randomly generate first term and common difference for arithmetic sequence
        a = random.randint(-25, 25)  # Random first term
        d = random.randint(1, 10)  # Random common difference

        # Map to random arithmetic sequence
        arithmetic_magic_square = apply_arithmetic_sequence(magic_square, a, d)

        # Apply random transformations to the arithmetic magic square
        random_arithmetic_magic_square = shuffle_magic_square(arithmetic_magic_square)

        answer=random_arithmetic_magic_square.tolist()
        puzzle = copy.deepcopy(answer)
        # random mask 4~7 of them
        
        ids=[0,1,2,3,4,5,6,7,8]
        dif_level = {"easy" : [2,3], "medium" : [4,5], "hard" : [6,7]}
        lo, hi = dif_level[difficulty][0], dif_level[difficulty][1]
        
        random.shuffle(ids)
        mask_ids=ids[:random.randint(lo, hi)]
        for id in mask_ids:
            puzzle[id//3][id%3]=None

        puzzle_str = puzzle_to_string(puzzle)

        yield {
            "prompt": prompt_template.format(question=puzzle_str),
            "answer":  answer,
            "task_name": "magic_square",    
            "ability": "logic_puzzle", 
            "language": language,
            "meta": {
                "id":"magic_square_"+difficulty+'_'+str(i),
                "question": puzzle,
                "masks": len(mask_ids),
                "answer": answer,
                "rationale": "", 
                "split": split,
                "type": "sudoku_puzzle", 
                "source_url": "auto-generated", 
                "dataset_name": "magic_square", 
                "difficulty_level": difficulty,
                "language": language,
            },
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
#save_to_jsonl('../eval.jsonl', 31500, 'en')
#save_to_jsonl('../ms_zh.jsonl', 31500, 'zh')