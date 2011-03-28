import random

class RandomAgent(object):
    """
       """
    def __init__(self, name):
        self.name = name

    def take_turn(self, state):
        """
           """
        request_from = random.choice(state.get_player_list(self.name))
        request_card = random.choice(state.get_hand(self.name))
        return request_from, request_card

    def give_reward(self, reward):
        """
           """
        pass
