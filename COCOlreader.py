import sys
from character import *
from characterPreprocess import *
from tokenObj import *
import copy
import basic

#+++++++++ Directo
from Arbol import *
import Directo as d

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


def procesarChar(seccion):
    print("CHAAAAAR")
    print()

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
            for error in errores:
                print(error)

        # Se guarda el resultado en el diccionario
        '''
        print(f'''
        {key}
        {item}
        {resultadoFinal}
        ''')
        '''
        expresionesTratadas[key] = copy.deepcopy(resultadoFinal)

        ####################

    print(expresionesTratadas)
    print()
    return expresionesTratadas


def crearListaExpresion(expresion, chars):

    separador = ['{', '}', '|', ' ', '[', ']']
    if (expresion.find("EXCEPT") != -1):
        expresion = expresion[:expresion.find("EXCEPT")].strip()
    print(expresion)
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
    print("KEYWORDSSSSSSSSSSSSSSSSSSSSSS")
    print()
    global diccionarioTokens
    global idDiccionarioTokens

    expresionesTratadas = {}
    for i in seccion:
        igual = i.find("=")
        punto = i.find(".")

        key = i[:igual].strip()
        item = i[igual + 2: punto - 1].strip()

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
            print(str(result))

    print(expresionesTratadas)
    return expresionesTratadas


def procesarTokens(seccion, chars, tokens):
    print("TOKENSSSSSSSSSSSSSSSSSSSSSS")
    print()

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

        print(key)
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
        print("IDENTIFICADO <END>")


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

    print(f'''
        {seccion}
        seccionActualLista = {setsSeparados}
    ''')

    if (seccion == "CHARACTERS"):
        expresionesChar = procesarChar(setsSeparados)
        print("char retorna")
        print(expresionesChar)

    elif (seccion == "KEYWORDS"):
        expresionesTokens = procesarKeyWords(setsSeparados)

    elif (seccion == "TOKENS"):
        print("en tokens entraaa")
        print(expresionesChar)
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

    # Limpieza de archivo .atg
    listaLimpia = eliminarEspacios(openFile('./test.atg'))

    listaLimpia = eliminarComentarios(listaLimpia)

    # Identificacion de informacion

    # Identificador de compilador
    getCompilerId(listaLimpia.pop(0))

    # Identificacion de secciones
    seccionInicial = identificarSeccion(listaLimpia.pop(0))
    separarSeccion(seccionInicial, listaLimpia)

    # print(expresionesTokens)

    # AUMENTAR EXPPRESIONES
    print(diccionarioTokens)
    print("============")
    for key, value in expresionesTokens.items():
        expresionesTokens[key] = [Token(TT_LPAREN)]+value+[Token(
            TT_CONCAT), Token(TT_HASHTAG, getHashTagId(key)), Token(TT_RPAREN)]

    # print(expresionesTokens)
    expresionFinal = crearOrGeneral()

    # print(expresionFinal)

    # Algoritmo directo
    a = Arbol()
    '''
    root = a.armarArbol(expresionFinal)
    a.postOrder(root)
    print(root)
    '''

    DFA_directo = d.construirFuncionesBasicas(a.armarArbol(expresionFinal))
    print(DFA_directo)
    print(f"""
    Simulacion DFA = {d.simularDirecto(DFA_directo, "if",diccionarioTokens)}
    """)
