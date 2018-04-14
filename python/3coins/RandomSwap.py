import random

class RandomSwap():
    def __init__(self,table):
        self.max_tries = 10
        self.table = table
        random.seed()

    def run(self):
        self.tries = 0
        self.table.printState()
        while not self.table.isValid() and self.tries < self.max_tries:
            self.table.swapTwoAdjacent(random.randint(0, self.table.count-2))
            self.table.printState()
            self.tries += 1

    def result(self):
        self.table.printState()
        if self.table.isValid():
            print("Done in "+str(self.tries))
        else:
            print("Failed in "+str(self.tries))
