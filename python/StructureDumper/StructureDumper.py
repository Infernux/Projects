#!/usr/bin/python
import os, sys
import re
from enum import Enum

known_types = dict()
known_types["uint32_t"] = "%d"
known_types["uint8_t"] = "%d"
known_types["int"] = "%d"
known_types["char"] = "%c"

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

def remove_comments_from_body(body):
    processed_body = ""
    reprocessed_body = ""
    #single line comments
    for l in body.split("\n"):
        comment_index = l.find("//")
        if comment_index != -1:
            processed_body += l[:comment_index - 1]
            continue

        processed_body += l

    comment_index_start = processed_body.find("/*", 0)
    current_index = 0
    while comment_index_start != -1:
        comment_index_end = processed_body.find("*/", comment_index_start)
        reprocessed_body += processed_body[current_index:comment_index_start]
        current_index = comment_index_end + len("*/")
        comment_index_start = processed_body.find("/*", comment_index_end)

    reprocessed_body += processed_body[current_index:]

    return reprocessed_body

def parse_body(body):
    level = 0
    started = False

    body = remove_comments_from_body(body)
    print("after body")
    print(body)
    print("---  --")

    current_variable = ""

    for l in body.split(";"):
        print(l)

    #find first {
    #parse till first ;
    #do, until last }

def parse_file(filename, re_struct):
    status = parse_status.START
    with open(filename) as f:
        for l in f:
            if re_struct.match(l):
                header, body, aliases = extract_body(f, l)
                #print("--- header ---")
                #print(header)
                print("--- body ---")
                print(body)
                #print("--- aliases ---")
                #print(aliases)
                print("---")
                parse_body(body)
                print("---")

if len(sys.argv) != 3:
    print("Not enough arguments")

filename=sys.argv[1]
structname=sys.argv[2]

re_struct = generate_struct_regex()
parse_file(filename, re_struct)
