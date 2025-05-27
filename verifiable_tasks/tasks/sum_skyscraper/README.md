# Puzzle Type & Task Name  
**Puzzle Type**: Sudoku Puzzle  
**Task Name**: sum_skyscrpaer  

## Task Overview  
This project generates puzzles based on the sum_skyscrpaer rules.  
Sum Skycraper is a logic puzzle game where the goal is to fill a grid matrix based on given clues and the height and number restrictions of rows and columns. Here are the basic rules:
1. Game Board: Typically, it is an n x n grid matrix. Each cell represents a building, with its height represented by a number ranging from 1 to n, where n is the length of the matrix side.
2. Building Heights: Each row and column must be filled with numbers representing the heights of the buildings. Each number can only appear once in a row or column, similar to Sudoku constraints.
3. Visibility Clues: The hint numbers outside the matrix tell you how many buildings can be seen from that direction. Taller buildings will block shorter buildings behind them. Therefore, a hint number indicates the total height of buildings visible from one end of the row or column.
   For example, if a column's hint is "11," it means that looking from the top or bottom of that column, the total height of visible buildings is 11. Additionally, the building heights need to be in increasing order, meaning shorter buildings are blocked by taller ones in front.
4. Objective: Fill the entire matrix according to the clues, ensuring that the heights of buildings in each row and each column are different, and that they comply with the visibility clues on the sides.



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
