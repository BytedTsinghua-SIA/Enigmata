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



# Movement direction offsets
moves = {
    'L': (0, -1),   # Move left (tile to the right of empty space moves left)
    'R': (0, 1),    # Move right (tile to the left of empty space moves right)
    'U': (-1, 0),   # Move up (tile below the empty space moves up)
    'D': (1, 0)     # Move down (tile above the empty space moves down)
}


# Find the position of the empty tile
def find_empty_tile(board):
    K = len(board)
    for i in range(K):
        for j in range(K):
            if board[i][j] == 0:
                return i, j


# Test function
def can_solve_puzzle(board, move_sequence, lang):
    board_copy = [row[:] for row in board]  # Create a copy of the initial board
    K = len(board)
    goal_state = [[(i * K + j + 1) % (K * K) for j in range(K)] for i in range(K)]
    #print(board, goal_state)
    empty_row, empty_col = find_empty_tile(board_copy)
    
    for move in move_sequence:
        if move in moves:
            new_row = empty_row + moves[move][0]
            new_col = empty_col + moves[move][1]

            # Check if out of bounds
            if 0 <= new_row < K and 0 <= new_col < K:
                # Swap the empty space and the tile at the new position
                board_copy[empty_row][empty_col], board_copy[new_row][new_col] = board_copy[new_row][new_col], board_copy[empty_row][empty_col]
                # Update empty space position
                empty_row, empty_col = new_row, new_col
            else:
                print('Out of the line')
                return False  # Return failure if out of bounds

    return board_copy == goal_state  # Check if goal state is reached

def verify(pred, answer, meta):
    if isinstance(answer, str):
        try:
            answer = json.loads(answer)
        except json.JSONDecodeError:
            pass
    else:
        pass
    
    if isinstance(meta, str):
        meta = json.loads(meta)
    elif isinstance(meta, dict):
        pass
    else:
        raise ValueError('meta should be dict or str')
        
    lang = meta['language']
    
    final_answer = extract_last_code_block(pred)
    if not final_answer:
        return 0
    if "No feasible" in answer:
        if not isinstance(final_answer, str):
            return 0
        if "No feasible" in final_answer:
            return 1
        return 0
    
    sequence = final_answer
    board = meta["question"]
    #print(sequence, board)
    try:
        result = int(can_solve_puzzle(board, sequence, lang))
        return result
    except Exception as ex:
        return 0