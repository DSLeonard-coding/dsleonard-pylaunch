# dsleonard-pylaunch  
A python project and git repo generator... 
---
with auto-documentation to run or import your code directly from the git remote with uv.  

Even the smallest helper modules can now, **in seconds**, be setup to run or use in any of your scripts  
directly on/from github/gitlab, with centralized maintenance and documentation. 

### Installation and use

You can use it directly from the git:
```bash
#install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh     # or if you have pip:  pip install pipx; pip install uv
#run both cookiecutter and pylaunch without installing either
uvx cookiecutter https://github.com/DSLeonard-coding/dsleonard-pylaunch.git
```
Pylaunch stores configuration inputs in your ~/.cookiecutterrc for reuse.

Works in linux, probably mac, not windows yet, more tested on github than gitlab.


### Example project
https://github.com/DSLeonard-coding/example-pylaunch-project
you can run that "app" with the uv command shown there.


### Features:

- Auto generates uv installable and importable **python project with pyproject.toml**.
- Auto generate local git repo  
  - Pre-fills name and email defaults from your git config
- Auto creates remote gitlab/github repo.
- **gitlab/github initial token and ssh key generation "Wizard"** 
- Auto **generates project README.md with usage instruction** to uv install or "require" the project from git url on cli.
- Auto generates **a wiki branch with a home.md**, linked to/from main repo, with auto DOCTOC on github.
      (More portable than gitlab/github wikis:  Moves with the repo)
- Project code layout uses dynamic __input__.py with 
  - auto-generated .pyi for IDE analysis/completion  (see below)
  - Facilitates easy import syntax (hoisting) for single-class-per-file project layouts. (directories for namespaces)
- Sets up scm versioning, with initial version tag. 
  - Tagging a commit (ex: ```git tag v1.2.3``` ) will set its installed version in python/uv environment
  - However, you shouldn't use version constraints for source-build requirements anyway.
- Auto copies cookie cutter defaults to your ~/.cookiecutterrc for you to edit for next use.
- Experimental: Sets up auto branch tracking of version branches to tags  (ie v1 branch -> v1.0.3 tag)
    (now tested on github and gitlab)

More to come, possibly static (web) pages setup too.


### Customizing defaults for reuse

After the initial run, pylaunch copies most defaults to your ~/.cookiecutterrc file.
They will apply on the next run.  They will not be automatically modified again, 
but you can edit them at any time.

Cloning the git and running cookie cutter may give you more customization control to modify the template of course.
It also allows modifying the dependencies.txt, but uv can add dependencies after project generation
with ```uv add -r my_dependencies.txt``` anyway.

As always though you can add more dependencies by hand after creation with
```bash
cd my_project_dir
uv add some-project
```


### Dynamic (automatic) __input__.py
#### Motivation
Python's import and namespaces are odd, in part because of using runtime code (__init__.py) to define them. 
If you keep one class per file, as is standard practice for most languages, things can be tedious.
What you want in that scenario is namespace.FancyClass()  or possibly to import the namespace (package/sub-package)
and just use FancyClass().  But unless you do a good bit of manually updating __init__.py, you will usually
be calling namespace.fancy_class.FancyClass() or fancy_class.FancyClass(), both of which are silly.  And the 
__init__.py entries cause merge conflicts in git if two branches modify different modules because both 
must edit __init__.py

#### Functionality
Instead pylaunch dynamically creates __init__.py so users don't have to.
All module names are exported unless the module 
a) it starts with an _                      OR  
does both of these:  
b) defines the __all__ list of exports      AND  
c) sets __expor_all__ to True (or truthy)  
Then I hoist module.__all__ to the package namespace.

So you can do
```python
from package import *
```
And for most modules you'll have this available: 
```python
module.module_method()
```
but if module.__export_all__ is set and __all__ = ["module_mehod", ...]
then you can just do:
```python
from package import *

module_method()
```
of course you can always directly do
```
from package import method  # for every method 
module.module_method()

```
or
```
from package.module import *

method()
```
But the first requires an import for every module, the latter also does and is a dangerous habit in general
because it brings in all sub-import names for modules that don't define __all__, and none of it allows
package.FancyMethod()  provided by fancy_method.

#### The IDE problem and included solution.
The dynamic generation isn't complicated, but it's probably not common advice for small development because
IDEs cannot understand dynamically generated __init__.py, and you can't get tab completion, 
code anlaysis (big time saver), and documentation.

So you need .pyi files.  The template includes a very custom solution to 
the [lack of a post-build uv hook](https://github.com/astral-sh/uv/issues/9645) in order 
to make generateion of pyi files as automatic as possible.   And that's it.

The scaffolding here is significant so that the use can be simple.

### Potentially  useful tip for side by side development of project and dependencies without/before publishing
It's useful to  develop your app and your dependency at the same time without pushing to git between tests.

#### What mostly works:
```
uv run --with-editable "dsleonard-git-tools@file:///full/path/to/your/module/clone/dsleonard-git-tools" my-app
```
This overrides the remote dependency with the local install.
The problem is it does not override transitive dependencies so you can still get conflicts. :(
It's a bit verbose.  You need a --with-editbale for every local requirement, but you can add it all to a shell script.

#### What doesn't work but probably should
Place a uv.toml in your app directory and point your dependency to your local clone with an override
```
override-dependencies = ["dsleonard-git-tools @ file:///full/path/to/your/module/clone/dsleonard-git-tools"]
```
This should override transitive dependencies.  I have not been able to get it working, in uv.toml, and maybe not
in pyproject.toml  (needs too.uv namespace there).
Relative paths do not work.
The advantage of uv.toml is supposed to be you can add it your .gitignore so it stays out of git, and it only applies during development

Regardless of the method, you need to uneable it and sync before committing a normal uv.lock.

