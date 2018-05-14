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


def run():
    data = open_file(argv[1])
    lex(data)

run()
