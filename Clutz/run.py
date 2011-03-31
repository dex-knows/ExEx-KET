from GameState import GameState
from Agent import Agent

test = GameState("map.txt", -0.04, .2, .8, False, 0)
agent = Agent(test, "policy.txt")

while not test.isEndOfGame():
    agent.move()
    print(test.getReward())
    input("Pause")
  
print(test.getWinLoc())
print(test.getLoseLoc())
print(test.getReward())

input("Hit enter to quit")