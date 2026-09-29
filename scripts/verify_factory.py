#!/usr/bin/env python3
from pathlib import Path
import subprocess, sys
root=Path(__file__).resolve().parents[1]
commands=[ [sys.executable,'-m','compileall','-q','factory','tests','scripts'], [sys.executable,'-m','unittest','discover','-s','tests'], [sys.executable,'-m','factory','self-test'] ]
for cmd in commands:
    print('RUN',' '.join(cmd))
    p=subprocess.run(cmd,cwd=root)
    if p.returncode: raise SystemExit(p.returncode)
print('VERIFY_FACTORY_PASS')

assert (root / '.github/workflows/ci.yml').exists()
assert (root / '.github/workflows/security.yml').exists()
assert (root / '.github/workflows/release-evidence.yml').exists()
