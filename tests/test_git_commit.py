from helpers import common

TEST_FILE_NAME = 'README.md'

def test_git_commit(api_create_git_repo):
    "Test the git commit command with -m flag"
    
    api_create_git_repo

    with open(TEST_FILE_NAME, 'w') as f:
        f.write('Test file content')

    result = common.run_shell_command(f'git add .')
    assert not result.stdout, "Error with git add."

    result = common.run_shell_command(f'git commit -m "initial commit"')
    assert 'initial commit' in result.stdout, "Commit failed."
    
def test_git_invalid_commit_syntax():
    "Test the git commit command by providing the commit argument with a syntax error"
    
    result = common.run_shell_command(f'git comit -m "test message"', with_errors=True)
    
    # We normalize the message so we don't get issues when running cross-platform due to \n\r
    expected_message = "git: 'comit' is not a git command. See 'git --help'.\n\nThe most similar command is\n\tcommit\n"
    normalized_stderr = ' '.join(result.stderr.split())
    normalized_expected = ' '.join(expected_message.split())
    assert normalized_stderr == normalized_expected, f"Expected: {normalized_expected}, but got: {normalized_stderr}"

def test_git_commit_empty_message(api_create_git_repo):
    "Test the git commit command by not providing any commit message"
    
    api_create_git_repo

    with open(TEST_FILE_NAME, 'w') as f:
        f.write('Test file content')

    result = common.run_shell_command(f'git add .')
    assert not result.stdout, "Error with git add."
    
    result = common.run_shell_command(f'git commit -m ""', with_errors=True)
    assert f"Aborting commit due to empty commit message." in result.stderr, f"Expected to find empty commit message error but got {result.stderr}"

def test_git_commit_invalid_flag():
    "Test the git commit command by providing a non existing flag"
    
    result = common.run_shell_command(f'git commit -k "test message"', with_errors=True)
    assert f"error: unknown switch `k" in result.stderr, f"Expected to find unknown flag error but got {result.stderr}"