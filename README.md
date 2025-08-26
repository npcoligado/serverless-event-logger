# Serverless Event Logger

## Tasks
[x] Create public Github repository <br>
[x] Create AWS architecture diagram (via drawio) <br>
[x] Scaffold project's folder structure <br>
[x] Setup venv + initial dependencies using uv (fastapi, mangum, dyntastic, uvicorn, ruff, pytest, moto) <br>
[x] Setup Github actions (dependency installation + lint + unit test) <br>
[x] Create tests for create event endpoint <br>
[x] Implement create event endpoint <br>
[x] Create tests for get event endpoint <br>
[x] Implement get event endpoint <br>
[ ] Create CDK app <br>
[x] Add deployment step in pipeline <br>
[ ] Perform integration testing (via Thunder Client extension in VS Code) <br>
[ ] Update readme


## Setting up local virtual environment
1. Install Python 3.13. Option to manage Python versions using `pyenv`.
2. Install `uv` via `pip install uv` if not yet done.
3. Create virtual environment: `uv venv .venv`.
4. Activate venv: `.venv\Scripts\activate`.
5. Install dependencies: `uv sync`.
6. To add dependencies, execute `uv add <package_name>`. If dependency is optional, add `--group dev`.
