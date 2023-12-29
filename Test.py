import os

def get_top_folder_sizes(base_path, num_folders=10):
    folder_sizes = []

    for dirpath, dirnames, filenames in os.walk(base_path):
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

        app_space_info[app_name] = {}

        for path_config in app_paths:
            path_name = path_config['name']
            path = path_config['path']

            # Get folder size
            folder_size = get_folder_size(path)

            # Get top 5 most occupied files
            top_files = get_top_files(path)

            # Get top 10 occupied folder sizes
            top_folders = get_top_folder_sizes(path, num_folders=10)

            # Add information to the app_space_info dictionary
            app_space_info[app_name][path_name] = {
                'folder_size': folder_size,
                'top_files': [{'file': file[0], 'size': file[1]} for file in top_files],
                'top_folders': [{'folder': folder[0], 'size': folder[1]} for folder in top_folders]
            }

    return app_space_info
    
