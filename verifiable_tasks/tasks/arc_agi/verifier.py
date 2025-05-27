import re
import ast


def extract_last_code_block(text: str):
    code_blocks = re.findall(r'```.*?\n(.*?)```', text, re.DOTALL)
    if not code_blocks:
        code_blocks = re.findall(r'```(.*?)```', text, re.DOTALL)
    return code_blocks[-1] if code_blocks else None


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
        result.append([int(grid) if grid.strip().isdigit() else None for grid in columns])
    
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


def matrix_equal(answer, pred):
    return isinstance(answer, list) and isinstance(pred, list) and answer == pred


def verify(pred: str, answer: str, meta=None):
    pred = extract_last_code_block(pred)
    normalized_pred = preprocess_answer_to_matrix(pred)
    if normalized_pred is None:
        return 0
    normalized_answer = preprocess_answer_to_matrix(answer)
    result = matrix_equal(normalized_pred, normalized_answer)
    if result:
        return 1
    else:
        return 0
