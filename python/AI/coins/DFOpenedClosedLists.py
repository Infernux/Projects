from SwapPolitic import SwapPolitic

class DFOpenedClosedLists(SwapPolitic):
    def __init__(self, table):
        self.max_depth = 3
        self.table = table
        self.tries = 0

        self.openedList = []
        self.closedList = []

        self.openedList.append((table, 0))

    def run(self):
        while len(self.openedList) != 0:
            (table, depth) = self.openedList.pop()
            if depth >= self.max_depth:
                continue

            self.tries += 1

            if table.isValid():
                self.table = table
                return

            ret = None
            tmp = []
            for i in range(0, table.count - 1):
                tt = table.copy()
                tt.swapTwoAdjacent(i)
                tmp.append((tt,depth+1))

            tmp.reverse() #yewwww
            self.openedList += tmp
            self.closedList.append((table, depth))
