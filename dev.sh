#!/bin/zsh
set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

# Derruba instância anterior na porta 8080
lsof -ti:8080 | xargs kill -9 2>/dev/null; sleep 1 && export PYTHONPATH=$(pwd) && source .venv/bin/activate
sleep 1
uvicorn app.main:app --host 0.0.0.0 --port 8080
