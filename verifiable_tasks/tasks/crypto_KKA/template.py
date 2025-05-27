PROMPT_TEMPLATE = """
Your task is to apply the provided decryption rules to decipher the given ciphertext.

### Instructions:
1. **Review the decryption rules** carefully to understand how the encryption method works.
2. **Decrypt the provided ciphertext** according to the rules, and derive the correct plaintext.

### Answer Format:
- Please output your answer within a code block (```) as follows:
```
<result>
```
- <result> should be the decrypted plaintext corresponding to the given ciphertext, for example:
```
LOVE
```

Here is the puzzle:
{question} 
""".strip()
