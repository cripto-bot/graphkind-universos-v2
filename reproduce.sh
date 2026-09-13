#!/usr/bin/env bash
# Reproducción completa del paper (v2). Uso: bash reproduce.sh [--rapido]
set -e
cd "$(dirname "$0")"
PY=${PY:-python3}
if [ -x /home/juri/graphlang-natural/.venv/bin/python ]; then
  PY=/home/juri/graphlang-natural/.venv/bin/python
fi
echo "== VERIFICACIONES DEL PAPER (v1: universos) =="
$PY codigo/verificaciones.py "$@"
echo "== VERIFICACIONES v2 (arco de universos) =="
$PY codigo/verificaciones_v2.py
