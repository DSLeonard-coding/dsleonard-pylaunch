#dsl-pylaunch post_gen_project script to setup local and remote repo, etc.
#(C) D.S. Leonard 2025
# MIT,  use with attribution only.
#TODO don't crash out on no overwrite.  But this is a little hard.
#Whole report should change.

import os
import platform
import textwrap
import traceback
from datetime import datetime

from pathlib import Path
import webbrowser

from typing import Any, List, Optional, Union
import getpass

from dsleonard_cc_rc_merge import cc_rc_merge
from dsleonard_qx import *
#from dsleonard_git_tools.dsleonard_git_api import *
from dsleonard_git_tools import *
#print(f'--- LOADING FROM: {dsleonard_git_tools.__file__} ---')
import json

# post_gen_project.by implementation by Douglas S. Leonard, Copyright 2024.  MIT license.
import sys
# Initialize the Git repository and push it to GitLab
repo_name = "{{ cookiecutter.__repo_slug }}"
description = "{{ cookiecutter.description }}"
repo_namespace = "{{ cookiecutter.repo_namespace }}"
host = "{{ cookiecutter.repo }}"
author_name = "{{ cookiecutter.author_name }}"
author_email = "{{ cookiecutter.author_email }}"
overwrite_repo = "{{ cookiecutter.overwrite_repo }}"
repo_type = "{{cookiecutter.repo_type}}"
auto_push = {{cookiecutter.auto_push_new_repo}}
#Somehow the CC vars get pasted as capitlaized True/False:
make_repo_public = {{cookiecutter.make_repo_public}}
is_create_wiki = {{cookiecutter.create_wiki_page}}
is_executable_project = {{cookiecutter.install_command_entry_point}}
project_pkg = "{{ cookiecutter.project_pkg }}"
show_repo = True
main_proj_dir = ""
summary = []
disclaimers = []

debug = False  # verbose output

def main():
    global main_proj_dir
    main_proj_dir=os.getcwd()
    uv_bin = sys.argv[1]
    os.environ["SETUPTOOLS_SCM_PRETEND_VERSION"] = "0.1.0"
    qx(f"{uv_bin} add -r dependencies.txt")
    qx(f"{uv_bin} lock")

    initialize_git_with_remote(uv_bin,
                               host,
                               repo_namespace,
                               repo_name,
                               overwrite_repo,
                               description,
                               repo_type,
                               author_name,
                               author_email)

    # Save cc defaults for local editing
    rc_path = os.path.expanduser("~/.cookiecutterrc")
    cc_data = json.loads(r'{{ cookiecutter | jsonify | replace("\n", "") }}')

    #merge configs with user defaults, silence status output:
    qx.verbosity_thresholds(verbose_thrsh=qx.PRIORITY)
    cc_rc_merge.merge_rc_from_json(cc_data, rc_path=rc_path)
    qx.verbosity_thresholds(verbose_thrsh=qx_verbosity)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    summary.append(f"     [ {timestamp} Requirements locked in uv.lock. ]")
    summary.append(f"     [ {timestamp} Editable default mission parameters stored in {rc_path}. ]")
    summary.append(f"     [ {timestamp} All systems nominal. ]")
    summary.append("\n\n")

    for line in summary:
        print(line)
    for line in disclaimers:
        print(line)

def add_requirements(uv_bin):
    qx(f"{uv_bin} add -r dependencies.txt")
    qx("rm requirements-cleaned.txt")
    qx("rm dependencies.txt")

def open_docs(filepath="README.md"):
    if platform.system() == 'Darwin':  # macOS
        subprocess.call(('open', filepath))
    elif platform.system() == 'Windows':
        os.startfile(filepath)
    else:  # Linux
        subprocess.call(('xdg-open', filepath))


