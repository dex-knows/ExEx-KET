from state import State

from agents.RandomAgent import RandomAgent

def run_game():
    josh = RandomAgent("josh")
    ryan = RandomAgent("ryan")
    mitch = RandomAgent("mitch")
    helen = RandomAgent("helen")

    s = State()
    player_loss_margin = s.start_new_game(False, False, False, False, [josh,ryan,mitch,helen])
    return player_loss_margin


if __name__ == "__main__":
    number_of_games = 0
    total_loss_margins = {} 

    for c in xrange(1000):
        results = run_game()
        number_of_games += 1

        for player_name, loss_margin in results.iteritems():
            try:
                total_loss_margins[player_name] += loss_margin
            except:
                total_loss_margins[player_name] = loss_margin
                

    for player_name, loss_margin in total_loss_margins.iteritems():
        print player_name, "lost by", float(loss_margin)/float(number_of_games), "on average"
    
