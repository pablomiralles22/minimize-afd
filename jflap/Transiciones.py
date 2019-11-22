'''
Created on 11 may. 2018

@author: Adri
'''

class Transiciones(object):
    '''
    Clase que contiene las transiciones de cada estado
    
    Atributos privados
    ------------------
    transiciones: dict
        Diccionario con las transiciones de salida desde el estado
        La clave es el simbolo, y el valor es el identificador del estado destino
        
    Metodos publicos
    ----------------
    addTransicion(simbolo,estado)
        Inserta una entrada en el diccionario transiciones
        
    mostrarTransicion()
        Imprime por salida estandar el contenido del diccionario
        
    gestEstado(simbolo): str
        Devuelve el estado asociado a la clave simbolo

    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.transiciones = dict()
        
    def addTransicion(self, simbolo, estado):
        '''
        Inserta una asociacion simbolo-estado para representar una transicion de salida
        
        Parametros
        ----------
        simbolo: str
            Cadena de un caracter que contiene el simbolo que etiqueta la transicion
        estado: str
            Cadena con el identificador del estado al que llega la transicion
        '''
        
        self.transiciones[simbolo] = estado
        
    def mostrarTransicion (self):
        '''
        Imprime por salida estandar el contenido del diccionario
        '''
        
        print(self.transiciones)
        
    def getEstado (self, simbolo):
        '''
        Recupera el estado asociado a la clave simbolo
        
        Parametros
        ----------
        simbolo: str
            Simbolo que etiqueta la transicion y es clave en el diccionario
        '''
        
        return self.transiciones[simbolo]
    