from __future__ import print_function
# ------------------------------------------------------------------------------------------------
# Copyright (c) 2016 Microsoft Corporation
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED `"AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ------------------------------------------------------------------------------------------------

from builtins import range
from builtins import object
import MalmoPython
import json
import logging
import os
import random
import sys
import time
import numpy as np
import math
import malmoutils

if sys.version_info[0] == 2:
    # Workaround for https://github.com/PythonCharmers/python-future/issues/262
    import Tkinter as tk
else:
    import tkinter as tk

def manhattan_norm(current, goal):
        return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

def euclidean_distance(current, goal):
    np_current, np_goal = np.array(current), np.array(goal)
    np_goal = np_goal + 0.5
    return math.sqrt(sum((np_current - np_goal) ** 2))

def probabilities_step(grid, user):
    user_float = user
    user = (int(user[0]), int(user[1]))
    global path, goals
    print(grid)
    for goal in goals:
        # print("total cost", goal, ":", np.exp(-(len(path) - 1)))
        # print("user->goal", goal, round(euclidean_distance(user_float, goal)))
        # print("whole thing", goal, (np.exp(-(len(path) - 1) - manhattan_norm(user, goal))) / np.exp(-manhattan_norm(start, goal)))
        # prediction = (np.exp(-(len(path) - 1) - euclidean_distance(user_float, goal))) / np.exp(-euclidean_distance(start_float, goal))
        prediction = (np.exp(-(len(path) - 1) - manhattan_norm(user, goal))) / np.exp(-manhattan_norm(start, goal))
        predictions.append(prediction)
        np_predictions = np.array(predictions[-len(goals):])
        
    probabilities = np_predictions/np.sum(np_predictions)

    for i in range(len(goals)):
        print("Goal", i + 1, "probability:", round(probabilities[i - len(goals)], 6))

    path.append(user)
    grid[path[-2]] = 'X'
    grid[user] = 'U'
    print("The Agent is now at:", user)
    return

class Agent(object):
    """Agent that will choose between goal states in the world."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        if False: # True if you want to see more information
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)
        self.logger.handlers = []
        self.logger.addHandler(logging.StreamHandler(sys.stdout))

        self.actions = ["movenorth 1", "movesouth 1", "movewest 1", "moveeast 1"]
        self.canvas = None
        self.root = None
        
    
    def act(self, world_state, backend_grid):

        obs_text = world_state.observations[-1].text
        obs = json.loads(obs_text) # most recent observation
        self.logger.debug(obs)
        if not u'XPos' in obs or not u'ZPos' in obs:
            self.logger.error("Incomplete observation received: %s" % obs_text)
            return 0
        
        global prev_state, current_state
        prev_state = current_state
        current_state = (int(obs[u'ZPos']), int(obs[u'XPos']))
        current_state_float = (float(obs[u'ZPos']), float(obs[u'XPos']))
        # print("current_state:", current_state_float)
        # print("euclidean_distance goal 1:", round(euclidean_distance(current_state_float, goals[0]), 4))
        # print("euclidean_distance goal 2:", round(euclidean_distance(current_state_float, goals[1]), 4))
        # if manhattan_norm(prev_state, current_state) > 0:
        probabilities_step(backend_grid, current_state)

        current_s = "%d:%d" % (int(obs[u'ZPos']), int(obs[u'XPos']))
        self.logger.debug("State: %s (x = %.2f, z = %.2f)" % (current_s, float(obs[u'XPos']), float(obs[u'ZPos'])))

    def run(self, agent_host):
        """run the agent on the world"""
        
        # Set-up grid
        print("The user will begin at:", start)
        grid = np.full((rows, columns), '*', dtype='U2')
        grid[start] = 'S'
        for i in range(len(goals)):
            grid[goals[i]] = 'G' + str(i + 1)
        path.append(start)
        print(grid)


        # main loop:
        world_state = agent_host.getWorldState()
        while world_state.is_mission_running:
            
            # wait until have received a valid observation
            while True:
                time.sleep(0.1)
                world_state = agent_host.getWorldState()
                for error in world_state.errors:
                    self.logger.error("Error: %s" % error.text)
                if world_state.is_mission_running and len(world_state.observations)>0 and not world_state.observations[-1].text=="{}":
                    self.act(world_state, grid)
                    break
                if not world_state.is_mission_running:
                    break

if sys.version_info[0] == 2:
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
    import functools
    print = functools.partial(print, flush=True)

# Hard code to set-up backend grid
rows, columns = 10, 15
goals = [(1, 1), (1, 13)]
start_float = (8.5, 7.5)
start = (8, 7)
predictions = []
current_state = start
prev_state = start
path = []

# malmoutils.fix_print()

# -- Instantiating the agents -- #
human = Agent()
human_host = MalmoPython.AgentHost()
bot = Agent()
bot_host = MalmoPython.AgentHost()
try:
    human_host.parse( sys.argv )
except RuntimeError as e:
    print('ERROR:',e)
    print(human_host.getUsage())
    exit(1)
if human_host.receivedArgument("help"):
    print(human_host.getUsage())
    exit(0)

malmoutils.parse_command_line(human_host)

# -- set up the mission -- #
mission_file = './goal_prediction.xml'
with open(mission_file, 'r') as f:
    print("Loading mission from %s" % mission_file)
    mission_xml = f.read()
    my_mission = MalmoPython.MissionSpec(mission_xml, True)

max_retries = 3
    
my_mission_record = MalmoPython.MissionRecordSpec()

client_pool = MalmoPython.ClientPool()
client_pool.add( MalmoPython.ClientInfo('127.0.0.1',10000) )
client_pool.add( MalmoPython.ClientInfo('127.0.0.1',10001) )

for retry in range(max_retries):
    try:
        human_host.startMission( my_mission, my_mission_record )
        break
    except RuntimeError as e:
        if retry == max_retries - 1:
            print("Error starting mission:",e)
            exit(1)
        else:
            time.sleep(2.5)

print("Waiting for the mission to start", end=' ')
world_state = human_host.getWorldState()
while not world_state.has_mission_begun:
    print(".", end="")
    time.sleep(0.1)
    world_state = human_host.getWorldState()
    for error in world_state.errors:
        print("Error:",error.text)
print()

# -- run the agent in the world -- #
human.run(human_host)

print("Done.")

print()
