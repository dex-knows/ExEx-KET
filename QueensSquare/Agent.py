"""This contains the different agents that can play Queens Square
   """
import random
from copy import deepcopy

from GameState import Game
from Helpful import * 
import timeit

@timeit.timereaction
def RandomAgent(Board):
    """An agent that will try to randomly place the queens to win."""
    a = 0
    for ThisQueen in Board.Queens:
        ThisQueen.Position = (a, a)
        a = a + 1
    RowGen = random.random
    while (Board.IsEndState() == False):
        Rows = range(Board.GetSize())
        for ThisQueen in Board.Queens:
            ThisRow = int(RowGen() * len(Rows))
            ThisQueen.Position = (ThisQueen.Position[0], Rows[ThisRow])
            del Rows[ThisRow]

def GetFitness(Board):
    """Calculates the fitness of the current layout"""
    
    pass

def FitnessGoal(Size):
    """Returns the goal fitness based on the size of the game"""
    #formulate based on combination Size choose 2.
    #perfect fitness is one in which all pairs of queens don't attack
    return (Size * (Size -1))/2  

@timeit.timereaction
def HillClimber(Board):
    """An agent that tries moving one piece at a time to win.  It will start over if
    it ever reaches diminishing returns.
       """
    def get_layout_score(Board):
        """Gives a general "fitness" score for the current layout and an updated heat map.
           """
        heat_map = get_heat_map(Board)
        score = 0
        for queen in Board.Queens:
            x,y = queen.Position
            score += heat_map[x][y]
        return score

    def map_moves(board):
        """Maps all possible single moves to their resulting scores.
           """
        moves = {} # key: ((x),(orig_y, new_y)) val: (score)
        size = board.GetSize()
        for i in xrange(size):
            board_copy = deepcopy(board)
            queen = board_copy.Queens[i]
            x, current_y = queen.Position
            for new_y in xrange(size):
                if new_y != current_y:
                    queen.Position = (x,new_y) # only moves it on the board copy!
                    score = get_layout_score(board_copy)
                    try:
                        moves[score].append(((x),(current_y,new_y)))
                    except:
                        moves[score] = [((x),(current_y,new_y))]
        return moves

    def move_queen(board, move):
        x = move[0]
        old_y, new_y = move[1]

        for queen in board.Queens:
            qX, qY = queen.Position
            if qX == x and qY == old_y:
                queen.Position = (x,new_y)
                break

    def start_over(Board):
        #place_pieces_randomly(Board) # moves the queens on Board
        #place_pieces_randomly_one_to_a_row(Board)
        place_pieces_randomly_one_to_a_row_and_column(Board)

    start_over(Board)
    old_score = None 

    while not Board.IsEndState():
        new_score = get_layout_score(Board)

        if not old_score or new_score < old_score:
            moves = map_moves(Board)
            best_move = min(moves)
            if best_move < new_score:
                #print "Best move results in a score of:", best_move, "Old Score:", new_score, "Move(s):", moves[best_move]
                move_to_take = random.choice(moves[best_move])
                move_queen(Board, move_to_take)
                old_score = new_score
            else:
                start_over(Board)
                old_score = None
        else:
            start_over(Board)
            old_score = None

@timeit.timereaction
def TrueRandomAgentA(Board):
    while not Board.IsEndState():
        place_pieces_randomly(Board) # moves the queens on Board

@timeit.timereaction
def TrueRandomAgentB(Board):
    while not Board.IsEndState():
        place_pieces_randomly_one_to_a_row(Board)

@timeit.timereaction
def TrueRandomAgentC(Board):
    while not Board.IsEndState():
        place_pieces_randomly_one_to_a_row_and_column(Board)
