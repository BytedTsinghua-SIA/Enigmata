PROMPT_TEMPLATE = """
You are playing a Minesweeper game.
On a grid composed of different cells, the player's goal is to deduce all cells that contain mines and avoid clicking on mines.
Each cell in the game may either contain a mine or show the number of adjacent mines.

### Grid and Mines:
The game grid consists of several cells, each of which may be:
- Mine: If the player clicks on a mine cell, the game ends.
- Numbered cell: This cell displays the number of mines adjacent to it. The number indicates how many of the eight neighboring cells contain mines.

### Current Grid State Representation:
The grid state is represented as:
-2: Indicates the cell is unknown (not revealed).
0-8: Revealed non-mine cells, where the number indicates how many mines are adjacent to that cell. For example, a cell with 0 means no mines adjacent, a cell with 1 means one mine adjacent, and so on.

### Task:
Based on the current grid state, infer the positions of the mines that can be definitively determined.
The current grid state is:
{question}

### Coordinate Explanation:
- Coordinates start from (0, 0), where the first row, first column is (0, 0), the second row, second column is (1, 1), and so on.
- You need to provide the coordinates of the determinable mines in the following format:

### Response Format:
- Please output your answer within a code block (```), formatted as a list of coordinates(r, c), for example:
```
[(1, 1), (2, 4), (4, 3)]
```
- If no solution exists, output within the code block:
```
"Unable to determine any mine locations."
```
""".strip()