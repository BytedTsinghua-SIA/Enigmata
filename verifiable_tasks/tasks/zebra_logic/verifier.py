import re
import json


def extract_final_answer(pred):
    tables = re.findall(r'(\|[^\n]+\|(?:\n\s*\|[^\n]+\|)*)', pred)
    if not tables:
        return None
    return tables[-1]


def convert_text_to_clean_lines(text):
    lines = text.strip().lower().split("\n")
    return [re.sub(r'\s+', ' ', line) for line in lines]


def convert_text_to_grid(text):
    lines = text.strip().lower().split("\n")
    grid_lines = [line.split("|")[1:-1] for line in lines]
    clean_grid_lines = [[re.sub(r'\s+', ' ', grid.strip()) for grid in line] for line in grid_lines]
    return clean_grid_lines
            

def verify(pred, answer, meta):
    """
    Verifies the prediction against the ground truth answer.
    """
    if isinstance(answer, str):
        try:
            answer = json.loads(answer)
        except json.JSONDecodeError:
            pass
    else:
        pass
    
    #meta = json.loads(meta) if isinstance(meta, str) else meta
    if isinstance(meta, str):
        meta = json.loads(meta)
    elif isinstance(meta, dict):
        pass
    else:
        raise ValueError('meta should be dict or str')
    # Extract the final answer from the prediction
    final_answer = extract_final_answer(pred)
    
    if final_answer is None:
        return 0  # No valid answer found
    
    final_answer_grid_lines = convert_text_to_grid(final_answer)
    label_grid_lines = convert_text_to_grid(answer)

    for line in label_grid_lines:
        if line not in final_answer_grid_lines:
            return 0  # Line does not match

    return 1  # All lines match
