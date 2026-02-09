-- Crear tabla de países
CREATE TABLE IF NOT EXISTS paises (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    codigo VARCHAR(3) NOT NULL UNIQUE,
    continente VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Agregar columna pais_id a animales_habitats
ALTER TABLE animales_habitats 
ADD COLUMN pais_id INT DEFAULT NULL,
ADD FOREIGN KEY (pais_id) REFERENCES paises(id) ON DELETE SET NULL;

-- Insertar países de ejemplo donde se pueden encontrar animales marinos
INSERT INTO paises (nombre, codigo, continente) VALUES
-- América
('México', 'MEX', 'América'),
('Estados Unidos', 'USA', 'América'),
('Brasil', 'BRA', 'América'),
('Argentina', 'ARG', 'América'),
('Chile', 'CHL', 'América'),
('Perú', 'PER', 'América'),
('Colombia', 'COL', 'América'),
('Ecuador', 'ECU', 'América'),
('Costa Rica', 'CRI', 'América'),
('Bahamas', 'BHS', 'América'),

-- Europa
('España', 'ESP', 'Europa'),
('Portugal', 'PRT', 'Europa'),
('Francia', 'FRA', 'Europa'),
('Italia', 'ITA', 'Europa'),
('Grecia', 'GRC', 'Europa'),
('Noruega', 'NOR', 'Europa'),
('Islandia', 'ISL', 'Europa'),

-- Asia
('Japón', 'JPN', 'Asia'),
('Tailandia', 'THA', 'Asia'),
('Indonesia', 'IDN', 'Asia'),
('Filipinas', 'PHL', 'Asia'),
('Maldivas', 'MDV', 'Asia'),
('India', 'IND', 'Asia'),

-- Oceanía
('Australia', 'AUS', 'Oceanía'),
('Nueva Zelanda', 'NZL', 'Oceanía'),
('Fiyi', 'FJI', 'Oceanía'),
('Palau', 'PLW', 'Oceanía'),

-- África
('Sudáfrica', 'ZAF', 'África'),
('Madagascar', 'MDG', 'África'),
('Egipto', 'EGY', 'África'),
('Kenia', 'KEN', 'África'),

-- Antártida
('Antártida', 'ATA', 'Antártida')
ON DUPLICATE KEY UPDATE nombre=nombre;
