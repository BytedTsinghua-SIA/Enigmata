PROMPT_TEMPLATE = """
You are tasked with solving a Binario Puzzle.

### Rules:
1. The Binario puzzle is played on a grid of size NxN, where N is an even number.
2. Each cell in the grid must be filled with either a 0 or a 1.
3. No more than half of the cells in any row or column can contain the same number.
4. No more than two identical numbers can be adjacent horizontally or vertically.
5. The puzzle must have a unique solution.

### Task:
Solve the following Binario puzzle by filling in the missing cells (denoted by '_') with 0s and 1s according to the rules above.

### Response Format:
- Please output your answer within a code block (```), formatted as a grid of numbers, for example:
```
1 0 0 1
0 1 1 0
1 0 1 0
0 1 0 1
```
- If no solution exists, output within the code block:
```
No valid solution exists for the given Binario puzzle.
```

Here is the puzzle: 
{question} """.strip()