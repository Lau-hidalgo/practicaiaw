from typing import Annotated
from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from typing import Optional
import os
from pathlib import Path
from data.database import database
from data.animalesmarinos_repository import AnimalesMarinosRepository
from data.usuario_repository import UsuarioRepository
from data.habitat_repository import HabitatRepository
from data.animal_habitat_repository import AnimalHabitatRepository
from data.pais_repository import PaisRepository
from data.comentario_repository import ComentarioRepository
from domain.model.AnimalMarino import AnimalMarino
from domain.model.Habitat import Habitat
from utils.auth_dependencies import (
    require_login, 
    require_admin, 
    crear_sesion, 
    destruir_sesion,
    obtener_usuario_actual,
    is_admin
)
import uvicorn

# Obtener el directorio base del proyecto
BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="Mi Primera Web FastAPI", description="Ejemplo básico con Jinja2")

SECRET_KEY = "tu_clave_secreta_muy_segura_cambiala_en_produccion"
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


@app.exception_handler(403)
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc):
    if exc.status_code == 403:
        usuario = obtener_usuario_actual(request)
        return templates.TemplateResponse(
            "error_403.html",
            {
                "request": request,
                "usuario": usuario,
                "is_admin": is_admin(request)
            },
            status_code=403
        )
    
    if exc.status_code == 303:
        return RedirectResponse(url=exc.headers.get("Location", "/login"), status_code=303)
    
    return templates.TemplateResponse(
        "error_403.html",
        {
            "request": request,
            "error_message": exc.detail,
            "usuario": obtener_usuario_actual(request),
            "is_admin": is_admin(request)
        },
        status_code=exc.status_code
    )

@app.get("/")
async def inicio(request: Request):
    usuario = obtener_usuario_actual(request)
    
    if not usuario:
        return RedirectResponse(url="/login", status_code=303)
    
    return RedirectResponse(url="/animalesmarinos", status_code=303)

@app.post("/do_insertar_animalesmarinos")
async def do_insertar_animalesmarinos(
    request: Request,
    nombre: Annotated[str, Form()] = None,
    imagen_url: Annotated[str, Form()] = None,
    habitats: Annotated[list[str], Form()] = [],
    pais_id: Annotated[str, Form()] = None,
    poblacion: Annotated[str, Form()] = None,
    estado: Annotated[str, Form()] = None,
    usuario: dict = Depends(require_admin)
):
    repo = AnimalesMarinosRepository()
    # Si no se proporciona imagen, usar imagen por defecto
    if not imagen_url:
        imagen_url = 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=400&h=400&fit=crop'
    
    animal = AnimalMarino(0, nombre, imagen_url)
    repo.insertar_animal(database, animal)
    
    # Obtener el ID del animal recién insertado
    cursor = database.cursor()
    cursor.execute("SELECT LAST_INSERT_ID()")
    animal_id = cursor.fetchone()[0]
    cursor.close()
    
    # Crear asociaciones con hábitats si se seleccionaron
    if habitats:
        ah_repo = AnimalHabitatRepository()
        pais = int(pais_id) if pais_id else None
        pob = int(poblacion) if poblacion else None
        
        for habitat_id in habitats:
            ah_repo.asociar_animal_habitat(
                database, 
                animal_id, 
                int(habitat_id), 
                pob, 
                estado, 
                pais
            )

    return templates.TemplateResponse("do_insert_animalesmarinos.html", {
        "request": request,
        "usuario": usuario,
        "is_admin": True
    })


@app.get("/insert_animalesmarinos")
async def insert_animalesmarinos(
    request: Request,
    usuario: dict = Depends(require_admin)
):
    habitat_repo = HabitatRepository()
    pais_repo = PaisRepository()
    habitats = habitat_repo.get_all(database)
    paises_por_continente = pais_repo.get_by_continente(database)
    
    return templates.TemplateResponse("insert_animalesmarinos.html", {
        "request": request,
        "usuario": usuario,
        "is_admin": True,
        "habitats": habitats,
        "paises_por_continente": paises_por_continente
    })


