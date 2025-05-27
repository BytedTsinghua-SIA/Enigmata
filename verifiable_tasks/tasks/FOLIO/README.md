# Puzzle Type & Task Name
**Puzzle Type**: Logic Puzzle
**Task Name**: FOLIO

## Task Overview
In the **FOLIO** task, you will be presented with logic puzzles that require you to analyze a set of premises and evaluate the validity of a given conclusion. These puzzles test your reasoning and logical deduction skills by asking you to determine whether the conclusion is **True**, **False**, or **Unknown** based solely on the provided premises.

## Data Volume
- **Test Set**: 1208 samples (741 easy, 303 medium, 164 hard)

## Data Difficulty Classification (easy/medium/hard)
The difficulty of the logic puzzles is determined by the number of premises provided:

1. Easy: Puzzles with 5 or fewer premises. These puzzles have straightforward premises that require minimal reasoning to reach a conclusion.
2. Medium: Puzzles with 6 remises. These puzzles involve more complex reasoning, requiring multiple premises to be combined or interpreted.
3. Hard: Puzzles with more than 6 premises. These puzzles are more challenging and require advanced reasoning, often involving several steps or intricate logical deductions.

Here's the script used to determine the difficulty of each puzzle:

```python
def get_difficulty_level(premises_count):
    if premises_count <= 5:
        return "easy"
    elif premises_count == 6:
        return "medium"
    else:
        return "hard"

You can download the dataset from [FOLIO](https://github.com/Yale-LILY/FOLIO)