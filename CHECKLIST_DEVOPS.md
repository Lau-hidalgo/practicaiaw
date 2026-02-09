# ✅ CHECKLIST COMPLETO - DevOps con WatchTower

## 📦 REQUISITOS PREVIOS

### 1. Instalar Git
- [ ] Descargar Git desde: https://git-scm.com/download/win
- [ ] Ejecutar el instalador (Next, Next, Finish)
- [ ] Abrir PowerShell y verificar: `git --version`

### 2. Crear cuenta en Docker Hub
- [ ] Ir a: https://hub.docker.com/signup
- [ ] Registrarte con email y contraseña
- [ ] Verificar email
- [ ] Recordar tu username: `__________________`

### 3. Crear Access Token en Docker Hub
- [ ] Ir a: https://hub.docker.com
- [ ] Click en tu usuario (arriba derecha) → Account Settings
- [ ] Security → New Access Token
- [ ] Nombre: `github-actions`
- [ ] Permissions: Read, Write, Delete
- [ ] Click en "Generate"
- [ ] **COPIAR Y GUARDAR EL TOKEN** (solo lo verás una vez)
- [ ] Token: `_______________________________________________`

### 4. Crear repositorio en GitHub
- [ ] Ir a: https://github.com/new
- [ ] Repository name: `login-webapp`
- [ ] Description: `Aplicación web con FastAPI, MySQL y DevOps`
- [ ] Public o Private (tu elección)
- [ ] **NO marcar**: Add README, .gitignore, license
- [ ] Click en "Create repository"
- [ ] URL del repo: `https://github.com/________/login-webapp`

---

## ⚙️ CONFIGURACIÓN

### 5. Configurar Secrets en GitHub
- [ ] Ir a tu repositorio en GitHub
- [ ] Settings → Secrets and variables → Actions
- [ ] Click en "New repository secret"

**Secret 1:**
- [ ] Name: `DOCKER_USERNAME`
- [ ] Value: [tu usuario de Docker Hub]
- [ ] Click "Add secret"

**Secret 2:**
- [ ] Name: `DOCKER_PASSWORD`
- [ ] Value: [el Access Token que guardaste]
- [ ] Click "Add secret"

### 6. Actualizar docker-compose.yml
- [ ] Abrir archivo: `docker-compose.yml`
- [ ] Buscar línea 22: `image: lauraiaw/webclase:latest`
- [ ] Cambiar `lauraiaw` por tu usuario de Docker Hub
- [ ] Ejemplo: `image: TU_USUARIO/webclase:latest`
- [ ] Guardar archivo (Ctrl+S)

### 7. Configurar Git en tu computadora
Abre PowerShell en tu proyecto:

```powershell
# Navegar al proyecto
cd c:\Users\laura\Desktop\asir2\iaw\2eva\login

# Configurar nombre
git config --global user.name "Tu Nombre"

# Configurar email
git config --global user.email "tu@email.com"

# Verificar
git config --list
```

- [ ] Comandos ejecutados ✅

---

## 🚀 SUBIR A GITHUB

### 8. Inicializar Git (si no está inicializado)

```powershell
# Verificar si ya es un repositorio
git status

# Si dice "not a git repository", ejecutar:
git init

# Configurar rama principal
git branch -M main
```

- [ ] Git inicializado ✅

### 9. Agregar remote de GitHub

```powershell
# Reemplaza TU_USUARIO con tu usuario de GitHub
git remote add origin https://github.com/TU_USUARIO/login-webapp.git

# Verificar
git remote -v
```

- [ ] Remote agregado ✅

### 10. Hacer primer commit

```powershell
# Ver archivos
git status

# Agregar todos los archivos
git add .

# Hacer commit
git commit -m "feat: Implementación completa con DevOps y WatchTower"

# Ver historial
git log --oneline
```

- [ ] Commit realizado ✅

### 11. Subir a GitHub

```powershell
# Subir a GitHub
git push -u origin main

# Si pide autenticación:
# 1. Username: tu usuario de GitHub
# 2. Password: usa un Personal Access Token (NO tu contraseña)
```

