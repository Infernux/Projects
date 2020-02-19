#!/usr/bin/python
import os, sys
import re
from enum import Enum

from collections import deque

from mytypes import known_types

MAX_ITER_COUNT = 100

class IR_node():
    def __init__(self, vartype = None, varname = None, pointer = 0, array = list()):
        self.type = vartype
        self.varname = varname
        self.pointer = 0 #* count
        self.array = array #number/const per array [cnt][3] -> "cnt" "3"

class parse_state(Enum):
    INIT = 0 #looking for typedef
    TYPEDEF = 1 # looking for struct
    STRUCT = 2 #looking for name
    NAME = 3 #looking for {
    START = 4 #looking for }
    END = 5 #looking for the final ;
    DONE = 6

class ir_state(Enum):
    INIT = 0
    TYPE = 1
    VARNAME = 2


def extract_IR_from_body(body):
    res = list()
    status = ir_state.INIT
    buf = ""
    pointer_cnt = 0
    array_list = list()

    for l in body.split("\n"):
        l = l.strip()
        if len(l) == 0:
            continue
        elif l[0] == "#": #a new line is mandatory before and after a preprocessor (I think)
            pass

        while l.find(";") != -1:
            if status == ir_state.INIT:
                new_l = l.split()
                if len(new_l) <= 1:
                    break

                star_split = new_l[0].split("*") #handle cases where the star is attached to the variable name
                vartype = star_split[0]
                l = " ".join(new_l[1:])

                if len(star_split) > 1:
                    l = star_split[1] + l
                status = ir_state.TYPE
                #print(vartype)
            if status == ir_state.TYPE:
                for c in l: #parse per character
                    if c == "*":
                        pointer_cnt+=1
                    elif c == " ":
                        pass
                    elif c.isalpha() == True:
                        buf += c
                        status = ir_state.VARNAME
                        l = l[1:]
                        break
                    else:
                        raise Exception
                    l = l[1:]
            if status == ir_state.VARNAME:
                for c in l: #parse per character
                    if c == ";":
                        #print(buf)
                        ir_node = IR_node(vartype, buf, pointer_cnt, array_list)
                        res.append(ir_node)

                        buf = ""
                        pointer_cnt = 0
                        array_list = list()
                        status = ir_state.INIT
                        l = l[1:]
                        break
                    elif c.isalnum() == True:
                        buf += c

    return res

def remove_comments_from_line(string, is_multiline_comment):
    if is_multiline_comment == True:
        index = string.find("*/")
        if index != -1:
            string = string[index + len("*/"):]
            string, is_multiline_comment = remove_comments_from_line(string, False)
        else:
            string = ""
    else:
        index_single = string.find("//")
        index_multi = string.find("/*")

        if index_single != -1 and index_multi != -1:
            if index_single < index_multi:
                string = string[:index_single]
            else:
                new_buf, is_multiline_comment = remove_comments_from_line(string[index_multi+len("/*"):], True)
                string = string[:index_multi] + new_buf
        elif index_single != -1:
            string = string[:index_single]
        elif index_multi != -1:
            new_buf, is_multiline_comment = remove_comments_from_line(string[index_multi+len("/*"):], True)
            string = string[:index_multi] + new_buf

    return string, is_multiline_comment

def extract_name_body_aliases(string):
    name = ""
    body = ""
    aliases = list()

    status = parse_state.INIT
    comment_status = False
    depth = 0

    iteration_count = 0

    for l in string.split("\n"):
        l, comment_status = remove_comments_from_line(l, comment_status)

        if iteration_count >= 10:
            print("we fucked up my dear")
            print(status)

        iteration_count = 0

        while len(l) != 0 and iteration_count < MAX_ITER_COUNT:
            l = l.lstrip()
            iteration_count += 1
            if status == parse_state.INIT:
                needed_token = "typedef"
                index = l.find(needed_token)
                if index != -1:
                    status = parse_state.TYPEDEF
                    l = l[index + len(needed_token):]
            elif status == parse_state.TYPEDEF:
                needed_token = "struct"
                index = l.find(needed_token)
                if index != -1:
                    status = parse_state.STRUCT
                    l = l[index + len(needed_token):]
            elif status == parse_state.STRUCT:
                needed_token = "{"
                index = l.find(needed_token)
                if index != -1:
                    name = l[:index].strip()
                    l = l[index-1:]
                    status = parse_state.NAME
                    continue

                needed_token = " "
                index = l.find(needed_token)

                if index != -1:
                    name = l[:index].strip()
                    l = l[index + len(needed_token):]
                else:
                    name = l.strip()
                    l = ""
                status = parse_state.NAME
            elif status == parse_state.NAME:
                needed_token = "{"
                index = l.find(needed_token)
                if index != -1:
                    status = parse_state.START
                    depth+=1
                    l = l[index + len(needed_token):]
                else:
                    break #out the while loop
            elif status == parse_state.START:
                needed_token_start = "{"
                needed_token_end = "}"
                index_start = l.find(needed_token_start)
                index_end = l.find(needed_token_end)

                if index_start != -1 and index_end != -1:
                    if index_start < index_end:
                        depth+=1
                        body += l[:index_start].strip()
                        l = l[index_start + len(needed_token_start):]
                    else:
                        body += l[:index_end].strip()
                        l = l[index_end + len(needed_token_end):]
                        depth-=1
                elif index_start != -1:
                    depth+=1
                    body += l[:index_start].strip()
                    l = l[index_start + len(needed_token_start):]
                elif index_end != -1:
                    depth-=1
                    body += l[:index_end].strip()
                    l = l[index_end + len(needed_token_end):]
                else:
                    body += l.strip()
                    l = ""

                if depth == 0:
                    status = parse_state.END
                else:
                    body += "\n"
            elif status == parse_state.END:
                needed_token_separator = ","
                needed_token_final = ";"

                index_separator = l.find(needed_token_separator)
                index_final = l.find(needed_token_final)

                if index_separator != -1 and index_final != -1:
                    if index_separator < index_final:
                        alias = l[:index_separator]
                        alias = alias.strip()
                        if len(alias) != 0:
                            aliases.append(alias)
                        l = l[index_separator + len(needed_token_separator):]
                    else:
                        alias = l[:index_final]
                        alias = alias.strip()
                        if len(alias) != 0:
                            aliases.append(alias)
                        l = l[index_final + len(needed_token_final):]
                        status = parse_state.DONE
                        break #TODO?: make it compatible with several typedef on the same line... is that even a thing ?
                elif index_separator != -1:
                    alias = l[:index_separator]
                    alias = alias.strip()
                    if len(alias) != 0:
                        aliases.append(alias)
                    l = l[index_separator + len(needed_token_separator):]
                elif index_final != -1:
                    alias = l[:index_final]
                    alias = alias.strip()
                    if len(alias) != 0:
                        aliases.append(alias)
                    l = l[index_final + len(needed_token_final):]
                    status = parse_state.DONE
                    break #TODO?: make it compatible with several typedef on the same line... is that even a thing ?
                else:
                    alias = l.strip()
                    aliases.append(alias)
                    break

    body = re.sub(' +', ' ', body)

    return name, body.strip(), aliases






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
