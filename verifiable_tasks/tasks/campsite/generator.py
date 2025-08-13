import json
import random
import numpy as np
from tqdm import tqdm
import hashlib
import time
from .template import PROMPT_TEMPLATE

TREE = 'X'
TENT = '*'
EMPTY = '.'
CONFIGS = {"easy": {"m": 4, "n": 4, "t": 4}, "medium": {"m": 5, "n": 5, "t": 5}, "hard": {"m": 6, "n": 6, "t": 6}}

PUZZLE_TYPE = "PUZZLE"
SOURCE_URL = "auto-generated"
DATASET_NAME = "campsite"

TEST_SPLIT_SIZE = 500

def generate_campsite_problem(language, m, n, t):
    board = np.array([[0 for _ in range(n)] for _ in range(m)])
    cnt = 0
    empty_cells = m * n
    # 0: empty, 1: tent, 2: adjacent
    while cnt < t:
        x, y = random.randint(0, m - 1), random.randint(0, n - 1)
        if board[x][y] == 0:
            board[x][y] = 1
            cnt += 1
            empty_cells -= 1
            # row-wise
            if x > 0 and board[x - 1][y] == 0:
                board[x - 1][y] = 2
                empty_cells -= 1
            if x < m - 1 and board[x + 1][y] == 0:
                board[x + 1][y] = 2
                empty_cells -= 1
            # column-wise
            if y > 0 and board[x][y - 1] == 0:
                board[x][y - 1] = 2
                empty_cells -= 1
            if y < n - 1 and board[x][y + 1] == 0:
                board[x][y + 1] = 2
                empty_cells -= 1
            # diagonal
            if x > 0 and y > 0 and board[x - 1][y - 1] == 0:
                board[x - 1][y - 1] = 2
                empty_cells -= 1
            if x > 0 and y < n - 1 and board[x - 1][y + 1] == 0:
                board[x - 1][y + 1] = 2
                empty_cells -= 1
            if x < m - 1 and y > 0 and board[x + 1][y - 1] == 0:
                board[x + 1][y - 1] = 2
                empty_cells -= 1
            if x < m - 1 and y < n - 1 and board[x + 1][y + 1] == 0:
                board[x + 1][y + 1] = 2
                empty_cells -= 1
        else:
            if empty_cells == 0:
                break
    # mask on tents only
    mask = np.where(board == 1, 1, 0)
    board = board * mask
    row_cnt = np.sum(board, axis=1)
    col_cnt = np.sum(board, axis=0)
    # allocate trees
    for i in range(m):
        for j in range(n):
            if board[i][j] == 1:
                # check if all 4 directions are occupied
                occupied_cnt = 4
                available_positions = []
                if i > 0 and board[i - 1][j] == 0:
                    occupied_cnt -= 1
                    available_positions.append((i - 1, j))
                if i < m - 1 and board[i + 1][j] == 0:
                    occupied_cnt -= 1
                    available_positions.append((i + 1, j))
                if j > 0 and board[i][j - 1] == 0:
                    occupied_cnt -= 1
                    available_positions.append((i, j - 1))
                if j < n - 1 and board[i][j + 1] == 0:
                    occupied_cnt -= 1
                    available_positions.append((i, j + 1))
                # if all 4 directions are occupied, remove the tent
                if occupied_cnt == 4:
                    board[i][j] = 0
                    cnt -= 1
                    continue
                # randomly allocate trees in 1 of the available positions
                x, y = random.choice(available_positions)
                board[x][y] = 3 # tree

    question = [[EMPTY if board[i][j] == 0 else TREE if board[i][j] == 3 else EMPTY for j in range(n)] for i in range(m)]
    answer = [[EMPTY if board[i][j] == 0 else TENT if board[i][j] == 1 else TREE for j in range(n)] for i in range(m)]

    total_tents = f"total number of tents: {cnt}"
    row_indication = "tents in each row: " + ' '.join(str(c) for c in row_cnt)
    col_indication = "tents in each column: " + ' '.join(str(c) for c in col_cnt)
    question = total_tents + '\n' + row_indication + '\n' + col_indication + '\n' + '\n'.join([' '.join(row) for row in question])
    answer = total_tents + '\n' + row_indication + '\n' + col_indication + '\n' + "<begin_board>\n" + '\n'.join([' '.join(row) for row in answer]) + '\n' + "<end_board>"


    problem = {"question": question, "answer": answer, "cnt": cnt}
    return problem

def string_to_md5(s):
    encoded_string = s.encode('utf-8')
    md5_hash = hashlib.md5()
    md5_hash.update(encoded_string)
    return md5_hash.hexdigest()

def transform_problem_to_meta(problem, idx, language, split):
    timestamp = str(time.time())  
    id_string = f"campsite_{idx}_{timestamp}"
    hash_id_string = string_to_md5(id_string)
    return{
        "id": hash_id_string,
        "question": problem["question"],
        "answer": problem["answer"],
        "rationale": "",
        "split": split, 
        "type": PUZZLE_TYPE,
        "source_url": SOURCE_URL,
        "dataset_name": DATASET_NAME,
        "difficulty_level":  problem["difficulty_level"],
        "language": language
    }

    
def generate(count=100, difficulty='medium', language='en', split="train", **kwargs):
    prompt_template = PROMPT_TEMPLATE
    #split = kwargs.get("split", "test")
    params = CONFIGS[difficulty]
    for i in tqdm(range(count)):
        problem = generate_campsite_problem(language, **params)
        problem["difficulty_level"] = difficulty
        assert problem["cnt"] >= params["t"] // 2, f"Invalid number of tents, expected: {params['t']}, actual: {problem['cnt']}"
        meta = transform_problem_to_meta(problem, i, language, split)
        yield {
            "prompt": prompt_template.format(question=meta["question"]),
            "answer": meta["answer"],
            "task_name": DATASET_NAME,
            "ability": PUZZLE_TYPE,
            "language": language,
            "meta": json.dumps(meta),
        }

def save_to_jsonl(output_file, count, language, split):
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in generate(count // 3, difficulty='easy', language=language, split=split):
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
        for item in generate(count // 3, difficulty='medium', language=language, split=split):
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
        for item in generate(count // 3, difficulty='hard', language=language, split=split):
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

if __name__ == "__main__":
     save_to_jsonl('train_en.jsonl', 20000, language='en', split="train")
     save_to_jsonl('test_en.jsonl', 1500, language='en', split="eval")