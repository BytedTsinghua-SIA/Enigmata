PROMPT_TEMPLATE="""
Analyze the given premises and determine the validity of the conclusion. Your task is to assess whether the conclusion is "True," "False," or "Unknown" based on the information provided.

### Rules:
1. **Premises:** You will be provided with a set of statements or premises. These premises are the foundational truths or assumptions for the puzzle.
2. **Conclusion:** A statement will be presented as the conclusion. Your task is to evaluate this conclusion in the context of the given premises.
3. **Evaluation Criteria:**
   - **True:** The conclusion logically follows from the premises.
   - **False:** The conclusion contradicts the premises.
   - **Unknown:** The conclusion cannot be determined from the premises alone due to insufficient information.

### Answer Format:
- Please output your answer within a code block (```) as follows:
```
<result>
```
- Replace `<result>` with one of the following options: "True", "False", or "Unknown".


Here is the puzzle:

{question} 

**Note:** Ensure that your evaluation is based solely on the information provided in the premises without introducing external knowledge or assumptions.
""".strip()

