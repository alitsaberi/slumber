# Contributing to the Project
This document outlines the process for contributing to the project, including our development and testing guidelines.

## Table of Contents

1. [Git flow](#git-flow)
2. [Development](#development)
3. [Testing](#testing)

## Git flow

This project uses Git Flow for version control. The main branches are:

- **develop**: Ongoing development.
- **feature/\<feature-name\>**: Branches for new features.
- **bugfix/\<issue-description\>**: Branches for bug fixes.

## Development

* **Setting Up**  
    * Ensure to install test dependencies:
    ```bash
    poetry install --with dev
    ```

    * Install pre-commit hooks:
    ```bash
    poetry run pre-commit install
    ```

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
    * Create a Pull Request (PR) from the feature branch to `develop` for review.  
    * After approval, merge the PR into `develop`.

### Tips

* Use descriptive commit messages.  
* Frequently pull changes from the develop branch into your feature branches to minimize merge conflicts.  

#### Pull Requests

* Ensure the PR title and description are clear and descriptive.  
* Assign the PR to the appropriate reviewer.  
* The reviewer should review the PR and provide feedback. After the review, the reviewer should approve the PR or request changes.  
* Address any feedback or comments in the PR.  
  * If changes are required, make the necessary updates in the branch. For each review, commit the changes and push them to the branch with message like: "Review \<review-number\>“  
* When merging an PR, squash the commits into a single commit with a meaningful message.

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
