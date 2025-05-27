PROMPT_TEMPLATE = """The 9 Puzzle is a classic sliding number puzzle. It consists of a 3x3 grid containing 9 tiles numbered from 1 to 9. Players can choose to move an entire row or column in a circular fashion each time. The ultimate goal is to arrange the tiles in numerical order from 1 to 9. The detailed rules are as follows:

Game Rules:
1.Initial State:
- The initial state of the puzzle consists of 9 number tiles randomly arranged on a 3x3 grid.
- The puzzle typically starts from a scrambled state.

2.Move Mechanism:
- Players can choose to move an entire row or column, shifting it by 1 to 2 steps in a circular manner. For example: 1 2 3, shifting by 1 step results in 2 3 1, shifting by 2 steps results in 3 1 2.
- We represent row moves as RAB, where A is the row number and B is the number of steps. Similarly, column moves are represented as CAB, where A is the column number and B is the number of steps.

3.Goal:
- The ultimate goal is to arrange the tiles in order from left to right, top to bottom as follows:
1  2  3  
4  5  6
7  8  9

4.Answer Format:
- - If a solution exists, output the sequence of moves within a code block (```), for example:
```
["R11", "C23", "R32", "C12", "R23", "C31"]
```
- If no solution exists, output within the code block:
```
"No valid sequence of moves exists."
```

Initial board: 
{question}

Please provide the solution according to the requirements above.
""".strip()