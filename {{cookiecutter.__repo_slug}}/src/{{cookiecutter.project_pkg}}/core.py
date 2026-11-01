#!/bin/env python3
# main.py
# Copyright  {{cookiecutter.author_name}} {% now 'utc', '%Y' %}.
#
# License: {{cookiecutter.license}}
#
# provided skeleton by D.S. Leonard, MIT licensed.

#Setup useful verbosity controls for messaging and shell command execution via qx:
#see https://github.com/DSLeonard-coding/qx
from dsleonard_qx import *  # noqa so linters won't move this # type: ignore

#Names available
#from  '{{cookiecutter.project_pkg}}'.core import *
__all__=[
    '{{cookiecutter.project_pkg}}',
]
# Set __export__all__ to True to elevate names in __all__ to package level,  ie now
# from '{{cookiecutter.project_pkg}}' import *
# For single-class modules, this prevents my_class.MyClass() redundancy or manual __init__.py maintenance.
__export_all__ = True

#From bash, use export {{cookiecutter.project_pkg}}_DEBUG="True" to enable debug output
_DEBUG: bool = False   # print commands called with qx commands
if "{{cookiecutter.project_pkg}}_DEBUG" in os.environ:
    _DEBUG = True
_PRETEND: bool = False  #Option to only print qx commands, not run.

def _setup_qx():
    qx.verbosity_thresholds(qx.INFO)
    if _DEBUG or _PRETEND:
        qx.verbosity_thresholds(qx.DEBUG)   # Debug output level
    # Edit default output severity for qx command echoing and stdout, and set pretend
    qx.defaults(out_lvl=qx.INFO, echo_lvl=qx.INFO, pretend=_PRETEND)

{% if cookiecutter.install_command_entry_point  %}
#Main entry point for project.
#Edit project.scripts in pyproject.toml if you rename it, or to change the cli name
{% else %}
#Edit project.scripts in pyproject.toml if you rename it, or to change the cli name
{% endif %}
def {{cookiecutter.project_pkg}}():
    _setup_qx()
    msg("This is {{cookiecutter.project_pkg}}")  #qx.INFO level message
    msg("Edit this code in src/{{cookiecutter.project_pkg}}/main.py")  #qx.INFO level message
    qx(f'echo Hello World')  # a simple shell command.
    dbg("This method only displays with _DEBUG == True")

