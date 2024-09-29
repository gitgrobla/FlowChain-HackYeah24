# saves extracted user steps to a file
import subprocess
import asyncio
from utils import exec_command, load_file, save_file, delete_file, replace_in_fill, USER_STEPS_FILE_PATH
import re

PLAYWRIGHT_FILE_PATH = "test.dev"
COMMAND = "playwright codegen --target python-async -o " + PLAYWRIGHT_FILE_PATH

def extract_page_lines(file_content: str) -> str:
    lines = file_content.splitlines()
    extracted_lines = [replace_in_fill(line) for line in lines if "page." in line]    

    return "\n".join(extracted_lines)

if __name__ == "__main__":
    asyncio.run(exec_command(COMMAND))
    content = load_file(PLAYWRIGHT_FILE_PATH)
    lines = extract_page_lines(content)
    save_file(USER_STEPS_FILE_PATH, lines)
    delete_file(PLAYWRIGHT_FILE_PATH)

