from __future__ import annotations
import hashlib, json, re, tomllib
from pathlib import Path


def load_spec(path):
    p=Path(path); raw=p.read_bytes(); data=tomllib.loads(raw.decode('utf-8')); validate_spec(data)
    data['_meta']={'path':str(p),'sha256':hashlib.sha256(raw).hexdigest()}; return data


def validate_spec(spec):
    target=spec.get('target') or {}
    for key in ('name','version','profile'):
        if not target.get(key): raise ValueError(f'target.{key} is required')
    entities=[x.get('name','') for x in spec.get('entities',[])]
    if len(entities)!=len(set(entities)): raise ValueError('Duplicate entity names')
    for name in entities:
        if not re.fullmatch(r'[a-z][a-z0-9_]*',name): raise ValueError(f'Unsafe entity name: {name}')
    rids=[str(x.get('id','')) for x in spec.get('requirements',[])]
    if len(rids)!=len(set(rids)): raise ValueError('Duplicate requirement IDs')
    if any(not x.get('id') or not x.get('statement') for x in spec.get('requirements',[])):
        raise ValueError('Every requirement needs id and statement')
    for wf in spec.get('workflows',[]):
        stages=wf.get('stages',[])
        if len(stages)<2 or len(stages)!=len(set(stages)): raise ValueError(f'Invalid workflow stages: {wf.get("name")}')


def spec_hash(spec):
    clean={k:v for k,v in spec.items() if k!='_meta'}
    return hashlib.sha256(json.dumps(clean,sort_keys=True,separators=(',',':')).encode()).hexdigest()
