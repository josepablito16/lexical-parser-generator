#######################################
# CONSTANTES
#######################################

DIGITOS = list(map(chr, range(ord('0'), ord('9')+1))) + \
    ['.'] + list(map(chr, range(ord('a'), ord('z')+1)))

#######################################
# ERRORS
#######################################


class Error:
    '''
    Clase principal de error,
    nos sirve para imprimir un error en pantalla
    '''

    def __init__(self, error_name, details):
        self.error_name = error_name
        self.details = details

    def asString(self):
        return f"{self.error_name}: {self.details}"


class IllegalCharError(Error):
    '''
    Clase que hereda de la clase Error, especificamente para
    caracteres que nuestro programa no reconoce
    '''

    def __init__(self, details):
        super().__init__('Illegal Character', details)


class InvalidSyntaxError(Error):
    '''
    Clase que hereda de la clase Error, especificamente para
    caracteres que nuestro programa no reconoce
    '''

    def __init__(self, details):
        super().__init__('Invalid Syntax', details)


#######################################
# TOKENS
#######################################
# Constantes tokens tipos
TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_OR = 'OR'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
TT_EOF = 'EOF'

# equivalente de cada token pero en simbolos
diccionario = {
    'PLUS': '+',
    'MINUS': '-',
    'MUL': '*',
    'DIV': '/',
    'OR': '|'
}


class Token:
    '''
    Objeto que guarda el tipo y valor de cada token
    '''

    def __init__(self, tipo, valor=None):
        self.tipo = tipo
        self.valor = valor

    def __repr__(self):
        if self.valor:
            return f'{self.tipo}:{self.valor}'
        return f'{self.tipo}'


#######################################
# LEXER
#######################################

class Lexer:
    '''
    Encargado de asignar tokens a cada conjunto
    de caracteres identificado, caso contrario
    error
    '''

    def __init__(self, textoPlano):
        self.textoPlano = textoPlano
        self.pos = -1
        self.charActual = None
        self.avanzar()

    def avanzar(self):
        '''
        Avanza una posicion en el textoPlano si no ha llegado al
        final del texto, caso contrario None
        '''
        self.pos += 1
        if self.pos < len(self.textoPlano):
            self.charActual = self.textoPlano[self.pos]
        else:
            self.charActual = None

    def crearTokens(self):
        '''
        Crea una lista de tokens
        '''
        tokens = []

        # Mientras no haya llegado al final
        while self.charActual != None:
            # si es un espacio o tab solo avanza
            if self.charActual in ' \t':
                self.avanzar()

                '''
                sino intenta reconocer el token y lo
                agrega a la lista tokens
                '''
            elif self.charActual in DIGITOS:
                tokens.append(self.crearNumero())
            elif self.charActual == '+':
                tokens.append(Token(TT_PLUS))
                self.avanzar()
            elif self.charActual == '-':
                tokens.append(Token(TT_MINUS))
                self.avanzar()
            elif self.charActual == '|':
                tokens.append(Token(TT_OR))
                self.avanzar()
            elif self.charActual == '*':
                tokens.append(Token(TT_MUL))
                self.avanzar()
            elif self.charActual == '/':
                tokens.append(Token(TT_DIV))
                self.avanzar()
            elif self.charActual == '(':
                tokens.append(Token(TT_LPAREN))
                self.avanzar()
            elif self.charActual == ')':
                tokens.append(Token(TT_RPAREN))
                self.avanzar()
            else:
                # Retorna error si no reconoce el caracter
                char = self.charActual
                self.avanzar()
                return [], IllegalCharError(f"'{char}'")

        # al final agrega el token de final
        tokens.append(Token(TT_EOF))
        return tokens, None

    def crearNumero(self):
        numContact = ''
        contadorPuntos = 0

        '''
        Mientras no haya llegado al final del texto plano
        y el char actual sea numero o punto
        '''
        while self.charActual != None and self.charActual in DIGITOS:

            # Cuenta los puntos
            if self.charActual == '.':
                # Si ya hay un punto para
                if contadorPuntos == 1:
                    break
                contadorPuntos += 1
                numContact += '.'
            else:
                numContact += self.charActual
            self.avanzar()

        # decide si es un numero int o float
        if contadorPuntos == 0:
            return Token(TT_INT, int(numContact))
        else:
            return Token(TT_FLOAT, float(numContact))

