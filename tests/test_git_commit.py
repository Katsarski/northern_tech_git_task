"""
Test suite for validating the behavior of the 'git commit' command in different scenarios.
"""


from helpers import common


def test_git_commit(api_create_git_repo):
    """Test the git commit command with the -m flag."""
    
    api_create_git_repo

    common.create_test_file()

    result = common.run_shell_command('git add .')
    assert not result.stdout, f"Expected empty stdout, but got {result.stdout}"

    result = common.run_shell_command('git commit -m "initial commit"')
    assert "initial commit" in result.stdout, "Commit failed: expected message not found."


def test_git_invalid_commit_syntax():
    """Test the git commit command with an invalid syntax."""
    
    result = common.run_shell_command('git comit -m "test message"', with_errors=True)

    # Normalize the message to avoid cross-platform issues with \n\r
    expected_message = (
        "git: 'comit' is not a git command. See 'git --help'.\n\n"
        "The most similar command is\n\tcommit\n"
    )

    common.compare_normalized_strings(result.stderr, expected_message)


def test_git_commit_empty_message(api_create_git_repo):
    """Test the git commit command with an empty commit message."""
    
    api_create_git_repo

    common.create_test_file()

    result = common.run_shell_command('git add .')
    assert not result.stdout, f"Expected empty stdout, but got: {result.stdout}"

    result = common.run_shell_command('git commit -m ""', with_errors=True)

    assert (
        "Aborting commit due to empty commit message." in result.stderr
    ), f"Expected empty commit message error, but got: {result.stderr}"


def test_git_commit_invalid_flag():
    """Test the git commit command with an invalid flag."""
    
    result = common.run_shell_command('git commit -k "test message"', with_errors=True)

    assert (
        "error: unknown switch `k" in result.stderr
    ), f"Expected unknown flag error, but got: {result.stderr}"
