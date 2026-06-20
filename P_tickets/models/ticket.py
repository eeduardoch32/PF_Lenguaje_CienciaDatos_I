class Ticket:
    def __init__(self, id_ticket, descripcion, fecha):
        self.id_ticket = id_ticket
        self.descripcion = descripcion
        self.fecha = fecha
        self.categoria = None  # Se clasifica y asignará con la IA
        self.prioridad = None

    def asignar_categoria(self, categoria):
        self.categoria = categoria

    def __repr__(self):
        return f"Ticket({self.id_ticket}) - Categoría: {self.categoria}"