from sys import *
from lexer import Lexer

def open_file(filename):
  data = open(filename, "r").read()
  data += "<E0F>"
  return data


def run():
    data = open_file(argv[1])
    lexer = Lexer(data)
    lexer.lex()

 #toks = lex(data)
 #parse(toks)

run()