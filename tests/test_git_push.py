import os
from conftest import get_repo_name
from helpers import common

TEST_FILE_NAME = 'README.md'

def test_git_push(api_create_git_repo):
    "Test the git push command with valid upstream branch"
    
    api_create_git_repo

    with open(TEST_FILE_NAME, 'w') as f:
        f.write('Test file content')
    result = common.run_shell_command(f'git add .')
    assert not result.stdout, "Error with git add."

    result = common.run_shell_command(f'git commit -m "initial commit"')
    assert 'initial commit' in result.stdout, "Commit failed."
    
    result = common.run_shell_command(f'git branch -M main')
    
    result = common.run_shell_command(f'git push -u origin main', with_errors=True)
    assert "branch 'main' set up to track 'origin/main'." in result.stdout, f"Expected to see tracking branch confirmation but got {result.stdout}"
    assert result.returncode == 0, f"Push command returned error code not 0 but {result.returncode}"

def test_git_push_no_upstream_branch_specified(api_create_git_repo):
    "Test the git push command by not providing upstream branch name"
    
    api_create_git_repo

    with open(TEST_FILE_NAME, 'w') as f:
        f.write('Test file content')
    result = common.run_shell_command(f'git add .')
    assert not result.stdout, "Error with git add."

    result = common.run_shell_command(f'git commit -m "initial commit"')
    assert 'initial commit' in result.stdout, "Commit failed."
    
    result = common.run_shell_command(f'git branch -M main')
    
    result = common.run_shell_command(f'git push -u', with_errors=True)
    assert f"fatal: The current branch main has no upstream branch" in result.stderr, f"Expected to find no upstream branch error but got {result.stderr}"

def test_push_invalid_syntax():
    "Test the git push command by providing the push argument with a syntax error"
    
    result = common.run_shell_command(f'git pushh -u origin main', with_errors=True)

    # We normalize the message so we don't get issues when running cross-platform due to \n\r
    expected_message = "git: 'pushh' is not a git command. See 'git --help'.\n\nThe most similar command is\n\tpush\n"
    normalized_stderr = ' '.join(result.stderr.split())
    normalized_expected = ' '.join(expected_message.split())
    assert normalized_stderr == normalized_expected, f"Expected: {normalized_expected}, but got: {normalized_stderr}"

def test_git_push_invalid_flag():
    "Test the git push command by providing a non existing flag"
    
    result = common.run_shell_command(f'git push -k origin main', with_errors=True)
    assert f"error: unknown switch `k" in result.stderr, f"Expected to find unknown flag error but got {result.stderr}"