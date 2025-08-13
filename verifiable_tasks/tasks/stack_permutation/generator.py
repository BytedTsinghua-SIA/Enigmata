import random
import json
from tqdm import tqdm
from .template import PROMPT_TEMPLATE

def is_valid_stack_permutation(input_sequence, output_sequence):
    stack = []
    output_index = 0
    
    for num in input_sequence:
        stack.append(num)
        
        # Pop from stack while top of stack matches the next output_sequence element
        while stack and stack[-1] == output_sequence[output_index]:
            stack.pop()
            output_index += 1

    # If the stack is empty and output_index reached the length of output_sequence, it's a valid permutation
    return output_index == len(output_sequence)

def generate_stack_permutations(input_sequence):
    def backtrack(stack, output_sequence, input_index, output_index, result):
        # If output sequence is complete, save it
        if output_index == len(input_sequence):
            result.append(output_sequence[:])
            return
        
        # Try push operation
        if input_index < len(input_sequence):
            stack.append(input_sequence[input_index])
            backtrack(stack, output_sequence, input_index + 1, output_index, result)
            stack.pop()  # Backtrack
        
        # Try pop operation
        if stack:
            output_sequence.append(stack.pop())
            backtrack(stack, output_sequence, input_index, output_index + 1, result)
            stack.append(output_sequence.pop())  # Backtrack
    
    result = []
    backtrack([], [], 0, 0, result)
    return result

def generate(count, difficulty='medium', language='en', split="train"):
    prompt_template = PROMPT_TEMPLATE
    for i in tqdm(range(count)):
        dif_level = {"easy" : [4,5], "medium" : [6,7], "hard" : [8,9]}
        length =  random.randint(dif_level[difficulty][0], dif_level[difficulty][1])
        input_sequence = list(range(1, length + 1))
        random.shuffle(input_sequence)
        valid_permutations = generate_stack_permutations(input_sequence)
        if random.random() < 0.6:
            output_sequence = random.choice(valid_permutations)
        else:
            output_sequence = list(range(1, length + 1))
            random.shuffle(output_sequence)
        if is_valid_stack_permutation(input_sequence, output_sequence):
            answer = "The output sequence is a valid stack permutation."
        else:
            answer = "The output sequence is not a valid stack permutation."
        yield {
            "prompt": prompt_template.format(input_sequence=input_sequence, output_sequence=output_sequence),
            "answer":  answer,
            "task_name": "stack_permutation",    
            "ability": "logic_puzzle", 
            "language": language,
            "meta": json.dumps({
                "id":"stack_permutation_"+difficulty+str(i),
                "input_sequence": input_sequence,
                "output_sequence": output_sequence,
                "sequence_length":length,
                "answer": answer, 
                "rationale": "", 
                "split": split,
                "type": "sequential_puzzle", 
                "source_url": "auto-generated", 
                "dataset_name": "stack_permutation", 
                "difficulty_level": difficulty,
                "language": language,
            }),
        }

def save_to_jsonl(output_file, count, lange='en'):
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in generate(count//3, 'easy', lange):
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
        for item in generate(count//3, 'medium', lange):
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
        for item in generate(count//3, 'hard', lange):
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

#save_to_jsonl('sp_en.jsonl', 10, 'en')
#save_to_jsonl('../sp_zh.jsonl', 21500, 'zh')