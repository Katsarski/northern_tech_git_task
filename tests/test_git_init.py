"""
Test suite for validating the behavior of the 'git init' command in different scenarios. 
"""


import os
from helpers import common


def test_git_init(api_create_git_repo):
    """Test the git init command."""
    
    repo_name = api_create_git_repo

    repo_path = os.path.join('test_repos', repo_name)
    
    assert (
        repo_path in os.getcwd()
    ), f"Expected repository path '{repo_path}' not found in current working directory."


def test_git_init_invalid_name():
    """Test the git init command with an invalid repository name containing whitespaces."""
    
    result = common.run_shell_command(
        'git init test_repos/test repo with whitespaces', with_errors=True
    )

    assert (
        'usage: git init' in result.stderr
    ), f"Expected usage-related error when trying to init repo, but got: {result.stderr}"


def test_git_init_invalid_syntax():
    """Test the git init command with an invalid syntax."""
    
    result = common.run_shell_command(
        'git int test_repos/test repo with whitespaces', with_errors=True
    )

    # Normalize the message to avoid cross-platform issues with \n\r
    expected_message = (
        "git: 'int' is not a git command. See 'git --help'.\n\n"
        "The most similar command is\n\tinit\n"
    )

    common.compare_normalized_strings(result.stderr, expected_message)


def test_git_init_invalid_flag():
    """Test the git init command with an invalid flag."""
    
    result = common.run_shell_command(
        'git init -k test_repos/test_repo', with_errors=True
    )

    assert (
        'usage: git init' in result.stderr
    ), f"Expected usage-related error when trying to init repo, but got: {result.stderr}"

    assert (
        "error: unknown switch `k" in result.stderr
    ), f"Expected unknown flag error, but got: {result.stderr}"
