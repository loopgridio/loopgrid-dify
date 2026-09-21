import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer

from tools.loopgrid_client import LoopGridClient, LoopGridError, parse_json_object


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        return

    def _json(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.headers.get("X-LoopGrid-Key") != "test-key":
            self._json(401, {"detail": "unauthorized"})
            return
        self._json(200, {"valid": True, "path": self.path})

    def do_POST(self):
        if self.headers.get("X-LoopGrid-Key") != "test-key":
            self._json(401, {"detail": "unauthorized"})
            return
        size = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(size) or b"{}")
        self._json(200, {"ok": True, "payload": payload, "path": self.path})


class LoopGridClientTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.thread.join(timeout=2)

    def test_parse_json_object(self):
        self.assertEqual(parse_json_object('{"a": 1}', "x"), {"a": 1})
        with self.assertRaises(ValueError):
            parse_json_object('[1]', "x")

    def test_credentials_and_get(self):
        client = LoopGridClient.from_credentials({"base_url": self.base_url, "api_key": "test-key", "workspace_id": "default"})
        result = client.get_json("/api/v1/decisions/abc/verify")
        self.assertTrue(result["valid"])

    def test_post_and_url_encoding(self):
        client = LoopGridClient(self.base_url, "test-key", "default")
        path = client.decision_path("a/b", "/events")
        self.assertEqual(path, "/api/v1/decisions/a%2Fb/events")
        result = client.post_json(path, {"event_type": "tool_executed"})
        self.assertEqual(result["payload"]["event_type"], "tool_executed")

    def test_safe_auth_error(self):
        client = LoopGridClient(self.base_url, "bad-secret-key", "default")
        with self.assertRaises(LoopGridError) as ctx:
            client.get_json("/api/v1/decisions")
        self.assertNotIn("bad-secret-key", str(ctx.exception))
        self.assertIn("HTTP 401", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
