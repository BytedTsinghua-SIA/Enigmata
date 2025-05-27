import re
import json
import ast


def extract_code_block(text):
    code_blocks = re.findall(r'```.*?\n(.*?)```', text, re.DOTALL)
    if not code_blocks:
        code_blocks = re.findall(r'```(.*?)```', text, re.DOTALL)
    return code_blocks

def extract_result_from_code_block(text):
    """
    Extract results from the code block.
    """
    code_blocks = extract_code_block(text)
    if len(code_blocks) == 0:
        return None
    
    # Use the last code block
    content = code_blocks[-1].strip()
    
    # Check if it's a no solution message
    no_solution_markers = ["No valid solution"]
    if any(marker in content for marker in no_solution_markers):
        return {"no_solution": True}
    
    # Parse the number grid
    try:
        rows = content.strip().split("\n")
        grid = []
        for row in rows:
            if not row.strip():
                continue
            # Split numbers in the row, handling multiple spaces
            columns = row.split()
            # Convert each element to integer
            grid.append([int(cell) for cell in columns if cell.strip()])
        
        return {"matrix": grid}
    except:
        return None

def is_valid_binario(board):
    """
    Verify if a Binario solution follows the rules.
    """
    size = len(board)
    half_size = size // 2

    # Check if each row and column follows the rules
    def is_valid_unit(unit):
        return unit.count(0) <= half_size and unit.count(1) <= half_size and all(
            unit[i] != unit[i + 1] or unit[i + 1] != unit[i + 2]
            for i in range(len(unit) - 2)
        )

    # Verify all rows
    for row in board:
        if not is_valid_unit(row):
            return False

    # Verify all columns
    for col in zip(*board):
        if not is_valid_unit(list(col)):
            return False

    return True

def verify(pred, answer, meta):
    """
    Verify if the prediction is correct.
    """
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

    # Extract result from prediction
    result = extract_result_from_code_block(pred)
    if result is None:
        return 0  # Return 0 when no valid code block is found
    
    # Handle no solution case
    if "no_solution" in result:
        # Check if answer also indicates no solution
        if isinstance(answer, str) and "No valid solution" in answer:
            return 1
        return 0
    
    # If no valid matrix found
    if "matrix" not in result:
        return 0
    
    normalized_pred = result["matrix"]
    
    # Get initial puzzle state
    puzzle = meta["question"]
    if isinstance(puzzle, str):
        puzzle_array = []
        for line in puzzle.splitlines():
            if line.strip():
                row = [None if char == '_' else int(char) for char in line.split()]
                puzzle_array.append(row)
        puzzle = puzzle_array

    # Check if answer matches the puzzle
    try:
        for i in range(len(puzzle)):
            for j in range(len(puzzle[i])):
                if puzzle[i][j] is not None and puzzle[i][j] != normalized_pred[i][j]:
                    return 0

        # Verify if answer follows Binario rules
        if is_valid_binario(normalized_pred):
            return 1
        else:
            return 0
    except Exception:
        return 0
