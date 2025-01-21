Clear-Host

Write-Host "Activating Python virtual environment" -ForegroundColor Green

.venv\Scripts\Activate.ps1

Write-Host "Running the application" -ForegroundColor Green

python geral.py

python empresas.py