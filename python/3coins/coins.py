#!/usr/bin/python

import random

COINS_COUNT=5
MAX_TRY=100

class Coin:
    def __init__(self, state):
        self.state = state

    def getState(self):
        return "up" if self.state else "down"
        #return "表" if self.state else "裏"

    def swapState(self):
        self.state = not self.state

def swapTwoAdjacent(table, index):
    if index >= COINS_COUNT-1:
        raise Exception

    table[index].swapState()
    table[index+1].swapState()

def isValid(table):
    prevState = table[0].getState() #fails if 0 coins
    for c in table:
        if c.getState() != prevState:
            return False

    return True

def printState(table):
    print('------')
    for c in table:
        print(c.getState())
    print('------')

table = []
for i in range(0,COINS_COUNT):
    if i % 2:
        table.append(Coin(True))
    else:
        table.append(Coin(False))

random.seed()

tries = 0
printState(table)
while not isValid(table) and tries < MAX_TRY:
    swapTwoAdjacent(table, random.randint(0, COINS_COUNT-2))
    printState(table)

    tries+=1

print("Done in "+str(tries))
