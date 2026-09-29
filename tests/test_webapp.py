import json
import tempfile
import threading
import urllib.request
from pathlib import Path
import unittest

from factory.repository import create_workspace
from factory.webapp import make_server


class TestWebGUI(unittest.TestCase):
    def test_health_status_targets_and_crud(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "workspaces" / "demo"
            create_workspace(root, "demo")
            server = __import__('http.server').server.ThreadingHTTPServer(("127.0.0.1", 0), make_server(root))
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            base = f"http://127.0.0.1:{server.server_address[1]}"
            try:
                def get(path):
                    with urllib.request.urlopen(base + path, timeout=5) as r:
                        return json.loads(r.read().decode())
                def post(path, payload):
                    req = urllib.request.Request(base + path, data=json.dumps(payload).encode(), headers={"Content-Type":"application/json"}, method="POST")
                    with urllib.request.urlopen(req, timeout=5) as r:
                        return json.loads(r.read().decode())
                self.assertTrue(get('/api/health')['ok'])
                self.assertGreaterEqual(len(get('/api/targets')['targets']), 4)
                self.assertEqual(get('/api/status')['file_count'], 0)
                self.assertTrue(post('/api/file', {'action':'create','path':'src/app.py','content':'VALUE=1\n'})['ok'])
                self.assertEqual(get('/api/file?path=src%2Fapp.py')['content'], 'VALUE=1\n')
                self.assertTrue(post('/api/file', {'action':'update','path':'src/app.py','content':'VALUE=2\n'})['ok'])
                self.assertTrue(post('/api/file', {'action':'copy','path':'src/app.py','destination':'src/copy.py'})['ok'])
                self.assertTrue(post('/api/file', {'action':'move','path':'src/copy.py','destination':'src/moved.py'})['ok'])
                self.assertTrue(post('/api/file', {'action':'delete','path':'src/moved.py'})['ok'])
                st = get('/api/tree')
                self.assertTrue(any(x['path']=='src/app.py' for x in st['tree']))

                self.assertTrue(post('/api/spec-validate', {'target':'mow'})['valid'])
                plan = post('/api/plan', {'target':'mow'})
                self.assertTrue(plan['tasks'])
                arch = post('/api/architecture', {'target':'mow'})
                self.assertTrue(arch['architecture']['components'])
                scaff = post('/api/scaffold', {'target':'mow'})
                self.assertIn('generated', scaff['output'])
                self.assertTrue(post('/api/checkpoint', {'label':'GUI test checkpoint'})['label'])
                self.assertTrue(get('/api/engineering-model')['version'])

            finally:
                server.shutdown(); thread.join(timeout=3); server.server_close()


if __name__ == '__main__':
    unittest.main()
