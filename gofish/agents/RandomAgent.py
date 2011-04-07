import time
import random

import sys
sys.path.append("../")
import timer

from BaseAgent import BaseAgent

class RandomAgent(BaseAgent):
    """
       """
    def __init__(self, name):
        self.name = name

    @timer.timeturn
    def take_turn(self, state):
        """
           """
        num_cards = state.get_number_of_cards(self.name)

        request_from = random.choice(state.get_player_list(self.name))
        request_card = random.choice(state.get_hand(self.name))
        #time.sleep(.5)
        return request_from, request_card

    def give_reward(self, reward):
        """
           """
        pass
