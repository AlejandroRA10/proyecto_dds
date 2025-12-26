<#
Script seguro para respaldar y eliminar archivos/carpetas legacy duplicadas.
NO toca la carpeta tp_importacion_xml.

Uso: abrir PowerShell en la raíz del repo y ejecutar:
  .\scripts\cleanup-legacy.ps1

El script hará:
- crear backups/servidor-docker-backup.zip
- renombrar (archivar) la carpeta servidor-docker a servidor-docker-archivado
- eliminar el docker-compose.traefik.yml del root si existe
#>

Param()

$root = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent | Split-Path -Parent
Write-Host "Repositorio raíz: $root"

$legacy = Join-Path $root 'servidor-docker'
$backupDir = Join-Path $root 'backups'
If (-not (Test-Path $backupDir)) { New-Item -ItemType Directory -Path $backupDir | Out-Null }

If (Test-Path $legacy) {
    $zipPath = Join-Path $backupDir 'servidor-docker-backup.zip'
    Write-Host "Creando backup de $legacy -> $zipPath"
    Compress-Archive -Path (Join-Path $legacy '*') -DestinationPath $zipPath -Force

    # Renombrar la carpeta (más seguro que eliminar)
    $archived = Join-Path $root 'servidor-docker-archivado'
    if (Test-Path $archived) {
        Write-Host "Existe servidor-docker-archivado; agregando timestamp"
        $ts = Get-Date -Format "yyyyMMddHHmmss"
        $archived = "$archived-$ts"
    }
    Write-Host "Renombrando $legacy -> $archived"
    Rename-Item -LiteralPath $legacy -NewName (Split-Path $archived -Leaf)
} else {
    Write-Host "No existe la carpeta servidor-docker; nada que archivar."
}

# Eliminar docker-compose.traefik.yml en la raíz si existe (ya movido a servidor_docker)
$rootCompose = Join-Path $root 'docker-compose.traefik.yml'
If (Test-Path $rootCompose) {
    Write-Host "Eliminando $rootCompose"
    Remove-Item -LiteralPath $rootCompose -Force
} else {
    Write-Host "No existe docker-compose.traefik.yml en la raíz."
}

Write-Host "Limpieza completa. Verifique backups/ y servidor-docker-archivado/."
