from tokenObj import *
from character import *
import string

# CONSTANTES
CHAR_IDENTIFICADOR = string.ascii_lowercase + \
    string.ascii_uppercase + "_" + "1234567890"

CHAR_OPERADOR = "-+"

#######################################
# TOKENS
#######################################
# Constantes tokens tipos
TT_UNION = 'UNION'
TT_DIF = 'DIF'
TT_ID = 'ID'
TT_CHAR = 'CHAR'


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

    def retroceder(self):
        if self.posActual != None:
            self.posActual -= 1

    def splitString(self):
        while self.posActual != None:
            self.avanzar()
            if self.posActual == None:
                break

            # identificar cadena de char
            if self.string[self.posActual] == '"':
                self.plainString()

            # identificar identificador
            elif self.string[self.posActual] in CHAR_IDENTIFICADOR:
                self.retroceder()
                self.identificador()

            # identificar operador
            elif self.string[self.posActual] in CHAR_OPERADOR:
                if self.string[self.posActual] == '+':
                    self.operaciones.append(Token(TT_UNION))
                elif self.string[self.posActual] == '-':
                    self.operaciones.append(Token(TT_DIF))

        print(self.operaciones)

    def identificador(self):
        tempIdentificador = ""
        self.avanzar()
        while self.string[self.posActual] in CHAR_IDENTIFICADOR:
            tempIdentificador += self.string[self.posActual]
            self.avanzar()
            if self.posActual == None:
                break

        self.retroceder()

        # print(tempIdentificador)
        self.operaciones.append(Token(TT_ID, tempIdentificador))

    def plainString(self):
        tempString = ""
        self.avanzar()
        while self.string[self.posActual] != '"':
            tempString += self.string[self.posActual]
            self.avanzar()

        # print(tempString)
        self.operaciones.append(Token(TT_CHAR, Character(tempString)))
