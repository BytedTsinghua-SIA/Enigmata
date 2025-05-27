PROMPT_TEMPLATE = """
Apply a function to the final input list to generate the output list. Use any preceding inputs and outputs as examples to find what is the function used. All example outputs have been generated using the same function.

### Response Format:
- Please output your answer within a code block (```), formatted as a list of numbers, for example:
```
[0, 2, 3]
```
""".strip()