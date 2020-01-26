#!/usr/bin/python
import os, sys
import re
from enum import Enum

known_types = dict()
known_types["uint32_t"] = "%d"

class parse_status(Enum):
    START = 1
    BODY = 2

def generate_struct_regex():
    return re.compile("typedef struct *")

def extract_body(filehandle, first_line):
    buf = ""
    body = ""
    header = ""
    aliases = ""

    level = 0
    started = False

    try:
        start_index = first_line.index("{")
        if start_index != None:
            header = first_line[:start_index]
            buf = first_line[start_index+1:]
            level += 1
            started = True
    except:
        buf = first_line

    for l in filehandle:
        try:
            start_index = l.index("{")
            if start_index != None:
                if started == False:
                    header = buf + l[:start_index]
                    buf = l[start_index+1:]
                    started = True
                else:
                    buf += l
                l = l[start_index+1:]
                level += 1
                continue
        except:
            pass

        try:
            close_index = l.index("}")
            if close_index != None:
                level -= 1

                if level == 0 and started == True:
                    buf += l[:close_index]
                    body = buf
                    buf = l[close_index+1:]
                    break
        except:
            pass

        buf += l

        #print("level : " + str(level))

    try:
        last_index = l.index(";")
        if last_index != None:
            aliases = buf[:last_index-1]
    except:
        for l in filehandle:
            last_index = l.index(";")
            if last_index != None:
                aliases = buf + l[:last_index]

    aliases = aliases.split(",")

    return header, body, aliases

def parse_body(body):
    level = 0
    started = False

    current_variable = ""

    #search for typedef to {
    td_idx = body.index("typedef")
    typedef_end_idx = body.index("{")

    struct_name = body[td_idx:typedef_end_idx]
    print(struct_name)

    return

    for l in body.split("\n"):
        try:
            index = l.index("{")
            started = True
            level += 1 #no need to test, index raises an exception if not found
            if index != len(l) :
                #parse rest
                pass
            continue
        except:
            pass

        try:
            index = l.index("}")
            level -= 1
            continue
        except:
            pass

        try:
            index = l.index(";")
            current_variable += l[:index]
            print(current_variable)
            current_variable = ""
            continue
        except:
            pass

        if level == 0 and started == True:
            return

        current_variable += l

    #find first {
    #parse till first ;
    #do, until last }

def parse_file(filename, re_struct):
    status = parse_status.START
    with open(filename) as f:
        for l in f:
            if re_struct.match(l):
                header, body, aliases = extract_body(f, l)
                print("--- header ---")
                print(header)
                print("--- body ---")
                print(body)
                print("--- aliases ---")
                print(aliases)
                print("---")
                #parse_body(body)

if len(sys.argv) != 3:
    print("Not enough arguments")

filename=sys.argv[1]
structname=sys.argv[2]

re_struct = generate_struct_regex()
parse_file(filename, re_struct)
