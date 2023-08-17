import yaml
from SparkManager import SparkManager
from SparkDatabaseUtility import SparkDatabaseUtility

# Read all configurations from YAML file
with open("db_config.yml", "r") as yml_file:
    all_config = yaml.safe_load(yml_file)

# Choose the environment (uat or prd)
environment = "uat"  # Change this to "prd" for production

# Get the environment-specific configuration
environment_config = all_config.get(environment, {})

# Merge common configuration with environment-specific configuration
common_config = all_config.get("common", {})
db_config = {
    "driver_batch_size": common_config.get("driver_batch_size", 100),
    **environment_config
}

# Create SparkManager instance
spark_manager = SparkManager("MySparkApp", db_config)

# ... Rest of the code remains the same ...
