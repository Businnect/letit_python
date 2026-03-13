# Deployment

## Prerequisites

```bash
pip install build twine
```

## PyPI Setup

1. Create an account at [https://pypi.org/account/register](https://pypi.org/account/register)
2. Create an API token at [https://pypi.org/manage/account/token](https://pypi.org/manage/account/token)
3. Save your token in `~/.pypirc`:

```ini
[pypi]
  username = __token__
  password = pypi-your-token-here
```

## Publishing

### 1. Update the version in `pyproject.toml`

```toml
[project]
version = "0.0.1"
```

### 2. Build the package

```bash
python -m build
```

This creates two files in `dist/`:
- `letit-0.0.1-py3-none-any.whl` (wheel)
- `letit-0.0.1.tar.gz` (source)

### 3. Check the build

```bash
twine check dist/*
```

### 4. Test on TestPyPI first (optional but recommended)

1. Create account at https://test.pypi.org/account/register
2. Get token at https://test.pypi.org/manage/account/token

```bash
twine upload --repository testpypi dist/*
```

Install from TestPyPI to verify:

```bash
pip install --index-url https://test.pypi.org/simple/ letit
```

### 5. Publish to PyPI

```bash
twine upload dist/*
```

### 6. Verify installation

```bash
pip install letit
```

## Releasing a New Version

1. Update `version` in `pyproject.toml`
2. Clean old builds: `rm -rf dist/`
3. Build: `python -m build`
4. Publish: `twine upload dist/*`

## Notes

- Update version and clean `dist/` with `$rm -rf dist` before every build to avoid uploading old versions
- PyPI does not allow re-uploading the same version — bump the version number for every release
- Use [semantic versioning](https://semver.org): `MAJOR.MINOR.PATCH`