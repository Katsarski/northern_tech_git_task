import logging
import requests
import os
import urllib

GITHUB_API_URL = "https://api.github.com"
GITHUB_ACCESS_TOKEN = os.getenv("GH_TOKEN")        

def api_create_github_repo(repo_name):
    """
    Creates a github repository using the github API and returns the created repo url

    Parameters:
    - repo_name (str): The name of the repository to be created.

    Returns:
    - str: The URL of the newly created github repo.

    Raises:
    - Exception: If the repository creation fails, an exception is raised with the error message from guithub.

    Notes:
    - The function requires a valid github access token to be set in the environment variable 'GH_TOKEN'.
    - The repository is created as a private repository by default.
    """
    
    logging.info(f"Creating github repo with name: {repo_name}")
    
    url = f"{GITHUB_API_URL}/user/repos"
    headers = {"Authorization": f"Bearer {GITHUB_ACCESS_TOKEN}", "Accept": "application/vnd.github+json"}
    data = {"name": repo_name, "private": True}
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code != 201:
        raise Exception(f"GitHub Repo creation failed: {response.text}")
        
    logging.info(f"Successfully created github repo with name: {repo_name}")
    return response.json()["clone_url"]

def api_delete_github_repo(repo_name, username):
    """
    Deletes a GitHub repository using the github API.

    Parameters:
    - repo_name (str): The name of the repository to be deleted.

    Returns:
    - None

    Raises:
    - Exception: If the repository deletion fails, an exception is raised with the error message from github.

    Notes:
    - The function requires a valid github access token to be set in the environment variable 'GH_TOKEN'.
    - The repository must exist and the authenticated user must have the necessary permissions to delete it (correct token scope).
    """
    
    logging.info(f"Deleting github repo with name: {repo_name}")
    
    repo_name_encoded = urllib.parse.quote(repo_name)
    url = f"{GITHUB_API_URL}/repos/{username}/{repo_name_encoded}"
    headers = {"Authorization": f"Bearer {GITHUB_ACCESS_TOKEN}", "Accept": "application/vnd.github+json"}
    
    response = requests.delete(url, headers=headers)
    
    if response.status_code != 204:
        raise Exception(f"GitHub Repo deletion failed: {response.text}")
    
    logging.info(f"Successfully deleted github repo with name: {repo_name}")
    return response
