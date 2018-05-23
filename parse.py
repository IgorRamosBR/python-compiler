class Parser(object):
    toks = "" #tokens
    symbols = {} #tabela de simbolos

    def __init__(self, tokens):
        self.toks = tokens

    def verificaPrint(self, i):
        if (self.toks[i] + " " + self.toks[i+1][0:6] == "PRINT STRING") or self.toks[i] + " " + self.toks[i+1][0:3] == "PRINT NUM" or self.toks[i] + " " + self.toks[i+1][0:4] == "PRINT EXPR" or self.toks[i] + " " + self.toks[i+1][0:3] == "PRINT VAR":
            return True

    def buscaVariavel(self, varname):
        varname = varname[4:]
        if varname in self.symbols:
            return self.symbols[varname]
        else:
            return "VARIABLE ERRROR: Undefined Variable"
            exit()

    def atribui(self, i):
        if self.toks[i+2][0:6] == "STRING":
            self.symbols[self.toks[i][4:]] = self.toks[i+2]
        elif self.toks[i+2][0:3] == "NUM":
            self.symbols[self.toks[i][4:]] = self.toks[i+2]
        elif self.toks[i+2][0:4] == "EXPR":
            self.symbols[self.toks[i][4:]] = "NUM:" + str(eval(self.toks[i+2][5:]))
        elif self.toks[i+2][0:3] == "VAR":
            self.symbols[self.toks[i][4:]] = self.buscaVariavel(self.toks[i+2])

    def fazAtribuicao(self, i):
        if self.toks[i][0:3] + " " + self.toks[i+1] + " " + self.toks[i+2][0:6] == "VAR EQUALS STRING" or self.toks[i][0:3] + " " + self.toks[i+1] + " " + self.toks[i+2][0:3] == "VAR EQUALS NUM" or self.toks[i][0:3] + " " + self.toks[i+1] + " " + self.toks[i+2][0:4] == "VAR EQUALS EXPR" or self.toks[i][0:3] + " " + self.toks[i+1] + " " + self.toks[i+2][0:3] == "VAR EQUALS VAR":
            self.atribui(i)
            return True

    def evalExpression(self, expr):
            return eval(expr)

    def doPrint(self, toPRINT):
        if(toPRINT[0:6] == "STRING"):
            toPRINT = toPRINT[8:]
            toPRINT = toPRINT[:-1]
            print(toPRINT) 
        elif(toPRINT[0:3] == "NUM"):
            toPRINT = toPRINT[4:]
            print(toPRINT)
        elif(toPRINT[0:4] == "EXPR"):
            toPRINT = self.evalExpression(toPRINT[5:])
            print(toPRINT)
        elif toPRINT[0:3] == "VAR":
            self.doPrint((self.buscaVariavel(toPRINT)))

    def realizaInput(self, i):
        if self.toks[i] + " " + self.toks[i+1][0:6] + " " + self.toks[i+2][0:3] == "INPUT STRING VAR":
            string = self.toks[i+1][7:]
            varname = self.toks[i+2][4:]

            i = input(string[1:-1] + " ")
            self.symbols[varname] = "STRING:\"" + i + "\""

            return True

    def verificaIf(self, i):
        if self.toks[i] + " " + self.toks[i+1][0:3] + " " + self.toks[i+2] + " " + self.toks[i+3][0:3] + " " + self.toks[i+4] == "IF NUM EQEQ NUM THEN":
            return True

    def parse(self):
        i = 0
        while(i < len(self.toks)):
            if self.toks[i] == "ENDIF":
                i+=1
            elif(self.verificaPrint(i)):
                self.doPrint(self.toks[i+1])
                i += 2
            elif (self.fazAtribuicao(i)):
                i+=3
            elif (self.realizaInput(i)):
                i+=3
            elif (self.verificaIf(i)):
                i+=5