def initialize_git_with_remote(uv_bin,host, repo_namespace, repo_name, overwrite_repo, description, repo_type,author_name,author_email):
    if author_name == None:
        git_name_result = git("config --get user.name")
        if git_name_result.stdout.strip():
            author_name = git_name_result.stdout.strip()

        else:
            raise RuntimeError("No git author_name provided or found.") from None
    if author_email == None:
        git_email_result = git("config --get user.email")
        if git_email_result.stdout.strip():
            raise RuntimeError("No git author_email provided or found.") from None

    msg(f"Initializing git repository for {repo_name}...")
    git("init")

    git(f"config user.name {author_name}")
    git(f"config user.email {author_email}")

    git(f"commit --allow-empty -m 'empty commit'")
    git(f"tag empty'")

    git(["add", "."])
    git(f"commit -m 'Initial commit of {repo_name}'")

    dflt_branch = git(["rev-parse", "--abbrev-ref", "HEAD"]).lines[0]
    msg(f"Local git repository has been created and and is ready to push:")



    force_flag, recreate_repo = (True, True ) if overwrite_repo == "YES" else (True, False)
    remote_push_status = True
    try:
        repo=CreateRemoteManager(host,repo_namespace,repo_name,recreate_repo,description,repo_type)
        repo.create_remote_repo_if_allowed("origin")
        if repo_type == "gitlab":
            repo.apply_default_protections(dflt_branch)
        repo.setup_ssh_keys()  #optional, can push with token directly.
        repo.push_git_webhost(dflt_branch,force_flag)
    except Exception as e:
        print (str(e).split("Traceback")[0].strip())
        remote_push_status = False
        disclaimers.append(f"\n{' '*4} Mission Note: Unable to create or push to remote repo.\n"
                           f"{' '*8}Your local repository is setup.\n"
                           f"{' '*8}You can manually setup your remote or review error messages above and try again.\n\n")

    try:
        repo.setup_ci_secrets()
    except Exception as e:
        print (str(e).split("Traceback")[0].strip())
        raise RuntimeError("\n{' '*4}Mission Note: Unable to setup authorization keys for CI/CD\n"
                           f"{' '*8}Your repo was successfully created and pushed to the remote.\n"
                           f"{' '*8}This only impacts automation on the remote, which you can setup manually.\n")
    wiki_url=""
    if is_create_wiki:
        git("checkout --orphan wiki")
        git("rm -rf . --cached")
        git("rm -rf .")
        qx(f"echo '# {repo_name} Wiki  \n' >> home.md")
        #TODO, mark the url as public (no _)
        qx(f'echo "[Link to the project repo]({repo.https_url})\n" >> home.md')

        # Add a doctoc tag to home.md.  Optional but makes TOC location explicit:
        doctoc_tags=textwrap.dedent('''
            <!-- START doctoc generated TOC please keep comment here to allow auto update -->
            <!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
            
            <!-- END doctoc generated TOC please keep comment here to allow auto update -->
            '''
        )
        qx(f'echo "{doctoc_tags}" >> home.md')
        qx(f"echo '\n\n## Section to be written' >> home.md")
        qx(f"echo '### Subsection to be written' >> home.md")
        git("add home.md")
        # Add the doctoc action workflow for github:
        git("add .github/workflows/toc.yml")
        git("commit -m 'First commit of wiki'")
        push_wiki_status = False
        if auto_push:
            try:
                repo.push_git_webhost("wiki", force_flag)
                push_wiki_status = True
            except:
                push_wiki_status = False

        if not auto_push or push_wiki_status == False:
            disclaimers.append(f"{' '* 4}Mission Note:  A wiki branch was created but not pushed")
            disclaimers.append(f"{' '* 8}Use` git push -u origin wiki` to deploy objective")


        wiki_url = repo.set_branch_wiki_link("wiki","home.md")
        git(f'checkout -f {dflt_branch}')

    #push a tag, trigger workflow
    git('tag v0.0.1')
    if auto_push:
        repo.push_git_webhost(dflt_branch,force_flag,push_tags=True)
    else:
        disclaimers.append(f"{' ' * 4}Mission Note:  A tag was created but not pushed")
        disclaimers.append(f"{' ' * 8}Use ` git push origin --tags` to deploy objective")

    if make_repo_public:
        repo.update_settings(public=True)

    def link(url, text=None):
        # OSC 8 escape sequence for clickable terminal links
        text = text if text is not None else url
        return f"\033]8;;{url}\033\\{text}\033]8;;\033\\"

    # Setup paths and links
    abs_path = os.path.abspath(main_proj_dir)
    local_base_raw = f"{abs_path}"
    local_base = link(local_base_raw)
    remote_orbit = link(repo.https_url, repo.https_url)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    summary.append(f"\n")
    summary.append(f"\n     🚀 {'-' * 80} 🚀")
    summary.append(f"\n     [ {timestamp} Mission Report: ]")
    summary.append(f"     🚀 PYLAUNCH SUCCESSFUL")
    summary.append(f"\n     🚀📂 LOCAL BASE   {local_base}")
    summary.append(f"\n     🚀🌐 REMOTE ORBIT {remote_orbit}")

    def code(text):
        return f"\033[48;5;236m\033[38;5;253m {text} \033[0m"

    if is_create_wiki:
        wiki_link = link(wiki_url, wiki_url)
        summary.append(f"\n     🚀📖 Wiki COMMS   {wiki_link}")

    command = f"uvx {repo.pygit_url}"
    if is_executable_project:
        summary.append(f"\n     🚀📡 EXECUTE mission ops: {code(link(command))}")

    command = f"uv add {repo.pygit_url}"
    summary.append(f"\n     🚀🛰️  MODULE integration: {code(link(command))}")
    src_dir = f"{local_base_raw}/src/{project_pkg}"
    summary.append(f"\n     🚀🛰️  PAYLOAD MAINTENANCE: {code(link(src_dir))}")

    summary.append(f"\n     🚀 {'-' * 80} 🚀")

    if show_repo:
        webbrowser.open(repo.https_url)

project_path = os.getcwd()
print(f"\n🚀 New repo created at: {project_path}")

qx_verbosity = qx.INFO
if debug:
    qx_verbosity=qx.DEBUG
    qx.verbosity_thresholds(verbose_thrsh=qx_verbosity)

try:
    cwd = os.getcwd()
    main()
except (SystemExit,Exception) as e:
    if isinstance(e, SystemExit) and (e.code == 0 or e.code is None):
        sys.exit(0)

    print("")
    print("***************Errors occurred in post-project generation*********")
    print("Your project,repo, or remotes may not be fully configured.")
    if not isinstance(e, SystemExit):
        os.chdir(cwd)
        errfile="post-gen-runner-error-log.txt"
        with open(errfile, "w") as f:
            traceback.print_exc(file=f)
            print(e, file=f)
        print(f"Traceback dumped to {cwd}/{errfile}")
        print("")
    sys.exit(1)


