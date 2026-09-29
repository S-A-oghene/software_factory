from __future__ import annotations
import json
from pathlib import Path
from .model import Model
from .tools import inspect_repository, read_files, search_repository, apply_patch, git_diff, run_validation, ToolError
from .redact import redact

TOOLS=[
 {'type':'function','function':{'name':'inspect_repository','description':'Inspect repository structure','parameters':{'type':'object','properties':{},'additionalProperties':False}}},
 {'type':'function','function':{'name':'read_files','description':'Read relevant files','parameters':{'type':'object','properties':{'paths':{'type':'array','items':{'type':'string'},'maxItems':12}},'required':['paths'],'additionalProperties':False}}},
 {'type':'function','function':{'name':'search_repository','description':'Search repository text','parameters':{'type':'object','properties':{'query':{'type':'string'}},'required':['query'],'additionalProperties':False}}},
 {'type':'function','function':{'name':'apply_patch','description':'Apply a bounded unified patch','parameters':{'type':'object','properties':{'patch':{'type':'string'}},'required':['patch'],'additionalProperties':False}}},
 {'type':'function','function':{'name':'get_git_diff','description':'Inspect current repository diff','parameters':{'type':'object','properties':{},'additionalProperties':False}}},
]


def execute(root,name,args):
    if name=='inspect_repository': return inspect_repository(root)
    if name=='read_files': return read_files(root,args.get('paths',[]))
    if name=='search_repository': return search_repository(root,args.get('query',''))
    if name=='apply_patch': return apply_patch(root,args.get('patch',''))
    if name=='get_git_diff': return git_diff(root)
    if name=='run_validation': return {'error':'run_validation is deliberately exposed through deterministic factory orchestration, not as arbitrary LLM command execution'}
    raise ToolError('Unknown tool: '+name)


def run_task(model: Model, root: Path, task: dict, max_calls=12):
    messages=[{'role':'user','content':json.dumps({'task':task,'repository':inspect_repository(root)},ensure_ascii=False)}]
    history=[]; applied=False
    for call in range(1,max_calls+1):
        response=model.complete(messages,TOOLS); msg=response.message; history.append({'call':call,'message':msg}); messages.append(msg)
        calls=msg.get('tool_calls') or []
        if not calls:
            return {'status':'COMPLETED' if applied else 'PLANNED','calls':call,'history':history,'final':redact(str(msg.get('content',''))),'changed':applied}
        for tc in calls:
            fn=tc.get('function',{}); name=fn.get('name'); args=json.loads(fn.get('arguments') or '{}')
            try: result=execute(root,name,args); applied = applied or name=='apply_patch'
            except Exception as e: result={'error':redact(str(e))}
            messages.append({'role':'tool','tool_call_id':tc.get('id',f'call-{call}'),'content':redact(json.dumps(result,ensure_ascii=False) if not isinstance(result,str) else result)})
    return {'status':'CALL_LIMIT','calls':max_calls,'history':history,'final':'call budget exhausted','changed':applied}