@app.get("/borrar_animalesmarinos")
async def borrar_animalesmarinos(
    request: Request,
    usuario: dict = Depends(require_admin)
):
    """Formulario para borrar animales marinos - Solo administradores"""
    repo = AnimalesMarinosRepository()
    animales = repo.get_all(database)

    return templates.TemplateResponse("borrar_animalesmarinos.html", {
        "request": request,
        "animales": animales,
        "usuario": usuario,
        "is_admin": True
    })



# RUTA BORRAR (acción) - Solo Admin
@app.post("/do_borrar_animalesmarinos")
async def do_borrar_animalesmarinos(
    request: Request,
    id: Annotated[str, Form()] = None,
    usuario: dict = Depends(require_admin)
):
    """Borrar un animal marino por id - Solo administradores"""
    repo = AnimalesMarinosRepository()
    repo.borrar_animal(database, int(id))

    return templates.TemplateResponse("do_borrar_animalesmarinos.html", {
        "request": request,
        "usuario": usuario,
        "is_admin": True
    })


# RUTA ACTUALIZAR (formulario) - Solo Admin
@app.get("/update_animalesmarinos")
async def update_animalesmarinos(
    request: Request,
    usuario: dict = Depends(require_admin)
):
    """Formulario para actualizar animales marinos - Solo administradores"""
    repo = AnimalesMarinosRepository()
    habitat_repo = HabitatRepository()
    pais_repo = PaisRepository()
    ah_repo = AnimalHabitatRepository()
    
    animales = repo.get_all(database)
    habitats = habitat_repo.get_all(database)
    paises_por_continente = pais_repo.get_by_continente(database)

    return templates.TemplateResponse("update_animalesmarinos.html", {
        "request": request,
        "animales": animales,
        "habitats": habitats,
        "paises_por_continente": paises_por_continente,
        "usuario": usuario,
        "is_admin": True
    })


# RUTA ACTUALIZAR (acción) - Solo Admin
@app.post("/do_update_animalesmarinos")
async def do_update_animalesmarinos(
    request: Request,
    id: Annotated[str, Form()] = None,
    nombre: Annotated[str, Form()] = None,
    imagen_url: Annotated[str, Form()] = None,
    habitats: Annotated[list[str], Form()] = [],
    pais_id: Annotated[str, Form()] = None,
    poblacion: Annotated[str, Form()] = None,
    estado: Annotated[str, Form()] = None,
    usuario: dict = Depends(require_admin)
):
    """Actualizar el nombre, imagen y hábitats de un animal marino - Solo administradores"""
    repo = AnimalesMarinosRepository()
    ah_repo = AnimalHabitatRepository()
    
    if id is not None and nombre is not None:
        # Actualizar animal - si imagen_url está vacío, pasamos None para mantener la actual
        img_url = imagen_url.strip() if imagen_url and imagen_url.strip() else None
        repo.actualizar_animal(database, int(id), nombre, img_url)
        
        # Si se seleccionaron hábitats, actualizar asociaciones
        if habitats:
            # Primero eliminar asociaciones existentes
            cursor = database.cursor()
            cursor.execute("DELETE FROM animales_habitats WHERE animal_id = %s", (int(id),))
            database.commit()
            cursor.close()
            
            # Crear nuevas asociaciones
            pais = int(pais_id) if pais_id else None
            pob = int(poblacion) if poblacion else None
            
            for habitat_id in habitats:
                ah_repo.asociar_animal_habitat(
                    database, 
                    int(id), 
                    int(habitat_id), 
                    pob, 
                    estado, 
                    pais
                )

    return templates.TemplateResponse("do_update_animalesmarinos.html", {
        "request": request,
        "usuario": usuario,
        "is_admin": True
    })