**Si pide Personal Access Token:**
- [ ] Ir a: https://github.com/settings/tokens
- [ ] Click "Generate new token (classic)"
- [ ] Note: `git-access`
- [ ] Expiration: 90 days
- [ ] Scopes: marcar `repo`
- [ ] Generate token
- [ ] Copiar token y usarlo como password
- [ ] Token: `_______________________________________________`

- [ ] Código subido a GitHub ✅

---

## ✅ VERIFICACIÓN

### 12. Verificar GitHub Actions

- [ ] Ir a: https://github.com/TU_USUARIO/login-webapp/actions
- [ ] Deberías ver un workflow ejecutándose
- [ ] Esperar a que termine (~3-5 minutos)
- [ ] Estado final debe ser: ✅ (verde)

Si falla:
- Revisar que los Secrets estén bien configurados
- Ver los logs del workflow para el error

### 13. Verificar Docker Hub

- [ ] Ir a: https://hub.docker.com/r/TU_USUARIO/webclase
- [ ] Deberías ver la imagen con tag `latest`
- [ ] Debería aparecer "Last pushed: hace unos minutos"

### 14. Ejecutar en tu servidor

```powershell
# Iniciar todos los servicios
docker-compose up -d

# Ver logs
docker-compose logs -f

# Deberías ver:
# - db: MySQL iniciando
# - web: FastAPI corriendo en puerto 8000
# - watchtower: Monitoring started
```

- [ ] Contenedores corriendo ✅

### 15. Verificar WatchTower

```powershell
# Ver logs de WatchTower
docker logs watchtower

# Debería mostrar:
# "Watchtower 1.x.x"
# "Running a one time update."
# "Checking lauraiaw/webclase:latest"
```

- [ ] WatchTower funcionando ✅

---

## 🧪 PROBAR EL FLUJO COMPLETO

### 16. Hacer un cambio de prueba

```powershell
# Editar README o cualquier archivo
echo "# Test DevOps" >> TEST.md

# Commit y push
git add .
git commit -m "test: Probando flujo DevOps"
git push
```

- [ ] Cambio subido ✅

### 17. Monitorear el proceso

```powershell
# Ver GitHub Actions (navegador)
# https://github.com/TU_USUARIO/login-webapp/actions

# Ver WatchTower (terminal)
docker logs watchtower -f

# Esperar ~5-10 minutos
```

Deberías ver:
1. GitHub Actions construyendo (navegador)
2. Imagen subida a Docker Hub
3. WatchTower detectando nueva imagen:
   ```
   Found new TU_USUARIO/webclase:latest image
   Stopping /webclase_app (abc123)
   Starting /webclase_app
   ```

- [ ] Actualización automática funcionó ✅

---

## 🎯 RESULTADO FINAL

Si todos los ítems están marcados:

✅ Git configurado
✅ Código en GitHub
✅ GitHub Actions funcionando
✅ Imagen en Docker Hub
✅ WatchTower monitoreando
✅ Actualización automática probada

**¡FELICIDADES! Tu proceso DevOps está completo.**

---

## 📝 COMANDOS DE REFERENCIA RÁPIDA

```powershell
# Desarrollo diario
git add .
git commit -m "feat: nueva funcionalidad"
git push

# Ver estado de servicios
docker ps
docker logs watchtower --tail 50
docker logs webclase_app --tail 50

# Reiniciar servicios
docker-compose restart web
docker-compose restart watchtower

# Detener todo
docker-compose down

# Iniciar todo
docker-compose up -d

# Ver logs en tiempo real
docker-compose logs -f
```

---

## 🆘 AYUDA

Si algo falla:

1. **GitHub Actions falla**
   - Revisar logs en GitHub → Actions → Click en el workflow
   - Verificar secrets en Settings → Secrets

2. **WatchTower no actualiza**
   - `docker logs watchtower`
   - `docker-compose pull web`
   - `docker-compose up -d web`

3. **Contenedor no inicia**
   - `docker logs webclase_app`
   - `docker-compose down && docker-compose up -d`

---

## ✨ ¡LISTO!

Ahora cada vez que hagas `git push`, tu aplicación se actualizará automáticamente en producción. 🚀
