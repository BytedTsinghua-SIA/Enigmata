import json
import re
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
    #meta = json.loads(meta) if isinstance(meta, str) else meta
    if isinstance(meta, str):
        meta = json.loads(meta)
    elif isinstance(meta, dict):
        pass
    else:
        raise ValueError('meta should be dict or str')
    
    # Extract the final JSON code block
    final_answer = extract_last_code_block(pred)
    if not final_answer:
        return 0
    
    try:
        # Extract the final answer from the parsed JSON
        final_answer = final_answer.strip()
        gold_answer = answer.strip()
        
        # Clean and compare the final answer with the gold answer
        cleaned_final_answer = ' '.join(final_answer.split())
        cleaned_gold_answer = ' '.join(gold_answer.split())
        
        # Return 1 if the answers match, otherwise return 0
        return 1 if cleaned_final_answer == cleaned_gold_answer else 0
    except Exception as ex:
        return 0
