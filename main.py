from jflap.Afd import Afd
from sys import stderr
from automatons.minimize import minimize

if __name__ == '__main__':
    leer = True
    while leer:
        leer = False
        path = input('Introduzca un autómata:')
        if path == '':
            print('No se debe introducir una ruta vacía.')
            exit()
        try:
            automaton = Afd(path)
        except FileNotFoundError:
            print('Me temo que la ruta está mal.', file=stderr)
            leer = True
        except Exception as error:
            print('Problema analizando el fichero: ', error, file=stderr)
    minimize(automaton)
