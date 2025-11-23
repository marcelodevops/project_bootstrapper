#!/usr/bin/env python3
"""
Project Bootstrapper
--------------------
This tool creates a GitHub repository and generates boilerplate project
resources based on input parameters.

Requirements:
- Python 3
- PyGithub (`pip install PyGithub`)
- A GitHub Personal Access Token with `repo` permissions set in env var GITHUB_TOKEN

Usage:
    python bootstrap.py --name myproject --description "My new tool" \
        --private true --with-readme true --with-license mit
"""

import os
import argparse
from github import Github

LICENSES = {
    "mit": "MIT License\n\nCopyright (c) 2025 YOUR NAME\n...",
    "apache2": "Apache License 2.0\n...",
    "gpl3": "GPLv3\n...",
}

def create_github_repo(name, description, private):
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise Exception("Environment variable GITHUB_TOKEN not set.")

    gh = Github(token)
    user = gh.get_user()
    repo = user.create_repo(
        name=name,
        description=description,
        private=private
    )
    return repo

def add_file(repo, path, content, message="Add file"):
    repo.create_file(path, message, content)

def main():
    parser = argparse.ArgumentParser(description="Bootstrap a GitHub project.")
    parser.add_argument("--name", required=True, help="Repository name")
    parser.add_argument("--description", default="", help="Description for repo")
    parser.add_argument("--private", default="true", help="Private repo? true/false")
    parser.add_argument("--with-readme", default="true")
    parser.add_argument("--with-license", default="none", help="License: mit, apache2, gpl3, none")

    args = parser.parse_args()
    is_private = args.private.lower() == "true"

    print(f"Creating GitHub repo '{args.name}'...")
    repo = create_github_repo(args.name, args.description, is_private)
    print(f"Repo created: {repo.clone_url}")

    if args.with_readme.lower() == "true":
        readme = f"# {args.name}\n\n{args.description}\n"
        add_file(repo, "README.md", readme)
        print("README.md added.")

    if args.with_license.lower() != "none":
        license_key = args.with_license.lower()
        content = LICENSES.get(license_key)
        if content:
            add_file(repo, "LICENSE", content)
            print("LICENSE added.")
        else:
            print(f"Unknown license '{license_key}'. Skipping.")

    # Basic project structure
    add_file(repo, ".gitignore", "*.pyc\n__pycache__/\n.env\n")
    add_file(repo, "src/main.py", "print('Hello from your new project!')\n")
    print("Basic structure created.")

if __name__ == "__main__":
    main()
