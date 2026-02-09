-- Script para crear la tabla de usuarios
-- Base de datos: laura

USE laura;

-- Crear tabla de usuarios
CREATE TABLE IF NOT EXISTS Usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    rol VARCHAR(20) NOT NULL DEFAULT 'usuario',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Nota: Ejecuta el script crear_usuario_inicial.py para crear el primer usuario admin
-- O crea manualmente un usuario administrador desde el registro y luego actualiza su rol en la base de datos
