"""
Test suite for validating the behavior of the 'git stash' command in different scenarios.
"""

from helpers import common

def test_git_stash_save(api_create_git_repo):
    """Test the git stash command to save changes in the working directory."""
    
    api_create_git_repo
    test_file_name = common.create_test_file()

    result = common.run_shell_command('git add .')
    assert not result.stdout, f"Expected empty stdout, but got: {result.stdout}"

    result = common.run_shell_command('git commit -m "initial commit"')
    assert 'initial commit' in result.stdout, "Commit failed: expected message not found."

    with open(test_file_name, 'a', encoding='utf-8') as f:
        f.write(' More content')

    # Stash the changes
    result = common.run_shell_command('git stash')
    assert 'Saved working directory and index state WIP on main' in result.stdout, (
        f"Expected stash save message, but got: {result.stdout}"
    )

    # Verify the working directory is clean
    result = common.run_shell_command('git status')
    expected_stdout = (
        'On branch main\n'
        'nothing to commit, working tree clean\n'
    )
    common.compare_normalized_strings(result.stdout, expected_stdout)


def test_git_stash_apply(api_create_git_repo):
    """Test the git stash command to apply stashed changes."""
    
    api_create_git_repo
    test_file_name = common.create_test_file()

    result = common.run_shell_command('git add .')
    assert not result.stdout, f"Expected empty stdout, but got: {result.stdout}"

    result = common.run_shell_command('git commit -m "initial commit"')
    assert 'initial commit' in result.stdout, "Commit failed: expected message not found."

    with open(test_file_name, 'a', encoding='utf-8') as f:
        f.write(' More content')

    # Stash the changes
    result = common.run_shell_command('git stash')
    assert 'Saved working directory and index state WIP on main' in result.stdout, (
        f"Expected stash save message, but got: {result.stdout}"
    )

    # Apply the stashed changes
    result = common.run_shell_command('git stash apply')
    assert 'Changes not staged for commit:' in result.stdout, (
        f"Expected stash apply message, but got: {result.stdout}"
    )

    # Verify the file content is restored
    with open(test_file_name, 'r', encoding='utf-8') as f:
        content = f.read()
    assert content == 'Test file content More content', f"Expected 'Test file content More content', but got: {content}"


def test_git_stash_drop(api_create_git_repo):
    """Test the git stash command to drop stashed changes."""
    
    api_create_git_repo
    test_file_name = common.create_test_file()

    result = common.run_shell_command('git add .')
    assert not result.stdout, f"Expected empty stdout, but got: {result.stdout}"

    result = common.run_shell_command('git commit -m "initial commit"')
    assert 'initial commit' in result.stdout, "Commit failed: expected message not found."

    with open(test_file_name, 'a', encoding='utf-8') as f:
        f.write(' More content')

    # Stash the changes
    result = common.run_shell_command('git stash')
    assert 'Saved working directory and index state WIP on main' in result.stdout, (
        f"Expected stash save message, but got: {result.stdout}"
    )

    # Drop the stashed changes
    result = common.run_shell_command('git stash drop')
    assert 'Dropped refs/stash@{0}' in result.stdout, (
        f"Expected stash drop message, but got: {result.stdout}"
    )

    # Verify the stash list is empty
    result = common.run_shell_command('git stash list')
    assert not result.stdout, f"Expected empty stash list, but got: {result.stdout}"


def test_git_stash_list(api_create_git_repo):
    """Test the git stash command to list stashed changes."""
    
    api_create_git_repo
    test_file_name = common.create_test_file()

    result = common.run_shell_command('git add .')
    assert not result.stdout, f"Expected empty stdout, but got: {result.stdout}"

    result = common.run_shell_command('git commit -m "initial commit"')
    assert 'initial commit' in result.stdout, "Commit failed: expected message not found."

    # Modify the file
    with open(test_file_name, 'a', encoding='utf-8') as f:
        f.write(' More content')

    # Stash the changes
    result = common.run_shell_command('git stash')
    assert 'Saved working directory and index state WIP on main' in result.stdout, (
        f"Expected stash save message, but got: {result.stdout}"
    )

    # List the stashed changes
    result = common.run_shell_command('git stash list')
    assert 'stash@{0}: WIP on main' in result.stdout, (
        f"Expected stash list message, but got: {result.stdout}"
    )