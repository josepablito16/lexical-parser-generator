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

expresiones = ['"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"+hola',
               '"0123456789"', 'digit+"ABCDEF"']


for i in expresiones:
    pre1 = CharacterPreprocess(i)
    pre1.splitString()
