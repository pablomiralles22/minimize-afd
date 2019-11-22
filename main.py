from jflap.Afd import Afd
from sys import stderr
from automatons.minimize import minimize

if __name__ == '__main__':
    path = r'./pruebas/proResuelto-minimizar.jff'
    try:
        automaton = Afd(path)
    except FileNotFoundError:
        print('Me temo que la ruta está mal', file=stderr)
    except Exception as error:
        print('Problema analizando el fichero: ', error, file=stderr)
    minimize(automaton)
