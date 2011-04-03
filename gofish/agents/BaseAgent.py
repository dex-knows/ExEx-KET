
import timeit

class BaseAgent(object):
    """Defines three key methods which should be overridden by a sub-class.  At a minimum, 
    you should override take_turn. For all overridden methods, be sure to use appropriate 
    timeit decorator. 
       """
    def __init__(self, name):
        self.name = name

    @timeit.timeturn
    def take_turn(self, state):
        """This returns whom the agent wants to request a card from and what card (both strings).
           """

        request_from = random.choice(state.get_player_list(self.name))
        request_card = random.choice(state.get_hand(self.name))
        return request_from, request_card

    @timeit.timereaction
    def trade_notification(self, state, requester, card, requested_from, number_given, set_made):
        """A notification from the state, which gives who requested the card, the card requested,
        who it was requested from, how many were given and if that trade resulted in a set.


        state ~ the state object
        requester ~ string
        card ~ string
        requested_from ~ string
        number_given ~ int
        set_made ~ boolean 
           """
        #print self.name, "got a trade notification:", requester, "requested", card + "'s from", 
        #print requested_from, "and received", number_given,
        #if set_made:
        #    print "resulting in a set!"
        #else:
        #    print '' # create a new line

        pass

    @timeit.timereaction
    def give_reward(self, reward):
        """
           """
        pass
