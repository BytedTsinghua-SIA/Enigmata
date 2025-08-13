import random
from .template import PROMPT_TEMPLATE
from itertools import permutations, product
import json
from tqdm import tqdm

def generate_numbers(num_nums):
    return [random.randint(1, 13) for _ in range(num_nums)]
operations = ['+', '-', '*', '/']

# Define error tolerance
EPSILON = 1e-6

# Try to calculate expression value, avoid division by zero
def save_eval(exp): 
    try:
        return eval(exp)
    except ZeroDivisionError:
        return None
        
def eval_4(n, o): 
    #(n1 op1 n2) op2 (n3 op3 n4)
    exp = '(' + n[0] + o[0] + n[1] + ')' + o[1] + '(' + n[2] + o[2] + n[3] + ')'
    if abs(save_eval(exp) - 24) < EPSILON:
        return exp
    #((n1 op1 n2) op2 n3) op3 n4
    exp = '(' + '(' + n[0] + o[0] + n[1] + ')' + o[1] + n[2] + ')' + o[2] + n[3]
    if abs(save_eval(exp) - 24) < EPSILON:
        return exp
    #n1 op1 ((n2 op2 n3) op3 n4)
    exp = n[0] + o[0] + '(' + '(' + n[1] + o[1] + n[2] + ')' + o[2] + n[3] + ')'
    if abs(save_eval(exp) - 24) < EPSILON:
        return exp
    #(n1 op1 (n2 op2 n3)) op3 n4
    exp = '(' + n[0] + o[0]+ '('  + n[1] + o[1] + n[2] + ')'  + ')' + o[2] + n[3]
    if abs(save_eval(exp) - 24) < EPSILON:
        return exp
    #n1 op1 (n2 op2 (n3 op3 n4))
    exp = n[0] + o[0] + '(' + n[1] + o[1] + '(' + n[2] + o[2] + n[3] + ')' + ')'
    if abs(save_eval(exp) - 24) < EPSILON:
        return exp
    return None


def eval_5(n, o): #n=['1', '2', '3', '4', '5'], o=[o1, o2, o3, o4]
    #Eval4((n1 o1 n2), n3, n4, n5)
    tmp = save_eval(n[0]+o[0]+n[1])
    if tmp is not None:
        res = eval_4([str(tmp), n[2], n[3], n[4]], [o[1], o[2], o[3]])
        if res:
            return n[0]+o[0]+n[1]+'='+str(tmp)+", "+res
    #Eval4(n1, (n2 o2 n3), n4, n5)
    tmp = save_eval(n[1]+o[1]+n[2])
    if tmp is not None:
        res = eval_4([n[0], str(tmp), n[3], n[4]], [o[0], o[2], o[3]])
        if res:
            return n[1]+o[1]+n[2]+'='+str(tmp)+", "+res
    #Eval4(n1, n2, (n3 o3 n4), n5)
    tmp = save_eval(n[2]+o[2]+n[3])
    if tmp is not None:
        res = eval_4([n[0], n[1], str(tmp), n[4]], [o[0], o[1], o[3]])
        if res:
            return n[2]+o[2]+n[3]+'='+str(tmp)+", "+res
    #Eval4(n1, n2, n3, (n4 o4 n5))
    tmp = save_eval(n[3]+o[3]+n[4])
    if tmp is not None:
        res = eval_4([n[0], n[1], n[2], str(tmp)], [o[0], o[1], o[2]])
        if res:
            return n[3]+o[3]+n[4]+'='+str(tmp)+", "+res
    return None
    

