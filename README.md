# FastAPI + PostgreSQL Project Starter

## Setup

1. navigate to project's root directory

2. create a python virtual environment - `python3 -m venv ./.venv`

3. activate the virtualenv - `source .venv/bin/activate` 
   - you should see `(.venv)` to the left of input)
   - running `pip -V` → should print out a path including your project directory

4. install packages with `pip install -r ./requirements/development.txt` ([source](https://www.freecodecamp.org/news/python-requirementstxt-explained/))

5. Run server with `uvicorn src.main:app --reload`



Note: to exit out of the `venv`, type `deactivate`.

### PyCharm

1. Install PyCharm Community Edition (free) from [here](https://www.jetbrains.com/pycharm/download/?section=mac).
2. Run `pip install -r requirements.txt`

#### Keyboard Shortcuts

| Key Combo         | Function           |
| ----------------- | ------------------ |
| `Shift` + `Shift` | open search menu   |
| `Ctrl/Cmd` + `,`  | open settings menu |
#### Plugins
- [Pydantic PyCharm Plugin](https://github.com/koxudaxi/pydantic-pycharm-plugin/)

## Troubleshooting

**Package requirements '...' are not satisfied**

Try to invalidate caches:

1. In the upper menu bar (next to "Edit"), click **File** → **Invalidate Caches**
2. Click **Invalidate and Restart**.

[Source](https://stackoverflow.com/a/55341896/9477827)

## Resources

- https://github.com/zhanymkanov/fastapi_production_template
- https://medium.com/@tclaitken/setting-up-a-fastapi-app-with-async-sqlalchemy-2-0-pydantic-v2-e6c540be4308
- https://praciano.com.br/fastapi-and-async-sqlalchemy-20-with-pytest-done-right.html

