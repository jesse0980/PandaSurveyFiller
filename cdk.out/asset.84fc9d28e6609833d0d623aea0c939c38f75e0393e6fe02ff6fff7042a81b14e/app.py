from playwright.sync_api import sync_playwright
import json

def handler(event, context):
    email = event.get("email")
    link = event.get("link")

    if not link:
        return {
            "statusCode": 400,
            "body": "link is required"
        }

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                '--disable-setuid-sandbox', '--disable-gpu', '--single-process', '--no-zygote'
            ]
        )
        page = browser.new_page()
        page.goto(link, timeout=30000)
        page.wait_for_timeout(3000)
        browser.close()

    return {
        "statusCode": 200,
        "body": json.dumps({"status": f"page loaded for {link} with email {email}"})
    }