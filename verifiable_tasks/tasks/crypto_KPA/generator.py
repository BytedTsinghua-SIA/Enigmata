import random
import string
import numpy as np
import json
import pandas as pd
from .template import PROMPT_TEMPLATE
from tqdm import tqdm
import hashlib
import time 

QUESTION_TEMPLATE = """
hint: {hint}
Use the example above to decode:
{ciphertext}
""".strip()

df_plaintext = pd.read_csv("verifiable_tasks/tasks/crypto_KPA/sentences_plaintext.csv")
df_hint = pd.read_csv("verifiable_tasks/tasks/crypto_KPA/sentences_hint.csv")

def get_plaintext_of_length(n):
    while True:
        selected_text = df_plaintext.sample(n=1).iloc[0]['sentence']
        cleaned_text = ''.join([char for char in selected_text if char.isalpha()])
        if len(cleaned_text) >= n:
            start_idx = random.randint(0, len(cleaned_text) - n)
            return cleaned_text[start_idx:start_idx + n].upper()
        
def get_hint_of_length(n):
    while True:
        selected_text = df_hint.sample(n=1).iloc[0]['sentence']
        cleaned_text = ''.join([char for char in selected_text if char.isalpha()])
        if len(cleaned_text) >= n:
            start_idx = random.randint(0, len(cleaned_text) - n)
            return cleaned_text[start_idx:start_idx + n].upper()

# Affine Cipher
def affine_encrypt(plaintext, a, b):
    ciphertext = [
        chr(((a * (ord(char) - ord('A')) + b) % 26) + ord('A')) for char in plaintext
    ]
    return ''.join(ciphertext)

def generate_affine_problem(language, plaintext_length, hint_range, key_difficulty, difficulty_label):
    if key_difficulty == 'K1': 
        a = random.choice([3, 5, 7, 9])
    elif key_difficulty == 'K2': 
        a = random.choice([11, 15, 17])
    else:  
        a = random.choice([19, 21, 23, 25])
    
    b = random.randint(0, 25)  
    
    ques_plaintext = get_plaintext_of_length(plaintext_length)
    ques_ciphertext = affine_encrypt(ques_plaintext, a, b)
    
    hint_length = random.randint(hint_range[0], hint_range[1])
    hint_plaintext = get_plaintext_of_length(hint_length)
    hint_ciphertext = affine_encrypt(hint_plaintext, a, b)

    hint = (f"Known plaintext and ciphertext pair:\n"
            f"Plaintext: '{hint_plaintext}'\n"
            f"Ciphertext: '{hint_ciphertext}'\n")

    solution = (f"Encryption method: Affine cipher\n"
                f"a: {a}, b: {b}")

    return {
        "ciphertext": ques_ciphertext,
        "plaintext": ques_plaintext,
        "hint": hint,
        "solution": solution,
        "method": "affine",
        "difficulty": f"{difficulty_label}" 
    }

# Atbash Cipher
def atbash_encrypt(plaintext):
    plaintext = ''.join([c for c in plaintext if c.isalpha()]).upper()
    standard_alphabet = string.ascii_uppercase
    reversed_alphabet = standard_alphabet[::-1]
    cipher_table = str.maketrans(standard_alphabet, reversed_alphabet)
    ciphertext = plaintext.translate(cipher_table)
    return ciphertext

def generate_atbash_problem(language, plaintext_length, hint_range, difficulty_label):
    ques_plaintext = get_plaintext_of_length(plaintext_length)
    ques_ciphertext = atbash_encrypt(ques_plaintext)
    
    hint_length = random.randint(hint_range[0], hint_range[1])
    hint_plaintext = get_plaintext_of_length(hint_length)
    hint_ciphertext = atbash_encrypt(hint_plaintext)
    
    hint = (f"Known plaintext and ciphertext pair:\n"
            f"Plaintext: '{hint_plaintext}'\n"
            f"Ciphertext: '{hint_ciphertext}'\n")

    solution = {
        "method": "Atbash Cipher"
    }

    return {
        "ciphertext": ques_ciphertext,
        "plaintext": ques_plaintext,
        "hint": hint,
        "solution": solution,
        "method": "atbash",
        "difficulty": difficulty_label
    }

