import random
import collections
import json
from .template import PROMPT_TEMPLATE
from tqdm import tqdm

def generate_maze(width, height, percentage=0.35):
    maze = [['.' for _ in range(width)] for _ in range(height)]
    
    num_obstacles = int((width * height) * percentage)
    for _ in range(num_obstacles):
        x, y = random.randint(0, width-1), random.randint(0, height-1)
        maze[y][x] = 'B'
    
    maze[0][0] = 'S'
    maze[height-1][width-1] = 'E'
    
    return maze


def print_maze(maze):
    for row in maze:
        print(' '.join(row))

def maze_to_str(maze):
    s = "\n".join([" ".join(row)for row in maze])
    return s

def get_answer(maze, lang='en'):
    rows, cols = len(maze), len(maze[0])

    # 定义起点和终点
    start = (0, 0)  # S (1, 1)
    end = (rows - 1, cols - 1)    # E (4, 5)

    # 定义四个方向的移动
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # BFS搜索最短路径
    def bfs(maze, start, end):
        queue = collections.deque([(start, [start])])
        visited = set([start])

        while queue:
            (x, y), path = queue.popleft()
            
            if (x, y) == end:
                return path

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                
                if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited and maze[nx][ny] != 'B':
                    queue.append(((nx, ny), path + [(nx, ny)]))
                    visited.add((nx, ny))

        return None

    # 找到路径
    path = bfs(maze, start, end)

    # 格式化输出
    if path:
        path_str = "->".join(f"({x+1},{y+1})" for x, y in path)
        answer = f"The answer is: {path_str}"
    else:
        answer = "The answer is: not exist."

    return answer

def generate(count=100, difficulty='medium', language='en', split="train"):
    height=5
    width=5
    prompt_template = PROMPT_TEMPLATE
    exist = {}
    dif_level = {"easy" : [15,25], "medium" : [26,40], "hard" : [41,55]}
    for i in tqdm(range(count)):
        while True:
            # random.seed(random.randint(0, 1024))
            #p = random.random() * 0.35 + 0.25
            p = random.randint(dif_level[difficulty][0], dif_level[difficulty][1])/100
            num_obs = int(p*height*width)
            maze = generate_maze(width, height, p)
            has_str = maze_to_str(maze)
            if has_str in exist:
                continue
            else:
                exist[has_str] = 1
                break
        answer = get_answer(maze, lang=language)
        yield {
            "prompt": prompt_template.format(question=maze_to_str(maze)),
            "answer":  answer,
            "task_name": "maze",    
            "ability": "logic_puzzle", 
            "language": language,
            "meta": json.dumps({
                "id":"maze_"+difficulty+'_'+str(i),
                "question": maze,
                "width": width,
                "height": height,
                "num_obstacles":num_obs,
                "answer": answer,
                "rationale": "", 
                "split": split,
                "type": "sequential_puzzle", 
                "source_url": "auto-generated", 
                "dataset_name": "maze", 
                "difficulty_level": difficulty,
                "language": language,
            }),
        }
def save_to_jsonl(output_file, count, lange='en'):
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in generate(5, 5, count//3, 'easy', lange):
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
        for item in generate(5, 5, count//3, 'medium', lange):
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
        for item in generate(5, 5, count//3, 'hard', lange):
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

