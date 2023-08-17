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


from SparkManager import SparkManager

class SparkDatabaseUtility:
    def __init__(self, spark_manager):
        self.spark_manager = spark_manager

    def execute_sql(self, sql_query):
        result = self.spark_manager.spark.sql(sql_query)
        return result

    def write_to_database(self, data_frame, table_name):
        data_frame.write \
            .format("jdbc") \
            .option("url", self.spark_manager.db_config["url"]) \
            .option("dbtable", table_name) \
            .option("user", self.spark_manager.db_config["user"]) \
            .option("password", self.spark_manager.db_config["password"]) \
            .save()


from SparkManager import SparkManager
from SparkDatabaseUtility import SparkDatabaseUtility

# Define your database configuration
db_config = {
    "url": "jdbc:postgresql://localhost:5432/mydb",
    "user": "username",
    "password": "password"
}

# Create SparkManager instance
spark_manager = SparkManager("MySparkApp", db_config)

# Read database configuration
db_config_read = spark_manager.read_db_config()
print("Database Configuration:", db_config_read)

# Create SparkDatabaseUtility instance
db_utility = SparkDatabaseUtility(spark_manager)

# Execute SQL query
sql_query = "SELECT * FROM mytable"
result_df = db_utility.execute_sql(sql_query)
result_df.show()

# Write data to database
data_to_write = ...
table_name = "mytable"
db_utility.write_to_database(data_to_write, table_name)


