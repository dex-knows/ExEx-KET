""" This class performs necessary functions of an agent manipulating it environment. The class also inputs the policies for an agent from
    a file. A policy is stored as a tuple formatted as such: (start time, end time, upper reward bound, lower reward bound, map with 
    directions). In the map, 1 denotes up, 2 denotes right, 3 denotes left, 4 denotes left, and % denotes a wall. The file should be formatted
    as follows: the first line is the start and end times to use the policies in that time frame, the second denotes the reward bounds to
    use the policy, and the rest is the map (must have exactly same layout as map file used by GameState) with directions. Every line
    denoting times must start with "TIME" followed by a space and every reward line must start "REWARD". The agent will evaluate and choose
    policies based on time first then reward.
"""

from GameState import GameState

class Agent:
    
    def __init__(self, GameState, policyFileName):
        """An agent will receive the GameState to be manipulated and the file name of the file containing the policies for that agent
        """
        self._game = GameState
        self._policies = []
        self._policy = ()
        self._inputPolicies(policyFileName)
        
    def _inputPolicies(self, fileName):
        """ Inputs the policies into a 2-D list
        """
        policyFile = open(fileName)
        policyString = policyFile.read().split("\n")
        start = 0
        end = 0
        lower = 0
        upper = 0
        policyMapRow = []
        policyMap = []
        for y in range(len(policyString)):
            policyLine = policyString[y].split(" ")  #gets time line
            if policyLine[0] == "TIME":
                start = int(policyLine[1])
                end = int(policyLine[2])
            elif policyLine[0] == "REWARD":   #gets reward line
                lower = int(policyLine[1])
                upper = int(policyLine[2])
            else:                           #gets map line by line
                for x in range(len(self._game.getMap()[0])):
                    if policyLine[0][x] == "1":
                        policyMapRow.append("UP")
                    elif policyLine[0][x] == "2":
                        policyMapRow.append("RIGHT")
                    elif policyLine[0][x] == "3":
                        policyMapRow.append("DOWN")
                    elif policyLine[0][x] == "4":
                        policyMapRow.append("LEFT")
                    elif policyLine[0][x] == "0":
                        policyMapRow.append("STAY")
                    else:
                        policyMapRow.append("%")
                policyMap.append(policyMapRow)
                policyMapRow = []      #clears row to add to map
                
            if len(policyMap) == len(self._game.getMap()):  #adds full policy to policies list
                self._policies.append((start, end, lower, upper, policyMap))
                policyMap = []
                
    def _choosePolicy(self):
        """ Chooses policy based on current time step and total reward in the GameState of the agent
        """
        time = self._game.getTime()
        reward = self._game.getReward()
        for x in self._policies:
            if time >= x[0] and time <= x[1]:
                if reward >= x[2] and reward <= x[3]:
                    self._policy = x
                    
    def move(self):
        """ Tells the GameState where to move the agent based on the current policy
        """
        location = self._game.getAgentPosition()
        self._choosePolicy()
        if not self._game.isEndOfGame():
            direction = self._policy[4][location[1]][location[0]]  #map represented as (y, x) locations
            self._game.moveAgent(direction)