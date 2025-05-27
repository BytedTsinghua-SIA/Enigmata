import re
import json
import re
def extract_last_code_block(text: str):
    code_blocks = re.findall(r'```.*?\n(.*?)```', text, re.DOTALL)
    if not code_blocks:
        code_blocks = re.findall(r'```(.*?)```', text, re.DOTALL)
    return code_blocks[-1].strip() if code_blocks else None

def calculate_switches(car_order, colors):
    """
    Calculate the number of color switches in a given car order
    
    Parameters:
    - car_order: List of car IDs
    - colors: List of colors corresponding to each car
    
    Returns:
    - Number of color switches
    """
    if not car_order:
        return 0
    
    switches = 0
    for i in range(1, len(car_order)):
        current_car = car_order[i]
        prev_car = car_order[i-1]
        # Car IDs start from 1, but list indices start from 0, so subtract 1
        if colors[current_car-1] != colors[prev_car-1]:
            switches += 1
    
    return switches

def is_valid_car_order(car_order, original_car_ids, K):
    """
    Check if the car order is valid
    
    Parameters:
    - car_order: Car ID order output by the model
    - original_car_ids: Original car ID order
    - K: Maximum allowed movement range
    
    Returns:
    - Boolean indicating validity, and optional error message
    """
    # Check if all cars are included and there are no duplicates
    if sorted(car_order) != sorted(original_car_ids):
        return False, "Car list contains duplicates or missing cars"
    
    # Check if each car's position is within the allowed range
    for new_pos, car_id in enumerate(car_order):
        # Car IDs and positions are 1-indexed
        new_pos += 1
        # Get the car's position in the original order
        original_pos = original_car_ids.index(car_id) + 1
        # Check if the movement is within the allowed range
        if abs(new_pos - original_pos) > K:
            return False, f"Car {car_id} moved from position {original_pos} to {new_pos}, which exceeds limit K={K}"
    
    return True, ""

def verify(pred, answer, meta):
    """
    Verify if the model's prediction is correct
    
    Parameters:
    - pred: Model's predicted answer (text)
    - answer: Correct answer (car order)
    - meta: Problem metadata
    
    Returns:
    - True/False indicating verification result, or None if prediction cannot be parsed
    """
    # Parse metadata
    if isinstance(meta, str):
        try:
            meta = json.loads(meta)
        except json.JSONDecodeError as e:
            #print(f"Meta parsing error: {e}")
            return 0
    elif isinstance(meta, dict):
        pass
    else:
        raise ValueError('meta should be dict or str')
    
    # Get original car order, colors, and constraints
    original_car_ids = meta.get("car_ids", [])
    colors = meta.get("colors", [])
    K = meta.get("K", 0)
    min_switches = meta.get("min_switches", 0)
    
    # Extract JSON code block from prediction
    car_order = None
    final_answer = extract_last_code_block(pred)
    if not final_answer:
        return 0

    try:
        # Look for patterns like [1, 2, 3, 4, 5]
        pattern = r'\[([\d\s,]+)\]'
        matches = re.findall(pattern, final_answer)
        if matches:
            car_order = [int(x.strip()) for x in matches[0].split(',') if x.strip()]
        else:
            #print("No list pattern found in prediction")
            return 0
    except Exception as e:
        #print(f"Error parsing direct list: {e}")
        return 0
    
    if not car_order:
        #print("Could not extract car order from prediction")
        return 0
    
    # Check validity of the car order
    valid, error_msg = is_valid_car_order(car_order, original_car_ids, K)
    if not valid:
        #print(f"Invalid car order: {error_msg}")
        #print(f"Car order: {car_order}")
        return 0
    
    # Calculate number of color switches and compare with optimal solution
    switches = calculate_switches(car_order, colors)
    #print(f"Car order: {car_order}")
    #print(f"Switches: {switches}, Min switches: {min_switches}")
    if switches == min_switches:
        return 1
    return 0
