import json
import boto3
import os
import re

lambda_client = boto3.client("lambda")

PANDA_SURVEY_REGEX = re.compile(
    r"^https://www\.pandaguestexperience\.com/\?cn=[^&]+&source=QR25$"
)


def handler(event, context):
    print("RAW EVENT:", event)

    body = event.get("body")

    if isinstance(body, str):
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            return {
                "statusCode": 400,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Methods": "POST,OPTIONS"
                },
                "body": json.dumps({
                    "error": "Invalid JSON body"
                })
            }

    if not isinstance(body, dict):
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "POST,OPTIONS"
            },
            "body": json.dumps({
                "error": "Invalid request body"
            })
        }

    email = body.get("email")
    link = body.get("link")

    # Basic validation
    if not email or not link:
        print("No link or no email returning 400...")
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "POST,OPTIONS"
            },
            "body": json.dumps({
                "error": "Missing email or link"
            })
        }

    # Validate Panda Express survey URL
    if not PANDA_SURVEY_REGEX.fullmatch(link):
        print(f"Invalid survey link rejected: {link}")

        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "POST,OPTIONS"
            },
            "body": json.dumps({
                "error": "Invalid Panda Express survey link"
            })
        }

    print(f"Valid Panda Express survey link: {link}")

    # Async invoke worker
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
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "POST,OPTIONS"
        },
        "body": json.dumps({
            "message": "accepted"
        })
    }

