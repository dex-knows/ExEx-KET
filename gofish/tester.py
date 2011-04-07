from state import State

from agents.RandomAgent import RandomAgent

if __name__ == "__main__":
    josh = RandomAgent("josh")
    ryan = RandomAgent("ryan")
    mitch = RandomAgent("mitch")
    helen = RandomAgent("helen")
    
    s = State()
    player_loss_margin = s.start_new_game(False, False, False, False, [josh,ryan,mitch,helen])
    for player_name, loss_margin in player_loss_margin.iteritems():
        print player_name, "lost by", loss_margin
