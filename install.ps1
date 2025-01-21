Clear-Host

Write-Host "Creating Python virtual environment" -ForegroundColor Green

python -m venv .venv

Write-Host "Activating Python virtual environment" -ForegroundColor Green

.venv\Scripts\Activate.ps1

Write-Host "Installing project dependencies" -ForegroundColor Green

python -m pip install -r requirements.txt
