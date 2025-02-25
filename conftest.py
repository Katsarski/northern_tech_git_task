import os
import pytest
from helpers import common, git_utils
import logging

GITHUB_URL = "https://github.com"

@pytest.fixture
def get_repo_name():
    "Fixture to generate a unique repo name."
    return common.generate_repo_name()


@pytest.fixture
def get_repo_path(get_repo_name):
    "Fixture to generate the full repo path"
    root_dir = os.path.abspath(os.path.dirname(__file__))
    # Adjust for GitHub Actions runner path
    if 'GITHUB_WORKSPACE' in os.environ:
        root_dir = os.path.join(os.environ['GITHUB_WORKSPACE'], 'northern_tech_git_task')
    return os.path.join(root_dir, 'test_repos', get_repo_name)

@pytest.fixture
def api_create_git_repo(get_repo_name, get_repo_path):
    "Fixture to create a git repo using the github API"
    result = common.run_shell_command(f'git init {get_repo_path}')
    assert 'Initialized empty Git repository' in result.stdout, "Git init failed."
    
    os.chdir(get_repo_path)
    
    response = git_utils.api_create_github_repo(get_repo_name)
    assert f'{GITHUB_URL}/{os.getenv("GH_USERNAME")}/{get_repo_name}.git' in response, "GitHub repo creation failed."
    
    result = common.run_shell_command(f'git remote add origin {GITHUB_URL}/{os.getenv("GH_USERNAME")}/{get_repo_name}.git')
    assert not result.stdout
    
    yield get_repo_name
    
    delete = git_utils.api_delete_github_repo(get_repo_name, os.getenv("GH_USERNAME"))
    assert delete.status_code == 204, "Failed to delete GitHub repo."

@pytest.fixture(autouse=True)
def restore_cwd():
    "Saves and restores the current working directory after each test"
    root_dir = os.path.abspath(os.path.dirname(__file__))
    # Adjust for GitHub Actions runner path
    if 'GITHUB_WORKSPACE' in os.environ:
        root_dir = os.path.join(os.environ['GITHUB_WORKSPACE'], 'northern_tech_git_task')
    yield
    os.chdir(root_dir)  # Reset back to the root dir of the project
    
def pytest_configure(config):
    "Configure some basic logging for pytest"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()]
    )
    logging.getLogger().setLevel(logging.INFO)
    config.option.log_cli = True
    config.option.log_cli_level = "INFO"