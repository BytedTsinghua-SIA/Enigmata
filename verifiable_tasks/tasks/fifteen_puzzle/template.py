PROMPT_TEMPLATE = """The 15 Puzzle is a classic sliding puzzle game. It consists of a 4×4 grid containing 15 numbered tiles from 1 to 15 and one blank space (represented by 0). The player moves these tiles with the ultimate goal of arranging them in order from 1 to 15. Below are the detailed rules:

Game Rules:
1. Initial State:
- The initial state of the puzzle is 15 numbered tiles randomly distributed in a 4×4 grid, with the blank space located anywhere.
- The puzzle usually starts from a scrambled state.

2. Movement:
- The player can move a tile adjacent to the blank space into the blank space.
- Tiles can only move in the four directions: up (U), down (D), left (L), and right (R).
- Only one tile can be moved at a time.

3. Goal:
- The ultimate goal is to arrange the tiles in order from left to right, top to bottom, as follows:

1  2  3  4
5  6  7  8
9  10 11 12
13 14 15 0

- Please output your answer within a code block (```) as follows:
```
<result>
```

- If there is an answer, the <result> is the sequence of moves, for example:
```
LRURDL
```
- If there is no answer, the <result> is: 
```
No feasible move path exists.
```

Here is the board of the question:
{question}

Please provide a solution based on the above requirements.
""".strip()