# Autokey Cipher
def generate_autokey_random_keyword(length):
    letters = string.ascii_uppercase
    keyword = ''.join(random.choice(letters) for _ in range(length))
    return keyword

def autokey_encrypt(plaintext, keyword):
    plaintext = ''.join([c for c in plaintext if c.isalpha()]).upper()
    keyword = keyword.upper()
    keystream = keyword + plaintext  
    key_length = len(keystream)
    keystream_int = [ord(i) - ord('A') for i in keystream]
    plaintext_int = [ord(i) - ord('A') for i in plaintext]
    ciphertext = ''
    for i in range(len(plaintext_int)):
        value = (plaintext_int[i] + keystream_int[i]) % 26
        ciphertext += chr(value + ord('A'))
    return ciphertext

def generate_autokey_problem(language, plaintext_length, hint_range, keyword_length, difficulty_label):
    keyword = generate_autokey_random_keyword(keyword_length)
    ques_plaintext = get_plaintext_of_length(plaintext_length)
    ques_ciphertext = autokey_encrypt(ques_plaintext, keyword)
    
    hint_length = random.randint(hint_range[0], hint_range[1])
    hint_plaintext = get_plaintext_of_length(hint_length)
    hint_ciphertext = autokey_encrypt(hint_plaintext, keyword)
    
    hint = (f"Known plaintext and ciphertext pair:\n"
            f"Plaintext: '{hint_plaintext}'\n"
            f"Ciphertext: '{hint_ciphertext}'\n")

    solution = {
        "method": "Autokey Cipher",
        "keyword": keyword
    }

    return {
        "ciphertext": ques_ciphertext,
        "plaintext": ques_plaintext,
        "hint": hint,
        "solution": solution,
        "method": "autokey",
        "difficulty": difficulty_label
    }

# Caesar Cipher
def caesar_encrypt(plaintext, shift):
    return ''.join(
        chr((ord(char) - ord('A') + shift) % 26 + ord('A')) for char in plaintext
    )

def generate_caesar_problem(language, plaintext_length, hint_range, difficulty_label):
    shift = random.randint(1, 25)
    ques_plaintext = get_plaintext_of_length(plaintext_length)
    ques_ciphertext = caesar_encrypt(ques_plaintext, shift)
    
    hint_length = random.randint(hint_range[0], hint_range[1])
    hint_plaintext = get_plaintext_of_length(hint_length)
    hint_ciphertext = caesar_encrypt(hint_plaintext, shift)
    
    hint = (f"Known plaintext and ciphertext pair:\n"
            f"Plaintext: '{hint_plaintext}'\n"
            f"Ciphertext: '{hint_ciphertext}'\n")

    solution = {
        "method": "Caesar Cipher",
        "shift": shift
    }

    return {
        "ciphertext": ques_ciphertext,
        "plaintext": ques_plaintext,
        "hint": hint,
        "solution": solution,
        "method": "caesar",
        "difficulty": difficulty_label
    }

# Hill Cipher
def generate_hill_matrix(size):
    while True:
        matrix = np.random.randint(0, 26, (size, size))
        det = int(round(np.linalg.det(matrix)))
        if det % 26 != 0 and np.gcd(det % 26, 26) == 1:
            return matrix

def hill_encrypt(plaintext, key_matrix):
    plaintext = plaintext.upper().replace(' ', '')
    while len(plaintext) % key_matrix.shape[0] != 0:
        plaintext += 'X'

    plaintext_nums = [ord(char) - ord('A') for char in plaintext]

    ciphertext = ''
    for i in range(0, len(plaintext_nums), key_matrix.shape[0]):
        block = plaintext_nums[i:i+key_matrix.shape[0]]
        block_vector = np.array(block).reshape(-1, 1)
        cipher_vector = np.dot(key_matrix, block_vector) % 26
        cipher_chars = ''.join([chr(int(num) + ord('A')) for num in cipher_vector.flatten()])
        ciphertext += cipher_chars
    return ciphertext

