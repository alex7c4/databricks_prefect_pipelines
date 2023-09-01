"""Script to build and upload 'pipelines_lib'"""
import os
from pathlib import Path
from pprint import pprint

from databricks.sdk import WorkspaceClient
from dotenv import load_dotenv


load_dotenv()

LOCAL_LIB_PATHS = (
    Path("./dist/databricks_pipelines-0.0.1.tar.gz"),
    Path("./dist/databricks_pipelines-0.0.1-py3-none-any.whl"),
)


def main():
    """Main logic"""
    # Make 'pipelines_lib' wheel
    os.system("make lib")

    workspace_client = WorkspaceClient()

    for f_path in LOCAL_LIB_PATHS:
        print(f"Uploading '{f_path}'")
        with f_path.open(mode="rb") as fileo:
            workspace_client.dbfs.upload(path=f"dbfs:/FileStore/jars/{f_path.name}", src=fileo, overwrite=True)

    pprint(list(workspace_client.dbfs.list(path="dbfs:/FileStore/", recursive=True)), width=150)


if __name__ == "__main__":
    main()
    print("--DONE--")
