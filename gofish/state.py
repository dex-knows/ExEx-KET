import random

class State(object):
    """State for Go Fish
    
    Players: 3-6
    Deck: Standard 52 card
    Goal: Collect the most sets of four.
    Setup: Five cards are dealt to each player. All remaining cards are left face down in a draw pile.
    Gameplay: A random player goes first. On your turn, ask a player for a specific card (e.g. Aces).  You must already hold at least one card of the
    requested type.  

    If the player you ask has any of that card, they must give all of them to you.  If you get one or more cards from the player you ask, you get another
    turn.  You may ask any player for any rank you already hold, including the one you just asked for. If the person you ask has no such cards, then you
    draw the top card from the draw pile.  

    If you happen to draw a card of the rank asked for, show it to the other players and you get another turn.  However, if you draw a card that is not
    the type you asked for, the person you asked takes a turn.  You keep the drawn card. 

    When you collect a set of four cards of the same type, immediately show the set to the other players and set them down.

    Winning:  The game ends when someone has no cards left in their hand or the draw pile runs out.  The winner is the player who then has the most sets of
    four.
        """

    def __init__(self):
        self.__deck = ('2 3 4 5 6 7 8 9 10 J Q K A '*4).split(' ')
        self.__deck.remove('')
        random.shuffle(self.__deck)
        self.__players = {} # keys are their handles, val is the player object
        self.__player_hands = {} # same keys as above, val is list of cards held

    def _end_of_play(self):
        """
           """
        return self.__deck # TODO: or if any of the players have an empty hand

    def _setup_game(self):
        """
           """
        pass

    def start_new_game(self):
        """
           """
        self._setup_game()
        for player_name, player_object in self.__players.iteritems():
            player_object.take_turn(self)

