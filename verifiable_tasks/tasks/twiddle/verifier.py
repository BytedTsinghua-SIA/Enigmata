import re
import json

# Helper function to rotate a 2x2 region counterclockwise
def rotate_counterclockwise(board, rotation):
    i, j = rotation
    t = board[i][j]
    board[i][j] = board[i][j+1]
    board[i][j+1] = board[i+1][j+1]
    board[i+1][j+1] = board[i+1][j]
    board[i+1][j] = t
    return board

# Helper function to check if the current board is the target state
def is_solved(board):
    target = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    return board == target

def parse_rotation(pred):
    '''
    Parse rotation sequence like (1,0)->(0,1)->(1,1)
    '''
    pattern = r"\((\d),(\d)\)"
    return [(int(m[0]), int(m[1])) for m in re.findall(pattern, pred)]

def extract_last_code_block(text: str):
    """Extract the content of the last code block from the text."""
    code_blocks = re.findall(r'```.*?\n(.*?)```', text, re.DOTALL)
    if not code_blocks:
        code_blocks = re.findall(r'```(.*?)```', text, re.DOTALL)
    return code_blocks[-1].strip() if code_blocks else None

# Twiddle verifier
def verify(pred, answer, meta):
    """
    Verify if the prediction solves the twiddle puzzle correctly.
    
    Args:
        pred: The prediction containing the rotation sequence
        answer: The expected answer
        meta: Metadata containing the initial puzzle state and other information
        
    Returns:
        1 if the prediction correctly solves the puzzle, 0 otherwise
    """
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
    lang = meta["language"]

    # Extract the rotation sequence from the prediction
    pred = extract_last_code_block(pred)
    if pred is None:
        return 0
    pred = pred.replace(" ", "")
    rotation_sequence = parse_rotation(pred)
    
    # Validate that all rotations are within bounds
    for i, j in rotation_sequence:
        if i not in [0, 1] or j not in [0, 1]:
            return 0
        
    puzzle = meta["question"]

    # Apply each rotation to the puzzle
    for move in rotation_sequence:
        i, j = move
        puzzle = rotate_counterclockwise(puzzle, (i, j))
        
    # Check if the puzzle is solved
    if is_solved(puzzle):
        return 1
    else:
        return 0
