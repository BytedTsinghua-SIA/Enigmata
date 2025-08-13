import numpy as np
from typing import List, Tuple, Set
import random
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
DATASET_NAME = "light_up"

class LightUpGenerator:
    def __init__(self, width: int, height: int, difficulty: str = 'medium'):
        """
        Initialize Light Up game generator
        
        Args:
            width: Board width
            height: Board height
            difficulty: Difficulty level ('medium', 'hard')
        """
        self.width = width
        self.height = height
        self.difficulty = difficulty
        
        # Difficulty parameter settings
        self.difficulty_params = {
            'medium': {'black_cell_ratio': 0.15, 'numbered_ratio': 0.7},
            'hard': {'black_cell_ratio': 0.2, 'numbered_ratio': 0.5},
        }
        
        # Initialize board
        self.board = np.zeros((height, width), dtype=int)  # 0:empty, -1:black cell, 1-4:numbered black cell
        self.solution = np.zeros((height, width), dtype=int)  # 0:empty, 1:light bulb
        self.light_positions = set()
        
        # Add new symbol mapping
        self.symbols = {
            0: '⬜',  # Empty cell
            -1: '⬛', # Black cell
            5: '💡',  # Light bulb
            6: '🟨',  # Illuminated cell
        }

        # Add new symbol mapping for model understanding
        self.model_symbols = {
            0: '.',    # Empty cell
            -1: '#',   # Black cell
            5: 'L',    # Light bulb
            6: '*'     # Illuminated cell
        }

    def _is_valid_position(self, x: int, y: int) -> bool:
        """Check if coordinates are within the board range"""
        return 0 <= x < self.height and 0 <= y < self.width

    def _get_adjacent_cells(self, x: int, y: int) -> List[Tuple[int, int]]:
        """Get coordinates of adjacent cells"""
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        return [(x + dx, y + dy) for dx, dy in directions if self._is_valid_position(x + dx, y + dy)]

    def _is_illuminated(self, x: int, y: int) -> bool:
        """Check if a position is illuminated"""
        # Check in four directions
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        for dx, dy in directions:
            curr_x, curr_y = x, y
            while self._is_valid_position(curr_x, curr_y):
                if (curr_x, curr_y) in self.light_positions:
                    return True
                if self.board[curr_x, curr_y] < 0:  # Encountered a black cell
                    break
                curr_x += dx
                curr_y += dy
        return False

    def _can_place_light(self, x: int, y: int) -> bool:
        """Check if a light bulb can be placed at the specified position"""
        if self.board[x, y] != 0 or (x, y) in self.light_positions:
            return False
            
        # Check if it will illuminate other light bulbs
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in directions:
            curr_x, curr_y = x, y
            while self._is_valid_position(curr_x, curr_y):
                if (curr_x, curr_y) in self.light_positions:
                    return False
                if self.board[curr_x, curr_y] < 0:  # Encountered a black cell
                    break
                curr_x += dx
                curr_y += dy
        return True

    def _find_all_solutions(self, board: np.ndarray, current_pos: int = 0) -> List[Set[Tuple[int, int]]]:
        """Find all possible solutions"""
        solutions = []
        if current_pos >= self.width * self.height:
            # Check if the current solution is valid
            if self._is_valid_solution(self.light_positions):
                return [self.light_positions.copy()]
            return []

        x, y = current_pos // self.width, current_pos % self.width
        
        # If it's a black cell or already illuminated, skip to the next position
        if board[x, y] < 0 or self._is_illuminated(x, y):
            return self._find_all_solutions(board, current_pos + 1)

        # Try placing a light bulb at the current position
        if self._can_place_light(x, y):
            self.light_positions.add((x, y))
            solutions.extend(self._find_all_solutions(board, current_pos + 1))
            self.light_positions.remove((x, y))

        # Try not placing a light bulb
        solutions.extend(self._find_all_solutions(board, current_pos + 1))

        return solutions[:2]  # Only return at most two solutions to check for uniqueness

    def _is_valid_solution(self, lights: Set[Tuple[int, int]]) -> bool:
        """Check if the solution is valid"""
        # Check if all empty cells are illuminated
        for x in range(self.height):
            for y in range(self.width):
                if self.board[x, y] == 0:
                    is_lit = False
                    # Check in four directions
                    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        curr_x, curr_y = x, y
                        while self._is_valid_position(curr_x, curr_y):
                            if (curr_x, curr_y) in lights:
                                is_lit = True
                                break
                            if self.board[curr_x, curr_y] < 0:
                                break
                            curr_x += dx
                            curr_y += dy
                    if not is_lit:
                        return False
        return True

    def generate(self) -> Tuple[np.ndarray, Set[Tuple[int, int]], np.ndarray]:
        """Generate a Light Up game with a unique solution"""
        max_attempts = 100
        attempt = 0
        
        while attempt < max_attempts:
            self.board = np.zeros((self.height, self.width), dtype=int)
            self.light_positions.clear()
            
            # 1. Randomly place black cells
            black_cells_count = int(self.width * self.height * self.difficulty_params[self.difficulty]['black_cell_ratio'])
            black_cells = set()
            
            while len(black_cells) < black_cells_count:
                x = random.randint(0, self.height - 1)
                y = random.randint(0, self.width - 1)
                if self.board[x, y] == 0:
                    self.board[x, y] = -1
                    black_cells.add((x, y))

            # 2. Randomly place light bulbs and verify solution feasibility
            self._place_lights()

            # 3. Add number hints to black cells
            numbered_count = int(len(black_cells) * self.difficulty_params[self.difficulty]['numbered_ratio'])
            numbered_cells = random.sample(list(black_cells), numbered_count)
            
            for x, y in numbered_cells:
                adjacent_lights = sum(1 for adj_x, adj_y in self._get_adjacent_cells(x, y) 
                                    if (adj_x, adj_y) in self.light_positions)
                self.board[x, y] = adjacent_lights

            # Find all solutions
            solutions = self._find_all_solutions(self.board)
            
            if len(solutions) == 1:
                # Found a unique solution
                self.light_positions = solutions[0]
                # 4. Create the final solution board
                solution_board = self.board.copy()
                for x, y in self.light_positions:
                    solution_board[x, y] = 1
                return self.board, self.light_positions, self.get_illuminated_board()
            
            attempt += 1
        
        raise Exception("Unable to generate a puzzle with a unique solution, please try again")

    def _place_lights(self):
        """Place light bulbs to create a valid solution"""
        self.light_positions.clear()
        
        # Traverse all empty cells
        for x in range(self.height):
            for y in range(self.width):
                if self.board[x, y] == 0 and not self._is_illuminated(x, y):
                    # If the current cell is not illuminated, try to place a light bulb
                    if self._can_place_light(x, y):
                        self.light_positions.add((x, y))

        # Ensure all empty cells are illuminated
        all_illuminated = all(self._is_illuminated(x, y) 
                            for x in range(self.height) 
                            for y in range(self.width) 
                            if self.board[x, y] == 0)
        
        if not all_illuminated:
            # If not all cells are illuminated, regenerate
            self.board = np.zeros((self.height, self.width), dtype=int)
            self._place_lights()

    def get_illuminated_board(self) -> np.ndarray:
        """Get a board with illumination status"""
        illuminated_board = self.board.copy()
        
        # Mark light bulb positions
        for x, y in self.light_positions:
            illuminated_board[x, y] = 5  # Light bulb symbol
        
        # Mark illuminated cells
        for x in range(self.height):
            for y in range(self.width):
                if illuminated_board[x, y] == 0 and self._is_illuminated(x, y):
                    illuminated_board[x, y] = 6  # Illuminated cell symbol
        
        return illuminated_board

    def print_board(self, board: np.ndarray):
        """Print the board"""
        for i in range(board.shape[0]):
            for j in range(board.shape[1]):
                if board[i, j] >= 0 and board[i, j] <= 4:
                    print(self.symbols[0] if board[i, j] == 0 else board[i, j], end=' ')
                else:
                    print(self.symbols[board[i, j]], end=' ')
            print()

    def get_model_friendly_string(self, board: np.ndarray) -> str:
        """
        Generate a string representation suitable for language models
        
        Returns:
            str: Format like:
            ...#2#...
            .L.*.#..
            ...*....
            #..L...#
            where:
            . represents an empty cell
            # represents a black cell
            1-4 represents a numbered black cell
            L represents a light bulb
            * represents an illuminated cell
        """
        result = []
        for i in range(board.shape[0]):
            row = []
            for j in range(board.shape[1]):
                if board[i, j] >= 0 and board[i, j] <= 4:
                    row.append(str(board[i, j]) if board[i, j] > 0 else self.model_symbols[0])
                else:
                    row.append(self.model_symbols[board[i, j]])
            result.append(''.join(row))
        return '\n'.join(result)

    def generate_puzzle_data(self) -> dict:
        """
        Generate a dictionary containing complete game data, suitable for model training or testing
        
        Returns:
            dict: Contains the following key-value pairs:
                - puzzle: String representation of the initial puzzle
                - solution: String representation of the solution
                - size: (width, height) tuple
                - difficulty: Difficulty level
                - light_positions: List of light bulb positions
        """
        initial_board, light_positions, solution_board = self.generate()
        
        return {
            'puzzle': self.get_model_friendly_string(initial_board),
            'solution': self.get_model_friendly_string(solution_board),
            'size': (self.width, self.height),
            'difficulty_level': self.difficulty,
            'light_positions': list(light_positions)
        }


