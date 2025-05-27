PROMPT_TEMPLATE = """
You are tasked with solving a Kakurasu puzzle.

### Rules:
1. The puzzle is played on a rectangular grid (with arbitrary row and column sizes).
2. Your goal is to "black out" certain cells, following these rules:
   - The black cells in each row must sum up to the target number for that row.
   - The black cells in each column must sum up to the target number for that column.
   - To calculate the row sum:
     - The value of the black cells in each row is determined by their position in the row. For example, the first black cell in a row has a value of 1, the second black cell has a value of 2, and so on.
   - To calculate the column sum:
     - The value of the black cells in each column is determined by their position in the column. For example, the first black cell in a column has a value of 1, the second black cell has a value of 2, and so on.

3. Coordinates are 1-based. For example, the first row is row 1, and the first column is column 1. 

### Task:
Solve the following Kakurasu puzzle by blacking out the cells where needed.
{question}

You must provide the coordinates of the blacked-out cells.

### Response Format:
- Please output your answer within a code block (```), formatted as a list of coordinates, for example:
```
[(1, 1), (2, 4), (4, 3)]
```
- If no solution exists, output within the code block:
```
"No valid solution exists for the given Kakurasu puzzle."
```
""".strip()