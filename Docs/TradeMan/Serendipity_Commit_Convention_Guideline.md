
# Serendipity Tech Department Commit Convention Guideline

This document outlines the commit message conventions for the Serendipity tech department. These conventions help ensure consistency, clarity, and automation compatibility when generating commit messages using an LLM based on git diffs.

## Commit Message Structure

Each commit message should be structured as follows:

```
<type>(<scope>): <short description>

[optional body]

[optional footer]
```

### 1. **Type**

The type indicates the category of the change. Choose one of the following:

- **feat**: A new feature or enhancement.
- **fix**: A bug fix or correction.
- **docs**: Changes related to documentation only.
- **style**: Code formatting changes (e.g., indentation, whitespace) without affecting functionality.
- **refactor**: Code changes that neither fix a bug nor add a feature (e.g., code structure improvement).
- **perf**: Changes that improve performance.
- **test**: Adding or modifying tests.
- **build**: Changes that affect the build system or dependencies.
- **ci**: Changes to CI/CD configuration files and scripts.
- **chore**: Routine tasks like maintenance, updates, or non-code changes.
- **revert**: Reverting a previous commit.

### 2. **Scope**

The scope is optional but recommended. It provides context about the part of the codebase affected. Examples:

- **auth**: For changes related to authentication mechanisms.
- **api**: For changes in the API layer.
- **ui**: For frontend/UI changes.
- **db**: For database-related changes.
- **docs**: For documentation updates.
- **deps**: For changes in dependencies.

### 3. **Description**

The short description should summarize the changes clearly and concisely (preferably within 50 characters). Use imperative mood, e.g., "add", "fix", "update", etc.

### 4. **Body (Optional)**

Provide a detailed explanation of the change if necessary. Include:

- **Motivation**: Why was this change necessary?
- **Implementation**: How was the issue resolved or the feature implemented?

### 5. **Footer (Optional)**

Use the footer to reference issues, breaking changes, or other important details:

- **Breaking changes**: Begin with `BREAKING CHANGE:` followed by a detailed description.
- **Issue reference**: Use `Closes #issue-number` to reference related issues.

## Examples

### Example 1
```
feat(auth): add OAuth2 support for user authentication

Implemented OAuth2 integration to enhance user login security.
```

### Example 2
```
fix(ui): correct button alignment on mobile view

Adjusted CSS styles to ensure buttons align correctly on small screens.
```

### Example 3
```
chore(deps): update Node.js version to 16.x

This update is needed for compatibility with the new build pipeline.
```

### Example 4
```
refactor(api): reorganize controller methods for clarity

Grouped similar methods and optimized routing logic for better readability.
```

## Using an LLM to Generate Commit Messages

When using an LLM to automate commit messages based on `git diff`, the model should:

1. **Identify the Type**: Analyze the diff to determine the type of change (e.g., `feat`, `fix`).
2. **Determine the Scope**: Infer the relevant scope (e.g., `ui`, `api`) based on the file paths and code context.
3. **Summarize Changes**: Generate a concise, imperative summary of the changes based on the diff content.
4. **Optionally Add Detail**: If the changes are complex, include a detailed body or footer as needed.
```

This guideline ensures that all commit messages are consistent, informative, and machine-readable, facilitating automation, versioning, and communication within the team.