def eval_6(n, o): #n=['1', '2', '3', '4', '5'], o=[o1, o2, o3, o4]
    #Eval5((n1 o1 n2), n3, n4, n5, n6)
    tmp = save_eval(n[0]+o[0]+n[1])
    if tmp is not None:
        res = eval_5([str(tmp), n[2], n[3], n[4], n[5]], [o[1], o[2], o[3], o[4]])
        if res:
            return n[0]+o[0]+n[1]+'='+str(tmp)+", "+res
    #Eval5(n1, (n2 o2 n3), n4, n5, n6)
    tmp = save_eval(n[1]+o[1]+n[2])
    if tmp is not None:
        res = eval_5([n[0], str(tmp), n[3], n[4], n[5]], [o[0], o[2], o[3], o[4]])
        if res:
            return n[1]+o[1]+n[2]+'='+str(tmp)+", "+res
    #Eval5(n1, n2, (n3 o3 n4), n5, n6)
    tmp = save_eval(n[2]+o[2]+n[3])
    if tmp is not None:
        res = eval_5([n[0], n[1], str(tmp), n[4], n[5]], [o[0], o[1], o[3], o[4]])
        if res:
            return n[2]+o[2]+n[3]+'='+str(tmp)+", "+res
    #Eval5(n1, n2, n3, (n4 o4 n5), n6)
    tmp = save_eval(n[3]+o[3]+n[4])
    if tmp is not None:
        res = eval_5([n[0], n[1], n[2], str(tmp), n[5]], [o[0], o[1], o[2], o[4]])
        if res:
            return n[3]+o[3]+n[4]+'='+str(tmp)+", "+res
    #Eval5(n1, n2, n3, n4, (n5 o5 n6))
    tmp = save_eval(n[4]+o[4]+n[5])
    if tmp is not None:
        res = eval_5([n[0], n[1], n[2], n[3], str(tmp)], [o[0], o[1], o[2], o[3]])
        if res:
            return n[4]+o[4]+n[5]+'='+str(tmp)+", "+res
    return None

def can_form_24(nums, lang='en'):
    #assert lang in ['zh', 'en']
    answer_cue = 'The answer is: ' if lang=='en' else "The answer is: "
    refuse_cue = 'cannot form 24' if lang=='en' else "cannot form 24"
    len_nums = len(nums)
    # Generate all permutations of numbers
    for n in permutations(nums):
        # Generate all combinations of operations
        for o in product(operations, repeat=(len_nums-1)):
            n = list(map(str, n))
            # Try different bracket combinations
            try:
                if len_nums==6:
                    res_o = eval_6(n, o)
                elif len_nums==5:
                    res_o = eval_5(n, o)
                elif len_nums==4:
                    res_o = eval_4(n, o)
                if res_o:
                    return f"{answer_cue}{res_o} = 24"

            except:
                continue
    return refuse_cue

def generate(count=100, difficulty='medium', language='en', split="train"):#, **kwargs):
    #param1 = kwargs.get('param1', default_value1)
    #param2 = kwargs.get('param2', default_value2)
    dic = {'easy':4, 'medium':5, 'hard':6}
    num_nums = dic[difficulty]
    prompt_template = PROMPT_TEMPLATE
    #exist = {}
    for i in tqdm(range(count)):
        numbers = generate_numbers(num_nums)
        sorted_numbers = tuple(numbers) #sorted(numbers)
        numbers_str = ",".join(map(str, numbers))
        answer = can_form_24(numbers, language)
        #print(numbers, answer)
        yield {
            "prompt":prompt_template.format(question=numbers_str), 
            "answer":  answer,
            "task_name": "game24",    
            "ability": "logic_puzzle", 
            "language": language,
            "meta": json.dumps({
                "id":"game24_"+difficulty+"_"+str(i), #hash?
                "question": numbers,
                "answer": answer,
                "rationale": "", 
                "split": split,
                "type": "code_puzzle", 
                "source_url": "auto-generated", 
                "dataset_name": "game24", 
                "difficulty_level": difficulty,
                "language": language,
            }),            
        }

def save_to_jsonl(of1, of2, count, lange='en'):
    with open(of1, 'w', encoding='utf-8') as f1, open(of2, 'w', encoding='utf-8') as f2:
        for item in generate(count//3, 'easy', lange):
            f1.write(json.dumps(item, ensure_ascii=False) + '\n')
            f2.write(json.dumps(item["meta"], ensure_ascii=False) + '\n')
        for item in generate(count//3, 'medium', lange):
            f1.write(json.dumps(item, ensure_ascii=False) + '\n')
            f2.write(json.dumps(item["meta"], ensure_ascii=False) + '\n')
        for item in generate(count//3, 'hard', lange):
            f1.write(json.dumps(item, ensure_ascii=False) + '\n')
            f2.write(json.dumps(item["meta"], ensure_ascii=False) + '\n')

# Call functions to generate and save
#save_to_jsonl('training/game24/en/train.jsonl', 'raw/game24/en/train.jsonl', 24000, 'en')
#save_to_jsonl('training/game24/zh/train.jsonl', 'raw/game24/zh/train.jsonl',24000, 'zh')

#save_to_jsonl('eval/game24/en/test.jsonl', 'raw/game24/en/test.jsonl', 1500, 'en')
#save_to_jsonl('eval/game24/zh/test.jsonl', 'raw/game24/zh/test.jsonl',1500, 'zh')