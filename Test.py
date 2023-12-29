import psutil
import json
import yaml

def read_config(filename='config.yml'):
    with open(filename, 'r') as file:
        config = yaml.safe_load(file)
    return config

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_memory_info():
    memory = psutil.virtual_memory()
    available = round(memory.available/1024.0/1024.0, 1)
    total = round(memory.total/1024.0/1024.0, 1)
    return {
        'available': f"{available} MB",
        'total': f"{total} MB",
        'percent': f"{memory.percent}%"
    }

def get_disk_usage(folder_path='/'):
    disk = psutil.disk_usage(folder_path)
    free = round(disk.free/1024.0/1024.0/1024.0, 1)
    total = round(disk.total/1024.0/1024.0/1024.0, 1)
    return {
        'free': f"{free} GB",
        'total': f"{total} GB",
        'percent': f"{disk.percent}%"
    }

def get_server_stats(config):
    stats = {}

    # Get server-level CPU, memory, and disk information
    stats['Server Level Stats'] = {
        'CPU Info': f"{get_cpu_usage()}%",
        'Memory Info': get_memory_info(),
        'Disk Info': get_disk_usage()
    }

    # App Server Space Summary section
    app_space_summary = {}

    for app_config in config['apps']:
        app_name = app_config['name']
        folder_path = app_config['folder_path']

        # Get disk usage for the app
        app_disk_stats = get_disk_usage(folder_path)

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
    
