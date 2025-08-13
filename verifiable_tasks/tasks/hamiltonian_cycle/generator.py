import time
import random
import json
from hashlib import sha256
from pysat.formula import CNF
from pysat.solvers import Solver
from tqdm import tqdm
import hashlib
from .template import PROMPT_TEMPLATE

PUZZLE_TYPE = "graph_puzzle"
SOURCE_URL = "auto_generated"
DATASET_NAME = "hamiltonian_cycle"

class TimeoutException(Exception):
    pass

def generate_unique_seed():
    """Generate a unique random seed"""
    return int(sha256(str(random.random()).encode()).hexdigest(), 16)

def has_hamiltonian_cycle(num_nodes, edges, timeout=1):
    """Determine if a Hamiltonian Cycle exists"""
    start_time = time.time()

    graph = {i: set() for i in range(num_nodes)}
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)

    for node, neighbors in graph.items():
        if len(neighbors) < 2:
            return {"reason": f"Node {node} has degree {len(neighbors)} (less than 2)."}, False

    cnf = CNF()
    nodes = range(num_nodes)
    var = lambda i, j: i * num_nodes + j + 1  

    cnf.append([var(0, 0)])

    for i in nodes:
        if time.time() - start_time > timeout:
            raise TimeoutException("Hamiltonian cycle computation timed out.")
        cnf.append([var(i, j) for j in nodes])
        for j in range(num_nodes):
            for k in range(j + 1, num_nodes):
                cnf.append([-var(i, j), -var(i, k)])

    for j in nodes:
        if time.time() - start_time > timeout:
            raise TimeoutException("Hamiltonian cycle computation timed out.")
        cnf.append([var(i, j) for i in nodes])
        for i in range(num_nodes):
            for k in range(i + 1, num_nodes):
                cnf.append([-var(i, j), -var(k, j)])

    edge_set = set((min(u, v), max(u, v)) for u, v in edges)
    for j in range(num_nodes - 1):
        if time.time() - start_time > timeout:
            raise TimeoutException("Hamiltonian cycle computation timed out.")
        for i in nodes:
            for k in nodes:
                if (min(i, k), max(i, k)) not in edge_set:
                    cnf.append([-var(i, j), -var(k, j + 1)])

    for i in nodes:
        for k in nodes:
            if time.time() - start_time > timeout:
                raise TimeoutException("Hamiltonian cycle computation timed out.")
            if (min(i, k), max(i, k)) not in edge_set:
                cnf.append([-var(i, num_nodes - 1), -var(k, 0)])

    with Solver(name='glucose3') as solver:
        solver.append_formula(cnf)

        if time.time() - start_time > timeout:
            raise TimeoutException("Hamiltonian cycle computation timed out before solving.")
        
        if solver.solve():
            model = solver.get_model()
            cycle = [None] * num_nodes
            for j in nodes:
                for i in nodes:
                    if model[var(i, j) - 1] > 0:
                        cycle[j] = i
            return cycle, True
        else:
            return None, False

