import numpy as np
from typing import Tuple, List
import random
from collections import deque
import random
import json
import hashlib
import random
import time
from tqdm import tqdm
from .template import PROMPT_TEMPLATE

PUZZLE_TYPE = "search_puzzle"
SOURCE_URL = "auto-generated"
DATASET_NAME = "slant"

def string_to_md5(s):
    encoded_string = s.encode('utf-8')
    md5_hash = hashlib.md5()
    md5_hash.update(encoded_string)
    return md5_hash.hexdigest()

CONFIG = {
    "easy": [0.1, 0.2],
    "medium": [0.3, 0.4],
    "hard": [0.5]
}

class GokigenGenerator:
    def __init__(self, rows: int, cols: int):
        """
        Initialize generator
        rows: Number of rows in the grid
        cols: Number of columns in the grid
        """
        self.rows = rows
        self.cols = cols
        # Store diagonal direction, 1 represents "/", -1 represents "\"
        self.solution = np.zeros((rows, cols))
        # Store numbers at intersections, -1 means no number
        self.puzzle = np.full((rows + 1, cols + 1), -1)
        
    def _has_loop(self) -> bool:
        """Check if there's a loop, return True if found"""
        visited = set()
        
        def dfs(x: int, y: int, prev_x: int, prev_y: int) -> bool:
            if (x, y) in visited:
                return True  # Found a loop
            
            visited.add((x, y))
            curr_direction = self.solution[x][y]
            
            # Get possible next points
            next_points = []
            if curr_direction == 1:  # "/"
                if x > 0 and y < self.cols - 1: next_points.append((x-1, y+1))
                if x < self.rows - 1 and y > 0: next_points.append((x+1, y-1))
            else:  # "\"
                if x > 0 and y > 0: next_points.append((x-1, y-1))
                if x < self.rows - 1 and y < self.cols - 1: next_points.append((x+1, y+1))
            
            for next_x, next_y in next_points:
                if (next_x, next_y) != (prev_x, prev_y):  # Avoid going back to previous point
                    if dfs(next_x, next_y, x, y):
                        return True
                        
            visited.remove((x, y))  # Remove visit mark when backtracking
            return False
            
        # Check each starting point
        for i in range(self.rows):
            for j in range(self.cols):
                visited = set()
                if dfs(i, j, -1, -1):
                    return True  # Found a loop
        return False  # No loop found
    
    def _count_lines(self, x: int, y: int) -> int:
        """Count the number of lines connected to an intersection"""
        count = 0
        # Check four adjacent cells
        if x > 0 and y > 0 and self.solution[x-1][y-1] == -1: count += 1
        if x > 0 and y < self.cols and self.solution[x-1][y] == 1: count += 1
        if x < self.rows and y > 0 and self.solution[x][y-1] == 1: count += 1
        if x < self.rows and y < self.cols and self.solution[x][y] == -1: count += 1
        return count
    
    def _has_unique_solution(self) -> bool:
        """Check if the puzzle has a unique solution"""
        def solve(curr_solution):
            # Create a copy for backtracking
            solution_copy = curr_solution.copy()
            changed = True
            while changed:
                changed = False
                # Check all intersections
                for i in range(self.rows + 1):
                    for j in range(self.cols + 1):
                        if self.puzzle[i][j] == -1:
                            continue
                            
                        target = self.puzzle[i][j]
                        # Calculate current determined lines
                        current = 0
                        unknown = []
                        
                        # Check four adjacent cells
                        positions = [
                            (i-1, j-1, -1), (i-1, j, 1),
                            (i, j-1, 1), (i, j, -1)
                        ]
                        
                        for x, y, line_type in positions:
                            if 0 <= x < self.rows and 0 <= y < self.cols:
                                if solution_copy[x][y] != 0:
                                    if solution_copy[x][y] == line_type:
                                        current += 1
                                else:
                                    unknown.append((x, y, line_type))
                        
                        # If the number of unknown lines equals target minus current, all unknown lines must be the specified direction
                        if len(unknown) > 0 and target - current == len(unknown):
                            for x, y, line_type in unknown:
                                solution_copy[x][y] = line_type
                                changed = True
                        # If current equals target, all unknown lines must be the opposite direction
                        elif len(unknown) > 0 and current == target:
                            for x, y, line_type in unknown:
                                solution_copy[x][y] = -line_type
                                changed = True
            
            return solution_copy
        
        # Try to solve
        test_solution = np.zeros((self.rows, self.cols))
        solved = solve(test_solution)
        
        # Check if all cells are filled
        if 0 in solved:
            return False  # Cannot fully solve
            
        # Check if solution is correct
        return np.array_equal(solved, self.solution)

    def generate_puzzle_data(self, difficulty_level = "medium") :
        """
        Generate a new puzzle
        difficulty: A number between 0.0-1.0 representing difficulty
        return: (puzzle, solution)
        """
        difficulty = random.choice(CONFIG[difficulty_level])
        while True:
            # Randomly generate solution
            self.solution = np.random.choice([1, -1], size=(self.rows, self.cols))
            
            # Ensure no loops
            while self._has_loop():  # Modified: continue generating when there's a loop
                self.solution = np.random.choice([1, -1], size=(self.rows, self.cols))
            
            # Decide number of hints based on difficulty
            total_intersections = (self.rows + 1) * (self.cols + 1)
            num_hints = int(total_intersections * (1 - difficulty))
            
            # Reset puzzle
            self.puzzle = np.full((self.rows + 1, self.cols + 1), -1)
            
            # Randomly select intersections and fill with numbers
            intersections = [(i, j) for i in range(self.rows + 1) 
                            for j in range(self.cols + 1)]
            random.shuffle(intersections)
            
            for i, j in intersections[:num_hints]:
                self.puzzle[i][j] = self._count_lines(i, j)
            
            # Check if it has a unique solution before returning
            if self._has_unique_solution():
                return {
                    "puzzle": self.to_string(),
                    "answer": self.solution.tolist(),
                    "difficulty_level": difficulty_level
                }
            
            # If no unique solution, regenerate
            self.solution = np.random.choice([1, -1], size=(self.rows, self.cols))

    def to_string(self) -> str:
        """Return printable string representation of the puzzle"""
        result = []
        for i in range(self.rows + 1):
            row = []
            for j in range(self.cols + 1):
                num = self.puzzle[i][j]
                row.append('.' if num == -1 else str(num))
            result.append(' '.join(row))
        return '\n'.join(result)

    def to_visual_string(self) -> str:
        """Return a more intuitive string representation of the puzzle"""
        # Create a larger grid to contain lines
        grid = [[' ' for _ in range(2 * self.cols + 1)] for _ in range(2 * self.rows + 1)]
        
        # Fill in the intersection numbers
        for i in range(self.rows + 1):
            for j in range(self.cols + 1):
                grid[i * 2][j * 2] = '.' if self.puzzle[i][j] == -1 else str(self.puzzle[i][j])
        
        # Fill in the diagonal lines
        for i in range(self.rows):
            for j in range(self.cols):
                if self.solution[i][j] == 1:  # "/"
                    grid[i * 2 + 1][j * 2 + 1] = '/'
                else:  # "\"
                    grid[i * 2 + 1][j * 2 + 1] = '\\'
        
        # Convert to string
        return '\n'.join([''.join(row) for row in grid])

    def print_puzzle_and_solution(self):
        """Print both the puzzle and its solution"""
        print("Puzzle:")
        print(self.to_string())
        print("\nSolution:")
        print(self.to_visual_string())


