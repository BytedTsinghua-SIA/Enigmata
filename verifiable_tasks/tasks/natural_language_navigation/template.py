PROMPT_TEMPLATE="""
You are tasked with solving a spatial reasoning puzzle involving navigation in a city. Follow these guidelines to determine the shortest path to a specific landmark:

1. **Landmarks Definition:**
   - Identify a set of landmarks which include: store, bank, house, cinema, garden, and school.
   - The total number of landmarks in the puzzle will range from 7 to 10.

2. **Structure:**
   - The landmarks are organized in a binary tree structure.
   - The root node of this tree represents the starting point for navigation.

3. **Objective:**
   - Your goal is to find the shortest path from the starting point to the nearest specified type of landmark.

4. **Puzzle Input:**
   - You will receive a question.
   - Use the information provided in the question to determine the path.

5. **Answer Format:**
- Please output your answer "([A-Z, ]+)" within a code block (```), containing only the path letters, for example:
```
EFJ
```
- Your answer should only include the uppercase letters representing the landmarks in the path.
- If the path is direct with no intermediate landmarks, provide an empty code block:
```
```

Here is the puzzle:
{question}
Please provide the solution according to the requirements above.
""".strip()