def generate_hamiltonian_cycle_problem(num_nodes_range=None, edge_density=None):
    while True:
        problem = {}
        ensure_hamiltonian = random.choice([True, False])  
        seed = generate_unique_seed()
        random.seed(seed)

        if num_nodes_range is None:
            num_nodes_range = (8, 12)  

        num_nodes = random.randint(num_nodes_range[0], num_nodes_range[1])
        
        if edge_density is None:
            edge_density = random.uniform(0.6, 0.9)

        assert 0 <= edge_density <= 1, "Edge density must be between 0 and 1"
        assert num_nodes > 0, "Number of nodes must be greater than 0"

        edges = set()
        reasons = []

        max_possible_edges = num_nodes * (num_nodes - 1) // 2
        target_edges = min(int(max_possible_edges * edge_density), max_possible_edges)

        if ensure_hamiltonian:
            nodes = list(range(num_nodes))
            random.shuffle(nodes)
            for i in range(num_nodes):
                u, v = nodes[i], nodes[(i + 1) % num_nodes]
                edges.add((min(u, v), max(u, v)))

            while len(edges) < target_edges:
                u, v = sorted(random.sample(range(num_nodes), 2))
                if (u, v) not in edges:
                    edges.add((u, v))
        else:
            issues = [
                "cycle_with_missing_connection",
                "isolated_nodes",
                "dead_ends",
                "sparse_graph",
                "multiple_small_cycles",
                "unbalanced_degree_distribution",
                "critical_bridge_node",
            ]
            selected_issue = random.choice(issues)

            if selected_issue == "isolated_nodes":
                num_isolated_nodes = random.randint(1, max(1, num_nodes // 5))
                isolated_nodes = random.sample(range(num_nodes), num_isolated_nodes)
                reasons.append(f"isolated_nodes: {isolated_nodes}")
                non_isolated_nodes = [n for n in range(num_nodes) if n not in isolated_nodes]
                while len(edges) < target_edges:
                    u, v = sorted(random.sample(non_isolated_nodes, 2))
                    edges.add((u, v))

            elif selected_issue == "cycle_with_missing_connection":
                nodes = list(range(num_nodes))
                random.shuffle(nodes)
                for i in range(num_nodes):
                    u, v = nodes[i], nodes[(i + 1) % num_nodes]
                    edges.add((min(u, v), max(u, v)))
                num_removed_edges = random.randint(1, 3)
                for _ in range(num_removed_edges):
                    if edges:
                        edge_to_remove = random.choice(list(edges))
                        edges.remove(edge_to_remove)
                reasons.append(f"cycle_with_missing_connection: removed {num_removed_edges} edges")

            elif selected_issue == "multiple_small_cycles":
                num_cycles = random.randint(2, 4)
                subgraph_sizes = [num_nodes // num_cycles] * num_cycles
                subgraph_sizes[0] += num_nodes % num_cycles 
        
                start = 0
                for size in subgraph_sizes:
                    cycle_nodes = list(range(start, start + size))
                    if size < 2:
                        continue
                    for i in range(size):
                        u, v = cycle_nodes[i], cycle_nodes[(i + 1) % size]
                        edges.add((min(u, v), max(u, v)))
                    start += size

                reasons.append("multiple_small_cycles")

            elif selected_issue == "unbalanced_degree_distribution":
                while len(edges) < target_edges and len(edges) < max_possible_edges:
                    u, v = sorted(random.sample(range(num_nodes), 2))
                    edges.add((u, v))

                low_degree_nodes = random.sample(range(num_nodes), random.randint(1, max(1, num_nodes // 5)))
                for node in low_degree_nodes:
                    connected_edges = [e for e in edges if node in e]
                    if len(connected_edges) > 1:
                        for e in connected_edges[1:]:
                            edges.remove(e)
                reasons.append(f"unbalanced_degree_distribution: {low_degree_nodes}")

            elif selected_issue == "multiple_small_cycles":
                num_cycles = random.randint(2, 4)
                subgraph_sizes = [num_nodes // num_cycles] * num_cycles
                subgraph_sizes[0] += num_nodes % num_cycles 

                start = 0
                for size in subgraph_sizes:
                    cycle_nodes = list(range(start, start + size))
                    if size < 2:
                        continue
                    for i in range(size):
                        u, v = cycle_nodes[i], cycle_nodes[(i + 1) % size]
                        edges.add((min(u, v), max(u, v)))
                    start += size

                reasons.append("multiple_small_cycles")

            elif selected_issue == "dead_ends":
                while len(edges) < target_edges:
                    u, v = sorted(random.sample(range(num_nodes), 2))
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
                while len(edges) < target_edges // 2: 
                    u, v = sorted(random.sample(range(num_nodes), 2))
                    edges.add((u, v))

                reasons.append(f"sparse_graph with edge_density={edge_density/2}")

            elif selected_issue == "critical_bridge_node":
                bridge_node = random.choice(range(num_nodes))
                left_subgraph = [n for n in range(num_nodes) if n != bridge_node][:num_nodes // 2]
                right_subgraph = [n for n in range(num_nodes) if n != bridge_node][num_nodes // 2:]

                for subgraph in [left_subgraph, right_subgraph]:
                    while len(edges) < target_edges // 2:
                        u, v = sorted(random.sample(subgraph, 2))
                        edges.add((u, v))

                for subgraph in [left_subgraph, right_subgraph]:
                    if len(edges) < target_edges:
                        u = bridge_node
                        v = random.choice(subgraph)
                        edges.add((min(u, v), max(u, v)))

                reasons.append(f"critical_bridge_node: {bridge_node}")

        edges = list(edges)[:max_possible_edges]
        output = [f"{num_nodes}"]
        output.extend([f"{u} {v}" for u, v in edges])
        question = "\n".join(output)

        try:
            cycle, verify = has_hamiltonian_cycle(num_nodes, edges, timeout=1)
        except TimeoutException:
            print("Timeout while verifying Hamiltonian Cycle. Retrying...")
            continue  
        except Exception as e:
            print(f"Unexpected error: {e}")
            continue
        if isinstance(cycle, list):
            cycle.append(cycle[0])
        problem["question"] = question
        problem["answer"] = cycle if verify else "NO"
        problem["reason"] = cycle if verify else reasons
        return problem

def string_to_md5(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()

def transform_problem_to_meta(problem, idx, language, split):
    timestamp = str(time.time())
    id_string = f"hamiltonian_path_{idx}_{timestamp}"
    hash_id_string = string_to_md5(id_string)
    return {
        "id": hash_id_string,
        "question": problem["question"],
        "answer": problem["answer"],
        "rationale": problem["reason"],
        "split": split,
        "type": PUZZLE_TYPE,
        "source_url": SOURCE_URL,
        "dataset_name": DATASET_NAME,
        "difficulty_level": problem.get("difficulty_level", "medium"),
        "language": language,
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
        problem = generate_hamiltonian_cycle_problem(**params)
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
    with open(output_file, 'w', encoding='utf-8') as f:
        for difficulty in ["easy", "medium", "hard"]:
            for item in generate(count // 3, difficulty=difficulty, language=language, split=split):
                f.write(json.dumps(item, ensure_ascii=False) + '\n')

if __name__ == "__main__":
    save_to_jsonl('train_en.jsonl', 20000, language='en', split="train")
    save_to_jsonl('test_en.jsonl', 1500, language='en', split="eval")
