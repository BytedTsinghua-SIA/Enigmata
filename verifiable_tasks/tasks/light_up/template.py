PROMPT_TEMPLATE = """
You need to solve a Light Up puzzle.

### Rules:
1. The puzzle is played on a rectangular grid (the number of rows and columns is not fixed).
2. The goal is to place light bulbs (represented by L) on the empty squares of the grid, following these rules:
   - Each numbered black square (represented by numbers 1-4) must have the specified number of light bulbs around it. For example, a black square with "1" means it must have exactly 1 light bulb around it, a "2" means exactly 2 light bulbs, and so on.
   - Light bulbs can only be placed on empty squares (represented by .) and must only light up empty squares; they cannot light up other light bulbs.
   - Black squares (represented by #) cannot be illuminated and block the light of the light bulbs.

### Coordinate Explanation:
- The coordinates start at (0, 0), meaning the first row, first column is (0, 0), the second row, second column is (1, 1), and so on.

### Task:
Solve the following Light Up puzzle by placing the required light bulbs (L):
{question}

You need to provide the coordinates of the light bulbs in the following format: 

### Response Format:
- Please output your answer within a code block (```), formatted as a list of numbers, for example:
```
[(2, 4]), (6, 2), (7, 5), (0, 0), (4, 3), (1, 1), (2, 0), (5, 1), (1, 7), (3, 2)]
```
- If there is no solution, output within the code block:
```
"No solution, unable to solve the given Light Up puzzle."
```
""".strip()