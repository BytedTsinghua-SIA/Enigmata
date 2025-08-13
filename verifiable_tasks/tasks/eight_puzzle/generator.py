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

# Check if the puzzle is solvable
def is_solvable(board, K):
    # Flatten the board into a one-dimensional list
    flat_board = [tile for row in board for tile in row if tile != 0]
    inversions = 0

    # Calculate the number of inversions
    for i in range(len(flat_board)):
        for j in range(i + 1, len(flat_board)):
            if flat_board[i] > flat_board[j]:
                inversions += 1

    # Find the row of the empty space, counting from the bottom
    empty_row = K - [row for row in board if 0 in row][0].index(0) if K%2==0 else 0

    # The puzzle is solvable if the sum of inversions and the row of the empty space is even
    return (inversions + empty_row) % 2 == 0

# Generate a random K-puzzle board
def generate_puzzle(K, diff):
    # Create a list from 0 to K^2-1, where 0 represents the empty space
    tiles = list(range(K**2))
    random.shuffle(tiles)

    # Convert the list to a KxK board
    board = [tiles[i:i + K] for i in range(0, K**2, K)]
    inv = diff_j(board, K)
    #print(inv, diff)
    # If the board is not solvable or doesn't meet difficulty requirements, regenerate
    while (not is_solvable(board, K)) or (not diff[0]<=inv<=diff[1]):
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
    dif_level = {"easy" : [0, 10], "medium" : [12,16], "hard" : [18,100]}
    diff = dif_level[difficulty]
    K = 3
    for i in tqdm(range(count)):
        board, inv = generate_puzzle(K, diff)
        board_str = board_to_string(board)
        yield {
            "prompt": prompt_template.format(question=board_str),
            "answer":  board,
            "task_name": "eight_puzzle",    
            "ability": "logic_puzzle", 
            "language": language,
            "meta": json.dumps({
                "id":"8-puzzle_"+difficulty+str(i),
                "question": board,
                "answer": board,
                "inversion": inv,
                "rationale": "", 
                "split": split,
                "type": "sequential_puzzle", 
                "source_url": "auto-generated", 
                "dataset_name": "eight_puzzle", 
                "difficulty_level": difficulty,
                "language": language,
            })
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
#save_to_jsonl('training/8puzzle/en/train.jsonl', 'raw/8puzzle/en/train.jsonl', 24000, 'en')
#save_to_jsonl('training/8puzzle/zh/train.jsonl', 'raw/8puzzle/zh/train.jsonl',24000, 'zh')

#save_to_jsonl('eval/8puzzle/en/test.jsonl', 'raw/8puzzle/en/test.jsonl', 1500, 'en')
#save_to_jsonl('eval/8puzzle/zh/test.jsonl', 'raw/8puzzle/zh/test.jsonl',1500, 'zh')
