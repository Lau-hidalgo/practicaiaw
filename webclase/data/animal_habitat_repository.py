from typing import List, Dict


class AnimalHabitatRepository:
    
    def asociar_animal_habitat(self, database, animal_id: int, habitat_id: int, 
                               poblacion_estimada: int = None, estado_conservacion: str = None,
                               pais_id: int = None):
        """Asociar un animal marino con un hábitat"""
        cursor = database.cursor()
        sql = """
            INSERT INTO animales_habitats (animal_id, habitat_id, poblacion_estimada, estado_conservacion, pais_id) 
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                poblacion_estimada = VALUES(poblacion_estimada),
                estado_conservacion = VALUES(estado_conservacion),
                pais_id = VALUES(pais_id)
        """
        cursor.execute(sql, (animal_id, habitat_id, poblacion_estimada, estado_conservacion, pais_id))
        database.commit()
        cursor.close()
    
    def desasociar_animal_habitat(self, database, animal_id: int, habitat_id: int):
        """Eliminar la asociación entre un animal y un hábitat"""
        cursor = database.cursor()
        cursor.execute(
            "DELETE FROM animales_habitats WHERE animal_id = %s AND habitat_id = %s",
            (animal_id, habitat_id)
        )
        database.commit()
        cursor.close()
    
    def get_habitats_por_animal(self, database, animal_id: int) -> List[Dict]:
        """Obtener todos los hábitats donde vive un animal"""
        cursor = database.cursor()
        sql = """
            SELECT h.id, h.nombre, h.descripcion, h.profundidad_min, h.profundidad_max, 
                   h.temperatura_media, ah.poblacion_estimada, ah.estado_conservacion,
                   ah.pais_id, p.nombre as pais_nombre
            FROM habitats h
            INNER JOIN animales_habitats ah ON h.id = ah.habitat_id
            LEFT JOIN paises p ON ah.pais_id = p.id
            WHERE ah.animal_id = %s
            ORDER BY h.nombre
        """
        cursor.execute(sql, (animal_id,))
        rows = cursor.fetchall()
        cursor.close()
        
        habitats = []
        for row in rows:
            habitat = {
                'id': row[0],
                'nombre': row[1],
                'descripcion': row[2],
                'profundidad_min': row[3],
                'profundidad_max': row[4],
                'temperatura_media': float(row[5]) if row[5] else None,
                'poblacion_estimada': row[6],
                'estado_conservacion': row[7],
                'pais_id': row[8],
                'pais_nombre': row[9]
            }
            habitats.append(habitat)
        
        return habitats
    
    def get_animales_por_habitat(self, database, habitat_id: int) -> List[Dict]:
        """Obtener todos los animales que viven en un hábitat"""
        cursor = database.cursor()
        sql = """
            SELECT a.id, a.nombre, ah.poblacion_estimada, ah.estado_conservacion,
                   ah.pais_id, p.nombre as pais_nombre
            FROM animalesmarinos a
            INNER JOIN animales_habitats ah ON a.id = ah.animal_id
            LEFT JOIN paises p ON ah.pais_id = p.id
            WHERE ah.habitat_id = %s
            ORDER BY a.nombre
        """
        cursor.execute(sql, (habitat_id,))
        rows = cursor.fetchall()
        cursor.close()
        
        animales = []
        for row in rows:
            animal = {
                'id': row[0],
                'nombre': row[1],
                'poblacion_estimada': row[2],
                'estado_conservacion': row[3],
                'pais_id': row[4],
                'pais_nombre': row[5]
            }
            animales.append(animal)
        
        return animales
    
    def get_all_asociaciones(self, database) -> List[Dict]:
        """Obtener todas las asociaciones entre animales y hábitats"""
        cursor = database.cursor()
        sql = """
            SELECT ah.animal_id, a.nombre as animal_nombre, 
                   ah.habitat_id, h.nombre as habitat_nombre,
                   ah.poblacion_estimada, ah.estado_conservacion,
                   ah.pais_id, p.nombre as pais_nombre, p.codigo as pais_codigo
            FROM animales_habitats ah
            INNER JOIN animalesmarinos a ON ah.animal_id = a.id
            INNER JOIN habitats h ON ah.habitat_id = h.id
            LEFT JOIN paises p ON ah.pais_id = p.id
            ORDER BY a.nombre, h.nombre
        """
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        
        asociaciones = []
        for row in rows:
            asociacion = {
                'animal_id': row[0],
                'animal_nombre': row[1],
                'habitat_id': row[2],
                'habitat_nombre': row[3],
                'poblacion_estimada': row[4],
                'estado_conservacion': row[5],
                'pais_id': row[6],
                'pais_nombre': row[7],
                'pais_codigo': row[8]
            }
            asociaciones.append(asociacion)
        
        return asociaciones
    
    def get_habitats_no_asociados(self, database, animal_id: int) -> List[Dict]:
        """Obtener hábitats que aún no están asociados a un animal específico"""
        cursor = database.cursor()
        sql = """
            SELECT h.id, h.nombre, h.descripcion
            FROM habitats h
            WHERE h.id NOT IN (
                SELECT habitat_id 
                FROM animales_habitats 
                WHERE animal_id = %s
            )
            ORDER BY h.nombre
        """
        cursor.execute(sql, (animal_id,))
        rows = cursor.fetchall()
        cursor.close()
        
        habitats = []
        for row in rows:
            habitat = {
                'id': row[0],
                'nombre': row[1],
                'descripcion': row[2]
            }
            habitats.append(habitat)
        
        return habitats
