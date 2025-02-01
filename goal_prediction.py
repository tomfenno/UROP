import numpy as np
from copy import deepcopy
from collections import deque
import time

# gs = []
# p1 = []
# print("Please specify the dimensions of the grid:")
# rows, columns = map(int, input().split())
# print("Grid is", rows, "x", columns)
# print("Enter the number of goal states:")
# num_of_goals = int(input())
# print("For each goal, enter its coordinates:")
# for i in range(num_of_goals):
#     x, y = map(int, input().split())
#     gs.append((x, y))
# print("There is a goal at:")
# for g in gs:
#     print(g)
# print("Enter the coordinates of# the start position:")
# x, y = map(int, input().split())
# p1.append((x, y))
# print("The user will begin at:", p1)

def predict_goal(grid, path):
    for i in range(len(path)):
        grid[path[i]] = 'x'
        for j in range(len(goals)):
            user_to_goals.append(bfs(grid, path[i], goals[j], deepcopy(dummy_path)))
            
            probabilities.append((prob, i + 1))
        print(grid)
        print("Step", i, ":")
        print("Start to goals:", start_to_goals)
        print("User to goals:", user_to_goals)
        print("Probabilities:", probabilities[0])
        time.sleep(5)

def bfs(matrix, start, end):
    path = []
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

start_to_goals, user_to_goals, user_to_each_goal, probabilities = [], [], [], []
rows, columns = 4, 5
goals = [(0,0), (0, 4)]
path = [(3, 2), (2, 2), (1, 2), (0, 2), (0, 1), (0, 0)]
start = path[0]
grid = np.full((rows, columns), '*', dtype='U1')
grid[path[0]] = 'S'

for goal in goals:
    grid[goal] = 'G'
    start_to_goals.append(bfs(grid, path[0], goal))

for step in path:
    for goal in goals:
        user_to_each_goal.append(bfs(grid, step, goal))
    user_to_goals.append((user_to_each_goal[0], user_to_each_goal[1]))
    user_to_each_goal.clear()

g1_likelihoods, g2_likelihoods, g1_probs, g2_probs = [], [], [], []


print(grid)
print(start_to_goals)
print(user_to_goals)

for i in range(len(path)):
    # prob = abs(((i) - user_to_goals[i][0]) / start_to_goals[i])
    # print("Step", i, "Goal 1:", user_to_goals[i][0])
    # print("Step", i, "Goal 2:", user_to_goals[i][1])
    g1_likelihoods.append(abs(((i) - user_to_goals[i][0]) / start_to_goals[0]))
    g2_likelihoods.append(abs(((i) - user_to_goals[i][1]) / start_to_goals[1]))

for i in range(len(path)):
    g1_probs.append(g1_likelihoods[i]/(g1_likelihoods[i] + g2_likelihoods[i]))
    g2_probs.append(g2_likelihoods[i]/(g1_likelihoods[i] + g2_likelihoods[i]))

print("G1 probs:", g1_probs)
print("G2 probs:", g2_probs)
# print(grid)
# print(start_to_goals)
# print(user_to_goals)