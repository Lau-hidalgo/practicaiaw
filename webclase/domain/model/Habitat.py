class Habitat:
    def __init__(self, id: int, nombre: str, descripcion: str = None, 
                 profundidad_min: int = None, profundidad_max: int = None, 
                 temperatura_media: float = None):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.profundidad_min = profundidad_min
        self.profundidad_max = profundidad_max
        self.temperatura_media = temperatura_media
