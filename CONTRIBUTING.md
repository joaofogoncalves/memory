# Contributing to LinkedIn Post Archiver

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Ways to Contribute

- 🐛 Report bugs
- 💡 Suggest new features
- 📝 Improve documentation
- 🔧 Submit bug fixes
- ✨ Add new features

## Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/joaofogoncalves/linkedin-post-archiver.git
cd linkedin-post-archiver
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Verify setup
python verify_setup.py
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

## Development Guidelines

### Code Style

- Follow PEP 8 style guide
- Use type hints for function parameters and return types
- Write descriptive variable names
- Add docstrings to all public functions (Google style)

Example:
```python
def fetch_posts(author_urn: str, limit: Optional[int] = None) -> List[LinkedInPost]:
    """
    Fetch posts for a LinkedIn user.

    Args:
        author_urn: LinkedIn person URN
        limit: Maximum number of posts to fetch

    Returns:
        List of LinkedInPost objects

    Raises:
        APIError: If the API request fails
    """
    pass
```

### Testing

Before submitting:

1. **Test your changes:**
   ```bash
   # Test with limited posts
   python scraper/main.py --limit 5
   ```

2. **Check logs:**
   ```bash
   cat logs/scraper.log
   ```

3. **Verify output:**
   ```bash
   ls -R posts/
   ```

### Documentation

- Update relevant documentation (README.md, CLAUDE.md, etc.)
- Add inline comments for complex logic
- Update CHANGELOG if significant changes

## Submitting Changes

### 1. Commit Your Changes

```bash
git add .
git commit -m "Brief description of changes

Detailed explanation of what was changed and why.
Fixes #issue_number (if applicable)"
```

**Commit Message Guidelines:**
- Use present tense ("Add feature" not "Added feature")
- First line: Brief summary (50 chars or less)
- Blank line, then detailed description if needed
- Reference issue numbers when applicable

### 2. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 3. Create Pull Request

1. Go to the original repository on GitHub
2. Click "New Pull Request"
3. Select your fork and branch
4. Fill in the PR template:
   - **Title:** Clear, concise description
   - **Description:** What changed and why
   - **Testing:** How you tested the changes
   - **Screenshots:** If UI-related

## Pull Request Guidelines

### Before Submitting

- ✅ Code follows project style guidelines
- ✅ All new code has appropriate docstrings
- ✅ Documentation updated if needed
- ✅ Tested with `--limit 5` to verify functionality
- ✅ No sensitive information committed

### PR Review Process

1. Maintainers will review your PR
2. Address any requested changes
3. Once approved, your PR will be merged

## Reporting Issues

### Bug Reports

Include:
- **Description:** Clear description of the bug
- **Steps to Reproduce:** Exact steps to reproduce the issue
- **Expected Behavior:** What should happen
- **Actual Behavior:** What actually happens
- **Environment:**
  - OS (macOS, Linux, Windows)
  - Python version
  - Relevant log output from `logs/scraper.log`
- **Screenshots:** If applicable

### Feature Requests

Include:
- **Description:** Clear description of the feature
- **Use Case:** Why this feature would be useful
- **Proposed Solution:** How you think it could work (optional)
- **Alternatives:** Alternative approaches considered (optional)

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards others

### Unacceptable Behavior

- Harassment or discriminatory language
- Trolling or insulting comments
- Publishing others' private information
- Other unprofessional conduct

## Questions?

If you have questions:
- Check existing issues and discussions
- Review documentation (README.md, CLAUDE.md)
- Open a new issue with the "question" label

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to LinkedIn Post Archiver! 🎉
