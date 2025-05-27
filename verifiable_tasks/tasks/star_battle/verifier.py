import re
import json

def extract_final_answer(text):
    match = re.findall(r"<begin_board>(.*?)<end_board>", text, re.DOTALL)
    if not match:
        return None
    return match[-1].strip()


def verify(pred, answer, meta):
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
    final_answer = extract_final_answer(pred)
    if final_answer is None:
        return 0

    final_answer_lines = final_answer.split("\n")
    answer_lines = answer.split("\n")

    final_answer_lines = [line.replace(" ", "") for line in final_answer_lines]
    answer_lines = [line.replace(" ", "") for line in answer_lines]

    # print(final_answer_lines)
    # print(answer_lines)

    if len(final_answer_lines) != len(answer_lines):
        return 0
    
    for i in range(len(final_answer_lines)):
        if final_answer_lines[i] != answer_lines[i]:
            return 0
   
    return 1