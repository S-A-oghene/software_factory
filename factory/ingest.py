from __future__ import annotations
import hashlib, json, os, shutil, zipfile
from pathlib import Path
from .repository import inventory
from .discovery import discover_engineering_model
from .state import record_event


def validate_member(name: str):
    p=Path(name)
    return not p.is_absolute() and '..' not in p.parts and not name.startswith('~')


def import_zip(zip_path: Path, workspace: Path, max_members=20000, max_uncompressed_bytes=250_000_000):
    workspace.parent.mkdir(parents=True,exist_ok=True)
    if workspace.exists() and any(workspace.iterdir()):
        raise FileExistsError(f'Workspace is not empty: {workspace}')
    workspace.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(zip_path) as z:
        infos=z.infolist()
        if len(infos)>max_members: raise ValueError(f'ZIP contains too many members: {len(infos)}')
        bad=[]; total=0
        for info in infos:
            total += max(0, info.file_size)
            mode=(info.external_attr >> 16) & 0o170000
            if mode==0o120000 or not validate_member(info.filename): bad.append(info.filename)
        if total>max_uncompressed_bytes: raise ValueError(f'ZIP uncompressed size exceeds limit: {total}')
        if bad: raise ValueError('Unsafe ZIP member(s): '+', '.join(bad[:10]))
        z.extractall(workspace)
    (workspace/'.factory').mkdir(exist_ok=True)
    original_hash=hashlib.sha256(zip_path.read_bytes()).hexdigest()
    inv=inventory(workspace)
    engineering_model=discover_engineering_model(workspace)
    (workspace/'.factory'/'engineering-model.json').write_text(json.dumps(engineering_model,indent=2,ensure_ascii=False),encoding='utf-8')
    manifest={'source_zip':str(zip_path),'source_sha256':original_hash,'inventory':inv,'engineering_model':engineering_model}
    (workspace/'.factory'/'import-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    record_event(workspace,'zip_import',{'source_sha256':original_hash,'file_count':inv['file_count']})
    return manifest
