#!/usr/bin/python3

import sys

class Token():
    def __init__(self, moji):
        self.moji = moji
        self.count = 1

class Ngram():
    def __init__(self,size):
        self.size = size
        self.table = []

    def newToken(self,token):
        #look if it is already here
        #token = token.strip()
        for t in self.table:
            if t.moji == token:
                t.count += 1
                return

        self.table.append(Token(token))

    def readSentence(self,sentence):
        for i in range(0,len(sentence) - self.size + 1):
            self.newToken(sentence[i:i+self.size])

    def sort(self):
        self.table.sort(key=lambda el:el.count, reverse=True)

    def dump(self):
        for t in self.table:
            print("token : %s (%d)" % (t.moji, t.count))

with open(sys.argv[1]) as f:
    ngram = Ngram(5)
    for line in f:
        #print(line)
        ngram.readSentence(line)

    ngram.sort()
    ngram.dump()
