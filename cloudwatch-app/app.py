import json
import random
import time
import socket
import sys
import os
import boto3
from datetime import datetime
from botocore.exceptions import ClientError

# ----------------------------
# Logstash config
# -----------------------ca-----
LOGSTASH_HOST = os.getenv("LOGSTASH_HOST", "logstash")
LOGSTASH_PORT = int(os.getenv("LOGSTASH_PORT", 5044))

# ----------------------------
# CloudWatch config
# ----------------------------
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
LOG_GROUP = os.getenv("CW_LOG_GROUP", "demo-log-app")
LOG_STREAM = os.getenv("CW_LOG_STREAM", "ribesh-stream")

logs_client = boto3.client("logs", region_name=AWS_REGION)
sequence_token = None


def init_cloudwatch():
    """Ensure log group and stream exist"""
    global sequence_token

    try:
        logs_client.create_log_group(logGroupName=LOG_GROUP)
    except ClientError as e:
        if e.response["Error"]["Code"] != "ResourceAlreadyExistsException":
            raise

    try:
        logs_client.create_log_stream(
            logGroupName=LOG_GROUP,
            logStreamName=LOG_STREAM
        )
    except ClientError as e:
        if e.response["Error"]["Code"] != "ResourceAlreadyExistsException":
            raise

    # fetch sequence token if stream already exists
    streams = logs_client.describe_log_streams(
        logGroupName=LOG_GROUP,
        logStreamNamePrefix=LOG_STREAM
    )
    if streams["logStreams"]:
        sequence_token = streams["logStreams"][0].get("uploadSequenceToken")


def send_to_cloudwatch(log):
    """Send log event to CloudWatch Logs"""
    global sequence_token

    event = {
        "timestamp": int(time.time() * 1000),
        "message": json.dumps(log)
    }

    kwargs = {
        "logGroupName": LOG_GROUP,
        "logStreamName": LOG_STREAM,
        "logEvents": [event]
    }

    if sequence_token:
        kwargs["sequenceToken"] = sequence_token

    try:
        response = logs_client.put_log_events(**kwargs)
        sequence_token = response["nextSequenceToken"]
    except ClientError as e:
        print(f"CloudWatch send failed: {e}", file=sys.stderr)


def send_to_logstash(log):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((LOGSTASH_HOST, LOGSTASH_PORT))
        sock.sendall((json.dumps(log) + "\n").encode("utf-8"))
        sock.close()
    except Exception as e:
        print(f"Logstash send failed: {e}", file=sys.stderr)


# ----------------------------
# Main
# ----------------------------
init_cloudwatch()

while True:
    level = random.choice(["INFO", "ERROR"])
    action = random.choice(["login", "upload", "download"])

    log = {
        "@timestamp": datetime.utcnow().isoformat(),
        "level": level,
        "service": "ribesh-with-cloudwatch",
        "message": f"Action {'failed' if level == 'ERROR' else 'success'}: {action}"
    }

    # stdout (docker logs)
    print(json.dumps(log), flush=True)

    # Logstash
    send_to_logstash(log)

    # CloudWatch
    send_to_cloudwatch(log)

    time.sleep(5)
