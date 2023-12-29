import psutil
import json
import yaml

def read_config(filename='config.yml'):
    with open(filename, 'r') as file:
        config = yaml.safe_load(file)
    return config

def get_cpu_usage():
    return psutil.cpu_percent(interval=1, percpu=True)

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

def get_process_info(process):
    try:
        process_exe = psutil.Process(process['pid']).exe()
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        process_exe = "N/A"
    return {
        'pid': process['pid'],
        'name': process['name'],
        'username': process['username'],
        'cpu_percent': f"{process['cpu_percent']}%",
        'exe': process_exe
    }

def get_top_cpu_user_id():
    processes = psutil.process_iter(['pid', 'name', 'username', 'cpu_percent'])
    user_processes = [p.info for p in processes if p.info['username'] != '']
    if not user_processes:
        return None
    sorted_user_processes = sorted(user_processes, key=lambda x: x['cpu_percent'], reverse=True)
    return sorted_user_processes[0]['username']

def get_top_cpu_processes(user_id, num_processes=10):
    processes = psutil.process_iter(['pid', 'name', 'username', 'cpu_percent'])
    user_processes = [p.info for p in processes if p.info['username'] == user_id]
    sorted_user_processes = sorted(user_processes, key=lambda x: x['cpu_percent'], reverse=True)[:num_processes]
    return [get_process_info(process) for process in sorted_user_processes]

def get_server_stats(config):
    stats = {}

    # Get server-level CPU and memory information
    cpu_stats = get_cpu_usage()
    
    # Determine the top CPU user ID
    top_cpu_user_id = config['server'].get('top_cpu_user_id', '')
    if not top_cpu_user_id:
        top_cpu_user_id = get_top_cpu_user_id()

    # Limit the number of top CPU processes to 10
    top_cpu_processes = get_top_cpu_processes(top_cpu_user_id, num_processes=10)

    stats['Server Level Stats'] = {
        'CPU Info': f"{cpu_stats}%",  # Display overall CPU usage
        'Memory Info': get_memory_info(),
        'Mounts': {},
        'Top CPU User ID': top_cpu_user_id,
        'Top CPU Processes': top_cpu_processes
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

def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path, followlinks=True):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.exists(filepath):  # Check if the file or symlink target exists
                total_size += os.path.getsize(filepath)
    return total_size / (2**30)  # Convert to GB

def get_top_files(folder_path, num_files=5):
    files_info = []
    for dirpath, dirnames, filenames in os.walk(folder_path, followlinks=True):
        file_sizes = [(os.path.join(dirpath, filename), os.path.getsize(os.path.join(dirpath, filename))) for filename in filenames]
        file_sizes.sort(key=lambda x: x[1], reverse=True)
        top_files = file_sizes[:num_files]
        files_info.extend(top_files)
    return files_info

def get_top_folder_sizes(base_path, num_folders=10):
    folder_sizes = []

    for dirpath, dirnames, filenames in os.walk(base_path, followlinks=True):
        folder_size = sum(os.path.getsize(os.path.join(dirpath, filename)) for filename in filenames)
        folder_sizes.append((dirpath, folder_size))

    # Sort folders based on size in descending order
    sorted_folders = sorted(folder_sizes, key=lambda x: x[1], reverse=True)

    # Get the top N folders
    top_folders = sorted_folders[:num_folders]

    # Convert sizes to GB
    top_folders_in_gb = [(folder[0], folder[1] / (2**30)) for folder in top_folders]

    return top_folders_in_gb

def get_app_server_space(config):
    app_space_info = {}

    for app_config in config['app_servers']:
        app_name = app_config['name']
        app_paths = app_config['paths']
        num_files_to_display = app_config.get('num_files_to_display', 5)
        num_folders_to_display = app_config.get('num_folders_to_display', 10)

        # Find services associated with the app
        app_services = next((service['services'] for service in config.get('app_services', []) if service['name'] == app_name), [])

        app_space_info[app_name] = {}

        for path_config in app_paths:
            path_name = path_config['name']
            path = path_config['path']

            # Get folder size
            folder_size = get_folder_size(path)

            # Get top N most occupied files
            top_files = get_top_files(path, num_files=num_files_to_display)

            # Get top N most occupied folders
            top_folders = get_top_folder_sizes(path, num_folders=num_folders_to_display)

            # Add information to the app_space_info dictionary
            app_space_info[app_name][path_name] = {
                'folder_size': folder_size,
                'top_files': [{'file': file[0], 'size': file[1]} for file in top_files],
                'top_folders': [{'folder': folder[0], 'size': folder[1]} for folder in top_folders],
                'services': app_services
            }

    return app_space_info

def monitor_services(app_space_info):
    monitored_services = {}

    for app_name, paths_info in app_space_info.items():
        for path_name, path_info in paths_info.items():
            services = path_info.get('services', [])
            for service in services:
                if service not in monitored_services:
                    monitored_services[service] = []

                # Check if the process with the service name is running
                process_running = any(
                    process.info['name'] == service
                    for process in psutil.process_iter(['pid', 'name'])
                )
                monitored_services[service].append({'app': app_name, 'path': path_name, 'status': int(process_running)})

    return monitored_services

if __name__ == "__main__":
    config = read_config()
    server_stats = get_server_stats(config)
    app_space_info = get_app_server_space(config)
    monitored_services = monitor_services(app_space_info)

    # Save server stats to JSON
    save_to_json(server_stats, filename='server_stats.json')

    # Save app space info to JSON
    save_to_json(app_space_info, filename='app_space_info.json')

    # Save monitored services to JSON
    save_to_json(monitored_services, filename='monitored_services.json')
        
