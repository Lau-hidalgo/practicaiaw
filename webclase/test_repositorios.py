"""
Script de prueba rápida para verificar que todos los repositorios funcionan
"""

from data.database import database
from data.habitat_repository import HabitatRepository
from data.animal_habitat_repository import AnimalHabitatRepository
from data.animalesmarinos_repository import AnimalesMarinosRepository

print("🧪 Iniciando pruebas...")
print("=" * 60)

# Probar HabitatRepository
print("\n📍 Probando HabitatRepository...")
try:
    repo_habitat = HabitatRepository()
    habitats = repo_habitat.get_all(database)
    print(f"✅ get_all(): {len(habitats)} hábitats encontrados")
    
    if habitats:
        primer_habitat = habitats[0]
        print(f"   Ejemplo: {primer_habitat.nombre}")
        
        # Probar get_by_id
        habitat = repo_habitat.get_by_id(database, primer_habitat.id)
        if habitat:
            print(f"✅ get_by_id(): Hábitat '{habitat.nombre}' encontrado")
        else:
            print("❌ get_by_id(): Falló")
except Exception as e:
    print(f"❌ Error en HabitatRepository: {e}")

# Probar AnimalesMarinosRepository
print("\n🐠 Probando AnimalesMarinosRepository...")
try:
    repo_animal = AnimalesMarinosRepository()
    animales = repo_animal.get_all(database)
    print(f"✅ get_all(): {len(animales)} animales encontrados")
    
    if animales:
        primer_animal = animales[0]
        print(f"   Ejemplo: {primer_animal.nombre}")
        
        # Probar get_by_id
        animal = repo_animal.get_by_id(database, primer_animal.id)
        if animal:
            print(f"✅ get_by_id(): Animal '{animal.nombre}' encontrado")
        else:
            print("❌ get_by_id(): Falló")
except Exception as e:
    print(f"❌ Error en AnimalesMarinosRepository: {e}")

# Probar AnimalHabitatRepository
print("\n🔗 Probando AnimalHabitatRepository...")
try:
    repo_ah = AnimalHabitatRepository()
    asociaciones = repo_ah.get_all_asociaciones(database)
    print(f"✅ get_all_asociaciones(): {len(asociaciones)} asociaciones encontradas")
    
    if asociaciones:
        primera = asociaciones[0]
        print(f"   Ejemplo: {primera['animal_nombre']} en {primera['habitat_nombre']}")
    
    # Probar obtener hábitats de un animal
    if animales:
        habitats_del_animal = repo_ah.get_habitats_por_animal(database, animales[0].id)
        print(f"✅ get_habitats_por_animal(): {len(habitats_del_animal)} hábitats para '{animales[0].nombre}'")
    
    # Probar obtener animales de un hábitat
    if habitats:
        animales_del_habitat = repo_ah.get_animales_por_habitat(database, habitats[0].id)
        print(f"✅ get_animales_por_habitat(): {len(animales_del_habitat)} animales en '{habitats[0].nombre}'")
    
    # Probar hábitats no asociados
    if animales:
        habitats_disponibles = repo_ah.get_habitats_no_asociados(database, animales[0].id)
        print(f"✅ get_habitats_no_asociados(): {len(habitats_disponibles)} hábitats disponibles")
        
except Exception as e:
    print(f"❌ Error en AnimalHabitatRepository: {e}")

print("\n" + "=" * 60)
print("🎉 Pruebas completadas!")
print("\n💡 Si todos los tests muestran ✅, ¡todo funciona correctamente!")
print("   Ahora puedes ejecutar: python main.py")
