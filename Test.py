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

def get_disk_usage(mount_path):
    disk = psutil.disk_usage(mount_path)
    free = round(disk.free/1024.0/1024.0/1024.0, 1)
    used = round(disk.used/1024.0/1024.0/1024.0, 1)
    total = round(disk.total/1024.0/1024.0/1024.0, 1)
    return {
        'free': f"{free} GB",
        'used': f"{used} GB",
        'total': f"{total} GB",
        'percent': f"{disk.percent}%"
    }

def get_server_stats(config):
    stats = {}

    # Get server-level CPU and memory information
    stats['Server Level Stats'] = {
        'CPU Info': f"{get_cpu_usage()}%",
        'Memory Info': get_memory_info(),
        'Mounts': {}
    }

    # Iterate through mounts in the configuration
    for mount_path in config['server']['mounts']:
        # Get disk usage for the mount
        mount_disk_stats = get_disk_usage(mount_path)

        # Add mount disk usage to the stats
        stats['Server Level Stats']['Mounts'][mount_path] = {
            'path': mount_path,
            'disk_usage': mount_disk_stats
        }

    return stats

def save_to_json(data, filename='server_stats.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    config = read_config()
    server_stats = get_server_stats(config)
    save_to_json(server_stats)
    
