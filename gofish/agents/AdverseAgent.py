import time
import random
import timer

from BaseAgent import BaseAgent

__all__ = ['AdverseAgent']

class AdverseAgent(BaseAgent):

    def __init__(self, name):
	print "In subclass"
        self.name = name
        
    @timer.timeturn
    def take_turn(self, state):
        return self._make_choice(self, state)

    def _make_choice(self, state):
        highest = 0
        highestPlayer, highestCard = ""
        print "\n", self._known_hands, "\n"
        for requester in self._known_hands:
            for card in self._known_hands[requester]:
                if (self._known_hands[card] > highest) and (card in state.get_hand(self.name)):
                    highest = self._known_hands[card]
                    highestPlayer = requester
                    highestCard = card
        print "\n", highestPlayer, highestCard, "\n"
        return highestPlayer, highestCard
        

    @timer.timereaction
    def trade_notification(self, state, requester, card, requested_from,  number_given):
        if number_given == 0:
            self._known_hands[requester][card] += 1
        else:
            self._known_hands[requester][card] += number_given
            self._known_hands[requested_from][card] -= number_given
     
    def setup(self, state):
        self._known_hands = {}
        for player in state.get_player_list(self.name):
            self._known_hands[player] = {2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,J:0,Q:0,K:0,A:0}
