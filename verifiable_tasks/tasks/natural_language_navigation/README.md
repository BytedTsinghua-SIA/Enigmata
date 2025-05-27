# Natural Language Navigation
## Task Overview  
- Define a set of landmarks: store, bank, house, cinema, garden, school.
- For each description, there are 7 to 10 landmarks.
- The relationship between landmarks forms a binary tree structure, with the root node representing the starting point.
- Question: How to reach the nearest landmark of a specific type from the starting point? Provide the shortest path.

## Data Volume  
The dataset includes problems split by difficulty levels:  

### Dataset  
- **Training Set**: 20000
- **Evaluation Set**: 1500

## Data Difficulty Classification  
Difficulty levels are determined by **length of the shortest path**:  

- **Easy**:
  - less than 2

- **Medium**:
  - 2-3

- **Hard**:
  - More than 3