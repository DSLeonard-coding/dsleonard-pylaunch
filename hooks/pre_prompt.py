#!/bin/env python3
#(C) D.S. Leonard 2025/2026
# MIT
import subprocess
from concurrent.futures import ThreadPoolExecutor
#pre_prompt.py implementation by Douglas S. Leonard, Copyright 2024.  MIT license.
#Generates cookiecutter.json defaults and replaces placeholders in templated
#initially to get author and email from git.
#Now also determines initial dependency constraints from dependencies.txt

import sys
import json
import os

sys.path.append('post_gen_resources/src')

# Initialize the Git repository and push it to GitLab
debug=False  # verbose output


def main():
    print(f"\nSTAGING DIRECTORY: {os.getcwd()}")
    apply_git_user()

def apply_git_user():
#---------git Author and email------------
    git_name_result = subprocess.run("git config --get user.name",
                                     shell=True,capture_output=True,text=True)
    if git_name_result.stdout.strip():
        author_name = git_name_result.stdout.strip()
    else:
        author_name = "author_name"

    git_email_result = subprocess.run("git config --get user.email",
                                      shell=True,capture_output=True,text=True)
    if git_email_result.stdout.strip():
        author_email = git_email_result.stdout.strip()
    else:
        author_email = "author@example.com"

    print(f"Fetched Git user: {author_name} ({author_email})")

    file_path="cookiecutter.json"
    with open(file_path, 'r') as f:
        cookiecutter_data = json.load(f)

    # Update the cookiecutter data
    cookiecutter_data['author_name'] = author_name
    cookiecutter_data['author_email'] = author_email
    #double _ varialbes do not trigger prompts but do get reparsed.
    cookiecutter_data['__repo_slug'] = "{{ cookiecutter.project_name }}"
    cookiecutter_data['__executable_name'] = "{{ cookiecutter.project_name }}"
    cookiecutter_data['project_pkg'] = "{{ cookiecutter.project_name.replace('-', '_') }}"
    # cookiecutter_data['repo_type'] = [
    #                                 "{% if 'gitlab.com' in cookiecutter.repo%}'gitlab'\
    #                                 {% else %}'github'\
    #                                 {% endif %}",
    #                                 "{% if 'github.com' in cookiecutter.repo%}'github'\
    #                                 {% else %}'gitlab'\
    #                                 {% endif %}"]

# Write the updated data back to the cookiecutter.json file
    with open(file_path, 'w') as f:
        json.dump(cookiecutter_data, f, indent=4)


main()

