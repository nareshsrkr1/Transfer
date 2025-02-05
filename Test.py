[main_service]
name = Main Service
process_name = main_service.py
start_command = nohup python3 /path/to/main_service.py &

[splitter_service]
name = Splitter Service
process_name = splitter_service.py
start_command = nohup python3 /path/to/splitter_service.py &

[rlen_service]
name = Rlen Service
process_name = rlen_service.py
start_command = nohup python3 /path/to/rlen_service.py &

[wind_down_service]
name = WindDown Service
process_name = wind_down_service.py
start_command = nohup python3 /path/to/wind_down_service.py &

Here’s the revised solution that does not use PID files. Instead, it checks for the process directly by matching the service name in the system processes. If the service is not running, it logs the failure and restarts it using the start command from the config file.


---

Step 1: Create the Configuration File

Create a file named service_monitor_config.ini with the following structure:

[main_service]
name = Main Service
process_name = main_service.py
start_command = nohup python3 /path/to/main_service.py &

[splitter_service]
name = Splitter Service
process_name = splitter_service.py
start_command = nohup python3 /path/to/splitter_service.py &

[rlen_service]
name = Rlen Service
process_name = rlen_service.py
start_command = nohup python3 /path/to/rlen_service.py &

[wind_down_service]
name = WindDown Service
process_name = wind_down_service.py
start_command = nohup python3 /path/to/wind_down_service.py &

process_name: Name of the running Python script to check.

start_command: Command to restart the service if not running.



---

Step 2: Create the Monitoring Script

service_monitor.py

import os
import time
import logging
import configparser
import psutil

# Configure logging
logging.basicConfig(filename="service_monitor.log", level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

CONFIG_FILE = "service_monitor_config.ini"

def read_config():
    """Read the service configuration file."""
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config

def is_service_running(process_name):
    """Check if a process with the given name is running."""
    for proc in psutil.process_iter(['pid', 'cmdline']):
        try:
            if proc.info['cmdline'] and process_name in ' '.join(proc.info['cmdline']):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return False

def restart_service(service_name, process_name, start_command):
    """Restart the service and log the action."""
    logging.warning(f"{service_name} ({process_name}) is not running. Restarting...")
    os.system(start_command)
    logging.info(f"{service_name} restarted successfully.")

def monitor_services():
    """Monitor all services and restart if necessary."""
    config = read_config()

    while True:
        for service in config.sections():
            service_name = config[service].get("name", service)
            process_name = config[service].get("process_name")
            start_command = config[service].get("start_command")

            # Check if service is running
            if not is_service_running(process_name):
                restart_service(service_name, process_name, start_command)

        time.sleep(30)  # Check every 30 seconds

if __name__ == "__main__":
    logging.info("Starting Service Monitor...")
    monitor_services()


---

Step 3: Running the Monitoring Script

Run the script in the background:

nohup python3 service_monitor.py &

This will continuously check if the services are running and restart them if needed.


---

How It Works

1. Reads service_monitor_config.ini to get the process names and start commands.


2. Checks if the process is running using psutil.process_iter().


3. Logs and restarts the service if it’s not running.


4. Runs in a loop every 30 seconds to monitor and restart services if needed.



Logging Example (service_monitor.log)

2025-02-05 10:00:00 - INFO - Starting Service Monitor...
2025-02-05 10:05:30 - WARNING - Main Service (main_service.py) is not running. Restarting...
2025-02-05 10:05:31 - INFO - Main Service restarted successfully.


---

Advantages of This Approach

✅ No PID files – Directly monitors process names.
✅ Configurable – Easily add/remove services via service_monitor_config.ini.
✅ Automated Logging – Logs failures and restarts for debugging.
✅ Lightweight – Uses psutil for efficient process monitoring.

Would you like any modifications to this setup?

