import psutil
import json
import yaml
import time

def read_config(filename='config.yml'):
    with open(filename, 'r') as file:
        config = yaml.safe_load(file)
    return config

def get_cpu_usage():
    return psutil.cpu_percent(interval=1, percpu=True)

def get_disk_usage(folder_path):
    disk_usage = psutil.disk_usage(folder_path)
    return {
        'total': disk_usage.total,
        'used': disk_usage.used,
        'free': disk_usage.free
    }

def get_server_stats(config):
    stats = {}

    # Get overall CPU usage
    cpu_stats = get_cpu_usage()

    # Include overall CPU usage in the stats
    stats['cpu_usage'] = cpu_stats

    for app_config in config['apps']:
        app_name = app_config['name']
        folder_path = app_config['folder_path']
        
        # Get CPU usage for the specific app
        app_cpu_stats = cpu_stats if app_name == 'overall' else get_cpu_usage()
        
        # Get disk usage for the app
        app_disk_stats = get_disk_usage(folder_path)

        # Include CPU and disk usage for each app in the stats
        stats[app_name] = {
            'cpu_usage': app_cpu_stats,
            'disk_usage': app_disk_stats
        }

    return stats

def save_to_json(data, filename='server_stats.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    config = read_config()

    while True:
        server_stats = get_server_stats(config)
        save_to_json(server_stats)

        # Adjust the sleep time based on your desired interval
        time.sleep(60)  # Sleep for 60 seconds

if __name__ == "__main__":
    main()
    
