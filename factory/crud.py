from __future__ import annotations
import shutil
from pathlib import Path
from .paths import safe_path
from .policy import validate_delete
from .state import record_event


def list_tree(root):
    rows=[]
    for p in sorted(root.rglob('*')):
        rel=p.relative_to(root).as_posix()
        if rel == '.git' or rel.startswith('.git/') or rel == '.factory' or rel.startswith('.factory/'):
            continue
        rows.append({'path':rel,'kind':'dir' if p.is_dir() else 'file','size':p.stat().st_size if p.is_file() else None})
    return rows


def create(root, rel, content=''):
    p=safe_path(root,rel); p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists(): raise FileExistsError(rel)
    p.write_text(content,encoding='utf-8'); record_event(root,'create_file',{'path':rel}); return p


def read(root, rel):
    p=safe_path(root,rel)
    if not p.is_file(): raise FileNotFoundError(rel)
    return p.read_text(encoding='utf-8',errors='replace')


def update(root, rel, content):
    p=safe_path(root,rel)
    if not p.is_file(): raise FileNotFoundError(rel)
    p.write_text(content,encoding='utf-8'); record_event(root,'update_file',{'path':rel}); return p


def delete(root, rel, allow_protected=False):
    validate_delete(rel,allow_protected)
    p=safe_path(root,rel)
    if not p.exists(): raise FileNotFoundError(rel)
    if p.is_dir(): shutil.rmtree(p)
    else: p.unlink()
    record_event(root,'delete_path',{'path':rel}); return True


def copy(root, src, dst):
    s=safe_path(root,src); d=safe_path(root,dst); d.parent.mkdir(parents=True,exist_ok=True)
    if s.is_dir(): shutil.copytree(s,d)
    else: shutil.copy2(s,d)
    record_event(root,'copy_path',{'src':src,'dst':dst}); return d


def move(root, src, dst):
    s=safe_path(root,src); d=safe_path(root,dst); d.parent.mkdir(parents=True,exist_ok=True)
    shutil.move(str(s),str(d)); record_event(root,'move_path',{'src':src,'dst':dst}); return d
