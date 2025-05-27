PROMPT_TEMPLATE = """
You are provided with a 3x3 Magic Square puzzle. Some cells are filled with numbers, while blank cells are represented by dots. 
Your task is to find a valid solution for the puzzle based on the following rules:

**Rules:**
1.Magic square is a 3x3 partially filled matrix.
2.You need to fill in the blanks in the matrix so that the sum of the numbers in each row, each column, and the two diagonals is equal.
3.You can only fill the blanks with integers, the filled matrix only consists of integers.
4.The filled numbers should not duplicate the already filled numbers.
5.Make sure that the sum of the numbers in each row, each column, and the two diagonals is equal.

**Task:**
- Fill the blank cells according to the given numbers and rules.
- Find a valid magic square solution for the given puzzle.

**Response format:**
- Please output your answer within a code block (```), formatted as a grid of numbers, for example:
```
2 4 3 1
3 1 2 4
4 3 1 2
1 2 4 3
```

Here is the puzzle:
{question}

Please provide the solution according to the requirements above.
""".strip()