# 🚀 Web Login App - FastAPI + MySQL + DevOps

Sistema de login y gestión de usuarios con **actualización automática** mediante WatchTower.

## ✨ Características

- ✅ Login y registro de usuarios
- ✅ Contraseñas hasheadas (bcrypt)
- ✅ Roles: Admin / Usuario
- ✅ Base de datos MySQL remota
- ✅ **Actualización automática cada 1 minuto con WatchTower**
- ✅ CI/CD con GitHub Actions

## 🔄 Flujo DevOps Automático

```
Tú haces cambios → Git Push → GitHub Actions → Docker Hub → WatchTower → ¡App Actualizada!
                                (construye)       (imagen)      (detecta)    (1 minuto)
```

## 🚀 Inicio Rápido

### 1. Configurar Entorno

```bash
# Clonar repositorio
git clone https://github.com/Lau-hidalgo/login-webapp.git
cd login-webapp

# Instalar dependencias
cd webclase
pip install -r requirements.txt
```

### 2. Ejecutar Localmente

```bash
# Desde la carpeta webclase/
python main.py
```

Abre: http://127.0.0.1:8000

### 3. Con Docker

```bash
# Iniciar todos los servicios (app + db + watchtower)
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```

## 📦 Estructura

```
login-webapp/
├── webclase/               # Código de la aplicación
│   ├── main.py            # App FastAPI
│   ├── data/              # Repositorios y DB
│   ├── domain/            # Modelos
│   ├── templates/         # HTML
│   └── static/            # CSS, JS
├── .github/
│   └── workflows/         # GitHub Actions
├── Dockerfile             # Imagen Docker
├── docker-compose.yml     # Orquestación (app + watchtower)
└── README.md
```

## 🐳 Docker Compose

El archivo `docker-compose.yml` incluye:

1. **db**: MySQL 8.0
2. **web**: Tu aplicación FastAPI
3. **watchtower**: Actualización automática cada 1 minuto

```yaml
watchtower:
  environment:
    - WATCHTOWER_POLL_INTERVAL=60  # Revisa cada 1 minuto
    - WATCHTOWER_CLEANUP=true      # Limpia imágenes antiguas
```

## 🔧 Configuración DevOps

### 1. Docker Hub

1. Crea cuenta: https://hub.docker.com
2. Crea Access Token: Account Settings → Security → New Access Token
3. Guarda el token

### 2. GitHub Secrets

Ve a: `Settings → Secrets → Actions → New repository secret`

Añade:
- **DOCKER_USERNAME**: tu usuario de Docker Hub
- **DOCKER_PASSWORD**: el Access Token

### 3. Actualizar docker-compose.yml

Línea 22, cambia:
```yaml
image: TU_USUARIO_DOCKER/webclase:latest
```

## 🚀 Despliegue Automático

### Primera vez:

```bash
# 1. Hacer cambios
git add .
git commit -m "feat: nueva funcionalidad"
git push

# 2. GitHub Actions construye y sube imagen
# 3. En tu servidor:
docker-compose up -d
```

### Después (automático):

```bash
# Solo haz cambios y push
git add .
git commit -m "fix: corrección"
git push

# WatchTower actualizará automáticamente en ~1 minuto
# ¡No necesitas hacer nada más!
```

## 📊 Monitoreo

```bash
# Ver logs de WatchTower
docker logs watchtower -f

# Ver logs de la app
docker logs webclase_app -f

# Ver todos los logs
docker-compose logs -f
```

Cuando WatchTower detecte una actualización verás:
```
Found new TU_USUARIO/webclase:latest image
Stopping /webclase_app
Starting /webclase_app
```

## 🛠️ Tecnologías

- **Backend**: FastAPI (Python 3.11)
- **Base de Datos**: MySQL 8.0
- **Autenticación**: bcrypt + sesiones
- **Contenedores**: Docker + Docker Compose
- **CI/CD**: GitHub Actions
- **Auto-deploy**: WatchTower

## 📝 Comandos Útiles

```bash
# Ver contenedores
docker ps

# Reiniciar un servicio
docker-compose restart web

# Ver uso de recursos
docker stats

# Forzar actualización
docker-compose pull web
docker-compose up -d web

# Limpiar todo
docker-compose down -v
```

## 🎯 Usuarios de Prueba

Los usuarios se gestionan en DBeaver:
- Host: `informatica.iesquevedo.es:3333`
- Base de datos: `laura`
- Tabla: `users`

## 🆘 Troubleshooting

### WatchTower no actualiza
```bash
# Ver logs
docker logs watchtower

# Verificar configuración
docker inspect watchtower
```

### GitHub Actions falla
- Verifica que los secrets estén configurados
- Revisa los logs en: Actions → Click en el workflow

### App no inicia
```bash
# Ver error
docker logs webclase_app

# Reiniciar
docker-compose restart web
```

## 📚 Documentación Adicional

- [CHECKLIST_DEVOPS.md](CHECKLIST_DEVOPS.md) - Guía paso a paso completa

## 👤 Autor

**Laura Hidalgo** - [Lau-hidalgo](https://github.com/Lau-hidalgo)

## 📄 Licencia

MIT License - ver [LICENSE](LICENSE)

---

⭐ Si te gusta el proyecto, dale una estrella en GitHub!
