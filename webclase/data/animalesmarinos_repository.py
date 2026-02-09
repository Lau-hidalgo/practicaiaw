from domain.model.AnimalMarino import AnimalMarino


class AnimalesMarinosRepository:

    def get_all(self, db) -> list[AnimalMarino]:
        cursor = db.cursor()

        cursor.execute("SELECT id, nombre, imagen_url FROM animalesmarinos")

        filas = cursor.fetchall()
        animales: list[AnimalMarino] = list()
        for fila in filas:
            animal = AnimalMarino(fila[0], fila[1], fila[2] if len(fila) > 2 else None)
            animales.append(animal)
        cursor.close()

        return animales

    def get_by_id(self, db, animal_id: int) -> AnimalMarino:
        """Obtener un animal marino por ID"""
        cursor = db.cursor()
        cursor.execute("SELECT id, nombre, imagen_url FROM animalesmarinos WHERE id = %s", (animal_id,))
        fila = cursor.fetchone()
        cursor.close()
        
        if fila:
            return AnimalMarino(fila[0], fila[1], fila[2] if len(fila) > 2 else None)
        return None

    def insertar_animal(self, db, animal: AnimalMarino) -> None:
        cursor = db.cursor()

        cursor.execute("INSERT INTO animalesmarinos (nombre, imagen_url) VALUES (%s, %s)", 
                      (animal.nombre, animal.imagen_url))

        db.commit()
        cursor.close()

    def borrar_animal(self, db, id: int) -> None:
        cursor = db.cursor()

        cursor.execute("DELETE FROM animalesmarinos WHERE id = %s", (id,))

        db.commit()
        cursor.close()

    def actualizar_animal(self, db, id: int, nuevo_nombre: str, imagen_url: str = None) -> None:
        """Actualizar el nombre y opcionalmente la imagen de un animal por id."""
        cursor = db.cursor()
        
        # Obtener la imagen actual si no se proporciona una nueva
        if imagen_url is None or imagen_url == '':
            cursor.execute("SELECT imagen_url FROM animalesmarinos WHERE id = %s", (id,))
            row = cursor.fetchone()
            if row:
                imagen_url = row[0]  # Mantener la imagen actual
        
        cursor.execute("UPDATE animalesmarinos SET nombre = %s, imagen_url = %s WHERE id = %s", 
                      (nuevo_nombre, imagen_url, id))

        db.commit()
        cursor.close()
