from sys import *

tokens = []

def open_file(filename):
    data = open(filename, "r").read()
    return data


def lex(filecontent):
    token = ""
    state = 0
    string = ""
    filecontents = list(filecontent)
    for char in filecontents:
        token += char
        if token == " ":
            if state == 0:
                token = ""
            else: 
                token = " "
        elif token == "\n":
            token = ""
        elif token == "PRINT":
            tokens.append("PRINT")
            token = ""
        elif token == "\"":
            if state == 0:
                state = 1
            elif state == 1:
                tokens.append("STRING:" + string + "\"")
                string = ""
                state = 0
                token = ""
        elif state == 1:
            string += token
            token = ""
    return tokens
    #print(tokens)


def parse(toks):
    i = 0
    print(toks)
    while (i < len(toks)):
        if toks[i] + " " + toks[i + 1][0:6] == "PRINT STRING":
            print(toks[i + 1][7:])
            i += 2


def run():
    data = open_file(argv[1])
    toks = lex(data)
    parse(toks)
run()
