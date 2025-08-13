#!/usr/bin/env python3
import os
import importlib
import json
import sys
import argparse
from pathlib import Path
import inspect

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Generate problems for specified tasks')
parser.add_argument('--count', type=int, default=100, help='Number of problems to generate per difficulty level')
parser.add_argument('--split', type=str, default='train', choices=['train', 'test'], help='Dataset split (train/test)')
parser.add_argument('--output', type=str, default=None, help='Output directory')
parser.add_argument('--tasks', type=str, nargs='+', default=[], help='Tasks to generate; if not specified, generate for all')
args = parser.parse_args()

# Add project root to Python path
root_dir = Path(__file__).parent.absolute()
sys.path.append(str(root_dir))

# Task directory
TASKS_DIR = os.path.join(root_dir, "verifiable_tasks", "tasks")

# Difficulty levels
DIFFICULTIES = ["easy", "medium", "hard"]
PROBLEMS_PER_DIFFICULTY = args.count

# Determine output directory
if args.output:
    os.makedirs(args.output, exist_ok=True)
    OUTPUT_DIR = args.output
else:
    OUTPUT_FILE = root_dir

def main():
    all_problems = {}

    # Determine which tasks to generate
    task_list = args.tasks if args.tasks else os.listdir(TASKS_DIR)

    for task_name in task_list:
        task_dir = os.path.join(TASKS_DIR, task_name)

        if not os.path.isdir(task_dir):
            print(f"Skipping {task_name}: not a directory")
            continue

        generator_path = os.path.join(task_dir, "generator.py")
        if not os.path.exists(generator_path):
            print(f"Skipping {task_name}: no generator.py file found")
            continue

        print(f"Found generator for task: {task_name}")
        all_problems[task_name] = {}

        # Check if output already exists
        output_task_dir = os.path.join(OUTPUT_DIR, task_name, "en")
        output_file = os.path.join(output_task_dir, f"{args.split}.jsonl")
        if os.path.exists(output_file):
            print(f"Skipping {task_name}: already generated at {output_file}")
            continue

        for difficulty in DIFFICULTIES:
            try:
                module_path = f"verifiable_tasks.tasks.{task_name}.generator"
                generator_module = importlib.import_module(module_path)

                if not hasattr(generator_module, "generate"):
                    print(f"  Warning: No `generate` function found in generator for {task_name}")
                    all_problems[task_name][difficulty] = []
                    continue

                generate_func = generator_module.generate
                sig = inspect.signature(generate_func)
                params = sig.parameters
                problems = []

                is_generator = inspect.isgeneratorfunction(generate_func)

                extra_kwargs = {}

                if is_generator:
                    if "count" in params:
                        generator = generate_func(PROBLEMS_PER_DIFFICULTY, difficulty=difficulty, language='en', split=args.split, **extra_kwargs)
                        for i, problem in enumerate(generator):
                            problems.append(problem)
                            if i + 1 >= PROBLEMS_PER_DIFFICULTY:
                                break
                    else:
                        for i in range(PROBLEMS_PER_DIFFICULTY):
                            try:
                                generator = generate_func(difficulty=difficulty, language='en', split=args.split, **extra_kwargs)
                                problem = next(generator)
                                problems.append(problem)
                            except Exception as e:
                                print(f"  Error generating problem {i+1} for {task_name} - {difficulty}: {str(e)}")
                                continue
                else:
                    for i in range(PROBLEMS_PER_DIFFICULTY):
                        try:
                            problem = generate_func(difficulty=difficulty, language='en', split=args.split, **extra_kwargs)
                            problems.append(problem)
                        except Exception as e:
                            print(f"  Error generating problem {i+1} for {task_name} - {difficulty}: {str(e)}")
                            continue

                all_problems[task_name][difficulty] = problems
                print(f"  Successfully generated {len(problems)} problems for {task_name} - {difficulty}")

            except Exception as e:
                print(f"  Error importing or using generator for {task_name}: {str(e)}")
                all_problems[task_name][difficulty] = []

        # Save generated problems for this task
        os.makedirs(output_task_dir, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            for difficulty, problems in all_problems[task_name].items():
                for problem in problems:
                    problem_copy = problem.copy() if isinstance(problem, dict) else {"data": problem}
                    if "meta" in problem_copy and isinstance(problem_copy["meta"], dict):
                        problem_copy["meta"]["task_name"] = task_name
                        problem_copy["meta"]["difficulty"] = difficulty
                    else:
                        problem_copy["task_name"] = task_name
                        problem_copy["difficulty"] = difficulty
                    f.write(json.dumps(problem_copy, ensure_ascii=False) + '\n')

        print(f"Saved problems for {task_name} to {output_file}")

    # Print summary statistics
    print("\nGeneration Summary:")
    for task_name in all_problems:
        for difficulty in DIFFICULTIES:
            count = len(all_problems.get(task_name, {}).get(difficulty, []))
            print(f"{task_name} - {difficulty}: {count}/{PROBLEMS_PER_DIFFICULTY}")

if __name__ == "__main__":
    main()
