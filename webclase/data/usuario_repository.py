import bcrypt
from typing import Optional
from domain.model.Usuario import Usuario


class UsuarioRepository:
    
    def get_all(self, db):
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id, nombre, contraseña FROM users")
        usuarios = cursor.fetchall()
        cursor.close()
        return [Usuario(u['id'], u['nombre'], u['contraseña'], 'admin' if u['nombre'] == 'admin' else 'usuario') for u in usuarios]
    
    def get_by_id(self, db, usuario_id: int) -> Optional[Usuario]:
        """Busca un usuario por ID"""
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id, nombre, contraseña FROM users WHERE id = %s", (usuario_id,))
        usuario_data = cursor.fetchone()
        cursor.close()
        
        if usuario_data:
            rol = 'admin' if usuario_data['nombre'].lower() == 'admin' else 'usuario'
            return Usuario(
                usuario_data['id'], 
                usuario_data['nombre'], 
                usuario_data['contraseña'],
                rol
            )
        return None
    
    def get_by_username(self, db, username: str) -> Optional[Usuario]:
        """Busca un usuario por nombre de usuario"""
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id, nombre, contraseña FROM users WHERE nombre = %s", (username,))
        usuario_data = cursor.fetchone()
        cursor.close()
        
        if usuario_data:
            rol = 'admin' if usuario_data['nombre'].lower() == 'admin' else 'usuario'
            return Usuario(
                usuario_data['id'], 
                usuario_data['nombre'], 
                usuario_data['contraseña'],
                rol
            )
        return None
    
    def insertar_usuario(self, db, username: str, password: str, email: str = None, rol: str = "usuario"):
        """Inserta un nuevo usuario con contraseña hasheada en la tabla users de DBeaver"""
        try:
            # Hash de la contraseña con bcrypt
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            cursor = db.cursor()
            query = "INSERT INTO users (nombre, contraseña) VALUES (%s, %s)"
            cursor.execute(query, (username, password_hash))
            db.commit()
            cursor.close()
            print(f"✅ Usuario {username} insertado en DBeaver (informatica.iesquevedo.es -> laura -> users)")
        except Exception as e:
            print(f"❌ Error al insertar usuario {username}: {str(e)}")
            raise e
    
    def verificar_password(self, password: str, password_hash) -> bool:
        """Verifica si una contraseña coincide con su hash"""
        # Asegurar que password_hash sea bytes
        if isinstance(password_hash, str):
            password_hash = password_hash.encode('utf-8')
        elif isinstance(password_hash, bytearray):
            password_hash = bytes(password_hash)
        
        return bcrypt.checkpw(password.encode('utf-8'), password_hash)
    
    def actualizar_usuario(self, db, usuario_id: int, username: str = None, email: str = None):
        """Actualiza los datos de un usuario"""
        if username:
            cursor = db.cursor()
            cursor.execute("UPDATE users SET nombre = %s WHERE id = %s", (username, usuario_id))
            db.commit()
            cursor.close()
    
    def cambiar_password(self, db, usuario_id: int, nueva_password: str):
        """Cambia la contraseña de un usuario"""
        password_hash = bcrypt.hashpw(nueva_password.encode('utf-8'), bcrypt.gensalt())
        
        cursor = db.cursor()
        cursor.execute("UPDATE users SET contraseña = %s WHERE id = %s", (password_hash, usuario_id))
        db.commit()
        cursor.close()
    
    def borrar_usuario(self, db, usuario_id: int):
        """Elimina un usuario por ID"""
        cursor = db.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (usuario_id,))
        db.commit()
        cursor.close()
