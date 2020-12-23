#!/usr/bin/python3

import sys
import argparse

def print_stats():
    average = total_us / count
    total = total_us

    print("Tag:{}".format(tag))
    print("Average {}us (Total {}ms)".format(average, total/1e3))
    print("Max {}us at frame {}".format(max_val, max_frame))

filename = sys.argv[1]
tag = sys.argv[2]

total_us = 0
count = 0
max_frame = 0
max_val = 0

with open(filename, 'r') as f:
    for line in f:
        line_tag = line.split(':')[0].strip()
        if line_tag == tag:
            rest = line.split(':')[1]
            rest = rest.split()

            seconds = int(rest[1][:-1]) #remove s
            ms = int(rest[2][:-2]) #remove ms
            us = int(rest[3][:-2]) #remove us

            us = (seconds * int(1e6) + ms * int(1e3) + us)

            if us > max_val:
                max_val = us
                max_frame = count

            total_us += us

            count += 1

print_stats()
