ERROR_STATE = 'q_error'


class CompleteAFD:
    """Clase wrapper para "completar" un autómata y eliminar estados inaccesibles.
    Exporta todas las funciones de un autómata, pero crea un nuevo estado 'q_error'
    en caso de que sea necesario, y extiende las funciones del autómata para que
    tengan en cuenta este nuevo estado
    """

    def __init__(self, automaton):
        """Constructor
        Guardamos una lista con los estados accesibles, guardamos el autómata
        original y añadimos el estado de error si es necesario
        """
        self.automaton = automaton
        self.accessible_states_list = [automaton.getEstadoInicial()]
        complete = True
        i = 0
        # Recorremos el autómata como si fuese un grafo, en anchura. De esta forma
        # solo guardamos estados accesibles
        while i < len(self.accessible_states_list):
            q = self.accessible_states_list[i]
            i += 1
            for c in automaton.getAlfabeto():
                q_next = automaton.estadoSiguiente(q, c)
                if q_next:
                    if q_next not in self.accessible_states_list:
                        self.accessible_states_list.append(q_next)
                # Si para algún elemento del alfabeto no se llega a otro estado
                # entonces el autómata no es completo
                else:
                    complete = False
        # Si el autómata no es completo añadimos el estado de error
        if not complete:
            self.accessible_states_list.append(ERROR_STATE)

    def get_accessible_states_list(self) -> list:
        """Método que devuelve una lista de los estados accesibles"""
        return self.accessible_states_list

    def get_next_state(self, q: str, c: str) -> str:
        """Devuelve el siguiente estado desde q con el elemento del alfabeto c"""
        # Si q es el estado de error, o el siguiente estado no existe, devolvemos
        # el estado de error.
        if q == ERROR_STATE or not self.automaton.estadoSiguiente(q, c):
            return ERROR_STATE
        return self.automaton.estadoSiguiente(q, c)

    def is_final(self, q: str) -> bool:
        """Devuelve si un estado q es final"""
        # El estado de error no es final
        if q == ERROR_STATE:
            return False
        return self.automaton.esFinal(q)

    def is_initial(self, q: str) -> bool:
        """Devuelve si un estado q es inicial"""
        # El estado de error no es inicial
        if q == ERROR_STATE:
            return False
        return self.automaton.getEstadoInicial() == q

    def get_initial_state(self, q: str) -> str:
        """Devuelve el estado inicial del autómata"""
        return self.automaton.getEstadoInicial()

    def get_alphabet(self) -> set:
        """Devuelve el alfabeto del autómata"""
        return self.automaton.getAlfabeto()
