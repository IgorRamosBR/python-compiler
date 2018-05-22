class Parser(object):
    toks = ""

    def __init__(self, tokens):
        self.toks = tokens

    def verificaPrint(self, i):
        if (self.toks[i] + " " + self.toks[i+1][0:6] == "PRINT STRING"):
            return True

    def evalExpression(self, expr):
            return eval(expr)

    def doPrint(self, toPRINT):
        if(toPRINT[0:6] == "STRING"):
            toPRINT = toPRINT[8:]
            toPRINT = toPRINT[:-1]
        elif(toPRINT[0:3] == "NUM"):
            toPRINT = toPRINT[4:]
        elif(toPRINT[0:4] == "EXPR"):
            toPRINT = self.evalExpression(toPRINT[5:])
        print(toPRINT)

    def parse(self):
        i = 0
        while(i < len(self.toks)):
            if(self.verificaPrint(i)):
                self.doPrint(self.toks[i+1])
            i += 2


