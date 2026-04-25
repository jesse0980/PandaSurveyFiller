import json

def handler(event, context):
    print("RAW EVENT:", event)

    body = event.get("body")

    # If body is already dict
    if isinstance(body, dict):
        parsed = body

    # If body is string
    elif isinstance(body, str):
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError:
            # 🔥 THIS IS YOUR CURRENT FAILURE MODE
            print("BAD BODY RECEIVED:", body)
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid JSON body", "raw": body})
            }
    else:
        parsed = {}

    return {
        "statusCode": 200,
        "body": json.dumps(parsed)
    }