class Coin:
    def __init__(self, state):
        self.state = state

    def getState(self):
        return "up" if self.state else "down"
        #return "表" if self.state else "裏"

    def swapState(self):
        self.state = not self.state

    def setState(self, newState):
        self.state = newState

class Table:
    def __init__(self, count):
        self.count = count
        #could completely randomise
        self.table = []
        for i in range(0,count):
            if i % 2:
                self.table.append(Coin(True))
            else:
                self.table.append(Coin(False))

    def swapTwoAdjacent(self, index):
        if index >= self.count-1:
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

    def copy(self):
        t = Table(self.count)
        i=0
        for c in self.table:
            t.table[i].setState(c.state)
            i=i+1

        return t
