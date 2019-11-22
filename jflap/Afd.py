'''
Created on 11 may. 2018

@author: Adri
'''

import xml.etree.ElementTree as ET
import re

from jflap.Transiciones import Transiciones

class Afd(object):
    '''
    Clase Afd que es capaz de interpretar un fichero JFLAP y extraer la informacion
    para obtener los estados y transiciones de un automata
    
    Atributos privados
    ------------------
    root : ElementTree
        Raíz del arbol XML del fichero JFLAP
    automata : dict
        Transiciones del automata representadas en un diccionario
    nombreEstados : dict
        La clave es el identificador del estado y el valor es su nombre
    idEstados : dict
        El inverso del anterior: la clave es el nombre del estado y el valor es su identificador
    nestados : int
        Número de estados del automata
    estadoInicial : str
        Nombre del estado inicial
    estadosFinales : set
        Conjunto de identificadores de estados finales
    alfabeto : set
        Conjunto de caracteres que forman el alfabeto del automata
        
    Metodos publicos
    ----------------
    estadoSiguiente(estado, simbolo) : str
        Devuelve el estado al que se llega desde otro, con cierto simbolo. Usa nombres de estados
    esFinal(estado) : bool
        Comprueba si un estado es final
    esSimbolo(simbolo) : bool
        Comprueba si un simbolo esta en el alfabeto del automata
    getEstadoInicial() : str
        Devuelve el nombre del estado inicial
    getAlfabeto() : set
        Devuelve el alfabeto del autómata
    mostrarAfd()
        Imprime por salida estandar toda la informacion del automata
        
    Metodos privados
    ----------------
    analizadorV6() : int
        Analiza un fichero JFLAP version 6 (editor version 7). Devuelve 1 si ok, 0 si error
    analizadorV8() : int
        Analiza un fichero JFLAP version 8 (editor version 8beta). Devuelve 1 si ok, 0 si error
    traductorEstados (estado): str
        Devuelve el nombre del estado, dado su identificador
    traductorEstadosInverso (estado) : str
        Devuelve el identificador del estado, dado su nombre
    addNombreEstado(estado, nombre)
        Inserta un estado en el diccionario nombreEstados
    mostrarTransiciones(identificador)
        Imprime por salida estandar las transiciones de un estado en forma de diccionario
    '''

    def __init__(self, ruta, version=6):
        '''
        Inicializador del automata
        
        Parametros
        ----------
        ruta : str
            Localizacion del fichero JFLAP
        version : int
            Version del fichero. Puede ser 6 y 8
            
        Excepciones
        -----------
            Lanza Exception si la version no es correcta o falla el analisis
        '''
        
        self.root = ET.parse(ruta).getroot()
        self.automata = dict()
        self.nombreEstados = dict()
        self.idEstados = dict()
        self.nestados = 0
        self.ntransiciones = 0
        self.estadoInicial = None
        self.estadosFinales = set()
        self.alfabeto = set()
        if version == 6:
            if self.analizadorV6() == 0:
                raise Exception('El analisis version 6 no ha podido continuar')
        elif version == 8:
            if self.analizadorV8() == 0:
                raise Exception('El analisis version 8 no ha podido continuar')
        else:
            raise Exception('Esa version no esta soportada por el Lector')
        
    def analizadorV6 (self):
        '''
        Funcion que analiza un fichero JFLAP correspondiente a la version 8
        Devuelve un 0 si el analisis falla, o un 1 si se analiza bien
        '''
        
        #Para cada estado
        for nodo in self.root.iter('state'):
            #Buscamos un estado por su 'id'
            estado = nodo.attrib['id']
            #Para este estado inicializamos su tabla de transiciones
            self.automata[estado] = Transiciones()
            #Incluimos el nombre del estado al diccionario de nombres
            self.addNombreEstado(estado, nodo.attrib['name'])
            self.idEstados[nodo.attrib['name']] = estado
            #Incrementamos el numero de estados de nuestro Automata
            self.nestados += 1
            #Comprobamos si es un estado inicial o final
            if nodo.find('initial') != None:
                self.estadoInicial = estado
            if nodo.find('final') != None:
                self.estadosFinales.add(self.traductorEstados(estado))
        #Para cada transicion
        for nodo in self.root.iter('transition'):
            #Buscamos la informarcion desde el estado que parte
            desdeEstado = nodo.find('./from').text
            #Al estado que va
            aEstado = nodo.find('./to').text
            #Con que simbolo realiza la transicion
            conSimbolo = nodo.find('./read').text
            aux = self.automata[desdeEstado]
            #Comprobamos si la transicion se realiza con lambda
            if conSimbolo == None:
                print('El automata que desea analizar no es determinista (AFND)')
                #devolvemos el valor de 0 dado que no podemos analizar AFND
                return 0
            #Insertamos una transicion en nuestro objeto
            aux.addTransicion(conSimbolo, aEstado)
            self.alfabeto.add(conSimbolo)
            #Incrementamos el numero de transiciones
            self.ntransiciones += 1
        #Devolvemos el valor de que la funcion ha conseguido crear el automata satisfactoriamente
        return 1
    
    def analizadorV8 (self):
        '''
        Funcion que analiza un fichero JFLAP correspondiente a la version 8
        Devuelve un 0 si el analisis falla, o un 1 si se analiza bien
        '''
    
        #Primero extraer los estados
        nodo = self.root.find(".//structure[@type='state_set']")
        for hijo in nodo.iter('state'):
            estado = hijo.find('id').text
            nombre = hijo.find('name').text
            self.idEstados[nombre] = estado
            #Para este estado inicializamos su tabla de transiciones
            self.automata[estado] = Transiciones()
            #Incluimos el nombre del estado al diccionario de nombres
            self.addNombreEstado(estado, nombre)
            #Incrementamos el numero de estados de nuestro Automata
            self.nestados += 1
        #Para cada estado
        for nodo in self.root.iter('structure'):
            tipo = nodo.attrib['type']
            #Insertar estados finales
            if tipo == "final_states":
                self.estadosFinales.add(nodo.find('.//name').text)
            #Insertar transiciones
            elif tipo == "transition_set":
                for hijo in nodo.iter('fsa_trans'):
                    desdeEstado = hijo.find('./from/id').text
                    aEstado = hijo.find('./to/id').text
                    conSimbolo = hijo.find('./input').text
                    if conSimbolo == None:
                        print('El automata que desea analizar no es determinista (AFND)')
                        #devolvemos el valor de 0 dado que no podemos analizar AFND
                        return 0
                    aux = self.automata[desdeEstado]
                    aux.addTransicion(conSimbolo, aEstado)
                    self.ntransiciones += 1
            #Extraer el alfabeto del automata
            elif tipo == "input_alph":
                for hijo in nodo.iter('symbol'):
                    simbolo = hijo.text
                    self.alfabeto.add(simbolo)
            #Detectar estado inicial
            elif tipo == "start_state":
                self.estadoInicial = nodo.find('*/id').text
        #Devolver el codigo de que la funcion ha realizado el analisis correctamente
        return 1

    def traductorEstados (self, estado):
        '''
        Dado el identificador de un estado, devuelve su nombre
        JFLAP usa como identificador una cadena con un entero unico.
        El nombre puede ser qX, donde X es un numero, o lo que edite el usuario de JFLAP.
        
        Parametros
        ----------
        estado: str
            Identificador del estado
        '''
        
        try:
            return self.nombreEstados[estado]
        except:
            #print('Esta intentando traducir un estado incorrecto: ', estado)
            return None
        
    def traductorEstadosInverso (self, estado):
        '''
        Dado un nombre de estado, devuelve su identificador
        
        Parametros
        ----------
        estado: str
            Nombre del estado
        '''
        
        try:
            return self.idEstados[estado]
        except:
            #print('Esta intentando traducir un estado incorrecto: ', estado)
            return None
        
    def estadoSiguiente (self, estado, simbolo):
        '''
        Dado un estado (nombre) y un simbolo, devuelve el estado siguiente (nombre) al que se llega
        
        Parametros
        ----------
        estado: str
            Nombre del estado
        simbolo: str
            Simbolo que etiqueta la transicion
        '''
        
        try:
            aux = self.automata[self.traductorEstadosInverso(estado)]
            return self.traductorEstados(aux.getEstado(simbolo))
        except:
            return None
        
    def addNombreEstado (self, estado, nombre):
        '''
        Inserta en el diccionario un nombre de estado si no esta repetido
        
        Parametros
        ----------
        estado: str
            Identificador del estado
        nombre: str
            Nombre del estado
        '''
        
        if nombre in self.nombreEstados.values() or re.match('\d+', nombre):
            raise Exception('El nombre del estado esta duplicado o esta formado solo por digitos: ', estado, ' -> ', nombre)
        else:
            self.nombreEstados[estado] = nombre
            
    def esFinal(self, estado):
        '''
        Devuelve True si el estado es final y False en caso contrario
        
        Parametros
        ----------
        estado: str
            Nombre del estado
        '''
        
        return estado in self.estadosFinales 
    
    def esSimbolo(self, simbolo):
        '''
        Devuelve True si el simbolo esta en el alfabeto
        
        Parametros
        ----------
        simbolo: str
            Cadena con un caracter que es el simbolo que se quiere comprobar
        '''
        
        return simbolo in self.alfabeto
    
    def getEstadoInicial (self):
        '''
        Devuelve el estado inicial del automata
        '''
        
        return self.traductorEstados(self.estadoInicial)
    
    def getAlfabeto (self):
        '''
        Devuelve el alfabeto del automata
        '''
        
        return self.alfabeto
    
    def mostrarTransiciones(self,i):
        '''
        Muestra las transiciones del estado i en forma de diccionario donde la clave es el simbolo
        y el valor el estado al que se llega
        
        Parametros
        ----------
        i: str
            Identificador del estado
        '''
        
        trans = self.automata[i].transiciones
        simbolos = trans.keys()
        linea = '{'
        for s in simbolos:
            linea += "'%s' : '%s', " % (s,self.traductorEstados(trans[s]))
        linea = linea[:len(linea)-2]
        print(linea,'}')
        
    def mostrarAfd (self):
        '''
        Muestra por salida estandar toda la informacion del automata
        '''
        
        print("Número de estados:", self.nestados)
        print("Número de transiciones:", self.ntransiciones)
        print("El estado inicial es: '%s'" % self.estadoInicial)
        print("Los estados finales son:", list(self.estadosFinales))
        print("El alfabeto del autómata es: ", list(self.alfabeto))
        for i in self.automata:
            print("El estado '%s' tiene estas transiciones:" % self.traductorEstados(i))
            self.mostrarTransiciones(i)
        print("______________________________________________")