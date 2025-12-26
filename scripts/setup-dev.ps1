param(
    [string]$RequirementsPath = "servidor_docker/requirements.txt",
    [string]$VenvPath = ".venv"
)

Write-Host "Creando virtualenv en: $VenvPath"
python -m venv $VenvPath

$pip = Join-Path $VenvPath 'Scripts\\pip.exe'
if (-Not (Test-Path $pip)) {
    Write-Error "pip no encontrado en la venv. Asegúrate de tener Python instalado y accesible como 'python'."
    exit 1
}

Write-Host "Actualizando pip..."
& $pip install --upgrade pip

$req = Join-Path (Get-Location) $RequirementsPath
if (-Not (Test-Path $req)) {
    Write-Error "Archivo de requirements no encontrado: $req"
    exit 1
}

Write-Host "Instalando dependencias desde: $req"
& $pip install -r $req

Write-Host "Listo. Activa la venv con: .\\.venv\\Scripts\\Activate.ps1"
