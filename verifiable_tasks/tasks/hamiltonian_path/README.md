# Puzzle Type & Task Name  
**Puzzle Type**: Graph Puzzle  
**Task Name**: hamiltonian_path  

## Task Overview  
This project generates various graph theory problems related to Hamiltonian paths.  
A Hamiltonian path is a path in an undirected graph that visits every vertex exactly once.  
Users must determine whether such a path exists in the given graph.

---

## Supported Difficulty Levels  
- **Easy**: Sparse graphs with straightforward structures.  
- **Medium**: Moderately dense graphs with potential disconnected subgraphs or dead ends.  
- **Hard**: Dense graphs with complex structures, including bridge nodes and sparse connectivity.  

---

## Data Volume  
The dataset includes problems split by language and difficulty levels:  

### English Dataset  
- **Training Set**: 20000
- **Evaluation Set**: 1500

### Chinese Dataset  
- **Training Set**: 20000
- **Evaluation Set**: 1500

---

## Data Difficulty Classification  
Difficulty levels are determined by **number of vertices** and **edge density**:  

- **Easy**:
  - The number of nodes ranges from 10 to 15.
  - The edge density is 0.2.

- **Medium**:
  - The number of nodes ranges from 15 to 20.
  - The edge density is 0.3.

- **Hard**:
  - The number of nodes ranges from 20 to 25.
  - The edge density is 0.4.

---

## Data Generation Logic  
The generator produces two types of problems:  

### 1. Problems Ensuring Hamiltonian Paths  
- **Structure**: A path is explicitly constructed, and additional edges are added randomly to meet the edge density.  
- **Purpose**: Ensures at least one valid Hamiltonian path exists.  

### 2. Problems Preventing Hamiltonian Paths  
- **Key Feature**:  
  Introduces **defects** such as:  
  - **Isolated Nodes**: Some vertices are disconnected entirely, ensuring they cannot participate in any path.  
  - **Disconnected Subgraphs**: Independent components with no connecting edges, making it impossible to traverse the entire graph.  
  - **Dead Ends**: Nodes with very low connectivity, causing traversal to end prematurely.  
  - **Sparse Graph**: Reduces the number of edges significantly, making the graph too sparse to form a Hamiltonian path.  
  - **Critical Bridge Nodes**: A specific node serves as the only bridge between two subgraphs; removing edges around it ensures no Hamiltonian path is possible.  

  These intentional flaws **guarantee the absence of a valid Hamiltonian path**, increasing the problem's complexity.

---

## Usage Guide

### Generate Problems  
Use the `generate()` function to create Hamiltonian path problems.

#### Parameters  
- **`count`**: Number of problems to generate (default: 10).  
- **`difficulty`**: `'easy'`, `'medium'`, or `'hard'` (default: `'medium'`).  
- **`language`**: `'en'` for English, `'zh'` for Chinese (default: `'en'`).  
- **`split`**: Dataset split (`train` or `eval`).  

#### Return Value  
Each generated problem contains the following fields:  
- **`prompt`**: The problem description.  
- **`meta`**: Metadata including the problem type, solution, and reasoning.  
- **`answer`**: The correct answer to the problem.  

#### Example Code  

```python
from your_module import generate

# Generate 10 medium-difficulty Hamiltonian path problems in English
puzzles = generate(
    count=10, 
    difficulty='medium', 
    language='en',
    split="train"
)

# Iterate over and print the generated problems
for puzzle in puzzles:
    print(puzzle)
