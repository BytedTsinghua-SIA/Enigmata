PROMPT_TEMPLATE = """
You are tasked with solving a Hamiltonian Path Puzzle.

### Rules:
A **Hamiltonian Path** in an undirected graph is a path that visits every vertex exactly once. The task is to determine whether a Hamiltonian Path exists in the given graph.

The graph is represented as follows:
- The first line contains a single integer `N`, which is the number of vertices in the graph.
- The subsequent lines each describe an edge in the graph. Each edge is represented by two space-separated integers `u` and `v`, which indicate that there is an undirected edge between vertex `u` and vertex `v`.
- The vertices are numbered from `0` to `N-1`.
    
### Response Format:
- Please output your answer within a code block (```) as follows:
```
<result>
```
- <result> should be a list of vertex indices that form the Hamiltonian Path if it exists, for example:
```
[0, 2, 3, 1, 0]
```
- If no Hamiltonian Path exists, <result> should be "NO".
Here is the puzzle:
{question} 
""".strip()

PROMPT_TEMPLATE_ZH = """
你的任务解决一个哈密顿路径（Hamiltonian Path）问题。

### 规则：
1. 哈密顿路径是无向图中的一条路径，该路径恰好访问每个顶点一次。任务是判断给定的图中是否存在哈密顿路径。

2. 图的表示方式如下：
- 第一行包含一个整数 `N`，表示图中的顶点数量。
- 后续每一行描述图中的一条边。每条边由两个以空格分隔的整数 `u` 和 `v` 表示，表示在顶点 `u` 和顶点 `v` 之间存在一条无向边。
- 顶点编号从 `0` 到 `N-1`。

### 回答格式：
- 输出格式为JSON格式:
```json
{{
  "answer": "<result>"
}}
```
- <result> 应该是一个包含构成哈密顿路径的顶点索引的列表，例如：[0, 2, 3, 1]。
- 如果图中不存在哈密顿路径，<result> 应该为 "NO"。

请解决以下的题目：
{question}
""".strip()