import pickle

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
    '''
    Retorna la letra que le corresponde a un estado
    '''
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
    '''
    Dado un DFA pone todos los nodos estado final
    que contengan un id dado []
    '''
    print("setEstadosFInales")
    for id, nodo in DFA.items():
        print(nodo.estados)
        for idHash in estadosHash:
            if (idHash in nodo.getEstados()):
                nodo.setEstadoFinal()
    return DFA


def getNombreToken(estadosFinales, diccionarioTokens, estadosHash, nodosHoja):
    print("\nEL TOKEN ES")
    print(estadosFinales)
    print(diccionarioTokens)
    print(estadosHash)
    estadosFinales = list(set(estadosHash).intersection(set(estadosFinales)))
    idToken = None
    for key, value in nodosHoja.items():
        for i in estadosFinales:
            if i in value:
                idToken = key
                token = diccionarioTokens[int(key[key.find('G') + 1:])]
                return token


def mover(estado, letra):
    '''
    Funcion mover utilizado para la simulacion
    '''
    try:
        for i in estado.getRelaciones():

            #print(f"Mover letra: {letra} set: {i[2]} = {letra in i[2] }")
            # print(type(i[2]))

            if (letra in i[2]):
                return i[1]
    except:
        return []

    return []





def simularDirecto(DFA, cadena, diccionarioTokens):
    '''
    Simula DFA dada una cadena
    '''

    s = getEstadosIniciales(DFA)[0]

    print()
    print("estados iniciales")
    print(s)
    print()

    sTemp = []
    for i in cadena:
        print(s)
        if (s == []):
            s = sTemp
            break
        s = mover(DFA[s], i)
        sTemp = s

    print("final")

    

    print("Estados finales")
    print(getEstadosFinales(DFA))

    # Si la interseccion de S y los estados finales no es vacia
    # Entonces se acepta la cadena
    if (list(set.intersection(set(s), set(getEstadosFinales(DFA)))) != []):
        token = getNombreToken(DFA[s].estados, diccionarioTokens,
                                  estadosHash, nodosHoja)
        return f"SI ES {token}"
    else:
        return "NO"

DFA_directo = pickle.load(open('DFA_directo', 'rb'))
diccionarioTokens = pickle.load(open('diccionarioTokens', 'rb'))
estadosHash = pickle.load(open('estadosHash', 'rb'))
nodosHoja = pickle.load(open('nodosHoja', 'rb'))

print(f"""
    Simulacion DFA = {simularDirecto(DFA_directo, "if",diccionarioTokens)}
    """)