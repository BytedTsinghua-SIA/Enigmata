PROMPT_TEMPLATE="""
In this puzzle, you are presented with a scenario involving inhabitants of an island where each person is either a knight or a knave. Knights always tell the truth, while knaves always lie. Your task is to determine the truth value of a given statement based on the information provided.

### Rules:
1. Knights always tell the truth.
2. Knaves always lie.
3. Use logical reasoning to determine the truth value of the statement.

### Answer Format:
- Please output your answer within a code block (```) as follows:
```
<result>
```

**<result> Options:**
- "Entailment": Use this if the statement is logically true based on the information provided.
- "Contradiction": Use this if the statement contradicts known facts or logical deductions.
- "Unknown": Use this if the truth value of the statement cannot be determined with the given information.

Here is the puzzle:
{question} 
""".strip()

