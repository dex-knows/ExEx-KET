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

def get_board_model(size, default_element):
    """Creates a two-dimensional dictionary using the default element specified 
    which represents the game board.
       """
    model = {}
    for x in xrange(size):
        model[x] = {}
        for y in xrange(size):
            model[x][y] = default_element 

    return model

def place_pieces_randomly(Board):
    """Places the queens randomly (though it does check that no two queens are in the same place) 
    and returns the model of that layout.
       """
    size = Board.GetSize() 
    size_list = range(size)
    model = get_board_model(size, False) # False~ No queen, True~ Queen

    for queen in Board.Queens:
        while True:
            x = random.choice(size_list)
            y = random.choice(size_list)
            if not model[x][y]: # if no queen exists here yet
                model[x][y] = True 
                queen.Position = (x, y)
                break # place the next queen
    return model

def get_heat_map(Board):
    """Returns a board model with each element being an integer from 0+.  Each 
    increment of 1 means that one queen is affecting that element, thus higher 
    counts are worse though one is fine and zero might be a good place to move.
       """

    def mark_row_col_and_diagonals(heat_map, queen):
        """Adds one to each element in the row, column and the appropriate 
        diagaonals.
           """
        queen_x, queen_y = queen.Position
        size = range(Board.GetSize())

        for x in size: # mark the row
            heat_map[x][queen_y] += 1
        for y in size: # mark the column
            heat_map[queen_x][y] += 1

        # mark the positive slope diagonal
        b = queen_y - queen_x 
        for x in size:
            y = x+b  
            try:
                heat_map[x][y] += 1
            except: 
                pass

        # mark the negative slope diagonal
        b = queen_y + queen_x 
        for x in size:
            y = -1*x+b  
            try:
                heat_map[x][y] += 1
            except: 
                pass

    heat_map = get_board_model(Board.GetSize(), 0)
    for queen in Board.Queens:
        mark_row_col_and_diagonals(heat_map, queen)

    return heat_map

def print_heat_map(queen_model, heat_map):
    """Prints a heat map and queen layout to standard output.
       """
    size = range(len(queen_model))
    size_reversed = size[:]
    size_reversed.reverse()
    for y in size_reversed:
        for x in size:
            if queen_model[x][y]:
                print 'x',
            else:
                print heat_map[x][y], 
        print ''

def print_queen_positions(Board):
    """Prints the queen's position, one on each line.
       """
    for count, queen in enumerate(Board.Queens):
        print "Queen", count, "@", queen.Position