#######################################
# NODES
#######################################


class NodoNumero:
    '''
    Nodo que solo contiene un numero
    '''

    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f'{self.token.valor}'


class NodoBinario:
    '''
    Nodo que contiene <nodo izquierdo> <operador> <nodo derecho>
    '''

    def __init__(self, nodoIzquierdo, tokenOperacion, nodoDerecho):
        self.nodoIzquierdo = nodoIzquierdo
        self.tokenOperacion = tokenOperacion
        self.nodoDerecho = nodoDerecho

    def __repr__(self):
        return f"({self.nodoIzquierdo}{diccionario[self.tokenOperacion.tipo]}{self.nodoDerecho})"


#######################################
# PARSER DE RESULTADOS
#######################################

class ParseResultados:
    '''
    Lleva el control de errores o avances del parser
    '''

    def __init__(self):
        self.error = None
        self.nodo = None

    def registrar(self, res):
        '''
        Registra una operacion nueva del parser,
        actualiza errores de ser necesario
        '''
        if isinstance(res, ParseResultados):
            if res.error:
                self.error = res.error
            return res.nodo
        return res

    def success(self, nodo):
        '''
        Marca como exitoso una operacion del parser
        '''
        self.nodo = nodo
        return self

    def failure(self, error):
        '''
        Marca como fallida una operacion del parser
        '''
        self.error = error
        return self

#######################################
# PARSER
#######################################


class Parser:
    '''
    Convierte una secuencia de tokens en una estructura
    de datos, crea parentesis donde sea necesario y retorna
    una cadena con los parentesis apropiados para armar el arbol
    '''

    def __init__(self, tokens):
        self.tokens = tokens
        self.tokenId = -1
        self.avanzar()

    def avanzar(self):
        '''
        Pasamo a la siguiente posicion si no hemos
        llegado al final
        '''
        self.tokenId += 1
        if self.tokenId < len(self.tokens):
            self.tokenActual = self.tokens[self.tokenId]
        return self.tokenActual

    def parse(self):
        res = self.expr()
        if not res.error and self.tokenActual.tipo != TT_EOF:
            return res.failure(InvalidSyntaxError("Expected '+', '-', '*' or '/'"))
        return res

    def factor(self):
        '''
        factor : INT | FLOAT
        '''
        res = ParseResultados()
        token = self.tokenActual

        if token.tipo in (TT_INT, TT_FLOAT):
            res.registrar(self.avanzar())
            return res.success(NodoNumero(token))

        elif token.tipo == TT_LPAREN:
            res.registrar(self.avanzar())
            expr = res.registrar(self.expr())
            if res.error:
                return res
            if self.tokenActual.tipo == TT_RPAREN:
                res.registrar(self.avanzar())
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    "Expected ')'"
                ))

        return res.failure(InvalidSyntaxError(
            "Expected int or float"
        ))

    def term(self):
        '''
        term : factor ((MUL | DIV) factor)*
        '''
        return self.bin_op(self.factor, (TT_MUL, TT_DIV))

    def expr(self):
        '''
        expr : term ((PLUS | MINUS) term)*
        '''
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS, TT_OR))

    def bin_op(self, func, ops):
        '''
        Codigo de term y expr
        Como se parecen tanto, se deja dinamico la funcion
        y los operadores que tienen que interpretar 
        '''
        res = ParseResultados()
        left = res.registrar(func())

        if res.error:
            return res

        while self.tokenActual.tipo in ops:
            tokenOperacion = self.tokenActual
            res.registrar(self.avanzar())
            right = res.registrar(func())
            if res.error:
                return res
            left = NodoBinario(left, tokenOperacion, right)

        return res.success(left)

#######################################
# RUN
#######################################


def run(textoPlano):
    '''
    Metodo principal que llama al lexer y al parser
    '''
    lexer = Lexer(textoPlano)
    tokens, error = lexer.crearTokens()
    if error:
        return None, error

    parser = Parser(tokens)
    ast = parser.parse()

    return ast.nodo, ast.error
