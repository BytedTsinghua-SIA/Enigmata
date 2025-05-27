PROMPT_TEMPLATE = """
You are tasked with solving a Hamiltonian Cycle Puzzle.

### Rules:
A **Hamiltonian Cycle** in an undirected graph is a cycle that visits every vertex exactly once and returns to the starting vertex. The task is to determine whether a Hamiltonian Cycle exists in the given graph.

The graph is represented as follows:
- The first line contains a single integer `N`, which is the number of vertices in the graph.
- The subsequent lines each describe an edge in the graph. Each edge is represented by two space-separated integers `u` and `v`, which indicate that there is an undirected edge between vertex `u` and vertex `v`.
- The vertices are numbered from `0` to `N-1`.

### Response Format:
- Please output your answer within a code block (```) as follows:
```
<result>
```
- If a Hamiltonian Cycle exists, <result> should be a list of vertex indices that form the cycle, where the last vertex is the same as the first vertex to complete the cycle, for example:
```
[0, 2, 3, 1, 0]
```
- If no Hamiltonian Cycle exists, <result> should be "NO".

Here is the puzzle:
{question} 
""".strip()

PROMPT_TEMPLATE_ZH = """
你的任务是解决一个哈密顿回路（Hamiltonian Cycle）问题。

### 规则：
1. 哈密顿回路是无向图中的一个回路，该回路恰好访问每个顶点一次，并返回到起始顶点。任务是判断给定的图中是否存在哈密顿回路。

2. 图的表示方式如下：
- 第一行包含一个整数 `N`，表示图中的顶点数量。
- 后续每一行描述图中的一条边。每条边由两个以空格分隔的整数 `u` 和 `v` 表示，表示在顶点 `u` 和顶点 `v` 之间存在一条无向边。
- 顶点编号从 `0` 到 `N-1`。

### 回答格式：
- 输出格式为 JSON 格式：
```json
{{
  "answer": "<result>"
}}
```
- 如果哈密顿回路存在，<result> 应该是一个数值列表，表示形成回路的顶点顺序，例如 [0, 2, 3, 1, 0]（其中最后一个顶点与第一个第一个顶点相同形成回路）。
- 如果不存在哈密顿回路，<result> 应该是 "NO"。

请解决以下的题目：
{question}
""".strip()