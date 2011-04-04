"""This contains the different agents that can play Queens Square
   """
import random

from GameState import Game
from GameState import Queen
from Helpful import * 

def RandomAgent(Board):
    """An agent that will try to randomly place the queens to win."""
    Rows = range(Board.GetSize())
    a = 0
    for ThisQueen in Board.Queens:
        ThisQueen.Position = (a, assign_random(Rows))
        a = a + 1
    while (Board.IsEndState() == False):
        Rows = range(Board.GetSize())
        assign_positions(Board.Queens, Rows)

def assign_positions(Queens, Rows):
    """Randomly assigns positions to Queens"""
    for ThisQueen in Queens:
        ThisQueen.Position = (ThisQueen.Position[0], assign_random(Rows))

def assign_random(Items):
    """Randomly returns an item from the list of items and removes it from the lise"""
    ItemIndex = int(random.random() * len(Items))
    Item = Items[ItemIndex]
    del Items[ItemIndex]
    return Item    

def GetFitness(Queens):
    """Calculates the fitness of the current layout"""
    Fitness = 0
    for QueenA in xrange(len(Queens)):
        for QueenB in xrange(QueenA + 1, len(Queens)):
            slope = Slope(Queens[QueenA].Position,\
                          Queens[QueenB].Position)
            #Checks to see if Queens are on diagonally, horizontally
            # or vertically aligned.
            if (slope != -1) and (slope != 1) and (slope != 0):
                Fitness = Fitness + 1
    return Fitness

def FitnessGoal(Size):
    """Returns the goal fitness based on the size of the game"""
    #formula based on combination Size choose 2.
    #perfect fitness is one in which all pairs of queens don't attack
    return (Size * (Size -1))/2  

def SingleGenetic(Board, PopSize):
    """Genetic algorithm with an 'asexual' approach using the specified population size"""
    Populations = []
    #Controls how big of a population there should be.
    for ThisPop in xrange(PopSize):
        Queens = []
        Rows = range(Board.GetSize())
        #Creates queens for each population.
        for a in xrange(Board.GetSize()):
            Queens[a:] = [Queen((a, assign_random(Rows)))]
        Populations[ThisPop:] = [Queens]
    
    GoalFit = FitnessGoal(Board.GetSize())
    BestFit = 0

    while (BestFit != GoalFit):
        BestFit = 0
        ThisFit = 0
        NextGen = []
        for ThisPop in xrange(len(Populations)):
            #Collect fitness info on the global populations.
            ThisFit = GetFitness(Populations[ThisPop])
            #If the fitness matches the goal fitness check to see if it is the end state.
            if ThisFit == GoalFit:
               for ThisQueen in xrange(len(Board.Queens)):
                   Board.Queens[ThisQueen].Position = \
                                   Populations[ThisPop][ThisQueen].Position
               if Board.IsEndState():
                  BestFit = GoalFit
            #Check to see if there is a new best population and reset the next generation.
            if ThisFit > BestFit:
                BestFit = ThisFit
                NextGen = []
            #Adds any best populations to the potential next generation.
            if ThisFit == BestFit:
               NextGen.append(Populations[ThisPop])
    
        #Randomly select one of the best Populations to create the next generation with.
        Seed = assign_random(NextGen)

        Populations = []
        NewPop = []
        
        #Create as many new populations as there were previously.
        for ThisPop in xrange(PopSize):
            #The new populations will be a mutation/premutation of the seed, such that
            #two of the columns row positions will be flip flopped.
            #this will preserve the one row, one column, one queen setup while allowing
            #for 'random' mutation.
            Cols = range(Board.GetSize())
            MutColA = assign_random(Cols) 
            MutColB = assign_random(Cols)    
            #Copy the seed into a new population.        
            for a in xrange(len(Seed)):
                NewPop[len(NewPop):] = [Queen(Seed[a].Position)]
            #preform the mutation.
            Temp = NewPop[MutColA].Position[1]
            NewPop[MutColA].Position = (MutColA, NewPop[MutColB].Position[1])
            NewPop[MutColB].Position = (MutColB, Temp)
            #add the new population to the global population.
            Populations[len(Populations):] = [NewPop]
            NewPop = []
        Board.IsEndState()

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

    queen_model = place_pieces_randomly(Board) # moves the queens on Board
    strikes = None
    reset_strikes(strikes, queen_model) 
    old_score = None 
    strikes = 0 

    while not Board.IsEndState():
        heat_map = get_heat_map(Board)
        #print_queen_positions(Board)
        #print_heat_map(queen_model, heat_map)
        new_score = get_layout_score(Board, heat_map)

        if not old_score or new_score < old_score:
            reset_strikes(strikes, queen_model) # made an improvement, reset
            queen = get_hottest_queen(Board, heat_map)
            new_position = get_lowest_temp_square(queen_model, heat_map, queen.Position) 
            #new_position = get_random_position(queen_model)
            change_queen_position(Board, queen_model, queen, new_position)
            old_score = new_score

        else:
            if strikes > 0:
                strikes -= 1
            else:
                queen_model = place_pieces_randomly(Board) # moves the queens on Board
                reset_strikes(strikes, queen_model)
                old_score = None