# RUTAS GET
@app.get("/animalesmarinos", response_class=HTMLResponse)
async def animalesmarinos(
    request: Request,
    usuario: dict = Depends(require_login)
):
    """Listar animales marinos - requiere login (todos los usuarios autenticados)"""
    repo = AnimalesMarinosRepository()
    animales = repo.get_all(database)

    return templates.TemplateResponse("animalesmarinos.html", {
        "request": request,
        "animales": animales,
        "usuario": usuario,
        "is_admin": is_admin(request)
    })


# ============== RUTAS DE AUTENTICACIÓN ==============

@app.get("/login")
async def login_form(request: Request):
    """Formulario de login"""
    # Si ya está autenticado, redirigir a inicio
    usuario = obtener_usuario_actual(request)
    if usuario:
        return RedirectResponse(url="/", status_code=303)
    
    return templates.TemplateResponse("login.html", {
        "request": request,
        "error": None
    })


@app.post("/login")
async def login(
    request: Request,
    username: Annotated[str, Form()],
    password: Annotated[str, Form()]
):
    """Procesar login"""
    usuario_repo = UsuarioRepository()
    
    # Buscar usuario por username
    usuario = usuario_repo.get_by_username(database, username)
    
    # Verificar usuario y contraseña
    if not usuario or not usuario_repo.verificar_password(password, usuario.password_hash):
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Usuario o contraseña incorrectos"
        })
    
    # Crear sesión
    crear_sesion(request, usuario)
    
    # Redirigir a la página principal
    return RedirectResponse(url="/", status_code=303)


@app.get("/logout")
async def logout(request: Request):
    """Cerrar sesión"""
    destruir_sesion(request)
    return RedirectResponse(url="/", status_code=303)


@app.get("/registro")
async def registro_form(request: Request):
    """Formulario de registro"""
    # Si ya está autenticado, redirigir a inicio
    usuario = obtener_usuario_actual(request)
    if usuario:
        return RedirectResponse(url="/", status_code=303)
    
    return templates.TemplateResponse("registro.html", {
        "request": request,
        "error": None,
        "success": None
    })


@app.post("/registro")
async def registro(
    request: Request,
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    password_confirm: Annotated[str, Form()],
    email: Annotated[str, Form()] = None,
):
    """Procesar registro de nuevo usuario"""
    usuario_repo = UsuarioRepository()
    
    # Validaciones
    if not username or len(username) < 3:
        return templates.TemplateResponse("registro.html", {
            "request": request,
            "error": "El nombre de usuario debe tener al menos 3 caracteres",
            "success": None
        })
    
    if not password or len(password) < 6:
        return templates.TemplateResponse("registro.html", {
            "request": request,
            "error": "La contraseña debe tener al menos 6 caracteres",
            "success": None
        })
    
    if password != password_confirm:
        return templates.TemplateResponse("registro.html", {
            "request": request,
            "error": "Las contraseñas no coinciden",
            "success": None
        })
    
    # Verificar si el usuario ya existe
    if usuario_repo.get_by_username(database, username):
        return templates.TemplateResponse("registro.html", {
            "request": request,
            "error": "El nombre de usuario ya está en uso",
            "success": None
        })
    
    # Crear el usuario
    try:
        print(f"📝 Iniciando registro de usuario: {username}")
        usuario_repo.insertar_usuario(database, username, password, email=email, rol="usuario")
        print(f"✅ Registro completado para: {username}")
        
        # Redirigir al login con mensaje de éxito
        return templates.TemplateResponse("registro.html", {
            "request": request,
            "error": None,
            "success": "Usuario creado exitosamente. Ahora puedes iniciar sesión."
        })
    except Exception as e:
        print(f"❌ ERROR en registro: {str(e)}")
        import traceback
        traceback.print_exc()
        return templates.TemplateResponse("registro.html", {
            "request": request,
            "error": f"Error al crear el usuario: {str(e)}",
            "success": None
        })


