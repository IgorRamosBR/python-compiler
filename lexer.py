#lexer.py
class Lexer(object):
    state = 0 #Se for igual a um que dizer que todo caracter será parte de uma string
    tokens = []
    isexpr = 0
    varstarted = 0
    var = ""
    string = "" #Contém a string delimitada por " "
    expr = ""
    n = ""
    filecontents = []

    def __init__(self, filecontent):
        self.filecontents = list(filecontent)

    def ignoraEspacoVazio(self, tok): 
        if tok == " ": 
            if self.state == 0: #VERIFICA SE NAO FAZ PARTE DE UMA STRING
                return True
            else: 
                return False

    def verificaKeywordPrint(self, tok):
        if tok == "PRINT" or tok == "print":
            self.tokens.append("PRINT")
            return True
    
    def verificaDelimitadorString(self, tok):
        if tok == "\"" or tok == " \"":
            if self.state == 0:
                self.state = 1
            elif self.state == 1:
                self.tokens.append("STRING:" + self.string + "\"")
                self.string = ""
                self.state = 0
                return True

    def verificaEAdicionaString(self, tok):
        if self.state == 1:
            self.string += tok
            return True

    def lex(self):
        tok = "" #Token

        for char in self.filecontents:
            tok += char 

            if(self.ignoraEspacoVazio(tok)):
                tok = ""
            elif (self.verificaKeywordPrint(tok)):
                tok = ""
            elif (self.verificaDelimitadorString(tok)):
                tok = ""
            elif (self.verificaEAdicionaString(tok)):
                tok = ""
        
        return self.tokens
            

