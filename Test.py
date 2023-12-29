import os

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
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.exists(filepath):  # Check if the file or symlink target exists
                files_info.append((filepath, os.path.getsize(filepath)))
    files_info.sort(key=lambda x: x[1], reverse=True)
    return files_info[:num_files]

def get_top_folder_sizes(base_path, num_folders=10):
    folder_sizes = []

    for dirpath, dirnames, filenames in os.walk(base_path, followlinks=True):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.exists(filepath):  # Check if the file or symlink target exists
                folder_sizes.append((dirpath, os.path.getsize(filepath)))

    # Sort folders based on size in descending order
    sorted_folders = sorted(folder_sizes, key=lambda x: x[1], reverse=True)

    # Get the top N folders
    top_folders = sorted_folders[:num_folders]

    # Convert sizes to GB
    top_folders_in_gb = [(folder[0], folder[1] / (2**30)) for folder in top_folders]

    return top_folders_in_gb
    
