from __future__ import annotations
import re, subprocess
from pathlib import Path
from .paths import safe_path, should_skip
from .policy import validate_patch_size
from .redact import redact

class ToolError(RuntimeError):
    pass


def inspect_repository(root):
    out=[]
    for p in sorted(root.rglob('*')):
        if p.is_file() and not should_skip(p.relative_to(root)):
            out.append(p.relative_to(root).as_posix())
            if len(out)>=1000: break
    return {'files':out,'count':len(out)}


def read_files(root, paths, max_total=160000, max_each=40000):
    chunks=[]; total=0
    for rel in paths:
        p=safe_path(root,rel)
        if not p.is_file(): raise ToolError(f'Not a file: {rel}')
        data=p.read_text(encoding='utf-8',errors='replace')[:max_each]
        if total+len(data)>max_total: break
        total += len(data)
        chunks.append(f'===== {rel} =====\n{redact(data)}')
    return '\n\n'.join(chunks)


def search_repository(root, query, max_results=120):
    if not query: raise ToolError('Query required')
    rx=re.compile(re.escape(query),re.I); out=[]
    for p in root.rglob('*'):
        if not p.is_file() or should_skip(p.relative_to(root)): continue
        try: lines=p.read_text(encoding='utf-8',errors='ignore').splitlines()
        except Exception: continue
        for i,line in enumerate(lines,1):
            if rx.search(line):
                out.append(f'{p.relative_to(root).as_posix()}:{i}:{redact(line[:500])}')
                if len(out)>=max_results: return '\n'.join(out)
    return '\n'.join(out) if out else 'NO_MATCHES'


def apply_patch(root, patch):
    validate_patch_size(patch)
    p=subprocess.run(['git','apply','--check','-'],input=patch,text=True,cwd=root,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=60)
    if p.returncode: raise ToolError(redact(p.stdout))
    p=subprocess.run(['git','apply','--whitespace=nowarn','-'],input=patch,text=True,cwd=root,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=60)
    if p.returncode: raise ToolError(redact(p.stdout))
    return 'PATCH_APPLIED'


def git_diff(root):
    p=subprocess.run(['git','diff','--no-ext-diff'],cwd=root,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=60)
    if p.returncode: raise ToolError(redact(p.stdout))
    return redact(p.stdout)


def run_validation(root, command):
    if not command: raise ToolError('Validation command required')
    if any(x in command for x in [';','&&','||','|','>','<','$(']):
        raise ToolError('Compound shell commands not permitted')
    args=command.split()
    p=subprocess.run(args,cwd=root,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=300)
    return {'command':args,'returncode':p.returncode,'passed':p.returncode==0,'output':redact(p.stdout[-50000:])}
