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
        pass # TODO: Setup variables for tracking wins/losses and time to win/loss?

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
            self.__player_time_taken[player.name] = 0
            self.__player_turns_taken[player.name] = 0

        for player in player_list:
            player.setup(self)

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
        return number_given

    def __check_for_set(self, card_to_check, player):
        """Returns true when a set is made, and false when none is made.
           """
        set_made = False
        number_found = 0
        card_indexes = []
        for position, card in enumerate(self.__player_hands[player]):
            if card == card_to_check:
                number_found = number_found + 1
                card_indexes.append(position)

        if number_found == 4:
            set_made = True
            self.__player_sets[player].append(card_to_check)
            #TODO: Dispatch notices of the set found (if any)
            card_indexes.reverse() # go in reverse so the indexes don't change as we start to pop things off the list!
            for position in card_indexes:
                self.__player_hands[player].pop(position)    

        return set_made, card_to_check

    def __setup_game(self, players_list):
        """
            """
        self.__deck = ('2 3 4 5 6 7 8 9 10 J Q K A '*4).split(' ')
        self.__deck.remove('')
        self.__shuffle_deck()
        self.__players = {} # keys are their handles, val is the player object
        self.__player_hands = {} # same keys as above, val is list of cards held
        self.__player_sets = {}
        self.__player_time_taken = {}
        self.__player_turns_taken = {}
        self.__setup_players(players_list) 
        
        for i in xrange(5): # Pass out five cards to each player
            for player_name, hand in self.__players.iteritems():
                self.__get_card_from_deck(player_name)

    def _empty_hand(self, player_name):
        self.__player_hands[player_name] = []

    def _anyones_hand_empty(self):
        """
           """
        for player_name, hand in self.__player_hands.iteritems():
            if not hand:
                #print player_name, "ran out of cards."
                return True
        return False 

    def _end_of_play(self):
        """
            """
        return not self.__deck or self._anyones_hand_empty()

    def start_new_game(self, print_start_state, print_intermediate_states, print_trades, print_end_state, players_list):
        """
            """
        self.__setup_game(players_list)
        next_player = random.choice(self.__player_hands.keys())
        if print_start_state:
            self.print_hands()
            print "First player:", next_player

        while True:
            number_given = 0 
            set_made = False

            p = self.__players[next_player]
            (request_from, card), duration = p.take_turn(self)
            self.__player_time_taken[next_player] += duration
            self.__player_turns_taken[next_player] += 1

            if print_trades:
                print next_player, "is asking", request_from, "for", card + "'s...", 

            if card in self.__player_hands[request_from]:
                number_given = self.__transfer_card(card, request_from, next_player)
                if print_trades:
                    print "giving them", number_given
                set_made, set_of = self.__check_for_set(card, next_player)
                if print_trades:
                    print "***", next_player, "made a set of", set_of, "'s !"

            else:
                if print_trades:
                    print "  Sorry, go fish!"
                # TODO: dispatch that what they requested from whom and the result
                self.__get_card_from_deck(next_player) # go fish (draw from draw pile)

            for player_name, player_object in self.__players.iteritems():
                duration = player_object.trade_notification(self, next_player, card, request_from, number_given)

                if set_made:
                    duration += player_object.set_notification(self, next_player, card)

                self.__player_time_taken[next_player] += duration
            
            if self._end_of_play():
                winners, most_sets = self.__get_winners() # gives out final rewards
                self.__give_final_rewards(winners)
                if print_end_state:
                    self.__print_results(winners, most_sets)
                return self.__get_margin_of_loss(most_sets)
            
            else:
                self.__players[next_player].give_reward(0)
                if print_intermediate_states:
                    self.print_state()
                next_player = request_from 
                continue

    def __get_winners(self):
        """
           """
        winners = []
        most_sets = -1
        for player_name, sets in self.__player_sets.iteritems():
            if len(sets) > most_sets:
                winners = [player_name]
                most_sets = len(sets)
            elif len(sets) == most_sets:
                winners.append(player_name)
                most_sets = len(sets)
        return winners, most_sets

    def __get_margin_of_loss(self, most_sets):
        """
           """
        margin_of_loss = {}
        for player_name, sets in self.__player_sets.iteritems():
            margin_of_loss[player_name] = most_sets - len(sets)
        return margin_of_loss

    def __print_results(self, winners, most_sets):
        """
           """
        seperator = '*'.join('+' for i in xrange(20))
        print ''
        print seperator
        print ' '.join(c for c in "    Game   Over")
        print seperator

        if len(winners) > 1:
            print "Tie between:", ', '.join(winners),
        else:
            print winners[0], "won",
        print "with", most_sets, "sets!"
        print ''

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

    def get_number_of_cards(self, name):
        """
           """
        return len(self.__player_hands[name])

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
        self.print_time_taken()
        print '' # Create a newline

    def print_time_taken(self):
        for player_name, time_taken in self.__player_time_taken.iteritems():
            avg_turn  = time_taken/self.__player_turns_taken[player_name]
            print player_name, "took an average of %d.3 seconds per turn" % avg_turn

