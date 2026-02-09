from typing import List
from domain.model.Comentario import Comentario


class ComentarioRepository:
    
    def get_by_animal(self, database, animal_id: int) -> List[dict]:
        """Obtener todos los comentarios de un animal ordenados por fecha (más recientes primero)"""
        cursor = database.cursor()
        sql = """
            SELECT id, animal_id, usuario_nombre, comentario, fecha
            FROM comentarios
            WHERE animal_id = %s
            ORDER BY fecha DESC
        """
        cursor.execute(sql, (animal_id,))
        rows = cursor.fetchall()
        cursor.close()
        
        comentarios = []
        for row in rows:
            comentario = {
                'id': row[0],
                'animal_id': row[1],
                'usuario_nombre': row[2],
                'comentario': row[3],
                'fecha': row[4]
            }
            comentarios.append(comentario)
        
        return comentarios
    
    def insertar(self, database, animal_id: int, usuario_nombre: str, comentario: str):
        """Insertar un nuevo comentario"""
        cursor = database.cursor()
        sql = "INSERT INTO comentarios (animal_id, usuario_nombre, comentario) VALUES (%s, %s, %s)"
        cursor.execute(sql, (animal_id, usuario_nombre, comentario))
        database.commit()
        cursor.close()
    
    def borrar(self, database, comentario_id: int, usuario_nombre: str = None):
        """Borrar un comentario (solo el autor o un admin)"""
        cursor = database.cursor()
        if usuario_nombre:
            # Usuario normal: solo puede borrar sus propios comentarios
            sql = "DELETE FROM comentarios WHERE id = %s AND usuario_nombre = %s"
            cursor.execute(sql, (comentario_id, usuario_nombre))
        else:
            # Admin: puede borrar cualquier comentario
            sql = "DELETE FROM comentarios WHERE id = %s"
            cursor.execute(sql, (comentario_id,))
        database.commit()
        affected = cursor.rowcount
        cursor.close()
        return affected > 0
