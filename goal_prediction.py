import numpy as np
from collections import deque
import time

def bfs(matrix, start, end):
    path = []
    queue = deque([(start[0], start[1], 0)])
    while queue:
        i, j, steps = queue.popleft()
        if (i, j) == end:
            return steps
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        for direction in directions:
            if in_bounds(matrix, (i + direction[0], j + direction[1]), path):
                path.append((i + direction[0], j + direction[1]))
                queue.append((i + direction[0], j + direction[1], steps + 1))
    return float('-inf')  

def in_bounds(matrix, position, path):
    i, j = position[0], position[1]
    if i >= matrix.shape[0] or i < 0 or j >= matrix.shape[1] or j < 0 or position in path:
        return False
    else:
        return True

def player_move(move):
    match move:
            case "n" | "N":
                return (-1, 0)
            case "s" | "S":
                return (1, 0)
            case "e" | "E":
                return (0 ,1)
            case "w" | "W":
                return (0, -1)
    
def main():
    # Code for reading input for different types of grids/goals
    # goals = []
    # print("Please specify the dimensions of the grid:")
    # rows, columns = map(int, input().split())
    # print("Grid is", rows, "x", columns)
    # print("Enter the number of goal states:")
    # num_of_goals = int(input())
    # print("For each goal, enter its coordinates:")
    # for i in range(num_of_goals):
    #     x, y = map(int, input().split())
    #     goals.append((x, y))
    # print("There is a goal at:")
    # for g in goals:
    #     print(g)
    # print("Enter the coordinates of the start position:")
    # x, y = map(int, input().split())
    # start = (x, y)

    # fixed values
    rows, columns = 4, 5
    goals = [(0,0), (0, 4)]
    start = (3, 2)

    print("The user will begin at:", start)
    start_to_goals, user_to_goals = [], []

    grid = np.full((rows, columns), '*', dtype='U1')
    grid[start] = 'S'
    for goal in goals:
        grid[goal] = 'G'
        start_to_goals.append(bfs(grid, start, goal))

    path = []
    path.append(start)

    move = (0, 0)
    user = start

    while move != "x":
        print(grid)
        for goal in goals:
            user_to_goals.append(bfs(grid, user, goal))
        goal1_prediction = abs(((len(path) - 1) - user_to_goals[0]) / start_to_goals[0])
        goal2_prediction = abs(((len(path) - 1)  - user_to_goals[1]) / start_to_goals[1])
        goal1_probability = round(goal1_prediction / (goal1_prediction + goal2_prediction), 2)
        goal2_probability = round(goal2_prediction / (goal1_prediction + goal2_prediction), 2)
        print("Goal 1 Probability:", goal1_probability)
        print("Goal 2 Probability:", goal2_probability)

        user_to_goals.clear()
        move = player_move(input())
        user = (path[-1][0] + move[0], + path[-1][1] + move[1])
        path.append(user)
        grid[user] = 'X'
        print("The user is now at:", user) 
        # time.sleep(1)

if __name__ == "__main__":
    main()