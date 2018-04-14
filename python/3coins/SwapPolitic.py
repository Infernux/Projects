class SwapPolitic(object):
    def result(self):
        self.table.printState()
        if self.table.isValid():
            print("Done in "+str(self.tries))
        else:
            print("Failed in "+str(self.tries))
