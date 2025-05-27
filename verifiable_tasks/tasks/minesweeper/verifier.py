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
    
    # Check if it's an "unable to determine any mine positions" case
    unable_markers = ["Unable to determine"]
    
    # Check if answer indicates inability to determine
    answer_str = str(answer) if isinstance(answer, (list, dict)) else answer
    answer_unable = any(marker in answer_str for marker in unable_markers)
    
    # Check if prediction indicates inability to determine
    result_str = str(result["answer"])
    result_unable = any(marker in result_str for marker in unable_markers)
    
    # If answer indicates inability to determine and prediction also indicates inability to determine, it's correct
    if answer_unable and result_unable:
        return 1
    # If answer indicates inability to determine but prediction doesn't, it's wrong
    elif answer_unable and not result_unable:
        return 0
    # If answer doesn't indicate inability to determine but prediction does, it's wrong
    elif not answer_unable and result_unable:
        return 0
    
    # Handle the case where there are mine positions
    if not isinstance(result["answer"], list):
        return 0
    
    # Normalize coordinate format to a set of tuples
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
