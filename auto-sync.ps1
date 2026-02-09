# Script de auto-sync que se ejecuta en segundo plano
# Monitorea cambios y los sube automáticamente a GitHub

param(
    [int]$intervalo = 300  # 5 minutos por defecto
)

Write-Host "🤖 Iniciando auto-sync..." -ForegroundColor Green
Write-Host "⏱️ Intervalo: $intervalo segundos" -ForegroundColor Cyan
Write-Host "⚠️ Presiona Ctrl+C para detener" -ForegroundColor Yellow
Write-Host ""

$ultimoHash = ""

while ($true) {
    try {
        # Obtener hash del último commit
        $hashActual = git rev-parse HEAD 2>$null
        
        # Verificar si hay cambios
        $cambios = git status --porcelain 2>$null
        
        if ($cambios) {
            Write-Host "[$(Get-Date -Format 'HH:mm:ss')] 📝 Cambios detectados, sincronizando..." -ForegroundColor Yellow
            
            # Agregar todos los cambios
            git add . 2>$null
            
            # Hacer commit
            $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
            git commit -m "Auto-sync: $timestamp" 2>$null
            
            # Push
            git push 2>$null
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "[$(Get-Date -Format 'HH:mm:ss')] ✅ Cambios sincronizados" -ForegroundColor Green
            } else {
                Write-Host "[$(Get-Date -Format 'HH:mm:ss')] ❌ Error al sincronizar" -ForegroundColor Red
            }
        } else {
            Write-Host "[$(Get-Date -Format 'HH:mm:ss')] 💤 Sin cambios" -ForegroundColor Gray
        }
        
    } catch {
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] ⚠️ Error: $_" -ForegroundColor Red
    }
    
    # Esperar intervalo
    Start-Sleep -Seconds $intervalo
}
