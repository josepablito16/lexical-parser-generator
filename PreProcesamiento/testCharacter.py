from character import *
from characterPreprocess import *


def testUnion():
    char1 = Character("prueba")

    char1.union("union")
    assert char1.elementos == {'a', 'b', 'e', 'i', 'n',
                               'o', 'p', 'r', 'u'}, "debería ser 'pruebaunion'"


def testDiferencia():
    char1 = Character("123")

    char1.diferencia("hola12")
    assert char1.elementos == {'3'}, "debería ser 'pruebaunion'"


testUnion()
testDiferencia()

expresiones = {
    'letter': '"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"',
    'digit': '"0123456789"',
    'hexdigit': 'digit + "ABCDEFabcdef"'
}

for key, item in expresiones.items():

    # se crea un objeto characterProcess
    preProcess = CharacterPreprocess(item)

    # se crean los tokens
    preProcess.splitString()

    # se opera para tener solo un set final
    resultadoFinal = preProcess.operar()

    # Se guarda el resultado en el diccionario
    expresiones[key] = resultadoFinal
    break

print(expresiones)

'''
for i in expresiones:
    #pre1 = CharacterPreprocess(i)
    pre1 = CharacterPreprocess('"abc"+"123"+"def"')
    break
'''
