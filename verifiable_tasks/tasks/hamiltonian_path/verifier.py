import json
import re
import re
import ast

def extract_last_code_block(text: str):
    code_blocks = re.findall(r'```.*?\n(.*?)```', text, re.DOTALL)
    if not code_blocks:
        code_blocks = re.findall(r'```(.*?)```', text, re.DOTALL)
    return code_blocks[-1].strip() if code_blocks else None

def is_valid_hamiltonian_path(num_nodes, path, edges):
    """Check if the provided path is a valid Hamiltonian path (undirected)."""
    if len(path) != num_nodes:
        return False
    
    if len(set(path)) != num_nodes:
        return False
    
    if set(path) != set(range(num_nodes)):
        return False
    
    for i in range(num_nodes - 1): 
        u = path[i]
        v = path[i + 1]
        if (min(u, v), max(u, v)) not in edges:
            return False
    return True

def parse_edges_from_question(question):
    """Parse the edges from the 'question' field in the meta."""
    edges = set()
    lines = question.strip().split("\n")
    
    num_nodes = int(lines[0].strip())
    
    for line in lines[1:]:
        u, v = map(int, line.split())
        edges.add((min(u, v), max(u, v)))
    
    return num_nodes, edges

def verify(pred, answer, meta):
    """Verify if the model's prediction matches the gold answer."""
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

    final_answer = extract_last_code_block(pred)
    if not final_answer:
        return 0
    
    #final_answer = eval(pred)
    try:
        # Look for patterns like [1, 2, 3, 4, 5]
        pattern = r'\[([\d\s,]+)\]'
        matches = re.findall(pattern, final_answer)
        if matches:
            final_answer = [int(x.strip()) for x in matches[0].split(',') if x.strip()]
        else:
            #print("No list pattern found in prediction")
            return 0
    except Exception as e:
        #print(f"Error parsing direct list: {e}")
        return 0
    
    if isinstance(final_answer, str):
        final_answer = final_answer.strip()
    
    elif isinstance(final_answer, list):
        pass
    else:
        return 0  
    
    if isinstance(answer, str) and answer.strip() == "NO":
        return 1 if final_answer == "NO" else 0

    try:
        if isinstance(final_answer, str):
            path = json.loads(final_answer)
        elif isinstance(final_answer, list):
            path = final_answer
        else:
            return 0

        if not all(isinstance(x, int) for x in path):
            return 0
    except (json.JSONDecodeError, ValueError):
        return 0  
    
    num_nodes, edges = parse_edges_from_question(meta.get('question', ''))
    
    if is_valid_hamiltonian_path(num_nodes, path, edges):
        return 1
    return 0
