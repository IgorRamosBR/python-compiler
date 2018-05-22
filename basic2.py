from sys import *

tokens = []
num_stack = []
symbols = {}

def open_file(filename):
  data = open(filename, "r").read()
  data += "<E0F>"
  return data

def lex(filecontents):
  tok = ""
  state = 0
  isexpr = 0
  varstarted = 0
  var = ""
  string = ""
  expr = ""
  n = ""
  filecontents = list(filecontents)
  for char in filecontents:
    tok += char
    if tok == " ":
      if state == 0:
        tok = ""
      else:
        tok = " "
    elif tok == "\n" or tok == "<E0F>":
      if expr != "" and isexpr == 1:
        tokens.append("EXPR:" + expr)
        expr = ""
      elif expr != "" and isexpr == 0:
        tokens.append("NUM:" + expr)
        expr = ""
      elif var != "":
        tokens.append("VAR:" + var)
        vaf = ""
        varstarted = 0
      tok = ""
    elif tok == "=" and state == 0:
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
      tok = ""
    elif tok == "$" and state == 0:
      varstarted = 1
      var += tok
      tok = ""
    elif varstarted == 1:
      if tok == "<" or tok == ">":
        if var != "":
          tokens.append("VAR:" + var)
          var = ""
          varstarted = 0
      var += tok
      tok = ""
    elif tok == "PRINT" or tok == "print":
      tokens.append("PRINT")
      tok = ""
    elif tok == "IF" or tok == "if":
      tokens.append("IF")
      tok = ""
    elif tok == "ENDIF" or tok == "endif":
      tokens.append("ENDIF")
      tok = ""
    elif tok == "THEN" or tok == "then":
      if expr != "" and isexpr == 0:
        tokens.append("NUM:" + expr)
        expr = ""
      tokens.append("THEN")
      tok = ""
    elif tok == "INPUT" or tok == "input":
      tokens.append("INPUT")
      tok = ""
    elif tok == "0" or tok == "1" or tok == "2" or tok == "3" or tok == "4" or tok == "5" or tok == "6" or tok == "7" or tok == "8" or tok == "9":
      expr += tok
      tok = ""
    elif tok == "+" or tok == "-" or tok == "*" or tok == "/" or tok == "(" or tok == ")":
      isexpr = 1
      expr += tok
      tok = ""
    elif tok == "\t":
      tok = ""  
    elif tok == "\"" or tok == " \"":
      if state == 0:
        state = 1
      elif state == 1:
        tokens.append("STRING:" + string + "\"")
        string = ""
        state = 0
        tok = ""
    elif state == 1:
      string += tok
      tok = ""

  print(tokens)
  return ''
  #return tokens



def evalExpression(expr):
  
  return eval(expr)

def doPRINT(toPRINT):
  if(toPRINT[0:6] == "STRING"):
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
    return "VARIABLE ERRROR: Undefined Variable"
    exit()

def getINPUT(string, varname):
  i = input(string[1:-1] + " ")
  symbols[varname] = "STRING:\"" + i + "\""

def parse(toks):
  i = 0
  while(i < len(toks)):
    if toks[i] + " " + toks[i+1][0:6] == "PRINT STRING" or toks[i] + " " + toks[i+1][0:3] == "PRINT NUM" or toks[i] + " " + toks[i+1][0:4] == "PRINT EXPR" or toks[i] + " " + toks[i+1][0:3] == "PRINT VAR":
      if toks[i+1][0:6] == "STRING":
        doPRINT(toks[i+1])
      elif toks[i+1][0:3] == "NUM":
        doPRINT(toks[i+1])
      elif toks[i+1][0:4] == "EXPR":
        doPRINT(toks[i+1])
      elif toks[i+1][0:3] == "VAR":
        doPRINT(getVARIABLE(toks[i+1]))  
      i += 2
    elif toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:6] == "VAR EQUALS STRING" or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "VAR EQUALS NUM" or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:4] == "VAR EQUALS EXPR":
      if toks[i+2][0:6] == "STRING":
        doASSIGN(toks[i],toks[i+2])
      elif toks[i+2][0:3] == "NUM":
        doASSIGN(toks[i],toks[i+2])
      elif toks[i+2][0:4] == "EXPR":
        doASSIGN(toks[i],"NUM:" + str(evalExpression(toks[i+2][5:])))
      i+=3


def run():
 data = open_file(argv[1])
 toks = lex(data)
 parse(toks)

run()