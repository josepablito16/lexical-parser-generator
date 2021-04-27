
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

    def __repr__(self):
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
