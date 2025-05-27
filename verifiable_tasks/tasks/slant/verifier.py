import re
import json
import re
import ast

def extract_last_code_block(text: str):
    code_blocks = re.findall(r'```.*?\n(.*?)```', text, re.DOTALL)
    if not code_blocks:
        code_blocks = re.findall(r'```(.*?)```', text, re.DOTALL)
    return code_blocks[-1].strip() if code_blocks else None


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False



def parse_answer(answer: str, delimiter: str = None):
    if not answer:
        return None
    rows = answer.split("\n")
    result = []
    
    for row in rows:
        row = row.strip()
        if not row:
            continue
        
        columns = row.split(delimiter) if delimiter else row.split()
        #import pdb
        #pdb.set_trace()
        result.append([int(float(grid)) if is_number(grid.strip()) else None for grid in columns])
    
    return result if all(None not in row for row in result) else None

def parse_list_str(input_string):
    try:
        return ast.literal_eval(input_string)
    except (ValueError, SyntaxError):
        return None

def preprocess_answer_to_matrix(raw_answer):
    if isinstance(raw_answer, list):
        return raw_answer
    
    answer = parse_answer(raw_answer, delimiter=None)
    if answer is None:
        answer = parse_answer(raw_answer, delimiter=',')
    if answer is None:
        answer = parse_list_str(raw_answer)
    
    return answer

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

    pred = extract_last_code_block(pred)
    if pred is None:
        return 0
    normalized_pred = preprocess_answer_to_matrix(pred)
    if normalized_pred is None:
        return 0
    return int(answer == normalized_pred)
