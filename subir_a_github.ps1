# Script para configurar Git y subir a GitHub
# Usuario: Lau-hidalgo

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 79) -ForegroundColor Cyan
Write-Host "🚀 CONFIGURACIÓN GIT Y GITHUB" -ForegroundColor Green
Write-Host ("=" * 80) -ForegroundColor Cyan
Write-Host ""

# Verificar si Git está instalado
Write-Host "📋 Verificando Git..." -ForegroundColor Yellow
try {
    $gitVersion = git --version
    Write-Host "✅ Git instalado: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git NO está instalado" -ForegroundColor Red
    Write-Host "Descárgalo desde: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 79) -ForegroundColor Cyan
Write-Host "PASO 1: Configurar Git" -ForegroundColor Yellow
Write-Host ("=" * 80) -ForegroundColor Cyan
Write-Host ""

# Configurar usuario
Write-Host "Configurando usuario de Git..." -ForegroundColor Yellow
git config --global user.name "Laura Hidalgo"
git config --global user.email "lau.hidalgo@example.com"
Write-Host "✅ Git configurado" -ForegroundColor Green

# Mostrar configuración
Write-Host ""
Write-Host "Configuración actual:" -ForegroundColor Cyan
git config --list | Select-String "user."

Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 79) -ForegroundColor Cyan
Write-Host "PASO 2: Inicializar repositorio Git" -ForegroundColor Yellow
Write-Host ("=" * 80) -ForegroundColor Cyan
Write-Host ""

# Inicializar Git si no está inicializado
if (Test-Path ".git") {
    Write-Host "✅ Ya es un repositorio Git" -ForegroundColor Green
} else {
    Write-Host "Inicializando repositorio..." -ForegroundColor Yellow
    git init
    Write-Host "✅ Repositorio Git inicializado" -ForegroundColor Green
}

Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 79) -ForegroundColor Cyan
Write-Host "PASO 3: Agregar archivos" -ForegroundColor Yellow
Write-Host ("=" * 80) -ForegroundColor Cyan
Write-Host ""

Write-Host "Agregando archivos al staging..." -ForegroundColor Yellow
git add .
Write-Host "✅ Archivos agregados" -ForegroundColor Green

Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 79) -ForegroundColor Cyan
Write-Host "PASO 4: Hacer commit" -ForegroundColor Yellow
Write-Host ("=" * 80) -ForegroundColor Cyan
Write-Host ""

Write-Host "Creando commit..." -ForegroundColor Yellow
git commit -m "feat: Aplicación web completa con login, usuarios y DevOps"
Write-Host "✅ Commit creado" -ForegroundColor Green

Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 79) -ForegroundColor Cyan
Write-Host "PASO 5: Configurar repositorio remoto" -ForegroundColor Yellow
Write-Host ("=" * 80) -ForegroundColor Cyan
Write-Host ""

# Nombre del repositorio
$repoName = "login-webapp"
$githubUser = "Lau-hidalgo"
$repoUrl = "https://github.com/$githubUser/$repoName.git"

Write-Host "Repositorio remoto: $repoUrl" -ForegroundColor Cyan
Write-Host ""

# Verificar si ya existe el remote
$existingRemote = git remote get-url origin 2>$null
if ($existingRemote) {
    Write-Host "⚠️  Remote 'origin' ya existe: $existingRemote" -ForegroundColor Yellow
    $cambiar = Read-Host "¿Quieres cambiarlo? (s/n)"
    if ($cambiar -eq 's') {
        git remote remove origin
        git remote add origin $repoUrl
        Write-Host "✅ Remote actualizado" -ForegroundColor Green
    }
} else {
    git remote add origin $repoUrl
    Write-Host "✅ Remote agregado" -ForegroundColor Green
}

Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 79) -ForegroundColor Cyan
Write-Host "PASO 6: Configurar rama principal" -ForegroundColor Yellow
Write-Host ("=" * 80) -ForegroundColor Cyan
Write-Host ""

Write-Host "Configurando rama 'main'..." -ForegroundColor Yellow
git branch -M main
Write-Host "✅ Rama configurada" -ForegroundColor Green

Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 79) -ForegroundColor Cyan
Write-Host "📝 INSTRUCCIONES FINALES" -ForegroundColor Yellow
Write-Host ("=" * 80) -ForegroundColor Cyan
Write-Host ""

