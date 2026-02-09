# Script para inicializar Git y subir a GitHub
# Ejecutar después de instalar Git

Write-Host "🚀 Iniciando proceso DevOps..." -ForegroundColor Green

# Verificar si Git está instalado
try {
    $gitVersion = git --version
    Write-Host "✅ Git instalado: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git no está instalado. Descárgalo de: https://git-scm.com/download/win" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "📝 Configurando Git..." -ForegroundColor Cyan
$nombre = Read-Host "Ingresa tu nombre"
$email = Read-Host "Ingresa tu email"

git config --global user.name "$nombre"
git config --global user.email "$email"

Write-Host "✅ Configuración completada" -ForegroundColor Green

Write-Host ""
Write-Host "📦 Inicializando repositorio..." -ForegroundColor Cyan
git init

Write-Host "📁 Agregando archivos..." -ForegroundColor Cyan
git add .

Write-Host "💾 Creando commit inicial..." -ForegroundColor Cyan
git commit -m "Initial commit: Sistema completo de gestión de animales marinos con FastAPI"

Write-Host ""
Write-Host "🌐 Conectando con GitHub..." -ForegroundColor Cyan
Write-Host "Primero crea un repositorio en GitHub (https://github.com/new)" -ForegroundColor Yellow
Write-Host ""

$username = Read-Host "Ingresa tu usuario de GitHub"
$reponame = Read-Host "Ingresa el nombre del repositorio (ej: gestion-animales-marinos)"

git remote add origin "https://github.com/$username/$reponame.git"
git branch -M main

Write-Host ""
Write-Host "🚀 Subiendo código a GitHub..." -ForegroundColor Cyan
git push -u origin main

Write-Host ""
Write-Host "✅ ¡Proceso completado exitosamente!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Próximos pasos:" -ForegroundColor Yellow
Write-Host "1. Instalar WakaTime en VS Code"
Write-Host "2. Verificar GitHub Actions en tu repositorio"
Write-Host "3. Ver estadísticas en https://wakatime.com/dashboard"
Write-Host ""
Write-Host "📖 Consulta DEVOPS.md para más información" -ForegroundColor Cyan
