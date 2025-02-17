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

# Tutorial sample #6: Discrete movement, rewards, and learning

# The "Cliff Walking" example using Q-learning.
# From pages 148-150 of:
# Richard S. Sutton and Andrews G. Barto
# Reinforcement Learning, An Introduction
# MIT Press, 1998

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

if sys.version_info[0] == 2:
    # Workaround for https://github.com/PythonCharmers/python-future/issues/262
    import Tkinter as tk
else:
    import tkinter as tk

def manhattan_norm(current, goal):
        return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

def probabilities_step(grid, user):
    global path, goals
    print(grid)
    for goal in goals:
        predictions.append((np.exp(-(len(path) - 1) - manhattan_norm(user, goal))) / np.exp(-manhattan_norm(start, goal)))
        np_predictions = np.array(predictions[-len(goals):])
        
    probabilities = np_predictions/np.sum(np_predictions)

    for i in range(len(goals)):
        print("Goal", i + 1, "probability:", round(probabilities[i - len(goals)], 6))

    grid[user] = 'X'
    path.append(user)
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
        # self.path = []
        self.canvas = None
        self.root = None
        
    
    def act(self, world_state, backend_grid):
        """take 1 action in response to the current world state"""
        
        obs_text = world_state.observations[-1].text
        obs = json.loads(obs_text) # most recent observation
        self.logger.debug(obs)
        if not u'XPos' in obs or not u'ZPos' in obs:
            self.logger.error("Incomplete observation received: %s" % obs_text)
            return 0
        
        # Original orientation (x, z)
        # current_s = "%d:%d" % (int(obs[u'XPos']), int(obs[u'ZPos']))
        
        global prev_state, current_state
        prev_state = current_state
        current_state = (int(obs[u'ZPos']), int(obs[u'XPos']))

        if manhattan_norm(prev_state, current_state) > 0:
            probabilities_step(backend_grid, current_state)

        current_s = "%d:%d" % (int(obs[u'ZPos']), int(obs[u'XPos']))
        self.logger.debug("State: %s (x = %.2f, z = %.2f)" % (current_s, float(obs[u'XPos']), float(obs[u'ZPos'])))

        # self.drawQ( curr_x = int(obs[u'XPos']), curr_y = int(obs[u'ZPos']) )

        # random action
        # rnd = random.random()
        # a = random.randint(0, len(self.actions) - 1)
        # self.logger.info("Random action: %s" % self.actions[a])

        # a = 1
        # self.logger.info("Action: %s" % self.actions[a])

        # try to send the selected action, only update prev_s if this succeeds
        # try:
        #     agent_host.sendCommand(self.actions[a])
        #     self.prev_s = current_s
        #     self.prev_a = a

        # except RuntimeError as e:
        #     self.logger.error("Failed to send command: %s" % e)

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
            
        # self.drawQ()
        
    # def drawQ( self, curr_x=None, curr_y=None ):
    #     scale = 40
    #     world_x = 6
    #     world_y = 14
    #     if self.canvas is None or self.root is None:
    #         self.root = tk.Tk()
    #         self.root.wm_title("Q-table")
    #         self.canvas = tk.Canvas(self.root, width=world_x*scale, height=world_y*scale, borderwidth=0, highlightthickness=0, bg="black")
    #         self.canvas.grid()
    #         self.root.update()
    #     self.canvas.delete("all")
    #     action_inset = 0.1
    #     action_radius = 0.1
    #     curr_radius = 0.2
    #     action_positions = [ ( 0.5, action_inset ), ( 0.5, 1-action_inset ), ( action_inset, 0.5 ), ( 1-action_inset, 0.5 ) ]
    #     # (NSWE to match action order)
    #     min_value = -20
    #     max_value = 20
    #     for x in range(world_x):
    #         for y in range(world_y):
    #             s = "%d:%d" % (x,y)
    #             self.canvas.create_rectangle( x*scale, y*scale, (x+1)*scale, (y+1)*scale, outline="#fff", fill="#000")
    #             for action in range(4):
    #                 if not s in self.q_table:
    #                     continue
    #                 value = self.q_table[s][action]
    #                 color = int( 255 * ( value - min_value ) / ( max_value - min_value )) # map value to 0-255
    #                 color = max( min( color, 255 ), 0 ) # ensure within [0,255]
    #                 color_string = '#%02x%02x%02x' % (255-color, color, 0)
    #                 self.canvas.create_oval( (x + action_positions[action][0] - action_radius ) *scale,
    #                                          (y + action_positions[action][1] - action_radius ) *scale,
    #                                          (x + action_positions[action][0] + action_radius ) *scale,
    #                                          (y + action_positions[action][1] + action_radius ) *scale, 
    #                                          outline=color_string, fill=color_string )
    #     if curr_x is not None and curr_y is not None:
    #         self.canvas.create_oval( (curr_x + 0.5 - curr_radius ) * scale, 
    #                                  (curr_y + 0.5 - curr_radius ) * scale, 
    #                                  (curr_x + 0.5 + curr_radius ) * scale, 
    #                                  (curr_y + 0.5 + curr_radius ) * scale, 
    #                                  outline="#fff", fill="#fff" )
    #     self.root.update()

if sys.version_info[0] == 2:
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
    import functools
    print = functools.partial(print, flush=True)

# Hard code to set-up backend grid
rows, columns = 10, 15
goals = [(1,1), (1, 13)]
start = (8, 7)
predictions = []
current_state = start
prev_state = start
path = []

agent = Agent()
agent_host = MalmoPython.AgentHost()
try:
    agent_host.parse( sys.argv )
except RuntimeError as e:
    print('ERROR:',e)
    print(agent_host.getUsage())
    exit(1)
if agent_host.receivedArgument("help"):
    print(agent_host.getUsage())
    exit(0)

# -- set up the mission -- #
mission_file = './goal_prediction.xml'
with open(mission_file, 'r') as f:
    print("Loading mission from %s" % mission_file)
    mission_xml = f.read()
    my_mission = MalmoPython.MissionSpec(mission_xml, True)

max_retries = 3
    
my_mission_record = MalmoPython.MissionRecordSpec()

for retry in range(max_retries):
    try:
        agent_host.startMission( my_mission, my_mission_record )
        break
    except RuntimeError as e:
        if retry == max_retries - 1:
            print("Error starting mission:",e)
            exit(1)
        else:
            time.sleep(2.5)

print("Waiting for the mission to start", end=' ')
world_state = agent_host.getWorldState()
while not world_state.has_mission_begun:
    print(".", end="")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print("Error:",error.text)
print()

# -- run the agent in the world -- #
agent.run(agent_host)

print("Done.")

print()
