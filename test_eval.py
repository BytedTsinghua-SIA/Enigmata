import json
import os
import importlib
import pandas as pd
import concurrent.futures
import argparse


def dummy_verify(solution_str, answer, meta):
    return 0


# Register all available task verifiers
registried_tasks = {}
try:
    folder_path = 'verifiable_tasks/tasks'
    for task in os.listdir(folder_path):
        if os.path.isdir(os.path.join(folder_path, task)):
            try:
                module = importlib.import_module(f'verifiable_tasks.tasks.{task}.verifier')
                registried_tasks[task] = module.verify
            except Exception:
                continue
except Exception:
    print('Cannot find verifiable_tasks directory')


def compute_score(solution_str, meta, task_name, answer) -> float:
    if isinstance(meta, str):
        meta = json.loads(meta)
    try:
        verify_fn = registried_tasks[task_name]
        return verify_fn(solution_str, answer, meta)
    except Exception:
        return dummy_verify(solution_str, answer, meta)


def process_row(row):
    row['result'] = compute_score(row['output'], row['meta'], row['task_name'], row['answer'])
    return row


if __name__ == '__main__':
    # Parse command line argument
    parser = argparse.ArgumentParser(description='Evaluate solutions in a result.parquet file')
    parser.add_argument('--input', type=str, required=True, help='Path to the input .parquet file')
    args = parser.parse_args()

    # Load data
    df = pd.read_parquet(args.input)

    # Ensure meta is a dictionary
    df['meta_dict'] = df['meta'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)

    # Extract difficulty level
    def get_difficulty(meta):
        return meta.get('difficulty_level') or meta.get('difficulty', 'unknown')

    df['difficulty_level'] = df['meta_dict'].apply(get_difficulty)

    # Process each row with multithreading
    with concurrent.futures.ThreadPoolExecutor(max_workers=512) as executor:
        results = list(executor.map(process_row, df.to_dict('records')))

    result_df = pd.DataFrame(results)

    # Overall accuracy
    overall_accuracy = result_df['result'].sum() / len(result_df)
    print(f"\nOverall Accuracy: {overall_accuracy:.4f}")

    # Accuracy by difficulty level
    difficulty_stats = result_df.groupby('difficulty_level').agg(
        accuracy=('result', lambda x: x.sum() / len(x)),
        count=('result', 'count')
    ).reset_index()
    print("\nAccuracy by Difficulty Level:")
    for _, row in difficulty_stats.iterrows():
        print(f"Difficulty: {row['difficulty_level']}, Accuracy: {row['accuracy']:.4f}, Count: {row['count']}")

    # Accuracy by task
    task_stats = result_df.groupby('task_name').agg(
        accuracy=('result', lambda x: x.sum() / len(x)),
        count=('result', 'count')
    ).reset_index()
    print("\nAccuracy by Task:")
    for _, row in task_stats.iterrows():
        print(f"Task: {row['task_name']}, Accuracy: {row['accuracy']:.4f}, Count: {row['count']}")

    # Accuracy by task and difficulty
    task_difficulty_stats = result_df.groupby(['task_name', 'difficulty_level']).agg(
        accuracy=('result', lambda x: x.sum() / len(x)),
        count=('result', 'count')
    ).reset_index()
    print("\nAccuracy by Task and Difficulty Level:")
    for _, row in task_difficulty_stats.iterrows():
        print(f"Task: {row['task_name']}, Difficulty: {row['difficulty_level']}, Accuracy: {row['accuracy']:.4f}, Count: {row['count']}")
