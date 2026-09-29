import unittest
from factory.policy import validate_patch_size, validate_delete
class TestPolicy(unittest.TestCase):
    def test_small_patch(self):
        self.assertTrue(validate_patch_size('--- a/a.txt\n+++ b/a.txt\n@@\n-old\n+new\n'))
    def test_protected_delete(self):
        with self.assertRaises(PermissionError): validate_delete('.factory/state.json')
if __name__=='__main__': unittest.main()
