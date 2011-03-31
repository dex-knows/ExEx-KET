import random

class GameState:
    'The state of the Clutz game, which holds info such as the map, rewards, etc.'\
    
    def __init__(self, mapFileName, stepReward, rightMoveProb, fowardMoveProb, finiteGame, time):
        'This is the constructor for the game state. It gets sent the file name containing the map layout.'
        self._winPlace = (0,0)
        self._winReward = 0
        self._losePlace = (0,0)
        self._loseReward = 0
        self._totalReward = 0
        self._map=[]
        self._rightProb = rightMoveProb
        self._fowardProb = fowardMoveProb
        self._leftProb = 1-rightMoveProb-fowardMoveProb
        self._agentLocation = (1,1)
        self._moveReward = stepReward
        self._endOfGame = False
        self._finite = finiteGame
        self._timeLimit = time
        self._gameTime = 0
        self._inputMap(mapFileName)
        
    def _inputMap(self, file):
        'This takes the input from the file containing the map layout and converts it into a 2-D list.'
        mapFile = open(file)
        mapString = mapFile.readline().split(" ")
        winVal = mapString[0]
        loseVal = mapString[1]
        mapString = mapFile.read().split('\n')
        xPlace = 0
        rowList = []
        for x in mapString:
            yPlace = 0
            rowList=[]
            for y in mapString[xPlace]:
                if mapString[xPlace][yPlace] == '%':
                    rowList.append(1)
                elif mapString[xPlace][yPlace] == 'W':
                    rowList.append(2)
                    self._winPlace = (yPlace, xPlace)
                    self._winReward = int(winVal)
                elif mapString[xPlace][yPlace] == 'L':
                    rowList.append(3)
                    self._losePlace = (yPlace, xPlace)
                    self._loseReward = int(loseVal)
                else:
                    rowList.append(0)
                yPlace += 1
            self._map.append(rowList)
            xPlace += 1
    
    def getAgentPosition(self):
        return self._agentLocation
    
    def getWinLoc(self):
        return (self._winPlace[0], self._winPlace[1])
    
    def getLoseLoc(self):
        return (self._losePlace[0], self._losePlace[1])
    
    def getReward(self):
        return self._totalReward
    
    def getMap(self):
        return self._map
    
    def getTime(self):
        return self._gameTime
    
    def moveAgent(self, direction):  
        if not self.isEndOfGame():
            self._move(direction)
            self._addReward()  
            if self._finite:
                self._gameTime += 1
        self.isEndOfGame()
        
    def _correctMove(self):
        prob = random.random()  
        if prob <= self._fowardProb:
            return 0
        elif prob > self._fowardProb and prob <= (self._fowardProb + self._rightProb):
            return -1
        elif prob > (self._fowardProb + self._rightProb) and prob <= 1:
            return 1
    
    def _isValid(self, location):
        if self._map[location[1]][location[0]] != 1:
            return True
        else:
            return False
        
    def _move(self, direction):
         rightMove = self._correctMove() 
         if direction == "UP":
            if rightMove == 0:
                if self._isValid((self._agentLocation[0], self._agentLocation[1]+1)):
                    self._agentLocation = (self._agentLocation[0], self._agentLocation[1]+1)
            elif rightMove == -1:
                if self._isValid((self._agentLocation[0]+1, self._agentLocation[1])):
                    self._agentLocation = (self._agentLocation[0]+1, self._agentLocation[1])
            elif rightMove == 1:
                if self._isValid((self._agentLocation[0]-1, self._agentLocation[1])):
                    self._agentLocation = (self._agentLocation[0]-1, self._agentLocation[1])
                    
         if direction == "DOWN":
            if rightMove == 0:
                if self._isValid((self._agentLocation[0], self._agentLocation[1]-1)):
                    self._agentLocation = (self._agentLocation[0], self._agentLocation[1]-1)
            elif rightMove == -1:
                if self._isValid((self._agentLocation[0]-1, self._agentLocation[1])):
                    self._agentLocation = (self._agentLocation[0]-1, self._agentLocation[1])
            elif rightMove == 1:
                if self._isValid((self._agentLocation[0]+1, self._agentLocation[1])):
                    self._agentLocation = (self._agentLocation[0]+1, self._agentLocation[1])
                    
         if direction == "LEFT":
            if rightMove == 0:
                if self._isValid((self._agentLocation[0]-1, self._agentLocation[1])):
                   self._agentLocation = (self._agentLocation[0]-1, self._agentLocation[1])
            elif rightMove == -1:
                if self._isValid((self._agentLocation[0], self._agentLocation[1]+1)):
                    self._agentLocation = (self._agentLocation[0], self._agentLocation[1]+1)
            elif rightMove == 1:
                if self._isValid((self._agentLocation[0], self._agentLocation[1]-1)):
                    self._agentLocation = (self._agentLocation[0], self._agentLocation[1]-1)
                    
         if direction == "RIGHT":
            if rightMove == 0:
                if self._isValid((self._agentLocation[0]+1, self._agentLocation[1])):
                      self._agentLocation = (self._agentLocation[0]+1, self._agentLocation[1])
            elif rightMove == -1:
                if self._isValid((self._agentLocation[0], self._agentLocation[1]-1)):
                    self._agentLocation = (self._agentLocation[0], self._agentLocation[1]-1)
            elif rightMove == 1:
                if self._isValid((self._agentLocation[0], self._agentLocation[1]+1)):
                    self._agentLocation = (self._agentLocation[0], self._agentLocation[1]+1)
                    
    def _addReward(self):
        if self._agentLocation == self._winPlace:
            self._totalReward += self._winReward
        elif self._agentLocation == self._losePlace:
            self._totalReward += self._loseReward
        else:
            self._totalReward += self._moveReward
        
    def isEndOfGame(self):
        if self._finite:
            if self._gameTime >= self._timeLimit:
                self._endOfGame = True
                return self._endOfGame
        elif self._agentLocation == self._winPlace:
            self._endOfGame = True
            return self._endOfGame
        elif self._agentLocation == self._losePlace:
            self._endOfGame = True
            return self._endOfGame
        else:
            return self._endOfGame