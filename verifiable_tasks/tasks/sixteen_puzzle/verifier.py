import re
import json

def extract_code_block(text):
    code_blocks = re.findall(r'```.*?\n(.*?)```', text, re.DOTALL)
    if not code_blocks:
        code_blocks = re.findall(r'```(.*?)```', text, re.DOTALL)
    return code_blocks

def extract_result_from_code_block(text):
    """Extract results from code block"""
    code_blocks = extract_code_block(text)
    if len(code_blocks) == 0:
        return None
    
    # Use the last code block
    content = code_blocks[-1].strip()
    
    # Check if it's an error message
    if content.startswith('"') and content.endswith('"'):
        # Remove quotes
        return {"answer": content.strip('"')}
    
    try:
        # Try to evaluate as Python list
        result = eval(content)
        if isinstance(result, list):
            return {"answer": result}
    except:
        pass
    
    return None

def can_move(board, moves, lang):
    K = len(board)
    goal_state = tuple(i for i in range(1, K*K+1))

    # Define a function to execute moves
    def apply_move(state, move, lang):
        state = list(state)
        move_type = move[0]
        row_or_col = int(move[1]) - 1  # Adjust index to start from 0
        steps = int(move[2]) % K       # Moving K steps equals not moving
        if steps == 0:
            return tuple(state)
        if move_type == 'R':
            idx = row_or_col * K
            row = state[idx:idx+K]
            # Circular shift of row
            row = row[steps:] + row[:steps]
            state[idx:idx+K] = row
        elif move_type == 'C':
            col = state[row_or_col::K]
            # Circular shift of column
            col = col[steps:] + col[:steps]
            state[row_or_col::K] = col
        else:
            print(f"Out of the boundary: {move}")
            return False  # Return failure if out of bounds
        return tuple(state)

    # Check the given path
    def verify_path(start_state, moves):
        current_state = start_state
        for move in moves:
            current_state = apply_move(current_state, move, lang)
            if current_state is False:  # If the move is invalid
                return False
        return current_state == goal_state

    flat_board = []
    for line in board:
        for item in line:
            flat_board.append(item)
    return verify_path(tuple(flat_board), moves)

def verify(pred, answer, meta):
    if isinstance(answer, str):
        try:
            answer = json.loads(answer)
        except json.JSONDecodeError:
            pass
    
    if isinstance(meta, str):
        meta = json.loads(meta)
    elif isinstance(meta, dict):
        pass
    else:
        raise ValueError('meta should be dict or str')
    
    lang = meta['language']
    
    # Extract results from prediction using the new code block extraction function
    result = extract_result_from_code_block(pred)
    if result is None:
        return 0
    
    # Check for no valid move sequence case
    invalid_markers = ["No valid sequence", "not exist"]
    
    # Check if the answer indicates no valid moves
    answer_str = str(answer) if isinstance(answer, (list, dict)) else answer
    answer_invalid = any(marker.lower() in answer_str.lower() for marker in invalid_markers)
    
    # Check if the prediction indicates no valid moves
    result_str = str(result["answer"])
    result_invalid = any(marker.lower() in result_str.lower() for marker in invalid_markers)
    
    # If answer indicates no valid moves and prediction also indicates no valid moves, it's correct
    if answer_invalid and result_invalid:
        return 1
    # If answer indicates no valid moves but prediction indicates valid moves, it's wrong
    elif answer_invalid and not result_invalid:
        return 0
    # If answer indicates valid moves but prediction indicates no valid moves, it's wrong
    elif not answer_invalid and result_invalid:
        return 0
    
    # Handle the case of valid move sequences
    moves = result["answer"]
    if not isinstance(moves, list):
        return 0
    
    board = meta["question"]
    try:
        result = int(can_move(board, moves, lang))
        return result
    except Exception:
        return 0