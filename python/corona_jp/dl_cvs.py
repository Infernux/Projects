#!/usr/bin/python3

from datetime import *
from tools import *

#print(datetime.utcnow())

main_page_src = getSource("https://www.mhlw.go.jp/stf/covid-19/kokunainohasseijoukyou.html").decode("utf-8")

start_idx = main_page_src.find("発生状況 （")
start_idx = main_page_src.find("（",start_idx) + 1
end_idx = main_page_src.find("日",start_idx) + 1

date = main_page_src[start_idx:end_idx]

categories = list()

base_url = "https://www.mhlw.go.jp/content/"

categories.append('current_situation.csv')
categories.append('pcr_positive_daily.csv')
categories.append('pcr_tested_daily.csv')
categories.append('cases_total.csv')
categories.append('recovery_total.csv')
categories.append('death_total.csv')
categories.append('pcr_case_daily.csv')

for categorie in categories:
    src = getSource("{}{}".format(base_url, categorie))
    src = src.decode('utf-8')
    path_part = categorie.split('.')
    with open("data/{}_{}.{}".format(path_part[0], date, path_part[1]), "w") as f:
        f.write(str(src))
    #print(src)
