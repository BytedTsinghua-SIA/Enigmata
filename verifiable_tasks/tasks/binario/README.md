# Puzzle Type & Task Name  
**Puzzle Type**: Grid Puzzle  
**Task Name**: binario  

## Task Overview  
This project generates puzzles based on the Binario rules.  
Binario is a logic-based grid puzzle where players must fill a grid with 0s and 1s according to specific constraints:  
1. Each row and column must contain an equal number of 0s and 1s.  
2. No more than two identical numbers can be adjacent.  
3. The puzzle must have a unique solution.  

---

## Supported Difficulty Levels  
- **Easy**: Smaller grids with a higher percentage of pre-filled cells.  
- **Medium**: Moderate-sized grids with fewer pre-filled cells.  
- **Hard**: Larger grids with minimal pre-filled cells.  

---

## Data Volume  
The dataset includes problems split by language and difficulty levels:  

### English Dataset  
- **Training Set**: 20000
- **Evaluation Set**: 1500

### Chinese Dataset  
- **Training Set**: 20000
- **Evaluation Set**: 1500

---

## Data Difficulty Classification  
Difficulty levels are determined by **grid size**, **masking ratio**, and **minimum filled cells**:  

- **Easy**:
  - A grid of size 4 with a mask rate of 0.2 and a minimum of 12 filled cells.
  - A grid of size 6 with a mask rate of 0.1 and a minimum of 24 filled cells.

- **Medium**:
  - A grid of size 4 with a mask rate of 0.3 and a minimum of 10 filled cells.
  - A grid of size 6 with a mask rate of 0.2 and a minimum of 20 filled cells.

- **Hard**:
  - A grid of size 6 with a mask rate of 0.3 and a minimum of 24 filled cells.
  - A grid of size 8 with a mask rate of 0.2 and a minimum of 40 filled cells.

---

## Data Generation Logic  
The generator produces puzzles that adhere to Binario rules:  

### Problem Construction  
1. **Generate Complete Grid**:  
   - A valid Binario grid is constructed using backtracking to ensure it satisfies all rules.  

2. **Mask Cells**:  
   - Cells are randomly masked (replaced with `_`) according to the specified masking ratio.  

3. **Validate Puzzle**:  
   - The masked grid is validated to ensure it has a unique solution.  

### Unique Solution Enforcement  
The following techniques are used to ensure the puzzle has a unique solution:  
- Recursive backtracking to solve the grid and identify multiple solutions.  
- If multiple solutions are found, the puzzle is re-generated.  

---

## Usage Guide

### Generate Puzzles  
Use the `generate_puzzles()` function to create Binario problems.

#### Parameters  
- **`count`**: Number of puzzles to generate (default: 30).  
- **`difficulty`**: `'easy'`, `'medium'`, or `'hard'` (default: `'medium'`).  
- **`language`**: `'en'` for English, `'zh'` for Chinese (default: `'en'`).  
- **`split`**: Dataset split (`train` or `eval`).  

#### Return Value  
Each generated problem contains the following fields:  
- **`prompt`**: The problem description formatted with rules and instructions.  
- **`meta`**: Metadata including the problem type, solution, and reasoning.  
- **`answer`**: The correct solution to the problem.  

---

### Example Code  

```python
from your_module import generate_puzzles

# Generate 10 medium-difficulty Binario puzzles in English
puzzles = generate_puzzles(
    count=10, 
    difficulty='medium', 
    language='en',
    split="train"
)

# Save the puzzles to a JSONL file
with open("binario_puzzles.jsonl", "w") as f:
    for puzzle in puzzles:
        f.write(json.dumps(puzzle, ensure_ascii=False) + "\n")
