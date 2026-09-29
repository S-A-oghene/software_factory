from __future__ import annotations
import json, hashlib
from pathlib import Path
from .evidence import write_evidence

DEFAULTS = {
    'critical_requirement_realization': 1.0,
    'weighted_requirement_realization': 0.95,
    'critical_e2e': 1.0,
    'other_e2e': 0.95,
    'critical_security_findings': 0,
    'governance_violations': 0,
    'evidence_coverage': 0.95,
    'autonomous_repair_success': 0.80,
    'regression_free_repair': 0.90,
    'human_implementation_intervention': 0.10,
    'portable_capabilities_passing': 1.0,
    'reference_functional_parity': 0.95,
}


def score_record(values=None):
    measured = values is not None
    v = dict(DEFAULTS); v.update(values or {})
    failures = []
    if not measured:
        failures.append('benchmark_values_not_provided')
    if v['critical_requirement_realization'] < 1: failures.append('critical_requirement_realization')
    for key in ('weighted_requirement_realization','other_e2e','evidence_coverage','autonomous_repair_success','regression_free_repair','portable_capabilities_passing','reference_functional_parity'):
        if v[key] < DEFAULTS[key]: failures.append(key)
    if v['critical_e2e'] < 1: failures.append('critical_e2e')
    if v['critical_security_findings'] > 0: failures.append('critical_security_findings')
    if v['governance_violations'] > 0: failures.append('governance_violations')
    if v['human_implementation_intervention'] > DEFAULTS['human_implementation_intervention']:
        failures.append('human_implementation_intervention')
    return {'values': v, 'measured': measured, 'passed': measured and not failures, 'failed_gates': failures}


def benchmark(spec, root: Path, values=None, notes=None):
    record = score_record(values)
    record.update({
        'target': spec.get('target',{}),
        'factory_version': '0.1.0',
        'spec_hash': hashlib.sha256(json.dumps({k:v for k,v in spec.items() if k != '_meta'}, sort_keys=True).encode()).hexdigest(),
        'notes': notes or ([] if values is not None else ['No empirical benchmark values were supplied; this is a not-measured benchmark template.']),
    })
    out = root/'.factory'; out.mkdir(exist_ok=True)
    (out/'benchmark.json').write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding='utf-8')
    md = ['# Frontier Benchmark Result','',f"Target: {record['target'].get('name')}",f"PASS: {record['passed']}",'', '## Gates']
    for k,v in record['values'].items(): md.append(f'- `{k}` = `{v}`')
    md += ['', '## Failed gates']
    md += [f'- {x}' for x in record['failed_gates']] if record['failed_gates'] else ['- none']
    (out/'benchmark.md').write_text('\n'.join(md)+'\n', encoding='utf-8')
    write_evidence(spec, root, {'benchmark': record})
    return record
