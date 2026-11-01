#(C) D.S. Leonard 2025
# MIT,  use with attribution only.
# Bootstrap coordinator to launch a full env project.

import subprocess
import os
import sys
import traceback
import venv
import shutil
from pathlib import Path

use_local_deps = {{ cookiecutter._use_local_deps }}
dsleonard_git_tools_path = "{{ cookiecutter._dsleonard_git_tools_path }}"
dsleonard_cc_rc_merge_path ="{{ cookiecutter._dsleonard_cc_rc_merge_path }}"
dsleonard_qx_path ="{{ cookiecutter._dsleonard_qx_path }}"

#from post_gen_resources import post_gen_runner
sys.path.append('post_gen_resources/')
from find_or_install_uv import find_or_install_uv

def cleanup(cwd, venv_dir):
    try:
        os.chdir(cwd)
        shutil.rmtree(Path(venv_dir))
        os.chdir(cwd)
        shutil.rmtree(Path("post_gen_resources"))
    except:
        # If cleanup fails don't be too loud about it.
        pass

def main():
    print("Running post generation script...")


    try:
        #if it's already setup, we'll just get the exe:
        cwd=os.getcwd()
        resource_dir = "post_gen_resources"
        venv_dir = os.path.join(resource_dir, ".venv")
        #        python_exe, uv_bin = provision_venv(venv_dir, toml_dir=resource_dir)
        uv_bin = find_or_install_uv(venv_dir, toml_dir=resource_dir)
        os.chdir(cwd)

        # the final pyproject.toml was masked to keep uv away from it during provisioning.
        os.rename("pyproject.template.toml", "pyproject.toml")
    except Exception as e:
        print(f"Error occurred in post-project environment setup {e}")
        sys.exit(1)

    try:
        resource_dir_path = Path(resource_dir)
        reqs_file = resource_dir_path / "requirements.txt"
        overrides_file = resource_dir_path / "overrides.txt"
        pyproject_file = resource_dir_path / "pyproject.toml"

        if use_local_deps:
            print("Configuring local dependency overrides.")
            overrides_content = (
                #These should already be provided in project@file:///path  format
                f"{dsleonard_git_tools_path}\n"
                f"{dsleonard_cc_rc_merge_path}\n"
                f"{dsleonard_qx_path}\n"
            )

            overrides_file.write_text(overrides_content)

            print("Ensuring virtual environment exists...")
            venv_cmd = [uv_bin, "venv", venv_dir, "--allow-existing"]
            subprocess.run(venv_cmd, check=True)

            lock_file = resource_dir_path / "uv.lock"

            if lock_file.exists():
                requirements_in = resource_dir_path / "requirements.in"
                compile_target = str(requirements_in)
                print("Found existing uv.lock. Exporting baseline...")
                export_cmd = [
                    uv_bin, "export",
                    "-q", #Quiet
                    "--locked",
                    "--format", "requirements-txt",
                    "-o", compile_target,
                    "--project", resource_dir
                ]
                subprocess.run(export_cmd, check=True)
            else:
                print("No uv.lock found. Compiling fresh from pyproject.toml...")
                compile_target = str(pyproject_file)

            compile_cmd = [
                uv_bin, "pip", "compile",
                "-q",  # Quiet
                compile_target,
                "-o", str(reqs_file),
                "--override", str(overrides_file)
            ]

            print("Compiling requirements...")
            subprocess.run(compile_cmd, check=True)

            # lock the requirements.txt into the venv
            sync_cmd = [uv_bin, "pip", "sync", str(reqs_file), "--prefix", str(venv_dir)]

            print("Syncing environment...")
            subprocess.run(sync_cmd, check=True)

            print(f"Executing post-gen runner... with {uv_bin}")
            subprocess.run([
                uv_bin, "run",
                "--no-sync",
                "--project", resource_dir,
                f"{resource_dir}/post_gen_runner.py", uv_bin
            ], check=True)

        else:
            print(f"Executing post-gen runner... with {uv_bin}")
            subprocess.run([
                uv_bin, "run",
                "--project", resource_dir,
                f"{resource_dir}/post_gen_runner.py", uv_bin
            ], check=True)


    except subprocess.CalledProcessError as e:
        print(f"Error running post_gen_runner.py")
        cleanup(cwd,venv_dir)
        sys.exit(0)

    cleanup(cwd, venv_dir)

if __name__ == "__main__":
    main()
    sys.exit(0)
