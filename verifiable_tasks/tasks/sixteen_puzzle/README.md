# Puzzle Type & Task Name  
**Puzzle Type**: Spatial&Sequential Puzzle  
**Task Name**: sixteen puzzle

## Task Overview  
The 16 Puzzle is a classic sliding number puzzle. It consists of a 4x4 grid containing 16 tiles numbered from 1 to 16. Players can choose to move an entire row or column in a circular fashion each time. The ultimate goal is to arrange the tiles in numerical order from 1 to 16. The detailed rules are as follows:

Game Rules:
1.Initial State:
- The initial state of the puzzle consists of 16 number tiles randomly arranged on a 4x4 grid.
- The puzzle typically starts from a scrambled state.

2.Move Mechanism:
- Players can choose to move an entire row or column, shifting it by 1 to 3 steps in a circular manner. For example: 1 2 3 4, shifting by 1 step results in 2 3 4 1, shifting by 2 steps results in 3 4 1 2, and shifting by 3 steps results in 4 1 2 3. 
- We represent row moves as RAB, where A is the row number and B is the number of steps. Similarly, column moves are represented as CAB, where A is the column number and B is the number of steps.

3.Goal:
- The ultimate goal is to arrange the tiles in order from left to right, top to bottom as follows:
1  2  3  4
5  6  7  8
9  10 11 12
13 14 15 16


---

## Supported Difficulty Levels  
- **Easy**: The invesion number is 0-45
- **Medium**: The invesion number is 46-59
- **Hard**: The invesion number is 60-100

---

## Data Volume  
The dataset includes problems split by language and difficulty levels:  

### English Dataset  
- **Training Set**: 24000
- **Evaluation Set**: 1500

### Chinese Dataset  
- **Training Set**: 24000
- **Evaluation Set**: 1500

---
