PROMPT_TEMPLATE="""
Your task is to decrypt the given ciphertext and provide the corresponding plaintext. You will be given a sample hint that illustrates a pair of ciphertext and its matching plaintext to guide you in solving the puzzle.

Instructions:
1. Analyze the provided ciphertext.
2. Use the sample hint as a reference to understand the encryption pattern or method used.
3. Apply the deciphering technique to convert the ciphertext into plaintext.

Answer Format:
- Please output your answer within a code block (```) as follows:
```
<result>
```
- <result> should be the plaintext string of the given ciphertext, for example:
```
ABCIDEFG
```

Here is the puzzle:

{question} 
""".strip()