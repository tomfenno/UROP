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
    # match move:
    #         case "n" | "N":
    #             return (-1, 0)
    #         case "s" | "S":
    #             return (1, 0)
    #         case "e" | "E":
    #             return (0 ,1)
    #         case "w" | "W":
    #             return (0, -1)
    return
        
def manhattan_norm(current, goal):
    return abs(current[0] - goal[0]) + abs(current[1] - goal[1])
    
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
    rows, columns = 10, 15
    goals = [(1,1), (1, 13)]
    start = (8, 7)

    print("The user will begin at:", start)
    grid = np.full((rows, columns), '*', dtype='U2')
    grid[start] = 'S'
    for i in range(len(goals)):
        grid[goals[i]] = 'G' + str(i + 1)
        # TODO
        # start_to_goals.append(manhattan_norm(start, goals[i]), goals[i])

    path = []
    path.append(start)

    move = (0, 0)
    user = start
    predictions = []

    while move != "x":
        print(grid)
        for goal in goals:
            predictions.append((np.exp(-(len(path) - 1) - manhattan_norm(user, goal))) / np.exp(-manhattan_norm(start, goal)))
            np_predictions = np.array(predictions[-len(goals):])
            
        probabilities = np_predictions/np.sum(np_predictions)

        for i in range(len(goals)):
            print("Goal", i + 1, "probability:", round(probabilities[i - len(goals)], 2))

        move = player_move(input())
        grid[user] = 'X'
        user = (path[-1][0] + move[0], + path[-1][1] + move[1])
        path.append(user)
        grid[user] = 'U'
        print("The user is now at:", user) 
        # print(goals)
        # time.sleep(1)

if __name__ == "__main__":
    main()