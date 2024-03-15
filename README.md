# FastAPI + PostgreSQL Project Starter

## Setup

1. Install python `v3.12`
2. Install poetry - `curl -sSL https://install.python-poetry.org | python3 -`
3. Run `cat poetry.toml > ~/Library/Application\ Support/pypoetry/config.toml`
4. Run `poetry install`
5. `cp .env.template .env` (do not alter contents of .env.template)
6. `docker compose up -d --build` (first run only)
7. `docker compose exec backend-api migrate`
8. for VSCode only
   - install python `3.12` and poetry, and run `poetry install` to auto-setup the virtualenv
   - make sure the python interpreter in VSCode is set to the poetry venv

### [TablePlus](https://tableplus.com/)

Connection Fields:

- Host/Socket: `127.0.0.1` (default, leave blank)
- Port: `5432` 
- Password: `changethis`
- Database: `app`

### VSCode Extensions

- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) → should automatically install [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance), [Python Debugger](https://marketplace.visualstudio.com/items?itemName=ms-python.debugpy)
- [Ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff) (linter, code formatter)
- [Mypy Type Checker](https://marketplace.visualstudio.com/items?itemName=ms-python.mypy-type-checker)
- [Even Better TOML](https://marketplace.visualstudio.com/items?itemName=tamasfe.even-better-toml)
- [pytest-fixtures](https://marketplace.visualstudio.com/items?itemName=nickmillerdev.pytest-fixtures)
- [Docker](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker)
- [DotENV](https://marketplace.visualstudio.com/items?itemName=mikestead.dotenv)
- [Path Intellisense](https://marketplace.visualstudio.com/items?itemName=christian-kohler.path-intellisense)

### Docker Command Shortcuts

Run the command below to install `docker compose` command shortcuts:

```bash
cat <<EOF >> ~/.bash_profile && source ~/.bash_profile # replace ~/.bash_profile with your preferred shell (I use /bin/bash in this case)

# Docker compose aliases
alias dc="docker compose"
alias dca="dc attach"
alias dcu="dc up -d"
alias dcd="dc down"
alias dce="dc exec"
alias dcps="dc ps"

# Docker network aliases
alias dn="docker network"
alias dni="dn inspect"
alias dnls="dn ls"
EOF
```

## Running the FastAPI Server

There are 3 ways you can run the server:

- in a docker container - `docker compose up` commands
- running it manually in poetry's virtual environment
  1. navigate to the backend project's root directory
  2. enter poetry's virtual env with: `source "$(poetry env info -p)/bin/activate`
  3. run the `uvicorn` command: `uvicorn --reload --port=8080 src.main:app`
- running locally in debug mode
  - this enables you to run and test with breakpoints using the OpenAPI docs or frontend code (**not the same** as running pytest integration tests)
  - go to Debugging → FastAPI for more info on how to do this

## Docker

Run `docker compose up -d --build` on these changes:

- `.env` file variables
- `Dockerfile`
- `compose.*.yml`

```sh
# Workflow:

# Start docker services (build is optional)
docker compose up -d # --build

# Alternative way to start
# docker compose build
docker compose up -d

# Terminal docker compose services
docker compose down # -v (to delete persisted volumes/data)

# Attach to see terminal output
docker compose attach <service_name>

# Start a terminal in a service
docker compose exec <service_name> bash

# Remove all unused/dangling resources
docker system prune
```

Services:

- `backend-api` - FastAPI web server
- `pg-db` - PostgreSQL database server

## iTermocil

Used to auto-open terminals in iTerm for quicker development. **Only run these commands after successfully running docker compose.**

1. Install [iTermocil](https://github.com/TomAnthony/itermocil) by running these commands in terminal:

```sh
brew install TomAnthony/brews/itermocil
mkdir ~/.itermocil
cd <proj-root-path> # replace this with your project directory
cp itermocil/dev.yml ~/.itermocil/dev.yml
code ~/.itermocil/dev.yml
```

2. Replace all `<proj-root-path>` with your project's path (see path to current dir with `pwd`)

3. Run `itermocil dev` -- which should successfully attach to running docker containers!

**Note:** there won't be any output because `docker compose attach` only shows ongoing output.

### Troubleshooting

If you encounter the below error:

```
Error: Invalid formula: /usr/local/Homebrew/Library/Taps/tomanthony/homebrew-brews/Formula/squid.rb
squid: Calling `sha256 "digest" => :tag` in a bottle block is disabled! Use `brew style --fix` on the formula to update the style or use `sha256 tag: "digest"` instead.
Please report this issue to the tomanthony/brews tap (not Homebrew/brew or Homebrew/core), or even better, submit a PR to fix it:
  /usr/local/Homebrew/Library/Taps/tomanthony/homebrew-brews/Formula/squid.rb:9

Error: Cannot tap tomanthony/brews: invalid syntax in tap!
```

[Try building the formula from sources:](https://github.com/TomAnthony/itermocil/issues/117#issuecomment-874879053)

```
git clone git@github.com:TomAnthony/homebrew-brews.git
cd homebrew-brews/
brew style --fix Formula
brew install --build-from-source Formula/itermocil.rb
mkdir ~/.itermocil # Continue with steps from above
```

## Debugging with Pytest

**⚠️⚠️⚠️ IMPORTANT ⚠️⚠️⚠️**: Whenever you run tests, make sure that your docker containers are running (at least the PostgreSQL one).

###  In Docker Container

To run tests without breakpoints, run this command:

```sh
# Run tests
docker compose exec backend-api pytest # [options] <path-to-test-file>

# [options]
# -rP - print all stdout at the end
# -s - print stdout in order
```

To run tests **with breakpoints** in VSCode, you need some extra steps:

1. to set a breakpoint → `import debugpy` and add `debugpy.breakpoint()` to your desired location
2. run the above command
3. go to VSCode's "Run and Debug" panel → select the `Pytest: Attach to Docker` option from the dropdown
4. click "Play"

VSCode should now stop execution at the breakpoint!

### In VSCode

([per this link](https://github.com/python-poetry/poetry/issues/5354#issuecomment-1179074941))

First, set a breakpoint → hover over the line numbers and click on the red dot 🔴

#### Specific Tests

1. navigate to "Testing" in the side panel
2. right click and click on "Debug Test" (**do not click on "Run" Test**)

If the tests aren't showing up in the "Testing" panel, try:

- refreshing tests - `Cmd + Shift + P` → Test: Refresh Tests
- delete `.pytest_cache` folder and refresh tests
- make sure the filter icon in the Testing panel isn't checked

#### Current Test File

1. navigate to "Run and Debug" in the side panel
2. click on `Pytest: Run Current Test File`
3. make sure the test file you want to run is open & active in VSCode
4. click "Play"

#### All Tests

1. navigate to "Run and Debug" in the side panel
2. click on `Pytest: Run All Tests`
3. click "Play"

#### FastAPI Server (on port 8888)

1. navigate to "Run and Debug" in the side panel
2. select the `Debug FastAPI (Port 8888)` option from the dropdown
3. click "Play"
4. navigate to `localhost:8888/docs` to access the app!

### In Local Terminal

2 methods:

- activate poetry's virtual environment with `source "$(poetry env info -p)/bin/activate` + run `pytest` command, OR
- run `poetry run pytest`

To set a breakpoint, use `breakpoint()`, which will halt execution and create a `pdb` shell at that breakpoint

To continue to the end, type `exit` into the `pdb` shell

### References

- https://code.visualstudio.com/docs/python/debugging#_remote-script-debugging-with-ssh:~:text=%7D%0A%20%20%5D%0A%7D-,Starting%20debugging,-Now%20that%20an
- https://www.python-engineer.com/posts/debug-python-docker/
- https://stackoverflow.com/questions/64013251/debugging-python-in-docker-container-using-debugpy-and-vs-code-results-in-timeou

## [Migrations](https://medium.com/@johnidouglasmarangon/using-migrations-in-python-sqlalchemy-with-alembic-docker-solution-bd79b219d6a)

```sh
# Make a new migration
docker compose exec backend-api makemigrations "migration name"

# Run all migrations
docker compose exec backend-api migrate

# Downgrade by x (ex. 1) migration
docker compose exec backend-api downgrade -1

# Remove all migrations
docker compose exec backend-api downgrade base
```

## Resources

- [SQLAlchemy Core Syntax](https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_core_selecting_rows.htm)

### Project Templates
- https://github.com/zhanymkanov/fastapi_production_template
- https://medium.com/@tclaitken/setting-up-a-fastapi-app-with-async-sqlalchemy-2-0-pydantic-v2-e6c540be4308
- https://praciano.com.br/fastapi-and-async-sqlalchemy-20-with-pytest-done-right.html

### Poetry

- https://www.pythoncheatsheet.org/blog/python-projects-with-poetry-and-vscode-part-1

| Command                                    | Description                                                  |
| ------------------------------------------ | ------------------------------------------------------------ |
| `poetry new [package-name]`                | Start a new Python Project.                                  |
| `poetry init`                              | Create a *pyproject.toml* file interactively.                |
| `poetry install`                           | Install the packages inside the *pyproject.toml* file and create a virtual environment. |
| `poetry add [package-name]`                | Add a package to a Virtual Environment.                      |
| `poetry add --group dev [package-name]`    | Add a dev package to a Virtual Environment.                  |
| `poetry remove [package-name]`             | Remove a package from a Virtual Environment.                 |
| `poetry remove --group dev [package-name]` | Remove a dev package from a Virtual Environment.             |
| `poetry run [package-name]`                | Run a package in a Virtual Environment. (without being in the virtual env) |

#### Sample Apps

- https://docs.docker.com/compose/samples-for-compose/
- https://github.com/zhanymkanov/fastapi_production_template
- https://github.com/tiangolo/full-stack-fastapi-postgresql

#### Poetry with Docker

- https://github.com/orgs/python-poetry/discussions/1879
- https://stackoverflow.com/questions/53835198/integrating-python-poetry-with-docker
- https://github.com/svx/poetry-fastapi-docker/blob/main/Dockerfile

### Extra Code (for future reference)

**Converting Python datetime object to JSON date string (UTC)**
See [this link](https://stackoverflow.com/questions/10805589/convert-json-date-string-to-python-datetime) for converting the other way around

```python
def convert_datetime_to_utc(dt: datetime) -> str:
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=timezone.utc)

    return dt.strftime("%Y-%m-%dT%H:%M:%S%z")


# Replaces Pydantic v1 json_encoders
# https://github.com/pydantic/pydantic/discussions/7199#discussioncomment-7798544
UTCDateTime = Annotated[
    datetime, PlainSerializer(func=convert_datetime_to_utc, return_type=str)
]
```

## TODOs

### FastAPI

#### Features

- add get user endpoint (get other user)
- Set up testing env + write tests
- Set up email confirmation on sign up
- Add reset password functionality
- implement refresh tokens
- learn about [background tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/) and use one for refresh tokens
- Install + setup redis cache

#### Refactoring

- organize `README.md`

- ~~[use ruff](https://docs.astral.sh/ruff/) instead of isort, black, and flake8~~

- add [pre-commit hooks](https://github.com/astral-sh/ruff-pre-commit?tab=readme-ov-file) (type-checking, linting, formatting)

- add [generic types](https://docs.python.org/3/library/typing.html#user-defined-generic-types) for reusable db methods

  

### Docker

- scripts need `chmod +x` (executable) permissions on host computer to work... which doesn't require permissions from the container's user. is that fine?
- split `compose.yml` file into `compose.yml` and `compose.override.yml` + clean up
  - [working with multiple compose files](https://docs.docker.com/compose/multiple-compose-files/)
  - [compose in prod](https://docs.docker.com/compose/production/)

- [properly use env vars](https://docs.docker.com/compose/environment-variables/) in `compose.*.yml` files
- [handle using secrets](https://docs.docker.com/compose/use-secrets/)
