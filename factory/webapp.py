from __future__ import annotations

import json
import mimetypes
import os
import shutil
import subprocess
import tempfile
import urllib.parse
from email.parser import BytesParser
from email.policy import default
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .architecture import write_architecture
from .benchmark import benchmark
from .crud import copy as crud_copy, create, delete, list_tree, move as crud_move, read, update
from .discovery import discover_engineering_model
from .frontier import create_session, export_context_zip
from .ingest import import_zip
from .integration import integrate_zip
from .planner import capability_graph, compile_tasks, requirement_graph
from .redact import redact
from .render import render_scaffold
from .repository import clone, create_workspace, export_zip, git, inventory
from .report import write_workspace_report
from .spec import load_spec
from .state import checkpoint, load_state


APP_VERSION = "0.1.0"
MAX_UPLOAD_BYTES = 50 * 1024 * 1024

HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Software_Factory v0.1.0 — GUI</title>
<style>
:root{--bg:#f6f7fb;--card:#fff;--ink:#18202a;--muted:#667085;--line:#d9dee7;--good:#0a7a45;--warn:#9a6700;--bad:#b42318;--accent:#335cff}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
header{background:var(--card);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:10}
.wrap{max-width:1280px;margin:0 auto;padding:16px 20px}.top{display:flex;gap:14px;align-items:center;justify-content:space-between}.brand{font-size:22px;font-weight:750}.sub{color:var(--muted)}
nav{display:flex;gap:8px;overflow:auto;padding-top:12px}nav a{color:var(--ink);text-decoration:none;padding:8px 10px;border-radius:8px;white-space:nowrap}nav a:hover{background:#eef1f7}
main{max-width:1280px;margin:0 auto;padding:22px 20px 60px}.hero{display:grid;grid-template-columns:1.5fr .9fr;gap:16px}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}.grid3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px;box-shadow:0 1px 2px rgba(16,24,40,.03);margin-bottom:16px}.card h2,.card h3{margin:0 0 8px}.card p{margin:7px 0;color:var(--muted)}
.step{display:flex;gap:12px;align-items:flex-start}.num{width:30px;height:30px;border:1px solid var(--line);border-radius:50%;display:grid;place-items:center;font-weight:700;flex:0 0 auto}.step strong{display:block}.status{display:inline-flex;padding:4px 8px;border-radius:999px;font-size:12px;font-weight:700}.status.good{background:#e8f7ef;color:var(--good)}.status.bad{background:#feeceb;color:var(--bad)}.status.info{background:#edf2ff;color:#2446c8}.status.warn{background:#fff5db;color:var(--warn)}
label{display:block;font-weight:650;margin:10px 0 5px}input,select,textarea{width:100%;border:1px solid #cbd2dc;border-radius:9px;padding:9px 10px;font:inherit;background:#fff}textarea{min-height:120px;resize:vertical}button{border:0;border-radius:9px;padding:9px 12px;background:var(--accent);color:white;font-weight:700;cursor:pointer;margin:4px 5px 4px 0}button.secondary{background:#eef1f6;color:#243041}button.danger{background:#b42318}button:disabled{opacity:.55;cursor:not-allowed}
pre{background:#101828;color:#e8eef7;padding:13px;border-radius:10px;overflow:auto;max-height:420px;white-space:pre-wrap}.muted{color:var(--muted)}.row{display:flex;gap:8px;align-items:center;flex-wrap:wrap}.hidden{display:none!important}.pill{padding:3px 8px;border:1px solid var(--line);border-radius:999px}.tree{display:grid;grid-template-columns:minmax(0,1fr) auto auto;gap:6px 8px;align-items:center}.tree button{margin:0}.small{font-size:12px}.banner{padding:11px 13px;border-radius:10px;border:1px solid var(--line);background:#fafbfc}.banner.good{border-color:#b7e2c8;background:#f2fbf6}.banner.warn{border-color:#f0d48b;background:#fffaf0}.banner.bad{border-color:#f3b8b2;background:#fff6f5}
.kpi{padding:14px;border:1px solid var(--line);border-radius:10px}.kpi .v{font-size:26px;font-weight:800}.kpi .l{font-size:12px;color:var(--muted)}
@media(max-width:900px){.hero,.grid,.grid3{grid-template-columns:1fr}}
</style>
</head>
<body>
<header><div class="wrap">
<div class="top"><div><div class="brand">Software_Factory v0.1.0</div><div class="sub">GUI-first autonomous engineering factory</div></div><span id="health" class="status info">Checking…</span></div>
<nav>
<a href="#start">Start</a><a href="#workspace">Workspace</a><a href="#design">Design</a><a href="#build">Build</a><a href="#files">Files</a><a href="#verify">Verify</a><a href="#frontier">Frontier LLM</a><a href="#export">Export</a><a href="#help">Help</a>
</nav></div></header>
<main>
<section id="start" class="hero">
<div class="card"><h1>One continuous browser workflow</h1><p>Use this page for normal Software_Factory operation. You should not need to remember CLI commands for routine work.</p>
<div id="nextStep" class="banner info" style="margin-top:12px"><strong>Next step:</strong> Start in Workspace → use <em>Use included demo ZIP</em> for the fastest first test.</div><div class="banner good"><strong>Beginner rule:</strong> use the GUI for workspace, ZIP ingestion, architecture, scaffolding, files, verification, benchmarks, frontier sessions, and exports. The CLI is primarily for starting this web UI, bootstrap recovery, and diagnostics.</div>
<div style="margin-top:14px" class="step"><div class="num">1</div><div><strong>Choose or create a workspace</strong><div class="muted">Then everything below acts on that workspace.</div></div></div>
<div class="step"><div class="num">2</div><div><strong>Understand → Design → Build</strong><div class="muted">Validate a target, inspect the plan, generate architecture, then scaffold.</div></div></div>
<div class="step"><div class="num">3</div><div><strong>Verify → Benchmark → Export</strong><div class="muted">Use evidence gates before treating a generated result as successful.</div></div></div>
</div>
<div class="card"><h2>Current workspace</h2><div id="currentWorkspace" class="kpi"><div class="v">…</div><div class="l">Loading</div></div><div class="row" style="margin-top:10px"><button onclick="refreshAll()">Refresh everything</button><button class="secondary" onclick="runAction('factory-self-test')">Run factory self-test</button></div><pre id="startOut"></pre></div>
</section>

<section id="workspace" class="card"><h2>1. Workspace</h2><p>Create a clean workspace, switch between workspaces under the configured workspaces directory, import a shipped ZIP, or integrate an external ZIP into the current system.</p>
<div class="grid">
<div><h3>Create / switch</h3><label>Workspace name</label><input id="workspaceName" placeholder="demo-import"><div class="row"><button onclick="createWorkspace()">Create & switch</button><button class="secondary" onclick="refreshWorkspaceList()">Refresh list</button></div><label>Existing workspace</label><select id="workspaceList"></select><button onclick="switchWorkspace()">Switch</button><pre id="workspaceOut"></pre></div>
<div><h3>ZIP workflows</h3><button onclick="importIncludedDemo()">Use included demo ZIP</button><span class="muted small"> Fastest first test.</span><label>Shipped solution ZIP from your computer</label><input id="zipNew" type="file" accept=".zip"><label>New workspace name for this ZIP</label><input id="zipWorkspaceName" placeholder="imported-solution"><button onclick="importZipNew()">Import as new workspace</button><label style="margin-top:16px">External ZIP for integration</label><input id="zipIntegrate" type="file" accept=".zip"><div class="row"><button onclick="integrateZip()">Integrate non-conflicting files</button><button class="secondary" onclick="integrateZip(true)">Plan only</button></div><pre id="zipOut"></pre></div>
</div>
</section>

<section id="design" class="card"><h2>2. Understand & design</h2><p>Select a target profile. The buttons below run in sequence but can also be used independently.</p>
<div class="grid"><div><label>Target specification</label><select id="target"></select><div class="row"><button onclick="validateTarget()">1. Validate specification</button><button onclick="makePlan()">2. Show engineering plan</button><button onclick="makeArchitecture()">3. Generate architecture</button><button onclick="makeScaffold()">4. Generate scaffold</button></div></div><div><div class="kpi"><div id="targetName" class="v">…</div><div class="l">Selected target</div></div><p>For advanced testing, run the same sequence for MOW, NG, Distributed Platform, and AMPA-AI.</p></div></div><pre id="designOut"></pre></section>

<section id="build" class="card"><h2>3. Build & evolve</h2><p>The GUI can make normal repository changes and maintain a visible audit trail. Use the Files area for direct CRUD and the Integration controls above for ZIP changes.</p>
<div class="grid"><div><h3>Repository</h3><label>Repository URL</label><input id="repoUrl" placeholder="https://github.com/org/repo.git"><label>Clone destination name</label><input id="cloneName" placeholder="cloned-repo"><div class="row"><button onclick="repoInit()">Initialize Git repo</button><button onclick="repoClone()">Clone into workspace directory</button><button class="secondary" onclick="gitStatus()">Git status</button><button class="secondary" onclick="gitDiff()">Git diff</button></div></div><div><h3>Checkpoint</h3><label>Checkpoint label</label><input id="checkpointLabel" placeholder="Before frontier integration"><button onclick="makeCheckpoint()">Create checkpoint</button><pre id="buildOut"></pre></div></div>
</section>

<section id="files" class="card"><h2>4. Files & repository CRUD</h2><p>Click a file in the tree to read it into the editor. Use Create, Update, Delete, Copy, and Move for ordinary file operations.</p>
<div class="grid"><div><div class="row"><button onclick="refreshTree()">Refresh tree</button><input id="treeFilter" placeholder="Filter path" oninput="renderTree()" style="max-width:280px"></div><div id="tree" class="tree"></div></div><div><label>Path</label><input id="filePath" placeholder="src/example.py"><label>Content</label><textarea id="fileContent" placeholder="Select a file or enter new content"></textarea><div class="row"><button onclick="fileAction('create')">Create</button><button onclick="fileAction('update')">Update</button><button class="secondary" onclick="fileAction('read')">Read</button><button class="danger" onclick="fileAction('delete')">Delete</button></div><label>Destination path (copy/move)</label><input id="fileDestination" placeholder="src/example-copy.py"><div class="row"><button class="secondary" onclick="fileAction('copy')">Copy</button><button class="secondary" onclick="fileAction('move')">Move</button></div><pre id="fileOut"></pre></div></div>
</section>

<section id="verify" class="card"><h2>5. Verify, benchmark & evidence</h2><p>Use these GUI buttons to run the deterministic factory checks and evaluate the current workspace against the selected target's frontier acceptance gates.</p>
<div class="grid3"><div class="kpi"><div class="v" id="fileCount">…</div><div class="l">Workspace files</div></div><div class="kpi"><div class="v" id="checkpointCount">…</div><div class="l">Checkpoints</div></div><div class="kpi"><div class="v" id="eventCount">…</div><div class="l">Recorded events</div></div></div>
<label style="margin-top:14px">Measured benchmark values (optional JSON)</label><textarea id="benchmarkValues" rows="8" placeholder='{"critical_requirement_realization":1.0,"weighted_requirement_realization":0.95,"critical_e2e":1.0,"other_e2e":0.95,"critical_security_findings":0,"governance_violations":0,"evidence_coverage":0.95,"autonomous_repair_success":0.8,"regression_free_repair":0.9,"human_implementation_intervention":0.1,"portable_capabilities_passing":1.0,"reference_functional_parity":0.95}'></textarea><div class="row" style="margin-top:12px"><button onclick="verifyFactory()">Run factory verification</button><button onclick="factorySelfTest()">Run self-test</button><button onclick="workspaceReport()">Generate workspace report</button><button onclick="runBenchmark()">Run frontier benchmark</button></div><pre id="verifyOut"></pre>
</section>

<section id="frontier" class="card"><h2>6. Frontier browser-LLM co-work</h2><p>Use a frontier provider's normal web interface. Software_Factory prepares the engineering context, prompt, and exportable context package; you can then bring the downloaded solution ZIP back into this GUI. This does not scrape or impersonate a third-party consumer web GUI.</p>
<div class="grid"><div><label>Engineering task</label><textarea id="frontierTask" placeholder="Example: redesign this platform for provider-neutral asynchronous execution and give me a complete architecture + migration plan."></textarea><label>Context paths (comma separated, optional)</label><input id="frontierContext" placeholder="README.md,docs/ARCHITECTURE.md"><div class="row"><button onclick="createFrontierSession()">Create co-work session</button><button class="secondary" onclick="openChatGPT()">Open ChatGPT Web</button></div><pre id="frontierOut"></pre></div><div><h3>Session handoff</h3><p class="muted">After creating a session, download the context bundle, use your frontier web LLM normally, download its resulting ZIP, then use Workspace → Integrate ZIP above.</p><div id="frontierLinks"></div><label>Returned solution ZIP</label><input id="zipFrontier" type="file" accept=".zip"><button onclick="integrateFrontierZip()">Integrate downloaded frontier ZIP</button></div></div>
</section>

<section id="export" class="card"><h2>7. Export / handoff</h2><p>Export the current workspace as a ZIP, so the system can be handed to another engineer, another chat, another Codespace, or a later Software_Factory release.</p><div class="row"><button onclick="exportWorkspace()">Download current workspace ZIP</button><button class="secondary" onclick="showEngineeringModel()">Show engineering model</button><button class="secondary" onclick="showState()">Show factory state</button></div><pre id="exportOut"></pre></section>

<section id="help" class="card"><h2>8. Help for absolute beginners</h2><div class="banner"><strong>You only need one CLI command for normal GUI operation:</strong><pre>python3 -m factory web --workspace workspaces/demo-import --host 0.0.0.0 --port 8787</pre>After the browser UI opens, use the buttons and forms on this page. Do not add <code>.cli</code> to the command. The canonical module is <code>factory</code>.</div><div class="banner warn" style="margin-top:10px"><strong>When CLI is necessary:</strong> bootstrapping the repository, starting the GUI if it was not auto-started, or diagnosing an environment problem. Routine target validation, planning, architecture generation, ZIP work, CRUD, benchmark, frontier handoff, and export are GUI operations.</div><div id="helpOut"></div></section>
</main>
<script>
let STATE={tree:[],workspaces:[],current:null,lastSession:null};
const $=id=>document.getElementById(id);
async function api(url, opts={}){const r=await fetch(url,opts);let d;try{d=await r.json()}catch{d={error:await r.text()}};if(!r.ok)throw new Error(d.error||`HTTP ${r.status}`);return d}
function out(id,d){$(id).textContent=typeof d==='string'?d:JSON.stringify(d,null,2)}
function err(id,e){out(id,{ok:false,error:String(e.message||e)})}
async function refreshAll(){await Promise.all([health(),refreshStatus(),refreshWorkspaceList(),refreshTargets(),refreshTree()])}
async function health(){try{$('health').textContent='GUI online';$('health').className='status good';out('startOut',await api('/api/health'))}catch(e){$('health').textContent='GUI error';$('health').className='status bad';err('startOut',e)}}
async function refreshStatus(){try{const d=await api('/api/status');STATE.current=d.current_workspace;$('currentWorkspace').innerHTML=`<div class="v">${esc(d.current_workspace)}</div><div class="l">${esc(d.workspace_type)} · ${d.file_count} files</div>`;$('fileCount').textContent=d.file_count;$('checkpointCount').textContent=d.checkpoint_count;$('eventCount').textContent=d.event_count}catch(e){err('startOut',e)}}
async function refreshWorkspaceList(){try{const d=await api('/api/workspaces');STATE.workspaces=d.workspaces;const s=$('workspaceList');s.innerHTML='';for(const w of d.workspaces){const o=document.createElement('option');o.value=w.path;o.textContent=`${w.name}${w.current?' (current)':''}`;s.appendChild(o)}}catch(e){err('workspaceOut',e)}}
async function refreshTargets(){try{const d=await api('/api/targets');const s=$('target');s.innerHTML='';for(const t of d.targets){const o=document.createElement('option');o.value=t.id;o.textContent=t.name;s.appendChild(o)}updateTargetName()}catch(e){err('designOut',e)}}
$('target').addEventListener('change',updateTargetName);function updateTargetName(){const o=$('target')?.selectedOptions?.[0];if(o)$('targetName').textContent=o.textContent}
async function createWorkspace(){try{const name=$('workspaceName').value.trim();if(!name)throw new Error('Enter a workspace name.');const d=await api('/api/workspace/create',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name})});out('workspaceOut',d);await refreshAll()}catch(e){err('workspaceOut',e)}}
async function switchWorkspace(){try{const path=$('workspaceList').value;if(!path)throw new Error('Choose a workspace.');const d=await api('/api/workspace/switch',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({path})});out('workspaceOut',d);await refreshAll()}catch(e){err('workspaceOut',e)}}
function fileOf(id){return $(id).files[0]}
async function importIncludedDemo(){try{const d=await api('/api/import-included-demo',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({workspace_name:'demo-import'})});out('zipOut',d);setNext('Imported the included demo. Next: open Files, click src/app.py, then make a small Update and create a checkpoint.');await refreshAll()}catch(e){err('zipOut',e)}}
async function importZipNew(){try{const f=fileOf('zipNew');if(!f)throw new Error('Choose a ZIP file.');const name=$('zipWorkspaceName').value.trim();if(!name)throw new Error('Enter the new workspace name.');const fd=new FormData();fd.append('file',f);fd.append('workspace_name',name);const d=await api('/api/import',{method:'POST',body:fd});out('zipOut',d);setNext('Imported a ZIP. Next: inspect the engineering model or continue to Files & CRUD.');await refreshAll()}catch(e){err('zipOut',e)}}
async function integrateZip(planOnly=false){try{const f=fileOf('zipIntegrate');if(!f)throw new Error('Choose a ZIP file.');const fd=new FormData();fd.append('file',f);fd.append('plan_only',String(planOnly));const d=await api('/api/integrate',{method:'POST',body:fd});out('zipOut',d);setNext(planOnly?'Plan-only integration complete. Next: review conflicts, then run integration again.':'ZIP integration complete. Next: run verification, then inspect the Files tree.');await refreshAll()}catch(e){err('zipOut',e)}}
async function validateTarget(){try{const d=await api('/api/spec-validate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({target:$('target').value})});out('designOut',d);setNext('Specification validated. Next: click Show engineering plan.')}catch(e){err('designOut',e)}}
async function makePlan(){try{const d=await api('/api/plan',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({target:$('target').value})});out('designOut',d);setNext('Engineering plan generated. Next: click Generate architecture.')}catch(e){err('designOut',e)}}
async function makeArchitecture(){try{const d=await api('/api/architecture',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({target:$('target').value})});out('designOut',d);setNext('Architecture package generated. Next: click Generate scaffold.')}catch(e){err('designOut',e)}}
async function makeScaffold(){try{const d=await api('/api/scaffold',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({target:$('target').value})});out('designOut',d);setNext('Scaffold generated. Next: go to Files to inspect/change it, then Verify.');await refreshTree()}catch(e){err('designOut',e)}}
async function repoInit(){try{out('buildOut',await api('/api/repo/init',{method:'POST'}));await refreshStatus()}catch(e){err('buildOut',e)}}
async function repoClone(){try{const url=$('repoUrl').value.trim(),name=$('cloneName').value.trim();if(!url||!name)throw new Error('Enter repository URL and clone destination name.');out('buildOut',await api('/api/repo/clone',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({url,name})}));await refreshWorkspaceList()}catch(e){err('buildOut',e)}}
async function gitStatus(){try{out('buildOut',await api('/api/repo/status'))}catch(e){err('buildOut',e)}}
async function gitDiff(){try{out('buildOut',await api('/api/repo/diff'))}catch(e){err('buildOut',e)}}
async function makeCheckpoint(){try{const label=$('checkpointLabel').value.trim();if(!label)throw new Error('Enter a checkpoint label.');out('buildOut',await api('/api/checkpoint',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({label})}));await refreshStatus()}catch(e){err('buildOut',e)}}
async function refreshTree(){try{const d=await api('/api/tree');STATE.tree=d.tree;renderTree()}catch(e){err('fileOut',e)}}
function renderTree(){const filter=($('treeFilter').value||'').toLowerCase();const box=$('tree');box.innerHTML='';const rows=STATE.tree.filter(x=>!filter||x.path.toLowerCase().includes(filter)).slice(0,1000);for(const x of rows){const span=document.createElement('span');span.textContent=x.path;span.title=x.kind==='file'?'Click to read':'';if(x.kind==='file')span.style.cursor='pointer',span.onclick=()=>readFile(x.path);box.appendChild(span);const meta=document.createElement('span');meta.className='small muted';meta.textContent=x.kind==='file'?`${x.size} bytes`:'';box.appendChild(meta);const b=document.createElement('button');b.className='secondary';b.textContent=x.kind==='file'?'Open':'—';b.disabled=x.kind!=='file';if(x.kind==='file')b.onclick=()=>readFile(x.path);box.appendChild(b)}}
async function readFile(path){$('filePath').value=path;try{const d=await api('/api/file?path='+encodeURIComponent(path));$('fileContent').value=d.content;out('fileOut',{ok:true,path})}catch(e){err('fileOut',e)}}
async function fileAction(action){try{const path=$('filePath').value.trim();if(!path)throw new Error('Enter/select a path.');let payload={action,path,content:$('fileContent').value,destination:$('fileDestination').value};const d=await api('/api/file',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});out('fileOut',d);await refreshTree();await refreshStatus()}catch(e){err('fileOut',e)}}
async function verifyFactory(){try{const d=await api('/api/verify');out('verifyOut',d);setNext('Factory verification complete. Next: generate the workspace report or run the benchmark.')}catch(e){err('verifyOut',e)}}
async function factorySelfTest(){try{const d=await api('/api/self-test');out('verifyOut',d);setNext('Factory self-test complete. Next: proceed to your target design workflow.')}catch(e){err('verifyOut',e)}}
async function workspaceReport(){try{out('verifyOut',await api('/api/report'))}catch(e){err('verifyOut',e)}}
async function runBenchmark(){try{let raw=$('benchmarkValues').value.trim();let values=null;if(raw) values=JSON.parse(raw);const d=await api('/api/benchmark',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({target:$('target').value,values})});out('verifyOut',d);setNext(d.measured?'Benchmark recorded. Next: use the evidence/result to decide the next engineering iteration.':'Benchmark is not measured yet. Next: enter evidence values or run the independent benchmark and bring the measurements back.')}catch(e){err('verifyOut',e)}}
async function createFrontierSession(){try{const task=$('frontierTask').value.trim();if(!task)throw new Error('Describe the engineering task.');const context=($('frontierContext').value||'').split(',').map(x=>x.trim()).filter(Boolean);const d=await api('/api/frontier/session',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({task,context_paths:context})});STATE.lastSession=d.session;out('frontierOut',d);setNext('Frontier co-work session prepared. Next: open the prompt/context, use the frontier web LLM normally, download its artifact ZIP, then integrate it here.');$('frontierLinks').innerHTML=`<p><a href="${d.prompt_url}" target="_blank">Open prompt</a> · <a href="${d.context_url}" target="_blank">Download context ZIP</a></p>`}catch(e){err('frontierOut',e)}}
function openChatGPT(){window.open('https://chatgpt.com/','_blank','noopener')}
async function integrateFrontierZip(){try{const f=fileOf('zipFrontier');if(!f)throw new Error('Choose the ZIP downloaded from the frontier web session.');const fd=new FormData();fd.append('file',f);fd.append('plan_only','false');const d=await api('/api/integrate',{method:'POST',body:fd});out('frontierOut',d);setNext('Frontier artifact integrated. Next: run verification and benchmark again.');await refreshAll()}catch(e){err('frontierOut',e)}}
function download(url){window.location.href=url}
function exportWorkspace(){window.location.href='/api/export'}
async function showEngineeringModel(){try{out('exportOut',await api('/api/engineering-model'))}catch(e){err('exportOut',e)}}
async function showState(){try{out('exportOut',await api('/api/state'))}catch(e){err('exportOut',e)}}
async function runAction(name){if(name==='factory-self-test')return factorySelfTest()}
function setNext(s){$('nextStep').innerHTML='<strong>Next step:</strong> '+esc(s)}
function esc(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
refreshAll();
</script>
</body></html>"""


def _parse_multipart(handler: BaseHTTPRequestHandler):
    ctype = handler.headers.get("Content-Type", "")
    length = int(handler.headers.get("Content-Length", "0"))
    if length > MAX_UPLOAD_BYTES:
        raise ValueError(f"Upload too large: {length} bytes")
    body = handler.rfile.read(length)
    msg = BytesParser(policy=default).parsebytes((f"Content-Type: {ctype}\r\n\r\n").encode() + body)
    parts = {}
    for p in msg.iter_parts():
        name = p.get_param("name", header="content-disposition")
        if not name:
            continue
        filename = p.get_filename()
        payload = p.get_payload(decode=True) or b""
        parts[name] = {"filename": filename, "bytes": payload, "text": payload.decode("utf-8", "replace")}
    return parts


def _load_targets(repo_root: Path):
    targets = []
    for p in sorted((repo_root / "specs" / "targets").glob("*.toml")):
        s = load_spec(p)
        targets.append({"id": p.stem, "name": s["target"]["name"], "path": str(p)})
    return targets


def _subprocess(repo_root: Path, args):
    p = subprocess.run(args, cwd=repo_root, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=300)
    return {"returncode": p.returncode, "output": redact(p.stdout)}


def make_server(initial_workspace: Path):
    initial_workspace = initial_workspace.resolve()
    allowed_root = initial_workspace.parent
    repo_root = Path(__file__).resolve().parent.parent
    current = {"path": initial_workspace}

    def ensure_workspace(path: Path):
        path = path.resolve()
        if allowed_root not in path.parents and path != allowed_root:
            raise ValueError("Workspace must remain inside the configured workspace directory.")
        path.mkdir(parents=True, exist_ok=True)
        return path

    ensure_workspace(current["path"])

    def workspace_list():
        allowed_root.mkdir(parents=True, exist_ok=True)
        rows = []
        for p in sorted(allowed_root.iterdir()):
            if not p.is_dir() or p.name.startswith("."):
                continue
            if (p / ".factory" / "workspace.json").exists() or (p / ".git").exists():
                rows.append({"name": p.name, "path": p.name, "current": p.resolve() == current["path"].resolve()})
        return rows

    class Handler(BaseHTTPRequestHandler):
        server_version = "Software_Factory_GUI/0.1.0"

        def log_message(self, fmt, *args):
            return

        @property
        def workspace(self):
            return ensure_workspace(current["path"])

        def json(self, obj, status=200):
            data = json.dumps(obj, ensure_ascii=False, indent=2).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def html(self):
            data = HTML.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def download(self, path: Path, filename: str | None = None, delete_after=False):
            if not path.exists() or not path.is_file():
                self.json({"error": "File not found"}, 404)
                return
            mime = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
            data = path.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", mime)
            self.send_header("Content-Disposition", f'attachment; filename="{filename or path.name}"')
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            if delete_after:
                try:
                    path.unlink()
                except OSError:
                    pass

        def do_GET(self):
            try:
                parsed = urllib.parse.urlparse(self.path)
                path = parsed.path
                q = urllib.parse.parse_qs(parsed.query)
                if path == "/": return self.html()
                if path == "/api/health": return self.json({"ok": True, "version": APP_VERSION, "mode": "gui-first"})
                if path == "/api/status":
                    w = self.workspace; st = load_state(w); inv = inventory(w)
                    return self.json({"current_workspace": str(w), "workspace_type": "software-factory-workspace", "file_count": inv["file_count"], "checkpoint_count": len(st.get("checkpoints", [])), "event_count": len(st.get("events", []))})
                if path == "/api/workspaces": return self.json({"workspaces": workspace_list(), "allowed_root": str(allowed_root)})
                if path == "/api/targets": return self.json({"targets": _load_targets(repo_root)})
                if path == "/api/tree": return self.json({"tree": list_tree(self.workspace)})
                if path == "/api/file":
                    rel = q.get("path", [""])[0]
                    return self.json({"path": rel, "content": read(self.workspace, rel)})
                if path == "/api/engineering-model":
                    p = self.workspace / ".factory" / "engineering-model.json"
                    if not p.exists():
                        model = discover_engineering_model(self.workspace)
                        p.write_text(json.dumps(model, indent=2, ensure_ascii=False), encoding="utf-8")
                    return self.json(json.loads(p.read_text(encoding="utf-8")))
                if path == "/api/state": return self.json(load_state(self.workspace))
                if path == "/api/export":
                    fd, tmp = tempfile.mkstemp(prefix=f"{self.workspace.name}-", suffix=".zip")
                    os.close(fd); out = Path(tmp); export_zip(self.workspace, out); return self.download(out, f"{self.workspace.name}.zip", delete_after=True)
                if path.startswith("/api/frontier/prompt/"):
                    sid = path.rsplit("/", 1)[-1]; p = self.workspace / ".factory" / "frontier_sessions" / sid / "PROMPT.md"; return self.download(p, "PROMPT.md")
                if path.startswith("/api/frontier/context/"):
                    sid = path.rsplit("/", 1)[-1]; session = self.workspace / ".factory" / "frontier_sessions" / sid
                    p = session / "CONTEXT.zip"
                    if not p.exists(): export_context_zip(self.workspace, session)
                    return self.download(p, "CONTEXT.zip")
                return self.json({"error": "not found"}, 404)
            except Exception as e:
                return self.json({"error": str(e)}, 400)

        def do_POST(self):
            try:
                path = urllib.parse.urlparse(self.path).path
                if path in {"/api/import", "/api/integrate"}:
                    parts = _parse_multipart(self)
                    if "file" not in parts or not parts["file"]["filename"]: raise ValueError("file field missing")
                    f = parts["file"]; name = Path(f["filename"]).name
                    tmp = Path(tempfile.mkstemp(prefix="sf-upload-", suffix=".zip")[1]); tmp.write_bytes(f["bytes"])
                    try:
                        if path == "/api/import":
                            ws_name = parts.get("workspace_name", {}).get("text", "imported-solution").strip()
                            ws = (allowed_root / ws_name).resolve()
                            if allowed_root not in ws.parents or ws.name.startswith("."): raise ValueError("Unsafe workspace name")
                            manifest = import_zip(tmp, ws)
                            current["path"] = ws
                            return self.json({"ok": True, "mode": "new-workspace", "workspace": str(ws), "manifest": manifest})
                        plan_only = parts.get("plan_only", {}).get("text", "false").lower() == "true"
                        plan = integrate_zip(tmp, self.workspace, apply_non_conflicting=not plan_only)
                        return self.json({"ok": True, "mode": "plan-only" if plan_only else "integrate", "plan": plan})
                    finally:
                        try: tmp.unlink()
                        except OSError: pass
                data = {}
                length = int(self.headers.get("Content-Length", "0"))
                if length:
                    raw = self.rfile.read(length)
                    data = json.loads(raw.decode("utf-8") or "{}")
                if path == "/api/import-included-demo":
                    ws_name = str(data.get("workspace_name", "demo-import")).strip() if 'data' in locals() else "demo-import"
                    if not ws_name or any(c in ws_name for c in "/\\") or ws_name in {".", ".."}: raise ValueError("Use a simple workspace name")
                    ws = (allowed_root / ws_name).resolve()
                    if allowed_root not in ws.parents: raise ValueError("Unsafe workspace name")
                    if ws.exists() and any(ws.iterdir()): raise FileExistsError(f"Workspace already exists and is not empty: {ws_name}")
                    manifest = import_zip(repo_root / "examples" / "shipped_solution.zip", ws)
                    current["path"] = ws
                    return self.json({"ok": True, "mode": "included-demo", "workspace": str(ws), "manifest": manifest})
                if path == "/api/workspace/create":
                    name = str(data.get("name", "")).strip()
                    if not name or any(c in name for c in "/\\") or name in {".", ".."}: raise ValueError("Use a simple workspace name")
                    ws = (allowed_root / name).resolve()
                    if ws.exists() and any(ws.iterdir()): raise FileExistsError(f"Workspace already exists and is not empty: {name}")
                    create_workspace(ws, name); current["path"] = ws; return self.json({"ok": True, "workspace": str(ws)})
                if path == "/api/workspace/switch":
                    rel = str(data.get("path", "")).strip(); ws = (allowed_root / rel).resolve()
                    if allowed_root not in ws.parents: raise ValueError("Workspace outside allowed root")
                    if not ws.is_dir(): raise FileNotFoundError(rel)
                    current["path"] = ws; return self.json({"ok": True, "workspace": str(ws)})
                if path == "/api/spec-validate":
                    spec = load_spec(repo_root / "specs" / "targets" / f"{data['target']}.toml")
                    return self.json({"valid": True, "target": spec["target"], "sha256": spec["_meta"]["sha256"]})
                if path == "/api/plan":
                    spec = load_spec(repo_root / "specs" / "targets" / f"{data['target']}.toml")
                    return self.json({"tasks": compile_tasks(spec), "requirements": requirement_graph(spec), "capabilities": capability_graph(spec)})
                if path == "/api/architecture":
                    spec = load_spec(repo_root / "specs" / "targets" / f"{data['target']}.toml"); out = self.workspace / "generated" / f"{data['target']}-architecture"; a = write_architecture(spec, out); return self.json({"output": str(out), "architecture": a})
                if path == "/api/scaffold":
                    spec = load_spec(repo_root / "specs" / "targets" / f"{data['target']}.toml"); out = self.workspace / "generated" / data['target']; result = render_scaffold(spec, out); return self.json({"output": str(result), "message": "Scaffold created"})
                if path == "/api/repo/init": return self.json(git(self.workspace, "init"))
                if path == "/api/repo/status": return self.json(git(self.workspace, "status", "--short", "--branch"))
                if path == "/api/repo/diff": return self.json(git(self.workspace, "diff", "--"))
                if path == "/api/repo/clone":
                    name = str(data.get("name", "")).strip(); url = str(data.get("url", "")).strip()
                    if not name or any(c in name for c in "/\\") or not url: raise ValueError("Enter repository URL and simple destination name")
                    dest = (allowed_root / name).resolve()
                    if allowed_root not in dest.parents: raise ValueError("Unsafe clone destination")
                    return self.json(clone(url, dest))
                if path == "/api/checkpoint": return self.json(checkpoint(self.workspace, str(data.get("label", "Checkpoint")), {"source": "gui"}))
                if path == "/api/file":
                    action, rel, content, dst = data.get("action"), data.get("path", ""), data.get("content", ""), data.get("destination", "")
                    if action == "create": result = str(create(self.workspace, rel, content))
                    elif action == "update": result = str(update(self.workspace, rel, content))
                    elif action == "read": result = read(self.workspace, rel)
                    elif action == "delete": result = delete(self.workspace, rel)
                    elif action == "copy": result = str(crud_copy(self.workspace, rel, dst))
                    elif action == "move": result = str(crud_move(self.workspace, rel, dst))
                    else: raise ValueError("Unknown file action")
                    return self.json({"ok": True, "action": action, "result": result})
                if path == "/api/verify": return self.json(_subprocess(repo_root, ["python3", "scripts/verify_factory.py"]))
                if path == "/api/self-test": return self.json(_subprocess(repo_root, ["python3", "-m", "factory", "self-test"]))
                if path == "/api/report": return self.json(write_workspace_report(self.workspace))
                if path == "/api/benchmark":
                    spec = load_spec(repo_root / "specs" / "targets" / f"{data['target']}.toml"); return self.json(benchmark(spec, self.workspace))
                if path == "/api/frontier/session":
                    context = [x for x in data.get("context_paths", []) if x]
                    s = create_session(self.workspace, data.get("task", ""), context); sid = s.name
                    export_context_zip(self.workspace, s, context or None)
                    return self.json({"ok": True, "session": str(s), "session_id": sid, "prompt_url": f"/api/frontier/prompt/{sid}", "context_url": f"/api/frontier/context/{sid}"})
                return self.json({"error": "not found"}, 404)
            except Exception as e:
                return self.json({"error": str(e)}, 400)

    return Handler


def serve(workspace: Path, host="127.0.0.1", port=8787):
    workspace = workspace.resolve()
    workspace.parent.mkdir(parents=True, exist_ok=True)
    workspace.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer((host, port), make_server(workspace))
    print(f"Software_Factory browser UI: http://{host}:{port}/", flush=True)
    server.serve_forever()
