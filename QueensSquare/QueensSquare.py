"""This will contain the code that executes the Queens Square Game
   """
import locale
import timeit

from GameState import Game
from Agent import *

if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, 'en_US.utf8')

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

    for game_size in range(4,14):
        
        Test = Game()
        Test.NewGame(game_size)
        NumRuns = 100
        TotalAttempts = 0
        for x in xrange(NumRuns): 
            #RandomAgent(Test)
            HillClimber(Test)
            TotalAttempts +=  Test.GetAttempts()

        print "Game Size:", game_size
        print "Average Attemps:", locale.format("%d", TotalAttempts/NumRuns, grouping=True)
        print 
    
