import json
import random
import time
import socket
import sys
from datetime import datetime

LOGSTASH_HOST = "<your-logstash-host>"      #<-- replace with your Logstash host
LOGSTASH_PORT = 5044

def send_to_logstash(log):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((LOGSTASH_HOST, LOGSTASH_PORT))
        sock.sendall((json.dumps(log) + "\n").encode("utf-8"))
        sock.close()
    except Exception as e:
        print(f"Logstash send failed: {e}", file=sys.stderr)

while True:
    level = random.choice(["INFO", "ERROR"])
    action = random.choice(["login", "upload", "download"])

    log = {
        "@timestamp": datetime.utcnow().isoformat(),
        "level": level,
        "service": "ribesh-app-main",
        "message": f"Action {'failed' if level=='ERROR' else 'success'}: {action}"
    }

    # 1️⃣ stdout  docker logs
    print(json.dumps(log), flush=True)

    # 2️⃣ logstash  elk
    send_to_logstash(log)

    time.sleep(5)