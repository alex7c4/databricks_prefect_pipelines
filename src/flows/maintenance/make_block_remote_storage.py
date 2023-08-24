"""Create Prefect Block for flows storage"""
import os

from prefect import filesystems
from pydantic import SecretStr


# Create Block for storing flows
# https://docs.prefect.io/2.11.4/concepts/filesystems/#azure
azure_storage = filesystems.Azure(  # type: ignore
    bucket_path="flows",
    azure_storage_account_name=SecretStr(os.environ.get("AZURE_STORAGE_ACCOUNT_NAME", "")),
    azure_storage_account_key=SecretStr(os.environ.get("AZURE_STORAGE_ACCOUNT_KEY", "")),
)
uuid = azure_storage.save(name="azure-fs", overwrite=True)
print(f"Azure Block created/updated: {uuid}")
