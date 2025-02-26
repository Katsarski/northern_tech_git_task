"""
Test suite for validating the behavior of the 'git restore' command in different scenarios.
"""

from helpers import common

def test_git_restore_discard_changes(api_create_git_repo):
    """Test the git restore command to discard changes in the working directory."""
    
    api_create_git_repo
    test_file_name = common.create_test_file()

    result = common.run_shell_command('git add .')
    assert not result.stdout, f"Expected empty stdout, but got: {result.stdout}"

    result = common.run_shell_command('git commit -m "initial commit"')
    assert 'initial commit' in result.stdout, "Commit failed: expected message not found."

    with open(test_file_name, 'a', encoding='utf-8') as f:
        f.write(' More content')

    result = common.run_shell_command(f'git restore {test_file_name}')
    assert not result.stdout, f"Expected empty stdout, but got: {result.stdout}"

    with open(test_file_name, 'r', encoding='utf-8') as f:
        content = f.read()
    assert content == 'Test file content', f"Expected 'Test file content', but got: {content}"


def test_git_restore_staged_changes(api_create_git_repo):
    """Test the git restore command to unstage changes."""
    
    api_create_git_repo
    test_file_name = common.create_test_file()

    result = common.run_shell_command('git add .')
    assert not result.stdout, f"Expected empty stdout, but got: {result.stdout}"

    result = common.run_shell_command('git commit -m "initial commit"')
    assert 'initial commit' in result.stdout, "Commit failed: expected message not found."

    with open(test_file_name, 'a', encoding='utf-8') as f:
        f.write(' More content')

    result = common.run_shell_command('git add .')
    assert not result.stdout, f"Expected empty stdout, but got: {result.stdout}"

    # Restore the file to unstage changes
    result = common.run_shell_command(f'git restore --staged {test_file_name}')
    assert not result.stdout, f"Expected empty stdout, but got: {result.stdout}"

    # Verify the file is still modified but not staged
    with open(test_file_name, 'r', encoding='utf-8') as f:
        content = f.read()
    assert content == 'Test file content More content', f"Expected 'Test file content More content', but got: {content}"

    result = common.run_shell_command('git status')
    expected_stdout = (
        'On branch main\n'
        'Changes not staged for commit:\n'
        '  (use "git add <file>..." to update what will be committed)\n'
        '  (use "git restore <file>..." to discard changes in working directory)\n'
        '\n'
        '\tmodified:   README.md\n'
        '\n'
        'no changes added to commit (use "git add" and/or "git commit -a")\n'
    )
    common.compare_normalized_strings(result.stdout, expected_stdout)


def test_git_restore_from_commit(api_create_git_repo):
    """Test the git restore command to restore a file from a specific commit."""
    
    api_create_git_repo
    test_file_name = common.create_test_file()

    result = common.run_shell_command('git add .')
    assert not result.stdout, f"Expected empty stdout, but got: {result.stdout}"

    result = common.run_shell_command('git commit -m "initial commit"')
    assert 'initial commit' in result.stdout, "Commit failed: expected message not found."

    with open(test_file_name, 'a', encoding='utf-8') as f:
        f.write(' More content')

    result = common.run_shell_command('git add .')
    assert not result.stdout, f"Expected empty stdout, but got: {result.stdout}"

    result = common.run_shell_command('git commit -m "modified content"')
    assert 'modified content' in result.stdout, "Commit failed: expected message not found."

    # Get the commit hash of the initial commit
    result = common.run_shell_command('git log --format="%H" -n 1 HEAD~1')
    initial_commit_hash = result.stdout.strip()

    # Restore the file from the initial commit
    result = common.run_shell_command(f'git restore --source {initial_commit_hash} {test_file_name}')
    assert not result.stdout, f"Expected empty stdout, but got: {result.stdout}"

    # Verify the file content is restored to the initial commit
    with open(test_file_name, 'r', encoding='utf-8') as f:
        content = f.read()
    assert content == 'Test file content', f"Expected 'Test file content', but got: {content}"