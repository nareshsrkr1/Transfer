import psutil
import json
import yaml

def read_config(filename='config.yml'):
    with open(filename, 'r') as file:
        config = yaml.safe_load(file)
    return config

# ... (Other functions remain unchanged)

def monitor_services(config):
    monitored_services = {}

    app_services = config.get('app_services', [])

    for app_service in app_services:
        app_name = app_service['name']
        services = app_service.get('services', '').split(',')

        for service in services:
            if service not in monitored_services:
                monitored_services[service] = []

            # Check if the process with the service name is running
            process_running = any(
                process.info['name'] == service
                for process in psutil.process_iter(['pid', 'name'])
            )
            monitored_services[service].append({'app': app_name, 'status': int(process_running)})

    return monitored_services

if __name__ == "__main__":
    config = read_config()
    server_stats = get_server_stats(config)
    monitored_services = monitor_services(config)

    # Save server stats to JSON
    save_to_json(server_stats, filename='server_stats.json')

    # Save monitored services to JSON
    save_to_json(monitored_services, filename='monitored_services.json')
    
