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

class Table:
    def __init__(self):
        #could completely randomise
        self.table = []
        for i in range(0,COINS_COUNT):
            if i % 2:
                self.table.append(Coin(True))
            else:
                self.table.append(Coin(False))

    def swapTwoAdjacent(self, index):
        if index >= COINS_COUNT-1:
            raise Exception

        self.table[index].swapState()
        self.table[index+1].swapState()

    def isValid(self):
        prevState = self.table[0].getState() #fails if 0 coins
        for c in self.table:
            if c.getState() != prevState:
                return False

        return True

    def printState(self):
        print('------')
        for c in self.table:
            print(c.getState())
        print('------')

table = Table()

random.seed()

tries = 0
table.printState()
while not table.isValid() and tries < MAX_TRY:
    table.swapTwoAdjacent(random.randint(0, COINS_COUNT-2))
    table.printState()

    tries+=1

print("Done in "+str(tries))
