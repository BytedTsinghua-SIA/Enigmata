PROMPT_TEMPLATE = """Sum Skycraper is a logic puzzle game where the goal is to fill a grid matrix based on given clues and the height and number restrictions of rows and columns. Here are the basic rules:

1. Game Board: Typically, it is an n x n grid matrix. Each cell represents a building, with its height represented by a number ranging from 1 to n, where n is the length of the matrix side.
2. Building Heights: Each row and column must be filled with numbers representing the heights of the buildings. Each number can only appear once in a row or column, similar to Sudoku constraints.
3. Visibility Clues: The hint numbers outside the matrix tell you how many buildings can be seen from that direction. Taller buildings will block shorter buildings behind them. Therefore, a hint number indicates the total height of buildings visible from one end of the row or column.
   For example, if a column's hint is "11," it means that looking from the top or bottom of that column, the total height of visible buildings is 11. Additionally, the building heights need to be in increasing order, meaning shorter buildings are blocked by taller ones in front.
4. Objective: Fill the entire matrix according to the clues, ensuring that the heights of buildings in each row and each column are different, and that they comply with the visibility clues on the sides.

Example:

    [7] [4] [5] [9]
    +---+---+---+---+
[7] |   |   |   |   | [6]
    +---+---+---+---+
[9] |   |   |   |   | [5]
    +---+---+---+---+
[4] |   |   |   |   | [7]
    +---+---+---+---+
[10] |   |   |   |   | [4]
    +---+---+---+---+
    [5] [9] [7] [4]

The above is an example of a Sum Skycraper:
- The numbers at the top and bottom of the columns indicate how many buildings can be seen from that direction. For example, the hint at the top of the first column is "7," meaning that the total height of the visible buildings from top to bottom is 7.
- The hints on the left and right of the rows are similar to those for the columns, indicating the total height of buildings visible from the left and right sides of that row. For example, if the hint is 10, it means the visible buildings could possibly be 1, 2, 3, 4.

Now, given a Sum Skycraper scenario, please restore the height of each building in the scenario. If there are multiple answers, output any one of them. If there is no valid solution, then respond with "no valid solution."

Response format:
- The input data consists of four lines: the first line represents the height seen from top to bottom, the second line from left to right, the third line from right to left, and the fourth line from bottom to top.
- Using the previous example, the input data would be:
7 4 5 9
7 9 4 10
6 5 7 4
5 9 7 4
- Please output your answer within a code block (```), formatted as a grid of numbers storing the heights of the buildings, for example:
```
2 4 3 1
3 1 2 4
4 3 1 2
1 2 4 3
```
- If no solution exists, the result should be: "No valid solution."

The puzzle to be solved is:

{question}

Please provide the answer according to the above requirements.
"""