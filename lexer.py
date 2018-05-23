#lexer.py
class Lexer(object):
    state = 0 #Se for igual a um que dizer que todo caracter será parte de uma string
    tokens = []
    isexpr = 0 #Flag que verifica se está numa expressão
    varstarted = 0
    var = ""
    string = "" #Contém a string delimitada por " "
    expr = ""  #Armazena as expressões
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
    
    def verificarFinalLinhaEDocumento(self, tok):
        if tok == "\n" or tok == "<E0F>":
            return True

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

    def isNumero(self, tok):
        if tok == "0" or tok == "1" or tok == "2" or tok == "3" or tok == "4" or tok == "5" or tok == "6" or tok == "7" or tok == "8" or tok == "9":
            self.expr += tok
            return True

    def isOperador(self, tok):
        if tok == "+" or tok == "-" or tok == "*" or tok == "/" or tok == "(" or tok == ")":
            self.isexpr = 1
            self.expr += tok
            return True

    def isExpressaoOuNumero(self):
        if self.expr != "" and self.isexpr == 1:
            self.tokens.append("EXPR:" + self.expr)
            return True
        elif self.expr != "" and self.isexpr == 0:
            self.tokens.append("NUM:" + self.expr)
            return True

    def lex(self):
        tok = "" #Token

        for char in self.filecontents:
            tok += char 

            if(self.ignoraEspacoVazio(tok)):
                tok = ""
            elif (self.verificarFinalLinhaEDocumento(tok)):
                tok = ""
                if(self.isExpressaoOuNumero()):
                    self.expr = ""
            elif (self.verificaKeywordPrint(tok)):
                tok = ""
            elif (self.verificaDelimitadorString(tok)):
                tok = ""
            elif (self.verificaEAdicionaString(tok)):
                tok = ""
            elif (self.isNumero(tok)):
                tok = ""
            elif (self.isOperador(tok)):
                tok = ""

        return self.tokens
            

