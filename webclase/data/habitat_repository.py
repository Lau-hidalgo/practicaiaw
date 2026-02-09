from domain.model.Habitat import Habitat
from typing import List


class HabitatRepository:
    
    def get_all(self, database) -> List[Habitat]:
        """Obtener todos los hábitats"""
        cursor = database.cursor()
        cursor.execute("SELECT id, nombre, descripcion, profundidad_min, profundidad_max, temperatura_media FROM habitats ORDER BY nombre")
        rows = cursor.fetchall()
        cursor.close()
        
        habitats = []
        for row in rows:
            habitat = Habitat(
                id=row[0],
                nombre=row[1],
                descripcion=row[2],
                profundidad_min=row[3],
                profundidad_max=row[4],
                temperatura_media=float(row[5]) if row[5] else None
            )
            habitats.append(habitat)
        
        return habitats
    
    def get_by_id(self, database, habitat_id: int) -> Habitat:
        """Obtener un hábitat por ID"""
        cursor = database.cursor()
        cursor.execute(
            "SELECT id, nombre, descripcion, profundidad_min, profundidad_max, temperatura_media FROM habitats WHERE id = %s",
            (habitat_id,)
        )
        row = cursor.fetchone()
        cursor.close()
        
        if row:
            return Habitat(
                id=row[0],
                nombre=row[1],
                descripcion=row[2],
                profundidad_min=row[3],
                profundidad_max=row[4],
                temperatura_media=float(row[5]) if row[5] else None
            )
        return None
    
    def insertar_habitat(self, database, habitat: Habitat):
        """Insertar un nuevo hábitat"""
        cursor = database.cursor()
        sql = """
            INSERT INTO habitats (nombre, descripcion, profundidad_min, profundidad_max, temperatura_media) 
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (
            habitat.nombre,
            habitat.descripcion,
            habitat.profundidad_min,
            habitat.profundidad_max,
            habitat.temperatura_media
        ))
        database.commit()
        cursor.close()
    
    def actualizar_habitat(self, database, habitat_id: int, nombre: str, descripcion: str = None,
                          profundidad_min: int = None, profundidad_max: int = None,
                          temperatura_media: float = None):
        """Actualizar un hábitat existente"""
        cursor = database.cursor()
        sql = """
            UPDATE habitats 
            SET nombre = %s, descripcion = %s, profundidad_min = %s, 
                profundidad_max = %s, temperatura_media = %s
            WHERE id = %s
        """
        cursor.execute(sql, (
            nombre, descripcion, profundidad_min, 
            profundidad_max, temperatura_media, habitat_id
        ))
        database.commit()
        cursor.close()
    
    def borrar_habitat(self, database, habitat_id: int):
        """Borrar un hábitat por ID"""
        cursor = database.cursor()
        cursor.execute("DELETE FROM habitats WHERE id = %s", (habitat_id,))
        database.commit()
        cursor.close()
