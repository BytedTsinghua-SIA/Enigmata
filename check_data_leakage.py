#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import argparse
from tqdm import tqdm
from pathlib import Path
import hashlib
import pandas as pd

def read_jsonl(file_path):
    """Read a JSONL file and return a list of dictionaries"""
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                item = json.loads(line.strip())
                data.append(item)
            except json.JSONDecodeError:
                print(f"Warning: Skipping invalid JSON line in {file_path}")
    return data

def save_jsonl(data, file_path):
    """Save a list of dictionaries to a JSONL file"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        for item in data:
            line = json.dumps(item, ensure_ascii=False)
            f.write(line + '\n')

def normalize_text(text):
    """Normalize text by removing whitespaces and newlines"""
    if not isinstance(text, str):
        return str(text)
    return ' '.join(text.split())

def get_prompt_hash(prompt):
    """Get a hash of the prompt for efficient comparison"""
    if isinstance(prompt, list):
        text = ' '.join([msg.get('content', '') for msg in prompt if isinstance(msg, dict)])
    else:
        text = str(prompt)
    
    normalized = text
    return hashlib.md5(normalized.encode('utf-8')).hexdigest()

def find_task_dirs(root_dir, task_name=None):
    """
    Find directories containing JSONL files.

    Args:
        root_dir: Root directory
        task_name: Specific task name, if provided, return only matched tasks

    Returns:
        List of task directories
    """
    task_dirs = []
    
    if task_name:
        for task_dir in Path(root_dir).glob(f'**/{task_name}'):
            if task_dir.is_dir() and list(task_dir.glob('*.jsonl')):
                task_dirs.append(task_dir)
        
        if not task_dirs:
            for task_dir in Path(root_dir).glob('**/'):
                if task_dir.is_dir() and task_name in str(task_dir) and list(task_dir.glob('*.jsonl')):
                    task_dirs.append(task_dir)
    else:
        for task_dir in Path(root_dir).glob('**/'):
            if task_dir.is_dir() and list(task_dir.glob('*.jsonl')):
                task_dirs.append(task_dir)
    
    return task_dirs

def check_data_leakage(eval_root, train_root, output_root=None, check_field='prompt', task_name=None):
    """
    Check for duplicated samples between evaluation and training datasets, optionally save clean data.

    Args:
        eval_root: Evaluation dataset root directory
        train_root: Training dataset root directory
        output_root: Output directory to save non-leaked data
        check_field: Field to check for duplication (default: 'prompt')
        task_name: Specific task name to check

    Returns:
        DataFrame with leakage statistics
    """
    eval_tasks = find_task_dirs(eval_root, task_name)
    
    if not eval_tasks:
        if task_name:
            print(f"Warning: No evaluation data found for task '{task_name}'")
        else:
            print("Warning: No evaluation tasks found")
        return pd.DataFrame()
    
    print(f"Found {len(eval_tasks)} evaluation task directories")
    
    results = []
    
    for eval_task_dir in tqdm(eval_tasks, desc="Checking tasks"):
        rel_path = eval_task_dir.relative_to(eval_root)
        train_task_dir = Path(train_root) / rel_path
        
        if not train_task_dir.exists():
            print(f"Warning: Training directory does not exist: {train_task_dir}")
            continue
        
        for eval_file in eval_task_dir.glob('*.jsonl'):
            train_file = train_task_dir / eval_file.name.replace('test', 'train')
            if not train_file.exists():
                train_file = train_task_dir / eval_file.name
            
            if not train_file.exists():
                print(f"Warning: Training file does not exist: {train_file}")
                continue
            
            eval_data = read_jsonl(eval_file)
            train_data = read_jsonl(train_file)
            
            train_prompts = set()
            for item in train_data:
                if check_field in item:
                    prompt_hash = get_prompt_hash(item[check_field])
                    train_prompts.add(prompt_hash)
            
            duplicates = 0
            duplicate_indices = []
            clean_data = []
            
            for i, item in enumerate(eval_data):
                is_duplicate = False
                if check_field in item:
                    prompt_hash = get_prompt_hash(item[check_field])
                    if prompt_hash in train_prompts:
                        duplicates += 1
                        duplicate_indices.append(i)
                        is_duplicate = True
                
                if not is_duplicate and output_root:
                    clean_data.append(item)
            
            leak_rate = (duplicates / len(eval_data) * 100) if eval_data else 0
            
            result = {
                'task': str(rel_path),
                'file': eval_file.name,
                'eval_samples': len(eval_data),
                'train_samples': len(train_data),
                'duplicates': duplicates,
                'clean_samples': len(clean_data),
                'leak_rate': leak_rate,
                'duplicate_indices': duplicate_indices
            }
            
            results.append(result)
            
            print(f"Checked {rel_path}/{eval_file.name}: {len(eval_data)} eval, {len(train_data)} train, {duplicates} duplicates ({leak_rate:.2f}%), {len(clean_data)} kept")
            
            if output_root and clean_data:
                output_dir = Path(output_root) / rel_path
                output_file = output_dir / eval_file.name
                save_jsonl(clean_data, str(output_file))
    
    df = pd.DataFrame(results)
    
    if df.empty:
        print("No matching data found")
        return df
    
    total_eval = df['eval_samples'].sum()
    total_duplicates = df['duplicates'].sum()
    total_clean = df['clean_samples'].sum()
    overall_leak_rate = (total_duplicates / total_eval * 100) if total_eval > 0 else 0
    
    print(f"\nTotal checked {total_eval} eval samples, {total_duplicates} duplicates found ({overall_leak_rate:.2f}%), {total_clean} kept")
    
    if output_root:
        print(f"Cleaned data saved to: {output_root}")
    
    return df

def main():
    parser = argparse.ArgumentParser(description="Check for duplicate samples between evaluation and training datasets")
    parser.add_argument("--eval-root", required=True, help="Root directory of evaluation dataset")
    parser.add_argument("--train-root", required=True, help="Root directory of training dataset")
    parser.add_argument("--output-root", help="Output directory to save cleaned data if specified")
    parser.add_argument("--check-field", default="prompt", help="Field name to check for duplication (default: 'prompt')")
    parser.add_argument("--task", help="Specific task name to check")
    parser.add_argument("--report", default="data_leakage_report.csv", help="Output path for CSV report")
    
    args = parser.parse_args()
    
    df = check_data_leakage(args.eval_root, args.train_root, args.output_root, args.check_field, args.task)
    
    if not df.empty:
        df.to_csv(args.report, index=False)
        print(f"Leakage check report saved to: {args.report}")
        
        json_output = args.report.replace('.csv', '.json')
        df.to_json(json_output, orient='records', indent=2)
        print(f"Detailed JSON report saved to: {json_output}")

if __name__ == "__main__":
    main()
