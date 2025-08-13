import random
from .template import PROMPT_TEMPLATE
from tqdm import tqdm
import json

CONFIGS = {
    "medium": [
        {"holes": 4, "min_moves": 4, "max_moves": 6},  # Configuration 1
    ],
    "hard": [
        {"holes": 6, "min_moves": 6, "max_moves": 8},  # Configuration 2
    ],
}

QUESTION_TEMPLATE = """
You are playing tic-tac-toe as {my_piece}.
Current board:
{current_board}

"""

def check_winner(board):
    # Check rows
    for row in board:
        if row[0] is not None and row[0] == row[1] == row[2]:
            return row[0]
    # Check columns
    for col in range(3):
        if board[0][col] is not None and board[0][col] == board[1][col] == board[2][col]:
            return board[0][col]
    # Check diagonals
    if board[0][0] is not None and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    if board[0][2] is not None and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]
    return None

def is_full(board):
    return all(cell is not None for row in board for cell in row)

def opponent(player):
    return 'O' if player == 'X' else 'X'

def minimax(board, turn, player):
    winner = check_winner(board)
    if winner is not None:
        return 1 if winner == player else -1
    if is_full(board):
        return 0

    if turn == player:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] is None:
                    board[i][j] = turn
                    score = minimax(board, opponent(turn), player)
                    board[i][j] = None
                    best_score = max(best_score, score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] is None:
                    board[i][j] = turn
                    score = minimax(board, opponent(turn), player)
                    board[i][j] = None
                    best_score = min(best_score, score)
        return best_score

def find_best_move(board, player):
    best_score = -float('inf')
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                board[i][j] = player
                score = minimax(board, opponent(player), player)
                board[i][j] = None
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    return best_move

def board_to_string(board):
    result = ""
    for i, row in enumerate(board):
        result += " | ".join(cell if cell is not None else " " for cell in row)
        result += "\n"
        if i < 2:
            result += "---------\n"
    return result

def generate_random_board_for(player, max_moves):
    if player == 'O':
        valid_move_counts = [1, 3, 5, 7]
    else:  # player == 'X'
        valid_move_counts = [0, 2, 4, 6, 8]
    
    while True:
        board = [[None for _ in range(3)] for _ in range(3)]
        moves = [(i, j) for i in range(3) for j in range(3)]
        random.shuffle(moves)
        move_count = random.choice(valid_move_counts)
        current = 'X'
        valid = True
        for idx in range(move_count):
            i, j = moves[idx]
            board[i][j] = current
            if check_winner(board) is not None:
                valid = False
                break
            current = opponent(current)
        if valid and check_winner(board) is None and current == player and move_count <= max_moves:
            return board

def generate_ttt_problem(difficulty):
    config = random.choice(CONFIGS[difficulty])
    holes, min_moves, max_moves = config["holes"], config["min_moves"], config["max_moves"]

    player = random.choice(['O', 'X'])
    board = generate_random_board_for(player, max_moves)
    
    current_board = [[cell if cell is not None else "" for cell in row] for row in board]
    
    best_move = find_best_move(board, player)
    best_answer = [row.copy() for row in board]
    if best_move is not None:
        i, j = best_move
        best_answer[i][j] = player

    answer_board = [[cell if cell is not None else "" for cell in row] for row in best_answer]
    
    return player, current_board, answer_board


from tqdm import tqdm
import json

def generate(count=100, difficulty="medium", language="en", split="train"):
    prompt_template = PROMPT_TEMPLATE
    generated = 0
    attempts = 0
    max_attempts = count * 10
    if difficulty not in CONFIGS:
        return

    # Initialize tqdm progress bar
    pbar = tqdm(total=count, desc=f"Generating TTT ({difficulty})", unit="sample")

    while generated < count and attempts < max_attempts:
        try:
            my_piece, current_board, answer_board = generate_ttt_problem(difficulty)
            question = QUESTION_TEMPLATE.format(my_piece=my_piece, current_board=board_to_string(current_board))
            meta_json = {
                "id": f"ttt_{difficulty}_{generated}",
                "question": question,
                "current_board": current_board,
                "active_player": my_piece,
                "answer": answer_board,
                "rationale": "", 
                "split": split,
                "type": "partially_observable", 
                "source_url": "auto-generated", 
                "dataset_name": "tic_tac_toe", 
                "difficulty_level": difficulty,
                "language": language,
            }
            meta_json["task_name"] = "tic_tac_toe"
            yield {
                "prompt": prompt_template.format(question=question),
                "answer": answer_board,
                "task_name": "tic_tac_toe",    
                "ability": "partially_observable", 
                "language": language,
                "meta": json.dumps(meta_json),
            }
            generated += 1
            pbar.update(1)  # Update progress bar
        except ValueError as e:
            print(f"Generation error: {e}")
        attempts += 1

    pbar.close()

    if attempts >= max_attempts:
        print(f"Warning: Maximum attempt count reached, generated {generated} / {count} puzzles.")

def save_to_jsonl(output_file, count, language, split):
    difficulties = ["medium", "hard"]
    per_difficulty = count // len(difficulties)
    remainder = count % len(difficulties)
    difficulty_counts = {d: per_difficulty for d in difficulties}
    for i in range(remainder):
        difficulty_counts[difficulties[i]] += 1

    with open(output_file, 'w', encoding='utf-8') as f:
        for difficulty in difficulties:
            num = difficulty_counts[difficulty]
            if num == 0:
                continue
            print(f"Generating {difficulty} puzzles: {num} puzzles")
            for item in tqdm(generate(num, difficulty=difficulty, language=language, split=split), desc=f"Generating {difficulty} puzzles"):
                f.write(json.dumps(item, ensure_ascii=False) + '\n')

if __name__ == "__main__":
    save_to_jsonl('train_en.jsonl', 20000, language='en', split="train")
    save_to_jsonl('test_en.jsonl', 1500, language='en', split="eval")