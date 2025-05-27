# Puzzle Type & Task Name  
**Puzzle Type**: Graph Puzzle  
**Task Name**: hamiltonian_cycle  

## Task Overview  
This project generates various graph theory problems related to Hamiltonian cycles.  
A Hamiltonian cycle is a cycle in an undirected graph that visits every vertex exactly once and returns to the starting vertex.  
Users must determine whether such a cycle exists in the provided graph.  

---

## Supported Difficulty Levels  
- **Easy**: Sparse graphs with straightforward structures.  
- **Medium**: Moderately dense graphs with potential small subcycles or uneven degree distribution.  
- **Hard**: Dense graphs with complex structures, including bridge nodes and disconnected components.  

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

### 1. Problems Ensuring Hamiltonian Cycles  
- **Structure**: A cycle is explicitly constructed, and additional edges are added randomly to meet the edge density.  
- **Purpose**: Ensures at least one valid Hamiltonian cycle exists.  

### 2. Problems Preventing Hamiltonian Cycles  
- **Key Feature**:  
  Introduces **defects** such as:  
  - **Isolated Nodes**: Some vertices are disconnected entirely, ensuring they cannot participate in any cycle.  
  - **Missing Edges**: Critical connections between vertices in the cycle are removed, breaking the possibility of completing a Hamiltonian cycle.  
  - **Multiple Small Cycles**: Creates independent subgraphs or disconnected components that form separate smaller cycles, making a single Hamiltonian cycle impossible.  
  - **Sparse Graph**: Reduces the number of edges significantly, making the graph too sparse to form a Hamiltonian cycle.  
  - **Dead Ends**: Some nodes are designed to have very low connectivity, making it impossible to traverse them as part of a complete cycle.  
  - **Unbalanced Degree Distribution**: Intentionally skews the degree of certain nodes, making it mathematically impossible to include all nodes in a single cycle.  
  - **Critical Bridge Nodes**: A specific node serves as the only bridge between two subgraphs; removing edges around it ensures no Hamiltonian cycle is possible.  

  These intentional flaws **guarantee the absence of a valid Hamiltonian cycle**, increasing the problem's complexity.

---

## Usage Guide

### Generate Problems  
Use the `generate()` function to create Hamiltonian cycle problems.

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

# Generate 10 medium-difficulty Hamiltonian cycle problems in English
puzzles = generate(
    count=10, 
    difficulty='medium', 
    language='en',
    split="train"
)

# Iterate over and print the generated problems
for puzzle in puzzles:
    print(puzzle)
