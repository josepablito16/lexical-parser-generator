import sys


def test():
    '''
    Finaliza la ejecucion del programa
    '''
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


def openFile(path):
    '''
    Abre el archivo y retorna una lista con su
    contenido
    '''
    file = open(path, 'r')
    return file.readlines()


def eliminarEspacios(listaSucia):
    '''
    Se eliminan los \n y multiples espacios en blanco
    '''
    listaLimpia = []

    for element in listaSucia:
        if element.strip() != '':
            listaLimpia.append(" ".join(element.strip().split()))

    return listaLimpia


def eliminarComentarios(lineas):
    listaSinComentarios = []
    comentarioAbierto = False

    for linea in lineas:
        print(f'''

            DEBUG
            linea = {linea}
            comentarioAbierto = {comentarioAbierto}

        ''')
        if (linea.find('.)') != -1 and comentarioAbierto):
            comentarioAbierto = False
            continue

        if (comentarioAbierto):
            continue

        if (linea.find('(.') != -1):

            if (linea.find('.)') == -1):
                # No termina el comentario en esa linea
                comentarioAbierto = True
            else:
                if (len(linea[:linea.find('(.')]) > 0):
                    listaSinComentarios.append(linea[:linea.find('(.')])
        else:
            listaSinComentarios.append(linea)

    print(listaSinComentarios)


if __name__ == "__main__":

    listaLimpia = eliminarEspacios(openFile('./test.atg'))

    eliminarComentarios(listaLimpia)

    # getCompilerId(listaLimpia.pop(0))

    # print(listaLimpia.pop(0))
