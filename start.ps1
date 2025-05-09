Write-Host "`n--- Ativando ambiente virtual..."
if (-Not (Test-Path ".\.venv\Scripts\Activate.ps1")) {
    Write-Host "`n--- Ambiente virtual não encontrado. Criando..."
    python -m venv .venv
}

. .\.venv\Scripts\Activate.ps1

Write-Host "`n--- Instalando dependencias..."
pip install --no-cache-dir -r requirements.txt

Write-Host "`n--- Subindo containers com build..."
docker-compose up -d --build

Start-Sleep -Seconds 5

Write-Host "`n--- Iniciando aplicacao Python..."
python .\main.py