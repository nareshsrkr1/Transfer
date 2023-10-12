import os
import pyodbc
import threading
import subprocess
import time

# Function to send an event to an Autosys job
def send_event(job_name, event_type):
    send_event_command = f"sendevent -E {event_type} -J {job_name}"
    subprocess.run(send_event_command, shell=True)

# Function to check the status of an Autosys job
def check_job_status(job_name):
    autostatus_command = f"autostatus -J {job_name}"
    result = subprocess.run(autostatus_command, shell=True, capture_output=True, text=True)
    status_output = result.stdout
    return status_output

# Function to set the profile based on the user (Unix username)
def set_profile(username):
    if username == "prod":
        profile = "/opt/autosys.pb3"
    else:
        profile = "/opt/autosys.ub3"
    return profile

# Function to invoke the shell script to set the profile
def invoke_profile_script(profile):
    subprocess.run(f"source {profile}", shell=True)

# Function to execute a job (placeholder for your job execution logic)
def execute_job(job_id, job_type, job_name):
    print(f"Executing Job {job_id} ({job_type})")
    # Here, you can replace this with actual job execution commands
    # e.g., subprocess.run(['command_to_execute', job_name])

# Database connection settings
server = 'YourServerName'
database = 'YourDatabaseName'
username = 'YourUsername'
password = 'YourPassword'
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Get the current Unix username
user = os.getlogin()

# Set the profile based on the user (Unix username)
profile = set_profile(user)

# Invoke the shell script to set the profile
invoke_profile_script(profile)

# Connect to the database
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

# Query the AutosysJobs table to retrieve job information, including the event to send and dependencies
cursor.execute("SELECT JobID, JobType, ExecutionOrder, DependsOn, EventToSend FROM AutosysJobs ORDER BY ExecutionOrder")
job_info = cursor.fetchall()

# Close the cursor and connection
cursor.close()
conn.close()

# Create and start threads for jobs
threads = []

# Dictionary to store job statuses
job_statuses = {}

for job_id, job_type, execution_order, depends_on, event_type in job_info:
    job_statuses[job_id] = "PENDING"

def check_dependencies_completed(job_id, depends_on):
    while job_statuses[depends_on] != "SUCCESS":
        time.sleep(5)

    job_statuses[job_id] = "PENDING"

# Start threads to check dependencies and execute jobs
for job_id, job_type, execution_order, depends_on, event_type in job_info:
    if not depends_on:
        # This job has no dependency, start it
        send_event(job_id, event_type)
        job_thread = threading.Thread(target=execute_job, args=(job_id, job_type, job_id))
        job_statuses[job_id] = "PENDING"
        job_thread.start()
    else:
        # This job has a dependency, check if the dependency is successful
        dependency_check_thread = threading.Thread(target=check_dependencies_completed, args=(job_id, depends_on))
        dependency_check_thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()

# The rest of your script continues here...
