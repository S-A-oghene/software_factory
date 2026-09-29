from __future__ import annotations


def compile_tasks(spec):
    tasks=[]
    def add(i,phase,title,detail,deps=None,mode='agent'):
        tasks.append({'id':i,'phase':phase,'title':title,'detail':detail,'deps':deps or [],'mode':mode,'status':'PENDING'})
    add('01-import-or-init','foundation','Establish workspace provenance','Initialize/import the source solution and record its identity',mode='deterministic')
    add('02-discover','foundation','Discover engineering model','Inventory repository, architecture, dependencies, tests, entry points and configuration',['01-import-or-init'],mode='deterministic')
    add('03-requirements','architecture','Compile requirements','Map user specification into weighted requirements and acceptance obligations',['02-discover'],mode='deterministic')
    add('04-capabilities','architecture','Compile capability graph','Derive provider-neutral capabilities from requirements',['03-requirements'],mode='deterministic')
    add('05-architecture','architecture','Compile architecture plan','Generate system topology, boundaries, workflows, data/event contracts and failure model',['04-capabilities'],mode='deterministic')
    add('06-design-review','frontier','Generate competing designs','Ask reasoning resources or browser frontier models for alternative architectures and critiques',['05-architecture'])
    add('07-implementation-plan','engineering','Compile implementation plan','Turn selected architecture into implementation, migration and validation work',['06-design-review'])
    add('08-integrate','engineering','Implement and integrate','Create/update repository artifacts and integrate imported or externally generated bundles',['07-implementation-plan'])
    add('09-verify','quality','Run deterministic verification','Run tests, static checks, traceability and policy validation',['08-integrate'],mode='deterministic')
    add('10-repair','quality','Repair failures','Autonomously diagnose and repair recoverable failures within bounded policy',['09-verify'])
    add('11-frontier-benchmark','quality','Run frontier benchmark','Compare the generated solution against the frozen benchmark and reference evidence',['10-repair'],mode='deterministic')
    add('12-evidence','release','Generate evidence pack','Create requirement coverage, provenance, benchmark and release evidence',['11-frontier-benchmark'],mode='deterministic')
    add('13-release','release','Prepare export','Checkpoint and export a reproducible release bundle',['12-evidence'],mode='deterministic')
    prev='13-release'
    for idx, req in enumerate(spec.get('requirements',[]),1):
        rid=str(req['id']); tid=f'R-{idx:03d}-{rid}'
        add(tid,'requirements',req.get('title',rid),req['statement'],[prev]); prev=tid
    if spec.get('requirements'):
        add('99-requirement-coverage','release','Prove critical coverage','Generate requirement to implementation/test evidence',['%s'%prev],mode='deterministic')
    return tasks


def requirement_graph(spec):
    nodes=[]; edges=[]
    for r in spec.get('requirements',[]):
        rid=str(r['id']); nodes.append({'id':rid,'type':'requirement','critical':bool(r.get('critical')),'weight':int(r.get('weight',5 if r.get('critical') else 1)),'statement':r['statement']})
        for tag in r.get('capabilities',[]): edges.append({'from':rid,'to':tag,'type':'requires_capability'})
    return {'nodes':nodes,'edges':edges}


def capability_graph(spec):
    nodes=[]; edges=[]
    caps=[]
    for c in spec.get('capabilities',{}).get('required',[]):
        caps.append(c)
        nodes.append({'id':c,'type':'capability'})
    for r in spec.get('requirements',[]):
        for c in r.get('capabilities',[]): edges.append({'from':str(r['id']),'to':c,'type':'requires'})
    return {'nodes':nodes,'edges':edges,'required':caps}
