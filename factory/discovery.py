from __future__ import annotations
import json
from pathlib import Path
from .paths import should_skip

MANIFESTS = {
    "package.json":"node/javascript ecosystem",
    "pyproject.toml":"python project",
    "requirements.txt":"python dependencies",
    "Cargo.toml":"rust project",
    "go.mod":"go project",
    "pom.xml":"java maven project",
    "build.gradle":"java/gradle project",
    "build.gradle.kts":"kotlin/gradle project",
    "Package.swift":"swift project",
    "Dockerfile":"container build",
    "docker-compose.yml":"compose deployment",
    "docker-compose.yaml":"compose deployment",
    "wrangler.toml":"cloudflare worker",
    "wrangler.jsonc":"cloudflare worker",
}

def discover_engineering_model(root: Path):
    files=[]; manifests=[]; tests=[]; entry_candidates=[]
    for p in sorted(root.rglob('*')):
        if not p.is_file() or should_skip(p.relative_to(root)): continue
        rel=p.relative_to(root).as_posix(); files.append(rel)
        if p.name in MANIFESTS: manifests.append({'path':rel,'type':MANIFESTS[p.name]})
        if '/tests/' in f'/{rel}' or rel.startswith('tests/') or p.name.startswith('test_') or p.name.endswith('.test.ts') or p.name.endswith('.spec.ts'): tests.append(rel)
        if p.name in {'main.py','app.py','server.py','manage.py','index.js','index.ts','main.ts','Main.java'}: entry_candidates.append(rel)
    return {
        'version':'0.1.0',
        'file_count':len(files),
        'manifests':manifests,
        'test_candidates':tests[:1000],
        'entry_candidates':entry_candidates[:200],
        'architecture_hints':{
            'has_backend': any(x in rel.lower() for rel in files for x in ('server','api','backend','worker')) ,
            'has_frontend': any(x in rel.lower() for rel in files for x in ('frontend','web','ui','app.tsx','app.jsx')) ,
            'has_infra': bool(manifests) and any(x['type'] in {'container build','compose deployment','cloudflare worker'} for x in manifests),
            'has_tests': bool(tests),
        },
        'next_questions':[
            'What are the critical business journeys?',
            'What are the trust/security boundaries?',
            'What data stores and event semantics are authoritative?',
            'Which provider capabilities must remain replaceable?',
            'Which non-functional requirements are release-blocking?',
        ],
    }
