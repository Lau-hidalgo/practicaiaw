# Script para auto-commit y push automático
# Ejecutar este script cada vez que hagas cambios

param(
    [string]$mensaje = "Auto-update: Cambios guardados"
)

Write-Host "🔄 Sincronizando cambios con GitHub..." -ForegroundColor Cyan

# Agregar todos los cambios
git add .

# Verificar si hay cambios
$status = git status --porcelain
if ([string]::IsNullOrWhiteSpace($status)) {
    Write-Host "✅ No hay cambios para sincronizar" -ForegroundColor Green
    exit 0
}

# Mostrar archivos modificados
Write-Host "📝 Archivos modificados:" -ForegroundColor Yellow
git status --short

# Hacer commit
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
git commit -m "$mensaje - $timestamp"

# Push a GitHub
Write-Host "⬆️ Subiendo a GitHub..." -ForegroundColor Cyan
git push

Write-Host "✅ Cambios sincronizados exitosamente!" -ForegroundColor Green
