import os
from helpers import common

def test_git_init(api_create_git_repo):
    "Test the git init command"
    
    repo_name = api_create_git_repo
    
    repo_path = os.path.join('test_repos', repo_name)
    assert repo_path in os.getcwd(), f"Expected repository path '{repo_path}' not found in current working dir"

def test_git_init_invalid_name():
    "Test the git init command by providing invalid repo name that contains whitespaces"
    
    result = common.run_shell_command(f'git init test_repos/test repo with whitespaces', with_errors=True)
    assert 'usage: git init' in result.stderr, f"Expected failure when trying to init repo but got {result.stderr}"
    
def test_git_init_invalid_syntax():
    "Test the git init command by providing the init argument with a syntax error"
    
    result = common.run_shell_command(f'git int test_repos/test repo with whitespaces', with_errors=True)

    # We normalize the message so we don't get issues when running cross-platform due to \n\r
    expected_message = "git: 'int' is not a git command. See 'git --help'.\n\nThe most similar command is\n\tinit\n"
    normalized_stderr = ' '.join(result.stderr.split())
    normalized_expected = ' '.join(expected_message.split())
    assert normalized_stderr == normalized_expected, f"Expected: {normalized_expected}, but got: {normalized_stderr}"
    
def test_git_init_invalid_flag():
    "Test the git commit command by providing a non existing flag"
    
    result = common.run_shell_command(f'git init -k test_repos/test_repo', with_errors=True)
    assert 'usage: git init' in result.stderr, f"Expected failure when trying to init repo but got {result.stderr}"
    assert f"error: unknown switch `k" in result.stderr, f"Expected to find unknown flag error but got {result.stderr}"
