from __future__ import annotations
import json, hashlib, time, zipfile
from pathlib import Path
from .repository import inventory
from .redact import redact
from .state import record_event

DEFAULT_PROVIDERS=[
 {'id':'chatgpt-web','label':'ChatGPT Web','url':'https://chatgpt.com/','mode':'human_browser_co_work'},
 {'id':'custom','label':'Custom Frontier Web LLM','url':'','mode':'human_browser_co_work'},
]


def build_prompt(workspace: Path, task: str, context_paths=None):
    inv=inventory(workspace)
    context_paths=context_paths or []
    snippets=[]
    for rel in context_paths:
        p=workspace/rel
        if p.is_file():
            snippets.append(f'===== {rel} =====\n{redact(p.read_text(encoding="utf-8",errors="replace")[:30000])}')
    return f"""You are participating as a frontier engineering collaborator with Software_Factory v0.1.0.

Objective:
{task}

Factory constraints:
- Return a complete system-level engineering result, not a superficial code sketch.
- State architecture, assumptions, interfaces, data flows, failure modes, security boundaries, deployment model and validation strategy.
- Prefer replaceable/provider-neutral capabilities.
- Distinguish established engineering from open research.
- Produce files/artifacts in a way that can be exported as a ZIP and re-imported.
- Do not claim state-of-the-art without measurable evidence.

Repository inventory:
{json.dumps(inv,indent=2)[:30000]}

Selected context:
{chr(10).join(snippets)}
"""


def create_session(workspace: Path, task: str, context_paths=None):
    sid=hashlib.sha256((task+str(time.time())).encode()).hexdigest()[:16]
    session=workspace/'.factory'/'frontier_sessions'/sid; session.mkdir(parents=True,exist_ok=True)
    prompt=build_prompt(workspace,task,context_paths)
    (session/'PROMPT.md').write_text(prompt,encoding='utf-8')
    manifest={'session_id':sid,'created_at':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'task':task,'providers':DEFAULT_PROVIDERS,'context_paths':context_paths or [],'mode':'human_browser_co_work'}
    (session/'SESSION.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    (session/'OPEN_WEB_SESSION.md').write_text("""# Open the Frontier Web Session

1. Open your chosen provider URL in a normal browser tab.
2. Copy `PROMPT.md` into the provider's normal chat UI.
3. Upload the requested workspace/context ZIP if the provider supports file upload.
4. Work normally in the provider web application.
5. Download the resulting ZIP/artifacts.
6. Upload/import them back into Software_Factory.

This workflow deliberately avoids scraping or automating a third-party consumer web GUI.
""",encoding='utf-8')
    record_event(workspace,'frontier_session_created',manifest)
    return session


def export_context_zip(workspace: Path, session: Path, paths=None):
    out=session/'CONTEXT.zip'; paths=paths or []
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
        if paths:
            for rel in paths:
                p=workspace/rel
                if p.is_file(): z.write(p,rel)
        else:
            for p in workspace.rglob('*'):
                if p.is_file() and '.git' not in p.parts and '.factory' not in p.parts:
                    z.write(p,p.relative_to(workspace).as_posix())
    return out
