# FastAPI + PostgreSQL Project Starter

## Setup

1. `cp .env.template .env` (do not alter contents of .env.template)
2. `docker compose up -d --build` (first run only)
3. `docker compose exec backend-api migrate`
4. (for VSCode)
   - install python `3.12` and poetry, and run `poetry install` to auto-setup the virtualenv
   - make sure the python interpreter in VSCode is set to the poetry venv

### [TablePlus](https://tableplus.com/)

Connection Fields:

- Host/Socket: `127.0.0.1` (default, leave blank)
- Port: `5555` 
- Password: `changethis`
- Database: `app`

### VSCode Extensions

- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) → should automatically install [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance), [Python Debugger](https://marketplace.visualstudio.com/items?itemName=ms-python.debugpy)

- [Ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff) (linter, code formatter)

- [Mypy Type Checker](https://marketplace.visualstudio.com/items?itemName=ms-python.mypy-type-checker)
- [Even Better TOML](https://marketplace.visualstudio.com/items?itemName=tamasfe.even-better-toml)

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
cp itermocil/dev.yml ~/.itermocil/dev.yml # inside project root dir
itermocil --edit dev
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

## [Migrations (Alembic)](https://medium.com/@johnidouglasmarangon/using-migrations-in-python-sqlalchemy-with-alembic-docker-solution-bd79b219d6a)

```sh
# Make a new migration
docker compose exec backend-api makemigrations "migration name"

# Run all migrations
docker compose exec backend-api migrate

# Downgrade by x (ex. 1) migration
docker compose exec backend-api downgrade -1
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
