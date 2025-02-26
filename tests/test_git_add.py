"""
Test suite for validating the behavior of the 'git add' command in different scenarios.
"""

import os
from helpers import common

def test_git_add_all_files(api_create_git_repo):
    """Test the git add command using the '.' wildcard to stage all modified files."""
    
    api_create_git_repo
    test_file_name = common.create_test_file()

    assert os.path.exists(test_file_name), f"{test_file_name} was not created."

    result = common.run_shell_command('git add .')

    assert not result.stdout, f"Expected empty stdout, but got: {result.stdout}"


def test_git_add_specific_file(api_create_git_repo):
    """Test the git add command by staging a specific file."""
    
    api_create_git_repo
    test_file_name = common.create_test_file()

    assert os.path.exists(test_file_name), f"{test_file_name} was not created."

    result = common.run_shell_command(f'git add {test_file_name}')

    assert not result.stdout, f"Expected empty stdout, but got: {result.stdout}"


def test_git_add_non_existing_file(api_create_git_repo):
    """Test the git add command by providing a non-existent file."""
    
    api_create_git_repo

    test_file_name = common.create_test_file()

    result = common.run_shell_command(f'git add {test_file_name}d', with_errors=True)

    assert (
        f"fatal: pathspec '{test_file_name}d' did not match any files" in result.stderr
    ), f"Expected error for missing file, but got: {result.stderr}"


def test_git_invalid_add_syntax(api_create_git_repo):
    """Test the git add command by providing an invalid add argument."""
    
    api_create_git_repo

    test_file_name = common.create_test_file()

    result = common.run_shell_command(f'git addd {test_file_name}', with_errors=True)

    expected_message = (
        "git: 'addd' is not a git command. See 'git --help'.\n\n"
        "The most similar command is\n\tadd\n"
    )

    common.compare_normalized_strings(result.stderr, expected_message)
    
    
def test_git_add_no_file(api_create_git_repo):
    """Test the git add command without providing a filename."""
    
    api_create_git_repo

    result = common.run_shell_command('git add', with_errors=True)

    assert "Nothing specified, nothing added" in result.stderr, (
        f"Expected error message about no files specified, but got: {result.stderr}"
    )


def test_git_add_invalid_flag(api_create_git_repo):
    """Test the git add command by providing a non-existing flag."""
    
    api_create_git_repo

    result = common.run_shell_command('git add -k', with_errors=True)

    assert (
        "error: unknown switch `k" in result.stderr
    ), f"Expected error message about unknown flag, but got: {result.stderr}"
