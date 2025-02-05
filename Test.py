[service1]
name = My Flask Service 1
pid_file = /tmp/service1.pid
start_command = nohup python3 /path/to/service1.py & echo $! > /tmp/service1.pid

[service2]
name = My Flask Service 2
pid_file = /tmp/service2.pid
start_command = nohup python3 /path/to/service2.py & echo $! > /tmp/service2.pid

[service3]
name = My Flask Service 3
pid_file = /tmp/service3.pid
start_command = nohup python3 /path/to/service3.py & echo $! > /tmp/service3.pid

[service4]
name = My Flask Service 4
pid_file = /tmp/service4.pid
start_command = nohup python3 /path/to/service4.py & echo $! > /tmp/service4.pid

Here’s a solution that allows you to control your Flask services via a configuration file (python_service_monitor_config.ini). The script will check for each service’s process ID (PID), and if it is not running, it will restart the service using the command specified in the config file.


---

Step 1: Create the Configuration File

Create a file named python_service_monitor_config.ini with the following structure:

[service1]
name = My Flask Service 1
pid_file = /tmp/service1.pid
start_command = nohup python3 /path/to/service1.py & echo $! > /tmp/service1.pid

[service2]
name = My Flask Service 2
pid_file = /tmp/service2.pid
start_command = nohup python3 /path/to/service2.py & echo $! > /tmp/service2.pid

[service3]
name = My Flask Service 3
pid_file = /tmp/service3.pid
start_command = nohup python3 /path/to/service3.py & echo $! > /tmp/service3.pid

[service4]
name = My Flask Service 4
pid_file = /tmp/service4.pid
start_command = nohup python3 /path/to/service4.py & echo $! > /tmp/service4.pid

pid_file: Stores the process ID for each service.

start_command: Command to restart the service.



---

Step 2: Create the Monitoring Script

Create a Python script to check the PIDs and restart services if necessary.

service_monitor.py

import os
import time
import configparser
import psutil

CONFIG_FILE = "python_service_monitor_config.ini"

def read_config():
    """Read the service configuration file."""
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config

def is_process_running(pid):
    """Check if a process is running given a PID."""
    try:
        return psutil.pid_exists(int(pid))
    except (ValueError, psutil.NoSuchProcess):
        return False

def restart_service(service_name, pid_file, start_command):
    """Restart the service and update the PID file."""
    print(f"Restarting {service_name}...")

    # Start the service and update the PID file
    os.system(start_command)

def monitor_services():
    """Monitor all services and restart if necessary."""
    config = read_config()

    while True:
        for service in config.sections():
            pid_file = config[service].get("pid_file")
            start_command = config[service].get("start_command")
            service_name = config[service].get("name", service)

            # Check if PID file exists and get the PID
            if os.path.exists(pid_file):
                with open(pid_file, "r") as f:
                    pid = f.read().strip()
            else:
                pid = None

            # Restart service if not running
            if not pid or not is_process_running(pid):
                restart_service(service_name, pid_file, start_command)

        time.sleep(30)  # Check every 30 seconds

if __name__ == "__main__":
    monitor_services()


---

Step 3: Running the Monitoring Script

Run the monitoring script in the background:

nohup python3 service_monitor.py &

This will continuously check if the services are running and restart them if needed.


---

How It Works

1. The script reads the python_service_monitor_config.ini file.


2. It checks if the PID in the pid_file exists.


3. If the process is not running, it restarts the service using start_command.


4. The start_command writes a new PID to pid_file after restarting.




---

Advantages of This Approach

✅ Configurable – Easily add/remove services via the config file.
✅ PID-based Monitoring – Ensures proper tracking of process status.
✅ Automated Restarts – Restarts only if a service is down.

Would you like any modifications to this setup?

