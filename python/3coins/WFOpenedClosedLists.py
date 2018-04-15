from SwapPolitic import SwapPolitic

from queue import Queue

class WFOpenedClosedLists(SwapPolitic):
    def __init__(self, table):
        self.max_depth = 3
        self.table = table
        self.tries = 0

        self.openedList = Queue()
        self.closedList = []

        self.openedList.put((table, 0))

    def run(self):
        while self.openedList.qsize() != 0:
            (table, depth) = self.openedList.get()
            table.printState()
            if depth >= self.max_depth:
                continue

            self.tries += 1

            if table.isValid():
                self.table = table
                return

            ret = None
            for i in range(0, table.count - 1):
                tt = table.copy()
                tt.swapTwoAdjacent(i)
                self.openedList.put((tt, depth+1))

            self.closedList.append((table, depth))
