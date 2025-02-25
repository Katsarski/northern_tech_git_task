import os
import random
import string
import subprocess
import logging


def run_shell_command(command, with_errors=False):
    """
    Executes a given shell command and returns all the std I/O streams and the program return code

    Parameters:
    - command (str): The shell command to execute
    - with_errors (bool): If False, the function asserts that there are no errors in the command execution

    Returns:
    - The std out, err streams along with the program return code

    Raises:
    - AssertionError: If with_errors is False and the command results in an error or non zero return code.
    """
    
    logging.info(f"Executing shell command: {command}")
    logging.info(f"Current working directory: {os.getcwd()}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    logging.info(f"Shell command stdout: {result.stdout}")
    logging.info(f"Shell command stderr: {result.stderr}")
    logging.info(f"Shell command return code: {result.returncode}")
    
    if not with_errors:
        assert not result.stderr, f"Expected no errors but got {result.stderr}"
        assert result.returncode == 0, f"Expected return code 0 but got {result.returncode}"
    return result

def generate_repo_name(name_length=15):
    """
    Generates a pseudo-random GitHub repository name with given length.
    The name consists of a combination of letters, digits, and allowed special characters

    Parameters:
    - name_length (int): The length of the repository name, defaults to 15

    Returns:
    - str: A randomly generated repository name suitable for github repos
    """
    
    allowed_special_chars = '-_.'
    repo_name = random.choice(string.ascii_letters) + random.choice(string.digits) + allowed_special_chars
    repo_name += ''.join(random.choices(string.ascii_letters + string.digits, k=name_length-len(repo_name)))
    logging.info(f"Generated test repo name: {repo_name}")
    return repo_name
