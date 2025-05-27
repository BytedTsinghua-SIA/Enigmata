PROMPT_TEMPLATE = """
You are tasked with solving a Hitori puzzle.

### Rules:
1. The puzzle is played on an NxN grid (where N is an even number), with each cell containing a number.
2. Your goal is to "black out" certain cells, following these rules:
   - In each row and column, the same number cannot appear more than once. To eliminate repetitions, you must black out some of the cells.
   - Black cells cannot be adjacent, either horizontally or vertically.
   - All white cells (cells that are not blacked out) must be connected, meaning you can travel between any two white cells through horizontal or vertical moves.

### Task:
Solve the following Hitori puzzle by blacking out the cells where needed.

You must provide the coordinates of the blacked-out cells.

### Response Format:
- Please output your answer within a code block (```), formatted as a list of coordinates, for example:
```
[(0, 0), (1, 3), (3, 2)]
```
- If no solution exists, output within the code block:
```
"No valid solution exists for the given Hitori puzzle."
```

Here is the puzzle: 
{question} """.strip()

PROMPT_TEMPLATE_ZH = """
你需要解决一个 Hitori 数独题目。

### 规则：
1. 该题目在一个 NxN 的网格上进行（N 是偶数），每个格子里包含一个数字。
2. 你的目标是“涂黑”某些格子，遵循以下规则：
   - 每行和每列中，不能有相同的数字出现超过一次。为了消除重复，你必须涂黑一些格子。
   - 涂黑的格子不能相邻，不能水平或垂直相连。
   - 所有未涂黑的格子（即白格）必须是连通的，意味着你可以通过水平或垂直的方式，从一个白格到达另一个白格。

### 任务：
解决以下的 Hitori 数独题目，标出需要涂黑的格子。

你需要提供涂黑格子的坐标。

### 回答格式：
- 请在代码块内(```)输出你的答案，格式为坐标(r, c)列表，例如：
```
[(0, 0), (1, 3), (3, 2)]
```
- 如果没有解，请在代码块内输出：
```
"给定的数独谜题没有有效的解决方案。"
```

请解决以下的题目：
{question}
""".strip()