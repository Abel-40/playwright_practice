from playwright.async_api import async_playwright
from urllib.parse import urljoin
import os
import asyncio
import json
import random

AUTH_FILE = "state/auth.json"
LOGIN_URL = "https://quotes.toscrape.com/login"
BASE_URL = "https://quotes.toscrape.com/"

# -------------------- LOGIN --------------------

async def go_login(page):
    print("Logging in...")
    await page.goto(LOGIN_URL)

    await page.get_by_label("Username").fill("abel")
    await page.get_by_label("Password").fill("12345678")
    await page.get_by_role("button", name="Login").click()

    # Wait until logout appears (proof of login)
    await page.locator("a[href='/logout']").wait_for(state="visible")


# -------------------- CONTEXT --------------------

async def get_authenticated_page(browser):
    os.makedirs("state", exist_ok=True)

    context_args = {
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "viewport": {"width": 1280, "height": 720}
    }

    if os.path.exists(AUTH_FILE):
        print("Loading saved session...")
        context = await browser.new_context(storage_state=AUTH_FILE, **context_args)
    else:
        print("No saved session found.")
        context = await browser.new_context(**context_args)

    page = await context.new_page()
    await page.goto(BASE_URL)

    # Validate login
    if await page.locator("a[href='/logout']").count() == 0:
        print("Session invalid. Logging in...")
        await go_login(page)
        await context.storage_state(path=AUTH_FILE)
        print("Session saved.")
    else:
        print("Session valid. Skipping login.")

    return page, context


# -------------------- EXTRACTION --------------------

async def extract_quotes_from_page(page):
    quotes_data = []

    quote_elements = await page.locator(".quote").all()

    for quote in quote_elements:
        try:
            text = await quote.locator(".text").inner_text()
            author = await quote.locator(".author").inner_text()

            # Extract multiple tags properly
            tags = await quote.locator(".tag").all_text_contents()

            author_link = await quote.get_by_text("(about)").get_attribute("href")
            author_url = urljoin(BASE_URL, author_link)

            quotes_data.append({
                "text": text,
                "author": author,
                "tags": tags,
                "about_author": author_url
            })

        except Exception as e:
            print(f"Error extracting quote: {e}")
            continue

    return quotes_data


# -------------------- MAIN SCRAPER --------------------

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        page, context = await get_authenticated_page(browser)

        all_quotes = []

        while True:
            # Wait for quotes to load
            await page.locator(".quote").first.wait_for()

            # Extract data
            quotes = await extract_quotes_from_page(page)
            all_quotes.extend(quotes)

            print(f"Collected {len(all_quotes)} quotes so far...")

            # Pagination
            next_btn = page.locator(".next a")

            if await next_btn.count() == 0:
                print("No more pages.")
                break

            old_url = page.url

            await next_btn.click()

            await page.wait_for_url(lambda url: url != old_url)
            await page.wait_for_load_state("networkidle")

            await asyncio.sleep(random.uniform(1, 2))

        # Save results
        with open("quotes.json", "w", encoding="utf-8") as f:
            json.dump(all_quotes, f, indent=4, ensure_ascii=False)

        print(f"Saved {len(all_quotes)} quotes.")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())