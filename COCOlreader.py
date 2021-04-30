import sys
from character import *
from characterPreprocess import *
from tokenObj import *
import copy
import basic

#+++++++++ Directo
from Arbol import *
import Directo as d

import pickle


secciones = ['CHARACTERS', 'KEYWORDS', 'TOKENS', 'PRODUCTIONS']
seccionesConsumidas = []
expresionesChar = {}
expresionesTokens = {}
diccionarioTokens = {}
idDiccionarioTokens = 0

TT_HASHTAG = 'HASHTAG'
TT_CONCAT = 'CONCAT'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
TT_OR = 'OR'


def getCompilerId(linea):
    '''
                    Revisa si en la linea contiene la palabra reservada COMPILER
                    y extrae el identificador
    '''
    if (linea[:linea.find(" ")] == "COMPILER" and len(linea[linea.find(" "):]) > 0):
        """
        print(f'''
                        IDENTIFICADO <COMPILER>
                        ident = {linea[linea.find(" "):]}
                ''')
        """
        return str(linea[linea.find(" "):]).strip()
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
        """
        print(f'''
                        IDENTIFICADO <{linea.strip()}>
                ''')
        """
        seccionesConsumidas.append(linea.strip())
        return linea.strip()

    if linea.strip()[0:3] == "END":
        return "END"

    print("ERROR")


def procesarChar(seccion):
    # print("CHAAAAAR")
    # print()
    errorControl = False

    expresionesTratadas = {}

    for i in seccion:
        igual = i.find("=")
        punto = i.find(".")

        key = i[:igual].strip()
        item = i[igual + 1:punto].strip()
        #########################
        # se crea un objeto characterProcess
        preProcess = CharacterPreprocess(item)

        # se crean los tokens
        preProcess.splitString()

        # se opera para tener solo un set final
        resultadoFinal, errores = preProcess.operar(
            copy.deepcopy(expresionesTratadas))

        if len(errores) > 0:
            errorControl = True
            for error in errores:
                print()
                print(i)
                print(error)

        # Se guarda el resultado en el diccionario

        expresionesTratadas[key] = copy.deepcopy(resultadoFinal)

        ####################

    # print(expresionesTratadas)
    # print()
    if (errorControl):
        sys.exit()
    return expresionesTratadas


def crearListaExpresion(expresion, chars):

    separador = ['{', '}', '|', ' ', '[', ']']
    if (expresion.find("EXCEPT") != -1):
        expresion = expresion[:expresion.find("EXCEPT")].strip()
    # print(expresion)
    listaExpresion = []
    temp = ""
    isCharacter = False
    for i in expresion:
        if i == '"':
            if not isCharacter:
                isCharacter = True
            if isCharacter:
                for item in temp:
                    listaExpresion.append(Character(item))
                isCharacter = False
                temp = ""
            continue
        if isCharacter:
            temp += i
        elif i not in separador:
            temp += i
        elif i in separador:
            if len(temp) > 0:
                listaExpresion.append(temp)
            temp = ""
            if i != " ":
                listaExpresion.append(i)

    # merge de tokens con sets creados en CHARACTERS
    for i in range(len(listaExpresion)):
        if(isinstance(listaExpresion[i], str) and listaExpresion[i] not in separador):
            listaExpresion[i] = chars[listaExpresion[i]]

    # preprocesamiento tokens
    result, error = basic.run(listaExpresion)

    if error:
        print(str(error.asString()))

    else:
        return result


def procesarKeyWords(seccion):
    # print("KEYWORDSSSSSSSSSSSSSSSSSSSSSS")
    # print()
    global diccionarioTokens
    global idDiccionarioTokens

    expresionesTratadas = {}
    for i in seccion:
        igual = i.find("=")
        punto = i.find(".")

        key = i[:igual].strip()
        item = i[igual + 2: punto - 1].strip()
        item = item.replace('"', '')

        diccionarioTokens[idDiccionarioTokens] = key
        idDiccionarioTokens += 1
        # print(key)
        # print(item)
        listaExpresion = []
        for letra in item:
            listaExpresion.append(Character(letra))

        result, error = basic.run(listaExpresion)

        if error:
            print(str(error.asString()))
        else:
            expresionesTratadas[key] = result
            # print(str(result))

    # print(expresionesTratadas)
    return expresionesTratadas


