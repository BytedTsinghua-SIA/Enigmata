import random
import collections
import json
from tqdm import tqdm
from .template import PROMPT_TEMPLATE

def diff_j(board, K):
    # Flatten the board into a one-dimensional list
    flat_board = [tile for row in board for tile in row if tile != 0]
    inversions = 0

    # Calculate the number of inversions
    for i in range(len(flat_board)):
        for j in range(i + 1, len(flat_board)):
            if flat_board[i] > flat_board[j]:
                inversions += 1

    return inversions

# Generate a random 16-puzzle board
def generate_puzzle(K, diff):
    # Create a list from 1 to K^2
    tiles = list(range(1, K**2+1))
    random.shuffle(tiles)

    # Convert the list to a KxK board
    board = [tiles[i:i + K] for i in range(0, K**2, K)]
    inv = diff_j(board, K)

    while (not diff[0]<=inv<=diff[1]):
        random.shuffle(tiles)
        board = [tiles[i:i + K] for i in range(0, K**2, K)]
        inv = diff_j(board, K)

    return [board, inv]

def board_to_string(board):
    board_str = '\n'.join(' '.join(str(tile).rjust(2, ' ') for tile in row) for row in board)
    return board_str


def generate(count=100, difficulty='medium', language='en', split="train"):
    prompt_template = PROMPT_TEMPLATE
    exist = {}
    dif_level = {"easy" : [0, 45], "medium" : [46,59], "hard" : [60,100]}
    diff = dif_level[difficulty]
    K =4
    for i in tqdm(range(count)):
        board,inv = generate_puzzle(K, diff)
        board_str = board_to_string(board)
        yield {
            "prompt": prompt_template.format(question=board_str),
            "answer":  board,
            "task_name": "sixteen_puzzle",    
            "ability": "logic_puzzle", 
            "language": language,
            "meta": {
                "id":"16-puzzle_"+difficulty+str(i),
                "question": board,
                "answer": board,
                "inversion": inv,
                "rationale": "", 
                "split": split,
                "type": "sequential_puzzle", 
                "source_url": "auto-generated", 
                "dataset_name": "sixteen_puzzle", 
                "difficulty_level": difficulty,
                "language": language,
            }
        }

def save_to_jsonl(of1, of2, count, lange='en'):
    with open(of1, 'w', encoding='utf-8') as f1, open(of2, 'w', encoding='utf-8') as f2:
        for item in generate(count//3, 'easy', lange):
            f1.write(json.dumps(item, ensure_ascii=False) + '\n')
            f2.write(json.dumps(item["meta"], ensure_ascii=False) + '\n')
        for item in generate(count//3, 'medium', lange):
            f1.write(json.dumps(item, ensure_ascii=False) + '\n')
            f2.write(json.dumps(item["meta"], ensure_ascii=False) + '\n')
        for item in generate(count//3, 'hard', lange):
            f1.write(json.dumps(item, ensure_ascii=False) + '\n')
            f2.write(json.dumps(item["meta"], ensure_ascii=False) + '\n')

# Call functions to generate and save
#save_to_jsonl('training/16puzzle/en/train.jsonl', 'raw/16puzzle/en/train.jsonl', 24000, 'en')
#save_to_jsonl('training/16puzzle/zh/train.jsonl', 'raw/16puzzle/zh/train.jsonl',24000, 'zh')

#save_to_jsonl('eval/16puzzle/en/test.jsonl', 'raw/16puzzle/en/test.jsonl', 1500, 'en')
#save_to_jsonl('eval/16puzzle/zh/test.jsonl', 'raw/16puzzle/zh/test.jsonl',1500, 'zh')