#!/usr/bin/python

from helpers import Coin, Table

from RandomSwap import RandomSwap

COINS_COUNT=3

table = Table(COINS_COUNT)
swap_politic = RandomSwap(table)
swap_politic.run()
swap_politic.result()
