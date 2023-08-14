"""Module with Spark related helpers"""
from pyspark.sql import SparkSession


def get_spark() -> SparkSession:
    """Return SparkSession"""
    return SparkSession.builder.getOrCreate()
