"""
This module provides pytest fixtures for setting up and testing git repo creation and 
configuration. It includes fixtures to generate repo names and manage paths accross 
test executionss
"""

import os
import logging
import pytest
import config
from helpers import common, git_utils

@pytest.fixture
def get_repo_name() -> str:
    """
    Fixture to generate a unique repository name.

    Returns:
        - A randomly generated repository name.
    """
    return common.generate_repo_name()


@pytest.fixture
def get_repo_path(get_repo_name: str) -> str:
    """
    Fixture to generate the full repository path based on the repo name

    Parameters:
        - get_repo_name: The name of the repository to be used.

    Returns:
        - The full path to the repo directory.
    """
    root_dir = os.path.abspath(os.path.dirname(__file__))
    
    # Adjust for GitHub Actions runner path if the environment variable exists
    if 'GITHUB_WORKSPACE' in os.environ:
        root_dir = os.environ['GITHUB_WORKSPACE']
    
    return os.path.join(root_dir, 'test_repos', get_repo_name)


@pytest.fixture
def api_create_git_repo(get_repo_name: str, get_repo_path: str, request):
    """
    Fixture to create a git repository using the GitHub API, set up local git configuration, 
    and add a remote repository.

    Parameters:
        - get_repo_name: The name of the repository to be created.
        - get_repo_path: The local file system path to the repository.
        - remote_only: If True, only the remote repository is created (no local).

    Yields:
        - The name of the created repository for further testing.

    Cleanup:
        - Deletes the created GitHub repository after the test.
    """
    remote_only = request.node.callspec.params["remote_only"] if hasattr(request.node, "callspec") else False
    
    # Set global default branch to 'main'
    result = common.run_shell_command(f'git config --global init.defaultBranch {config.DEFAULT_BRANCH}')
    assert not result.stdout, "Error with git config for default branch."
    assert not result.stderr, f"Unexpected error: {result.stderr}"
    
    if not remote_only:
        os.makedirs(get_repo_path, exist_ok=True)
        # Initialize loclaly the git repository
        result = common.run_shell_command(f'git init {get_repo_path}')
        assert 'Initialized empty Git repository' in result.stdout, "Git init failed."
        os.chdir(get_repo_path)  # Change directory to the new repo path
    
    # Create the git repo using the API
    response = git_utils.api_create_github_repo(get_repo_name)
    assert f'{config.GH_URL}/{config.GH_USERNAME}/{get_repo_name}.git' in response.text, (
    "GitHub repo creation failed.")

    if not remote_only:
        # Add the remote repository
        result = common.run_shell_command(
            f'git remote add origin {config.GH_URL}/'
            f'{os.getenv("GH_USERNAME")}/{get_repo_name}.git'
        )
        assert not result.stdout, "Error adding remote origin."
    
    yield get_repo_name  # Yield the repository name to the test
    
    # Delete the git repo after the test is finished
    delete = git_utils.api_delete_github_repo(get_repo_name)
    assert delete.status_code == 204, (
        f"Failed to delete GitHub repo. Status code: {delete.status_code}")


@pytest.fixture(autouse=True)
def restore_cwd():
    """
    Fixture to save and restore the current working dir after each test
    """
    original_cwd = os.getcwd()
    yield
    os.chdir(original_cwd)  # Reset back to the original working directory


def pytest_configure(config: pytest.Config):
    """
    Configures basic logging for pytest to capture detailed logs during testing

    Parameters:
        - config: The pytest configuration object.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()]
    )
    logging.getLogger().setLevel(logging.INFO)
    config.option.log_cli = True
    config.option.log_cli_level = "INFO"
