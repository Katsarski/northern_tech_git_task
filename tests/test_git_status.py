"""
Test suite for validating the behavior of the 'git status' command in 
different scenarios.
"""


import config
from helpers import common


def test_git_status_no_changes(api_create_git_repo):
    """Test the git status command without any changes to files"""
    
    api_create_git_repo

    result = common.run_shell_command('git status')
    expected_stdout = (
        'On branch main\n\nNo commits yet\n\nnothing to commit '
        '(create/copy files and use "git add" to track)\n'
                       )
    common.compare_normalized_strings(result.stdout, expected_stdout)

    common.create_test_file()

    result = common.run_shell_command('git status')
    
    expected_stdout = (
        'On branch main\n\nNo commits yet\n\nUntracked files:\n  (use "git add '
        '<file>..." to include in what will be committed)\n\tREADME.md\n\nnothing '
        'added to commit but untracked files present (use "git add" to track)\n'
    )
    common.compare_normalized_strings(result.stdout, expected_stdout)
    
def test_git_status_with_changed_file(api_create_git_repo):
    """Test the git status command with file ready for tracking"""
    
    api_create_git_repo

    common.create_test_file()

    result = common.run_shell_command('git status')
    
    expected_stdout = (
        'On branch main\n\nNo commits yet\n\nUntracked files:\n  (use "git add '
        '<file>..." to include in what will be committed)\n\tREADME.md\n\nnothing'
        ' added to commit but untracked files present (use "git add" to track)\n'
    )
    common.compare_normalized_strings(result.stdout, expected_stdout)
    

def test_git_status_with_tracked_file(api_create_git_repo):
    """Test the git status command with file that is tracked"""
    
    api_create_git_repo

    common.create_test_file()

    result = common.run_shell_command('git add .')

    result = common.run_shell_command('git status')
    
    expected_stdout = (
        'On branch main\n\nNo commits yet\n\nChanges to be committed:\n  (use "git '
        'rm --cached <file>..." to unstage)\n\tnew file:   README.md\n\n'
    )
    common.compare_normalized_strings(result.stdout, expected_stdout)
    

def test_git_status_invalid_flag():
    """Test the git status command with an invalid flag."""
    
    result = common.run_shell_command(f'git status -k', with_errors=True)

    assert (
        "error: unknown switch `k" in result.stderr
    ), f"Expected error for unknown flag, but got: {result.stderr}"


def test_git_invalid_status_syntax():
    """Test the git status command by providing an invalid status argument."""
        
    result = common.run_shell_command(f'git stats', with_errors=True)

    assert not result.stdout, f"Expected empty stdout, but got: {result.stdout}"
    expected_error = (
        "git: 'stats' is not a git command. See 'git --help'.\n\nThe most "
        "similar command is\n\tstatus\n"
    )
    
    common.compare_normalized_strings(result.stderr, expected_error)
    assert result.returncode == 1, f"Expected return code 1, but got {result.returncode}"
    
    
def test_git_status_after_pushing_files(api_create_git_repo):
    """Test the git status command after files are modified, staged, and pushed"""
    
    api_create_git_repo

    common.create_test_file()

    result = common.run_shell_command('git add .')
    assert not result.stdout, f"Expected empty stdout, but got: {result.stdout}"

    result = common.run_shell_command('git commit -m "initial commit"')
    assert 'initial commit' in result.stdout, "Commit failed: expected message not found."

    result = common.run_shell_command(f'git branch -M {config.DEFAULT_BRANCH}')

    result = common.run_shell_command(f'git push -u origin {config.DEFAULT_BRANCH}', with_errors=True)
    
    result = common.run_shell_command('git status')
    
    expected_stdout = (
        "On branch main\nYour branch is up to date with 'origin/main'.\n\nnothing to "
        "commit, working tree clean\n"
                       )
    common.compare_normalized_strings(result.stdout, expected_stdout)
