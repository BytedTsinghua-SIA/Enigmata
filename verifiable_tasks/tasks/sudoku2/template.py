PROMPT_TEMPLATE="""
You are provided with a 4x4 Sudoku puzzle. Some cells are filled with numbers, while empty cells are represented by dots. 
Your task is to find a valid solution for the puzzle based on the following rules:

1. **Board Structure:** The Sudoku board is a 4×4 grid, divided into 4 smaller 2×2 subgrids (regions).
2. **Number Range:** Each cell can only contain a number between 1 and 4.
3. **Row Rule:** Each row must contain the numbers 1 through 4, with no repeats.
4. **Column Rule:** Each column must contain the numbers 1 through 4, with no repeats.
5. **Subgrid Rule:** Each 2×2 subgrid must contain the numbers 1 through 4, with no repeats.

**Task:**
- Find a valid Sudoku solution for the given puzzle.
- If there are multiple solutions, provide one.

**Response format:**
- Please output your answer within a code block (```) representing the solved Sudoku board, formatted as a grid of numbers, for example::
```
2 4 3 1
3 1 2 4
4 3 1 2
1 2 4 3
```

Here is the puzzle:
{question}

Please provide the solution according to the requirements above.
""".strip()