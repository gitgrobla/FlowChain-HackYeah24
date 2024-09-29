import asyncio
import re
from playwright.async_api import Playwright, async_playwright, expect


async def run(playwright: Playwright) -> None:
    browser = await playwright.chromium.launch()
    context = await browser.new_context()
    page = await context.new_page()
    
    

    print(await page.content())
    # ---------------------
    await context.close()
    await browser.close()


async def main() -> str:
    async with async_playwright() as playwright:
        await run(playwright)


asyncio.run(main())