Write-Host "PASO A: Crear cuenta en Docker Hub (si no la tienes)" -ForegroundColor Cyan
Write-Host "1. Ve a: https://hub.docker.com/signup" -ForegroundColor White
Write-Host "2. Crea una cuenta y verifica tu email" -ForegroundColor White
Write-Host "3. Recuerda tu username (ej: lauhidalgo)" -ForegroundColor White
Write-Host ""

$dockerUser = Read-Host "¿Cuál es tu usuario de Docker Hub?"

Write-Host ""
Write-Host "PASO B: Crear Access Token en Docker Hub" -ForegroundColor Cyan
Write-Host "1. Ve a: https://hub.docker.com" -ForegroundColor White
Write-Host "2. Account Settings → Security → New Access Token" -ForegroundColor White
Write-Host "3. Nombre: github-actions" -ForegroundColor White
Write-Host "4. Permissions: Read, Write, Delete" -ForegroundColor White
Write-Host "5. COPIA Y GUARDA EL TOKEN (solo lo verás una vez)" -ForegroundColor White
Write-Host ""

Read-Host "Presiona ENTER cuando hayas creado el token"

Write-Host ""
Write-Host "PASO C: Actualizar docker-compose.yml" -ForegroundColor Cyan
Write-Host "IMPORTANTE: Abre el archivo docker-compose.yml y cambia:" -ForegroundColor Yellow
Write-Host "   Línea 22: image: lauhidalgo/webclase:latest" -ForegroundColor White
Write-Host "   Cambia 'lauhidalgo' por: $dockerUser" -ForegroundColor White
Write-Host ""

Read-Host "Presiona ENTER cuando hayas actualizado el archivo"

Write-Host ""
Write-Host "PASO D: Crear repositorio en GitHub" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Ve a: https://github.com/new" -ForegroundColor White
Write-Host "2. Repository name: $repoName" -ForegroundColor White
Write-Host "3. Description: Aplicación web con FastAPI y MySQL" -ForegroundColor White
Write-Host "4. Public o Private (tu elección)" -ForegroundColor White
Write-Host "5. NO marques: Add README, .gitignore, license" -ForegroundColor White
Write-Host "6. Click en 'Create repository'" -ForegroundColor White
Write-Host ""

$continuar = Read-Host "¿Ya creaste el repositorio en GitHub? (s/n)"

if ($continuar -eq 's') {
    Write-Host ""
    Write-Host "=" -NoNewline -ForegroundColor Cyan
    Write-Host ("=" * 79) -ForegroundColor Cyan
    Write-Host "PASO 7: Subir a GitHub" -ForegroundColor Yellow
    Write-Host ("=" * 80) -ForegroundColor Cyan
    Write-Host ""
    
    Write-Host "Subiendo código a GitHub..." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "⚠️  Se te pedirá autenticación:" -ForegroundColor Yellow
    Write-Host "   Username: $githubUser" -ForegroundColor White
    Write-Host "   Password: [usa tu contraseña de GitHub]" -ForegroundColor White
    Write-Host ""
    
    git push -u origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "=" -NoNewline -ForegroundColor Green
        Write-Host ("=" * 79) -ForegroundColor Green
        Write-Host "✅ ¡CÓDIGO SUBIDO EXITOSAMENTE!" -ForegroundColor Green
        Write-Host ("=" * 80) -ForegroundColor Green
        Write-Host ""
        Write-Host "🎯 Próximos pasos:" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "1. Ve a tu repositorio: https://github.com/$githubUser/$repoName" -ForegroundColor White
        Write-Host "2. Configura los Secrets para Docker Hub (ver CHECKLIST_DEVOPS.md)" -ForegroundColor White
        Write-Host "3. GitHub Actions se ejecutará automáticamente" -ForegroundColor White
        Write-Host ""
    } else {
        Write-Host ""
        Write-Host "❌ Error al subir el código" -ForegroundColor Red
        Write-Host "Verifica tu usuario y contraseña de GitHub" -ForegroundColor Yellow
    }
} else {
    Write-Host ""
    Write-Host "⏸️  Proceso pausado" -ForegroundColor Yellow
    Write-Host "Cuando hayas creado el repositorio, ejecuta:" -ForegroundColor Cyan
    Write-Host "   git push -u origin main" -ForegroundColor White
}

Write-Host ""
