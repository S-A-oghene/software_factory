from __future__ import annotations
import hashlib, json, os, shutil, subprocess, zipfile
from pathlib import Path
from .paths import safe_path, should_skip
from .redact import redact
from .state import record_event

TEXT_EXTS={'.py','.js','.ts','.tsx','.jsx','.json','.toml','.yaml','.yml','.md','.txt','.html','.css','.sql','.sh','.rs','.go','.java','.kt','.swift','.xml','.csv','.env.example','.mjs','.c','.cpp','.h'}


def inventory(root: Path):
    files=[]; languages={}; total=0
    for p in sorted(root.rglob('*')):
        if not p.is_file() or should_skip(p.relative_to(root)): continue
        rel=p.relative_to(root).as_posix(); size=p.stat().st_size; total += size
        ext=p.suffix.lower(); languages[ext]=languages.get(ext,0)+1
        files.append({'path':rel,'size':size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    return {'root':str(root),'file_count':len(files),'total_bytes':total,'extensions':languages,'files':files[:5000]}


def git(root,*args):
    p=subprocess.run(['git',*args],cwd=root,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
    return {'returncode':p.returncode,'output':redact(p.stdout)}


def init_repo(root):
    root.mkdir(parents=True,exist_ok=True); r=git(root,'init'); record_event(root,'repo_init',r); return r


def clone(url: str, root: Path):
    root.parent.mkdir(parents=True,exist_ok=True)
    p=subprocess.run(['git','clone',url,str(root)],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=600)
    result={'returncode':p.returncode,'output':redact(p.stdout)}
    if p.returncode==0: record_event(root,'repo_clone',{'url':url})
    return result


def create_workspace(root: Path, name='workspace'):
    root.mkdir(parents=True,exist_ok=True); init_repo(root)
    (root/'.factory').mkdir(exist_ok=True)
    (root/'.factory'/'workspace.json').write_text(json.dumps({'name':name,'type':'software-factory-workspace','version':'0.1.0'},indent=2),encoding='utf-8')
    return root


def export_zip(root: Path, out: Path):
    out.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
        for p in root.rglob('*'):
            if p.is_file() and not should_skip(p.relative_to(root)):
                z.write(p,p.relative_to(root).as_posix())
    record_event(root,'workspace_export',{'path':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest()})
    return out
