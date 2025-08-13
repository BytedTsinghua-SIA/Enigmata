import numpy as np
from typing import List, Tuple, Set
from collections import deque
import random
import json
import hashlib
import random
import time
from tqdm import tqdm
from .template import PROMPT_TEMPLATE

def string_to_md5(s):
    encoded_string = s.encode('utf-8')
    md5_hash = hashlib.md5()
    md5_hash.update(encoded_string)
    return md5_hash.hexdigest()

PUZZLE_TYPE = "search_puzzle"
SOURCE_URL = "auto-generated"
DATASET_NAME = "minesweeper"


class MinesweeperGenerator:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.board = None  # Complete mine distribution
        self.revealed = None  # Revealed cells
        self.directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        self.difficulty_settings = {
            'easy': {
                'mine_density': 0.1,  # Mine density (proportion of total cells)
                'initial_reveal_ratio': 0.3,  # Proportion of initially revealed cells
            },
            'medium': {
                'mine_density': 0.15,
                'initial_reveal_ratio': 0.2,
            },
            'hard': {
                'mine_density': 0.2,
                'initial_reveal_ratio': 0.15,
            },
            'expert': {
                'mine_density': 0.25,
                'initial_reveal_ratio': 0.1,
            }
        }
    
    def generate_board(self, num_mines: int) -> np.ndarray:
        """Generate random mine distribution"""
        positions = [(i, j) for i in range(self.height) for j in range(self.width)]
        mine_positions = np.random.choice(len(positions), num_mines, replace=False)
        
        self.board = np.zeros((self.height, self.width), dtype=int)
        for pos in mine_positions:
            i, j = positions[pos]
            self.board[i][j] = -1  # -1 represents a mine
        
        # Calculate number of mines around each cell
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] != -1:
                    self.board[i][j] = self._count_adjacent_mines(i, j)
        
        return self.board
    
    def _count_adjacent_mines(self, row: int, col: int) -> int:
        """Count mines adjacent to the specified position"""
        count = 0
        for di, dj in self.directions:
            ni, nj = row + di, col + dj
            if 0 <= ni < self.height and 0 <= nj < self.width:
                if self.board[ni][nj] == -1:
                    count += 1
        return count
    
    def set_revealed_state(self, revealed_board: np.ndarray):
        """Set the current known board state"""
        self.revealed = revealed_board
    
    def find_definite_mines(self) -> Set[Tuple[int, int]]:
        """Find definite mine positions"""
        definite_mines = set()
        changed = True
        
        while changed:
            changed = False
            for i in range(self.height):
                for j in range(self.width):
                    if self.revealed[i][j] > 0:  # Number cell
                        unknown_cells = self._get_unknown_neighbors(i, j)
                        if not unknown_cells:
                            continue
                            
                        # If the number of unknown cells equals the number, all unknown cells are mines
                        remaining_mines = self.revealed[i][j] - len(self._get_flagged_neighbors(i, j))
                        if len(unknown_cells) == remaining_mines:
                            for cell in unknown_cells:
                                if cell not in definite_mines:
                                    definite_mines.add(cell)
                                    changed = True
        
        return definite_mines
    
    def _get_unknown_neighbors(self, row: int, col: int) -> Set[Tuple[int, int]]:
        """Get surrounding unknown cells"""
        unknown = set()
        for di, dj in self.directions:
            ni, nj = row + di, col + dj
            if 0 <= ni < self.height and 0 <= nj < self.width:
                if self.revealed[ni][nj] == -2:  # -2 represents an unknown cell
                    unknown.add((ni, nj))
        return unknown
    
    def _get_flagged_neighbors(self, row: int, col: int) -> Set[Tuple[int, int]]:
        """Get surrounding cells flagged as mines"""
        flagged = set()
        for di, dj in self.directions:
            ni, nj = row + di, col + dj
            if 0 <= ni < self.height and 0 <= nj < self.width:
                if self.revealed[ni][nj] == -1:  # -1 represents a flagged mine
                    flagged.add((ni, nj))
        return flagged

