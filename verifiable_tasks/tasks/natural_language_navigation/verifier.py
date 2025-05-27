import re
import json

def extract_code_block(text):
    code_blocks = re.findall(r'```.*?\n(.*?)```', text, re.DOTALL)
    if not code_blocks:
        code_blocks = re.findall(r'```(.*?)```', text, re.DOTALL)
    return code_blocks

def extract_path_from_code_block(text):
    """
    Extract path from code block.
    """
    code_blocks = extract_code_block(text)
    if not code_blocks:
        return ""
    
    # Use the last code block
    content = code_blocks[-1].strip()
    
    # If content only contains uppercase letters and commas, return directly
    if re.match(r'^[A-Z, ]*$', content):
        # Remove possible spaces and commas, keep only letters
        return re.sub(r'[^A-Z]', '', content)
    
    return ""

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
    
    # Extract path from prediction
    parsed_path = extract_path_from_code_block(pred)
    
    # Check if the extracted path matches the answer
    if answer == "we dont need to remove":
        return int(len(parsed_path) == 0)
    return int(parsed_path == answer)