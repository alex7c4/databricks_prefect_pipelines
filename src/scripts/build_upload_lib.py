"""
Build and upload pipelines_lib.

NOTE: NOT WORKING WITH DATABRICKS COMMUNITY.
Upload lib manually with DBFS explorer.
"""
import os
from pathlib import Path

from databricks.sdk import WorkspaceClient
from dotenv import load_dotenv


# Make 'pipelines_lib'
os.system("make lib")

# Upload it
load_dotenv()

workspace = WorkspaceClient(
    host=os.environ.get("DATABRICKS_HOST"),
    username=os.environ.get("DATABRICKS_USERNAME"),
    password=os.environ.get("DATABRICKS_PASSWORD"),
)

loca_whl_path = Path("./dist/databr_pipelines-0.0.1-py3-none-any.whl")


with loca_whl_path.open(mode="rb") as fileo:
    workspace.dbfs.upload(path=f"dbfs:/FileStore/{loca_whl_path.name}", src=fileo, overwrite=True)

print(list(workspace.dbfs.list(path="dbfs:/FileStore/", recursive=True)))
