# Project Summary

The Child Care Management System is an Odoo 17-based solution designed to automate and streamline operations in a childcare facility. It covers child enrollment, contracts, medical records, classroom management, billing, payroll, and inventory control. The system ensures compliance with business rules such as automatic contract expiration, late fee calculations, and medical supply deductions.

## Project Base Structure

```plaintext
/childcare_management/
├── /controllers/               # Contains controllers (HTTP routes)
├── /data/                      # Demo and data xml
├── /demo/                      # Loaded in demostration mode
├── /models/                    # Models definition
├── /security/                  # System security groups and access rules
├── /static/                    # Contains the web assets, separated into css/js/, img/
├── /views/                     # Contains the views and templates
├── __manifest__.py             # Odoo module metadata
├── __init__.py                 # Module initialization
/README.md                      # Documentation
```

## Contribution Guidelines

To ensure consistency and maintainability, follow Odoo 17's official development guidelines:
 <https://www.odoo.com/documentation/17.0/es/contributing/development/coding_guidelines.html>

## Best Practices for Collaboration

1. Branch Naming: Use **feature/**, **fix/**, or **refactor/** prefixes (e.g., **feature/contract-renewal**).
2. Code Reviews: Submit pull requests for review before merging.
3. Documentation: Comment your code and update relevant documentation.
4. Modularization: Each feature should be in its own module for maintainability.
5. Avoid Core Modifications: Always use inheritance instead of modifying core models.

## Conventional Commits

For this project, we will use the **Conventional Commits** standard. The following are the prefixes and formats to follow when committing to the repository.

- link: <https://www.conventionalcommits.org/en/v1.0.0/>

### General Format

Each commit must follow this format:

<type>(<area>): <short description>.

#### Format Description

- **`<type>`**: Type of change you are making.

- **`<<area>`**: Area of code affected, such as a specific file or component.

- **`<<brief description>`**: A brief description of what the commit does.

  - Use an imperative tone and lowercase (e.g., “adds”, “fixes”).

  - The description should be a maximum of 50 characters.

### Types of Commits

The following are the types of commits you can use:

#### 1. `feat`: New Features

Use when you add a new feature or functionality to the project.

- feat(<component>): adds support for JWT authentication.

#### 2. `fix`: Bug Fixes

For fixing bugs and errors.

- fix(<module>): fixes error in totals calculation.

#### 3. `docs`: Documentation

When updating or modifying project documentation (README, comments, etc.).

- docs(<file>): update installation documentation in README

#### 4. `style`: Styles and Formatting

Changes that do not affect the logic of the code, such as corrections to style, formatting, spaces, commas, etc.

- style(<file>): adjusts identation and removes extra spaces.

#### 5. `refactor`: Refactoring

Code changes that do not fix a bug or add functionality, such as code structure improvements or cleanup.

- refactor(<component>): optimizes render function

#### 6. `test`: Testing

Exclusive use for creating or modifying tests.

- test(<service>): add unit tests for login function

#### 7. `chore`: General Tasks

For minor tasks or tasks that do not affect the code logic (dependencies update, configuration, etc.).

- chore(<dependencies>): upgrade eslint version to 8.0.0

#### 8. `perf`: Performance Improvements

Optimization of the application in terms of performance.

- perf(<component>): improved data table rendering efficiency.

#### 9. `ci`: Continuous Integration

Changes to CI configuration files and scripts (e.g., GitHub Actions, CircleCI).

- ci(<pipeline>): add deployment script for production environment.

