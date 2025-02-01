import numpy as np
from copy import deepcopy
from collections import deque
import time

def predict_goal(rows, columns, goals, path):
    grid = np.full((rows, columns), '*', dtype='U1')
    grid[path[0]] = 'S'
    dummy_path = []
    start_to_goals, user_to_goals, probabilities = [], [], []
    for goal in goals:
        grid[goal] = 'G'
        start_to_goals.append(bfs(grid, path[0], goal, deepcopy(dummy_path)))
    for i in range(len(path)):
        grid[path[i]] = 'x'
        for j in range(len(goals)):
            user_to_goals.append(bfs(grid, path[i], goals[j], deepcopy(dummy_path)))
            prob = abs(((len(path) - 1) - user_to_goals[j]) / start_to_goals[j]) / len(goals)
            probabilities.append((prob, i + 1))
        print(grid)
        print("Step", i, ":")
        print("Start to goals:", start_to_goals)
        print("User to goals:", user_to_goals)
        print("Probabilities:", probabilities[0])
        time.sleep(5)

def bfs(matrix, start, end, path):
    queue = deque([(start[0], start[1], 0)])
    while queue:
        i, j, steps = queue.popleft()
        if (i, j) == end:
            return steps
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        for direction in directions:
            if in_bounds(matrix, tuple(np.add((i, j), direction)), path):
                path.append(tuple(np.add((i, j), direction)))
                queue.append((i + direction[0], j + direction[1], steps + 1))
    return float('-inf')  

def in_bounds(matrix, position, path):
    i, j = position[0], position[1]
    if i >= matrix.shape[0] or i < 0 or j >= matrix.shape[1] or j < 0 or position in path:
        return False
    else:
        return True

gs = [(0,0), (0, 4)]
p1 = [(3, 2)]

predict_goal(4, 5, gs, p1)