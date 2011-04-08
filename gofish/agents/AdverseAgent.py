import time
import random
import timer

from BaseAgent import BaseAgent

class AdverseAgent(BaseAgent):

    def __init__(self, name):
        self.name = name
        
    @timer.timeturn
    def take_turn(self, state):
        return self._make_choice(state)

    def _make_choice(self, state):
        highest = 0
        highestPlayer, highestCard = '  '
        for requester in self._known_hands:
            for card in self._known_hands[requester]:
                if (self._known_hands[requester][card] > highest) and (card in state.get_hand(self.name)):
                    highest = self._known_hands[requester][card]
                    highestPlayer = requester
                    highestCard = card
        if highestPlayer == ' ' or highestCard == ' ':
            request_from = random.choice(state.get_player_list(self.name))
            request_card = random.choice(state.get_hand(self.name))
            return request_from, request_card
        else:        
            return highestPlayer, highestCard    

    @timer.timereaction
    def trade_notification(self, state, requester, card, requested_from,  number_given):
        if requester != self.name and requested_from != self.name:
            if number_given == 0:
                self._known_hands[requester][card] += 1
            else:
                self._known_hands[requester][card] += number_given
                self._known_hands[requested_from][card] -= number_given
     
    def setup(self, state):
        self._known_hands = {}
        for player in state.get_player_list(self.name):
            self._known_hands[player] = {'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'10':0,'J':0,'Q':0,'K':0,'A':0}