def transform_problem_to_meta(problem, idx, language, split):
    timestamp = str(time.time())
    random_suffix = random.randint(0, int(1e6))
    id_string = f"binario_{idx}_{timestamp}_{random_suffix}"
    hash_id_string = string_to_md5(id_string)
    return {
        "id": hash_id_string,
        "question": problem["puzzle"],
        "answer": problem["answer"],
        "rationale": "",
        "split": split,
        "type": PUZZLE_TYPE,
        "source_url": SOURCE_URL,
        "dataset_name": DATASET_NAME,
        "difficulty_level": problem["difficulty_level"],
        "language": language,
    }

def generate(count=100, width=6, height=6, difficulty="medium", language="en", split="train"):
    prompt_template = PROMPT_TEMPLATE
    generated = 0
    attempts = 0
    max_attempts = count * 10  

    while generated < count and attempts < max_attempts:
        try:
            while True:
                generator = GokigenGenerator(height, width)
                problem = generator.generate_puzzle_data(difficulty_level=difficulty)
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
            for item in tqdm(generate(num, width=4, height=4, difficulty=difficulty, language=language, split=split), desc=f"Generating {difficulty} puzzles"):
                f.write(json.dumps(item, ensure_ascii=False) + '\n')

if __name__ == "__main__":
    save_to_jsonl("train_en.jsonl", 20000, language="en", split="train")
    save_to_jsonl("test_en.jsonl", 1500, language="en", split="eval")
