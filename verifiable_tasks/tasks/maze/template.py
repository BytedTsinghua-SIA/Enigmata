PROMPT_TEMPLATE = """Given a 5x5 maze map, as shown below:

{question}

Where:
S represents the start point (located in the top-left corner at coordinates (1, 1))
E represents the end point (located in the bottom-right corner at coordinates (5, 5))
B represents an obstacle (impassable)
. represents open space (passable)

Rules:
1.You can only move up, down, left, or right, not diagonally.
2.You cannot pass through obstacles (B).
3.You can move freely on open spaces (.).
4.The goal is to find a path from the start point (S) to the end point (E).

Please find a valid path from the start point (S) to the end point (E). If there are multiple paths, provide any one of them. If no valid path exists, state that it is impossible to reach the end point.

**Response format:**
- Please output your answer within a code block (```) as follows:
```
<result>
```
- If there is a path, <result> is the sequence of coordinates in the path. For example: 
```
(1,1)->(1,3)->(3, 5)
```
- If no path exists, output directly: 
```
not exist the path from start to end.
```

Please provide the solution according to the requirements above.
"""