def procesarTokens(seccion, chars, tokens):
    # print("TOKENSSSSSSSSSSSSSSSSSSSSSS")
    # print()

    global diccionarioTokens
    global idDiccionarioTokens

    expresionesTratadas = {}
    for i in seccion:
        igual = i.find("=")
        punto = i.find(".")

        key = i[:igual].strip()
        item = i[igual + 1: punto].strip()

        diccionarioTokens[idDiccionarioTokens] = key
        idDiccionarioTokens += 1

        # print(key)
        # print(item)
        tokens[key] = crearListaExpresion(item, chars)


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

    # SEPARAR SECCIONES
    separarSets(seccionActualLista, seccionActual)

    siguienteSeccion = identificarSeccion(residuo.pop(0))
    if (siguienteSeccion != "END"):
        separarSeccion(siguienteSeccion, residuo)

    if (siguienteSeccion == "END"):
        #print("IDENTIFICADO <END>")
        pass


def separarSets(sets, seccion):
    global expresionesChar
    global expresionesTokens

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
    """
    print(f'''
        {seccion}
        seccionActualLista = {setsSeparados}
    ''')
    """

    if (seccion == "CHARACTERS"):
        expresionesChar = procesarChar(setsSeparados)
        #print("char retorna")
        # print(expresionesChar)

    elif (seccion == "KEYWORDS"):
        expresionesTokens = procesarKeyWords(setsSeparados)

    elif (seccion == "TOKENS"):
        #print("en tokens entraaa")
        # print(expresionesChar)
        procesarTokens(setsSeparados, expresionesChar, expresionesTokens)


def getHashTagId(nombre):
    global diccionarioTokens
    for key, value in diccionarioTokens.items():
        if (nombre == value):
            return key


def crearOrGeneral():
    global expresionesTokens

    elementos = list(expresionesTokens.values())

    temp = []
    temp.append(Token(TT_LPAREN))
    temp += elementos[0]
    temp.append(Token(TT_OR))
    temp += elementos[1]
    temp.append(Token(TT_RPAREN))

    for i in range(2, len(elementos)):
        temp2 = temp.copy()
        temp = []
        temp.append(Token(TT_LPAREN))
        temp += temp2
        temp.append(Token(TT_OR))
        temp += elementos[i]
        temp.append(Token(TT_RPAREN))

    return temp


