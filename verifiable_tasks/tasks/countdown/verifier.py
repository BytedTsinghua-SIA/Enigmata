import re
import json
import re
def extract_last_code_block(text: str):
    code_blocks = re.findall(r'```.*?\n(.*?)```', text, re.DOTALL)
    if not code_blocks:
        code_blocks = re.findall(r'```(.*?)```', text, re.DOTALL)
    return code_blocks[-1].strip() if code_blocks else None

def verify(pred, answer, meta):
    """Verify if the prediction is correct"""
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
    target = meta["target"]
    num_len = len(input_numbers)
    
    final_answer = extract_last_code_block(pred)
    if not final_answer:
        return 0
    
    if not isinstance(final_answer, str):
        return 0
    
    # Check if no solution
    if f"cannot form {target}" in answer:
        if f"cannot form {target}" in final_answer:
            return 1
        return 0
    
    expression = final_answer
    try:
        # Replace possible multiplication and division symbol variants
        expression = expression.replace("x", "*")
        expression = expression.replace("×", "*")
        expression = expression.replace("÷", "/")
        
        # Calculate the value of the expression
        value = eval(expression)
        
        # Check if the result equals the target value
        if abs(value - target) > 1e-4:
            return 0
        
        # Extract numbers from the expression
        number_pattern = r"\d+"
        extract_numbers = re.findall(number_pattern, expression)
        
        # Check if the number of digits used is correct
        if len(extract_numbers) != num_len:
            return 0
        
        # Check if the digits used match the input digits
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