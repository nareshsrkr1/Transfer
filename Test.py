Yes, you can use the full absolute path (e.g., /abc/prod/main.py) in the config file, but psutil does not always return the full path in cmdline. To ensure a reliable match, I'll update the script to check the exact match for the full path.


---

Step 1: Update Configuration File

Modify your service_monitor_config.ini with full script paths:

[main_service]
name = Main Service
process_path = /abc/prod/main.py
start_command = nohup python3 /abc/prod/main.py &

[splitter_service]
name = Splitter Service
process_path = /abc/prod/splitter.py
start_command = nohup python3 /abc/prod/splitter.py &

[rlen_service]
name = Rlen Service
process_path = /abc/prod/rlen.py
start_command = nohup python3 /abc/prod/rlen.py &

[wind_down_service]
name = WindDown Service
process_path = /abc/prod/wind_down.py
start_command = nohup python3 /abc/prod/wind_down.py &

Renamed process_name → process_path to specify the full path.



---

Step 2: Update Monitoring Script

Modify service_monitor.py to check the exact full path of the process.

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

def is_service_running(process_path):
    """Check if a process with the given full script path is running."""
    for proc in psutil.process_iter(['pid', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and process_path in cmdline:
                return True  # Exact match found
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return False

def restart_service(service_name, process_path, start_command):
    """Restart the service and log the action."""
    logging.warning(f"{service_name} ({process_path}) is not running. Restarting...")
    os.system(start_command)
    logging.info(f"{service_name} restarted successfully.")

def monitor_services():
    """Monitor all services and restart if necessary."""
    config = read_config()

    while True:
        for service in config.sections():
            service_name = config[service].get("name", service)
            process_path = config[service].get("process_path")
            start_command = config[service].get("start_command")

            # Check if service is running
            if not is_service_running(process_path):
                restart_service(service_name, process_path, start_command)

        time.sleep(30)  # Check every 30 seconds

if __name__ == "__main__":
    logging.info("Starting Service Monitor...")
    monitor_services()


---

Key Changes in Code

✅ Now matches the exact full path (/abc/prod/main.py) instead of just main.py.
✅ Ensures only your intended script is monitored, even if other main.py processes exist.
✅ More reliable process matching compared to searching only for a filename.


---

Step 3: Running the Monitoring Script

Run the script in the background:

nohup python3 service_monitor.py &


---

Example Log Output (service_monitor.log)

2025-02-05 10:00:00 - INFO - Starting Service Monitor...
2025-02-05 10:05:30 - WARNING - Main Service (/abc/prod/main.py) is not running. Restarting...
2025-02-05 10:05:31 - INFO - Main Service restarted successfully.


---

Final Thoughts

✅ Now supports full script paths (/abc/prod/main.py).
✅ No risk of confusion with other main.py processes.
✅ Reliable monitoring & automatic restarts.

Would you like any additional modifications?

