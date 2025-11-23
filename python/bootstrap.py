#!/usr/bin/env python3
"""
Project Bootstrapper CLI (Step 1: Convert to pip-installable package)
--------------------------------------------------------------------
This version restructures the tool as a proper Python package ready
for packaging and installation via pip.

Features included:
- Typer-based CLI
- Commands: init (create repo + scaffold)
- Package-ready layout

Next steps will add templates, org support, issues, etc.
"""

import os
from pathlib import Path
import typer
from github import Github

app = typer.Typer()

LICENSES = {
    "mit": "MIT License Copyright (c) 2025 YOUR NAME...",
    "apache2": "Apache License 2.0...",
    "gpl3": "GPLv3...",
}

def get_github(org: str | None = None):
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise Exception("Environment variable GITHUB_TOKEN not set.")

    gh = Github(token)
    if org:
        return gh.get_organization(org)
    return gh.get_user()


def add_file(repo, path: str, content: str, message: str = "Add file"):
    repo.create_file(path, message, content)


@app.command()
def init(
    name: str = typer.Option(..., help="Repository name"),
    description: str = typer.Option("", help="Repo description"),
    private: bool = typer.Option(True, help="Make repo private"),
    org: str | None = typer.Option(None, help="GitHub org name"),
    readme: bool = typer.Option(True, help="Include README.md"),
    license: str = typer.Option("none", help="License type: mit/apache2/gpl3/none"),
):
    """Create a GitHub project and scaffold it."""

    owner = get_github(org)
    repo = owner.create_repo(name=name, description=description, private=private)
    typer.echo(f"Repo created: {repo.clone_url}")

    if readme:
        add_file(repo, "README.md", f"# {name} {description}")
        typer.echo("README.md added.")

    if license != "none":
        content = LICENSES.get(license)
        if content:
            add_file(repo, "LICENSE", content)
            typer.echo("LICENSE added.")
        else:
            typer.echo(f"Unknown license '{license}'. Skipping.")

    # Project structure
    add_file(repo, ".gitignore", "*.pyc__pycache__/.env")
    add_file(repo, "src/main.py", "print('Hello from your new project!')")

    # Dockerfile
    dockerfile = """
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt || true
CMD [\"python\", \"src/main.py\"]
"""
    add_file(repo, "Dockerfile", dockerfile)

    # GitHub CI
    ci_yaml = """
name: CI
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt || true
      - run: python src/main.py
"""
    add_file(repo, ".github/workflows/ci.yml", ci_yaml)

    # Microservice example
    add_file(repo, "services/example_service/main.py", "print('Example microservice running')")

    typer.echo("Project scaffold complete.")


if __name__ == "__main__":
    app()
