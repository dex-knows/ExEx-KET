"""Contains useful functions
   """
import random

def Slope(PosA, PosB):
    """Calculates the slope between two points"""
    if PosA[0] == PosB[0]:
        #The points are vertically aligned
        return 0;
    else:
        return (float(PosA[1]) -\
                float(PosB[1])) /\
               (float(PosA[0]) -\
                float(PosB[0]))

def get_board_model(size):
    """Creates a two-dimensional dictionary of True/False values which represents the game board.

    False means that there is no queen there, and True means that there is.
       """
    model = {}
    for row in xrange(size):
        model[row] = {}
        for col in xrange(size):
            model[row][col] = False 
    return model

def place_pieces_randomly(Board):
    size = Board.GetSize() 
    size_list = range(size)
    model = get_board_model(size)

    for queen in Board.Queens:
        while True:
            row = random.choice(size_list)
            col = random.choice(size_list)
            if not model[row][col]: # if no queen exists here yet
                model[row][col] = True 
                queen.Position = (row, col)
                break # place the next queen




