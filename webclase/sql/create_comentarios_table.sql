-- Crear tabla de comentarios
CREATE TABLE IF NOT EXISTS comentarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    animal_id INT NOT NULL,
    usuario_nombre VARCHAR(100) NOT NULL,
    comentario TEXT NOT NULL,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (animal_id) REFERENCES animalesmarinos(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Índices para mejorar el rendimiento
CREATE INDEX idx_animal_id ON comentarios(animal_id);
CREATE INDEX idx_fecha ON comentarios(fecha DESC);