def generate_hill_problem(language, plaintext_length, hint_range, matrix_size, difficulty_label):
    matrix = generate_hill_matrix(matrix_size)
    ques_plaintext = get_plaintext_of_length(plaintext_length)
    ques_ciphertext = hill_encrypt(ques_plaintext, matrix)
    
    hint_length = random.randint(hint_range[0], hint_range[1])
    hint_plaintext = get_plaintext_of_length(hint_length)
    hint_ciphertext = hill_encrypt(hint_plaintext, matrix)
    
    hint = (f"Known plaintext and ciphertext pair:\n"
            f"Plaintext: '{hint_plaintext}'\n"
            f"Ciphertext: '{hint_ciphertext}'\n")

    solution = {
        "method": "Hill Cipher",
        "matrix": matrix.tolist()
    }

    return {
        "ciphertext": ques_ciphertext,
        "plaintext": ques_plaintext,
        "hint": hint,
        "solution": solution,
        "method": "hill",
        "difficulty": difficulty_label
    }

def generate_playfair_key(keyword):
    keyword = ''.join(dict.fromkeys(keyword.upper().replace('J', 'I'))) 
    alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
    key_square = [char for char in keyword if char in alphabet] + [c for c in alphabet if c not in keyword]
    return [key_square[i:i + 5] for i in range(0, 25, 5)]

def generate_playfair_random_keyword(length):
    letters = list(string.ascii_uppercase.replace('J', ''))
    random.shuffle(letters)
    keyword = ''.join(letters[:length])
    return keyword

def playfair_encrypt(plaintext, key_matrix):
    def find_position(letter):
        for i, row in enumerate(key_matrix):
            if letter in row:
                return i, row.index(letter)
        raise ValueError(f"Letter '{letter}' not found in key matrix.")
    def encrypt_pair(a, b):
        a_row, a_col = find_position(a)
        b_row, b_col = find_position(b)
        if a_row == b_row:  
            return key_matrix[a_row][(a_col + 1) % 5], key_matrix[b_row][(b_col + 1) % 5]
        elif a_col == b_col:  
            return key_matrix[(a_row + 1) % 5][a_col], key_matrix[(b_row + 1) % 5][b_col]
        else: 
            return key_matrix[a_row][b_col], key_matrix[b_row][a_col]
    plaintext = ''.join([c for c in plaintext if c.isalpha()]).upper().replace('J', 'I')
    i = 0
    pairs = []
    while i < len(plaintext):
        a = plaintext[i]
        if i + 1 < len(plaintext):
            b = plaintext[i + 1]
            if a == b:
                b = 'X'
                i += 1  
            else:
                i += 2
        else:
            b = 'X'
            i += 1
        pairs.append((a, b))
    ciphertext = ''.join(''.join(encrypt_pair(a, b)) for a, b in pairs)
    return ciphertext

def generate_playfair_problem(language, plaintext_length, hint_range, keyword_length, difficulty_label):
    keyword = generate_playfair_random_keyword(keyword_length)
    key_matrix = generate_playfair_key(keyword)
    
    ques_plaintext = get_plaintext_of_length(plaintext_length)
    ques_ciphertext = playfair_encrypt(ques_plaintext, key_matrix)
    
    hint_length = random.randint(hint_range[0], hint_range[1])
    hint_plaintext = get_plaintext_of_length(hint_length)
    hint_ciphertext = playfair_encrypt(hint_plaintext, key_matrix)
    hint = {}
    solution = {}
    
    hint = (f"Known plaintext and ciphertext pair:\n"
            f"Plaintext: '{hint_plaintext}'\n"
            f"Ciphertext: '{hint_ciphertext}'\n")

    solution = {
        "method": "Playfair Cipher",
        "keyword": keyword,
        "key_matrix": key_matrix
    }
    

    return {
        "ciphertext": ques_ciphertext,
        "plaintext": ques_plaintext,
        "hint": hint,
        "solution": solution,
        "method": "playfair",
        "difficulty": difficulty_label
    }

