from domain.model.Pais import Pais
from typing import List


class PaisRepository:
    
    def get_all(self, database) -> List[Pais]:
        """Obtener todos los países ordenados por nombre"""
        cursor = database.cursor()
        cursor.execute("SELECT id, nombre, codigo, continente FROM paises ORDER BY nombre")
        rows = cursor.fetchall()
        cursor.close()
        
        paises = []
        for row in rows:
            pais = Pais(
                id=row[0],
                nombre=row[1],
                codigo=row[2],
                continente=row[3]
            )
            paises.append(pais)
        
        return paises
    
    def get_by_id(self, database, pais_id: int) -> Pais:
        """Obtener un país por ID"""
        cursor = database.cursor()
        cursor.execute(
            "SELECT id, nombre, codigo, continente FROM paises WHERE id = %s",
            (pais_id,)
        )
        row = cursor.fetchone()
        cursor.close()
        
        if row:
            return Pais(
                id=row[0],
                nombre=row[1],
                codigo=row[2],
                continente=row[3]
            )
        return None
    
    def get_animales_por_pais(self, database, pais_id: int) -> list:
        """Obtener todos los animales que se encuentran en un país específico"""
        cursor = database.cursor()
        sql = """
            SELECT DISTINCT a.id, a.nombre, a.imagen_url, h.nombre as habitat_nombre, 
                   ah.poblacion_estimada, ah.estado_conservacion
            FROM animalesmarinos a
            INNER JOIN animales_habitats ah ON a.id = ah.animal_id
            INNER JOIN habitats h ON ah.habitat_id = h.id
            WHERE ah.pais_id = %s
            ORDER BY a.nombre
        """
        cursor.execute(sql, (pais_id,))
        rows = cursor.fetchall()
        cursor.close()
        
        animales = []
        for row in rows:
            animal = {
                'id': row[0],
                'nombre': row[1],
                'imagen_url': row[2],
                'habitat_nombre': row[3],
                'poblacion_estimada': row[4],
                'estado_conservacion': row[5]
            }
            animales.append(animal)
        
        return animales
    
    def get_by_continente(self, database) -> dict:
        """Obtener países agrupados por continente"""
        cursor = database.cursor()
        cursor.execute("SELECT id, nombre, codigo, continente FROM paises ORDER BY continente, nombre")
        rows = cursor.fetchall()
        cursor.close()
        
        paises_por_continente = {}
        for row in rows:
            continente = row[3] or 'Otros'
            if continente not in paises_por_continente:
                paises_por_continente[continente] = []
            
            pais = Pais(
                id=row[0],
                nombre=row[1],
                codigo=row[2],
                continente=row[3]
            )
            paises_por_continente[continente].append(pais)
        
        return paises_por_continente
