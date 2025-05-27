import re
import json
import re
import ast

def extract_last_code_block(text: str):
    code_blocks = re.findall(r'```.*?\n(.*?)```', text, re.DOTALL)
    if not code_blocks:
        code_blocks = re.findall(r'```(.*?)```', text, re.DOTALL)
    return code_blocks[-1].strip() if code_blocks else None

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
    input_numbers = meta["question"]
    num_len = len(input_numbers)
    final_answer = extract_last_code_block(pred)
    if final_answer is None:
        return 0
    if not isinstance(final_answer, str):
        return 0
    if "cannot form 24" in answer:
        if "cannot form 24" in final_answer:
            return 1
        return 0
    expression = final_answer
    try:
        expression = expression.replace("x","*")
        expression = expression.replace("×","*")
        expression = expression.replace("÷","/")
        if abs(eval(expression) - 24) > 1e-4:
            return 0
        number_pattern = r"\d+"
        extract_numbers = re.findall(number_pattern, expression)
        if len(extract_numbers) != num_len:
            return 0
        sorted_extract_numbers = sorted(extract_numbers)
        original_numbers = []
        for num in input_numbers:
            original_numbers.append(str(num))
        sorted_original_numbers = sorted(original_numbers)
        for i in range(num_len):
            if sorted_extract_numbers[i] != sorted_original_numbers[i]:
                return 0
        return 1
    except Exception as ex:
        return 0