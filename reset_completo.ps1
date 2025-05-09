# Ativa o ambiente virtual
Write-Host "`n--- Ativando ambiente virtual..."
if (-Not (Test-Path ".\.venv\Scripts\Activate.ps1")) {
    Write-Host "`n--- Ambiente virtual não encontrado. Criando..."
    python -m venv .venv
}

. .\.venv\Scripts\Activate.ps1

# Para e remove containers, volumes e rede
Write-Host "`n--- Parando e removendo containers, volumes e rede..."
docker-compose down -v

# Remove redes Docker órfãs (opcional)
Write-Host "`n--- Limpando redes Docker orfas..."
docker network prune -f

# Reinstala dependências Python
Write-Host "`n--- Reinstalando dependencias do Python..."
pip install --no-cache-dir -r requirements.txt

# Sobe os containers com build
Write-Host "`n--- Subindo containers com build..."
docker-compose up -d --build

# Aguarda alguns segundos para Kafka inicializar
Start-Sleep -Seconds 5

# Define variável de ambiente USE_ONVIF
$env:USE_ONVIF = "false"

# Executa a aplicação Python
Write-Host "`n--- Iniciando aplicacao Python..."
python .\main.py
