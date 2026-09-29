from __future__ import annotations
import json
from pathlib import Path
from .repository import inventory


def write_workspace_report(root: Path, extra=None):
    report={'inventory':inventory(root),'extra':extra or {}}
    out=root/'.factory'; out.mkdir(exist_ok=True)
    (out/'workspace-report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    return report
