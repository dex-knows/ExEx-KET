"""This will contain the code that executes the Queens Square Game
   """
import locale

from GameState import Game
from Agent import *

if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, 'en_US.utf8')

    for game_size in range(20,25):
        
        Test = Game()
        Test.NewGame(game_size)
        NumRuns = 10
        TotalAttempts = 0
        for x in xrange(NumRuns): 
            #RandomAgent(Test)
            #HillClimber(Test)
            SingleGenetic(Test, x + 2)
            TotalAttempts +=  Test.GetAttempts()

        print "Game Size:", game_size
        print "Average Attemps:", locale.format("%d", TotalAttempts/NumRuns, grouping=True)
        print 
    
