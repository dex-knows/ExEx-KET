#This will contain the code that executes the Queens Square Game
from GameState import Game
from Agent import *

if __name__ == "__main__":
#    a = Game()
#    a.NewGame(4)
#    a.MoveQueen(0, (0, 2))
#    a.MoveQueen(1, (1, 0))
#    a.MoveQueen(2, (2, 3))
#    a.MoveQueen(3, (3, 1))
#    print a.IsEndState()
#    a.MoveQueen(0, (2, 1))
#    print a.IsEndState()
#    a.NewGame(8)
#    a.MoveQueen(0, (0, 1))
#    a.MoveQueen(1, (1, 3))
#    a.MoveQueen(2, (2, 5))
#    a.MoveQueen(3, (3, 7))
#    a.MoveQueen(4, (4, 2))
#    a.MoveQueen(5, (5, 0))
#    a.MoveQueen(6, (6, 6))
#    a.MoveQueen(7, (7, 4))
#    print a.IsEndState()

    for i in xrange(10):
        
        Test = Game()
        GameSize = i + 4
        Test.NewGame(GameSize)
        NumRuns = 100
        TotalAttempts = 0
        for x in xrange(NumRuns): 
            #RandomAgent(Test)
            HillClimber(Test)
            TotalAttempts = TotalAttempts + Test.GetAttempts()

        print "Game Size"
        print GameSize
        print "Average Attemps"
        print TotalAttempts/NumRuns
        print "Total Attempts"
        print TotalAttempts
        print
    
