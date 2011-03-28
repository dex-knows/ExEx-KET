from pydispatch import dispatcher 
import random

class State(object):
    """State for Go Fish
    Players: 3-6
    Deck: Standard 52 card
    Goal: Collect the most sets of four.
    Setup: Five cards are dealt to each player. All remaining cards are left face down in a draw pile.
    Gameplay: A random player goes first. On your turn, ask a player for a specific card (e.g. Aces). You must already hold at least one card of the
    requested type.

        If the player you ask has any of that card, they must give all of them to you. If you get one or more cards from the player you ask, you get another
        turn. You may ask any player for any rank you already hold, including the one you just asked for. If the person you ask has no such cards, then you
        draw the top card from the draw pile.

        If you happen to draw a card of the rank asked for, show it to the other players and you get another turn. However, if you draw a card that is not
        the type you asked for, the person you asked takes a turn. You keep the drawn card.

        When you collect a set of four cards of the same type, immediately show the set to the other players and set them down.

    Winning: The game ends when someone has no cards left in their hand or the draw pile runs out. The winner is the player who then has the most sets of
    four.
        """

    def __init__(self):
        self.__setup_pubsub()
        pass # TODO: Setup variables for tracking wins/losses and time to win/loss?

    def __setup_pubsub(self):
        """
           """
        dispatcher.connect(self.get_player_list, "get_player_list")
        dispatcher.connect(self.get_hand, "get_hand")

    def __shuffle_deck(self):
        """
           """
        for i in xrange(5):
            random.shuffle(self.__deck)

    def __setup_players(self, player_list):
        """
           """
        for player in player_list:
            self.__players[player.name] = player
            self.__player_hands[player.name] = []
            self.__player_sets[player.name] = []

    def __get_card_from_deck(self, player_name):
        """
           """
        card = self.__deck.pop()
        self.__player_hands[player_name].append(card)

    def __transfer_card(self, card_requested, request_from, requested_by):
        """
           """
        
        number_given = 0
        for position, card in enumerate(self.__player_hands[request_from]):
            if card == card_requested:
                self.__player_hands[request_from].pop(position)
                self.__player_hands[requested_by].append(card)
                number_given = number_given + 1
                
        #TODO: Dispatch notices of the transfer  (num given and who it was between)  
        print "giving them", number_given
        return number_given

    def __check_for_set(self, card_to_check, player):
        """
           """
        number_found = 0
        card_indexes = []
        for position, card in enumerate(self.__player_hands[player]):
            if card == card_to_check:
                number_found = number_found + 1
                card_indexes.append(position)

        if number_found == 4:
            print "***", player, "made a set of", card_to_check, "'s !"
            self.__player_sets[player].append(card_to_check)
            #TODO: Dispatch notices of the set found (if any)
            card_indexes.reverse() # go in reverse so the indexes don't change as we start to pop things off the list!
            for position in card_indexes:
                self.__player_hands[player].pop(position)    

    def __setup_game(self, players_list):
        """
            """
        print "Setting up game..."
        self.__deck = ('2 3 4 5 6 7 8 9 10 J Q K A '*4).split(' ')
        self.__deck.remove('')
        self.__shuffle_deck()
        self.__players = {} # keys are their handles, val is the player object
        self.__player_hands = {} # same keys as above, val is list of cards held
        self.__player_sets = {}
        self.__setup_players(players_list) 
        
        for i in xrange(5): # Pass out five cards to each player
            for player_name, hand in self.__players.iteritems():
                self.__get_card_from_deck(player_name)
                
        self.print_hands()

    def _empty_hand(self, player_name):
        self.__player_hands[player_name] = []

    def _anyones_hand_empty(self):
        """
           """
        for player_name, hand in self.__player_hands.iteritems():
            if not hand:
                print player_name, "ran out of cards."
                return True
        return False

    def _end_of_play(self):
        """
            """
        return not self.__deck or self._anyones_hand_empty()

    def start_new_game(self, print_intermediate_states, players_list):
        """
            """
        self.__setup_game(players_list)
        next_player = random.choice(self.__player_hands.keys())
        print "First player:", next_player
        while True:
            p = self.__players[next_player]
            request_from, card = p.take_turn(self)
            print next_player, "is asking", request_from, "for", card + "'s...", 
            if card in self.__player_hands[request_from]:
                number_given = self.__transfer_card(card, request_from, next_player)
                self.__check_for_set(card, next_player)
            else:
                print "  Sorry, go fish!"
                # TODO: dispatch that what they requested from whom and the result
                self.__get_card_from_deck(next_player) # go fish (draw from draw pile)
            
            if self._end_of_play():
                self.__handle_game_ending() # gives out final rewards
                break;# todo , return marin of win, who won, and how long everyone took on average (per turn) and margin of loss
                return {'winner': winner, 
                           'players': {'player1': 
                               {'magin-of-loss': 0, # for winner
                                'average-turn-length': 2 # in seconds)
                               }
                            }
                       }
            
            else:
                self.__players[next_player].give_reward(0)
                if print_intermediate_states:
                    self.print_state()
                next_player = request_from 
                continue

    def __handle_game_ending(self):
        print ''
        seperator = '*'.join('+' for i in xrange(20))
        print seperator
        print ' '.join(c for c in "    Game   Over")
        print seperator
        
        players_with_the_most_sets = []
        most_sets = -1
        for player_name, sets in self.__player_sets.iteritems():
            if len(sets) > most_sets:
                players_with_the_most_sets = [player_name]
                most_sets = len(sets)
            elif len(sets) == most_sets:
                players_with_the_most_sets.append(player_name)
                most_sets = len(sets)

        if len(players_with_the_most_sets) > 1:
            print "Tie between:", ', '.join(players_with_the_most_sets),
        else:
            print players_with_the_most_sets[0], "won",
        print "with", most_sets, "sets!"
        print ''

        self.__give_final_rewards(players_with_the_most_sets)
        self.print_state()
            
    def __give_final_rewards(self, winning_players):
        """
           """
        reward = 0

        for player in self.__players.keys():
            if player in winning_players:
                reward = 1
            self.__players[player].give_reward(reward)
                
    def get_hand(self, name):
        """
           """
        return self.__player_hands[name]

    def get_player_list(self, exclude=None):
        """
           """
        return [key for key in self.__player_hands.keys() if key != exclude]
        
    def print_hands(self):
        """
           """
        print "Hands:"
        for player_name, hand in self.__player_hands.iteritems():
            print "  ", player_name + "'s hand ~", ' '.join(hand)
            
    def print_hands_and_sets(self):
        """
           """
        print "Hands and Sets:"
        for player_name, hand in self.__player_hands.iteritems():
            print "  ", player_name + "'s [Hand: ", ' '.join(hand), "]",
            print " [Sets:", ' '.join(self.__player_sets[player_name])  , "]"
        print '' # create a newline

    def print_draw_pile(self):
        """
           """
        print "Draw Pile (", len(self.__deck), "cards ) :", ' '.join(self.__deck)

    def print_state(self):
        self.print_hands_and_sets()
        self.print_draw_pile()
        print '' # Create a newline

