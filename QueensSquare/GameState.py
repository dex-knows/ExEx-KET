from Helpful import Slope

#This is the Game State Module for the Queens Square Problem.

#Represent the queens
class Queen(object):
    def __init__(self, Position):
        """Takes an arguement to represent the (x, y) coordinate of the Queen"""
        self.Position = Position

#Represents the actually game execution
class Game(object):
    def __init__(self):
        self.__DefaultStart = -1, -1

    def NewGame(self, GameSize):
        self.__Size = GameSize
        self.Queens = []
        self.Queens = [Queen(self.__DefaultStart) for i in\
                                                  xrange(self.__Size)]
        self.__Attempts = 0

    def GetSize(self):
        return self.__Size

    def GetQueensPositions(self):
        Positions = []
        for ThisQueen in self.Queens:
            Positions.append(ThisQueen.Position)
        return Positions

    def MoveQueen(self, QueenNumber, NewPosition):
        """Moves the specified queen to a new position

           The queen will be referenced by an index matching the 
           GetQueensPositions function.
           Will only accept valid positions. Valid positions being:
           the lowest left hand corner of the board being (0, 0) and
           the highest right hand cornder of the board being (n-1, n-1)
           where n is the size of the game."""

        #Checks for valid position and queen number
        if (self._ValidPosition(NewPosition)) and (QueenNumber < self.__Size):
            self.Queens[QueenNumber].Position = NewPosition
            return True
        else:
            return False

    def IsEndState(self):
        """Returns whether the queens position is valid for a Queens Square"""
        self.__Attempts = self.__Attempts + 1
        if (self._QueensOnBoard()) and (self._QueensPositionValidity()):
            return True
        else:
            return False

    def _ValidPosition(self, Position):
        """Checks to see if the position is on the current game board"""
        if (0 <= Position[0]) and (Position[0] < self.__Size)\
            and ( 0 <= Position[1] ) and (Position[1] < self.__Size):
            return True
        else:
            return False

    def _QueensOnBoard(self):
        """Checks to make sure all queens are on the board."""
        for ThisQueen in self.Queens:
            if (self._ValidPosition(ThisQueen.Position) == False):
                return False
        return True

    def _QueensPositionValidity(self):
        """Checks to see if Queens are positions correctly"""
        for QueenA in xrange(self.__Size):
            for QueenB in xrange(QueenA + 1, self.__Size):
                slope = Slope(self.Queens[QueenA].Position,\
                              self.Queens[QueenB].Position)
                    #Checks to see if Queens are on diagonally, horizontally
                    # or vertically aligned.
                if (slope == -1) or (slope == 1) or (slope == 0):
                    return False
        return True

    def PrintBoard(self):
        """Creates a graphical representation of what the board looks like"""
        GenericRow = []
        Layout = []
        for a in xrange(self.__Size):
            Layout.append([])
            for b in xrange(self.__Size):
                Layout[a].append("[ ]")

        for ThisQueen in self.Queens:
            if self._ValidPosition(ThisQueen.Position):
                Layout[ThisQueen.Position[0]][ThisQueen.Position[1]] = "[X]"

        for a in xrange(len(Layout)):
            for b in xrange(len(Layout[a])):
                 print Layout[a][b],
            print
    def GetAttempts(self):
        """Provides the number of attempts"""
        return self.__Attempts
