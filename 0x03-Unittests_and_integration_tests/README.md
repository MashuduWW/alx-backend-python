# GithubOrgClient Test Suite

This project contains unit and integration tests for the `GithubOrgClient` class, which interacts with the GitHub public API.

## Structure

The tests are organized into multiple test classes:

### Unit Tests (`test_client.py`)
These tests mock external dependencies and test logic in isolation:

- `TestGithubOrgClient.test_org`: Tests the `.org` property using mocked `get_json`.
- `TestGithubOrgClient.test_public_repos_url`: Tests the `_public_repos_url` property using a mocked `.org` property.
- `TestGithubOrgClient.test_public_repos`: Tests the `public_repos()` method using mocked `_public_repos_url` and `get_json`.
- `TestGithubOrgClient.test_has_license`: Tests the `has_license()` static method using parameterized inputs.

### Integration Tests (`test_client_integration.py`)
These tests mock only HTTP calls (`requests.get`) to simulate realistic interactions:

- `TestIntegrationGithubOrgClient.test_public_repos`: Tests fetching repository names from the GitHub API.
- `TestIntegrationGithubOrgClient.test_public_repos_with_license`: Tests filtering repositories by license (e.g., `apache-2.0`).

Fixtures for these tests are provided in `fixtures.py`.

## Running the Tests

To run all tests:


python -m unittest discover

or to run a single test:

python -m unittest test_client.py


## Dependencies

unittest (Python standard library)

parameterized

unittest.mock


