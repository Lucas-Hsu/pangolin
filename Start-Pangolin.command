#!/bin/bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"

if command -v uv >/dev/null 2>&1; then
  exec uv run --no-build-package PyQt6 --no-build-package PyQt6-Qt6 --no-build-package PyQt6-sip --no-build-package cryptography pangolin
fi

if [ ! -x .venv/bin/python ]; then
  python_cmd=""
  for candidate in python3.12 python3.13 python3.14 python3.15 python3.11 python3.10 python3; do
    if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -c 'import sys; sys.exit(sys.version_info < (3, 10))' 2>/dev/null; then
      python_cmd="$candidate"
      break
    fi
  done
  if [ -z "$python_cmd" ]; then
    echo "Install Python 3.10 or newer from https://www.python.org/downloads/macos/"
    echo "Then open this launcher again. Python 3.12 is recommended."
    exit 1
  fi
  "$python_cmd" -m venv .venv
fi

if ! .venv/bin/python -c 'import sys; sys.exit(sys.version_info < (3, 10))'; then
  echo "The existing .venv uses an older Python. Rename it and launch again."
  exit 1
fi

# Local dependencies allow subsequent launches to work without a download.
if ! .venv/bin/python -c 'import pangolin, PyQt6.QtWidgets, cryptography.fernet' >/dev/null 2>&1; then
  if ! .venv/bin/python -m pip --version >/dev/null 2>&1; then
    .venv/bin/python -m ensurepip --upgrade
  fi
  .venv/bin/python -m pip install --only-binary=PyQt6,PyQt6-Qt6,PyQt6-sip,cryptography -e .
fi
exec .venv/bin/python main.py
