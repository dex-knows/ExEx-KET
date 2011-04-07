"""This contains the different agents that can play Queens Square
   """
import random
from copy import deepcopy

from GameState import Game
from GameState import Queen

from Helpful import * 
import timer

@timer.timereaction
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

@timer.timereaction
def SingleGeneticAgent(Board, PopSize=8):
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

@timer.timereaction
def HillClimberAgent(Board):
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

@timer.timereaction
def TrueRandomAgentA(Board):
    while not Board.IsEndState():
        place_pieces_randomly(Board) # moves the queens on Board

@timer.timereaction
def TrueRandomAgentB(Board):
    while not Board.IsEndState():
        place_pieces_randomly_one_to_a_row(Board)

@timer.timereaction
def TrueRandomAgentC(Board):
    while not Board.IsEndState():
        place_pieces_randomly_one_to_a_row_and_column(Board)
