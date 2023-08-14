"""Schemas for expected output and input data for pipelines"""
import pyspark.sql.types as T
from pydantic import BaseModel, Field
from pyspark.sql import DataFrame

from src.pipelines_lib.spark import get_spark


class BaseSchema(BaseModel):
    """Base schema class"""

    class Config:
        """Config for pydantic BaseModel"""

        allow_population_by_field_name = True

    def dict(self, **kwargs):
        """Use `by_alias=True` for all to dict conversion"""
        return super().dict(by_alias=True, **kwargs)

    @classmethod
    def spark_schema(cls) -> T.StructType:
        """Make spark schema from extra `spark_type` fields"""
        schema = T.StructType()
        for _, field_info in cls.__fields__.items():
            data_type = field_info.field_info.extra.get("spark_type")
            if not data_type:
                raise ValueError("Spark data type is not provided (no field `spark_type`)")
            schema.add(field=field_info.alias, data_type=data_type)
        return schema

    def dummy_df(self) -> DataFrame:
        """Make dummy DF from provided values"""
        result_df: DataFrame = get_spark().createDataFrame(data=[self.dict], schema=self.spark_schema())
        return result_df


class PopulationVsPriceSchema(BaseSchema):
    """Schema description for raw Population Vs PriceSchema data"""

    rank_2014: int = Field(alias="2014 rank", default=111, spark_type=T.IntegerType())
    city: str = Field(alias="City", default="city", spark_type=T.StringType())
    state: str = Field(alias="State", default="state", spark_type=T.StringType())
    state_code: str = Field(alias="State Code", default="state code", spark_type=T.StringType())
    pop_est_2014: int = Field(alias="2014 Population estimate", default=12345, spark_type=T.LongType())
    med_sales_pr_2015: float = Field(alias="2015 median sales price", default=123.45, spark_type=T.FloatType())


class PopulationVsPriceProcessedSchema(BaseSchema):
    """Schema description for processed Population Vs PriceSchema data"""

    state_code: str = Field(default="state code", spark_type=T.StringType())
    med_sales_pr_2015_avg: float = Field(alias="2015_median_sales_price_avg", default=123.45, spark_type=T.FloatType())
