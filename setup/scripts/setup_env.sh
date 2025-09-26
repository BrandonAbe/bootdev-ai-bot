#!/usr/bin/env bash
set -e

VENV=".venv"
ENV_FILE=".env"

# Prefer uv if available
if command -v uv &>/dev/null; then
    echo "Using uv to create environment..."
    uv venv $VENV
    source $VENV/bin/activate
    uv pip install -r pyproject.toml
else
    echo "uv not found, falling back to pip..."
    python3 -m venv $VENV
    source $VENV/bin/activate
    pip install --upgrade pip
    pip install -r requirements-dev.txt
fi

# Create .env if missing
if [ ! -f "$ENV_FILE" ]; then
    echo 'Creating .env file...'
    cat > "$ENV_FILE" <<EOL
# Local environment variables
GEMINI_API_KEY="YOUR_KEY_HERE"
EOL
else
    echo ".env file already exists, skipping creation."
fi

echo "Environment setup complete. To activate, run:"
echo "source $VENV/bin/activate"
