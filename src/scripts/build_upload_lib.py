"""Script to build and upload 'pipelines_lib'"""
# pylint: disable=duplicate-code
import os
from pathlib import Path

from databricks.sdk import WorkspaceClient
from dotenv import load_dotenv


load_dotenv()

LOCAL_WHL_PATH = Path("./dist/databricks_pipelines-0.0.1-py3-none-any.whl")


def main():
    """Main logic"""
    # Make 'pipelines_lib' wheel
    os.system("make lib")

    db_username = os.environ.get("DATABRICKS_USERNAME")
    db_token = os.environ.get("DATABRICKS_TOKEN")
    db_password = os.environ.get("DATABRICKS_PASSWORD")

    if not db_username:
        raise ValueError("Environment variable 'DATABRICKS_USERNAME' is empty.")

    workspace_client = WorkspaceClient(
        host=os.environ.get("DATABRICKS_HOST"),
        username=db_username,
        token=db_token,
        password=db_password,
        auth_type="pat" if db_token else "basic",
    )

    with LOCAL_WHL_PATH.open(mode="rb") as fileo:
        workspace_client.dbfs.upload(path=f"dbfs:/FileStore/jars/{LOCAL_WHL_PATH.name}", src=fileo, overwrite=True)

    print(list(workspace_client.dbfs.list(path="dbfs:/FileStore/", recursive=True)))


if __name__ == "__main__":
    main()
    print("--DONE--")