# ============== RUTAS DE HÁBITATS ==============

@app.get("/habitats", response_class=HTMLResponse)
async def habitats(
    request: Request,
    usuario: dict = Depends(require_login)
):
    """Listar hábitats - requiere login"""
    repo = HabitatRepository()
    habitats = repo.get_all(database)

    return templates.TemplateResponse("habitats.html", {
        "request": request,
        "habitats": habitats,
        "usuario": usuario,
        "is_admin": is_admin(request)
    })


# ==================== RUTAS DE PAÍSES ====================

@app.get("/paises", response_class=HTMLResponse)
async def paises(
    request: Request,
    usuario: dict = Depends(require_login)
):
    """Listar países - requiere login"""
    repo = PaisRepository()
    paises = repo.get_all(database)

    return templates.TemplateResponse("paises.html", {
        "request": request,
        "paises": paises,
        "usuario": usuario,
        "is_admin": is_admin(request)
    })


@app.get("/pais/{pais_id}/animales", response_class=HTMLResponse)
async def pais_animales(
    request: Request,
    pais_id: int,
    usuario: dict = Depends(require_login)
):
    """Ver animales de un país específico - requiere login"""
    repo = PaisRepository()
    pais = repo.get_by_id(database, pais_id)
    
    if not pais:
        raise HTTPException(status_code=404, detail="País no encontrado")
    
    animales = repo.get_animales_por_pais(database, pais_id)
    
    return templates.TemplateResponse("pais_animales.html", {
        "request": request,
        "pais": pais,
        "animales": animales,
        "usuario": usuario,
        "is_admin": is_admin(request)
    })


@app.get("/insert_habitats")
async def insert_habitats(
    request: Request,
    usuario: dict = Depends(require_admin)
):
    """Formulario para insertar hábitats - Solo administradores"""
    return templates.TemplateResponse("insert_habitats.html", {
        "request": request,
        "usuario": usuario,
        "is_admin": True
    })


@app.post("/do_insertar_habitats")
async def do_insertar_habitats(
    request: Request,
    nombre: Annotated[str, Form()] = None,
    descripcion: Annotated[str, Form()] = None,
    profundidad_min: Annotated[str, Form()] = None,
    profundidad_max: Annotated[str, Form()] = None,
    temperatura_media: Annotated[str, Form()] = None,
    usuario: dict = Depends(require_admin)
):
    """Insertar nuevo hábitat - Solo administradores"""
    repo = HabitatRepository()
    
    # Convertir valores vacíos a None
    prof_min = int(profundidad_min) if profundidad_min else None
    prof_max = int(profundidad_max) if profundidad_max else None
    temp = float(temperatura_media) if temperatura_media else None
    
    habitat = Habitat(0, nombre, descripcion, prof_min, prof_max, temp)
    repo.insertar_habitat(database, habitat)

    return templates.TemplateResponse("do_insert_habitats.html", {
        "request": request,
        "usuario": usuario,
        "is_admin": True
    })


@app.get("/update_habitats")
async def update_habitats(
    request: Request,
    usuario: dict = Depends(require_admin)
):
    """Formulario para actualizar hábitats - Solo administradores"""
    repo = HabitatRepository()
    habitats = repo.get_all(database)

    return templates.TemplateResponse("update_habitats.html", {
        "request": request,
        "habitats": habitats,
        "usuario": usuario,
        "is_admin": True
    })