def rail_fence_encrypt(plaintext, rails):
    fence = [[] for _ in range(rails)]
    rail = 0
    direction = 1  

    for char in plaintext:
        fence[rail].append(char)
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1

    return ''.join([''.join(row) for row in fence])

def generate_rail_fence_problem(language, plaintext_length, hint_range, rails, difficulty_label):
    ques_plaintext = get_plaintext_of_length(plaintext_length)
    ques_ciphertext = rail_fence_encrypt(ques_plaintext, rails)
    
    hint_length = random.randint(hint_range[0], hint_range[1])
    hint_plaintext = get_plaintext_of_length(hint_length)
    hint_ciphertext = rail_fence_encrypt(hint_plaintext, rails)
    
    hint = (f"Known plaintext and ciphertext pair:\n"
            f"Plaintext: '{hint_plaintext}'\n"
            f"Ciphertext: '{hint_ciphertext}'\n")

    solution = {
        "method": "Rail Fence Cipher",
        "rails": rails
    }

    return {
        "ciphertext": ques_ciphertext,
        "plaintext": ques_plaintext,
        "hint": hint,
        "solution": solution,
        "method": "rail_fence",
        "difficulty": difficulty_label
    }

def generate_substitution_key():
    alphabet = list(string.ascii_uppercase)
    shuffled_alphabet = alphabet[:]
    random.shuffle(shuffled_alphabet)
    return shuffled_alphabet

def substitution_encrypt(plaintext, key):
    alphabet = string.ascii_uppercase
    key_map = {alphabet[i]: key[i] for i in range(len(alphabet))}
    return ''.join([key_map[char] if char in key_map else char for char in plaintext])

def generate_substitution_problem(language, plaintext_length, hint_range, difficulty_label):
    key = generate_substitution_key()
    ques_plaintext = get_plaintext_of_length(plaintext_length)
    ques_ciphertext = substitution_encrypt(ques_plaintext, key)
    
    hint_length = random.randint(hint_range[0], hint_range[1])
    hint_plaintext = get_plaintext_of_length(hint_length)
    hint_ciphertext = substitution_encrypt(hint_plaintext, key)
    
    hint = (f"Known plaintext and ciphertext pair:\n"
            f"Plaintext: '{hint_plaintext}'\n"
            f"Ciphertext: '{hint_ciphertext}'\n")

    solution = {
        "method": "Substitution Cipher",
        "key": key
    }

    return {
        "ciphertext": ques_ciphertext,
        "plaintext": ques_plaintext,
        "hint": hint,
        "solution": solution,
        "method": "substitution",
        "difficulty": difficulty_label
    }

def generate_vigenere_random_keyword(length):
    letters = string.ascii_uppercase
    keyword = ''.join(random.choice(letters) for _ in range(length))
    return keyword

def vigenere_encrypt(plaintext, keyword):
    plaintext = ''.join([c for c in plaintext if c.isalpha()]).upper()
    keyword = keyword.upper()
    key_length = len(keyword)
    key_int = [ord(i) - ord('A') for i in keyword]
    plaintext_int = [ord(i) - ord('A') for i in plaintext]
    ciphertext = ''
    for i in range(len(plaintext_int)):
        value = (plaintext_int[i] + key_int[i % key_length]) % 26
        ciphertext += chr(value + ord('A'))
    return ciphertext

def vigenere_decrypt(ciphertext, keyword):
    ciphertext = ''.join([c for c in ciphertext if c.isalpha()]).upper()
    keyword = keyword.upper()
    key_length = len(keyword)
    key_int = [ord(i) - ord('A') for i in keyword]
    ciphertext_int = [ord(i) - ord('A') for i in ciphertext]
    plaintext = ''
    for i in range(len(ciphertext_int)):
        value = (ciphertext_int[i] - key_int[i % key_length]) % 26
        plaintext += chr(value + ord('A'))
    return plaintext

