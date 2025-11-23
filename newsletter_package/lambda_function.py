import json
import os
import re
import boto3
from botocore.exceptions import ClientError

SNS_TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN")  # set via env var

sns = boto3.client("sns")

EMAIL_REGEX = re.compile(r"^[^@]+@[^@]+\.[^@]+$")

def build_response(status_code, body):
    # CORS headers included here
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",   # adjust to your domain for production
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
        },
        "body": json.dumps(body)
    }

def handle_options():
    return {
        "statusCode": 204,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
        },
        "body": ""
    }

def lambda_handler(event, context):
    # Handle HTTP API v2 proxy and CORS preflight
    http_method = None
    if event.get("httpMethod"):
        http_method = event["httpMethod"]
    elif event.get("requestContext") and event["requestContext"].get("http"):
        http_method = event["requestContext"]["http"].get("method")

    if http_method == "OPTIONS":
        return handle_options()

    try:
        body = event.get("body")
        if isinstance(body, str):
            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                return build_response(400, {"message": "Invalid JSON body."})
        elif isinstance(body, dict):
            data = body
        else:
            data = event.get("queryStringParameters") or {}

        email = (data.get("email") or "").strip()
        if not email or not EMAIL_REGEX.match(email):
            return build_response(400, {"message": "Provide a valid email in JSON payload: {"email": "you@example.com"}"})

        # Subscribe the email to SNS topic (user must confirm via email)
        response = sns.subscribe(
            TopicArn=SNS_TOPIC_ARN,
            Protocol='email',
            Endpoint=email,
            ReturnSubscriptionArn=False
        )

        return build_response(200, {"message": "Subscription requested. Check your email to confirm.", "sns_response": "pending_confirmation"})

    except ClientError as e:
        return build_response(500, {"message": "AWS ClientError", "error": str(e)})
    except Exception as e:
        return build_response(500, {"message": "Internal server error", "error": str(e)})