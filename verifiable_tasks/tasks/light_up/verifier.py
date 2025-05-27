import re

def extract_code_block(text):
    code_blocks = re.findall(r'```.*?\n(.*?)```', text, re.DOTALL)
    if not code_blocks:
        code_blocks = re.findall(r'```(.*?)```', text, re.DOTALL)
    return code_blocks

def extract_coordinates(text):
    """
    Extract a list of coordinates from the code block in the given text.
    """
    code_blocks = extract_code_block(text)
    
    if not code_blocks:
        return None
    
    # Use the last code block
    result = code_blocks[-1].strip()
    
    # Check if it's a no-solution case
    if "No solution" in result or "no solution" in result:
        return "No solution"
    
    try:
        # Try to evaluate the coordinate list string as a Python object
        # Note: eval has security risks, only used here for verification
        coords = eval(result)
        if isinstance(coords, list):
            return coords
    except:
        return None
    
    return None

def verify(pred, answer, meta):
    """
    Verify if the prediction is correct.
    """
    # Extract coordinate list from prediction
    pred_coords = extract_coordinates(pred)
    
    if pred_coords is None:
        return 0  # No valid coordinate list found
    
    # Handle no-solution case
    if pred_coords == "No solution" and isinstance(answer, str) and "No solution" in answer:
        return 1
    
    # Ensure answer is in list format
    if isinstance(answer, str):
        if "No solution" in answer:
            return 0  # Prediction has a solution but answer doesn't
        try:
            # Try to convert string to list
            import json
            answer = json.loads(answer)
        except:
            return 0
    
    # Check if prediction format is correct
    if not isinstance(pred_coords, list):
        return 0
    
    # Compare by sorting each coordinate and using set comparison
    # Convert tuples in prediction to lists for comparison with answer
    pred_coords_lists = [list(coord) if isinstance(coord, tuple) else coord for coord in pred_coords]
    
    # Sort coordinates for comparison
    sorted_pred = sorted([tuple(coord) for coord in pred_coords_lists])
    sorted_answer = sorted([tuple(coord) for coord in answer])

    return int(sorted_pred == sorted_answer)