class Comentario:
    def __init__(self, id: int, animal_id: int, usuario_nombre: str, comentario: str, fecha=None):
        self.id = id
        self.animal_id = animal_id
        self.usuario_nombre = usuario_nombre
        self.comentario = comentario
        self.fecha = fecha
