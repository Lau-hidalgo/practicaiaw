-- Agregar columna imagen_url a la tabla animalesmarinos
ALTER TABLE animalesmarinos ADD COLUMN imagen_url VARCHAR(500) DEFAULT NULL;

-- Actualizar con imágenes de ejemplo de Unsplash (puedes cambiarlas)
UPDATE animalesmarinos SET imagen_url = 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=400&h=400&fit=crop' WHERE nombre LIKE '%kai%';
UPDATE animalesmarinos SET imagen_url = 'https://images.unsplash.com/photo-1583212292454-1fe6229603b7?w=400&h=400&fit=crop' WHERE nombre LIKE '%ballena%';
UPDATE animalesmarinos SET imagen_url = 'https://images.unsplash.com/photo-1546026423-cc4642628d2b?w=400&h=400&fit=crop' WHERE nombre LIKE '%tiburon%' OR nombre LIKE '%shark%';
UPDATE animalesmarinos SET imagen_url = 'https://images.unsplash.com/photo-1535591273668-578e31182c4f?w=400&h=400&fit=crop' WHERE nombre LIKE '%delfin%' OR nombre LIKE '%dolphin%';
UPDATE animalesmarinos SET imagen_url = 'https://images.unsplash.com/photo-1583212292454-1fe6229603b7?w=400&h=400&fit=crop' WHERE nombre LIKE '%orca%';
UPDATE animalesmarinos SET imagen_url = 'https://images.unsplash.com/photo-1583212292454-1fe6229603b7?w=400&h=400&fit=crop' WHERE nombre LIKE '%pulpo%' OR nombre LIKE '%octopus%';
UPDATE animalesmarinos SET imagen_url = 'https://images.unsplash.com/photo-1546182990-dffeafbe841d?w=400&h=400&fit=crop' WHERE nombre LIKE '%tortuga%' OR nombre LIKE '%turtle%';

-- Si no tienen imagen específica, poner una imagen genérica de océano
UPDATE animalesmarinos SET imagen_url = 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=400&h=400&fit=crop' 
WHERE imagen_url IS NULL;
