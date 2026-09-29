from __future__ import annotations
import json
from pathlib import Path


def compile_architecture(spec):
    target = spec['target']
    profile = target.get('profile','provider-neutral')
    components = [
        {'id':'experience','responsibility':'browser/web experience and human oversight'},
        {'id':'application','responsibility':'domain workflows and policies'},
        {'id':'orchestrator','responsibility':'goal decomposition, scheduling and coordination'},
        {'id':'domain-agents','responsibility':'specialized business/engineering capabilities'},
        {'id':'data','responsibility':'transactional state, analytical state and evidence'},
        {'id':'events','responsibility':'asynchronous messages, jobs and replay'},
        {'id':'model-gateway','responsibility':'provider-neutral model/agent access'},
        {'id':'integration','responsibility':'external systems and provider adapters'},
        {'id':'observability','responsibility':'logs, metrics, traces and audit evidence'},
        {'id':'security-governance','responsibility':'identity, authorization, policy and trust boundaries'},
    ]
    if target.get('name','').upper().startswith('AMPA') or profile == 'cyber-physical':
        components += [
            {'id':'digital-thread','responsibility':'design/material/process/machine/quality lineage'},
            {'id':'world-model','responsibility':'simulation and state estimation'},
            {'id':'safety-supervisor','responsibility':'independent cyber-physical safety boundary'},
            {'id':'edge-control','responsibility':'real-time control integration; not LLM direct motor control'},
        ]
    return {
        'target': target,
        'principles': [
            'provider-neutral core','capability-driven architecture','evidence-first delivery',
            'deterministic validation','replaceable intelligence',
            'human governance for consequential actions'
        ],
        'components': components,
        'scale_profile': target.get('scale_profile','bootstrap'),
        'deployment_profiles': target.get('deployment_profiles',['zero-budget','generic-linux','docker','kubernetes']),
        'workflows': spec.get('workflows',[]),
        'required_capabilities': spec.get('capabilities',{}).get('required',[]),
    }


def write_architecture(spec, out: Path):
    out.mkdir(parents=True, exist_ok=True)
    arch = compile_architecture(spec)
    (out/'architecture.json').write_text(json.dumps(arch, indent=2, ensure_ascii=False), encoding='utf-8')
    md = ['# Generated Architecture Plan','',f"Target: {spec['target']['name']}",'', '## Components']
    for c in arch['components']:
        md.append(f"- **{c['id']}** — {c['responsibility']}")
    md += ['', '## Principles'] + [f'- {x}' for x in arch['principles']]
    md += ['', '## Deployment profiles'] + [f'- {x}' for x in arch['deployment_profiles']]
    (out/'architecture.md').write_text('\n'.join(md)+'\n', encoding='utf-8')
    return arch
