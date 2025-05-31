import os
from datetime import datetime
from urllib.parse import parse_qs
from upstash_redis import Redis

def __vercel_python_handler__(request):
    if request.method != "POST":
        return {"statusCode": 405, "body": "Method Not Allowed"}

    body = request.body.decode()
    data = parse_qs(body)
    x_letter = data.get('x', [None])[0]
    num_value = data.get('num', [None])[0]

    allowed_letters = ['B', 'L', 'D', 'C', 'U', 'T', 'R', 'M']
    allowed_nums = [f"{i:03d}" for i in range(10, 1000, 10)]

    if x_letter not in allowed_letters or num_value not in allowed_nums:
        return {"statusCode": 400, "body": "Invalid input"}

    key = datetime.utcnow().strftime("%Y%m%d%H%M")
    value = f"{x_letter}{num_value}"

    kv_url = os.environ.get("KV_URL")
    kv_token = os.environ.get("KV_REST_API_READ_ONLY_TOKEN")
    if not kv_url or not kv_token:
        return {"statusCode": 500, "body": "Missing KV_URL or KV_REST_API_READ_ONLY_TOKEN"}

    redis = Redis(kv_url, kv_token)
    redis.set(key, value)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/plain"},
        "body": f"Stored {key}:{value}"
    }
