"""This will contain the code that executes the Queens Square Game
   """
import locale
from datetime import datetime

from GameState import Game
import Agent

VERSION = "0.20"

def run_test(agent):
    #locale.setlocale(locale.LC_ALL, 'English_United States')
    locale.setlocale(locale.LC_ALL, 'en_US.utf8')

    print "Starting Queens Square Test Using:", agent , "at", datetime.now()

    for game_size in range(4,14):
        
        Test = Game()
        Test.NewGame(game_size)
        NumRuns = 100
        TotalAttempts = 0
        duration = float(0)
        for x in xrange(NumRuns): 
            duration += getattr(Agent, agent)(Test)

            TotalAttempts +=  Test.GetAttempts()

        print "Game Size:", game_size
        print "Average Attemps:", locale.format("%d", TotalAttempts/NumRuns, grouping=True)
        print "Average Time to Solve:", locale.format("%f", duration/NumRuns, grouping=True), "seconds"
        print
        #raw_input("Hit enter to continue.")
    

if __name__ == "__main__":
    from optparse import OptionParser
    usage = "usage: %prog [options] Algorithm \n"
    usage += '\n'
    usage += "available agents: \n"
    for method in dir(Agent):
        if 'Agent' in method:
            usage += '\n    ' + method

    parser = OptionParser(usage, version="%prog "+VERSION)
    # See default variables at the top of this file 
    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("incorrect number of arguments")
    else:
        agent = args[0]
        run_test(agent)
