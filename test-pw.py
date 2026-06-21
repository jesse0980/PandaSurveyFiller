from playwright.sync_api import sync_playwright
import random
import re
email = "cooljesseguy2@gmail.com"
link = "https://www.pandaguestexperience.com/?cn=2716-53768-2800-0015-0212-0106&source=QR25"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    try:
        page = browser.new_page()

        print("Navigating...")
        page.goto(link, wait_until="domcontentloaded")

        # Start survey
        page.wait_for_selector("#NextButton", state="visible")
        page.click("#NextButton")
        print("Clicked Start")

        # -------------------------
        # MAIN SURVEY LOOP (PAGES)
        # -------------------------
        while True:

            page.wait_for_timeout(random.randint(3000, 5000))


            # ---------------- #
            # Main Feedback Text
            # ---------------- #
            satisfaction_label = page.locator("label").filter(has_text="Please tell us in three or more sentences why you wer")
            if satisfaction_label.count() > 0:
                print("found satisfaction label!!!")

                # Get the textarea ID from the label's "for" attribute
                textarea_id = satisfaction_label.get_attribute("for")

                if textarea_id:

                    custom_message = (
                        "I had a great experience at Panda Express. "
                        "The food was fresh and the staff was friendly. "
                        "Everything was quick, clean, and accurate. My name is Jesse Landis and I am the #1 panda fan"
                    )

                    # Fill the linked textarea dynamically
                    textarea = page.locator(f"#{textarea_id}")
                    textarea.click()
                    textarea.type(
                        custom_message,
                        delay=random.randint(20, 50)
                    )

                    print(f"Filled textarea: {textarea_id}")

                else:
                    print("Label found but no 'for' attribute present.")

                page.wait_for_timeout(random.randint(2000, 2900))
            # -------------------------
            # RADIOS (per page)
            # -------------------------
            radio_rows = page.locator('tr[id^="FNSR"]')

            for i in range(radio_rows.count()):
                print("in radio rows!")
                row = radio_rows.nth(i)
                options = row.locator('td[role="radio"], td[class*="Opt"]')

                problem_question = page.locator("tr").filter(has_text="Did you have a problem during your experience?")
                employee_question = page.locator("tr").filter(has_text="Would you like to recognize")
                if problem_question.count() > 0 or employee_question.count() > 0:
                    if options.count() > 1:
                        options.nth(1).click()  # second option (No)
                        print("Problem page reached!!!")

                        page.wait_for_timeout(random.randint(1400, 1600))

                elif options.count() > 0:
                    options.first.click()
                    page.wait_for_timeout(random.randint(600, 1500))
                    print(f"Radio answered row {i + 1}")

            # -------------------------
            # CHECKBOXES (per page)
            # -------------------------
            checkboxes = page.locator("div.cataOption")

            count = checkboxes.count()
            print("Checkbox count:", count)
            if count > 0:
                random_index = random.randint(0, count - 1)
                checkbox = checkboxes.nth(random_index)
                checkbox.scroll_into_view_if_needed()
                checkbox.focus()
                page.wait_for_timeout(random.randint(150, 400))
                checkbox.press(" ")
                print(f"Selected checkbox #{random_index}")
                page.wait_for_timeout(random.randint(300, 700))

            # ----------------------------
            # Question for frequency
            # ----------------------------
            radios = page.locator("div.rbloption") if radio_rows.count() == 0 else None
            count = radios.count() if radios else 0
            print("Radio count:", count)
            if count > 0:
                random_index = random.randint(0, count - 1)
                radio = radios.nth(random_index)
                radio.scroll_into_view_if_needed()
                radio.focus()
                page.wait_for_timeout(random.randint(150, 400))
                radio.press(" ")
                print(f"Selected radio #{random_index}")
                page.wait_for_timeout(random.randint(300, 700))

            # -------------------------
            # Fill email
            # -------------------------
            email = "cooljesseguy2@gmail.com"

            email_label = page.locator('label').filter(
                has_text="Email Address"
            ).first

            confirm_label = page.locator('label').filter(
                has_text="Confirm Email"
            ).first
            
            if email_label.count() > 0 and confirm_label.count() > 0:
                email_input_id = email_label.get_attribute("for")
                confirm_input_id = confirm_label.get_attribute("for")

                email_box = page.locator(f"#{email_input_id}")
                confirm_box = page.locator(f"#{confirm_input_id}")

                email_box.scroll_into_view_if_needed()
                email_box.click()

                page.wait_for_timeout(random.randint(300, 800))

                email_box.type(
                    email,
                    delay=random.randint(40, 90)
                )

                page.wait_for_timeout(random.randint(400, 1000))

                confirm_box.scroll_into_view_if_needed()
                confirm_box.click()

                page.wait_for_timeout(random.randint(300, 800))

                confirm_box.type(
                    email,
                    delay=random.randint(40, 90)
                )

                print("Filled email fields")

                page.wait_for_timeout(random.randint(500, 1200))
            

            # -------------------------
            # NEXT BUTTON
            # -------------------------
            next_btn = page.locator("#NextButton")

            if next_btn.count() == 0:
                print("No Next button — survey complete")
                break

            page.wait_for_timeout(random.randint(200, 700))
            next_btn.click()
            print("Clicked Next")

        input("Press Enter to close...")

    except Exception as e:
        print("ERROR OCCURRED:", e)
        input("Press Enter to inspect...")

    finally:
        browser.close()

print(f"Done for email: {email}")