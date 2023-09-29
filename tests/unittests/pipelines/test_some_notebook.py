"""Tests for some_notebook pipeline"""
import pytest
from pyspark.sql import SparkSession
from pyspark.testing.utils import assertDataFrameEqual

from src.pipelines.some.some_notebook import transform
from src.pipelines_lib.schemas.data_schemas import PopulationVsPriceProcessedSchema, PopulationVsPriceSchema


@pytest.mark.parametrize(
    ("input_data", "expected_data"),
    [
        (
            [
                PopulationVsPriceSchema(med_sales_pr_2015=100).dict(),
                PopulationVsPriceSchema(med_sales_pr_2015=200).dict(),
            ],
            [PopulationVsPriceProcessedSchema(med_sales_pr_2015_avg=150).dict()],
        ),
    ],
)
def test_some_notebook(spark_session: SparkSession, input_data: list[dict], expected_data: list[dict]):
    """Check `transform` from `some_notebook`"""
    input_df = spark_session.createDataFrame(data=input_data, schema=PopulationVsPriceSchema.spark_schema())
    expected_df = spark_session.createDataFrame(
        data=expected_data, schema=PopulationVsPriceProcessedSchema.spark_schema()
    )
    result_df = transform(source_df=input_df)

    # show
    # result_df.show(100, truncate=False)
    # expected_df.show(100, truncate=False)
    # result_df.printSchema()
    # expected_df.printSchema()

    assertDataFrameEqual(actual=result_df, expected=expected_df)
