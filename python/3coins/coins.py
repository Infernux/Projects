#!/usr/bin/python

from helpers import Coin, Table

from RandomSwap import RandomSwap
from DepthFirst import DepthFirst

COINS_COUNT=3

table = Table(COINS_COUNT)

#swap_politic = RandomSwap(table)
swap_politic = DepthFirst(table)

swap_politic.run()
swap_politic.result()
