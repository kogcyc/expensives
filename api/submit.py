
import os
from datetime import datetime
from urllib.parse import parse_qs
from upstash_redis import Redis

def handler(request):
    if request.method != "POST":
        return {"statusCode": 405, "body": "Method Not Allowed"}

    # Read form data
    body = request.body.decode()
    data = parse_qs(body)
    x_letter = data.get('x', [None])[0]
    num_value = data.get('xxx', [None])[0]

    if not x_letter or not num_value:
        return {"statusCode": 400, "body": "Missing 'x' or 'xxx' value"}

    # Build key as yymmddhhmm
    key = datetime.utcnow().strftime("%y%m%d%H%M")
    value = f"{x_letter}{num_value}"

    # Connect to Redis (Vercel KV)
    kv_url = os.environ.get("KV_URL")
    kv_token = os.environ.get("KV_REST_API_READ_ONLY_TOKEN")
    if not kv_url or not kv_token:
        return {"statusCode": 500, "body": "Missing KV_URL or KV_REST_API_READ_ONLY_TOKEN"}

    redis = Redis(kv_url, kv_token)

    # Set key:value in Redis
    redis.set(key, value)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/plain"},
        "body": f"Stored {key}:{value}"
    }
