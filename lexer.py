#lexer.py
class Lexer(object):
    state = 0 #Se for igual a um que dizer que todo caracter será parte de uma string
    tokens = [] #Lista de Tokens
    isexpr = 0 #Flag que verifica se está numa expressão
    varstarted = 0 #Flag que verifica se está numa variável
    var = "" #Contém a váriavel
    string = "" #Contém a string delimitada por " "
    expr = ""  #Armazena as expressões
    filecontents = [] #Arquivo texto

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

    def verificaExpressaoOuNumero(self):
        if self.expr != "" and self.isexpr == 1:
            self.tokens.append("EXPR:" + self.expr)
            return True
        elif self.expr != "" and self.isexpr == 0:
            self.tokens.append("NUM:" + self.expr)
            return True

    def verificaVariavel(self):
        if self.var != "":
            self.tokens.append("VAR:" + self.var)
            self.varstarted = 0
            return True

    def verificaSinalIgual(self, tok):
        if tok == "=" and self.state == 0:
            if self.verificaExpressaoOuNumero() and self.isexpr == 0:
                    self.expr = ""
            if self.verificaVariavel():
                self.var = ""
            if self.tokens[-1] == "EQUALS": #VERIFICA SE EXISTE UM == USADO PARA COMPARACAO
                self.tokens[-1] = "EQEQ"
            else:
                self.tokens.append("EQUALS")
            return True

    def verificaDelimitadorVariavel(self, tok): 
        if (tok == "$" and self.state == 0):
            self.varstarted = 1
            self.var += tok
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

    def verificaTabulacao(self, tok):
        if tok == "\t":
            return True

    def verificaString(self, tok):
        if self.state == 1:
            self.string += tok
            return True

    def verificaKeywordIf(self, tok):
        if tok == "IF" or tok == "if":
            self.tokens.append("IF")
            return True

    def verificaKeywordEndif(self, tok):
        if tok == "ENDIF" or tok == "endif":
            self.tokens.append("ENDIF")
            return True

    def verificaKeywordThen(self, tok):
        if tok == "THEN" or tok == "then":
            if self.expr != "" and self.isexpr == 0:
                self.tokens.append("NUM:" + self.expr)
                self.expr = ""
            self.tokens.append("THEN")
            return True

    def verificaKeywordInput(self, tok):
        if tok == "INPUT" or tok == "input":
            self.tokens.append("INPUT")
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

    def isVariavel(self, tok):
        if self.varstarted == 1:
            if tok == "<" or tok == ">":
                    if self.var != "":
                        self.tokens.append("VAR:" + self.var)
                        self.var = ""
                        self.varstarted = 0
            self.var += tok
            return True

    def lex(self):
        tok = "" #Token

        for char in self.filecontents:
            tok += char 

            if(self.ignoraEspacoVazio(tok)):
                tok = ""
            elif (self.verificarFinalLinhaEDocumento(tok)):
                if(self.verificaExpressaoOuNumero()):
                    self.expr = ""
                elif (self.verificaVariavel()):
                    self.var = ""
                tok = ""
            elif (self.verificaSinalIgual(tok)):
                tok = ""
            elif(self.verificaDelimitadorVariavel(tok)):
                tok = ""
            elif (self.isVariavel(tok)):
                tok = ""
            elif (self.verificaKeywordPrint(tok)):
                tok = ""
            elif (self.verificaTabulacao(tok)):
                tok = ""  
            elif (self.verificaDelimitadorString(tok)):
                tok = ""
            elif (self.verificaString(tok)):
                tok = ""
            elif (self.verificaKeywordIf(tok)):
                tok = ""
            elif (self.verificaKeywordEndif(tok)):
                tok = ""
            elif (self.verificaKeywordThen(tok)):
                tok = ""
            elif (self.verificaKeywordInput(tok)):
                tok = ""
            elif (self.isNumero(tok)):
                tok = ""
            elif (self.isOperador(tok)):
                tok = ""

        return self.tokens
            

