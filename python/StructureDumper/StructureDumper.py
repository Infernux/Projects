#!/usr/bin/python
import os, sys
import re
from enum import Enum

from collections import deque

from mytypes import known_types

def extract_name_body_aliases(string):
    name = ""
    body = ""
    aliases = list()
    return name, body, aliases

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

#TODO: add support for several guards (&& or ||)
#TODO: add support for else
def find_and_extract_guards(line, guards):
    if line.strip().find('#') != 0:
        return line, guards

    print("=== guards start ===")
    print(line)
    guard_index = line.find("#ifdef ")
    if guard_index != -1:
        guard = line[guard_index + len("#ifdef "):]
        guards.append(guard)
        print(guards)

    guard_index = line.find("#ifndef ")
    if guard_index != -1:
        guard = line[guard_index + len("#ifndef "):]
        guards.append(guard)
        print(guards)

    guard_index = line.find("defined(")
    if guard_index != -1:
        guard = line[guard_index + len("defined("):]
        guards.append(guard)
        print(guards)

    line_split = line.split('\n')
    print(len(line_split))

    print("=== guards ===")

    return line, guards

def parse_body(body):
    level = 0
    started = False

    define_queue = deque()

    body = remove_comments_from_body(body)
    #print("after body")
    #print(body)
    #print("---  --")

    current_variable = ""

    for l in body.split(";"):
        array_size = -1
        # look for defines
        l, guards = find_and_extract_guards(l, define_queue)

        if len(define_queue) != 0 and l.find("#endif") != -1:
            define_queue.pop()

        tokens = l.split()
        if len(tokens) != 0:
            variable_type = tokens[0].strip()
            if variable_type in known_types.keys():
                variable_name = tokens[1].strip()
                #look for an array
                array_start = variable_name.find("[")
                if array_start != -1:
                    array_end = variable_name.find("]", array_start)
                    array_size = variable_name[array_start+len("["):array_end]
                    variable_name = variable_name[:array_start]
                    #print("array size : "+str(array_size))

                #print("found known type:", token)
                if variable_type == "char" and array_size != -1:
                    print_method = "%s"
                    print('printf("'+variable_name+'('+variable_type+'):'+print_method+'\\n", pointer->'+variable_name+');')
                else:
                    print_method = known_types[variable_type]
                    if array_size != -1:
                        print('for(U4 var_index = 0; var_index < '+str(array_size) + '; ++var_index) {')
                        print('\tprintf("'+variable_name+'[%d]'+'('+variable_type+'):'+print_method+'\\n", var_index, pointer->'+variable_name+'[var_index]);')
                        print('}')
                    else:
                        print('printf("'+variable_name+'('+variable_type+'):'+print_method+'\\n", pointer->'+variable_name+');')

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
                parse_body(body)
                print("---")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Not enough arguments")

    filename=sys.argv[1]
    structname=sys.argv[2]

    re_struct = generate_struct_regex()
    parse_file(filename, re_struct)
