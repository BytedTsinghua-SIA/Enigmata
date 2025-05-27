import re
import json
import re
import ast

def extract_last_code_block(text: str):
    code_blocks = re.findall(r'```.*?\n(.*?)```', text, re.DOTALL)
    if not code_blocks:
        code_blocks = re.findall(r'```(.*?)```', text, re.DOTALL)
    return code_blocks[-1].strip() if code_blocks else None


def parse_answer(answer: str, delimiter: str = None):
    if not answer:
        return None
    rows = answer.split("\n")
    result = []
    
    for row in rows:
        row = row.strip()
        if not row:
            continue
        
        columns = row.split(delimiter) if delimiter else row.split()
        result.append([int(grid) if grid.strip().isdigit() else None for grid in columns])
    
    return result if all(None not in row for row in result) else None

def parse_list_str(input_string):
    try:
        return ast.literal_eval(input_string)
    except (ValueError, SyntaxError):
        return None

def preprocess_answer_to_matrix(raw_answer):
    if isinstance(raw_answer, list):
        return raw_answer
    
    answer = parse_answer(raw_answer, delimiter=None)
    if answer is None:
        answer = parse_answer(raw_answer, delimiter=',')
    if answer is None:
        answer = parse_list_str(raw_answer)
    
    return answer

def is_valid_sudoku(board):
    # Check if each row is valid
    def is_valid_row(board):
        for row in board:
            if not is_valid_unit(row):
                return False
        return True

    # Check if each column is valid
    def is_valid_column(board):
        for col in zip(*board):  # Convert columns to rows
            if not is_valid_unit(col):
                return False
        return True

    # Check if each 2x2 subgrid is valid
    def is_valid_subgrid(board):
        for i in range(0, 4, 2):
            for j in range(0, 4, 2):
                subgrid = [
                    board[x][y]
                    for x in range(i, i + 2)
                    for y in range(j, j + 2)
                ]
                if not is_valid_unit(subgrid):
                    return False
        return True

    # Check if a unit (row, column, or 2x2 subgrid) is valid
    def is_valid_unit(unit):
        length = len(unit)
        for i in range(1, length + 1):
            if i not in unit:
                return 0
        return 1

    # Overall validation
    return is_valid_row(board) and is_valid_column(board) and is_valid_subgrid(board)

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

    puzzle = meta["question"]
    
    # convert to 2d array
    if isinstance(puzzle, str):
        puzzle_array = []
        for line in puzzle.splitlines():
            # Skip empty lines
            if line.strip():
                # Replace . with 0, keep numbers as is
                row = [0 if char == '.' else int(char) for char in line.split()]
                puzzle_array.append(row)
        puzzle = puzzle_array
    
    pred = extract_last_code_block(pred)
    if pred is None:
        return 0
    normalized_pred = preprocess_answer_to_matrix(pred)
    if normalized_pred is None:
        return 0
    if len(normalized_pred) != 4:
        return 0
    try:
        for i in range(4):
            for j in range(4):
                if puzzle[i][j] != 0 and puzzle[i][j] != normalized_pred[i][j]:
                    return 0
        if is_valid_sudoku(normalized_pred):
            return 1
        else:
            return 0
    except Exception as ex:
        return 0

