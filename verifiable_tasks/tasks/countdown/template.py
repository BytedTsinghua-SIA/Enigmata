PROMPT_TEMPLATE = """Solution for the Countdown Number Game

# Description:
You are given {num_count} integers and a target number. Your task is to create an arithmetic expression that results in exactly the target number.

# Rules:
- You must use ALL the given numbers, each exactly once.
- The operators you can use include: addition (+), subtraction (-), multiplication (*), and division (/).
- You can use parentheses to change the order of operations.
- All intermediate results must be positive integers (no fractions or negative numbers allowed).

**Response format:**
- Please output your answer within a code block (```) as follows:
```
<result>
```
- If there is a solution, <result> is the sequence of numbers and operators that results in the target, for example:
```
(8 / 2) * (8 - 2)
```
- If there is no solution, <result> is "cannot form {target}".

# Input:
Numbers: {numbers}
Target: {target}

Please provide a solution according to the above rules and input."""