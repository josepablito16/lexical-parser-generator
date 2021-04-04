import sys

secciones = ['CHARACTERS', 'KEYWORDS', 'TOKENS', 'PRODUCTIONS']


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
			IDENTIFICADO <COMPILER>
			ident = {linea[linea.find(" "):]}
		''')
    else:
        print("ERROR")


def getCharactersVerificacion(linea):
    if linea.strip() == "CHARACTERS":
        print('''
			IDENTIFICADO <CHARACTERS>
		''')
    else:
        print("ERROR")


def getKeyWordsVerificacion(linea):
    if linea.strip() == "KEYWORDS":
        print('''
			IDENTIFICADO <KEYWORDS>
		''')
    else:
        print("ERROR")


def getTokensVerificacion(linea):
    if linea.strip() == "TOKENS":
        print('''
			IDENTIFICADO <TOKENS>
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

    return listaSinComentarios


def getCharactersSeccion(lista):
    nuevaLista = []
    characters = []
    for i in range(len(lista)):
        if (lista[i].strip() in secciones):
            nuevaLista = lista[i:]
            break
        characters.append(lista[i])

    print(f'''
        characters = {characters}

        resto = {nuevaLista}
    ''')

    return nuevaLista


def getKeyWordsSeccion(lista):
    nuevaLista = []
    keywords = []
    for i in range(len(lista)):
        if (lista[i].strip() in secciones):
            nuevaLista = lista[i:]
            break
        keywords.append(lista[i])

    print(f'''
        keywords = {keywords}

        resto = {nuevaLista}
    ''')

    return nuevaLista


def getTokensSeccion(lista):
    nuevaLista = []
    tokens = []
    for i in range(len(lista)):
        if (lista[i].strip() in secciones or lista[i].strip()[0:3] == "END"):
            nuevaLista = lista[i:]
            break
        tokens.append(lista[i])

    print(f'''
        tokens = {tokens}

        resto = {nuevaLista}
    ''')

    return nuevaLista


if __name__ == "__main__":

    # Limpieza de archivo .atg

    listaLimpia = eliminarEspacios(openFile('./test.atg'))

    listaLimpia = eliminarComentarios(listaLimpia)
    # print(listaLimpia)

    # Identificacion de informacion

    # Identificador de compilador
    getCompilerId(listaLimpia.pop(0))

    # Characters
    getCharactersVerificacion(listaLimpia.pop(0))
    listaLimpia = getCharactersSeccion(listaLimpia)

    # KeyWords
    getKeyWordsVerificacion(listaLimpia.pop(0))
    listaLimpia = getKeyWordsSeccion(listaLimpia)

    # Tokens
    getTokensVerificacion(listaLimpia.pop(0))
    getTokensSeccion(listaLimpia)

    # print(listaLimpia)

    # print(listaLimpia.pop(0))
