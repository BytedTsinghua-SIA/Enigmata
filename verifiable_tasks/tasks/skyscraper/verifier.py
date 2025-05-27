import re
import json
import numpy as np

import re
import ast

def extract_last_code_block(text: str):
    code_blocks = re.findall(r'```.*?\n(.*?)```', text, re.DOTALL)
    if not code_blocks:
        code_blocks = re.findall(r'```(.*?)```', text, re.DOTALL)
    return code_blocks[-1].strip() if code_blocks else None

def parse_answer(answer: str, delimiter: str = None):
    if not answer:
        return None
    rows = answer.split("\n")
    result = []
    
    for row in rows:
        row = row.strip()
        if not row:
            continue
        
        columns = row.split(delimiter) if delimiter else row.split()
        result.append([int(grid) if grid.strip().isdigit() else None for grid in columns])
    
    return result if all(None not in row for row in result) else None

def parse_list_str(input_string):
    try:
        return ast.literal_eval(input_string)
    except (ValueError, SyntaxError):
        return None

def preprocess_answer_to_matrix(raw_answer):
    if isinstance(raw_answer, list):
        return raw_answer
    
    answer = parse_answer(raw_answer, delimiter=None)
    if answer is None:
        answer = parse_answer(raw_answer, delimiter=',')
    if answer is None:
        answer = parse_list_str(raw_answer)
    
    return answer

def is_valid(board, top_clues, left_clues, right_clues, bottom_clues):
    n = len(board)
    if n != len(top_clues):
        return 0

    # Check each column against top and bottom clues
    for col in range(n):
        visible_from_top = visible_buildings(board[:, col])
        visible_from_bottom = visible_buildings(board[::-1, col])
        
        if top_clues[col] and visible_from_top != top_clues[col]:
            return False
        if bottom_clues[col] and visible_from_bottom != bottom_clues[col]:
            return False

    # Check each row against left and right clues
    for row in range(n):
        visible_from_left = visible_buildings(board[row, :])
        visible_from_right = visible_buildings(board[row, ::-1])
        
        if left_clues[row] and visible_from_left != left_clues[row]:
            return False
        if right_clues[row] and visible_from_right != right_clues[row]:
            return False
    
    return True

# Function to count visible buildings from a given direction
def visible_buildings(line):
    max_height = 0
    visible_count = 0
    for height in line:
        if height > max_height:
            visible_count += 1
            max_height = height
    return visible_count


def verify(pred, answer, meta):
    if isinstance(answer, str):
        try:
            answer = json.loads(answer)
        except json.JSONDecodeError:
            pass
    else:
        pass
    
    #meta = json.loads(meta) if isinstance(meta, str) else meta
    if isinstance(meta, str):
        meta = json.loads(meta)
    elif isinstance(meta, dict):
        pass
    else:
        raise ValueError('meta should be dict or str')
    lang = meta["language"]    
    pred = extract_last_code_block(pred)
    if pred is None:
        return 0
    normalized_pred = preprocess_answer_to_matrix(pred)
    if normalized_pred is None:
        return 0
    board = normalized_pred
    try:
        board = np.array(board)
    except Exception as ex:
        return 0
    top_clues = meta["question"]["top"]
    bottom_clues = meta["question"]["bottom"]
    left_clues = meta["question"]["left"]
    right_clues = meta["question"]["right"]
    try:
        if is_valid(board, top_clues, left_clues, right_clues, bottom_clues):
            return 1
        else:
            return 0
    except Exception as ex:
        return 0