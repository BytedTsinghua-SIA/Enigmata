PROMPT_TEMPLATE = """
You are tasked with solving a Car Painting Problem.

In the Car Painting Problem, you play the role of a scheduler at a car painting factory. Your job is to arrange the painting sequence for a batch of cars to minimize the number of color switches, reducing paint waste and production time.

### Rules:
1. There are N cars numbered from 1 to N that need to be painted.
2. Each car has a predetermined color (labeled as A, B, C, etc., for a total of M colors).
3. Cars enter the painting workshop in a fixed order, but can be rearranged within a range.
4. Each car can be moved forward or backward by at most K positions from its original position.
5. A color switch occurs when two adjacent cars have different colors, adding to the cost.
6. Your goal is to minimize the number of color switches by optimally arranging the cars.

### Task:
Find a rearranged sequence of cars that minimizes the number of color switches.

You must provide a list of car IDs in their new order (rearranged to minimize color switches).

Given the following information:
- Number of Cars (N): {n}
- Number of Colors (M): {m}
- Maximum Movement Range (K): {k}
- Initial car sequence: {car_ids}
- Corresponding colors: {colors}

Please find a rearranged car sequence that minimizes the number of color switches.
Remember: Each car can only be moved at most {k} positions forward or backward from its original position.

### Response Format:
- Please output your answer within a code block (```), formatted as an array of integers representing the new order of car IDs, for example:
```
[2, 3, 1, 5, 8, 4, 6, 9, 7, 10]
```

""".strip()