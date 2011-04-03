""" This class holds the game state of Clutz. Input for the map comes from a file specified when creating the GameState object.
    Input should be formatted as having the first line holding the values for the 'winning' and 'losing'  rewards. The winning
    reward comes first, then the losing separated by a single space. The next part of the file is the layout of the map with %
    specifying walls, a W specifying the winning location, and a L specifying the losing location. The game state controls almost
    all aspects of the game. In this class, movement is handled (including validation), time is kept (each move is 1 unit of time),
    and the ending state of a game is monitored.
"""

import random

class GameState:
    'The state of the Clutz game, which holds info such as the map, rewards, etc.'\
    
    def __init__(self, mapFileName, stepReward, rightMoveProb, fowardMoveProb, finiteGame, time):
        """ The GameState object receives a file name for the map, a number for the reward of a move, probability of moving to the
            right of intended direction, the probability the move will be in the direction given, if the game is finite or not, and
            the time limit if finite.
        """
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
        """ This takes the input from the file containing the map layout and converts it into a 2-D list.
            Locations on the map will be represented (x, y), but the 2-D list refers to its locations as
            (y, x)
        """
        mapFile = open(file)
        mapString = mapFile.readline().split(" ") #first line containing winning and losing value
        winVal = mapString[0]
        loseVal = mapString[1]
        mapString = mapFile.read().split('\n') #map is separated into lines of strings
        xPlace = 0
        rowList = []  #list holding single line of map
        for x in mapString:
            yPlace = 0
            rowList=[]   #empty list before each iteration
            for y in mapString[xPlace]:
                if mapString[xPlace][yPlace] == '%':    #signifies wall
                    rowList.append(1)
                elif mapString[xPlace][yPlace] == 'W':   #signifies winning location
                    rowList.append(2)
                    self._winPlace = (yPlace, xPlace)
                    self._winReward = int(winVal)
                elif mapString[xPlace][yPlace] == 'L':   #signifies losing location
                    rowList.append(3)
                    self._losePlace = (yPlace, xPlace)
                    self._loseReward = int(loseVal)
                else:
                    rowList.append(0)   #signifies empty space
                yPlace += 1
            self._map.append(rowList)    #adds row to map
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
    
    def restart(self):
        """ Puts the time, reward, and location of agent back to starting values
        """
        self._totalReward = 0
        self._agentLocation = (1,1)
        self._endOfGame = False
        self._gameTime = 0
        
    def moveAgent(self, direction):  
        """ Used for outside call to move agent
        """
        if not self.isEndOfGame():
            self._move(direction)  #move specified direction
            self._addReward()  
            if self._finite:
                self._gameTime += 1  #add to time for each move
        
    def _correctMove(self):
        """ Chooses whether the direction given will be the direction to move
        """
        prob = random.random()  
        if prob <= self._fowardProb:   #returns 0 to denote that the direction will stay the same
            return 0
        elif prob > self._fowardProb and prob <= (self._fowardProb + self._rightProb):    #returns -1 to denote that the direction
            return -1                                                                     #to the right of the given
        elif prob > (self._fowardProb + self._rightProb) and prob <= 1:     #returns 1 to denote the direction will be to the left
            return 1                                                        #of the given
    
    def _isValid(self, location):
        """Checks if the given location is still on the map
        """
        if self._map[location[1]][location[0]] != 1:   #map represents location (y, x)
            return True
        else:
            return False
        
    def _move(self, direction):
         """The agent is moved the direction determined by the given and the probability of moving that direction as long as
            the move is still on the map. Up moves and down moves are backward because of the representation of the map.
         """
         rightMove = self._correctMove() 
         if direction == "UP":
            if rightMove == 0:
                if self._isValid((self._agentLocation[0], self._agentLocation[1]-1)):
                    self._agentLocation = (self._agentLocation[0], self._agentLocation[1]-1)
            elif rightMove == -1:
                if self._isValid((self._agentLocation[0]+1, self._agentLocation[1])):
                    self._agentLocation = (self._agentLocation[0]+1, self._agentLocation[1])
            elif rightMove == 1:
                if self._isValid((self._agentLocation[0]-1, self._agentLocation[1])):
                    self._agentLocation = (self._agentLocation[0]-1, self._agentLocation[1])
                    
         if direction == "DOWN":
            if rightMove == 0:
                if self._isValid((self._agentLocation[0], self._agentLocation[1]+1)):
                    self._agentLocation = (self._agentLocation[0], self._agentLocation[1]+1)
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
        """Adds reward to the total reward received by the agent for this game
        """
        if self._agentLocation == self._winPlace:
            self._totalReward += self._winReward
        elif self._agentLocation == self._losePlace:
            self._totalReward += self._loseReward
        else:
            self._totalReward += self._moveReward
        
    def isEndOfGame(self):
        """ Checks for end of game conditions. End of game occurs when time has reached limit or agent has reached a win or lose 
            location.
        """
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