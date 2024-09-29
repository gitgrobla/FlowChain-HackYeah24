from utils import load_file, save_file, USER_STEPS_FILE_PATH, OUTPUT_HTML_FILE_PATH, PLACEHOLDER
HTML = """"""
def inject_user_steps(lines: str) -> str:
    return f"""
import asyncio
import re
from playwright.async_api import Playwright, async_playwright, expect


async def run(playwright: Playwright) -> None:
    global HTML
    browser = await playwright.chromium.launch()
    context = await browser.new_context()
    page = await context.new_page()
    
    {lines.strip()}

    HTML = await page.content()
    # ---------------------
    await context.close()
    await browser.close()


async def run_playwright() -> str:
    async with async_playwright() as playwright:
        await run(playwright)
        """

def assemble_user_steps(code: str, inputs: list[str]) -> str:
    for i, inp in enumerate(inputs):
        code = code.replace(PLACEHOLDER, f"{inp}", 1) 
    return code

async def eval_user_steps(*inputs) -> str:
    content = load_file(USER_STEPS_FILE_PATH)
    injected_code = inject_user_steps(content)

    assembled_code = assemble_user_steps(injected_code, inputs)
    
    exec(assembled_code)
    asyncio.run(run_playwright())
    save_file(OUTPUT_HTML_FILE_PATH, HTML)