"""Module with Databricks related helpers"""
from unittest.mock import MagicMock


def get_dbutils():
    """Get `dbutils` if in Databricks environment, or just mock if running locally"""

    class Widgets:
        """`dbutils.widgets` methods mock"""

        text = MagicMock()
        get = MagicMock(return_value="")

    class DButils:
        """`dbutils.widgets` mock"""

        widgets = Widgets()

    try:
        from dbruntime import UserNamespaceInitializer  # pylint: disable=unused-import
    except ModuleNotFoundError:
        _dbutils = DButils()
    else:
        from databricks.sdk.runtime import dbutils

        _dbutils = dbutils  # pylint: disable=redefined-variable-type
    return _dbutils
