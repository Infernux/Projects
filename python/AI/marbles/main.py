#!/usr/bin/python3

class Pile():
    def __init__(self, index, total):
        self.index = index
        self.count = total

    def take(self, count):
        if(count > self.count):
            raise Exception

        self.count -= count

    def put(self, count):
        self.count += count

class Board():
    def __init__(self):
        self.piles = []
        self.piles.append(Pile(0, 1))
        self.piles.append(Pile(1, 3))

    def isEmpty(self):
        for pile in self.piles:
            if pile.count != 0:
                return False

        return True

    def play(self, pile, count):
        self.piles[pile].take(count)

    def printState(self):
        print("(%d)    (%d)" % (self.piles[0].count, self.piles[1].count))

class AlphaBeta():
    def play(self, board):
        pile = 0
        count = 0

        #winning, (pile, count) = self.step(board, True, None)
        res = self.enumerateCases(board, True)

        for c in res:
            if c[0] == True:
                return c

        raise Exception("Can't win")

    def stoppingCondition(self, board, aiTurn, play):
        #if the board is empty, the current player lost
        #if it is us :(, if it is the opponent :)
        if board.isEmpty():
            return not aiTurn, play
        return None

    def enumerateCases(self, board, aiTurn):
        cases = []
        for p in board.piles:
            for c in range(1, p.count+1): #HAVE TO take at least one, can't take more than total
                p.take(c)
                cases.append(self.step(board, not aiTurn, (p.index, c)))
                p.put(c)

        return cases

    def decide(self, cases, aiTurn):
        if aiTurn: #any winning solution if good for us
            for c in cases:
                if c[0] == True:
                    return True
            return False
        else: #any winning solution is bad for us
            for c in cases:
                if c[0] == False:
                    return False
            return True

    def step(self, board, aiTurn, play):
        res = self.stoppingCondition(board, aiTurn, play)
        if res != None:
            return res

        res = self.enumerateCases(board, aiTurn)
        return self.decide(res, aiTurn), play

def askUserToPlay():
    pile = int(input("Which pile do you want to take from ? "))
    count = int(input("How many marbles to you want to take ? "))

    return pile, count

board = Board()
ai = AlphaBeta()

while not board.isEmpty():
    winning, (pile, count) = ai.play(board)
    print("ai: pile %d, count %d" % (pile, count))
    board.play(pile, count)

    if board.isEmpty():
        print("Congratz, AI won\n")
        break

    board.printState()

    pile, count = askUserToPlay()
    board.play(pile, count)

    board.printState()

    if board.isEmpty():
        print("Congratz, you won\n")
        break
