import os

import pytest
from helpers import common

def test_git_remote_add_origin(api_create_git_repo):
    "Test the git remote add origin command"
    
    repo_name = api_create_git_repo
    # Remove origin so we don't get an error that it is already added
    result = common.run_shell_command(f'git remote remove origin')
    result = common.run_shell_command(f'git remote add origin https://github.com/{os.getenv("GH_USERNAME")}/{repo_name}.git')
    assert not result.stdout, f"Error adding remote origin for {repo_name}."

def test_git_remote_add_invalid_origin_existing_origin(api_create_git_repo):
    "Test the git remote add command by providing the remote when remote was already added"
    
    repo_name = api_create_git_repo
    
    result = common.run_shell_command(f'git remote add origin https://github.com/{os.getenv("GH_USERNAME")}/{repo_name}.git', with_errors=True)
    assert 'error: remote origin already exists' in result.stderr, f"Expected to see origin already exists error but got {result.stderr}."

def test_git_remote_add_invalid_remote_syntax(api_create_git_repo):
    "Test the git remote add command by providing the remote argument with a syntax error"
    
    repo_name = api_create_git_repo
    
    result = common.run_shell_command(f'git remot add origin https://github.com/{os.getenv("GH_USERNAME")}/{repo_name}.git', with_errors=True)

    # We normalize the message so we don't get issues when running cross-platform due to \n\r
    expected_message = "git: 'remot' is not a git command. See 'git --help'.\n\nThe most similar command is\n\tremote\n"
    normalized_stderr = ' '.join(result.stderr.split())
    normalized_expected = ' '.join(expected_message.split())
    assert normalized_stderr == normalized_expected, f"Expected: {normalized_expected}, but got: {normalized_stderr}"

def test_git_remote_add_invalid_remote_add_syntax(api_create_git_repo):
    "Test the git remote add command by providing the add argument with a syntax error"
    
    repo_name = api_create_git_repo
    
    result = common.run_shell_command(f'git remote adb origin https://github.com/{os.getenv("GH_USERNAME")}/{repo_name}.git', with_errors=True)
    assert "error: unknown subcommand: `adb" in result.stderr, f"Expected to find error for wrong add usage but got {result.stderr}"

@pytest.skip("This test is expected to fail as there is an issue with the error message")
def test_git_remote_add_invalid_remote_add_origin_syntax(api_create_git_repo):
    "Test the git remote add command by providing the origin argument with a syntax error"
    
    repo_name = api_create_git_repo
    
    result = common.run_shell_command(f'git remote add originncxzsda https://github.com/{os.getenv("GH_USERNAME")}/{repo_name}.git', with_errors=True)
    assert result.stderr, "Expected to fail as there is potentially an issue with the error returned (described in the readme.md)"
    
def test_git_remote_add_missing_remote_repo():
    "Test the git remote add by not providing a remote repo"
    
    result = common.run_shell_command(f'git remote add origin', with_errors=True)
    assert 'usage: git remote add' in result.stderr, f"Expected to see the usage message but got {result.stderr} instead"

def test_git_remote_add_origin_invalid_flag(api_create_git_repo):
    "Test the git remote add origin command by providing a non existing flag"

    api_create_git_repo
    
    result = common.run_shell_command(f'git remote add origin -k', with_errors=True)
    assert f"error: unknown switch `k" in result.stderr, f"Expected to find unknown flag error but got {result.stderr}"
