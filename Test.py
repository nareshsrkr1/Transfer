import os
import psutil
import json
import yaml

def read_config(filename='config.yml'):
    with open(filename, 'r') as file:
        config = yaml.safe_load(file)
    return config

def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return total_size / (2**30)  # Convert to GB

def get_top_files(folder_path, num_files=5):
    files_info = []
    for dirpath, dirnames, filenames in os.walk(folder_path):
        file_sizes = [(os.path.join(dirpath, filename), os.path.getsize(os.path.join(dirpath, filename))) for filename in filenames]
        file_sizes.sort(key=lambda x: x[1], reverse=True)
        top_files = file_sizes[:num_files]
        files_info.extend(top_files)
    return files_info

def get_app_server_space(config):
    app_space_info = {}

    for app_config in config['app_servers']:
        app_name = app_config['name']
        app_paths = app_config['paths']

        app_space_info[app_name] = {}

        for path_config in app_paths:
            path_name = path_config['name']
            path = path_config['path']

            # Get folder size
            folder_size = get_folder_size(path)

            # Get top 5 most occupied files
            top_files = get_top_files(path)

            # Add information to the app_space_info dictionary
            app_space_info[app_name][path_name] = {
                'folder_size': folder_size,
                'top_files': [{'file': file[0], 'size': file[1]} for file in top_files]
            }

    return app_space_info

def get_server_stats(config):
    stats = {}

    # ... (existing code for CPU, memory, mounts)

    # Add app server space information
    app_server_space = get_app_server_space(config)
    stats['App Server Space'] = app_server_space

    return stats

# ... (remaining code remains the same)

if __name__ == "__main__":
    config = read_config()
    server_stats = get_server_stats(config)
    save_to_json(server_stats)
    
