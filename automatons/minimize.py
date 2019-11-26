from .auxiliar_classes.complete_afd import CompleteAFD as CompleteAFD
from .auxiliar_classes.disjoint_set_union import StateDisjointSetUnion as StateDisjointSetUnion
from .auxiliar_classes.state_pair import StatePair as StatePair
from tabulate import tabulate


def triangular_table(complete_automaton: CompleteAFD) -> dict:
    accessible_states = complete_automaton.get_accessible_states_list()
    # Ordenamos para saber como acceder a la tabla triangular
    accessible_states.sort()
    # Inicializamos la tabla triangular
    table = {}
    for i in range(0, len(accessible_states)):
        table[accessible_states[i]] = {}
        for j in range(0, i):
            table[accessible_states[i]][accessible_states[j]] = StatePair()
    # Arrancamos el algoritmo
    for q_a in accessible_states:
        for q_b in table[q_a]:
            if complete_automaton.is_final(q_a) != complete_automaton.is_final(q_b):
                table[q_a][q_b].mark()
            else:
                for c in complete_automaton.get_alphabet():
                    q_a_next = complete_automaton.get_next_state(q_a, c)
                    q_b_next = complete_automaton.get_next_state(q_b, c)
                    # Si son el mismo estado no podemos saber nada
                    if q_a_next == q_b_next:
                        continue
                    # Cambiamos los índices para no salirnos de la tabla
                    if q_a_next < q_b_next:
                        temp = q_a_next
                        q_a_next = q_b_next
                        q_b_next = temp
                    # Si los nuevos estados son distinguibles, los anteriores
                    # también
                    if table[q_a_next][q_b_next].is_marked():
                        table[q_a][q_b].mark()
                        break
                    # Si no, los añadimos a su lista
                    else:
                        table[q_a_next][q_b_next].add_edge(table[q_a][q_b])
    return table


def minimize(automaton) -> None:
    # Completamos el autómata a través de una clase wrapper que nos
    # abstrae de lo que hace y nos proporciona las mismas funciones
    # que un autómata normal.
    complete_automaton = CompleteAFD(automaton)
    # Obtenemos una lista con los estados accesibles
    accessible_states = complete_automaton.get_accessible_states_list()
    # Aplicamos el algoritmo de la tabla triangular
    table = triangular_table(complete_automaton)
    # Usamos un DisjointSetUnion para crear las clases de equivalencia
    dsu = StateDisjointSetUnion(complete_automaton)
    # Unimos todos los estados no distinguibles
    for q_a in accessible_states:
        for q_b in table[q_a]:
            if not table[q_a][q_b].is_marked():
                dsu.join(q_a, q_b)
    # Usamos un diccionario que lleve cada representante de su clase de
    # equivalencia a su nuevo estado
    dic_representatives = dsu.dic_representative_to_new_state()
    # Formamos la tabla
    # La primera fila es el encabezado
    header = ['Name']
    # Añadimos al encabezado los elementos del alfabeto
    for c in complete_automaton.get_alphabet():
        header.append(c)
    # Ahora creamos la tabla en sí, y la guardamos en values
    values = []
    # Para cada estado representante de su clase
    for key in dic_representatives.keys():
        # Añadimos al nombre de la clase de estados'->' ó '#' si es inicial y final, respectivamente
        suffix = ''
        if dic_representatives[key]['initial']:
            suffix += '->'
        if dic_representatives[key]['final']:
            suffix += '#'
        # Creamos una lista que comienza con el nombre de la clase de estados
        lst = [suffix + dic_representatives[key]['str']]
        # Para cada elemento del alfabeto, guardamos en la lista la clase de estados a la que nos lleva
        # desde el estado actual
        for c in complete_automaton.get_alphabet():
            # Tomamos el representante de nuestra clase, vemos a qué estado lleva, el cual guardamos
            # en new_representative
            new_representative = dsu.get_representative(complete_automaton.get_next_state(
                key, c))
            # Obtenemos la clase de estados a la que representa new_representative y la añadimos a la lista
            lst.append(dic_representatives[new_representative]['str'])
        # Al final añadimos a la tabla la fila de la clase de estados actual.
        values.append(lst)
    # Utilizamos la librería tabulate para formatear la tabla
    print(tabulate(values, header, tablefmt='orgtbl'))
