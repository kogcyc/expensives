from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs
from datetime import datetime
import os
from upstash_redis import Redis

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        data = parse_qs(body)
        x_letter = data.get('x', [None])[0]
        num_value = data.get('num', [None])[0]

        allowed_letters = ['B', 'L', 'D', 'C', 'U', 'T', 'R', 'M']
        allowed_nums = [f"{i:03d}" for i in range(10, 1000, 10)]

        if x_letter not in allowed_letters or num_value not in allowed_nums:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Invalid input")
            return

        key = datetime.utcnow().strftime("%Y%m%d%H%M")
        value = f"{x_letter}{num_value}"

        kv_url = os.environ.get("KV_URL")
        kv_token = os.environ.get("KV_REST_API_READ_ONLY_TOKEN")
        if not kv_url or not kv_token:
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Missing KV_URL or KV_REST_API_READ_ONLY_TOKEN")
            return

        redis = Redis(kv_url, kv_token)
        redis.set(key, value)

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(f"Stored {key}:{value}".encode('utf-8'))
