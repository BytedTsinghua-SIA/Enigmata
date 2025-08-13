import random
import copy
import collections
import json
import numpy as np
from .template import PROMPT_TEMPLATE


def rotate(board, rotation):
    i,j=rotation
    t=board[i][j]
    board[i][j]=board[i+1][j]
    board[i+1][j]=board[i+1][j+1]
    board[i+1][j+1]=board[i][j+1]
    board[i][j+1]=t
    return board

def puzzle_to_string(board):
    puzzle_str = ""
    for row in board:
        puzzle_str += " ".join(str(num) if num != 0 else "." for num in row) + "\n"
    return puzzle_str

# generate a twiddle puzzle
# 1. generate a original 3*3 grid
# 2. rotate randomly for many times
def generate(count, difficulty='medium', language='en', split="train"):
    prompt_template = PROMPT_TEMPLATE
    
    for i in range(count):
        board = [[1,2,3],[4,5,6],[7,8,9]]
        rotations=[[0,0],[0,1],[1,0],[1,1]]
        answer = []
        dif_level = {"easy" : [1,2], "medium" : [3,4], "hard" : [5,6]}
        ramdom_rotations =  random.randint(dif_level[difficulty][0], dif_level[difficulty][1])
        for _ in range(ramdom_rotations):
            rotation = random.choice(rotations)
            board = rotate(board, rotation)
            answer.append(rotation)

        answer = answer[::-1]
        puzzle_str = puzzle_to_string(board)
        yield {
            "prompt": prompt_template.format(question=puzzle_str),
            "answer":  answer,
            "task_name": "twiddle",    
            "ability": "logic_puzzle", 
            "language": language,
            "meta": json.dumps({
                "id":"twiddle_"+difficulty+'_'+str(i),
                "question": board,
                "answer": answer,
                "rotations":ramdom_rotations,
                "rationale": "", 
                "split": split,
                "type": "spatial_puzzle", 
                "source_url": "auto-generated", 
                "dataset_name": "twiddle", 
                "difficulty_level": difficulty,
                "language": language,
            }),
        }

def save_to_jsonl(output_file, count, lange='en'):
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in generate(count//3, 'easy', lange):
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
        for item in generate(count-2*count//3+1, 'medium', lange):
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
        for item in generate(count//3, 'hard', lange):
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
