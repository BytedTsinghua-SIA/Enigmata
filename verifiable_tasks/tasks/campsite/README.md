# Campsite
## Task Overview  
Given the total number of tents, and the number of tents in each row and each column, place the tents ('*') in the grid according to the following rules:

- There are two types of cells in the grid: 'X' represents a tree, and '.' represents an empty space where tents can be placed ('*').
- Each tent must be adjacent to a tree either horizontally or vertically.
- No two tents can be adjacent to each other, including horizontally, vertically, and diagonally.
- The number of tents in each row and column must match the given numbers.
- The total number of tents must match the given number.
- A tent can be adjacent to multiple trees.

Example:

Puzzle
```
total number of tents: 4
tents in each row: 2 0 2 0
tents in each column: 2 0 2 0
. X . .
X . X .
. . . .
. . X .
```
Solution
```
total number of tents: 4
tents in each row: 2 0 2 0
tents in each column: 2 0 2 0
<begin_board>
* X * .
X . X .
* . * .
. . X .
<end_board>
```

## Data Volume  
The dataset includes problems split by language and difficulty levels:  

### English Dataset  
- **Training Set**: 20000
- **Evaluation Set**: 1500

### Chinese Dataset  
- **Training Set**: 20000
- **Evaluation Set**: 1500

## Data Difficulty Classification  
Difficulty levels are determined by **grid size**:  

- **Easy**:
  - A grid of size 4

- **Medium**:
  - A grid of size 5

- **Hard**:
  - A grid of size 6

---
