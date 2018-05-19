from sys import *

tokens = []
num_stack = []

def open_file(filename):
    data = open(filename, "r").read()
    data += "<EOF>"
    return data


def lex(filecontent):
    token = ""
    state = 0
    isexpr = 0
    string = ""
    expr = ""
    n = ""
    filecontents = list(filecontent)
    for char in filecontents:
        token += char
        if token == " ":
            if state == 0:
                token = ""
            else: 
                token = " "
        elif token == "\n" or token == "<EOF>":
            if expr != "" and isexpr == 1:
                tokens.append("EXPR:" + expr)
                expr = ""
            elif expr != "" and isexpr == 0:
                tokens.append("NUM:" + expr)
                expr = ""
            token = ""
        elif token.isdigit():
            expr += token
            token = ""
        elif token == "+" or token == "-" or token == "/" or token== "*" or token == "(" or token == ")":
            isexpr = 1
            expr += token
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
    
    #print(tokens)
    return tokens

def evalExpression(expr):
    return eval(expr)

def doPRINT(toPRINT):
    if (toPRINT[0:6] == "STRING"):
        toPRINT = toPRINT[8:]
        toPRINT = toPRINT[:-1]
    elif(toPRINT[0:3] == "NUM"):
        toPRINT = toPRINT[4:]
    elif(toPRINT[0:4] == "EXPR"):
        toPRINT = evalExpression(toPRINT[5:])
    print(toPRINT)


def parse(toks):
    i = 0
    while (i < len(toks)):
        if toks[i] + " " + toks[i + 1][0:6] == "PRINT STRING" or toks[i] + " " + toks[i + 1][0:3] == "PRINT NUM" or toks[i] + " " + toks[i + 1][0:4] == "PRINT EXPR":
            if toks[i+1][0:6] == "STRING":
                doPRINT(toks[i + 1])
            elif toks[i+1][0:3] == "NUM":
                doPRINT(toks[i + 1])
            elif toks[i+1][0:4] == "EXPR":
                doPRINT(toks[i + 1])
            i += 2


def run():
    data = open_file(argv[1])
    toks = lex(data)
    parse(toks)
run()
