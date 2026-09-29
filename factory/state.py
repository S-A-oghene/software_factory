from __future__ import annotations
import json, hashlib, time
from pathlib import Path


def now():
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())


def load_state(root: Path) -> dict:
    p=root/'.factory'/'state.json'; p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        state={'version':'0.1.0','created_at':now(),'updated_at':now(),'events':[],'checkpoints':[]}
        p.write_text(json.dumps(state,indent=2), encoding='utf-8'); return state
    return json.loads(p.read_text(encoding='utf-8'))


def record_event(root: Path, event_type: str, payload: dict):
    state=load_state(root)
    state['updated_at']=now()
    event={'id':hashlib.sha256((event_type+now()+json.dumps(payload,sort_keys=True)).encode()).hexdigest()[:20], 'time':now(), 'type':event_type, 'payload':payload}
    state.setdefault('events',[]).append(event)
    (root/'.factory'/'state.json').write_text(json.dumps(state,indent=2,ensure_ascii=False),encoding='utf-8')
    return event


def checkpoint(root: Path, label: str, metadata=None):
    state=load_state(root); cp={'label':label,'time':now(),'metadata':metadata or {}}
    state.setdefault('checkpoints',[]).append(cp); state['updated_at']=now()
    (root/'.factory'/'state.json').write_text(json.dumps(state,indent=2,ensure_ascii=False),encoding='utf-8')
    return cp
