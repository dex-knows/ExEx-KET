"""This contains the different agents that can play Queens Square
   """
import random

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
    def get_layout_score(Board, heat_map):
        """Gives a general "fitness" score for the current layout and an updated heat map.
           """
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

    def change_queen_position(Board, queen_model, queen, new_position):
        """Moves the queen and updates the board and model as necessary.
           """
        old_x, old_y = queen.Position
        new_x, new_y = new_position
        queen_model[old_x][old_y] = False
        queen_model[new_x][new_y] = True 
        queen.Position = new_position

    queen_model = place_pieces_randomly(Board) # moves the queens on Board
    old_score = None 

    while not Board.IsEndState():
        heat_map = get_heat_map(Board)
        #print_queen_positions(Board)
        #print_heat_map(queen_model, heat_map)
        new_score = get_layout_score(Board, heat_map)

        if not old_score or new_score < old_score:
            queen = get_hottest_queen(Board, heat_map)
            new_position = get_lowest_temp_square(queen_model, heat_map, queen.Position) 
            change_queen_position(Board, queen_model, queen, new_position)
            old_score = new_score

        else:
            queen_model = place_pieces_randomly(Board) # moves the queens on Board
            old_score = None
            
    
