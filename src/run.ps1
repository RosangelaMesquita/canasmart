# run.ps1
Set-Location $PSScriptRoot
if (!(Test-Path ".\.venv\Scripts\python.exe")) {
  Write-Host "[INFO] Criando venv..."
  py -3 -m venv .venv
}
. .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
