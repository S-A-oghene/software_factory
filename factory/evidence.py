from __future__ import annotations
import json, hashlib
from pathlib import Path
from .state import now


def requirement_evidence(spec, root: Path):
    texts = []
    for p in root.rglob('*'):
        if p.is_file() and '.git' not in p.parts and '.factory' not in p.parts:
            try:
                texts.append((p.relative_to(root).as_posix(), p.read_text(encoding='utf-8', errors='ignore')))
            except Exception:
                pass
    items = []
    for r in spec.get('requirements',[]):
        rid = str(r['id'])
        hits = [path for path,text in texts if rid in text]
        items.append({'id':rid,'critical':bool(r.get('critical')),'evidence_files':sorted(set(hits))[:20], 'status':'EVIDENCED' if hits else 'UNPROVEN'})
    return items


def write_evidence(spec, root: Path, extra=None):
    out = root/'.factory'; out.mkdir(exist_ok=True)
    payload = {'generated_at':now(),'target':spec.get('target',{}),'requirements':requirement_evidence(spec,root),'extra':extra or {}}
    payload['critical_unproven']=[x['id'] for x in payload['requirements'] if x['critical'] and x['status']!='EVIDENCED']
    payload['sha256']=hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()
    (out/'evidence.json').write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding='utf-8')
    md=['# Evidence Report','',f"Generated: {payload['generated_at']}",'', '## Requirements']
    for x in payload['requirements']:
        md.append(f"- {x['id']}: {x['status']} — {', '.join(x['evidence_files'][:5]) or 'no file evidence'}")
    md += ['', '## Critical unproven']
    md += [f'- {x}' for x in payload['critical_unproven']] if payload['critical_unproven'] else ['- none']
    (out/'evidence.md').write_text('\n'.join(md)+'\n', encoding='utf-8')
    return payload
