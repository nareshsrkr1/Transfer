import os
import psutil
import pandas as pd
from configparser import ConfigParser
from sqlalchemy import create_engine

def read_config():
    config = ConfigParser()
    config.read('config.ini')
    return config['Database']

def get_top_n_largest(path, n=5):
    # Get the top N largest folders/files in the specified path
    top_n = []
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            full_path = os.path.join(root, name)
            size = os.path.getsize(full_path)
            top_n.append((full_path, size))

        for name in dirs:
            full_path = os.path.join(root, name)
            size = sum(os.path.getsize(os.path.join(dirpath, filename)) for dirpath, dirnames, filenames in os.walk(full_path) for filename in filenames)
            top_n.append((full_path, size))

    top_n.sort(key=lambda x: x[1], reverse=True)
    return top_n[:n]

def collect_and_insert():
    db_config = read_config()

    cpu_usage = get_cpu_usage()
    cpu_df = pd.DataFrame(cpu_usage, columns=[f'Core_{i}' for i in range(len(cpu_usage))])

    memory_usage = get_memory_usage()
    memory_df = pd.DataFrame([memory_usage])

    disk_usage = get_disk_usage()
    disk_df = pd.DataFrame(disk_usage).T

    network_stats = get_network_stats()
    network_df = pd.DataFrame(network_stats).T

    result_df = pd.concat([cpu_df, memory_df, disk_df, network_df], axis=1)

    # Connect to the database and insert data
    engine = create_engine(f"{db_config['engine']}://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")
    result_df.to_sql('server_stats', con=engine, if_exists='replace', index=False)

    # Get and print the top N largest folders/files on a specific path (replace 'YOUR_PATH' with the desired path)
    top_n = get_top_n_largest('YOUR_PATH', n=5)
    print(f"\nTop {len(top_n)} Largest Folders/Files:")
    for item in top_n:
        print(f"{item[0]}: {item[1]} bytes")

if __name__ == "__main__":
    collect_and_insert()
