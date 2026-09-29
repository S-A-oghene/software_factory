import tempfile, zipfile
from pathlib import Path
import unittest
from factory.repository import create_workspace, inventory
from factory.crud import create, read, update, delete, copy, move
from factory.ingest import import_zip
from factory.integration import integrate_zip
from factory.frontier import create_session
from factory.benchmark import benchmark
from factory.spec import load_spec
from factory.architecture import compile_architecture

class TestCore(unittest.TestCase):
    ROOT = Path(__file__).resolve().parents[1]
    def test_crud_and_import(self):
        with tempfile.TemporaryDirectory() as td:
            base=Path(td); w=base/'w'; create_workspace(w)
            create(w,'a/b.txt','one'); self.assertEqual(read(w,'a/b.txt'),'one')
            update(w,'a/b.txt','two'); self.assertEqual(read(w,'a/b.txt'),'two')
            copy(w,'a/b.txt','a/c.txt'); move(w,'a/c.txt','a/d.txt'); delete(w,'a/d.txt')
            z=base/'source.zip'
            src=base/'src'; src.mkdir(); (src/'hello.txt').write_text('hello')
            with zipfile.ZipFile(z,'w') as out: out.write(src/'hello.txt','hello.txt')
            imported=base/'imported'; m=import_zip(z,imported)
            self.assertEqual(m['inventory']['file_count'],1)  # hello + factory state files may be absent? inventory happens before events
            self.assertTrue((imported/'hello.txt').exists())
            create(w,'same.txt','base'); (src/'same.txt').write_text('incoming')
            with zipfile.ZipFile(z,'w') as out: out.write(src/'hello.txt','hello.txt'); out.write(src/'same.txt','same.txt')
            plan=integrate_zip(z,w)
            self.assertIn('same.txt',plan['conflicts']); self.assertIn('hello.txt',plan['added'])

    def test_frontier_session(self):
        with tempfile.TemporaryDirectory() as td:
            w=Path(td); create_workspace(w); create(w,'x.md','context')
            s=create_session(w,'build a resilient platform',['x.md'])
            self.assertTrue((s/'PROMPT.md').exists()); self.assertTrue((s/'SESSION.json').exists())

    def test_benchmark(self):
        with tempfile.TemporaryDirectory() as td:
            w=Path(td); create_workspace(w)
            s=load_spec(str(self.ROOT/'specs/targets/distributed-platform.toml'))
            r=benchmark(s,w,{'critical_requirement_realization':0.0})
            self.assertFalse(r['passed'])
            r=benchmark(s,w,{'critical_requirement_realization':1,'weighted_requirement_realization':1,'critical_e2e':1,'other_e2e':1,'evidence_coverage':1,'autonomous_repair_success':1,'regression_free_repair':1,'portable_capabilities_passing':1,'reference_functional_parity':1,'human_implementation_intervention':0})
            self.assertTrue(r['passed'])

    def test_architecture(self):
        s=load_spec(str(self.ROOT/'specs/targets/ampa-ai.toml'))
        a=compile_architecture(s)
        ids={x['id'] for x in a['components']}
        self.assertIn('world-model',ids); self.assertIn('safety-supervisor',ids)

if __name__=='__main__': unittest.main()
