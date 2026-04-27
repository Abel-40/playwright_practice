from playwright.async_api import async_playwright
from urllib.parse import urljoin
import asyncio

async def main():
  async with async_playwright() as p:
    browser = await p.chromium.launch(headless=True)
    page = await browser.new_page()
    url = "http://books.toscrape.com/"
    await page.goto(url=url)

    books = []
    rating_map = {
      "One":1,
      "Two":2,
      "Three":3,
      "Four":4,
      "Five":5
    }
    while True:
      items = await page.locator(".product_pod").all()
      
      for book in items:
        title_element = book.locator("h3 a")
        title = await title_element.get_attribute("title")
        link = await title_element.get_attribute("href")
        full_link = urljoin(url,link)
        price = await book.locator(".price_color").inner_text()
        rate_clases = await book.locator(".star-rating").get_attribute("class")
        rate_word = rate_clases.replace("star-rating","").strip()
        rate = rating_map.get(rate_word,0)
        
        books.append(
          {
            "title":title,
            "price":price,
            "rate":rate,
            "link":full_link,
            "description":""
          }
        )
      next = page.locator(".next a")
      if await next.count() == 0:
        break
      
      old_url = page.url
      await next.click()
      
      await page.wait_for_url(lambda url: url != old_url)
      await page.wait_for_selector(".product_pod")
      
      
    await browser.close()
    print(f"Total books--->> {len(books)}")

if __name__ == "__main__":
  asyncio.run(main())