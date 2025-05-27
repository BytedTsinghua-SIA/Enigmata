PROMPT_TEMPLATE = """Skycraper is a logic puzzle game where the goal is to fill a grid matrix based on the given clues. Here are the basic rules:

1. Game Board: It typically consists of an n x n grid matrix. Each cell represents a building, and the building height is represented by a number ranging from 1 to n, where n is the size of the matrix.
2. Building Heights: Each row and column must be filled with numbers that represent building heights. Each number can only appear once in a row or column, similar to Sudoku constraints.
3. Visibility Clues: The hint numbers outside the matrix indicate how many buildings can be seen from that direction. Taller buildings block the view of shorter buildings behind them. Thus, a hint number represents how many buildings are visible from one end of a row or column.
For example, if the clue for a column is "3", it means that from the top or bottom of that column, 3 buildings can be seen, and the building heights must increase, as shorter buildings will be blocked by taller ones.
4. Objective: Fill the entire matrix based on the clues, ensuring that the heights of the buildings are distinct in each row and column and follow the visibility clues at the edges.

Example:

    [2] [1] [2] [3]
    +---+---+---+---+
[2] |   |   |   |   | [2]
    +---+---+---+---+
[3] |   |   |   |   | [2]
    +---+---+---+---+
[1] |   |   |   |   | [2]
    +---+---+---+---+
[4] |   |   |   |   | [1]
    +---+---+---+---+
    [2] [3] [2] [1]

This is an example of a Skycraper puzzle:
- The numbers at the top and bottom of the columns indicate how many buildings can be seen from that direction. For instance, the clue at the top of the first column is "2", meaning that 2 buildings can be seen from the top, indicating that at least one building is hidden by a taller one.
- The left and right clues for the rows work similarly, indicating how many buildings are visible from that row's left or right side.

Now, given a Skycraper puzzle, your task is to reconstruct the height of the buildings in each cell. If there are multiple solutions, return any one. If no valid solution exists, state that no solution exists.

Response format:
- Please output your answer within a code block (```), formatted as a grid of numbers, for example:
```
2 4 3 1
3 1 2 4
4 3 1 2
1 2 4 3
```

The input clues are:

{question}

Please provide the solution according to the requirements above.
"""