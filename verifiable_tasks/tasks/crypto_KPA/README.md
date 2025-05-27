# Puzzle Type & Task Name  
**Puzzle Type**: Cryptographic Puzzle  
**Task Name**: crypto_KPA (Known Plaintext Attack)  

---

## Task Overview  
This project generates cryptographic puzzles simulating **Known Plaintext Attack (KPA)** scenarios. In these puzzles, participants are provided with a ciphertext and a known plaintext-ciphertext hint. The goal is to use the hint and encryption method to decode the given ciphertext. The difficulty of each puzzle is based on **plaintext length**, **hint length**, and other cipher-specific parameters such as **keyword length**, **key complexity**, **matrix size**, or **number of rails**.

---

## Data Volume  
The dataset contains cryptographic puzzles across multiple difficulty levels. Each difficulty level can have a user-defined number of generated puzzles.

Puzzles(en)：
- **Training Set**: 20250 (naive: 4050, easy: 4050, medium: 4050, hard: 4050, extreme: 4050) 
- **Test Set**: 1800 (naive: 360, easy: 360, medium: 360, hard: 360, extreme: 360) 

Puzzles(zh)：
- **Training Set**: 20250 (naive: 4050, easy: 4050, medium: 4050, hard: 4050, extreme: 4050) 
- **Test Set**: 1800 (naive: 360, easy: 360, medium: 360, hard: 360, extreme: 360) 

## Difficulty Levels and Configurations  
The difficulty of each puzzle is defined based on:
1. **Plaintext Length**: The length of the encrypted message.
2. **Hint Length**: The length of the known plaintext-ciphertext pair.
3. **Key Complexity / Keyword Length**: Cipher-specific parameters such as key or keyword length.
4. **Overall Difficulty**: A combination of these factors defines the final difficulty level.  

---

### 1. **Affine Cipher**  
- **Naive**:  
  - Plaintext Length: 5  
  - Hint Length: 120-150  
  - Key: K1 (`a ∈ {3, 5, 7, 9}`)  
- **Easy**:  
  - Plaintext Length: 10  
  - Hint Length: 120-150  
  - Key: K1  
- **Medium**:  
  - Plaintext Length: 10  
  - Hint Length: 120-150  
  - Key: K2 (`a ∈ {11, 15, 17}`)  
- **Hard**:  
  - Plaintext Length: 10  
  - Hint Length: 80-100  
  - Key: K3 (`a ∈ {19, 21, 23, 25}`)  
- **Extreme**:  
  - Plaintext Length: 15  
  - Hint Length: 80-100  
  - Key: K3  

---

### 2. **Vigenère Cipher**  
- **Naive**:  
  - Plaintext Length: 5  
  - Hint Length: 120-150  
  - Keyword Length: 2  
- **Easy**:  
  - Plaintext Length: 10  
  - Hint Length: 120-150  
  - Keyword Length: 3  
- **Medium**:  
  - Plaintext Length: 10  
  - Hint Length: 80-100  
  - Keyword Length: 4  
- **Hard**:  
  - Plaintext Length: 15  
  - Hint Length: 80-100  
  - Keyword Length: 5  
- **Extreme**:  
  - Plaintext Length: 20  
  - Hint Length: 80-100  
  - Keyword Length: 5  

---

### 3. **Caesar Cipher**  
- **Naive**:  
  - Plaintext Length: 5  
  - Hint Length: 120-150  
  - Shift: 1-5  
- **Easy**:  
  - Plaintext Length: 10  
  - Hint Length: 120-150  
  - Shift: 6-10  
- **Medium**:  
  - Plaintext Length: 10  
  - Hint Length: 80-100  
  - Shift: 11-15  
- **Hard**:  
  - Plaintext Length: 15  
  - Hint Length: 80-100  
  - Shift: 16-25  
- **Extreme**:  
  - Plaintext Length: 20  
  - Hint Length: 80-100  
  - Shift: 16-25  

---

### 4. **Hill Cipher**  
- **Naive**:  
  - Plaintext Length: 4  
  - Hint Length: 120-150  
  - Matrix Size: 2x2  
- **Easy**:  
  - Plaintext Length: 8  
  - Hint Length: 120-150  
  - Matrix Size: 2x2  
- **Medium**:  
  - Plaintext Length: 6  
  - Hint Length: 80-100  
  - Matrix Size: 3x3  
- **Hard**:  
  - Plaintext Length: 9  
  - Hint Length: 80-100  
  - Matrix Size: 3x3  
