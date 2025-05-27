# Puzzle Type & Task Name  
**Puzzle Type**: Sudoku Puzzle  
**Task Name**: skyscraper

## Task Overview  
Skycraper is a logic puzzle game where the goal is to fill a grid matrix based on the given clues. Here are the basic rules:

1. Game Board: It typically consists of an n x n grid matrix. Each cell represents a building, and the building height is represented by a number ranging from 1 to n, where n is the size of the matrix.
2. Building Heights: Each row and column must be filled with numbers that represent building heights. Each number can only appear once in a row or column, similar to Sudoku constraints.
3. Visibility Clues: The hint numbers outside the matrix indicate how many buildings can be seen from that direction. Taller buildings block the view of shorter buildings behind them. Thus, a hint number represents how many buildings are visible from one end of a row or column.
For example, if the clue for a column is "3", it means that from the top or bottom of that column, 3 buildings can be seen, and the building heights must increase, as shorter buildings will be blocked by taller ones.
4. Objective: Fill the entire matrix based on the clues, ensuring that the heights of the buildings are distinct in each row and column and follow the visibility clues at the edges.



---

## Supported Difficulty Levels  
- **Easy**: The grid size is 3*3 and 4*4
- **Medium**: The grid size is 5*5 and 6*6
- **Hard**: The grid size is 7*7 and 8*8 

---

## Data Volume  
The dataset includes problems split by language and difficulty levels:  

### English Dataset  
- **Training Set**: 30000
- **Evaluation Set**: 1500

### Chinese Dataset  
- **Training Set**: 30000
- **Evaluation Set**: 1500

---
