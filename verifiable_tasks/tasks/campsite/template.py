PROMPT_TEMPLATE = """
You are tasked with solving a campsite puzzle.

### Rules:
1. **Notations**: 
    - Trees are represented by `X`, tents are represented by `*`, and empty spaces are represented by `.`.
    - You will be given a board with trees and empty spaces, the total number of tents, and indications for the number of tents in each row and column. Your goal is to place tents on the empty spaces.
2. **Constraints**:
    - Every tree on the board is associated with one tent, which is always horizontally or vertically adjacent to it.
    - No tent can be horizontally, vertically or diagonally adjacent to another tent.
    - The number of tents in each row and column should match the given indications.
    - The number of tents on the board should match the given total number of tents.
    - A tent can only be associated with one tree, but it can be adjacent to more than one tree.

    
### Response Format:
- Your response should include a solution followed by the final board.
- You must not change trees (`X`) on the board, but only place tents (`*`) on empty spaces (`.`).
- The final board should be wrapped between `<begin_board>` and `<end_board>` tags.
    
    Final Board:
    ```
    <begin_board>
    [Final Board]
    <end_board>
    ```

Here is the puzzle:
{question} 
""".strip()
