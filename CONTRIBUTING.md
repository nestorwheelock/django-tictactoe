# Contributing to Django Tic-Tac-Toe

Thank you for your interest in contributing to django-tictactoe! This document provides guidelines and instructions for contributing to the project.

## Welcome

We appreciate your contributions, whether they're bug reports, feature requests, documentation improvements, or code changes. Every contribution helps make this package better for everyone.

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub first, then:
git clone https://github.com/YOUR_USERNAME/django-tictactoe.git
cd django-tictactoe
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements-dev.txt
pip install -e .
```

### 4. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

## Code Standards

### Python Code Style

- **Follow PEP 8**: Use [PEP 8](https://pep8.org/) style guidelines
- **Use Black**: Format all code with black (line length: 88)
- **Use Flake8**: Check code quality with flake8
- **Type Hints**: Add type hints to all function signatures
- **Docstrings**: Write docstrings for all classes and public methods

```python
def make_move(self, position: int) -> dict:
    """
    Make a move in the game.

    Args:
        position: Board position (0-8)

    Returns:
        dict with success status and message

    Raises:
        ValidationError: If move is invalid
    """
    # implementation
```

### Code Quality Commands

```bash
# Format code
black tictactoe/ tests/

# Check style
flake8 tictactoe/

# Type checking (optional, if mypy configured)
mypy tictactoe/
```

## Testing Requirements

### Write Tests for All Changes

- **New features**: Must include comprehensive tests
- **Bug fixes**: Must include regression tests
- **Coverage**: Must maintain >95% test coverage
- **Test types**: Include unit, integration, and edge case tests

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=tictactoe --cov-report=html --cov-report=term-missing

# Run specific test file
pytest tictactoe/tests/test_models.py -v

# Run specific test class
pytest tictactoe/tests/test_api.py::TestGameAPI -v

# Run specific test method
pytest tictactoe/tests/test_api.py::TestGameAPI::test_create_game -v
```

### Test Structure

```python
import pytest
from tictactoe.models import Game

@pytest.mark.django_db
class TestYourFeature:
    """Test suite for your feature."""

    def test_feature_happy_path(self):
        """Test the main success scenario."""
        # Arrange
        game = Game.objects.create()

        # Act
        result = game.some_method()

        # Assert
        assert result is True

    def test_feature_edge_case(self):
        """Test edge cases and error handling."""
        # Test implementation
```

## Pull Request Process

### Before Submitting

1. **Update Documentation**: Update README.md if adding features
2. **Add Tests**: Ensure all tests pass and coverage is maintained
3. **Update CHANGELOG**: Add entry to CHANGELOG.md under [Unreleased]
4. **Format Code**: Run black and flake8
5. **Run Full Test Suite**: `pytest --cov=tictactoe`

### Commit Messages

Follow conventional commits format:

```
type(scope): brief description

Longer explanation if needed.

Closes #issue_number
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Test additions or changes
- `refactor`: Code refactoring
- `style`: Code style changes (formatting, etc.)
- `chore`: Maintenance tasks

**Examples:**
```
feat(api): add endpoint for game statistics

Implemented new /api/stats/ endpoint that returns
aggregate game statistics.

Closes #42
```

```
fix(models): correct win detection for diagonal

Fixed bug where diagonal wins weren't detected when
position 4 was the last move.

Closes #58
```

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] All tests pass
- [ ] Added tests for new features
- [ ] Coverage maintained/improved

## Checklist
- [ ] Code follows project style
- [ ] Self-reviewed code
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] No new warnings generated
```

### Review Process

1. Submit pull request to `master` branch
2. Automated tests will run
3. Maintainers will review your code
4. Address review comments if any
5. Once approved, maintainer will merge

## Reporting Issues

### Bug Reports

Use this template for bug reports:

```markdown
## Bug Description
Clear description of the bug

## To Reproduce
Steps to reproduce:
1. Go to...
2. Click on...
3. See error

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- Python version:
- Django version:
- DRF version:
- OS:

## Additional Context
Screenshots, error messages, etc.
```

### Feature Requests

Use this template for feature requests:

```markdown
## Feature Description
Clear description of the feature

## Use Case
Why is this feature needed?

## Proposed Solution
How would you implement this?

## Alternatives Considered
Other approaches you've thought about

## Additional Context
Mockups, examples, etc.
```

## Code Review Guidelines

When reviewing pull requests, consider:

- **Functionality**: Does the code work as intended?
- **Tests**: Are there adequate tests?
- **Style**: Does it follow project conventions?
- **Documentation**: Is it well-documented?
- **Performance**: Are there any performance concerns?
- **Security**: Are there any security issues?

## Development Workflow

### Typical Development Cycle

1. **Pick an issue** or create one for discussion
2. **Fork and clone** the repository
3. **Create branch** from master
4. **Write failing tests** (TDD approach)
5. **Implement feature** to make tests pass
6. **Run full test suite**
7. **Update documentation**
8. **Update CHANGELOG.md**
9. **Format code** with black
10. **Submit pull request**
11. **Address review comments**
12. **Get merged!**

### Testing Strategy

Follow Test-Driven Development (TDD):

1. **Red**: Write a failing test
2. **Green**: Write minimal code to pass
3. **Refactor**: Improve code while keeping tests green

## Project Structure

```
django-tictactoe/
├── tictactoe/              # Main package
│   ├── models.py           # Game model
│   ├── serializers.py      # DRF serializers
│   ├── views.py            # API and template views
│   ├── urls.py             # URL routing
│   ├── admin.py            # Admin configuration
│   ├── templates/          # HTML templates
│   ├── static/             # CSS and JavaScript
│   └── tests/              # Test suite
├── tests/                  # Test configuration
├── planning/               # Project planning docs
├── setup.py                # Package configuration
├── requirements.txt        # Production dependencies
├── requirements-dev.txt    # Development dependencies
├── pytest.ini              # Pytest configuration
├── README.md               # Main documentation
├── CONTRIBUTING.md         # This file
├── CHANGELOG.md            # Version history
└── LICENSE                 # MIT License
```

## Questions or Need Help?

- **GitHub Issues**: https://github.com/nestorwheelock/django-tictactoe/issues
- **Discussions**: Use GitHub Discussions for questions
- **Email**: Contact maintainer if needed

## Recognition

Contributors will be:
- Listed in the project contributors
- Credited in release notes
- Appreciated in the community!

Thank you for contributing to django-tictactoe! 🎉
