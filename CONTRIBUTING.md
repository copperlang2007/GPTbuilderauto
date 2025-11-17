# Contributing to GPTbuilderauto

Thank you for your interest in contributing to GPTbuilderauto!

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/copperlang2007/GPTbuilderauto.git
cd GPTbuilderauto
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -r requirements.txt
pip install -e .
```

4. Set up pre-commit hooks:
```bash
# Install pre-commit
pip install pre-commit
pre-commit install
```

## Running Tests

Run all tests:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=gptbuilderauto --cov-report=html
```

Run specific test file:
```bash
pytest tests/test_code_generator.py
```

## Code Style

We follow PEP 8 style guidelines. Format your code with:
```bash
black gptbuilderauto/
flake8 gptbuilderauto/
```

## Making Changes

1. Create a new branch:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and add tests

3. Run tests and linting:
```bash
pytest
black gptbuilderauto/
flake8 gptbuilderauto/
```

4. Commit your changes:
```bash
git add .
git commit -m "Description of changes"
```

5. Push and create a pull request:
```bash
git push origin feature/your-feature-name
```

## Pull Request Guidelines

- Include tests for new features
- Update documentation as needed
- Follow existing code style
- Write clear commit messages
- Keep changes focused and atomic

## Reporting Bugs

When reporting bugs, please include:
- Python version
- GPTbuilderauto version
- Steps to reproduce
- Expected vs actual behavior
- Error messages and logs

## Feature Requests

We welcome feature requests! Please:
- Check if the feature already exists
- Describe the use case
- Explain the expected behavior
- Consider submitting a PR

## Questions?

Feel free to open an issue for any questions or concerns.

Thank you for contributing!
