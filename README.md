# Northern Tech Git Task

This repository contains a series of automated tests for various Git commands using Python and Pytest. 

The tests are able to run on multiple platforms (Windows, Linux, and macOS) using GitHub Actions.

The code is automatically checked when a PR is opened using linter pylint (not blocking)

## Project Structure

- `.github/workflows/tests.yml`: GitHub Actions workflow configuration for running tests on different platforms
- `.github/workflows/linter.yml`: Pylint actions workflow configuration to check code quality
- `conftest.py`: Pytest configuration and fixtures for setting up and tearing down test execution
- `helpers/`: Helper modules for common functions and github API interactions
- `tests/`: Directory containing test cases for various Git commands
- `requirements.txt`: List of dependencies required for running the tests

## Tests

The tests cover the following Git commands:

- `git add`
- `git commit`
- `git init`
- `git push`
- `git remote add`

## Improvements

The following improvements can be made to enhance the project::

1. **Additional Test Cases**:
   - Add more test cases to cover edge cases and additional Git commands (e.g., `git merge`, `git rebase`, `git pull` and more).

2. **Continuous Integration**:
   - Fix parallel runs - currently fails due to issues related to the various threads trying to use the .git files concurently

## Running the Tests

To run the tests locally, follow these steps:

1. Clone the repository:
   ```sh
   git clone https://github.com/Katsarski/northern_tech_git_task.git
   cd northern_tech_git_task

2. Create a virtual environment and install dependencies:

    # Linux/MacOS
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

    # Windows
    python -m venv .venv
    .venv\Scripts\activate  # On PowerShell or Command Prompt
    pip install -r requirements.txt
    Optional (might be required): Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

3. Run: pytest