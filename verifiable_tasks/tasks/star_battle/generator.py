import numpy as np
from dataclasses import dataclass
from .template import PROMPT_TEMPLATE
import json
from tqdm import tqdm
import hashlib
import time

PUZZLE_TYPE = "grid_puzzle"
SOURCE_URL = "auto-generated"
DATASET_NAME = "star_battle"
TEST_SPLIT_SIZE=500

EMPTY = '.'
STAR = '*'
BLOCK = 'X'

SIZES = [5, 6, 7]
NUM_STARS = 1

## backtracker to generate star configs

@dataclass
class ProblemSpecs:
    size: int
    n_stars: int
    candidates: list
    successors: list
    boards: list

def compute_candidates(size, n_stars):
    def recurse(candidates, cols=[]):
        if len(cols) == n_stars:
            candidates.append(cols)
            return
        for c in range(cols[-1] + 2 if cols else 0, size - 2 * (n_stars - len(cols) - 1)):
            recurse(candidates, cols + [c])
    candidates = []; recurse(candidates)
    return candidates

def compute_successors(candidates):
    successors = [[] for _ in range(len(candidates))]
    def compare_candidates(candidates, i, j):
        for c1 in candidates[i]:
            for c2 in candidates[j]:
                if abs(c2 - c1) <= 1:
                    return False
        return True
    for i in range(len(candidates)):
        for j in range(len(candidates)):
            if compare_candidates(candidates,i, j):
                successors[i].append(j)
    return successors

def backtrack(specs, board, col_counts, successors, row):
    if row == specs.size:
        specs.boards.append(tuple(board))
        return
    for s in successors:
        cols = specs.candidates[s]
        valid = True
        for col in cols:
            if col_counts[col] == specs.n_stars:
                valid = False
                break
        if valid:
            board[row] = cols
            for col in cols:
                col_counts[col] += 1
            backtrack(specs, board, col_counts, specs.successors[s], row + 1)
            board[row] = None
            for col in cols:
                col_counts[col] -= 1

def generate_star_configs(S, N):
    candidates = compute_candidates(S, N)
    successors = compute_successors(candidates)
    specs = ProblemSpecs(
            size=S,
            n_stars=N,
            candidates=candidates,
            successors=successors,
            boards=[]
        )
    backtrack(specs, [None] * S, [0] * S, range(len(candidates)), 0)
    return specs.boards

def matrixify_star_configs(S, star_configs):
    mat = np.zeros((len(star_configs), S, S), dtype=int)
    for i, star_config in enumerate(star_configs):
        for r in range(S):
            for c in star_config[r]:
                mat[i, r, c] = 1
    return mat


def generate_star_battle_problem(S, N=1, temperature=20, star_configs=None):
    while True:
        # init board
        board = np.zeros((S, S), dtype=int)
        # sample solution
        idx = np.random.randint(star_configs.shape[0])
        solution = star_configs[idx]
        mask = 1 - solution
        # copy database
        remaining_sols = np.delete(star_configs, idx, axis=0)
        # place blocks
        while remaining_sols.shape[0] > 0:
            # compute star frequencies
            star_freqs = remaining_sols.mean(0) * mask
            # generate distribution (weighted boltzmann thing)
            logits = np.exp(temperature * (star_freqs - star_freqs.max())) * star_freqs
            p = logits / logits.sum()
            # sample block
            block = np.random.choice(S * S, p=p.flatten())
            board[block // S, block % S] = 1
            # prune solutions
            remaining_sols = remaining_sols[(remaining_sols * board).sum(2).sum(1) == 0]
        # extra constraints (filter boards, etc.)
        if not ((board.sum(0) == S - N).any() or (board.sum(1) == S - N).any()):
            break
    problem = {"board": board, "solution": solution}
    return problem

def string_to_md5(s):
    encoded_string = s.encode('utf-8')
    md5_hash = hashlib.md5()
    md5_hash.update(encoded_string)
    return md5_hash.hexdigest()

def transform_problem_to_meta(problem, idx, language, split):
    timestamp = str(time.time())  
    id_string = f"star_battle_{idx}_{timestamp}"
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

def get_question(S, board):
    question = '\n'.join(' '.join(BLOCK if board[r, c] == 1 else EMPTY for c in range(S)) for r in range(S))
    # print(question)
    return question


def get_answer(S, board, solution):
    answer = '\n'.join(' '.join(STAR if solution[r, c] == 1 else BLOCK if board[r, c] == 1 else EMPTY for c in range(S)) for r in range(S))
    # print(answer)
    return answer
    

def generate(count=100, difficulty='medium', language='en', split="train", **kwargs):
    prompt_template = PROMPT_TEMPLATE
    #split = kwargs.get("split", "eval")
    if difficulty == "easy": S = SIZES[0]
    elif difficulty == "medium": S = SIZES[1]
    elif difficulty == "hard": S = SIZES[2]
    star_configs = matrixify_star_configs(S, generate_star_configs(S, NUM_STARS))
    for i in tqdm(range(count)):
        problem = generate_star_battle_problem(S=S, N=NUM_STARS, temperature=20, star_configs=star_configs)
        problem["question"] = get_question(S, problem["board"])
        problem["answer"] = get_answer(S ,problem["board"], problem["solution"])
        problem["difficulty_level"] = difficulty
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