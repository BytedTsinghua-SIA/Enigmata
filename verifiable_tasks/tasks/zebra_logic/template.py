PROMPT_TEMPLATE="""
You are tasked with solving a grid puzzle. This type of puzzle requires careful analysis of the provided background information and clues to deduce the correct arrangement of elements in a grid format. Follow the steps below to solve the puzzle and present your solution in the specified format.

1. **Background Information:** Carefully read any introductory information provided with the puzzle. This may include context or specific constraints that apply to the puzzle.

2. **Clues:** Analyze each clue given. These clues will guide you in determining the relationships between different elements in the grid.

3. **Logical Deduction:** Use logical reasoning to deduce the correct placement of each element in the grid. Consider all possible options and eliminate those that contradict the clues.

4. **Consistency Check:** Ensure that your solution is consistent with all the clues and background information provided.

Your response should include a solution followed by the final answer in a markdown table format. Use the following structure:

Assume column 1 is Year, column 2 is Wine, column 3 is Type.

Final Answer:
```
| 1984 | [Correct Wine] | [Correct Type] |
| 1988 | [Correct Wine] | [Correct Type] |
| 1992 | [Correct Wine] | [Correct Type] |
| 1996 | [Correct Wine] | [Correct Type] |
```

Here is the puzzle:

{question}

You must stick to the given uncompleted table and must not transpose the table.
""".strip()