def transform_problem_to_meta(problem, idx, language, split):
    timestamp = str(time.time())
    random_suffix = random.randint(0, int(1e6))
    id_string = f"binario_{idx}_{timestamp}_{random_suffix}"
    hash_id_string = string_to_md5(id_string)
    return {
        "id": hash_id_string,
        "question": problem["puzzle"],
        "answer": problem["light_positions"],
        "rationale": "",
        "split": split,
        "type": PUZZLE_TYPE,
        "source_url": SOURCE_URL,
        "dataset_name": DATASET_NAME,
        "difficulty_level": problem["difficulty_level"],
        "language": language,
    }

def generate(count=100, width=6, height=6, difficulty="medium", language="en", split="train"):
    generator = LightUpGenerator(width, height, difficulty)
    prompt_template = PROMPT_TEMPLATE
    generated = 0
    attempts = 0
    max_attempts = count * 10  

    while generated < count and attempts < max_attempts:
        try:
            while True:
                problem = generator.generate_puzzle_data()
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
            for item in tqdm(generate(num,  width=6, height=6, difficulty=difficulty, language=language, split=split), desc=f"Generating {difficulty} puzzles"):
                f.write(json.dumps(item, ensure_ascii=False) + '\n')

if __name__ == "__main__":
    save_to_jsonl("eval_en.jsonl", 10, language="en", split="eval")

