# Puzzle Type & Task Name
**Puzzle Type**: Crosswords Puzzle  
**Task Name**: full crosswords

## Task Overview
This task involves solving a **crossword puzzle** by filling in the provided grid with the correct words based on the given clues. The goal is to ensure that all across and down words are valid, meaningful, and match at intersections. Participants must strictly follow the grid layout without altering any blocked spaces (`'*'`).

## Data Volume
- **Training Set**: 19000 samples (9500 easy, 9500 medium)
- **Test Set**: 1500 samples (500 easy, 1500 medium(3 types))

## Data Difficulty Classification (easy/medium/hard)
We classify full crossword puzzles based on the shape of grids:

1. easy
    ```python
    _ _ _ _ _
    _ * _ * _
    _ _ _ _ _
    _ * _ * _
    _ _ _ _ _
    ```
    
2. medium

    ```python
    _ _ _ _ _ _ _
    _ * _ * _ * _
    _ _ _ _ _ _ _
    _ * _ * _ * _
    _ _ _ _ _ _ _
    _ * _ * _ * _
    _ _ _ _ _ _ _
    ```

    ```python

    * _ * _ * _ *
    _ _ _ _ _ _ _
    * _ * _ * _ *
    _ _ _ _ _ _ _
    * _ * _ * _ *
    _ _ _ _ _ _ _
    * _ * _ * _ *
    ```

    ```python
    _ _ _ _ _ _ _
    * _ _ * _ _ *
    _ _ _ _ _ _ _
    * _ _ * _ _ *
    _ _ _ _ _ _ _
    * _ _ * _ _ *
    _ _ _ _ _ _ _
    ```


You can download the dataset from [full_crossword_puzzles](https://huggingface.co/datasets/jeggers/full_crossword_puzzles)