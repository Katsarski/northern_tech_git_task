"""
Test suite for validating the behavior of the 'git clone' command in different scenarios.
"""

import os
import pytest
import config
from helpers import common

@pytest.mark.parametrize("remote_only", [True])
def test_git_clone(api_create_git_repo, remote_only):
    """Test the git clone command by cloning a remote repository."""

    repo_name = api_create_git_repo
    repo_url = f"{config.GH_URL}/{config.GH_USERNAME}/{repo_name}"
    
    os.chdir('test_repos')
    
    result = common.run_shell_command(f'git clone {repo_url}', with_errors=True)

    assert not result.stdout, f"Expected empty stdout, but got: {result.stdout}"
    expected_error = (
        f"Cloning into '{repo_name}'...\n"
        "warning: You appear to have cloned an empty repository.\n"
    )
    
    common.compare_normalized_strings(result.stderr, expected_error)
    assert result.returncode == 0, f"Expected return code 0, but got {result.returncode}"


def test_git_invalid_clone_syntax():
    """Test the git clone command by providing an invalid clone argument."""
        
    result = common.run_shell_command(f'git clon {config.GH_URL}', with_errors=True)

    assert not result.stdout, f"Expected empty stdout, but got: {result.stdout}"
    expected_error = (
        "git: 'clon' is not a git command. See 'git --help'.\n"
        "\nThe most similar commands are\n\tclone\n\tcolumn\n"
    )
    
    common.compare_normalized_strings(result.stderr, expected_error)
    assert result.returncode == 1, f"Expected return code 1, but got {result.returncode}"
    
    
def test_git_clone_invalid_flag():
    """Test the git clone command by providing a non-existing flag."""
    
    result = common.run_shell_command(f'git clone {config.GH_URL} -k', with_errors=True)

    assert (
        "error: unknown switch `k" in result.stderr
    ), f"Expected error message about unknown flag, but got: {result.stderr}"
