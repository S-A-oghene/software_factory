#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
out="$(dirname "$ROOT")/software-factory-zero-budget-v0.1.0-corrected.zip"
rm -f "$out"
cd "$ROOT"
zip -qr "$out" . -x '*/__pycache__/*' '*/.git/*'
echo "$out"
