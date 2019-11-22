from .complete_afd import CompleteAFD as CompleteAFD

NO_PARENT = '-1'


class State:
    """Clase que representa un estado en nuestro DSU"""

    def __init__(self, final: bool, initial: bool) -> None:
        """Guarda si un el estado es final, inicial y quien es su padre"""
        self.parent = NO_PARENT
        self.final = final
        self.initial = initial


class StateDisjointSetUnion:
    """
    Clase para unir los estados no distinguibles
    """

    # Comenzamos con todos distinguibles
    def __init__(self, complete_automaton: CompleteAFD) -> None:
        """Construimos un diccionario que lleve cadenas a estados"""
        self.dic = {}
        for key in complete_automaton.get_accessible_states_list():
            # Al principio cada estado no tiene padre, guardamos también si es final o inicial
            self.dic[key] = State(complete_automaton.is_final(key), complete_automaton.is_initial(key))

    def get_representative(self, q: str) -> str:
        """Devuelve el representante de la clase de q"""
        # Si no tiene padre, el representante es él
        if self.dic[q].parent == NO_PARENT:
            return q
        # Comprimimos el árbol
        self.dic[q].parent = self.get_representative(self.dic[q].parent)
        return self.dic[q].parent

    def join(self, q_a: str, q_b: str):
        """Une las clases de q_a y q_b"""
        # Obtenemos los representantes de ambos
        q_a_rep = self.get_representative(q_a)
        q_b_rep = self.get_representative(q_b)
        # Si son distintos los unimos
        if q_a_rep != q_b_rep:
            self.dic[q_b_rep].parent = q_a_rep
            # Solo mantenmos actualizado el padre, que será final o inicial
            # si alguno de los hijos lo son
            self.dic[q_a_rep].final = self.dic[q_a_rep].final or self.dic[q_b_rep].final
            self.dic[q_a_rep].initial = self.dic[q_a_rep].initial or self.dic[q_b_rep].initial

    # Devuelve un diccionario que lleva a los representates
    # a una cadena que representa el nuevo estado

    def dic_representative_to_string(self) -> dict:
        """Devolvemos un diccionario que lleve un estado a su clase en forma de cadena
        El objeto al que lleva cada estado tiene un string con todos los estados de la
        clase entre corchetes, y un par de booleanos para comprobar que es final o inicial.
        """
        # dic_ret es el diccionario que vamos a devolver
        dic_ret = {}
        # dic_list es un diccionario que lleva representantes de una clase a listas de
        # sus miembros
        dic_list = {}
        # Para cada estado key, si es el representante de su clase, entonces lo añadimos
        # a los diccionarios
        for key in self.dic.keys():
            if self.dic[key].parent == NO_PARENT:
                # Para cada representante guardamos si es final y si es inicial
                dic_ret[key] = {
                    'final': self.dic[key].final,
                    'initial': self.dic[key].initial
                }
                # Para cada representante guaramos una lista vacía
        # Guardamos cada estado key en la lista de su representante
        for key in self.dic.keys():
            dic_list[self.get_representative(key)].append(key)
        # Creamos en el diccionario a devolver una cadena con el nombre de la clase de
        # equivalencia, es decir, los nombres de los miembros separados por comas y
        # entre corchetes
        for key in dic_ret:
            dic_ret[key]['str'] = '{' + str(dic_list[key]).strip('[]') + '}'
        return dic_ret
