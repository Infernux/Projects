#!/usr/bin/python3

import matplotlib.pylab as plt

data_folder = "data"
cases_total = "cases_total"

date = "{}月{}日".format(7,25)

x = list()
y = list()

with open("{}/{}_{}.csv".format(data_folder, cases_total, date), "r") as f:
    content = f.read()
    content = content.split("\n")
    content = content[2:-1]

    for line in content:
        line=line.split(",")
        x.append(line[0])
        y.append(int(line[1]))

plt.title("")
plt.stem(x,y)
plt.axis('off')
plt.show()