@app.post("/do_update_habitats")
async def do_update_habitats(
    request: Request,
    id: Annotated[str, Form()] = None,
    nombre: Annotated[str, Form()] = None,
    descripcion: Annotated[str, Form()] = None,
    profundidad_min: Annotated[str, Form()] = None,
    profundidad_max: Annotated[str, Form()] = None,
    temperatura_media: Annotated[str, Form()] = None,
    usuario: dict = Depends(require_admin)
):
    """Actualizar hábitat - Solo administradores"""
    repo = HabitatRepository()
    
    if id and nombre:
        prof_min = int(profundidad_min) if profundidad_min else None
        prof_max = int(profundidad_max) if profundidad_max else None
        temp = float(temperatura_media) if temperatura_media else None
        
        repo.actualizar_habitat(database, int(id), nombre, descripcion, prof_min, prof_max, temp)

    return templates.TemplateResponse("do_update_habitats.html", {
        "request": request,
        "usuario": usuario,
        "is_admin": True
    })


@app.get("/borrar_habitats")
async def borrar_habitats(
    request: Request,
    usuario: dict = Depends(require_admin)
):
    """Formulario para borrar hábitats - Solo administradores"""
    repo = HabitatRepository()
    habitats = repo.get_all(database)

    return templates.TemplateResponse("borrar_habitats.html", {
        "request": request,
        "habitats": habitats,
        "usuario": usuario,
        "is_admin": True
    })


@app.post("/do_borrar_habitats")
async def do_borrar_habitats(
    request: Request,
    id: Annotated[str, Form()] = None,
    usuario: dict = Depends(require_admin)
):
    """Borrar hábitat - Solo administradores"""
    repo = HabitatRepository()
    repo.borrar_habitat(database, int(id))

    return templates.TemplateResponse("do_borrar_habitats.html", {
        "request": request,
        "usuario": usuario,
        "is_admin": True
    })


# ============== RUTAS DE ASOCIACIONES N-M ==============

