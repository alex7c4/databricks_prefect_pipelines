"""Some module docstring"""
import os
from pathlib import Path

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.workspace import ImportFormat, Language
from dotenv import load_dotenv


load_dotenv()


w = WorkspaceClient(
    host=os.environ.get("DATABRICKS_HOST"),
    username=os.environ.get("DATABRICKS_USERNAME"),
    password=os.environ.get("DATABRICKS_PASSWORD"),
)

# pipelines = Path("./src/pipelines").rglob("*.py")
# existing = list(workspace.workspace.list(path="/Users/alex-7c4@ya.ru/"))

local_notebook_path = Path("./src/pipelines/some/some_notebook.py")
w.workspace.mkdirs(path="/Users/alex-7c4@ya.ru/test/")

upload_res = w.workspace.upload(
    path="/Users/alex-7c4@ya.ru/test/some_notebook",
    content=local_notebook_path.read_bytes(),
    format=ImportFormat.SOURCE,
    language=Language.PYTHON,
    overwrite=True,
)

print("--DONE--")