if __name__ == "__main__":

    if (len(sys.argv) == 2):
        nombreAtg = sys.argv[1]
    else:
        print("Por favor, ingrese el nombre de la definicion del scanner")
        sys.exit()
    # Limpieza de archivo .atg
    listaLimpia = eliminarEspacios(openFile(nombreAtg))

    listaLimpia = eliminarComentarios(listaLimpia)

    # Identificacion de informacion

    # Identificador de compilador
    nombreCompiler = getCompilerId(listaLimpia.pop(0))

    # Identificacion de secciones
    seccionInicial = identificarSeccion(listaLimpia.pop(0))
    separarSeccion(seccionInicial, listaLimpia)

    # print(expresionesTokens)

    # AUMENTAR EXPPRESIONES
    # print(diccionarioTokens)
    # print("============")
    for key, value in expresionesTokens.items():
        expresionesTokens[key] = [Token(TT_LPAREN)]+value+[Token(
            TT_CONCAT), Token(TT_HASHTAG, getHashTagId(key)), Token(TT_RPAREN)]

    # print(expresionesTokens)
    expresionFinal = crearOrGeneral()

    print("ExpresionFinal")
    print(expresionFinal)

    # Algoritmo directo
    a = Arbol()
    '''
    root = a.armarArbol(expresionFinal)
    a.postOrder(root)
    print(root)
    '''
    DFA_directo, estadosHash, nodosHoja = d.construirFuncionesBasicas(
        a.armarArbol(expresionFinal))

    # se guardan los objetos auxiliares del scanner
    pickle.dump(DFA_directo, open('DFA_directo', 'wb'))
    pickle.dump(diccionarioTokens, open('diccionarioTokens', 'wb'))
    pickle.dump(estadosHash, open('estadosHash', 'wb'))
    pickle.dump(nodosHoja, open('nodosHoja', 'wb'))

    # se genera el scanner
    f = open(f"scanner{nombreCompiler}.py", "w", encoding='utf8')
    f.write(
        '''
# Scanner generado por proyecto Jose Cifuentes
# Universidad del Valle de Guatemala
import pickle
import copy
import sys


class NodoDirecto(object):
    """
    Este objeto guarda toda la informacion de un nodo
    especificamente para el algoritmo directo

    Variable
    ----------
    relaciones : list
        guarda una lista de objetos relacion del nodo
    estadoFinal : Bool
        es estado final?
    estadoInicial : Bool
        es estado inicial?
    estados : lsit
        ids de todos los estados que representa el nodo
    """

    def __init__(self, estados, estadoInicial=False):
        self.relaciones = []
        self.estadoFinal = False
        self.estadoInicial = estadoInicial
        self.estados = estados  # es lista

    def agregarRelacion(self, nuevaRelacion):
        self.relaciones.append(nuevaRelacion)

    def isEstadoFinal(self):
        return self.estadoFinal

    def isEstadoInicial(self):
        return self.estadoInicial

    def setEstadoFinal(self):
        self.estadoFinal = True

    def getRelacionesObjeto(self):
        return self.relaciones

    def getRelaciones(self):
        relacionesList = []
        for relacion in self.relaciones:
            relacionesList.append(relacion.getRelacion())
        return relacionesList

    def getEstados(self):
        return self.estados


class RelacionDirecto(object):
    """
    Este objeto guarda toda la informacion de una relacion
    especificamente para el algoritmo directo

    Variable
    ----------
    idNodo1 : int
        id del nodo que posee la relacion
    nombreRelacion : str
        texto de la transicion de la relacion
    idNodo2 : int
        id del nodo a que se llega con la relacion
    """

    def __init__(self, idNodo1, nombreRelacion, idNodo2):
        self.idNodo1 = idNodo1
        self.nombreRelacion = nombreRelacion
        self.idNodo2 = idNodo2

    def getRelacion(self):
        return [self.idNodo1, self.idNodo2, self.nombreRelacion]

    def actualizarRelacion(self, diccionarioId):
        try:
            self.idNodo1 = diccionarioId[self.idNodo1]
            self.idNodo2 = diccionarioId[self.idNodo2]
        except:
            pass


# Funciones complementarias
def getLetraDeEstados(DFA, estados):
    """
    Retorna la letra que le corresponde a un estado
    """
    for letra, nodo in DFA.items():
        if(
            list(set(nodo.getEstados()) - set(estados))
            ==
            list(set(estados) - set(nodo.getEstados()))
            ==
            []
        ):
            return letra


def getEstadosFinales(DFA):
    estadosFinales = []
    for id, nodo in DFA.items():
        if (nodo.isEstadoFinal()):
            estadosFinales.append(id)

    return estadosFinales


def getEstadosIniciales(DFA):
    estadosFinales = []
    for id, nodo in DFA.items():
        if (nodo.isEstadoInicial()):
            estadosFinales.append(id)

    return estadosFinales


def getRelacionesDFA(DFA):
    relaciones = []
    for id, nodo in DFA.items():
        relaciones.append(nodo.getRelaciones())
    return relaciones


def setEstadosFinales(DFA, estadosHash):
    """
    Dado un DFA pone todos los nodos estado final
    que contengan un id dado []
    """

    for id, nodo in DFA.items():

        for idHash in estadosHash:
            if (idHash in nodo.getEstados()):
                nodo.setEstadoFinal()
    return DFA


def getNombreToken(estadosFinales, diccionarioTokens, estadosHash, nodosHoja):

    estadosFinales = list(set(estadosHash).intersection(set(estadosFinales)))
    idToken = None
    for key, value in nodosHoja.items():
        for i in estadosFinales:
            if i in value:
                idToken = key
                token = diccionarioTokens[int(key[key.find('G') + 1:])]
                return token


def mover(estado, letra):
    """
    Funcion mover utilizado para la simulacion
    """
    try:
        for i in estado.getRelaciones():

            if (letra in i[2]):
                return i[1]
    except:
        return []

    return []


def simularDirecto(DFA, cadena, diccionarioTokens):
    """
    Simula DFA dada una cadena
    """

    s = getEstadosIniciales(DFA)[0]

    for i in cadena:

        if (s == []):
            break
        s = mover(DFA[s], i)

    # Si la interseccion de S y los estados finales no es vacia
    # Entonces se acepta la cadena
    if (list(set.intersection(set(s), set(getEstadosFinales(DFA)))) != []):
        token = getNombreToken(DFA[s].estados, diccionarioTokens,
                               estadosHash, nodosHoja)
        return f"Cadena: {cadena} es token: {token}"
    else:
        return f"Cadena: {cadena} no identificado"


try:
    # Intentamos abrir los archivos auxiliares del scanner
    DFA_directo = pickle.load(open('DFA_directo', 'rb'))
    diccionarioTokens = pickle.load(open('diccionarioTokens', 'rb'))
    estadosHash = pickle.load(open('estadosHash', 'rb'))
    nodosHoja = pickle.load(open('nodosHoja', 'rb'))
except:
    print("No fue posible abrir los archivos auxiliares del scanner")

if (len(sys.argv) == 2):
    # si tenemos el argumento del nombre del .txt
    try:
        with open(sys.argv[1]) as f:
            lines = f.readlines()

            for linea in lines:
                print(simularDirecto(DFA_directo, linea.strip(), diccionarioTokens))
    except:
        print("No fue posible abrir el archivo")


else:
    print("Por favor, ingrese el nombre del archivo que quiere escanear")

        '''
    )

    f.close()

    # print(DFA_directo)
    print(f"""
    Simulacion DFA = {d.simularDirecto(DFA_directo, "1234",diccionarioTokens)}
    """)
