import subprocess
import requests
import random
import string
import os

import urllib

def run_git_command(command):
    """Run a git command and return the output."""
    result = subprocess.run(f'git {command}', capture_output=True, text=True)
    return result.stdout, result.stderr, result.returncode

def create_github_repo(repo_name, username, github_token):
    """Create a github repo using the github API and return the output"""
    url = f"https://api.github.com/user/repos"
    headers = {"Authorization": f"Bearer {github_token}", "Accept": "application/vnd.github+json"}
    data = {"name": repo_name, "private": True}
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()["clone_url"]

def delete_github_repo(repo_name, username, github_token):
    """Delete a github repo using the github API and return the output"""
    repo_name_encoded = urllib.parse.quote(repo_name)
    url = f"https://api.github.com/repos/{username}/{repo_name_encoded}"
    headers = {"Authorization": f"Bearer {github_token}", "Accept": "application/vnd.github+json"}
    response = requests.delete(url, headers=headers)
    response.raise_for_status()
    return response

def generate_repo_name(name_length=15):
    """Generate a pseudo random github repo name using the allowed characters by github and return the name"""
    allowed_special_chars = '-_.'
    repo_name = random.choice(string.ascii_letters) + random.choice(string.digits) + allowed_special_chars
    repo_name += ''.join(random.choices(string.ascii_letters + string.digits, k=name_length-len(repo_name)))
    return repo_name