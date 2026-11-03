# {{cookiecutter.__repo_slug}}
> {{cookiecutter.description}}  
By {{cookiecutter.author_name}}, Copyright {% now 'utc', '%Y' %}

## License

This project is licensed under the following terms:  
{{cookiecutter.license}}  

### Install uv if you don't have it
```
curl -LsSf https://astral.sh/uv/install.sh | sh    # or with pip:  pip install pipx; pip install uv
```

{% if cookiecutter.install_command_entry_point -%}
### Install and run the app/command:
```bash
uv tool install "git+https://{{ cookiecutter.repo }}/{{ cookiecutter.repo_namespace }}/{{ cookiecutter.__repo_slug }}.git"
{{ cookiecutter.__executable_name }}
```

To use ssh (if this is a private project) use:
```bash
uv tool install "git+ssh://git@{{ cookiecutter.repo }}/{{ cookiecutter.repo_namespace }}/{{ cookiecutter.__repo_slug }}.git"
```

If want to use libraries provided by the application...
{% endif %}
### Use in your custom library or app
To use {{ cookiecutter.__repo_slug }} in a python program, cd to your working directory or project directory, if it's already a  project, and just do:
```bash
uv add "{{ cookiecutter.__repo_slug }} @ git+https://{{ cookiecutter.repo }}/{{ cookiecutter.repo_namespace }}/{{ cookiecutter.__repo_slug }}.git" --refresh
uv sync --refresh
uv run myscript.py    # optionally can skip sync and provide --refresh to uv run
```
for private repos replace ```git+https://```   with ```git+ssh://git@``` to use ssh authentication.

`--refresh` is important for bypassing your local cache and getting the latest versions of source dependencies.

### Use in a quick script:
The --script option will embed the dependencies to the top of your script, avoiding the need for a pyproject.toml
```bash
uv add --script myscript.py "{{ cookiecutter.__repo_slug }} @ git+https://{{ cookiecutter.repo }}/{{ cookiecutter.repo_namespace }}/{{ cookiecutter.__repo_slug }}.git" --refresh
```
Then add the following uv shebang as the first line in your script file:
```sh
#!/usr/bin/env -S uv run --script --python 3.13
```
and make the script executable:
```bash
chmod +x myscript.py
```
Then you can just execute your script:
```bash
./myscript.py
```
This spins up a cached virtual environment with all the dependencies installed associated just with this script.

Or if you don't like the shebang, leave it out and run with uv manually with
```bash
uv run --python 3.13 myscript.py    # the --python <version> is optional
```

If you want today's version of your script to always run with today's tested dependencies, you need to produce a lock file for it made with:
```bash
uv lock --script myscript.py --refresh
```
Don't worry, future commits can be re-locked to updated dependencies.  It just makes sure
that every commit works the same as the day you committed it.


## Development

### Cloning 
If you want to develop the project locally, if you don't already have a clone make one:
```bash
git clone https://{{ cookiecutter.repo }}/{{ cookiecutter.repo_namespace }}/{{ cookiecutter.__repo_slug }}.git
cd {{ cookiecutter.__repo_slug }}
```

{% if cookiecutter.install_command_entry_point -%}

###  Running your cloned app
You can run your project from the cloned directory with:
```
uv run {{ cookiecutter.__executable_name }}
```
This will run ```uv sync``` and will run `{{ cookiecutter.__executable_name }}` in the virtual environment.
{% endif %}

### Adding dependencies
you can add new dependencies with
```
uv add some_dep
```
which will add some_dep to the pyproject.toml and will run a uv sync which will install it to your virtual environment in .venv/ , and finally will add it to your uv.lock file.  As shown above, some_dep can be a git repo.  

Th some_dep specifier for git repos can optionally end in @ref where ref is a branch or tag. Do not be tempted to select a tag, or even version-limited branch, in the add command.  This will strongly restrict/break dependency resolution in even moderately bigger projects.  Source distribution is different from binary registry distribution. Version constraints essentially do not work for source-distributed dependencies.  This is what uv.lock is for. You should generally target the default branch or master/main/trunk. 

{% if not cookiecutter.install_command_entry_point -%}
If  `{{ cookiecutter.__repo_slug }}` remains a library only.  You likely don't care a lot about the rest of this section.  The virtual environment and lock files are not used by an app that depends on your library.  Only the pyproject.toml is used.  However, if you run test scripts against your repo manually, or in CI/CD, it can still be good to have each commit have locked-down dependencies, so continue reading.
{% endif %}

### Locking dependencies

Resolving dependency problems with source builds has become almost impossible with pip and was never great.  The lock file and various overrides make
uv a clear winner for source-based (non-pypi) github sharing.

After some development you can update any added dependancies to the virtual environment with:
```bash
uv sync --refresh
```

This will add or remove dependancies in the virtual evnironment and in the ```uv.lock``` file but will not unpin previously locked versions unless needed to satisfy new constraints.  The `--refresh` option is not mentioned often but is important for source-distribution dependencies, because for reasons that are complicated, specifying version constraints on source dependencies is presently a disaster, so we instead should only specify the default branch or master/main/trunk.  Without ```--refresh``` uv sync will look for solutions in the local cache first, and it will not find the latest version from the repo.  If you are re-locking, this not usually what you want.

If you want to completely update version dependencies to the latest that match, you can run
```bash
uv lock --upgrade --refresh
```
or remove the `uv.lock` file and run `uv sync --refresh`

In the toughest cases you can even edit the uv.lock by hand to specify exact commit shas for your source dependencies, or use the included `overrides.txt` tools and then lock in.

You should always get your locks settled the way you want before committing to main branches.  In particular you should usually remove any local source overrides and ```uv sync --refresh``` before committing.  Whatever version you have pinned in an app commit are the versions anyone who checks out that commit will get by default. 

The virtual environment is stored in .venv, and if in doubt, you can safely remove the whole directory and resync it.





---
This project was made and launched using the [dsleonard-pylauch](https://github.com/DSLeonard-coding/dsleonard-pylaunch.git) cookie cutter.  To launch your own just do:
```bash
uvx cookiecutter https://github.com/DSLeonard-coding/dsleonard-pylaunch.git
```



