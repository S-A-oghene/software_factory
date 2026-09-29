import unittest
from factory.spec import load_spec, spec_hash
class TestSpec(unittest.TestCase):
    def test_all_targets(self):
        for name in ['mow.toml','ng-opportunity-intelligence.toml','distributed-platform.toml','ampa-ai.toml']:
            s=load_spec('specs/targets/'+name); self.assertTrue(spec_hash(s))
if __name__=='__main__': unittest.main()
