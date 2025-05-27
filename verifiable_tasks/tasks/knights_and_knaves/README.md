# Puzzle Type & Task Name
**Puzzle Type**: Logic Puzzle  
**Task Name**: Knights and Knaves

## Task Overview
In the **Knights and Knaves** task, you will be presented with logic puzzles involving inhabitants of an island. Each inhabitant is either a **knight**, who always tells the truth, or a **knave**, who always lies. Your task is to determine the truth value of a given statement based on the provided information.

## Data Volume
- **Train Set**: 3414 samples (926 easy, 1724 medium, 764 hard)
- **Test Set**: 600 samples (200 easy, 200 medium, 200 hard)

## Data Difficulty Classification (easy/medium/hard)
For ambiguous puzzle: medium
For unambiguous puzzle:determined by the number of inhabitants involved in the scenario:
1. Easy: Puzzles that involve two to five inhabitants. These puzzles require straightforward logical deductions and involve fewer participants, making it easier to evaluate the truth of statements.
2. Medium: Puzzles that involve six or seven inhabitants. These puzzles increase in complexity as more characters are involved, requiring more intricate reasoning.
3. Hard: Puzzles that involve eight or more inhabitants. These puzzles are more challenging as they involve more participants and require advanced logical deductions and multi-step reasoning.

You can download the dataset from [puzzte](https://huggingface.co/datasets/tasksource/puzzte)