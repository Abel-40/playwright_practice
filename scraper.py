from playwright.async_api import async_playwright
import asyncio

from playwright.async_api import async_playwright
import asyncio

async def main():
  async with async_playwright() as p:
    browser = await p.chromium.launch(headless=False)
    page = await browser.new_page()
    
    await page.goto("http://localhost:5050/login?next=/")
    title = await page.title()
    await page.get_by_role("textbox",name="Email Address").click()
    await page.get_by_role("textbox",name="Email Address").press_sequentially("abel@gmail.com",delay=5)
    
    await page.get_by_role("textbox",name="Password").click()
    await page.get_by_role("textbox",name="Password").press_sequentially("Abel0916",delay=10)
    
    
    await page.get_by_role("button",name="Login").click()

    # await page.wait_for_load_state("networkidle")
    
        # await page.wait_for_selector("#sqleditor-container")
    await page.wait_for_selector('[id^="id-query-tool_"]', state="attached")

    frames = page.frame_locator('[id^="id-query-tool_"]')

    frame = frames.nth(1)  # adjust if needed

    # Wait INSIDE frame (important)
    input_box = frame.get_by_test_id("input-text")
    await input_box.wait_for(state="visible")

    await input_box.fill("Abel0916addis,80")
    await frame.locator('[data-test="save"]').click()
    await page.locator("#rc-tabs-1-tab-id-query-tool_6698600").get_by_text("public.roles/insight_stream/").click()
    await page.get_by_role("button",name="Execute script").click()
    
    await asyncio.sleep(10)
    print("log in to pgadmin")
    await page.screenshot(path=f"screenshots/{title}.png")
    
    
    await browser.close()
  
  
if __name__ == "__main__":
  asyncio.run(main())


# from playwright.async_api import async_playwright
# import asyncio
# import os

# async def main():
#     os.makedirs("screenshots", exist_ok=True)

#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=False)
#         page = await browser.new_page()

#         await page.goto("http://localhost:5050/login?next=/")

#         # Login
#         await page.get_by_role("textbox", name="Email Address").fill("abel@gmail.com")
#         await page.get_by_role("textbox", name="Password").fill("Abel0916")
#         await page.get_by_role("button", name="Login").click()

#         # --- THE FIX STARTS HERE ---
        
#         # Define the frame locator clearly. 
#         # Using .first or a filter is safer than .nth(1)
#         frame = page.frame_locator('iframe[id^="id-query-tool_"]').first

#         # Instead of waiting for the selector, we wait for a specific element 
#         # INSIDE the frame to be ready. This ensures the frame is fully loaded.
#         connect_input = frame.get_by_label("Connect to server").get_by_test_id("input-text")
        
#         # Give it a bit more time if your local server is slow
#         await connect_input.wait_for(state="visible", timeout=45000)
        
#         await connect_input.fill("Abel0916addis,80")
#         await frame.locator('[data-test="save"]').click()

#         # --- THE FIX ENDS HERE ---

#         await page.get_by_text("public.roles/insight_stream/").click()
#         await page.get_by_role("button", name="Execute script").click()

#         await asyncio.sleep(5)
        
#         # Take screenshot
#         title = await page.title()
#         safe_title = "".join([c if c.isalnum() else "_" for c in title])
#         await page.screenshot(path=f"screenshots/{safe_title}.png")

#         print("Logged in and executed script successfully")
#         await browser.close()

# if __name__ == "__main__":
#   asyncio.run(main())


async def main2():
  async with async_playwright() as p:
    browser = await p.chromium.launch(headless=True)
    page = await browser.new_page()
    
    await page.goto("https://amazon.com")
    title = await page.title()
    print(f"title::--->> {title}")
    
    url = page.url
    print(f"page url::---->> {url}")
    
    await page.screenshot(path="screenshots/amazon_test.png")
    
    await browser.close()

