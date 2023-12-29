import psutil
import json
import yaml

def read_config(filename='config.yml'):
    with open(filename, 'r') as file:
        config = yaml.safe_load(file)
    return config

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_disk_usage(folder_path):
    disk_usage = psutil.disk_usage(folder_path)
    return {
        'total': disk_usage.total / (2**30),  # Convert to GB
        'used': disk_usage.used / (2**30),
        'free': disk_usage.free / (2**30)
    }

def get_server_stats(config):
    stats = {}

    # Get overall CPU usage
    cpu_stats = get_cpu_usage()

    # Include overall CPU usage in the stats
    stats['cpu_usage'] = cpu_stats

    # App Server Space Summary section
    app_space_summary = {}

    for app_config in config['apps']:
        app_name = app_config['name']
        folder_path = app_config['folder_path']

        # Get disk usage for the app
        app_disk_stats = get_disk_usage(folder_path)

        # Include disk usage for each app in the stats
        stats[app_name] = {
            'cpu_usage': None,  # No CPU usage for individual apps
            'disk_usage': app_disk_stats
        }

        # Add app disk usage to the summary
        app_space_summary[app_name] = {
            'total': app_disk_stats['total'],
            'used': app_disk_stats['used'],
            'free': app_disk_stats['free']
        }

    # Add the App Server Space Summary section
    stats['App Server Space Summary'] = app_space_summary

    return stats

def save_to_json(data, filename='server_stats.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    config = read_config()
    server_stats = get_server_stats(config)
    save_to_json(server_stats)
    
