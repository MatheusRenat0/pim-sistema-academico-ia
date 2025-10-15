Write-Host "=== Atualizando repositório local com o remoto ===" -ForegroundColor Cyan

git fetch origin
git checkout main
git pull origin main --rebase

Write-Host "Repositorio sincronizado" -ForegroundColor Green