def generate_vigenere_problem(language, plaintext_length, hint_range, keyword_length, difficulty_label):
    keyword = generate_vigenere_random_keyword(keyword_length)
    ques_plaintext = get_plaintext_of_length(plaintext_length)
    ques_ciphertext = vigenere_decrypt(ques_plaintext, keyword)
    
    hint_length = random.randint(hint_range[0], hint_range[1])
    hint_plaintext = get_plaintext_of_length(hint_length)
    hint_ciphertext = vigenere_encrypt(hint_plaintext, keyword)
    
    hint = (f"Known plaintext and ciphertext pair:\n"
            f"Plaintext: '{hint_plaintext}'\n"
            f"Ciphertext: '{hint_ciphertext}'\n")

    solution = {
        "method": "Vigenère Cipher",
        "keyword": keyword
    }
    
    return {
        "ciphertext": ques_ciphertext,
        "plaintext": ques_plaintext,
        "hint": hint,
        "solution": solution,
        "method": "vigenere",
        "difficulty_level": difficulty_label
    }

difficulty_mappings = {
    "vigenere": {
        "naive":   {"plaintext_length": 5,  "hint_range": [120, 150],  "keyword_length": 2,  "difficulty_label": "naive"},
        "easy":    {"plaintext_length": 10,  "hint_range": [120, 150],  "keyword_length": 3,  "difficulty_label": "easy"},
        "medium":  {"plaintext_length": 10,  "hint_range": [80, 100], "keyword_length": 4,  "difficulty_label": "medium"},
        "hard":    {"plaintext_length": 15, "hint_range": [80, 100], "keyword_length": 5,  "difficulty_label": "hard"},
        "extreme": {"plaintext_length": 20, "hint_range": [80, 100], "keyword_length": 5,  "difficulty_label": "extreme"}
    },

    "affine": {
        "naive":   {"plaintext_length": 5,  "hint_range": [120, 150],  "key_difficulty": 'K1', "difficulty_label": "naive"},
        "easy":    {"plaintext_length": 10,  "hint_range": [120, 150],  "key_difficulty": 'K1',  "difficulty_label": "easy"},
        "medium":  {"plaintext_length": 10,  "hint_range": [120, 150], "key_difficulty": 'K2',  "difficulty_label": "medium"},
        "hard":    {"plaintext_length": 10, "hint_range": [80, 100], "key_difficulty": 'K3',  "difficulty_label": "hard"},
        "extreme": {"plaintext_length": 15, "hint_range": [80, 100], "key_difficulty": 'K3',  "difficulty_label": "extreme"}
    },

    "caesar": {
        "naive":   {"plaintext_length": 5,  "hint_range": [120, 150], "difficulty_label": "naive"},
        "easy":    {"plaintext_length": 10,  "hint_range": [120, 150], "difficulty_label": "easy"},
        "medium":  {"plaintext_length": 10,  "hint_range": [80, 100], "difficulty_label": "medium"},
        "hard":    {"plaintext_length": 15, "hint_range": [80, 100], "difficulty_label": "hard"},
        "extreme": {"plaintext_length": 20, "hint_range": [80, 100], "difficulty_label": "extreme"}
    },

    "rail_fence": {
        "naive":   {"plaintext_length": 5,  "hint_range": [120, 150],  "rails": 2,  "difficulty_label": "naive"},
        "easy":    {"plaintext_length": 10,  "hint_range": [120, 150],  "rails": 2,  "difficulty_label": "easy"},
        "medium":  {"plaintext_length": 10,  "hint_range": [80, 100], "rails": 3,  "difficulty_label": "medium"},
        "hard":    {"plaintext_length": 15, "hint_range": [80, 100], "rails": 3,  "difficulty_label": "hard"},
        "extreme": {"plaintext_length": 20, "hint_range": [80, 100], "rails": 4,  "difficulty_label": "extreme"}
    },

    "playfair": {
        "naive":   {"plaintext_length": 5,  "hint_range": [120, 150],  "keyword_length": 5,  "difficulty_label": "naive"},
        "easy":    {"plaintext_length": 10,  "hint_range": [120, 150],  "keyword_length": 6,  "difficulty_label": "easy"},
        "medium":  {"plaintext_length": 10,  "hint_range": [80, 100], "keyword_length": 7,  "difficulty_label": "medium"},
        "hard":    {"plaintext_length": 15, "hint_range": [80, 100], "keyword_length": 7,  "difficulty_label": "hard"},
        "extreme": {"plaintext_length": 20, "hint_range": [80, 100], "keyword_length": 8,  "difficulty_label": "extreme"}
    },

    "substitution": {
        "naive":   {"plaintext_length": 5,  "hint_range": [120, 150], "difficulty_label": "naive"},
        "easy":    {"plaintext_length": 10,  "hint_range": [120, 150], "difficulty_label": "easy"},
        "medium":  {"plaintext_length": 10,  "hint_range": [80, 100], "difficulty_label": "medium"},
        "hard":    {"plaintext_length": 15, "hint_range": [80, 100], "difficulty_label": "hard"},
        "extreme": {"plaintext_length": 20, "hint_range": [80, 100], "difficulty_label": "extreme"}
    },

    "atbash": {
        "naive":   {"plaintext_length": 5,  "hint_range": [120, 150], "difficulty_label": "naive"},
        "easy":    {"plaintext_length": 10,  "hint_range": [120, 150], "difficulty_label": "easy"},
        "medium":  {"plaintext_length": 10,  "hint_range": [80, 100], "difficulty_label": "medium"},
        "hard":    {"plaintext_length": 15, "hint_range": [80, 100], "difficulty_label": "hard"},
        "extreme": {"plaintext_length": 20, "hint_range": [80, 100], "difficulty_label": "extreme"}
    },
    
    "autokey": {
        "naive":   {"plaintext_length": 5,  "hint_range": [120, 150],  "keyword_length": 2,  "difficulty_label": "naive"},
        "easy":    {"plaintext_length": 10,  "hint_range": [120, 150],  "keyword_length": 3,  "difficulty_label": "easy"},
        "medium":  {"plaintext_length": 10,  "hint_range": [80, 100], "keyword_length": 4,  "difficulty_label": "medium"},
        "hard":    {"plaintext_length": 15, "hint_range": [80, 100], "keyword_length": 5,  "difficulty_label": "hard"},
        "extreme": {"plaintext_length": 20, "hint_range": [80, 100], "keyword_length": 5,  "difficulty_label": "extreme"}
    },
    
    "hill": {
        "naive":   {"plaintext_length": 4,  "hint_range": [120, 150],  "matrix_size": 2,  "difficulty_label": "naive"},
        "easy":    {"plaintext_length": 8,  "hint_range": [120, 150],  "matrix_size": 2,  "difficulty_label": "easy"},
        "medium":  {"plaintext_length": 6,  "hint_range": [80, 100], "matrix_size": 3,  "difficulty_label": "medium"},
        "hard":    {"plaintext_length": 9, "hint_range": [80, 100], "matrix_size": 3,  "difficulty_label": "hard"},
        "extreme": {"plaintext_length": 15, "hint_range": [80, 100], "matrix_size": 3,  "difficulty_label": "extreme"}
    }
}


