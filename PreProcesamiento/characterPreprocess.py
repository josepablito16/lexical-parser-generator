class CharacterPreprocess:
    def __init__(self, string):
        self.posActual = -1
        self.string = string
        self.operaciones = []
        self.dobleComillaAbierta = False
        self.comillaAbierta = False

    def avanzar(self):
        if self.posActual < len(self.string) - 1:
            self.posActual += 1
        else:
            self.posActual = None

    def splitString(self):
        while self.posActual != None:
            self.avanzar()
            if self.posActual == None:
                break

            # identificar cadena de char
            if self.string[self.posActual] == '"':
                self.plainString()

    def plainString(self):
        tempString = ""
        self.avanzar()
        while self.string[self.posActual] != '"':
            tempString += self.string[self.posActual]
            self.avanzar()

        print(tempString)
