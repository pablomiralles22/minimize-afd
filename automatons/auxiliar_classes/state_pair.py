class StatePair:
    """Clase que representa una pareja de estados en la tabla triangular."""

    def __init__(self) -> None:
        self.adjacency_list = []
        self.marked = False

    def mark(self) -> None:
        """Marca la pareja, y todas las que haya en su lista que no estén marcadas."""
        self.marked = True
        for sp in self.adjacency_list:
            if not sp.is_marked():
                sp.mark()

    def is_marked(self) -> bool:
        """Devuelve si la pareja está marcada"""
        return self.marked

    def add_edge(self, other) -> None:
        """Añade otra pareja como arista"""
        self.adjacency_list.append(other)
