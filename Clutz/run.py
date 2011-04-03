from GameState import GameState
from Agent import Agent

test = GameState("map.txt", -0.04, .2, .8, False, 0)
agent = Agent(test, "policy.txt")

avgReward = 0

for x in range(1000):
    print("Playing game ", x+1)
    while not test.isEndOfGame():
        agent.move()
    print(test.getReward())
    avgReward += test.getReward()
    test.restart()
    
print(avgReward/1000)

input("Hit enter to quit")