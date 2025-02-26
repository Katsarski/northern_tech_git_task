"""
Test suite for validating the behavior of the 'git remote add origin' command in 
different scenarios.
"""


import os
from helpers import common


def test_git_remote_add_origin(api_create_git_repo):
    """Test the git remote add origin command."""
    
    repo_name = api_create_git_repo

    # Remove origin to avoid error if it already exists
    result = common.run_shell_command('git remote remove origin')
    result = common.run_shell_command(
        f'git remote add origin https://github.com/{os.getenv("GH_USERNAME")}/{repo_name}.git'
    )

    assert not result.stdout, f"Error adding remote origin for {repo_name}."


def test_git_remote_add_invalid_origin_existing_origin(api_create_git_repo):
    """Test the git remote add command when the remote is already added."""
    
    repo_name = api_create_git_repo

    result = common.run_shell_command(
        f'git remote add origin https://github.com/{os.getenv("GH_USERNAME")}/{repo_name}.git', 
        with_errors=True
    )

    assert (
        'error: remote origin already exists' in result.stderr
    ), f"Expected 'origin already exists' error, but got: {result.stderr}."


def test_git_remote_add_invalid_remote_syntax(api_create_git_repo):
    """Test the git remote add command with a syntax error in the remote argument."""
    
    repo_name = api_create_git_repo

    result = common.run_shell_command(
        f'git remot add origin https://github.com/{os.getenv("GH_USERNAME")}/{repo_name}.git', 
        with_errors=True
    )

    # Normalize the message to avoid cross-platform issues with \n\r
    expected_message = (
        "git: 'remot' is not a git command. See 'git --help'.\n\n"
        "The most similar command is\n\tremote\n"
    )

    common.compare_normalized_strings(result.stderr, expected_message)


def test_git_remote_add_invalid_remote_add_syntax(api_create_git_repo):
    """Test the git remote add command with a syntax error in the 'add' argument."""
    
    repo_name = api_create_git_repo

    result = common.run_shell_command(
        f'git remote adb origin https://github.com/{os.getenv("GH_USERNAME")}/{repo_name}.git', 
        with_errors=True
    )

    assert (
        "error: unknown subcommand: `adb" in result.stderr
    ), f"Expected error for wrong 'add' syntax, but got: {result.stderr}"


def test_git_remote_add_missing_remote_repo():
    """Test the git remote add command without providing a remote repository."""
    
    result = common.run_shell_command('git remote add origin', with_errors=True)

    assert (
        'usage: git remote add' in result.stderr
    ), f"Expected usage message for missing repository, but got: {result.stderr}"


def test_git_remote_add_origin_invalid_flag(api_create_git_repo):
    """Test the git remote add origin command with an invalid flag."""
    
    api_create_git_repo

    result = common.run_shell_command('git remote add origin -k', with_errors=True)

    assert (
        "error: unknown switch `k" in result.stderr
    ), f"Expected error for unknown flag, but got: {result.stderr}"
