from state import State

from agents import *

VERSION = ".10"

def run_game(agent):
    #josh = getattr(agents, agent)("agent")
    josh = RandomAgent("AdverseAgent")
    ryan = RandomAgent("ryan")
    mitch = RandomAgent("mitch")
    helen = RandomAgent("helen")

    s = State()
    player_loss_margin = s.start_new_game(False, False, False, False, [josh,ryan,mitch,helen])
    return player_loss_margin

def run_test(agent, iterations):
    number_of_games = 0
    total_loss_margins = {} 

    for c in xrange(iterations):
        results = run_game(agent)
        number_of_games += 1

        for player_name, loss_margin in results.iteritems():
            try:
                total_loss_margins[player_name] += loss_margin
            except:
                total_loss_margins[player_name] = loss_margin
                

    for player_name, loss_margin in total_loss_margins.iteritems():
        print player_name, "lost by", float(loss_margin)/float(number_of_games), "on average"
 

if __name__ == "__main__":
    import os
    from optparse import OptionParser
    usage = "usage: %prog [options] agent \n"
    usage += '\n'
    usage += "available agents: "
    for method in os.listdir("agents"):
        if 'Agent' in method:
            usage += '\n    ' + method.replace('.py','')

    parser = OptionParser(usage, version="%prog "+VERSION)
    parser.add_option("-i", "--iterations", dest="iterations", help="how many games to run for the test", default=1000)
    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("incorrect number of arguments")
    else:
        agent = args[0]
        run_test(agent, options.iterations)


