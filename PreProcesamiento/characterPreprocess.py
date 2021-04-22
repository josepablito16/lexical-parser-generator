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

    def avanzarChar(self):
        if self.posActual < len(self.string) - 1:
            self.posActual += 1
        else:
            self.posActual = None

    def avanzarOperaciones(self):
        if self.posActual < len(self.operaciones) - 1:
            self.posActual += 1
        else:
            self.posActual = None

    def retroceder(self):
        if self.posActual != None:
            self.posActual -= 1

    def splitString(self):
        while self.posActual != None:
            self.avanzarChar()
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

    def identificador(self):
        tempIdentificador = ""
        self.avanzarChar()
        while self.string[self.posActual] in CHAR_IDENTIFICADOR:
            tempIdentificador += self.string[self.posActual]
            self.avanzarChar()
            if self.posActual == None:
                break

        self.retroceder()

        # print(tempIdentificador)
        self.operaciones.append(Token(TT_ID, tempIdentificador))

    def plainString(self):
        tempString = ""
        self.avanzarChar()
        while self.string[self.posActual] != '"':
            tempString += self.string[self.posActual]
            self.avanzarChar()

        # print(tempString)
        self.operaciones.append(Token(TT_CHAR, Character(tempString)))

    def operar(self, expresionesTratadas):
        self.posActual = -1
        operacionCola = []
        while self.posActual != None:
            self.avanzarOperaciones()
            if self.posActual == None:
                break

            # solo es char
            if self.operaciones[self.posActual].tipo == TT_CHAR:
                operacionCola.append(self.operaciones[self.posActual])

            # operacion de union
            elif self.operaciones[self.posActual].tipo == TT_UNION:
                self.avanzarOperaciones()
                char1 = operacionCola.pop().valor
                char2 = self.operaciones[self.posActual].valor.elementos
                char1.union(char2)

                operacionCola.append(Token(TT_CHAR, char1))

            # solo es un identificador
            elif self.operaciones[self.posActual].tipo == TT_ID:
                print(f'es id {self.operaciones[self.posActual]}')
                if self.operaciones[self.posActual].valor in expresionesTratadas:
                    valorId = expresionesTratadas[self.operaciones[self.posActual].valor]

                    operacionCola.append(Token(TT_CHAR, valorId))
                else:
                    print('error')

        resultado = operacionCola.pop().valor

        return resultado
