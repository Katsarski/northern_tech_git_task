"""
Test suite for validating the behavior of the 'git push' command in different scenarios.
"""


from helpers import common


def test_git_push(api_create_git_repo):
    """Test the git push command with a valid upstream branch."""
    
    api_create_git_repo

    common.create_test_file()

    result = common.run_shell_command('git add .')
    assert not result.stdout, f"Expected empty stdout, but got: {result.stdout}"

    result = common.run_shell_command('git commit -m "initial commit"')
    assert 'initial commit' in result.stdout, "Commit failed: expected message not found."

    result = common.run_shell_command('git branch -M main')

    result = common.run_shell_command('git push -u origin main', with_errors=True)
    assert (
        "branch 'main' set up to track 'origin/main'." in result.stdout
    ), f"Expected to see tracking branch confirmation, but got: {result.stdout}"

    assert (
        result.returncode == 0
    ), f"Push command returned error code {result.returncode} instead of 0."


def test_git_push_no_upstream_branch_specified(api_create_git_repo):
    """Test the git push command without specifying an upstream branch."""
    
    api_create_git_repo

    common.create_test_file()

    result = common.run_shell_command('git add .')
    assert not result.stdout, f"Expected empty stdout, but got: {result.stdout}"

    result = common.run_shell_command('git commit -m "initial commit"')
    assert 'initial commit' in result.stdout, "Commit failed: expected message not found."

    result = common.run_shell_command('git branch -M main')

    result = common.run_shell_command('git push -u', with_errors=True)
    assert (
        "fatal: The current branch main has no upstream branch" in result.stderr
    ), f"Expected error for no upstream branch, but got: {result.stderr}"


def test_push_invalid_syntax():
    """Test the git push command with an invalid syntax."""
    
    result = common.run_shell_command('git pushh -u origin main', with_errors=True)

    # Normalize the message to avoid cross-platform issues with \n\r
    expected_message = (
        "git: 'pushh' is not a git command. See 'git --help'.\n\n"
        "The most similar command is\n\tpush\n"
    )

    common.compare_normalized_strings(result.stderr, expected_message)


def test_git_push_invalid_flag():
    """Test the git push command with an invalid flag."""
    
    result = common.run_shell_command('git push -k origin main', with_errors=True)

    assert (
        "error: unknown switch `k" in result.stderr
    ), f"Expected error for unknown flag, but got: {result.stderr}"
