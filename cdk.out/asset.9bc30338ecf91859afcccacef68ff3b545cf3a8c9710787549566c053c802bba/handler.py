from playwright.sync_api import sync_playwright
import json

def handler(event, context):
    survey_url = event.get("survey_url")
    if not survey_url:
        return {
            "statusCode": 400,
            "body": "survey_url is required"
        }

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]
        )
        page = browser.new_page()
        page.goto(survey_url, timeout=30000)
        page.wait_for_timeout(3000)
        browser.close()

    return {
        "statusCode": 200,
        "body": json.dumps({"status": "page loaded"})
    }