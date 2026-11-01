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
uv add "{{ cookiecutter.__repo_slug }} @ git+https://{{ cookiecutter.repo }}/{{ cookiecutter.repo_namespace }}/{{ cookiecutter.__repo_slug }}.git"
uv sync   # redundant here actually.
uv run myscript.py

```
for private repos replace ```git+https://```   with ```git+ssh://git@``` to use ssh authentication.


### Use in a quick script:
The --script option will embed the dependencies to the top of your script, avoiding the need for a pyproject.toml
```bash
uv add --script myscript.py "{{ cookiecutter.__repo_slug }} @ git+https://{{ cookiecutter.repo }}/{{ cookiecutter.repo_namespace }}/{{ cookiecutter.__repo_slug }}.git"
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


However, if you want today's version of your script to always run with today's tested dependencies, 
you need to commit it with an extra lock file anyway, made with:

```bash
uv lock --script myscript.py
```
Don't worry, future commits can be re-locked to updated dependencies.  It just makes sure
that every commit works the same as the day you committed it.


### Explanation, uv vs conda, pip,  and best practices
Here ```uv add``` adds the dependency to an existing pyproject.toml file, or creates a new one, and actually
does a ``` uv sync ```, which replaces ```conda activate``` and ```pip install```.  It creates a venv that applies within that directory and all subdirectories,  installs the latest version of the library in it, and creates the uv.lock file to lock dependency versions for future use.  

To make sure your script always builds with the same library version you tested with, include the created uv.lock file in your distribution of the script (git or otherwise).  Further use of ```uv sync``` will be version pinned, ensuring old git commits are locked to build the same as when the commit was made.  

Do not be tempted to select a tag in the add command.  This will strongly restrict/break dependency resolution in even moderately bigger projects.  Source distribution is different from binary registry distribution. Version constraints essentially do not work for source-distributed dependencies.  This is what uv.lock is for.

Resolving dependency problems with source builds has become almost impossible with pip and was never great.  The lock file and various overrides make
uv a clear winner for source-based (non-pypi) github sharing.


---
This project was made and launched using the [dsleonard-pylauch](https://github.com/DSLeonard-coding/dsleonard-pylaunch.git) cookie cutter.  To launch your own just do:
```bash
uvx cookiecutter https://github.com/DSLeonard-coding/dsleonard-pylaunch.git
```



