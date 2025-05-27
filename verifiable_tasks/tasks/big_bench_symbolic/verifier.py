import json
import re
import re
def extract_last_code_block(text: str):
    code_blocks = re.findall(r'```.*?\n(.*?)```', text, re.DOTALL)
    if not code_blocks:
        code_blocks = re.findall(r'```(.*?)```', text, re.DOTALL)
    return code_blocks[-1].strip() if code_blocks else None

def verify(pred, answer, meta=None):
    """Verify if the model's prediction matches the gold answer."""
    #meta = json.loads(meta) if isinstance(meta, str) else meta
    if isinstance(answer, str):
        try:
            answer = json.loads(answer)
        except json.JSONDecodeError:
            pass
    else:
        pass

    final_answer = extract_last_code_block(pred)
    if not final_answer:
        return 0

    try:
        # 寻找类似 [1, 2, 3, 4, 5] 的模式
        pattern = r'\[([\d\s,]+)\]'
        matches = re.findall(pattern, final_answer)
        if matches:
            final_pred = [int(x.strip()) for x in matches[0].split(',') if x.strip()]
        else:
            #print("No list pattern found in prediction")
            return 0
    except Exception as e:
        #print(f"Error parsing direct list: {e}")
        return 0
    
    
    if final_pred == answer:
        return 1
    return 0