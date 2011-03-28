from state import State

from agents.RandomAgent import RandomAgent

if __name__ == "__main__":
    josh = RandomAgent("josh")
    ryan = RandomAgent("ryan")
    mitch = RandomAgent("mitch")
    helen = RandomAgent("helen")
    
    s = State()
    s.start_new_game(False, [josh,ryan,mitch,helen])
