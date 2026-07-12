import json
import boto3
import os

lambda_client = boto3.client("lambda")

def handler(event, context):
    print("RAW EVENT:", event)

    body = event.get("body")

    if isinstance(body, str):
        body = json.loads(body)

    email = body.get("email")
    link = body.get("link")

    # basic validation
    if not email or not link:
        print("no link or no email returning 400...")
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing email or link"})
        }

    # async invoke worker
    lambda_client.invoke(
        FunctionName=os.environ["WORKER_FUNCTION_NAME"],
        InvocationType="Event",
        Payload=json.dumps({
            "email": email,
            "link": link
        })
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "accepted"})
    }