#!/usr/bin/python

from helpers import Coin, Table

import random

COINS_COUNT=3
MAX_TRY=10

table = Table(COINS_COUNT)

random.seed()

tries = 0
table.printState()
while not table.isValid() and tries < MAX_TRY:
    table.swapTwoAdjacent(random.randint(0, COINS_COUNT-2))
    table.printState()

    tries+=1

print("Done in "+str(tries))
