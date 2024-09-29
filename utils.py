import os
import re
import asyncio

PLACEHOLDER="@"
USER_STEPS_FILE_PATH = "user_steps.txt"
OUTPUT_HTML_FILE_PATH = "output.html"

def replace_in_fill(content: str, replacement: str = PLACEHOLDER) -> str:
    return re.sub(r'\.fill\(".*?"\)', f'.fill("{replacement}")', content)

def load_file(file_path):
    """
    Loads the content of a file.
    
    :param file_path: Path to the file (string)
    :return: Content of the file (string)
    """
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return f"Error: File {file_path} not found."
    except Exception as e:
        return f"Error loading file: {e}"


async def exec_command(command):
    """
    Executes a shell command asynchronously.
    
    :param command: Command to be executed (string)
    :return: Output of the command execution (string)
    """
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    stdout, stderr = await process.communicate()

    if process.returncode == 0:
        return stdout.decode('utf-8')
    else:
        return stderr.decode('utf-8') or f"Error executing command: {process.returncode}"


def delete_file(file_path):
    """Delete a specified file.

    Args:
        file_path (str): The path of the file to delete.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        PermissionError: If the user does not have permission to delete the file.
    """
    try:
        os.remove(file_path)
        print(f"File '{file_path}' has been deleted successfully.")
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except PermissionError:
        print(f"Error: You do not have permission to delete '{file_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

def save_file(file_path, content):
    """
    Saves content to a file.
    
    :param file_path: Path to the file (string)
    :param content: Content to be saved (string)
    :return: True if successful, False otherwise
    """
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        return True
    except Exception as e:
        print(f"Error saving file: {e}")
        return False