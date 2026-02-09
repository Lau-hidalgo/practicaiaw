from fastapi import Request, HTTPException, status
from fastapi.responses import RedirectResponse
from typing import Optional
from data.usuario_repository import UsuarioRepository
from data.database import database


def obtener_usuario_actual(request: Request) -> Optional[dict]:
    if not request.session or not request.session.get("authenticated"):
        return None
    
    return {
        "user_id": request.session.get("user_id"),
        "username": request.session.get("username"),
        "rol": request.session.get("rol")
    }


def require_login(request: Request) -> dict:
    usuario = obtener_usuario_actual(request)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail="Debe iniciar sesión",
            headers={"Location": "/login"}
        )
    return usuario


def require_admin(request: Request) -> dict:
    usuario = obtener_usuario_actual(request)
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail="Debe iniciar sesión",
            headers={"Location": "/login"}
        )
    
    if usuario.get("rol") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Se requieren privilegios de administrador."
        )
    
    return usuario


def crear_sesion(request: Request, usuario):
    """Crea una sesión para el usuario autenticado"""
    request.session["user_id"] = usuario.id
    request.session["username"] = usuario.username
    request.session["rol"] = usuario.rol
    request.session["authenticated"] = True


def destruir_sesion(request: Request):
    """Destruye la sesión del usuario"""
    request.session.clear()


def is_authenticated(request: Request) -> bool:
    """Verifica si hay un usuario autenticado"""
    return obtener_usuario_actual(request) is not None


def is_admin(request: Request) -> bool:
    """Verifica si el usuario actual es administrador"""
    usuario = obtener_usuario_actual(request)
    return usuario is not None and usuario.get("rol") == "admin"
