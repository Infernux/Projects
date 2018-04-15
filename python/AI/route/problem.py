class Point():
    def __init__(self, name, heuristic=0):
        self.name = name
        self.links = []
        self.heuristic = heuristic

    def dump(self):
        ret = self.name+":"
        for dest, weight in self.links:
            ret += "(%s,%d)" % (dest.name, weight)
            ret += ";"

        print(ret)

    def addRoute(self, point, weight):
        self.links.append((point, weight))

class Problem():
    def __init__(self):
        self.points = []
        self.setRoutes()
        self.startName = "S"

    def getStart(self):
        return self.getPoint(self.startName)

    def setRoutes(self):
        s = self.createPoint("S")
        a = self.createPoint("A", 8)
        b = self.createPoint("B", 9)
        c = self.createPoint("C", 7)
        d = self.createPoint("D", 5)
        e = self.createPoint("E", 8)
        f = self.createPoint("F", 5)
        g = self.createPoint("G")
        h = self.createPoint("H", 4)
        i = self.createPoint("I", 2)
        j = self.createPoint("J", 3)
        k = self.createPoint("K", 2)
        l = self.createPoint("L", 3)
        m = self.createPoint("M", 4)
        n = self.createPoint("N", 4)

        s.addRoute(a, 2)
        a.addRoute(b, 2)
        a.addRoute(c, 2)
        a.addRoute(d, 15)
        c.addRoute(e, 2)
        c.addRoute(f, 4)
        c.addRoute(h, 4)
        d.addRoute(i, 4)
        d.addRoute(h, 2)
        i.addRoute(m, 2)
        i.addRoute(l, 2)
        h.addRoute(k, 3)
        h.addRoute(j, 2)
        j.addRoute(g, 4)
        j.addRoute(n, 2)

    def getPoint(self, name):
        for p in self.points:
            if p.name == name:
                return p

        raise Exception("Not found")

    def createPoint(self, name, heuristic=0):
        p = Point(name, heuristic)
        self.points.append(p)
        return p

    def dump(self):
        for p in self.points:
            p.dump()