def generate_cipher_problem(language, method, **kwargs):
    if method == "vigenere":
        return generate_vigenere_problem(language, **kwargs)
    elif method == "substitution":
        return generate_substitution_problem(language, **kwargs)
    elif method == "rail_fence":
        return generate_rail_fence_problem(language, **kwargs)
    elif method == "playfair":
        return generate_playfair_problem(language, **kwargs)
    elif method == "hill":
        return generate_hill_problem(language, **kwargs)
    elif method == "affine":
        return generate_affine_problem(language, **kwargs)
    elif method == "caesar":
        return generate_caesar_problem(language, **kwargs)
    elif method == "autokey":
        return generate_autokey_problem(language, **kwargs)
    elif method == "atbash":
        return generate_atbash_problem(language, **kwargs)
    else:
        raise ValueError(f"Unsupported cipher method: {method}")

def string_to_md5(s):
    encoded_string = s.encode('utf-8')
    md5_hash = hashlib.md5()
    md5_hash.update(encoded_string)
    return md5_hash.hexdigest()

def transform_problem_to_meta(problem, idx, language, split):
    ciphertext = problem.get("ciphertext", "")
    plaintext = problem.get("plaintext", "")
    hint = problem.get("hint", "")
    solution = problem.get("solution", {})
    method = problem.get("method", "")
    question_template = QUESTION_TEMPLATE
    question_text = question_template.format(
        ciphertext=ciphertext, hint=hint
    )
    timestamp = str(time.time())  
    id_string = f"KPA_{method}_{idx}_{timestamp}"
    hash_id_string = string_to_md5(id_string)
    return {
        "id": hash_id_string,
        "question": question_text,
        "answer": plaintext,
        "rationale": solution,
        "split": split,
        "type": "crypto_puzzle",
        "source_url": "auto-generated",
        "dataset_name": f"crypto_KPA_{method}",
        "difficulty_level": problem.get("difficulty_level", ""),
        "language": language
    }


