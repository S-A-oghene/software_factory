#!/usr/bin/env bash
set -euo pipefail
WORKSPACE="${1:-workspaces/demo-import}"
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8787}"
PIDFILE=".software-factory-gui.pid"
LOGFILE=".software-factory-gui.log"
mkdir -p "$(dirname "$WORKSPACE")"
if [[ -f "$PIDFILE" ]]; then
  PID="$(cat "$PIDFILE" || true)"
  if [[ -n "$PID" ]] && kill -0 "$PID" 2>/dev/null; then
    echo "Software_Factory GUI already running (PID $PID)."
    exit 0
  fi
  rm -f "$PIDFILE"
fi
nohup python3 -m factory web --workspace "$WORKSPACE" --host "$HOST" --port "$PORT" > "$LOGFILE" 2>&1 &
echo $! > "$PIDFILE"
echo "Software_Factory GUI starting on http://$HOST:$PORT/"
