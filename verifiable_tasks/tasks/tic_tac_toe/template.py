PROMPT_TEMPLATE = """
Tic Tac Toe Game Rules:
1. The board consists of 3x3 cells.
2. Players take turns placing their mark on an empty cell, one move per turn. The two players use "O" or "X".
3. A player wins by placing three of their marks consecutively in a row, column, or diagonal.
4. If the board is completely filled without a winner, the game is a draw.

{question}

Question: What is the best next move? Please provide only your move and display the board.

Answer format:
- Please output your answer within a code block (```), for example:
```
\"X\" \"O\" \"\"
\"\" \"X\" \"\"
\"O\" \"\" \"X\"
```
"""