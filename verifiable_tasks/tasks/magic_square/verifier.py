import re
import json
import ast

def extract_last_code_block(text: str):
    """Extract the content of the last code block from the text."""
    code_blocks = re.findall(r'```.*?\n(.*?)```', text, re.DOTALL)
    if not code_blocks:
        code_blocks = re.findall(r'```(.*?)```', text, re.DOTALL)
    return code_blocks[-1].strip() if code_blocks else None


def parse_answer(answer: str, delimiter: str = None):
    """Parse a string representation of a matrix into a 2D array."""
    if not answer:
        return None
    rows = answer.split("\n")
    result = []
    
    for row in rows:
        row = row.strip()
        if not row:
            continue
        
        columns = row.split(delimiter) if delimiter else row.split()
        result.append([int(grid) if grid.strip().isdigit() else None for grid in columns])
    
    return result if all(None not in row for row in result) else None

def parse_list_str(input_string):
    """Parse a string representation of a Python list."""
    try:
        return ast.literal_eval(input_string)
    except (ValueError, SyntaxError):
        return None

def preprocess_answer_to_matrix(raw_answer):
    """Convert various answer formats to a 2D matrix."""
    if isinstance(raw_answer, list):
        return raw_answer
    
    answer = parse_answer(raw_answer, delimiter=None)
    if answer is None:
        answer = parse_answer(raw_answer, delimiter=',')
    if answer is None:
        answer = parse_list_str(raw_answer)
    
    return answer


def verify(pred, answer, meta):
    """Verify if the prediction matches the answer."""
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
    pred = extract_last_code_block(pred)
    if pred is None:
        return 0
    normalized_pred = preprocess_answer_to_matrix(pred)
    if normalized_pred is None:
        return 0
    
    # Check if the prediction matches the answer
    for i in range(3):
            for j in range(3):
                if normalized_pred[i][j] is not None:
                    if normalized_pred[i][j] != answer[i][j]:
                        return 0
    return 1