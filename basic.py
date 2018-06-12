from sys import *

tokens = []
num_stack = []
symbols = {}

def open_file(filename):
    data = open(filename, "r").read()
    data += "<EOF>"
    return data


def lex(filecontent):
    token = ""
    state = 0
    isexpr = 0
    varstarted = 0
    var = ""
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
            elif var != "":
                tokens.append("VAR:" + var)
                var = "" 
                varstarted = 0
            token = ""
        elif token == "=" and state  == 0:
            if expr != "" and isexpr == 0:
                tokens.append("NUM:" + expr)
                expr = ""
            if var != "":
                tokens.append("VAR:" + var)
                var = "" 
                varstarted = 0
            if tokens[-1] == "EQUALS":
                tokens[-1] = "EQEQ"
            else:    
                tokens.append("EQUALS")
            token = ""     
       
        elif token == "$" and state == 0:
            varstarted = 1   
            var += token
            token = ""
        elif varstarted == 1:
            if token == "<" or token ==">":
                if var != "":
                    tokens.append("VAR:" + var)
                    var = "" 
                    varstarted = 0
            var += token
            token = "" 
        elif token.isdigit():
            expr += token
            token = ""
        elif token == "+" or token == "-" or token == "/" or token== "*" or token == "(" or token == ")":
            isexpr = 1
            expr += token
            token = ""
        elif token == "\t":
            token = ""
        elif token == "PRINT":
            tokens.append("PRINT")
            token = ""
        elif token == "IF":
            tokens.append("IF")
            token = ""
        elif token == "ENDIF":
            tokens.append("ENDIF")
            token = ""
        elif token == "THEN":
            if expr != "" and isexpr == 0:
                tokens.append("NUM:" + expr)
                expr = ""
            tokens.append("THEN")
            token = ""
        elif token == "INPUT":
            tokens.append("INPUT")
            token = ""
        elif token == "\"" or token == " \"":
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
    
    print(tokens)
    #return ''
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

def doASSIGN(varname, varvalue):
    symbols[varname[4:]] = varvalue

def getVARIABLE(varname):
    varname = varname[4:]
    if varname in symbols:
        return symbols[varname]
    else:
        return "Variable Error: Undefined Variable"
        exit()

def getINPUT(string, varname):
    i = input(string[1:-1] + " ")
    symbols[varname] = "STRING:\"" + i + "\""

def parse(toks):
    i = 0
    while (i < len(toks)):
        if toks[i] == "ENDIF":
            i+=1
        elif toks[i] + " " + toks[i + 1][0:6] == "PRINT STRING" or toks[i] + " " + toks[i + 1][0:3] == "PRINT NUM" or toks[i] + " " + toks[i + 1][0:3] == "PRINT VAR":
            if toks[i+1][0:6] == "STRING":
                doPRINT(toks[i + 1])
            elif toks[i+1][0:3] == "NUM":
                doPRINT(toks[i + 1])
            elif toks[i+1][0:4] == "EXPR":
                doPRINT(toks[i + 1])
            elif toks[i+1][0:3] == "VAR":
                doPRINT(getVARIABLE(toks[i+1]))
            i += 2
        elif toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:6] == "VAR EQUALS STRING" or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "VAR EQUALS NUM" or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:4] == "VAR EQUALS EXPR" or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "VAR EQUALS VAR":
            if toks[i+2][0:6] == "STRING":
                doASSIGN(toks[i],toks[i+2])
            elif toks[i+2][0:3] == "NUM":
                doASSIGN(toks[i],toks[i+2])
            elif toks[i+2][0:4] == "EXPR":
                doASSIGN(toks[i],"NUM:" + str(evalExpression(toks[i+2][5:])))
            elif toks[i+2][0:3] == "VAR":
                doASSIGN(toks[i],getVARIABLE(toks[i+2]))
            i += 3
        elif toks[i] + " " + toks[i+1][0:6] + " " + toks[i+2][0:3] == "INPUT STRING VAR":
            getINPUT(toks[i+1][7:],toks[i+2][4:])
            i += 3
        elif toks[i] + " " + toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3] + " " + toks[i+4] == "IF NUM EQEQ NUM THEN":
            
            if toks[i+1][4:] == toks[i+3][4:]:
                print("True")
            else:
                print ("False")

            i += 5
        #INPUT STRING:"" VAR:$VARIABLE       
        #print (symbols)


def run():
    data = open_file(argv[1])
    toks = lex(data)
    parse(toks)
run()
