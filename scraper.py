from playwright.async_api import async_playwright
import asyncio

async def main():
  async with async_playwright() as p:
    browser = await p.chromium.launch(headless=True)
    page = await browser.new_page()
    
    await page.goto("https://facebook.com")
    title = await page.title()
    print(f"title::--->> {title}")
    
    url = await page.url()
    print(f"page url::---->> {url}")
    
    await page.screenshot(path="screenshots/fb_test.png")
    
    await browser.close()
  