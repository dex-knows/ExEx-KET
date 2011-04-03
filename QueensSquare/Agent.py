"""This contains the different agents that can play Queens Square
   """
import random
from copy import deepcopy

from GameState import Game
from Helpful import * 

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

    def get_hottest_queen(Board, heat_map):
        """Returns the position or the queen under the hottest square.

        If there is a tie, it randomly chooses one.
           """
        highest_score = 0
        hottest_queens = []
        for queen in Board.Queens:
            x,y = queen.Position
            score = heat_map[x][y]

            if score > highest_score:
                hottest_queens = [queen]
            elif score == highest_score:
                hottest_queens.append(queen)

        return random.choice(hottest_queens)

    def get_lowest_temp_square(queen_model, heat_map, preferred_position):
        """Returns the lowest temperature square on the board.

        If there is a tie, it prefers one in the same row or column 
        as the preferred position passed in.
           """
        lowest_score = 100000000  
        lowest_temp_squares = []
        for x in heat_map:
            for y in heat_map[x]:
                if not queen_model[x][y]: # skip squares already occupied
                    score = heat_map[x][y]
                    if score < lowest_score:
                        lowest_temp_squares = [(x,y)]
                        lowest_score = score
                    elif score == lowest_score:
                        lowest_temp_squares.append((x,y))

        if len(lowest_temp_squares) > 1:
            for position in lowest_temp_squares:
                x,y = position
                if x == preferred_position[0] or \
                   y == preferred_position[0]:  
                    return position
            # else... return a random one...
            return random.choice(lowest_temp_squares)
        else:
            return lowest_temp_squares[0]

    def get_random_position(queen_model):
        while True:
            x = random.choice(range(len(queen_model)))
            y = random.choice(range(len(queen_model)))
            if not queen_model[x][y]:
                return (x,y)

    def change_queen_position(Board, queen_model, queen, new_position):
        """Moves the queen and updates the board and model as necessary.
           """
        old_x, old_y = queen.Position
        new_x, new_y = new_position
        queen_model[old_x][old_y] = False
        queen_model[new_x][new_y] = True 
        queen.Position = new_position

    def reset_strikes(strikes, queen_model):
        strikes = len(queen_model)*2
        #strikes = len(queen_model)^len(queen_model)

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

    

    place_pieces_randomly(Board) # moves the queens on Board
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
                place_pieces_randomly(Board) # moves the queens on Board
                old_score = None
        else:
            place_pieces_randomly(Board) # moves the queens on Board
            old_score = None
            
    
