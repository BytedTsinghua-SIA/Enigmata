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
    lang = meta["language"]
    normalized_pred = extract_last_code_block(pred)
    
    if normalized_pred is None:
        return 0
    if "not exist" in answer:
        if not isinstance(normalized_pred, str):
            return 0
        if "not exist" in normalized_pred:
            return 1
        else:
            return 0
    maze = meta["question"]
    height = meta["height"]
    width = meta["width"]
    # Use regular expressions to extract coordinates and verify start and end coordinates
    if isinstance(normalized_pred, str):
        coordinates = re.findall(r'\(\d+,\s*\d+\)', normalized_pred)
        coordinates = [tuple(map(int, coord.strip('()').split(','))) for coord in coordinates]
    elif isinstance(normalized_pred, list):
        coordinates = normalized_pred
    else:
        return 0
    try:
        coordinate_list = [(int(x), int(y)) for x, y in coordinates]
        length = len(coordinate_list)
        if coordinate_list[0][0] != 1 or coordinate_list[0][1] != 1:
            return 0
        if coordinate_list[-1][0] != height or coordinate_list[-1][1] != width:
            return 0
        for i in range(1, length):
            if coordinate_list[i][0] < 1 or coordinate_list[i][0] > height:
                return 0
            if coordinate_list[i][1] < 1 or coordinate_list[i][1] > width:
                return 0
            if maze[coordinate_list[i][0]-1][coordinate_list[i][1]-1] == 'B':
                return 0
            if abs(coordinate_list[i][1] - coordinate_list[i - 1][1]) + abs(coordinate_list[i][0] - coordinate_list[i - 1][0]) != 1:
                return 0
        return 1
    except Exception as ex:
        return 0