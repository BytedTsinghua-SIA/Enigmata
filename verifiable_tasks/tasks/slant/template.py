PROMPT_TEMPLATE = """
You need to solve a Slant puzzle.

### Rules
1. **Grid Numbers**:
   - Each cell in the grid may contain a number, indicating how many diagonal lines meet at that intersection. The number ranges from 0 to 4, representing the number of intersecting diagonal lines.
2. **Diagonal Line Rules**:
   - Each cell must contain one diagonal line, either a "/" (forward slash, representing top-left to bottom-right) or a "\" (backslash, representing top-right to bottom-left).
3. **Intersection Numbers**:
   - The number indicates how many diagonal lines meet at that intersection. For example:
     - **Number 1**: Indicates 1 diagonal line intersects at that point.
     - **Number 2**: Indicates 2 diagonal lines intersect at that point.
     - **Number 0**: Indicates no diagonal lines intersect at that point.
     - **Numbers 3 and 4**: Represent 3 and 4 intersecting diagonal lines, respectively.
4. **No Loops**:
   - The diagonal lines must not form loops. All diagonal lines must connect, and no closed cycle can be formed.

### Puzzle
Solve the following slant puzzle:
{question}

### Answer Format:
- Please output your answer within a code block (```), formatted as a grid of numbers, for example:
```
1 1 1 1
-1 1 -1 1
1 -1 -1 1
```
- 1 represents “/” (forward slash, top-left to bottom-right)
- -1 represents “" (backslash, top-right to bottom-left)

""".strip()