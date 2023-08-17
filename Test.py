from pyspark.sql import SparkSession

class SparkManager:
    def __init__(self, app_name, db_config):
        self.app_name = app_name
        self.db_config = db_config
        self.spark = self._create_spark_session()

    def _create_spark_session(self):
        return SparkSession.builder \
            .appName(self.app_name) \
            .config("spark.some.config.option", "config_value") \
            .getOrCreate()

    def read_db_config(self):
        return self.db_config
