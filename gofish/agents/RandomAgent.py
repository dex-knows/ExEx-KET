import time
import random
import timeit

from BaseAgent import BaseAgent

class RandomAgent(BaseAgent):
    """
       """
    def __init__(self, name):
        self.name = name

    @timeit.timeturn
    def take_turn(self, state):
        """
           """
        request_from = random.choice(state.get_player_list(self.name))
        request_card = random.choice(state.get_hand(self.name))
        time.sleep(.5)
        return request_from, request_card

    def give_reward(self, reward):
        """
           """
        pass
