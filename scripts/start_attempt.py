#!/usr/bin/env python3
"""Create a new standalone practice copy without changing previous attempts."""
import argparse
from datetime import datetime, timezone
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
IGNORED = ('.venv', 'venv', 'env', '__pycache__', '.pytest_cache', '.mypy_cache',
           '.ruff_cache', '.tox', '.nox', '.git', 'build', 'dist', '*.egg-info', '*.pyc')


def start_attempt(project_id, name=None, root=ROOT):
    """Resolve an ID from the catalog and copy it into an unused attempt directory."""
    project_id = project_id.upper()
    if not re.fullmatch(r'[EMH]0[1-5]', project_id):
        raise ValueError(f'Unknown project ID: {project_id}')
    matches = list((root / 'projects').glob(f'*/{project_id.lower()}-*'))
    if len(matches) != 1 or not (matches[0] / 'pyproject.toml').is_file():
        raise ValueError(f'Unknown or unavailable project ID: {project_id}')
    name = name or datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,79}', name):
        raise ValueError('Attempt name must be 1–80 letters, numbers, underscores or hyphens')
    destination = root / 'attempts' / f'{project_id.lower()}-{name}'
    if destination.exists():
        raise FileExistsError(f'Attempt already exists: {destination}')
    destination.parent.mkdir(exist_ok=True)
    shutil.copytree(matches[0], destination, ignore=shutil.ignore_patterns(*IGNORED))
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project_id', help='E01–E05, M01–M05 or H01–H05')
    parser.add_argument('--name', help='Optional unique attempt label')
    args = parser.parse_args()
    try:
        destination = start_attempt(args.project_id, args.name)
    except (ValueError, FileExistsError) as error:
        parser.error(str(error))
    print(destination)
    print(f'cd {str(destination)!r}')
    print('python3 -m venv .venv')
    print('source .venv/bin/activate')
    print('python -m pip install -e ".[test]"')
    print('python -m pytest -q')


if __name__ == '__main__':
    main()
