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
    '''
    Se eliminan comentarios
     * de multiples lineas
     * de una sola linea
     * junto con codigo en la linea
    '''
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
    '''
        Valida que la linea contenga una seccion no consumida
    '''
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
    '''
        Identifica las secciones del .atg y las separa
        de forma recursiva
    '''
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

    # SEPARAR SECCIONES
    separarSets(seccionActualLista)

    siguienteSeccion = identificarSeccion(residuo.pop(0))
    if (siguienteSeccion != "END"):
        separarSeccion(siguienteSeccion, residuo)

    if (siguienteSeccion == "END"):
        print("IDENTIFICADO <END>")


def separarSets(sets):
    setsSeparados = []
    setTemportal = ""
    for element in sets:
        if (element[-1] == "."):
            if (len(setTemportal) == 0):
                setsSeparados.append(element)

            else:
                setsSeparados.append(setTemportal + element)
                setTemportal = ""

        else:
            setTemportal += element
    
    print(setsSeparados)


if __name__ == "__main__":

    # Limpieza de archivo .atg
    listaLimpia = eliminarEspacios(openFile('./test.atg'))

    listaLimpia = eliminarComentarios(listaLimpia)

    # Identificacion de informacion

    # Identificador de compilador
    getCompilerId(listaLimpia.pop(0))

    # Identificacion de secciones
    seccionInicial = identificarSeccion(listaLimpia.pop(0))
    separarSeccion(seccionInicial, listaLimpia)
