PROMPT_TEMPLATE = """
Stack permutation is a permutation problem related to stacks (a last-in, first-out data structure). Given an input sequence, the goal is to generate different output sequences using stack operations (push and pop). A sequence is called a valid stack permutation if it can be obtained through stack operations.

Given a sequence of natural numbers, such as [1, 2, 3, 4], we want to know if a particular output sequence can be obtained through stack operations. The stack operations include:

1. Push: Add numbers from the input sequence to the stack in order.
2. Pop: Remove elements from the top of the stack and add them to the output sequence.

Example:

Suppose the input sequence is [1, 2, 3]. Here are some possible valid stack permutations:

• [1, 2, 3]: Directly push all elements into the stack and then pop them in order.
• [2, 1, 3]: Push 1 and 2 into the stack, pop 2, then pop 1, and finally push and pop 3.
• [3, 2, 1]: Push all elements into the stack, then pop them in reverse order.


Here is the question:
Input sequence: {input_sequence}
Output sequence: {output_sequence}

Please provide the solution according to the requirements below: 

Response format:
- Please output your answer within a code block (```), for example:
```
["Push(1)", "Pop()", "Push(2)", "Push(3)", "Pop()", "Pop()"]
```
- If the output sequence is not a valid stack permutation of the input sequence, output within the code block:
```
"The output sequence is not a valid stack permutation."
```
""".strip()
