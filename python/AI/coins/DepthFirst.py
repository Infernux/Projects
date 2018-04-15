#another idea is, instead of creating copies of the table
#create lists of actions to take
#and repeat them on a clean table everytime, without modifying it

from SwapPolitic import SwapPolitic

class DepthFirst(SwapPolitic):
    def __init__(self,table):
        self.max_depth = 4
        self.table = table
        self.tries = 0

    def run(self):
        ret = None
        for i in range(0, self.table.count - 1):
            ret = self.oneStep(self.table, i, 0)
            if ret:
                self.table = ret

        return None

    def oneStep(self, table, indexToSwap, depth):
        self.tries += 1
        if depth >= self.max_depth:
            return None

        table = table.copy()

        table.swapTwoAdjacent(indexToSwap)

        print("d:%d, index:%d"% (depth, indexToSwap))
        table.printState()

        if table.isValid():
            return table

        ret = None
        for i in range(0, table.count - 1):
            ret = self.oneStep(table, i, depth+1)
            if ret:
                return ret

        return None
