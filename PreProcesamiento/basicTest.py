import basic
from character import *
#test = ['2+5*3', '2+2+2+2+2', '(1+2)/(1+2)', '123 123 123 +', '1+', '1 + d']


def getTest(texto):
    result, error = basic.run(texto)

    if error:
        return str(error.asString())
    else:
        return str(result)


assert getTest([Character('a'), '|', Character('b'), '|', Character(
    'c')]) == "(({'a'}|{'b'})|{'c'})", "debería crear paréntesis"

print()

#assert getTest('(2|5)6') == '((2|5).6)', "debería crear concatenacion"
'''
assert getTest('2+5*3') == '(2+(5*3))', "debería crear paréntesis"
assert getTest('2+2+2+2+2') == '((((2+2)+2)+2)+2)', "debería crear paréntesis"
assert getTest(
    '(1+2)/(1+2)') == '((1+2)/(1+2))', "solo crea paréntesis externos"

assert getTest(
    '123 123 123 +') == "Invalid Syntax: Expected '+', '-', '*' or '/'", "debería crear error de espera operador"

assert getTest(
    '1+') == 'Invalid Syntax: Expected int or float', "debería crear error de espera num"

'''

print("TODO BIEN!")


'''
while len(test) > 0:
    text = test.pop()
    print(text)
    result, error = basic.run(text)

    if error:
        print(error.asString())
    else:
        print(result)
    print()
'''
