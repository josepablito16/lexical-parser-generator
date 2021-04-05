import sys

secciones = ['CHARACTERS', 'KEYWORDS', 'TOKENS', 'PRODUCTIONS']
seccionesConsumidas = []


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


def identificarSeccion(linea):
    if (linea.strip() in secciones and linea.strip() not in seccionesConsumidas):
        print(f'''
			IDENTIFICADO <{linea.strip()}>
		''')
        seccionesConsumidas.append(linea.strip())
        return linea.strip()

    if linea.strip()[0:3] == "END":
        return "END"

    print("ERROR")


def separarSeccion(seccionActual, lista):
    residuo = []
    seccionActualLista = []
    for i in range(len(lista)):
        if (lista[i].strip() in secciones or lista[i].strip()[0:3] == "END"):
            residuo = lista[i:]
            break
        seccionActualLista.append(lista[i])

    print(f'''
        {seccionActual}
        seccionActualLista = {seccionActualLista}
    ''')

    siguienteSeccion = identificarSeccion(residuo.pop(0))
    if (siguienteSeccion != "END"):
        separarSeccion(siguienteSeccion, residuo)

    if (siguienteSeccion == "END"):
        print("IDENTIFICADO <END>")


if __name__ == "__main__":

    # Limpieza de archivo .atg

    listaLimpia = eliminarEspacios(openFile('./test.atg'))

    listaLimpia = eliminarComentarios(listaLimpia)
    # print(listaLimpia)

    # Identificacion de informacion

    # Identificador de compilador
    getCompilerId(listaLimpia.pop(0))

    # Characters
    seccionInicial = identificarSeccion(listaLimpia.pop(0))
    separarSeccion(seccionInicial, listaLimpia)
