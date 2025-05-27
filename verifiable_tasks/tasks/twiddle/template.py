PROMPT_TEMPLATE = """
Given a 3x3 sliding puzzle where each cell contains a number (1 to 9), your goal is to restore the puzzle to its original sorted order through a series of rotation operations.

Rules:
1. You can select a 2x2 region within the 3x3 puzzle and rotate the positions of these 4 cells counterclockwise.
2. The goal is to restore the puzzle to its initial state (as shown below):

1 2 3
4 5 6
7 8 9

Please provide the steps to restore the puzzle to its initial state.

Response format:
- Please output your answer within a code block (```) as follows:
```
<result>
```
- Replace `<result>` with a sequence of rotation steps, where each step is represented by a 2D coordinate (i, j) indicating the selection of the 2x2 region with (i, j) as the top-left corner for a counterclockwise rotation. For example
```
(0,0)->(1,1)->(0,1)
```
- The problem guarantees that a solution exists.

Here is the puzzle for you to solve:
{question}

Please provide the answer according to the above requirements.
"""