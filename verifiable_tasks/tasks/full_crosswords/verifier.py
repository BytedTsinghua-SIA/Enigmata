import re
import json


def extract_code_block(text):
    code_blocks = re.findall(r'```.*?\n(.*?)```', text, re.DOTALL)
    if not code_blocks:
        code_blocks = re.findall(r'```(.*?)```', text, re.DOTALL)
    return code_blocks

def parse_crossword_answers(content):
    """
    Parse horizontal and vertical answers from code block content.
    Format should be:
    across: ANSWER1, ANSWER2, ..., ANSWER_N
    down: ANSWER1, ANSWER2,..., ANSWER_N
    """
    if content.startswith('"') and content.endswith('"'):
        # No solution case
        return {"no_solution": True, "message": content.strip('"')}
    
    result = {"across": [], "down": []}
    
    # Process line by line
    lines = content.strip().split("\n")
    for line in lines:
        line = line.strip()
        if line.lower().startswith("across:"):
            # Get horizontal answers
            answers_part = line.split(":", 1)[1].strip()
            result["across"] = [ans.strip() for ans in answers_part.split(",")]
        elif line.lower().startswith("down:"):
            # Get vertical answers
            answers_part = line.split(":", 1)[1].strip()
            result["down"] = [ans.strip() for ans in answers_part.split(",")]
    
    return result

def extract_result_from_code_block(text):
    """
    Extract results from code block.
    """
    code_blocks = extract_code_block(text)
    if len(code_blocks) == 0:
        return None
    
    # Use the last code block
    content = code_blocks[-1].strip()
    
    # Parse answers
    return {"answer": parse_crossword_answers(content)}

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

    # Extract results from prediction
    result = extract_result_from_code_block(pred)
    if result is None:
        return 0  # Return 0 if no valid code block is found
    
    # Handle no solution case
    if "no_solution" in result["answer"]:
        # Check if the answer also indicates no solution
        if isinstance(answer, str) and "No valid solution" in answer:
            return 1
        return 0
    
    final_answer = result["answer"]
    gold_answer = answer
    
    # If gold_answer is a string, it means no solution
    if isinstance(gold_answer, str):
        return 0  # Prediction has solution but answer has none
    
    categories = ['across', 'down']
    all_correct = 1
    
    for category in categories:
        try:
            cleaned_final_answers = final_answer.get(category, [])
            cleaned_gold_answers = gold_answer.get(category, [])
            
            if len(cleaned_final_answers) != len(cleaned_gold_answers):
                return 0
            
            for final, gold in zip(cleaned_final_answers, cleaned_gold_answers):
                final_cleaned = final.replace(" ", "").strip().upper()
                gold_cleaned = gold.replace(" ", "").strip().upper()
                if final_cleaned != gold_cleaned:
                    all_correct = 0
                    break
        except Exception:
            return 0
            
    return all_correct