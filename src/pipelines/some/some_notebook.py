# Databricks notebook source
# MAGIC %fs cp 'dbfs:/FileStore/jars/databr_pipelines-0.0.1-py3-none-any.whl'
# MAGIC 'file:/tmp/databr_pipelines-0.0.1-py3-none-any.whl'

# COMMAND ----------

# MAGIC %pip install --progress-bar=off -U /tmp/databr_pipelines-0.0.1-py3-none-any.whl

# COMMAND ----------

# MAGIC %pip install --force-reinstall --no-deps /tmp/databr_pipelines-0.0.1-py3-none-any.whl

# COMMAND ----------

import pyspark.sql.functions as F
from pyspark.sql import DataFrame

from src.pipelines_lib.databricks import get_dbutils
from src.pipelines_lib.schemas.data_schemas import PopulationVsPriceSchema
from src.pipelines_lib.spark import get_spark


class Config:
    def __init__(self):
        get_dbutils().widgets.text(
            name="source_path",
            defaultValue="dbfs:/databricks-datasets/samples/population-vs-price/data_geo.csv",
        )

        self.source_path = get_dbutils().widgets.get("source_path")
        self.source_df = get_spark().read.csv(
            path=self.source_path, schema=PopulationVsPriceSchema.spark_schema(), header=True, mode="FAILFAST"
        )


# COMMAND ----------


def transform(source_df: DataFrame) -> DataFrame:
    """Main transformation"""
    result_df = (
        source_df
        .groupBy(F.col("State Code").alias("state_code"))
        .agg(
            F.round(F.avg("2015 median sales price"), 2).alias("2015_median_sales_price_avg"),
        )
        .orderBy(F.col("2015_median_sales_price_avg").desc())
    )  # fmt: skip
    return result_df


def write_result(result_df: DataFrame):
    """Imitate DF writing"""
    result_df.show(100, truncate=False)


# COMMAND ----------


def main():
    """Main logic"""
    config = Config()
    result_df = transform(source_df=config.source_df)
    write_result(result_df)


if __name__ == "__main__":
    main()
