#!/usr/bin/python
import os, sys
import re
from enum import Enum

class parse_status(Enum):
    START = 1
    BODY = 2

def generate_struct_regex():
    return re.compile("typedef struct *")

def extract_body(filehandle, first_line):
    body = ""
    body += first_line
    level = 0
    started = False
    for l in filehandle:
        try:
            if l.index("}") != None:
                level -= 1
        except:
            pass
        try:
            if l.index("{") != None:
                level += 1
                started = True
        except:
            pass

        if level == 0 and started == True:
            body += l
            return body
        body += l

        #print("level : " + str(level))

    return body
                

def parse_file(filename, re_struct):
    status = parse_status.START
    with open(filename) as f:
        for l in f:
            if re_struct.match(l):
                body = extract_body(f, l)
                print(body)

if len(sys.argv) != 3:
    print("Not enough arguments")

filename=sys.argv[1]
structname=sys.argv[2]

re_struct = generate_struct_regex()
parse_file(filename, re_struct)
