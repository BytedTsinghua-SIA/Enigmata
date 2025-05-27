PROMPT_TEMPLATE = """
You are tasked with finding a move in the chess position resulting in checkmate:

### Response Format:
- Please output your answer within a code block (```) as follows, for example:
```
Rg5#
```

Here is the chess position:
{question}

""".strip()

