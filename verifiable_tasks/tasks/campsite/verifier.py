import re
import json

LOG=True


def log(text):
    if LOG:
        print(text)


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
    
    total = answer.split("\n")[0]
    total = total.split(":")[1].strip()
    total = int(total)
    row = answer.split("\n")[1]
    row = row.split(":")[1].strip().split(" ")
    row = [int(r) for r in row]
    col = answer.split("\n")[2]
    col = col.split(":")[1].strip().split(" ")
    col = [int(c) for c in col]
    
    answer = extract_final_answer(answer)

    final_answer_lines = final_answer.split("\n")
    answer_lines = answer.split("\n")

    final_answer_lines = [line.replace(" ", "") for line in final_answer_lines]
    answer_lines = [line.replace(" ", "") for line in answer_lines]

    #log(final_answer_lines)
    #log(answer_lines)

    # first check if the positions of the trees are the same
    if len(final_answer_lines) != len(answer_lines):
        # log("Column length mismatch")
        return 0
    
    for i in range(len(answer_lines)):
        if len(final_answer_lines[i]) != len(answer_lines[i]):
            # log("Row length mismatch")
            return 0
        for j in range(len(answer_lines[i])):
            if answer_lines[i][j] == "X":
                if final_answer_lines[i][j] != "X":
                    # log("Tree position mismatch")
                    return 0
                
    # then check if the number of tents in each row and column are correct, and if the total number of tents is correct
    row_cnt = [0] * len(row)
    col_cnt = [0] * len(col)
    for i in range(len(final_answer_lines)):
        for j in range(len(final_answer_lines[i])):
            if final_answer_lines[i][j] == "*":
                row_cnt[i] += 1
                col_cnt[j] += 1
    
    if row_cnt != row or col_cnt != col:
        # log("row/column count mismatch")
        return 0
    if sum(row_cnt) != total:
        # log("total count mismatch")
        return 0
    
    # finally check adjacency
    for i in range(len(final_answer_lines)):
        for j in range(len(final_answer_lines[i])):
            if final_answer_lines[i][j] == "*":
                if i > 0 and final_answer_lines[i - 1][j] == "*":
                    # log("Adjacency")
                    return 0
                if i < len(final_answer_lines) - 1 and final_answer_lines[i + 1][j] == "*":
                    # log("Adjacency")
                    return 0
                if j > 0 and final_answer_lines[i][j - 1] == "*":
                    # log("Adjacency")
                    return 0
                if j < len(final_answer_lines[i]) - 1 and final_answer_lines[i][j + 1] == "*":
                    # log("Adjacency")
                    return 0
   
    return 1