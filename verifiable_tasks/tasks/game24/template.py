PROMPT_TEMPLATE = """Solution for the 24 Game

# Description:
You are given four or five or six integers, ranging from 1 to 13, provide an arithmetic expression that results in 24.

# Rules:

You must use all the given numbers, each exactly once.
The operators you can use include: addition (+), subtraction (-), multiplication (*), and division (/).
You can use parentheses to change the order of operations.

**Response format:**
- Please output your answer within a code block (```) as follows:
```
<result>
```
- If there is a solution, <result> is the sequence of numbers and operators that results in 24, for example: 
```
(8 / 2) * (8 - 2)
```
- If there is no solution, <result> is "cannot form 24".

# Input:
{question}

Please provide a solution for the 24 game according to the above rules and input."""

