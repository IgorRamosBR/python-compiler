class Parser(object):
    toks = ""
    symbols = {}

    def __init__(self, tokens):
        self.toks = tokens

    def verificaPrint(self, i):
        if (self.toks[i] + " " + self.toks[i+1][0:6] == "PRINT STRING") or self.toks[i] + " " + self.toks[i+1][0:3] == "PRINT NUM" or self.toks[i] + " " + self.toks[i+1][0:4] == "PRINT EXPR" or self.toks[i] + " " + self.toks[i+1][0:3] == "PRINT VAR":
            return True

    def evalExpression(self, expr):
            return eval(expr)

    def getVARIABLE(self, varname):
        varname = varname[4:]
        if varname in self.symbols:
            return self.symbols[varname]
        else:
            return "VARIABLE ERRROR: Undefined Variable"
            exit()

    def doPrint(self, toPRINT):
        if(toPRINT[0:6] == "STRING"):
            toPRINT = toPRINT[8:]
            toPRINT = toPRINT[:-1]
            print(toPRINT) #diferente
        elif(toPRINT[0:3] == "NUM"):
            toPRINT = toPRINT[4:]
            print(toPRINT)
        elif(toPRINT[0:4] == "EXPR"):
            toPRINT = self.evalExpression(toPRINT[5:])
            print(toPRINT)
        elif toPRINT[0:3] == "VAR":
            self.doPrint((self.getVARIABLE(toPRINT)))
        

    def doASSIGN(self, varname, varvalue):
        self.symbols[varname[4:]] = varvalue

    def parse(self):
        i = 0
        while(i < len(self.toks)):
            if(self.verificaPrint(i)):
                self.doPrint(self.toks[i+1])
                i += 2
            elif self.toks[i][0:3] + " " + self.toks[i+1] + " " + self.toks[i+2][0:6] == "VAR EQUALS STRING"  or self.toks[i][0:3] + " " + self.toks[i+1] + " " + self.toks[i+2][0:3] == "VAR EQUALS NUM" or self.toks[i][0:3] + " " + self.toks[i+1] + " " + self.toks[i+2][0:4] == "VAR EQUALS EXPR" or self.toks[i] + " " + self.toks[i+1][0:3] == "PRINT VAR":
                if self.toks[i+2][0:6] == "STRING":
                    self.doASSIGN(self.toks[i],self.toks[i+2])
                elif self.toks[i+2][0:3] == "NUM":
                    self.doASSIGN(self.toks[i],self.toks[i+2])
                elif self.toks[i+2][0:4] == "EXPR":
                    self.doASSIGN(self.toks[i],"NUM:" + str(eval(self.toks[i+2][5:])))
                i+=3



