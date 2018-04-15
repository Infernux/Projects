#!/usr/bin/python

from helpers import Coin, Table

from RandomSwap import RandomSwap
from DepthFirst import DepthFirst
from WidthFirst import WidthFirst
from DFOpenedClosedLists import DFOpenedClosedLists
from WFOpenedClosedLists import WFOpenedClosedLists

COINS_COUNT=3

table = Table(COINS_COUNT)

#swap_politic = RandomSwap(table)
#swap_politic = WidthFirst(table)
#swap_politic = DepthFirst(table)
#swap_politic = DFOpenedClosedLists(table)
swap_politic = WFOpenedClosedLists(table)

swap_politic.run()
swap_politic.result()
