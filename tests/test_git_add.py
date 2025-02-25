import os
from helpers import common

TEST_FILE_NAME = 'README.md'

def test_git_add_all_files(api_create_git_repo):
    "Test the git add command by using the '.' wildcard to add all modified files for staging"
    
    api_create_git_repo
    with open(TEST_FILE_NAME, 'w') as f:
        f.write('Test file content')
    assert os.path.exists(TEST_FILE_NAME), f"{TEST_FILE_NAME} was not created."

    result = common.run_shell_command(f'git add .')
    assert not result.stdout, f"Expected to find empty stdout but got {result.stdout}"
    
def test_git_add_specific_file(api_create_git_repo):
    "Test the git add command by providing a specific file name for staging"
    
    api_create_git_repo
    with open(TEST_FILE_NAME, 'w') as f:
        f.write('Test file content')
    assert os.path.exists(TEST_FILE_NAME), f"{TEST_FILE_NAME} was not created."
    
    result = common.run_shell_command(f'git add {TEST_FILE_NAME}')
    assert not result.stdout, f"Expected to find empty stdout but got {result.stdout}"
    
def test_git_add_non_existing_file(api_create_git_repo):
    "Test the git add command by providing a file name that doesn't exist for staging"
    
    api_create_git_repo
    
    result = common.run_shell_command(f'git add {TEST_FILE_NAME}d', with_errors=True)
    assert f"fatal: pathspec '{TEST_FILE_NAME}d' did not match any files" in result.stderr, f"Expected to find not matching file error but got {result.stderr}"
    
def test_git_invalid_add_syntax(api_create_git_repo):
    "Test the git add command by providing add argument with a syntax error"
    
    api_create_git_repo
    
    result = common.run_shell_command(f'git addd {TEST_FILE_NAME}', with_errors=True)
    # We normalize the message so we don't get issues when running cross-platform due to \n\r
    expected_message = "git: 'addd' is not a git command. See 'git --help'.\n\nThe most similar command is\n\tadd\n"
    normalized_stderr = ' '.join(result.stderr.split())
    normalized_expected = ' '.join(expected_message.split())
    assert normalized_stderr == normalized_expected, f"Expected: {normalized_expected}, but got: {normalized_stderr}"
    
def test_git_add_no_file(api_create_git_repo):
    "Test the git add command by not providing any filename"
    
    api_create_git_repo
    
    result = common.run_shell_command(f'git add', with_errors=True)
    assert f"Nothing specified, nothing added" in result.stderr, f"Expected to find no files specified error but got {result.stderr}"
    
def test_git_add_invalid_flag(api_create_git_repo):
    "Test the git add command by providing a non existing flag"
    
    api_create_git_repo
    
    result = common.run_shell_command(f'git add -k', with_errors=True)
    assert f"error: unknown switch `k" in result.stderr, f"Expected to find unknown flag error but got {result.stderr}"