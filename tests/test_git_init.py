from helpers.git_utils import run_git_command, generate_repo_name, create_github_repo, delete_github_repo
import os
import shutil

def test_git_init():
    """Test the git init command"""
    repo_path = os.path.join('test_repos', generate_repo_name())
    result, error, code = run_git_command(f'init {repo_path}')
    assert code == 0
    assert 'Initialized empty Git repository' in result
    assert not error
    
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)
        print('Test repo dir removed successfully')
        
def test_git_create_repo():
    repo_name = generate_repo_name()
    repo_path = os.path.join('test_repos', repo_name)
    result, error, code = run_git_command(f'init {repo_path}')
    assert 'Initialized empty Git repository' in result
    assert not error
    assert code == 0
    
    result, error, code = run_git_command(f'remote remove origin')
    assert not result
    assert not error
    assert code == 0
    
    response = create_github_repo(repo_name, 'Katsarski', os.getenv("GH_ACCESS_TOKEN"))
    
    result, error, code = run_git_command(f'remote add origin https://github.com/Katsarski/{repo_name}.git')
    assert not result
    assert not error
    assert code == 0
    
    result, error, code = run_git_command(f'add .')
    assert not result
    assert not error
    assert code == 0
    
    result, error, code = run_git_command(f'commit -m "initial commit"')
    assert 'initial commit' in result
    assert not error
    assert code == 0
    
    result, error, code = run_git_command(f'push -u origin main')
    assert not result
    assert not error
    assert code == 0
    
    result, error, code = run_git_command(f'remote -v')
    assert result.count(repo_name) == 2
    assert not error
    assert code == 0

    delete = delete_github_repo(repo_name, 'Katsarski', os.getenv("GH_ACCESS_TOKEN"))
    assert repo_name in response
    print("HDSHA")
    