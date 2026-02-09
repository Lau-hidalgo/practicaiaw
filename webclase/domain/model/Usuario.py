class Usuario:
    def __init__(self, id: int, username: str, password_hash: str, rol: str = "usuario", email: str = None):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.rol = rol  # "admin" o "usuario"
        self.email = email
