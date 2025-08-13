import random
import time
from collections import defaultdict
import json
from tqdm import tqdm
import random
import hashlib
from .template import PROMPT_TEMPLATE
from pysat.formula import CNF
from pysat.solvers import Solver

PUZZLE_TYPE = "graph_puzzle"
SOURCE_URL = "auto_generated"
DATASET_NAME = "hamiltonian_path"

_seed_offset = 0

def generate_unique_seed():
    global _seed_offset
    seed = time.time_ns() + _seed_offset
    _seed_offset += 1
    return seed


def generate_hamiltonian_path_problem(num_nodes_range=None, edge_density=None):
    while True:
        problem = {}
        ensure_hamiltonian = random.choice([True, False])  
        seed = generate_unique_seed()
        random.seed(seed)

        if num_nodes_range is None:
            num_nodes_range = (8, 12)  
            
        num_nodes = random.randint(num_nodes_range[0], num_nodes_range[1])
        if num_nodes is None:
            num_nodes = random.randint(20, 30)
        if edge_density is None:
            edge_density = random.uniform(0.6, 0.9)

        assert 0 <= edge_density <= 1, "Edge density must be between 0 and 1"
        assert num_nodes > 0, "Number of nodes must be greater than 0"

        problem = {}
        ensure_hamiltonian = random.choice([True, False])  
        seed = generate_unique_seed()
        random.seed(seed)

        edges = set()
        reasons = []

        max_possible_edges = num_nodes * (num_nodes - 1) // 2  
        target_edges = int(max_possible_edges * edge_density)  

        if ensure_hamiltonian:
            nodes = list(range(num_nodes))
            random.shuffle(nodes)
            for i in range(num_nodes - 1):
                u, v = sorted((nodes[i], nodes[i + 1]))
                edges.add((u, v))

            while len(edges) < target_edges + random.randint(5, 10):
                node1, node2 = random.sample(range(num_nodes), 2)
                u, v = sorted((node1, node2))
                if (u, v) not in edges:
                    edges.add((u, v))

        else:
            issues = [
                "isolated_nodes",
                "disconnected_subgraphs",
                "dead_ends",
                "sparse_graph",
                "critical_bridge_node"
            ]
            selected_issue = random.choice(issues)

            if selected_issue == "isolated_nodes":
                num_isolated_nodes = random.randint(1, max(1, num_nodes // 5))
                isolated_nodes = random.sample(range(num_nodes), num_isolated_nodes)
                reasons.append(f"isolated_nodes: {isolated_nodes}")

                non_isolated_nodes = [n for n in range(num_nodes) if n not in isolated_nodes]
                for _ in range(len(non_isolated_nodes) * (len(non_isolated_nodes) - 1) // 4):
                    u, v = random.sample(non_isolated_nodes, 2)
                    edges.add((u, v))

            elif selected_issue == "disconnected_subgraphs":
                partition = num_nodes // 2
                subgraph_1 = list(range(partition))
                subgraph_2 = list(range(partition, num_nodes))

                for _ in range(len(subgraph_1) * (len(subgraph_1) - 1) // 4):
                    u, v = random.sample(subgraph_1, 2)
                    edges.add((u, v))

                for _ in range(len(subgraph_2) * (len(subgraph_2) - 1) // 4):
                    u, v = random.sample(subgraph_2, 2)
                    edges.add((u, v))

                reasons.append(f"disconnected_subgraphs with edge_density={edge_density}")

            elif selected_issue == "dead_ends":
                for _ in range(target_edges // 2):
                    u, v = random.sample(range(num_nodes), 2)
                    edges.add((u, v))

                dead_ends = []
                for _ in range(random.randint(1, max(1, num_nodes // 10))):
                    node = random.choice(range(num_nodes))
                    connected_edges = [e for e in edges if node in e]
                    if len(connected_edges) > 1:
                        for e in connected_edges[1:]:
                            edges.remove(e)
                        dead_ends.append(node)

                reasons.append(f"dead_ends: {dead_ends}")

            elif selected_issue == "sparse_graph":
                for _ in range(target_edges // 4):
                    u, v = random.sample(range(num_nodes), 2)
                    edges.add((u, v))

                reasons.append(f"sparse_graph with edge_density={edge_density}")

            elif selected_issue == "critical_bridge_node":
                bridge_node = random.randint(0, num_nodes - 1)
                subgraph_1 = list(range(num_nodes // 2))
                subgraph_2 = list(range(num_nodes // 2, num_nodes))

                for node in subgraph_1:
                    edges.add((bridge_node, node))
                for node in subgraph_2:
                    edges.add((bridge_node, node))

                reasons.append("critical_bridge_node")

        output = [f"{num_nodes}"]
        output.extend([f"{u} {v}" for u, v in sorted(edges)])
        question = "\n".join(output)
        path, verify = has_hamiltonian_path(num_nodes, edges)
        problem["question"] = question
        problem["answer"] = path if verify else "NO"
        problem["reason"] = path if verify else reasons
        return problem

def has_hamiltonian_path(num_nodes, edges):
    cnf = CNF()
    nodes = range(num_nodes)
    var = lambda i, j: i * num_nodes + j + 1
    for i in nodes:
        cnf.append([var(i, j) for j in nodes])
        for j in nodes:
            for k in nodes:
                if j < k:
                    cnf.append([-var(i, j), -var(i, k)])

    for j in nodes:
        cnf.append([var(i, j) for i in nodes])
        for i in nodes:
            for k in nodes:
                if i < k:
                    cnf.append([-var(i, j), -var(k, j)])

    edge_set = set((min(u, v), max(u, v)) for u, v in edges)
    for j in range(num_nodes - 1):
        for i in nodes:
            for k in nodes:
                if i != k and (min(i, k), max(i, k)) not in edge_set:
                    cnf.append([-var(i, j), -var(k, j + 1)])

    with Solver(name='glucose3') as solver:
        solver.append_formula(cnf)
        if solver.solve():
            model = solver.get_model()
            path = [0] * num_nodes
            for i in nodes:
                for j in nodes:
                    if model[var(i, j) - 1] > 0:
                        path[j] = i
            return path, True
        else:
            return None, False


def string_to_md5(s):
    encoded_string = s.encode('utf-8')
    md5_hash = hashlib.md5()
    md5_hash.update(encoded_string)
    return md5_hash.hexdigest()

def transform_problem_to_meta(problem, idx, language, split):
    timestamp = str(time.time())  
    id_string = f"hamiltonian_path_{idx}_{timestamp}"
    hash_id_string = string_to_md5(id_string)
    return{
        "id": hash_id_string,
        "question": problem["question"],
        "answer": problem["answer"],
        "rationale": problem["reason"],
        "split": split, 
        "type": PUZZLE_TYPE,
        "source_url": SOURCE_URL,
        "dataset_name": DATASET_NAME,
        "difficulty_level":  problem["difficulty_level"],
        "language": language
    }

difficulty_mappings = {
    "easy": {"num_nodes_range": (10, 15), "edge_density": 0.2},
    "medium": {"num_nodes_range": (15, 20), "edge_density": 0.3},
    "hard": {"num_nodes_range": (20, 25), "edge_density": 0.4},
}

def generate(count=10, difficulty='medium', language='en', split="train", **kwargs):
    prompt_template = PROMPT_TEMPLATE
    #split = kwargs.get("split", "eval")
    params = difficulty_mappings[difficulty]
    for i in tqdm(range(count)):
        problem = generate_hamiltonian_path_problem(**params)
        problem["difficulty_level"] = difficulty
        meta = transform_problem_to_meta(problem, i, language, split)
        yield {
            "prompt": prompt_template.format(question=meta["question"]),
            "answer": meta["answer"],
            "task_name": DATASET_NAME,
            "ability": PUZZLE_TYPE,
            "language": language,
            "meta": json.dumps(meta),
        }

def save_to_jsonl(output_file, count, language, split):
    """Save generated problems to a JSONL file"""
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in generate(count // 3, difficulty='easy', language=language, split=split):
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
        for item in generate(count // 3, difficulty='medium', language=language, split=split):
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
        for item in generate(count // 3, difficulty='hard', language=language, split=split):
            f.write(json.dumps(item, ensure_ascii=False) + '\n')


if __name__ == "__main__":
    save_to_jsonl('train_en.jsonl', 20000, language='en', split="train")
    save_to_jsonl('test_en.jsonl', 1500, language='en', split="eval")
