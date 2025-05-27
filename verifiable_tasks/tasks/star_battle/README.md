# Star Battle
## Task Overview  
Place stars ('*') in the grid according to the following rules:

- The grid contains two types of cells: '.' represents a space where a star can be placed, and 'X' represents a space where a star cannot be placed.
- Each row and each column must contain exactly one star.
- Stars cannot be adjacent to each other, including horizontally, vertically, and diagonally.

Each problem has a unique solution.

Example

Puzzle
```
. . . .
X . . .
. . . .
. . . .
```
Solution
```
. * . .
X . . *
* . . .
. . * .
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