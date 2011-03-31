#This contains the different agents that can play Queens Square

from GameState import Game
import random



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
