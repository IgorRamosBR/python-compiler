from sys import *
from lexer import Lexer
from parse import Parser

def open_file(filename):
  data = open(filename, "r").read()
  data += "<E0F>"
  return data


def run():
    data = open_file(argv[1])
    lexer = Lexer(data)
    tokens = lexer.lex()
    
    parser = Parser(tokens)
    parser.parse()
 #toks = lex(data)
 #parse(toks)

run()
