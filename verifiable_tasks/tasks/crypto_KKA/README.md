# Puzzle Type & Task Name  
**Puzzle Type**: Cryptographic Puzzle  
**Task Name**: crypto_KKA  (Known Key Attack)

## Task Overview  
This project generates various cryptographic puzzles using multiple classical ciphers. Each puzzle involves encrypting plaintext with a given cipher and parameters. The task for participants is to decrypt the provided ciphertext based on the encryption method and derive the correct plaintext.

## Supported Ciphers and Configurations  
- **Affine Cipher**  
- **Vigenère Cipher**  
- **Caesar Cipher**  
- **Hill Cipher**  
- **Playfair Cipher**  
- **Rail Fence Cipher**  
- **Atbash Cipher**  
- **Autokey Cipher**  
- **Substitution Cipher**  

Each cipher type supports different configurations and difficulty levels, as described below.

## Data Volume  
The dataset contains cryptographic puzzles across multiple difficulty levels. Each difficulty level can have a user-defined number of generated puzzles.

Puzzles(en)：
- **Training Set**: 19800 (naive: 4950, easy: 4950, medium: 4950, hard: 4950) 
- **Test Set**: 1800 (naive: 450, easy: 450, medium: 450, hard: 450) 

Puzzles(zh)：
- **Training Set**: 19800 (naive: 4950, easy: 4950, medium: 4950, hard: 4950) 
- **Test Set**: 1800 (naive: 450, easy: 450, medium: 450, hard: 450) 

## Data Difficulty Classification  
Puzzles are classified based on **key complexity** and **plaintext length**. The following mappings describe the difficulty configuration for each cipher:

### 1. **Affine Cipher**  
- **K1**: Simple keys (`a ∈ {3, 5, 7, 9}`)  
- **K2**: Moderate keys (`a ∈ {11, 15, 17}`)  
- **K3**: Complex keys (`a ∈ {19, 21, 23, 25}`)  

**Length-based Difficulty Mapping**:
- **Mini**: 2 characters, K1 keys  
- **Easy**: 5 characters, K1 keys  
- **Medium**: 10 characters, K2 keys  
- **Hard**: 15 characters, K3 keys  

### 2. **Vigenère Cipher**  
- **Mini**: 2 characters, keyword length 2  
- **Easy**: 5 characters, keyword length 3  
- **Medium**: 8 characters, keyword length 4  
- **Hard**: 12 characters, keyword length 5  

### 3. **Caesar Cipher**  
- **Mini**: 5 characters, shift 1-5  
- **Easy**: 10 characters, shift 6-10  
- **Medium**: 15 characters, shift 11-15  
- **Hard**: 20 characters, shift 16-25  

### 4. **Hill Cipher**  
- **Mini**: 2 characters, matrix size 2x2  
- **Easy**: 4 characters, matrix size 2x2  
- **Medium**: 6 characters, matrix size 3x3  
- **Hard**: 9 characters, matrix size 3x3  

### 5. **Playfair Cipher**  
- **Mini**: 2 characters, keyword length 5  
- **Easy**: 6 characters, keyword length 6  
- **Medium**: 10 characters, keyword length 7  
- **Hard**: 20 characters, keyword length 8  

### 6. **Rail Fence Cipher**  
- **Mini**: 3 characters, 2 rails  
- **Easy**: 5 characters, 2 rails  
- **Medium**: 10 characters, 3 rails  
- **Hard**: 15 characters, 4 rails  

### 7. **Atbash Cipher**  
- **Mini**: 10 characters  
- **Easy**: 15 characters  
- **Medium**: 20 characters  
- **Hard**: 25 characters  

### 8. **Autokey Cipher**  
- **Mini**: 3 characters, keyword length 2  
- **Easy**: 5 characters, keyword length 3  
- **Medium**: 10 characters, keyword length 4  
- **Hard**: 15 characters, keyword length 5  

### 9. **Substitution Cipher**  
- **Mini**: 1 character  
- **Easy**: 5 characters  
- **Medium**: 10 characters  
- **Hard**: 15 characters  

## Classification Logic  
1. **Plaintext Length**: Longer plaintexts increase puzzle difficulty.  
2. **Key Complexity**: Higher key levels or longer keywords make decryption more challenging.  
3. **Overall Difficulty**: A combination of plaintext length and key difficulty determines the final difficulty label.

---

## How to Generate Puzzles

Use the `generate()` function to create encryption puzzles with your desired parameters.

### Parameters

- **`count`**: Number of puzzles to generate (default: 100).
- **`difficulty`**: `'naive'`, `'easy'`, `'medium'`, or `'hard'` (default: `'medium'`).
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