PROMPT_TEMPLATE = """
You are tasked with solving a customized version of the star-battle puzzle. The star-battle puzzle is a logic puzzle that requires the placement of stars in a grid.
There is only one solution to this puzzle.
Your goal is to determine the location of each star, adhering to the following rules:
1. **NOTATIONS:**
    The initial board consists of empty cells and blocked cells.
    Empty cells are denoted by '.', blocked cells are denoted by 'X', and stars are denoted by '*'.
2. **STAR MUST BE PLACED IN EMPTY CELL:**
    Each star must be placed in an EMPTY cell.
    Blocked cells cannot contain stars.
    You can only change cells denoted by '.', and must not change cells denoted by 'X'.
3. **EXACTLY 1 STAR IN EACH ROW AND COLUMN:**
    Each row and column must contain EXACTLY one star.
    No two stars can be in the same row or column.
    There shouldn't be rows or columns without stars.
4. **NO ADJACENT STARS ROW-WISE, COLUMN-WISE, OR DIAGONALLY:**
    No two stars can be adjacent to each other, even diagonally.
    - Row-wise adjacency: two stars are in the same row, and there is no empty cell between them.
    - Column-wise adjacency: two stars are in the same column, and there is no empty cell between them.
    - Diagonal adjacency: two stars are in the same diagonal, and there is no empty cell between them.
    Note that you are prone to make mistakes in diagonal adjacency, so be extra careful. Here are 2 examples of diagonal adjacency in a partial grid:
    ```
    . * . .
    . . * .
    ```
    ```
    . . * .
    . * . .
    ```
    In both cases, the two stars are diagonally adjacent. You should avoid this situation.
5. **CHECK FOR CONSTRAINTS AND BACKTRACK:** 
    In each step, you should check if it violates the constraints in 2., 3., and 4.
    If you find inconsistencies, you should backtrack and try a different placement.
    If you find that you can't place a star anywhere without violating the constraints, you should backtrack and try a different placement.
    Since there is only one solution, there is great chance your first placement is incorrect, which means you might need to start over.
6. **RESPONSE FORMAT:** 
    Your response should include the final board.
    The final board is a revised version of the initial board in a way that if you need to place a star in an empty cell, replace the '.' with a '*'.
    Don't change the blocked cells denoted by 'X'.
    Your final board should be wrapped between <begin_board> and <end_board> tags.
    Use the following structure:

    Final Board:
    ```
    <begin_board>
    [Final Board]
    <end_board>
    ```

Here is the puzzle:
{question}
Please provide the solution according to the requirements above.
""".strip()