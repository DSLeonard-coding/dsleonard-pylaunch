# dsleonard-pylaunch  
A uv-based python project and git repo generator to streamline modular python source development
---

with auto-generated project README.md with instructions to run or import your code directly from the git remote using uv.  

Even the smallest helper modules can now, **in seconds**, be setup to run or use in any of your other codedirectly on/from github/gitlab, with centralized maintenance and documentation. 



## Just try it! <br><sub>*Installation and Use*</sub>

You can use it directly from the git without even cloning:
```console
#install uv if you do not have it
curl -LsSf https://astral.sh/uv/install.sh | sh     # or if you have pip:  pip install pipx; pipx install uv


#Then run  pylaunch via cookiecutter without pre-installing either 
uvx cookiecutter https://github.com/DSLeonard-coding/dsleonard-pylaunch.git
```
---
Pylaunch stores configuration inputs in your ~/.cookiecutterrc for reuse. 

Works in linux, mac, and windows (See [Installing on Windows](#installing-on-windows), and on both github and gitlab (slightly more tested on github).

### Example project
https://github.com/DSLeonard-coding/example-pylaunch-project
you can run that "app" with the uv command shown there.


<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents** 

 - [Features:](#features)
 - [Motivation](#motivation)
 - [Customizing defaults for reuse](#customizing-defaults-for-reuse)
 - [Developing with local source overrides](#developing-with-local-source-overrides)
 - [A little about uv, source distribution dependencies, lockfiles](#a-little-about-uv-source-distribution-dependencies-lockfiles)
 - [Automated \_\_init\_\_.py and class name hoisting](#automated-%5C_%5C_init%5C_%5C_py-and-class-name-hoisting)
   - [Motivation](#motivation-1)
   - [Functionality](#functionality)
 - [The IDE problem and included solution.](#the-ide-problem-and-included-solution)
 - [Installing On Windows](#installing-on-windows)
   - [Windows issues](#windows-issues)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


### Features:

- Auto generates uv installable and importable **python project with pyproject.toml**.
- Auto generate local git repo  
  - Pre-fills name and email defaults from your git config
- Auto creates remote gitlab/github repo.
- **gitlab/github initial token and ssh key generation "Wizard"** 
- Auto **generates project README.md with usage instruction** to uv install or "require" the project from git url on cli.
- Auto generates **a wiki branch with a home.md**, linked to/from main repo, with auto DOCTOC on github.
      (More portable than gitlab/github wikis:  Moves with the repo)
- Project code layout uses automated `__input__.py` with 
  - auto-generated .pyi for IDE analysis/completion  (see below)
  - Facilitates easy import syntax (hoisting) for single-class-per-file project layouts. (directories for namespaces)
- Includes overrides.txt, and custom helper devsync and devrun scripts to run your dependencies
     from your local filesystem for development, overriding the remote repo sources.
- Sets up scm versioning, with initial version tag. 
  - Tagging a commit (ex: ```git tag v1.2.3``` ) will set its installed version in python/uv environment
  - However, you shouldn't use version constraints for source-build requirements anyway.
- Auto copies cookie cutter defaults to your ~/.cookiecutterrc for you to edit for next use.
- Sets up auto branch tracking of version branches to tags  (ie v1 branch -> v1.0.3 tag)
    (now tested on github and gitlab)
- Not just for python. It's an easy way to spin up a repo even if you ignore or gut the python.

More to come?, possibly static (web) pages setup too, maybe auto override-dependencies inherritance (https://github.com/astral-sh/uv/issues/18706), possibly a testing automation skeleton, and forks for CPPLaunch (with doxygen?), C#Launch, etc?.  Everything cookie cutters can already do can be piled onto this base.

### Motivation

As python project management, and dependency resolution has been a very moving target, greatly so for source-distributed dependencies, and git itself adds extra work, the overhead of trying to publish small but useful codes as modular importable libraries for reuse and development is often just too much in goal-oriented contexts like research.  This encourages scratch-pad style working with Jupyter notebooks (which still have their place) instead, and makes code re-use, version control/coordination, and bugfix/improvement sharing chaotic.

The python distribution and dependency resolution model is primarily based around binary registries, either public or "in-house," largely, in my opinion, because the loudest and most expert/involved voices use these.  But linking dependencies of source-distributions for easy re-use and sharing of code within communities has been at times difficult to essentially impossible. 

Pylaunch, with use of the uv python environment manager, aims to be the "less than a minute" solution to publishing and re-importing source-distributed python code at small scale.

### Customizing defaults for reuse

After the initial run, pylaunch copies most defaults to your ~/.cookiecutterrc file. They will apply on the next run.  They will not be automatically modified again, 
but you can edit them at any time.

Cloning the git and running cookie cutter may give you more customization control to modify the template of course. It also allows modifying the dependencies.txt, but uv can add dependencies after project generation
with ```uv add -r my_dependencies.txt``` anyway.

As always though you can add more dependencies by hand after creation with
```bash
cd my_project_dir
uv add some-project
```

Also, you can alternatively clone the pylaunch repo to a pylaunch directory, install cookiecutter (with pip or uv) and run it locally with ```cookiecutter pylaunch``` but there is little need to other than maybe customizing your repo template files.


### Developing with local source overrides
pyprojetc.toml defines dependency locations, including git sources and this determines where your libraries come from, including ones you wrote. A big aim of this launcher
is to make publishing small, reusable interlinked modules easy and painless.

But developing related sources is a pain if you have to keep publishing one to gitlab 
to test another that uses the upgrade.

Pylaunch projects include an overrides.txt file where you can add local sources to override remote dependencies during development.  The local sources can just be your local git repo directories for the remotes. An example is included, commented out, in the file.

Define your overrides and run ```./devsync``` to sync them to your the uv virtual environment for the repo (in .venv). This will not change the uv.lock.  That's important because uv.lock tells consumers of your commit how to always run this commit with the same remote versions or git commits.  But it also means that a uv sync or a uv run will wipe out the change.  You thus have to run code with ```uv run --no-sync```.  A helper commad is included. Type:
```./devrun```
at your repo root for simple examples like ```devrun mycommand```

### A little about uv, source distribution dependencies, lockfiles

Linking source dependency trees with pip has become essentially impossible. Since the solver was added it's impossible to resolve transitive version conflicts, especially in older commits, and it was never easy.

Recently uv is better than pip in many ways including speed and modularity (every project gets its own virtual environment). But it's the only option for source dependency trees without using a corporate or public binary registry.  The main reason is the uv.lock file.  When you run ```uv sync``` or ```uv run``` it produces or updates the lock file. This file contains the exact coordinates/versions of every dependency presently used.  They only update the lock with new dependencies and don't invalidate old ones unless explicitly told to. Since the file is pushed to the repo with each commit, this means anyone checking out that commit will always have the same solution you did.  There is no dependency solving done until you need to make and commit dependency changes.

uv does not work well with version constraints on source dependencies (as oposed to binnary registries), but neither does pip. The general solution is to always point your dependencies to main, master or trunk, etc, and update your latest consumers to work with the latest libraries.  The lock will do the rest.  

If needed you can use ```uv pip``` commands (which are not pip) to hand construct a requirements.txt and manually solve and lock anything.   
```sh
uv pip compile pyproject.toml -o requirements.txt
```
Will export dependencies that you can manually edit and then do
```sh
uv lock --requirements requirements.txt
```
to create the lock. The user of the commit will just use ```uv run``` as usual.


### Automated \_\_init\_\_.py and class name hoisting
#### Motivation
Python's import and namespaces are odd, in part because of using runtime code (``__init__.py``) to define them. If you keep one class per file, as is standard practice for most languages, things can be tedious. What you want in that scenario is namespace.FancyClass()  or possibly to import the namespace (package/sub-package)and just use FancyClass().  But unless you do a good bit of manually updating `__init__.py`, you will usually be calling namespace.fancy_class.FancyClass() or fancy_class.FancyClass(), both of which are silly.  And the `__init__.py` entries cause merge conflicts in git if two branches modify different modules because both must edit `__init__.py`

#### Functionality
Instead pylaunch dynamically creates `__init__.py` so users don't have to.  
All module names are exported unless the module 
a) it starts with an _                      OR    
does both of these:  
b) defines the `__all__` list of exports      AND  
c) sets `__export_all__` to True (or truthy)  
Then I hoist module.`__all__` to the package namespace.

So you can do
```python
from package import *
```
And for "traditional" modules you'll have this available: 
```python
module.module_method()
```
but if module.`__export_all__` is set and `__all__` = ["module_mehod", ...]
then you can just do:
```python
from package import *

module_method()
```
This is largely intended to allow one class per file/module, avoiding myclass.MyClass(). Namespaces can then be made by directories instead of by giant source files.  

of course you can always directly do  
```python
from package import method  # for every method 
module.module_method()

```
or  
```python
from package.module import *

method()
```
But the first requires an import for every module, the latter also does and is a dangerous habit in general because it brings in all sub-import names for modules that don't define `__all__`, and none of it allows package.FancyMethod()  provided by fancy_method.

#### The IDE problem and included solution.
The dynamic generation isn't too complicated, but it's probably not common advice for small development because IDEs cannot understand dynamically generated `__init__.py`, and you can't get tab completion, code anlaysis (big time saver), and documentation.  

So you need .pyi files.  The template includes a very custom solution to 
the [lack of a post-build uv hook](https://github.com/astral-sh/uv/issues/9645) in order 
to make generation of pyi files as automatic as possible.   And that's it.  

The scaffolding here is significant so that the use can be simple.  

### Installing on Windows

Pylaunch is 99% windows compatible. See [Windows Issues](#windows-issues)

This has been tested on a git bash terminal in windows. So you should install git bash. Because the project uses symlinks, you must either enable developer mode on windows (search in settings) or, simpler and probably safer, run the gitbash terminal as administrator.  

You will probably need to run
```sh
source $HOME/.local/bin/env  
 ```
or restart your shell after installing uv the first time.  You should get a message about it when you try to run uv.

Also for making symlinks work when uv clones the project you will first need to run this command once: 
```sh
git config --global core.symlinks true
```
It's sticks in your global git config and won't be needed again.

For development, if you need `ln -s` to work you also need to do this:
```sh
export MSYS=winsymlinks:nativestrict
```
#### Windows issues
The only thing that presently doesn't work in windows on gitbash is the post-uv sync hook in the generated project.  This means run_inits.py will not run automatically and pyi files are not generated.
The only impact is that IDE auto-completion and analysis doesn't work until you manually run `scripts/run_inits.py`
This may be fixed in the future.
