"""Script to build and upload 'pipelines_lib'"""
# pylint: disable=duplicate-code
import os
from pathlib import Path
from pprint import pprint

from databricks.sdk import WorkspaceClient
from dotenv import load_dotenv


load_dotenv()

LOCAL_WHL_PATH = Path("./dist/databricks_pipelines-0.0.1.tar.gz")


def main():
    """Main logic"""
    # Make 'pipelines_lib' wheel
    os.system("make lib")

    workspace_client = WorkspaceClient()

    with LOCAL_WHL_PATH.open(mode="rb") as fileo:
        workspace_client.dbfs.upload(path=f"dbfs:/FileStore/jars/{LOCAL_WHL_PATH.name}", src=fileo, overwrite=True)

    pprint(list(workspace_client.dbfs.list(path="dbfs:/FileStore/", recursive=True)), width=150)


if __name__ == "__main__":
    main()
    print("--DONE--")
