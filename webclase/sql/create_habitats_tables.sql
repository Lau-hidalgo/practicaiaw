-- Tabla de hábitats
CREATE TABLE IF NOT EXISTS habitats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    profundidad_min INT,  -- profundidad mínima en metros
    profundidad_max INT,  -- profundidad máxima en metros
    temperatura_media DECIMAL(5,2),  -- temperatura media en grados celsius
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla intermedia para la relación N-M entre animales marinos y hábitats
CREATE TABLE IF NOT EXISTS animales_habitats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    animal_id INT NOT NULL,
    habitat_id INT NOT NULL,
    poblacion_estimada INT,  -- población estimada de este animal en este hábitat
    estado_conservacion VARCHAR(50),  -- Abundante, Común, Raro, En peligro, etc.
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (animal_id) REFERENCES animalesmarinos(id) ON DELETE CASCADE,
    FOREIGN KEY (habitat_id) REFERENCES habitats(id) ON DELETE CASCADE,
    UNIQUE KEY unique_animal_habitat (animal_id, habitat_id)
);

-- Insertar algunos hábitats de ejemplo
INSERT INTO habitats (nombre, descripcion, profundidad_min, profundidad_max, temperatura_media) 
VALUES 
    ('Arrecife de Coral', 'Ecosistema marino de aguas cálidas y poco profundas', 1, 50, 26.5),
    ('Fosa Abisal', 'Zona de las profundidades oceánicas con presión extrema', 6000, 11000, 2.0),
    ('Plataforma Continental', 'Extensión submarina de los continentes', 0, 200, 18.0),
    ('Zona Pelágica', 'Aguas abiertas lejos de la costa', 200, 1000, 15.5),
    ('Manglares', 'Bosques costeros en zonas intermareales', 0, 5, 28.0),
    ('Zona Polar', 'Aguas frías de los polos', 0, 500, -1.5)
ON DUPLICATE KEY UPDATE nombre=nombre;
