import json
import boto3
import os
import re

lambda_client = boto3.client("lambda")

EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

def handler(event, context):
    body = json.loads(event.get("body", "{}"))

    email = body.get("email")
    link = body.get("link")

    if not email or not re.match(EMAIL_REGEX, email):
        return {"statusCode": 400, "body": "Invalid email"}

    if not link or not link.startswith("http"):
        return {"statusCode": 400, "body": "Invalid link"}

    # async invoke worker
    lambda_client.invoke(
        FunctionName=os.environ["WORKER_FUNCTION_NAME"],
        InvocationType="Event",
        Payload=json.dumps({"email": email, "link": link})
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"message": f"accepted  for {email} and {link}"})
    }