from SwapPolitic import SwapPolitic

class WidthFirst(SwapPolitic):
    def __init__(self,table):
        self.max_depth = 4
        self.table = table
        self.tries = 0

    def run(self):
        if self.oneStep(self.table, 0):
            print ("Valid option found :)");
        else:
            print ("No valid option found :(");

    #can probably be improved by repeating the same action on the same one
    def oneStep(self, table, depth):
        if depth >= self.max_depth:
            return None

        tables = []
        for i in range(0, table.count - 1):
            self.tries += 1
            t = table.copy()
            t.swapTwoAdjacent(i)
            print("d:%d, index:%d"% (depth, i))
            t.printState()
            if t.isValid():
                self.table = t
                return True

            tables.append(t)

        for t in tables:
            if self.oneStep(t, depth+1):
                return True

        return False
