import re
import json

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
    
    # Check if it's an error message
    if content.startswith('"') and content.endswith('"'):
        # Remove quotes
        return {"answer": content.strip('"')}
    
    try:
        # Try to evaluate as a Python list
        result = eval(content)
        if isinstance(result, list):
            return {"answer": result}
    except:
        pass
    
    return None

def is_valid_hitori(board):
    """
    Verify if a hitori solution follows the rules.
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
            return 0

    # Verify all columns
    for col in zip(*board):
        if not is_valid_unit(list(col)):
            return 0

    return 1

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
    
    # Check if it's a "no valid solution" case
    no_solution_markers = ["No valid solution"]
    
    # Check if answer indicates no solution
    answer_str = str(answer) if isinstance(answer, (list, dict)) else answer
    answer_no_solution = any(marker in answer_str for marker in no_solution_markers)
    
    # Check if prediction indicates no solution
    result_str = str(result["answer"])
    result_no_solution = any(marker in result_str for marker in no_solution_markers)
    
    # If answer indicates no solution and prediction also indicates no solution, it's correct
    if answer_no_solution and result_no_solution:
        return 1
    # If answer indicates no solution but prediction doesn't, it's wrong
    elif answer_no_solution and not result_no_solution:
        return 0
    # If answer doesn't indicate no solution but prediction does, it's wrong
    elif not answer_no_solution and result_no_solution:
        return 0
    
    # Handle the case where there is a solution
    if not isinstance(result["answer"], list):
        return 0
    
    # Normalize coordinate format and compare
    try:
        # Normalize prediction results to a set of tuples
        pred_coords = set()
        for coord in result["answer"]:
            if isinstance(coord, tuple):
                # Tuple format (x, y)
                pred_coords.add(coord)
            elif isinstance(coord, list):
                # List format [x, y]
                pred_coords.add(tuple(coord))
            else:
                return 0  # Invalid format
        
        # Normalize answer to a set of tuples
        answer_coords = set()
        for coord in answer:
            if isinstance(coord, tuple):
                answer_coords.add(coord)
            elif isinstance(coord, list):
                answer_coords.add(tuple(coord))
            else:
                return 0  # Invalid format
        
        # Directly compare if sets are equal
        return int(pred_coords == answer_coords)
    except:
        return 0  # Return 0 if any error occurs during processing