@app.get("/animal/{animal_id}/habitats")
async def animal_habitats(
    request: Request,
    animal_id: int,
    usuario: dict = Depends(require_login)
):
    """Gestionar hábitats de un animal - requiere login"""
    animal_repo = AnimalesMarinosRepository()
    habitat_repo = HabitatRepository()
    ah_repo = AnimalHabitatRepository()
    pais_repo = PaisRepository()
    
    # Obtener el animal
    animal = animal_repo.get_by_id(database, animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal no encontrado")
    
    # Obtener hábitats asociados
    habitats_asociados = ah_repo.get_habitats_por_animal(database, animal_id)
    
    # Obtener hábitats disponibles (no asociados)
    habitats_disponibles = ah_repo.get_habitats_no_asociados(database, animal_id)
    
    # Obtener países agrupados por continente
    paises_por_continente = pais_repo.get_by_continente(database)

    return templates.TemplateResponse("animal_habitats.html", {
        "request": request,
        "animal": animal,
        "habitats_asociados": habitats_asociados,
        "habitats_disponibles": habitats_disponibles,
        "paises_por_continente": paises_por_continente,
        "usuario": usuario,
        "is_admin": is_admin(request)
    })


# ==================== RUTAS DE COMENTARIOS ====================

@app.get("/animal/{animal_id}/detalle", response_class=HTMLResponse)
async def animal_detalle(
    request: Request,
    animal_id: int,
    usuario: dict = Depends(require_login)
):
    """Ver detalle de un animal con comentarios"""
    animal_repo = AnimalesMarinosRepository()
    comentario_repo = ComentarioRepository()
    ah_repo = AnimalHabitatRepository()
    
    animal = animal_repo.get_by_id(database, animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal no encontrado")
    
    comentarios = comentario_repo.get_by_animal(database, animal_id)
    habitats = ah_repo.get_habitats_por_animal(database, animal_id)
    
    return templates.TemplateResponse("animal_detalle.html", {
        "request": request,
        "animal": animal,
        "comentarios": comentarios,
        "habitats": habitats,
        "usuario": usuario,
        "is_admin": is_admin(request)
    })


@app.post("/animal/{animal_id}/comentario")
async def agregar_comentario(
    request: Request,
    animal_id: int,
    comentario: Annotated[str, Form()],
    usuario: dict = Depends(require_login)
):
    """Agregar comentario a un animal"""
    comentario_repo = ComentarioRepository()
    comentario_repo.insertar(database, animal_id, usuario['username'], comentario)
    return RedirectResponse(url=f"/animal/{animal_id}/detalle", status_code=303)


@app.post("/comentario/{comentario_id}/borrar")
async def borrar_comentario(
    request: Request,
    comentario_id: int,
    usuario: dict = Depends(require_login)
):
    """Borrar un comentario (solo el autor o admin)"""
    comentario_repo = ComentarioRepository()
    
    if is_admin(request):
        # Admin puede borrar cualquier comentario
        comentario_repo.borrar(database, comentario_id)
    else:
        # Usuario normal solo puede borrar sus propios comentarios
        comentario_repo.borrar(database, comentario_id, usuario['username'])
    
    # Redirigir de vuelta al animal
    return RedirectResponse(url=request.headers.get('referer', '/animalesmarinos'), status_code=303)


@app.post("/asociar_animal_habitat")
async def asociar_animal_habitat(
    request: Request,
    animal_id: Annotated[int, Form()],
    habitat_id: Annotated[int, Form()],
    poblacion_estimada: Annotated[str, Form()] = None,
    estado_conservacion: Annotated[str, Form()] = None,
    pais_id: Annotated[str, Form()] = None,
    usuario: dict = Depends(require_login)
):
    """Asociar un animal con un hábitat - requiere login"""
    ah_repo = AnimalHabitatRepository()
    
    poblacion = int(poblacion_estimada) if poblacion_estimada else None
    estado = estado_conservacion if estado_conservacion else None
    pais = int(pais_id) if pais_id else None
    
    ah_repo.asociar_animal_habitat(database, animal_id, habitat_id, poblacion, estado, pais)
    
    return RedirectResponse(url=f"/animal/{animal_id}/habitats", status_code=303)


@app.post("/desasociar_animal_habitat")
async def desasociar_animal_habitat(
    request: Request,
    animal_id: Annotated[int, Form()],
    habitat_id: Annotated[int, Form()],
    usuario: dict = Depends(require_login)
):
    """Eliminar asociación entre animal y hábitat - requiere login"""
    ah_repo = AnimalHabitatRepository()
    ah_repo.desasociar_animal_habitat(database, animal_id, habitat_id)
    
    # Verificar si la solicitud viene de la página de asociaciones
    referer = request.headers.get("referer", "")
    if "/asociaciones" in referer:
        return RedirectResponse(url="/asociaciones", status_code=303)
    else:
        return RedirectResponse(url=f"/animal/{animal_id}/habitats", status_code=303)


@app.get("/habitat/{habitat_id}/animales")
async def habitat_animales(
    request: Request,
    habitat_id: int,
    usuario: dict = Depends(require_login)
):
    """Ver animales de un hábitat - requiere login"""
    habitat_repo = HabitatRepository()
    ah_repo = AnimalHabitatRepository()
    
    # Obtener el hábitat
    habitat = habitat_repo.get_by_id(database, habitat_id)
    if not habitat:
        raise HTTPException(status_code=404, detail="Hábitat no encontrado")
    
    # Obtener animales del hábitat
    animales = ah_repo.get_animales_por_habitat(database, habitat_id)

    return templates.TemplateResponse("habitat_animales.html", {
        "request": request,
        "habitat": habitat,
        "animales": animales,
        "usuario": usuario,
        "is_admin": is_admin(request)
    })


@app.get("/asociaciones")
async def asociaciones(
    request: Request,
    usuario: dict = Depends(require_login)
):
    """Ver todas las asociaciones - requiere login"""
    ah_repo = AnimalHabitatRepository()
    asociaciones = ah_repo.get_all_asociaciones(database)

    return templates.TemplateResponse("asociaciones.html", {
        "request": request,
        "asociaciones": asociaciones,
        "usuario": usuario,
        "is_admin": is_admin(request)
    })


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
