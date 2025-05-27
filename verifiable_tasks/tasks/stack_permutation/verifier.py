import re
import json


def extract_code_block(text):
    code_blocks = re.findall(r'```.*?\n(.*?)```', text, re.DOTALL)
    if not code_blocks:
        code_blocks = re.findall(r'```(.*?)```', text, re.DOTALL)
    return code_blocks

def extract_result_from_code_block(text):
    """Extract result from code block"""
    code_blocks = extract_code_block(text)
    if len(code_blocks) == 0:
        return None
    
    # Use the last code block
    content = code_blocks[-1].strip()
    
    # Check if it's an error message
    if content.startswith('"') and content.endswith('"'):
        # Remove quotes
        return {"answer": content.strip('"')}
    
    # Try to parse as Python list
    try:
        result = eval(content)
        if isinstance(result, list):
            return {"answer": result}
    except:
        pass
    
    return None

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
    
    # Extract result from prediction
    result = extract_result_from_code_block(pred)
    if result is None:
        return 0
    
    # Check if it's a "not a valid stack permutation" case
    invalid_markers = ["not a valid", "not valid"]
    
    # Check if the answer indicates invalid stack permutation
    answer_str = str(answer) if isinstance(answer, (list, dict)) else answer
    answer_invalid = any(marker in answer_str for marker in invalid_markers)
    
    # Check if the prediction indicates invalid stack permutation
    result_str = str(result["answer"])
    result_invalid = any(marker in result_str for marker in invalid_markers)
    
    # If answer indicates invalid and prediction also indicates invalid, it's correct
    if answer_invalid and result_invalid:
        return 1
    # If answer indicates invalid but prediction indicates valid, it's wrong
    elif answer_invalid and not result_invalid:
        return 0
    # If answer indicates valid but prediction indicates invalid, it's wrong
    elif not answer_invalid and result_invalid:
        return 0
    
    # Handle valid stack permutation cases
    if not isinstance(result["answer"], list):
        return 0
    
    input_sequence = meta["input_sequence"]
    output_sequence = meta["output_sequence"]
    
    try:
        stack = []
        output_idx = 0
        input_idx = 0
        
        for item in result["answer"]:
            if item.startswith("Pop"):
                if len(stack) == 0:
                    return 0
                top_element = stack.pop()
                if top_element != output_sequence[output_idx]:
                    return 0
                output_idx += 1
            elif item.startswith("Push"):
                push_element = int(item.strip()[5:-1])
                if push_element != input_sequence[input_idx]:
                    return 0
                stack.append(input_sequence[input_idx])
                input_idx += 1
            else:
                return 0  # Invalid operation
    except Exception:
        return 0
    
    # Make sure all input and output are processed
    if input_idx != len(input_sequence) or output_idx != len(output_sequence):
        return 0
    
    return 1