def generate(count=100, difficulty='medium', language='en', split="train", **kwargs):
    """
    Generate encryption puzzles based on the specified method, difficulty, and language.

    Parameters:
    -----------
    count : int, optional (default=100) Number of puzzles to generate.
    difficulty : str, optional (default='medium') Difficulty level ('naive', 'easy', 'medium', 'hard', 'extreme').
    **kwargs : method (str):('vigenere', 'substitution', 'rail_fence', 'playfair', 'hill', 'affine', 'caesar', 'autokey', 'atbash').

    Yields:
    -------
    dict
        A puzzle containing 'prompt', 'meta', 'answer', 'ability',  and 'task'.
    """
    method = kwargs.get("method", "caesar")
    #split = kwargs.get("split", "eval")
    prompt_template = PROMPT_TEMPLATE
    config = difficulty_mappings[method]
    params = config[difficulty]
    for i in tqdm(range(count)):
        problem = generate_cipher_problem(language, method, **params)
        meta = transform_problem_to_meta(problem, i, language, split)
        meta['difficulty'] = difficulty
        if meta["difficulty_level"] == "":
            meta["difficulty_level"] = meta["difficulty"]
        yield {
            "prompt": prompt_template.format(question=meta["question"]),
            "answer": meta["answer"],
            "task_name": "crypto_KPA",
            "ability": "crypto_puzzle",
            "language": language,
            "meta": json.dumps(meta),
        }



def save_to_jsonl(output_file, count, language, encryption_method, split):
    with open(output_file, 'a', encoding='utf-8') as f:
        for item in generate(count // 5, difficulty='naive', language=language, method=encryption_method, split=split):
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
        for item in generate(count // 5, difficulty='easy', language=language, method=encryption_method, split=split):
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
        for item in generate(count // 5, difficulty='medium', language=language, method=encryption_method, split=split):
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
        for item in generate(count // 5, difficulty='hard', language=language, method=encryption_method, split=split):
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
        for item in generate(count // 5, difficulty='extreme', language=language, method=encryption_method, split=split):
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

if __name__ == "__main__":
    ciphers = [
        'vigenere',
        'substitution',
        'rail_fence',
        'playfair',
        'hill',
        'affine',
        'caesar',
        'autokey',
        'atbash'
    ]
    for cipher in ciphers:
        save_to_jsonl('train_en.jsonl', 20000, language='en', encryption_method=cipher, split="train")



