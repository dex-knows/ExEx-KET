from GameState import GameState

class Agent:
    
    def __init__(self, GameState, policyFileName):
        self._game = GameState
        self._policies = []
        self._policy = ()
        self._inputPolicies(policyFileName)
        
    def _inputPolicies(self, fileName):
        policyFile = open(fileName)
        policyString = policyFile.read().split("\n")
        start = 0
        end = 0
        lower = 0
        upper = 0
        policyMapRow = []
        policyMap = []
        for y in range(len(policyString)):
            policyLine = policyString[y].split(" ")
            if policyLine[0] == "TIME":
                start = int(policyLine[1])
                end = int(policyLine[2])
            elif policyLine[0] == "REWARD":
                lower = int(policyLine[1])
                upper = int(policyLine[2])
            else:
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
                policyMapRow = []
                
            if len(policyMap) == len(self._game.getMap()):
                self._policies.append((start, end, lower, upper, policyMap))
                policyMap = []
                
    def _choosePolicy(self):
        time = self._game.getTime()
        reward = self._game.getReward()
        for x in self._policies:
            if time >= x[0] and time <= x[1]:
                if reward >= x[2] and reward <= x[3]:
                    self._policy = x
                    print("Policy Change")
                    
    def move(self):
        location = self._game.getAgentPosition()
        self._choosePolicy()
        if not self._game.isEndOfGame():
            direction = self._policy[4][location[1]][location[0]]
            self._game.moveAgent(direction)
        print(self._game.getAgentPosition())
        
        
        
        
        