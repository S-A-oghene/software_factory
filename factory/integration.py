from __future__ import annotations
import hashlib, json, shutil, tempfile, zipfile
from pathlib import Path
from .ingest import validate_member
from .paths import should_skip
from .state import record_event

def integrate_zip(zip_path: Path, workspace: Path, apply_non_conflicting=True):
    incoming_root=workspace/'.factory'/'incoming'
    incoming_root.mkdir(parents=True,exist_ok=True)
    token=hashlib.sha256(zip_path.read_bytes()).hexdigest()[:16]
    stage=incoming_root/token; stage.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(zip_path) as z:
        infos=z.infolist(); bad=[]; total=0
        for info in infos:
            total += max(0, info.file_size)
            mode=(info.external_attr >> 16) & 0o170000
            if mode==0o120000 or not validate_member(info.filename): bad.append(info.filename)
        if total>250_000_000: raise ValueError('ZIP uncompressed size exceeds integration limit')
        if bad: raise ValueError('Unsafe ZIP member(s): '+', '.join(bad[:10]))
        z.extractall(stage)
    conflicts=[]; added=[]; updated=[]; unchanged=[]
    for p in sorted(stage.rglob('*')):
        if not p.is_file() or should_skip(p.relative_to(stage)): continue
        rel=p.relative_to(stage).as_posix(); dest=workspace/rel
        if not dest.exists():
            if apply_non_conflicting:
                dest.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(p,dest)
            added.append(rel)
        else:
            if hashlib.sha256(p.read_bytes()).hexdigest()==hashlib.sha256(dest.read_bytes()).hexdigest():
                unchanged.append(rel)
            else:
                conflicts.append(rel)
                cpath=workspace/'.factory'/'conflicts'/token/rel
                cpath.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(p,cpath)
    plan={'source_zip':str(zip_path),'source_sha256':hashlib.sha256(zip_path.read_bytes()).hexdigest(),'applied_non_conflicting':apply_non_conflicting,'added':added,'updated':updated,'unchanged':unchanged,'conflicts':conflicts}
    (workspace/'.factory'/'integration-plan.json').write_text(json.dumps(plan,indent=2,ensure_ascii=False),encoding='utf-8')
    record_event(workspace,'zip_integration',plan)
    return plan
