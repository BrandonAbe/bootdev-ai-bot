$VENV = ".venv"
$ENV_FILE = ".env"

if (Get-Command uv -ErrorAction SilentlyContinue) {
    Write-Host "Using uv to create environment..."
    uv venv $VENV
    .\$VENV\Scripts\Activate.ps1
    uv pip install -r pyproject.toml
}
else {
    Write-Host "uv not found, falling back to pip..."
    python -m venv $VENV
    .\$VENV\Scripts\Activate.ps1
    pip install --upgrade pip
    pip install -r requirements-dev.txt
}

# Create .env if missing
if (!(Test-Path $ENV_FILE)) {
    Write-Host "Creating .env file..."
    @'
# Local environment variables
GEMINI_API_KEY="YOUR_KEY_HERE"
'@ | Out-File -Encoding UTF8 $ENV_FILE
}
else {
    Write-Host ".env file already exists, skipping creation."
}

Write-Host "Environment setup complete. To activate later, run:"
Write-Host ".\$VENV\Scripts\Activate.ps1"
