"""
This module provides utility functions for interacting with the system shell,
generating random GitHub repository names, normalizing and comparing strings, 
and creating test files for use in a repository
"""

import os
import random
import string
import subprocess
import logging

def run_shell_command(command: str, with_errors: bool = False) -> subprocess.CompletedProcess:
    """
    Executes a given shell command and returns the std I/O streams and the program return code

    Parameters:
    - command: The shell command to execute
    - with_errors: If False, asserts that there are no errors in the command execution

    Returns:
    - subprocess.CompletedProcess: stdout, stderr, and returncode

    Raises:
    - AssertionError: If with_errors is False and the command results in an error or 
    a non zero program return code
    """
    
    logging.info(f"Executing shell command: {command}")
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    logging.info(f"stdout: {result.stdout}")
    logging.info(f"stderr: {result.stderr}")
    logging.info(f"return code: {result.returncode}")
    
    if not with_errors:
        assert not result.stderr, f"Expected no errors but got {result.stderr}"
        assert result.returncode == 0, f"Expected return code 0 but got {result.returncode}"
    
    return result


def generate_repo_name(name_length: int = 15) -> str:
    """
    Generates a random GitHub repository name by a given length.
    The name consists off a combination of letters, digits, and allowed special chars

    Parameters:
    - name_length: The length of the repository name (defaults to 15)

    Returns:
    - A random generated repo name
    """
    
    allowed_special_chars = '-_.' 
    repo_name = (random.choice(string.ascii_letters) + 
                 random.choice(string.digits) + allowed_special_chars)
    repo_name += (''.join(random.choices(string.ascii_letters + string.digits, 
                                         k=name_length - len(repo_name))))
    
    logging.info(f"Generated test repo with name: {repo_name}")
    
    return repo_name


def compare_normalized_strings(actual: str, expected: str):
    """
    Normalizes two input strings by removing extra whitespace characters and asserts equality

    Parameters:
    - actual: The actual string to compare
    - expected: The expected string to compare

    Raises:
    - AssertionError: If the strings do not match
    """
    
    # Normalize the message to avoid issues with \n\r across platforms
    normalized_actual = ' '.join(actual.split())
    normalized_expected = ' '.join(expected.split())
    
    assert normalized_actual == normalized_expected, (
        f"Expected: {normalized_expected}, but got: {normalized_actual}"
    )


def create_test_file() -> str:
    """
    Helper function to create a test file inside an initialized repo
    
    Returns:
    - Test file name that was created inside the repo from the given context
    """
    
    test_file_name = 'README.md'
    
    with open(test_file_name, 'w', encoding='utf-8') as f:
        f.write('Test file content')
    
    return test_file_name
