PROMPT_TEMPLATE = """
Your task is to complete the crossword puzzle grid based on the given clues. **Ensure that all words are meaningful and semantically valid.** The grid consists of **fillable blank spaces** ('_') and **blocked spaces** ('*'). You must strictly follow the provided grid layout, with no modifications allowed.

### Puzzle Rules:
1. **Completing the Grid:**
   - Fill each blank space ('_') with a letter to form valid words according to the given clues.
   - Blocked spaces ('*') must remain unchanged and cannot contain any letters.
   - The number of rows and columns must match the provided grid exactly.
   - All blank spaces ('_') must be filled—no empty spaces are allowed.

2. **Clue Mapping Logic:**
   - **Across Clues:**
     - Rows without '*' characters represent across words. These words correspond to across clues in order from top to bottom.
     - Rows containing '*' do not correspond to any across word or clue.

   - **Down Clues:**
     - Columns without '*' characters represent down words. These words correspond to down clues in order from left to right.
     - Columns containing '*' do not correspond to any down word or clue.

3. **Matching Letters at Intersections:**
   - Letters at the intersections of across and down words must match, ensuring valid words are formed both horizontally and vertically.

### Answer Format:

- Please output your answer within a code block (```) as follows:
```
across: ANSWER1, ANSWER2, ..., ANSWER_N
down: ANSWER1, ANSWER2,..., ANSWER_N
```

- "across" contains the list of across words, ordered from top to bottom.
- "down" contains the list of down words, ordered from left to right.
---

Here is the crosswords puzzle:
{question} 
""".strip()

