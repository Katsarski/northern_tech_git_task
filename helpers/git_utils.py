"""
This module provides functions to interact with the git API, specifically for creating 
and deleting git repositories
"""

import logging
import os
import urllib
import requests
import config


def api_create_github_repo(repo_name: str) -> requests.Response:
    """
    Creates a git repo using the git API and returns the response with the repo details

    Parameters:
    - repo_name: The name of the repo to be created.

    Returns:
    - requests.Response: The response object containing details of the created git repo

    Raises:
    - Exception: If the repo creation fails, an exception is raised with the error 
      message from Github

    Notes:
    - The function requires a valid git access token to be set in the environment 
      variable anmed as 'GH_TOKEN'
    - The repo is created as a private one by default
    """
    
    logging.info(f"Creating repo with name: {repo_name}")
    
    url = f"{config.GH_API_URL}/user/repos"
    headers = {
        "Authorization": f"Bearer {config.GH_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    data = {"name": repo_name, "private": True}
    response = requests.post(url, json=data, headers=headers, timeout=30)
    
    if response.status_code != 201:
        raise requests.exceptions.HTTPError(f"Repo creation failed: {response.text}")
        
    logging.info(f"Successfully created repo with name: {repo_name}")
    return response


def api_delete_github_repo(repo_name: str) -> requests.Response:
    """
    Deletes a repo using the github API

    Parameters:
    - repo_name: The name of the repo to be deleted

    Returns:
    - requests.Response: The response object confirming the deletion

    Raises:
    - Exception: If the repo deletion fails, an exception is raised with the error 
      message from Github
    """
    
    logging.info(f"Deleting git repo with name: {repo_name}")
    
    # URL encode the repo name to handle special characters in the name.
    repo_name_encoded = urllib.parse.quote(repo_name)
    url = f"{config.GH_API_URL}/repos/{os.getenv('GH_USERNAME')}/{repo_name_encoded}"
    
    headers = {
        "Authorization": f"Bearer {config.GH_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    
    response = requests.delete(url, headers=headers, timeout=30)
    
    if response.status_code != 204:
        raise requests.exceptions.HTTPError(f"Repo deletion failed: {response.text}")
    
    logging.info(f"Successfully deleted repo with name: {repo_name}")
    return response
