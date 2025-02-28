# Northern Tech Git Task

This repository contains a series of automated tests for various Git commands using Python and Pytest. 

The tests are able to run on multiple platforms (Windows, Linux, and macOS) using GitHub Actions.

The code is automatically checked when a PR is opened using linter pylint (not blocking)

**Further planned implementations (as required in the task) are listed later in the README.md**

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
- `git branch`
- `git clone`
- `git status`
- `git stash`
- `git restore`

## Potential issues found

The following issue was observed when creating the tests:
- Running the below tests (specifically the `git status` command) on macOS caused the stdout stream to output message that is not the same as on Windows and Linux platforms causing the assertion to fail. Further I've checked the installed git version on each runner which is the same i.e. 2.48.1. I would recommend aligning the output to avoid confusion and keep consistency between the different OSs. The errors and differences can be checked in one of the CI/CD test runs on macOS e.g. https://github.com/Katsarski/northern_tech_git_task/actions/runs/13562642040/job/37909273632: 
  - tests/test_git_restore.py::test_git_restore_staged_changes
  - tests/test_git_status.py::test_git_status_no_changes
  - tests/test_git_status.py::test_git_status_with_changed_file
  - tests/test_git_status.py::test_git_status_with_tracked_file

## Solution Improvements

The following improvements can be made to enhance the project::

1. **Additional Test Cases**:
   - Add more test cases to cover edge cases and additional Git commands (e.g., `git merge`, `git rebase`, `git pull` and more).

2. **Continuous Integration**:
   - Fix parallel runs - currently fails due to issues related to the various threads trying to use the .git files concurently
   - Improve workflow by merging common configuration steps for the various OSs to avoid duplication
   - Rate limit the requests against GitHub to avoid depleting the dedicated quota
   - Introduce docker containers with pre-build images containing the base image and dependencies to speed up the execution

## Running the Tests

To run the tests locally, follow these steps:

1. Clone the repository:
   ```sh
   Run `git clone https://github.com/Katsarski/northern_tech_git_task.git`
   Run `cd northern_tech_git_task`

2. Create a virtual environment and install dependencies:

    # Linux/MacOS
    - python3.# (tested and developed on 3.13) installed
    - run `apt install python3.13-venv` if not already there
    - run `python3 -m venv .venv`
    - run `source .venv/bin/activate`
    - run `pip install -r requirements.txt`

    # Windows
    - python3.# (tested and developed on 3.13) installed
    - run `python -m venv .venv`
    - run `.venv\Scripts\activate`  # On PowerShell or Command Prompt
    - run `pip install -r requirements.txt`
    - Optional (might be required): run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`

3. Introduce the following (example) environment variables
   - GH_EMAIL: boyankatsarski@gmail.com <-- change to your account
   - GH_TOKEN: PAT OR regular GitHub access token with CRUD operations for the given account
   - GH_USERNAME: Katsarski <-- change to your username

4. Run: `pytest`

## QA Homework Task references and thoughts

- Given the broad scope of the task ("...test the Git software.") I've decided to implement some tests for the Git CLI. There are various other related services that need to be tested for throughout coverage like the gh CLI, the API client, the Desktop client, and the integrations that the Git offers/is integrated into. Given the context of the Git software and that is used by technical people the Git CLI is the most important component that covers the product core features so that is my argument for covering it and not the rest of the components listed. Some actions are not accessible purely by invoking the CLI e.g. create remote repo so I had to invoke the API also to cover my scenarios. 

- There are core commands I haven't yet covered, however the approach would be more or less similar to what I've done so far hence I've decided to stop at this point. 

- Obviously there are quite a lot more scenarios that I haven't covered that potentially affect all the commands that I've covered and the ones I haven't, I'll list some examples here. This list is my proposal for the further steps to be automated (not listed by priority since determining the priority requires lots of assumptions I don't think would be grounded on solid information without taking into account some business-related aspects at the time of implementation in a real-world scenario).

- I realized that listing all of my ideas and permutations is going to be a bit too much so I've decided squeeze the ideas in the form of a list that briefly touches upon some important (IMO) aspects which can be used as guidance  for the next phases of test creation. 

  - **Proposal for more positive tests**  
    - Test mmore core commands e.g. git merge, git fetch, git revert, git tag, git diff, git rm
    - Test the core flags of the core commands e.g. init (--quiet, --template), clone (--branch), add (--all), commit (--squash, --amend), checkout (--force) etc.
    - Test fof concistency in terms of behavior and messages returned between the commands
    - Test the submodules features e.g. cloning, adding, updating, and removing submodules
    - Test git hooks e.g. pre-commit, post-commit, pre-push, etc.
    - Test the performance aspects
      - Test with repos with many small files (small file size but high count)
      - Test with repos with large files (few large files with large size)
      - Test with repos with a large history (many commits, branches, and tags)
      - Test withh repos with a mix of large files and small files
      - Tests should be around bandwidth consumption and response times
      - Test performance on a slow network
      - Test performance on a PC with limited resources
    - Test the security aspects
      - Test that the communication between the client and servert happens using a secure protocol e.g. SSH, HTTPS
      - SSH Key Management (use, storage, removal)
      - HTTPS authentication
      - Authentication mechanism in case of 2FA
      - Personal Access Tokens (use, scope (read/write))
      - .gitignore - in the context of excluding senstiive files
      - Repo access controls in general - read/write operations, privileges, private/public repo concept
      - Git user configuration (user.name, user.email) not exposed in any way 
      - Integrate static/dynamic application security testing solutions into the CI/CD pipeline

  - **Proposal for more negative tests**  
    - Test the currently covered and the ones that are not in a negative context
      - Test for invalid invocation of the core command and assert helpful error displayed
      - Test for invalid flags and assert usage error displayed
    - Test the performance aspects
      - Failover mechanisms
      - Disaster recovery mechanism
      - Stress testing
    - Test the security aspects
      - Try to use tampered token
      - Brute-forcing the access token
      - Accessing a private repo (check for responces indicating that e.g. the repo exists but is not accessible i.e. 404 vs 401)
      - Using the repo with expired/removed SSH/Access token

  - **Describe what the second phase of the test implementation would be**  
    - In my opinion the next phase would be to cover the above listed scenarios (and more oriented around the different functional/non-functional aspects) and then move to the other Git components (API/UI), this will help build the rest on a solid working solution helping reliably extend the ways users can interact with Git. 

- **Describe the requirements of the system that would run these tests in a continuous integration manner.**  
    - Github actions is working for me at this point. Any other CI/CD tool should be able to run tests against git having the dependencies installed - being a self-hosted solution or with cloud-based runners. The tests shall be running on multiple OSs to confirm cross OS support. Tests should be running in parallel to speed up execution and shall ideally run on a regular-basis e.g. on each MR created against the main branch