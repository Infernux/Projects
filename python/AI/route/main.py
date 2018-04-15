#!/usr/bin/python

from problem import Problem

class MostOptimisedRoute():
    def __init__(self, start, endName):
        self.openedList = []
        self.openedList.append(start)
        self.closedList = []
        self.endName = endName

    def run(self):
        while len(self.openedList) != 0:
            cur, curWeight = self.openedList[0]
            self.openedList.remove((cur, curWeight))
            if cur.name == self.endName:
                return True

            tmp = []

            inserted = False

            for link, weight in cur.links:
                found = False
                i = 0
                for l, w in self.openedList:
                    #find duplicates and replace weight if <
                    if link.name == l.name:
                        if weight < w:
                            w = weight
                        else:
                            found = True
                            continue

                    if weight < w:
                        break

                    i += 1

                self.openedList.insert(i, (link, weight))

            self.closedList.append(cur)

class Aminus():
    def __init__(self, start, endName):
        self.openedList = []
        self.openedList.append(start)
        self.closedList = []
        self.endName = endName

    def run(self):
        while len(self.openedList) != 0:
            cur, curWeight = self.openedList[0]
            self.openedList.remove((cur, curWeight))
            if cur.name == self.endName:
                for p in self.closedList:
                    print(p.name)
                return True

            tmp = []

            inserted = False

            for link, weight in cur.links:
                weight += link.heuristic*2 #add heuristic
                print("name:%s, w:%d" % (link.name, weight))
                found = False
                i = 0
                for l, w in self.openedList:
                    #find duplicates and replace weight if <
                    if link.name == l.name:
                        if weight < w:
                            w = weight
                        else:
                            found = True
                            continue

                    if weight < w:
                        break

                    i += 1

                self.openedList.insert(i, (link, weight))

            self.closedList.append(cur)

p = Problem()
start = p.getStart()
#mo = MostOptimisedRoute((start, 0), "G")
#mo.run()
am = Aminus((start, 0), "G")
am.run()
