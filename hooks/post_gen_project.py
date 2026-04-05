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

use_local_deps = "{{ cookiecutter._use_local_deps }}"
dsleonard_git_tools_path = "{{ cookiecutter._dsleonard_git_tools_path }}"
dsleonard_cc_rc_merge_path ="{{ cookiecutter._dsleonard_cc_rc_merge_path }}"
dsleonard_qx_path ="{{ cookiecutter._dsleonard_qx_path }}"

#from post_gen_resources import post_gen_runner
sys.path.append('post_gen_resources/')
from find_or_install_uv import find_or_install_uv

def main():
    print("Running post generation script...")

    try:
        #if it's already setup, we'll just get the exe:
        cwd=os.getcwd()
        resource_dir = "post_gen_resources"
        venv_dir = os.path.join(resource_dir, ".setup_venv")
#        python_exe, uv_bin = provision_venv(venv_dir, toml_dir=resource_dir)
        uv_bin = find_or_install_uv(venv_dir, toml_dir=resource_dir)
        os.chdir(cwd)

        # the final pyproject.toml was masked to keep uv away from it during provisioning.
        os.rename("pyproject.template.toml", "pyproject.toml")
    except Exception as e:
        print(f"Error occurred in post-project environment setup {e}")
        sys.exit(1)

    try:

        if use_local_deps:
            cmd = [
                uv_bin,"run",
                "--with-editable", dsleonard_git_tools_path,
                "--with-editable", dsleonard_cc_rc_merge_path,
                #This one cannot work because dsleonard_git_tools itself uses it and conflicts!
                #Forced to hard code it temporarily in tool.uv.sources or override-dependencies.
                #"--with-editable", dsleonard_qx_path,
                "--project", resource_dir,
                f"{resource_dir}/post_gen_runner.py",uv_bin
                   ]
            cmd_str=" ".join(cmd)
            print(cmd_str)
            print("\n")
            subprocess.run(cmd_str, shell=True, check=True)

        else:
            subprocess.run([uv_bin,"run",
                            "--project", resource_dir,
                            f"{resource_dir}/post_gen_runner.py",uv_bin], check=True)
#            subprocess.run([python_exe,f"{resource_dir}/post_gen_runner.py",uv_bin], check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error running post_gen_runner.py")
        #At this point, we're exiting anyway.  Allow cleanup.
        pass

    try:
        os.chdir(cwd)
        shutil.rmtree(Path(venv_dir))
        os.chdir(cwd)
        shutil.rmtree(Path("post_gen_resources"))
    except:
        #if cleanup fails don't be too loud about it.
        pass



if __name__ == "__main__":
        main()
        sys.exit(0)
