import json
import re
import re
import ast

def extract_last_code_block(text: str):
    code_blocks = re.findall(r'```.*?\n(.*?)```', text, re.DOTALL)
    if not code_blocks:
        code_blocks = re.findall(r'```(.*?)```', text, re.DOTALL)
    return code_blocks[-1].strip() if code_blocks else None

def verify(pred, answer, meta):
    """
    Verifies the prediction against the expected answer.
    
    Parameters:
    - pred: The prediction string from the model.
    - meta: A dictionary containing additional information, including the expected answer.
    
    Returns:
    - 1 if the prediction is correct, 0 otherwise.
    """
    #meta = json.loads(meta) if isinstance(meta, str) else meta
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
    
    final_answer = extract_last_code_block(pred)
    
    if not final_answer:
        return 0
    if not final_answer or not isinstance(final_answer, str):
        return 0
    
    # Compare the final answer with the expected answer
    gold_answer = answer
    if final_answer == gold_answer:
        return 1
    
    return 0