# Contributing to the Project
This document outlines the process for contributing to the project, including our Git Flow and testing guidelines.

## Table of Contents

1. [Setup](#setup) 
2. [Git Flow](#git-flow)
3. [Testing](#testing)

## Setup
### Requirements
- Python 3.10
### Installation
1. Create a virtual environment and activate it
```
python -m venv $VENV_PATH
source $VENV_PATH/bin/activate
```
2. Install [Poetry](https://python-poetry.org/docs/#installing-manually)
```
pip install -U pip setuptools
pip install poetry
```
3. Install dependencies
```
poetry install
```
4. Install pre-commit hooks
```
pre-commit install
```

## Git Flow

This project uses Git Flow for version control. The main branches are:

- **main**: Stable, production-ready code.
- **develop**: Ongoing development.
- **feature/<feature-name>**: Branches for new features.
- **bugfix/<issue-description>**: Branches for bug fixes.

### Development

* **Creating a feature branch**  
    * Start by pulling the latest changes from the `develop` branch.
    ```
    git checkout develop
    git pull --rebase origin develop
    ```
    * Create a new feature/bugfix branch:
    ```
    git checkout -b feature/<feature-name>
    ```

* **Developing the feature**  
    * Implement the new feature or fix in your branch.  
    * Commit changes with meaningful messages.  
        * Example commit message: "Add logging for better debugging"

* **Merging the feature branch into `develop`**  
    * Push the feature branch to the remote repository.
    ```
    git push origin feature/<feature-name>
    ```
    * Create a Merge Request (MR) from the feature branch to `develop` in GitLab for review.  
    * After approval, merge the MR into `develop`.

### Tips

* Use descriptive commit messages.  
* Frequently pull changes from the develop branch into your feature branches to minimize merge conflicts.  

#### Merge Requests

* Ensure the MR title and description are clear and descriptive.  
* Ensure the CI/CD pipeline passes successfully.  
* Assign the MR to the appropriate reviewer.  
* The reviewer should review the MR and provide feedback. After the review, the reviewer should approve the MR or request changes.  
* Address any feedback or comments in the MR.  
  * If changes are required, make the necessary updates in the feature branch. For each review, commit the changes and push them to the feature branch with message like: "Review \<review-number\>“  
* When merging an MR, squash the commits into a single commit with a meaningful message.

## Testing

Testing is a crucial part of the development process. This project uses `pytest` for writing and running tests. Below are the guidelines for writing tests:

* **Setting Up**  
    * Ensure to install test dependencies:
    ```bash
    poetry install --with test
    ```

* **Writing Tests**  
    * **Organizing Test Files**  
        * Place your test files in the `tests` directory. Name them `test_<module>.py` and organize them in sub-directories if necessary.
        * Each test directory, file, and function should start with `test_`.

    * **Writing Effective Tests**  
        * Write tests that cover various scenarios, including edge cases and corner cases.
        * Ensure your tests are isolated and do not depend on each other.
        * Use fixtures to set up any necessary state before tests run.
        * Use AI tools like GitHub Copilot to assist in writing tests.

    * **Example Test Function**  
        ```python
        def test_example_function():
            assert example_function() == expected_result
        ```

* **Running Tests**  
    * Run all tests using the following command:
    ```bash
    pytest
    ```
