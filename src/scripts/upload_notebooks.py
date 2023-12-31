"""Script to upload pipelines to Databricks"""
from pathlib import Path

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.workspace import ImportFormat, Language
from dotenv import load_dotenv


load_dotenv()

PIPELINES_PATH = Path("src/pipelines")


def main():
    """Main logic"""
    workspace_client = WorkspaceClient()

    # get all PY-files under pipelines dir
    py_files = PIPELINES_PATH.rglob("*.py")
    # prepare future Databricks' directory full path
    py_files_dirs = [(Path("/master") / x.parent.relative_to(PIPELINES_PATH), x) for x in py_files]

    # create directory in databricks
    for db_dir in {x[0] for x in py_files_dirs}:
        # db_dir_path = f"/Users/{db_username}/{pipeline_dir}"
        print(f"Creating remote directory: '{db_dir}'")
        workspace_client.workspace.mkdirs(path=db_dir.as_posix())

    # upload notebook
    for db_dir, local_file_path in py_files_dirs:
        print(f"Uploading: '{local_file_path}'")
        workspace_client.workspace.upload(
            path=(db_dir / local_file_path.stem).as_posix(),
            content=local_file_path.read_bytes(),
            format=ImportFormat.SOURCE,
            language=Language.PYTHON,
            overwrite=True,
        )


if __name__ == "__main__":
    main()
    print("--DONE--")