- **Extreme**:  
  - Plaintext Length: 15  
  - Hint Length: 80-100  
  - Matrix Size: 3x3  

---

### 5. **Playfair Cipher**  
- **Naive**:  
  - Plaintext Length: 5  
  - Hint Length: 120-150  
  - Keyword Length: 5  
- **Easy**:  
  - Plaintext Length: 10  
  - Hint Length: 120-150  
  - Keyword Length: 6  
- **Medium**:  
  - Plaintext Length: 10  
  - Hint Length: 80-100  
  - Keyword Length: 7  
- **Hard**:  
  - Plaintext Length: 15  
  - Hint Length: 80-100  
  - Keyword Length: 7  
- **Extreme**:  
  - Plaintext Length: 20  
  - Hint Length: 80-100  
  - Keyword Length: 8  

---

### 6. **Rail Fence Cipher**  
- **Naive**:  
  - Plaintext Length: 5  
  - Hint Length: 120-150  
  - Rails: 2  
- **Easy**:  
  - Plaintext Length: 10  
  - Hint Length: 120-150  
  - Rails: 2  
- **Medium**:  
  - Plaintext Length: 10  
  - Hint Length: 80-100  
  - Rails: 3  
- **Hard**:  
  - Plaintext Length: 15  
  - Hint Length: 80-100  
  - Rails: 3  
- **Extreme**:  
  - Plaintext Length: 20  
  - Hint Length: 80-100  
  - Rails: 4  

---

### 7. **Substitution Cipher**  
- **Naive**:  
  - Plaintext Length: 5  
  - Hint Length: 120-150  
- **Easy**:  
  - Plaintext Length: 10  
  - Hint Length: 120-150  
- **Medium**:  
  - Plaintext Length: 10  
  - Hint Length: 80-100  
- **Hard**:  
  - Plaintext Length: 15  
  - Hint Length: 80-100  
- **Extreme**:  
  - Plaintext Length: 20  
  - Hint Length: 80-100  

---

### 8. **Atbash Cipher**  
- **Naive**:  
  - Plaintext Length: 5  
  - Hint Length: 120-150  
- **Easy**:  
  - Plaintext Length: 10  
  - Hint Length: 120-150  
- **Medium**:  
  - Plaintext Length: 10  
  - Hint Length: 80-100  
- **Hard**:  
  - Plaintext Length: 15  
  - Hint Length: 80-100  
- **Extreme**:  
  - Plaintext Length: 20  
  - Hint Length: 80-100  

---

### 9. **Autokey Cipher**  
- **Naive**:  
  - Plaintext Length: 5  
  - Hint Length: 120-150  
  - Keyword Length: 2  
- **Easy**:  
  - Plaintext Length: 10  
  - Hint Length: 120-150  
  - Keyword Length: 3  
- **Medium**:  
  - Plaintext Length: 10  
  - Hint Length: 80-100  
  - Keyword Length: 4  
- **Hard**:  
  - Plaintext Length: 15  
  - Hint Length: 80-100  
  - Keyword Length: 5  
- **Extreme**:  
  - Plaintext Length: 20  
  - Hint Length: 80-100  
  - Keyword Length: 5  

---

## How to Generate Puzzles

Use the `generate()` function to create encryption puzzles with your desired parameters.

### Parameters

- **`count`**: Number of puzzles to generate (default: 100).
- **`difficulty`**: `'naive'`, `'easy'`, `'medium'`, `'hard'` or `'extreme'` (default: `'medium'`).
- **`language`**: `'en'` for English, `'zh'` for Chinese (default: `'en'`).
- **`method`**: Encryption method – `'vigenere'`, `'substitution'`, `'rail_fence'`, `'playfair'`, `'hill'`, `'affine'`, `'caesar'`, `'autokey'`, or `'atbash'` (default: `'caesar'`).
- **`split`**: train/eval

The `generate()` function yields a dictionary containing:

- **`prompt`**: The puzzle question.
- **`meta`**: Metadata including solution details.
- **`answer`**: The correct answer to the puzzle.

### Example

```python
from your_module import generate

# Generate 10 medium-difficulty Vigenère cipher puzzles in English
puzzles = generate(
    count=10, 
    difficulty='medium', 
    language='en', 
    method='vigenere',
    split="train"
)

# Iterate over the puzzles and print them
for puzzle in puzzles:
    print(puzzle)

