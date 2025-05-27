import json
import re

import re
import ast
import pdb
def extract_last_code_block(text: str):
    code_blocks = re.findall(r'```.*?\n(.*?)```', text, re.DOTALL)
    if not code_blocks:
        code_blocks = re.findall(r'```(.*?)```', text, re.DOTALL)
    return code_blocks[-1].strip() if code_blocks else None


def verify(pred, answer, meta):
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
    
    # Extract the final JSON code block from the prediction
    final_answer = extract_last_code_block(pred).strip()
    #pdb.set_trace()
    if '"' in final_answer:
        final_answer = final_answer.replace('"','')
    
    if not final_answer:
        return 0
    # Retrieve the gold answer from the meta data
    gold_answer = answer
    
    # Compare the final answer with the gold answer
    if final_answer == gold_answer:
        return 1
    return 0
