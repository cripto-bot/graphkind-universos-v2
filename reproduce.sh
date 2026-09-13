#!/usr/bin/env bash
# Reproducción completa del paper. Uso: bash reproduce.sh [--rapido]
set -e
cd "$(dirname "$0")"
PY=${PY:-python3}
if [ -x /home/juri/graphlang-natural/.venv/bin/python ]; then
  PY=/home/juri/graphlang-natural/.venv/bin/python
fi
echo "== VERIFICACIONES DEL PAPER =="
$PY codigo/verificaciones.py "$@"
