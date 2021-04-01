import sys


def test():
    sys.exit()


def getCompilerId(linea):
    '''
            Revisa si en la linea contiene la palabra reservada COMPILER
            y extrae el identificador
    '''
    if (linea[:linea.find(" ")] == "COMPILER" and len(linea[linea.find(" "):]) > 0):
        print(f'''
			COMPILER
			ident = {linea[linea.find(" "):]}
		''')
    else:
        print("ERROR")


path = './test.atg'
file = open(path, 'r')
listaOriginal = file.readlines()

listaLimpia = []

# Se eliminan los \n y multiples espacios en blanco
for element in listaOriginal:
    if element.strip() != '':
        listaLimpia.append(" ".join(element.strip().split()))

getCompilerId(listaLimpia.pop(0))

print(listaLimpia.pop(0))
