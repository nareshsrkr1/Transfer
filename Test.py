import sqlite3
import json
import yaml

def read_config(filename='config.yml'):
    with open(filename, 'r') as file:
        config = yaml.safe_load(file)
    return config

# ... (Other functions remain unchanged)

def is_process_running(service_name):
    # Use ps command with grep to check if the process is running
    command = f"ps aux | grep {service_name} | grep -v grep"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()

    # Check the return code to determine if the process is running
    return process.returncode == 0

def monitor_services(config):
    monitored_services = []

    app_services = config.get('app_services', [])

    for app_service in app_services:
        app_name = app_service['name']
        services = app_service.get('services', '').split(',')

        for service in services:
            # Check if the process with the service name is running
            process_running = is_process_running(service)
            monitored_services.append({
                'app_name': app_name,
                'service': service,
                'status': int(process_running)
            })

    return monitored_services

def generate_combined_json(config):
    server_stats = get_server_stats(config)
    app_space_info = get_app_server_space(config)
    monitored_services = monitor_services(config)

    combined_json = {
        'server_stats': server_stats,
        'app_space_info': app_space_info,
        'monitored_services': monitored_services
    }

    return combined_json

def create_database_tables(connection):
    cursor = connection.cursor()

    # Create a table for server stats
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS server_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cpu_usage REAL,
            memory_available REAL,
            memory_total REAL,
            memory_percent REAL,
            disk_free REAL,
            disk_total REAL,
            disk_percent REAL
        )
    ''')

    # Create a table for app space info
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS app_space_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            app_name TEXT,
            folder_path TEXT,
            total_size REAL,
            used_size REAL,
            free_size REAL
        )
    ''')

    # Create a table for monitored services
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS monitored_services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            app_name TEXT,
            service TEXT,
            status INTEGER
        )
    ''')

    # Commit the changes
    connection.commit()

def save_to_database(data, db_filename='stats.db'):
    connection = sqlite3.connect(db_filename)

    # Create database tables if they don't exist
    create_database_tables(connection)

    # Insert data into server_stats table
    server_stats = data.get('server_stats', {})
    connection.execute('''
        INSERT INTO server_stats (
            cpu_usage, memory_available, memory_total, memory_percent,
            disk_free, disk_total, disk_percent
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        server_stats.get('cpu_usage', 0),
        server_stats.get('memory_info', {}).get('available', 0),
        server_stats.get('memory_info', {}).get('total', 0),
        server_stats.get('memory_info', {}).get('percent', 0),
        server_stats.get('disk_info', {}).get('free', 0),
        server_stats.get('disk_info', {}).get('total', 0),
        server_stats.get('disk_info', {}).get('percent', 0)
    ))

    # Insert data into app_space_info table
    app_space_info = data.get('app_space_info', {})
    for app_name, space_info in app_space_info.items():
        connection.execute('''
            INSERT INTO app_space_info (
                app_name, folder_path, total_size, used_size, free_size
            ) VALUES (?, ?, ?, ?, ?)
        ''', (
            app_name,
            space_info.get('folder_path', ''),
            space_info.get('total', 0),
            space_info.get('used', 0),
            space_info.get('free', 0)
        ))

    # Insert data into monitored_services table
    monitored_services = data.get('monitored_services', [])
    for service_info in monitored_services:
        connection.execute('''
            INSERT INTO monitored_services (app_name, service, status) VALUES (?, ?, ?)
        ''', (
            service_info.get('app_name', ''),
            service_info.get('service', ''),
            service_info.get('status', 0)
        ))

    # Commit the changes and close the connection
    connection.commit()
    connection.close()

if __name__ == "__main__":
    config = read_config()
    combined_json = generate_combined_json(config)

    # Save combined information to the database
    save_to_database(combined_json)
    