def generate_minesweeper_puzzle(difficulty: str = 'medium', board_size: tuple = (9, 9)) -> Tuple[np.ndarray, np.ndarray, Set[Tuple[int, int]]]:
    """
    Generate a minesweeper puzzle with a definite solution
    
    Parameters:
        difficulty: Difficulty level ('easy', 'medium', 'hard', 'expert')
        board_size: Board size, format (width, height)
    """
    width, height = board_size
    generator = MinesweeperGenerator(width, height)
    
    # Set parameters based on difficulty
    settings = generator.difficulty_settings[difficulty]
    total_cells = width * height
    num_mines = int(total_cells * settings['mine_density'])
    min_revealed = int(total_cells * settings['initial_reveal_ratio'])
    max_revealed = min_revealed + int(total_cells * 0.05)  # Add some randomness
    
    while True:
        # Generate random board
        board = generator.generate_board(num_mines)
        
        # Randomly reveal some cells
        revealed = np.full((height, width), -2)  # -2 means unknown
        num_revealed = np.random.randint(min_revealed, max_revealed)
        revealed_positions = np.random.choice(total_cells, num_revealed, replace=False)
        
        for pos in revealed_positions:
            i, j = pos // width, pos % width
            if board[i][j] != -1:  # Only reveal non-mine cells
                revealed[i][j] = board[i][j]
        
        # Set current state and check if there's a definite solution
        generator.set_revealed_state(revealed)
        definite_mines = generator.find_definite_mines()
        
        if definite_mines:  # If there's a definite solution, return the result
            return {
                "board": board, 
                "revealed": revealed, 
                "mines": list(definite_mines),
                "difficulty_level": difficulty
            }      
    return None

# Usage example
def demo_different_difficulties():
    difficulties = ['easy', 'medium', 'hard', 'expert']
    board_sizes = {
        'easy': (9, 9),
        'medium': (12, 12),
        'hard': (16, 16),
        'expert': (16, 20)
    }
    
    for diff in difficulties:
        print(f"\nGenerating {diff} difficulty minesweeper puzzle:")
        problem = generate_minesweeper_puzzle(
            difficulty=diff,
            board_size=board_sizes[diff]
        )
        board, revealed, mines = problem["board"], problem["revealed"],  problem["mines"]
        print(f"Board:\n{board}")
        print(f"Output board:\n{revealed}")
        print(f"Board size: {board_sizes[diff]}")
        print(f"Number of mines: {np.sum(board == -1)}")
        print(f"Number of revealed cells: {np.sum(revealed >= 0)}")
        print(f"Number of definite mine positions: {len(mines)}")
        print(f"Definite mine positions: {mines}")



def transform_problem_to_meta(problem, idx, language, split):
    timestamp = str(time.time())
    random_suffix = random.randint(0, int(1e6))
    id_string = f"binario_{idx}_{timestamp}_{random_suffix}"
    hash_id_string = string_to_md5(id_string)
    return {
        "id": hash_id_string,
        "question": problem["revealed"].tolist(),
        "answer": problem["mines"],
        "rationale": "",
        "split": split,
        "type": PUZZLE_TYPE,
        "source_url": SOURCE_URL,
        "dataset_name": DATASET_NAME,
        "difficulty_level": problem["difficulty_level"],
        "language": language,
    }

def generate(count=100, difficulty="medium", language="en", split="train"):
    prompt_template = PROMPT_TEMPLATE
    generated = 0
    attempts = 0
    max_attempts = count * 10  

    board_sizes = {
        'easy': (9, 9),
        'medium': (12, 12),
        'hard': (16, 16),
        'expert': (16, 20)
    }

    while generated < count and attempts < max_attempts:
        try:
            while True:
                problem = generate_minesweeper_puzzle(difficulty=difficulty, board_size=board_sizes[difficulty])
                if problem: break
            meta = transform_problem_to_meta(problem, generated, language, split)
            meta["task_name"] = DATASET_NAME
            yield {
                "prompt": prompt_template.format(question=meta["question"]),
                "answer": meta["answer"],
                "task_name": DATASET_NAME,
                "ability": PUZZLE_TYPE,
                "language": language,
                "meta": json.dumps(meta, ensure_ascii=False),
            }
            generated += 1
        except ValueError as e:
            print(f"Generation error: {e}")
        attempts += 1

    if attempts >= max_attempts:
        print(f"Warning: Maximum attempt count reached, generated {generated} / {count} puzzles.")

def save_to_jsonl(output_file, count, language, split):
    difficulties = ["easy", "medium", "hard"]
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
    #save_to_jsonl("train_en.jsonl", 20000, language="en", split="train")
    #save_to_jsonl("test_en.jsonl", 1500, language="en", split="eval")
    save_to_jsonl("eval_zh.jsonl", 100, language="zh", split="eval")
    #save_to_jsonl("test_zh.jsonl", 1500, language="zh", split="eval")


"""
if __name__ == "__main__":
    demo_different_difficulties()
"""

