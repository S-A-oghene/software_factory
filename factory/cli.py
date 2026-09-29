from __future__ import annotations
import argparse, json
from pathlib import Path
from .spec import load_spec, spec_hash
from .planner import compile_tasks, requirement_graph, capability_graph
from .architecture import write_architecture
from .render import render_scaffold
from .repository import inventory, create_workspace, clone, export_zip, git
from .ingest import import_zip
from .integration import integrate_zip
from .crud import list_tree, create, read, update, delete, copy, move
from .frontier import create_session, export_context_zip
from .benchmark import benchmark
from .report import write_workspace_report


def cmd_self_test():
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)/'workspace'
        create_workspace(root)
        create(root,'src/app.py','VALUE=1\n')
        assert read(root,'src/app.py') == 'VALUE=1\n'
        update(root,'src/app.py','VALUE=2\n')
        copy(root,'src/app.py','src/app-copy.py')
        move(root,'src/app-copy.py','src/app-renamed.py')
        assert 'src/app-renamed.py' in {x['path'] for x in list_tree(root)}
        delete(root,'src/app-renamed.py')
        sess = create_session(root,'Design a provider-neutral distributed architecture',['src/app.py'])
        assert (sess/'PROMPT.md').exists()
        write_workspace_report(root)
        spec = {
            'target': {'name':'Self Test','version':'0.1.0','profile':'provider-neutral'},
            'requirements': [{'id':'REQ-1','statement':'do thing','critical':True,'weight':5}],
            'capabilities': {'required':['auditability']},
            'workflows': []
        }
        out = Path(td)/'generated'
        render_scaffold(spec,out)
        assert (out/'README.md').exists()
        tasks = compile_tasks(spec)
        assert tasks
        arch = write_architecture(spec,Path(td)/'arch')
        assert arch['components']
        result = benchmark(spec,root,{
            'critical_requirement_realization':1.0,
            'weighted_requirement_realization':1.0,
            'critical_e2e':1.0,
            'other_e2e':1.0,
            'evidence_coverage':1.0,
            'autonomous_repair_success':1.0,
            'regression_free_repair':1.0,
            'portable_capabilities_passing':1.0,
            'reference_functional_parity':1.0,
            'human_implementation_intervention':0.0,
        })
        assert result['passed']
    print('SELF_TEST_PASS')
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(prog='software-factory')
    sub = p.add_subparsers(dest='cmd', required=True)
    sub.add_parser('self-test')
    x=sub.add_parser('spec-validate'); x.add_argument('--spec',required=True)
    x=sub.add_parser('plan'); x.add_argument('--spec',required=True)
    x=sub.add_parser('architecture'); x.add_argument('--spec',required=True); x.add_argument('--output',default='generated/architecture')
    x=sub.add_parser('scaffold'); x.add_argument('--spec',required=True); x.add_argument('--output',required=True)
    x=sub.add_parser('import-zip'); x.add_argument('zip'); x.add_argument('--workspace',required=True)
    x=sub.add_parser('integrate-zip'); x.add_argument('zip'); x.add_argument('--workspace',required=True); x.add_argument('--plan-only',action='store_true')
    x=sub.add_parser('workspace-status'); x.add_argument('--workspace',required=True)
    x=sub.add_parser('crud-create'); x.add_argument('--workspace',required=True); x.add_argument('--path',required=True); x.add_argument('--content',default='')
    x=sub.add_parser('crud-read'); x.add_argument('--workspace',required=True); x.add_argument('--path',required=True)
    x=sub.add_parser('crud-update'); x.add_argument('--workspace',required=True); x.add_argument('--path',required=True); x.add_argument('--content',required=True)
    x=sub.add_parser('crud-delete'); x.add_argument('--workspace',required=True); x.add_argument('--path',required=True)
    x=sub.add_parser('crud-copy'); x.add_argument('--workspace',required=True); x.add_argument('--src',required=True); x.add_argument('--dst',required=True)
    x=sub.add_parser('crud-move'); x.add_argument('--workspace',required=True); x.add_argument('--src',required=True); x.add_argument('--dst',required=True)
    x=sub.add_parser('repo-init'); x.add_argument('--workspace',required=True)
    x=sub.add_parser('repo-clone'); x.add_argument('--url',required=True); x.add_argument('--workspace',required=True)
    x=sub.add_parser('export-zip'); x.add_argument('--workspace',required=True); x.add_argument('--output',required=True)
    x=sub.add_parser('frontier-session'); x.add_argument('--workspace',required=True); x.add_argument('--task',required=True); x.add_argument('--context',action='append',default=[])
    x=sub.add_parser('frontier-context-export'); x.add_argument('--workspace',required=True); x.add_argument('--session',required=True); x.add_argument('--context',action='append',default=[])
    x=sub.add_parser('benchmark'); x.add_argument('--spec',required=True); x.add_argument('--workspace',required=True); x.add_argument('--values-json',default='')
    x=sub.add_parser('web'); x.add_argument('--workspace',required=True); x.add_argument('--host',default='127.0.0.1'); x.add_argument('--port',type=int,default=8787)
    args=p.parse_args(argv)

    if args.cmd == 'self-test': return cmd_self_test()
    if args.cmd == 'spec-validate':
        s=load_spec(args.spec); print(json.dumps({'valid':True,'target':s['target'],'sha256':s['_meta']['sha256']},indent=2)); return 0
    if args.cmd == 'plan':
        s=load_spec(args.spec); print(json.dumps({'tasks':compile_tasks(s),'requirements':requirement_graph(s),'capabilities':capability_graph(s)},indent=2,ensure_ascii=False)); return 0
    if args.cmd == 'architecture':
        s=load_spec(args.spec); a=write_architecture(s,Path(args.output)); print(json.dumps(a,indent=2,ensure_ascii=False)); return 0
    if args.cmd == 'scaffold':
        s=load_spec(args.spec); print(render_scaffold(s,Path(args.output))); return 0
    if args.cmd == 'import-zip':
        m=import_zip(Path(args.zip),Path(args.workspace)); print(json.dumps(m,indent=2,ensure_ascii=False)); return 0
    if args.cmd == 'integrate-zip':
        m=integrate_zip(Path(args.zip),Path(args.workspace),apply_non_conflicting=not args.plan_only); print(json.dumps(m,indent=2,ensure_ascii=False)); return 0
    if args.cmd == 'workspace-status':
        print(json.dumps({'inventory':inventory(Path(args.workspace))},indent=2)); return 0
    if args.cmd == 'crud-create': print(create(Path(args.workspace),args.path,args.content)); return 0
    if args.cmd == 'crud-read': print(read(Path(args.workspace),args.path)); return 0
    if args.cmd == 'crud-update': print(update(Path(args.workspace),args.path,args.content)); return 0
    if args.cmd == 'crud-delete': print(delete(Path(args.workspace),args.path)); return 0
    if args.cmd == 'crud-copy': print(copy(Path(args.workspace),args.src,args.dst)); return 0
    if args.cmd == 'crud-move': print(move(Path(args.workspace),args.src,args.dst)); return 0
    if args.cmd == 'repo-init': print(json.dumps(git(Path(args.workspace),'init'),indent=2)); return 0
    if args.cmd == 'repo-clone': print(json.dumps(clone(args.url,Path(args.workspace)),indent=2)); return 0
    if args.cmd == 'export-zip': print(export_zip(Path(args.workspace),Path(args.output))); return 0
    if args.cmd == 'frontier-session':
        s=create_session(Path(args.workspace),args.task,args.context); print(s); return 0
    if args.cmd == 'frontier-context-export':
        print(export_context_zip(Path(args.workspace),Path(args.session),args.context)); return 0
    if args.cmd == 'benchmark':
        s=load_spec(args.spec); vals=json.loads(args.values_json) if args.values_json else None; print(json.dumps(benchmark(s,Path(args.workspace),vals),indent=2)); return 0
    if args.cmd == 'web':
        from .webapp import serve
        serve(Path(args.workspace),args.host,args.port); return 0
    return 2

if __name__ == '__main__':
    raise SystemExit(main())
