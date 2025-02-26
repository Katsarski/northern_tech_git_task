"""
Test suite for validating the behavior of the 'git branch' command in 
different scenarios.
"""


import config
from helpers import common


def test_git_branch_no_branches(api_create_git_repo):
    """Test the git branch with no branches present"""
    
    api_create_git_repo

    result = common.run_shell_command('git branch')
    assert not result.stdout, "Expected empty stdout, but got: {result.stdout}"
    
    
def test_git_branch_with_branches(api_create_git_repo):
    """Test the git branch with at least one branch created"""
    
    test_branch_name = "test_branch"
    
    api_create_git_repo
    result = common.run_shell_command('git commit --allow-empty -m "Initial commit"')
    
    result = common.run_shell_command('git branch test_branch')
    
    assert not result.stdout, f"Expected empty stdout, but got: {result.stdout}"
    
    result = common.run_shell_command('git branch')
    
    expected_stdout = (f'* main\n  {test_branch_name}\n')
    
    common.compare_normalized_strings(result.stdout, expected_stdout)
    
    result = common.run_shell_command(f'git checkout {test_branch_name}', True)
    
    expected_stderr = f"Switched to branch '{test_branch_name}'\n"
    
    common.compare_normalized_strings(result.stderr, expected_stderr)
    
    assert not result.stdout
    assert result.returncode == 0, f"Expected return code 0, but got {result.returncode}"
    
    result = common.run_shell_command('git status')
    
    expected_stdout = 'On branch test_branch\nnothing to commit, working tree clean\n'
    
    common.compare_normalized_strings(result.stdout, expected_stdout)

def test_git_branch_delete_branch(api_create_git_repo):
    """Test the git branch delete command"""
    
    test_branch_name = "test_branch"
    
    api_create_git_repo
    result = common.run_shell_command('git commit --allow-empty -m "Initial commit"')
    
    result = common.run_shell_command('git branch test_branch')
    
    result = common.run_shell_command('git branch')
    
    expected_stdout = (f'* main\n  {test_branch_name}\n')
    
    common.compare_normalized_strings(result.stdout, expected_stdout)
    
    result = common.run_shell_command(f'git branch -d {test_branch_name}')
    
    assert f'Deleted branch {test_branch_name}' in result.stdout, f"Expected branch deletion message not found in stdout: {result.stdout}"
    assert not result.stderr, f"Expected empty stderr, but got: {result.stderr}"
    assert result.returncode == 0, f"Expected return code 0, but got {result.returncode}"
    
    result = common.run_shell_command('git branch')
    
    expected_stdout = (f'* main\n'), "Expected only the main branch to be present"
