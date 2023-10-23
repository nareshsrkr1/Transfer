import pyodbc
import subprocess
import configparser

def send_event(job_name, event_type):
    send_event_command = f"sendevent -E {event_type} -J {job_name}"
    print(f"Executing: {send_event_command}")
    subprocess.run(send_event_command, shell=True)
    print(f"Executed: {job_name}")

def execute_jobs_in_order(rows, event_success_states):
    job_dict = {}
    for row in rows:
        job_id, job_name, exec_order, send_event, comment, dependency_condition = row
        if exec_order not in job_dict:
            job_dict[exec_order] = []
        job_dict[exec_order].append((job_name, send_event))

    executed_jobs = set()

    while job_dict:
        for order, jobs in job_dict.items():
            ready_to_run = True
            for job, event in jobs:
                if job not in executed_jobs and event is not None:
                    event_type, success_state = event.split(':')
                    if success_state not in executed_jobs:
                        ready_to_run = False
                        break

            if ready_to_run:
                print(f"Executing jobs for order {order}:")
                for job, event in jobs:
                    event_type, success_state = event.split(':')
                    send_event(job, event_type)
                    executed_jobs.add(success_state)
                    print(f"Executed: {job}")
                del job_dict[order]
                break

if __name__ == "__main__":
    try:
        config = configparser.ConfigParser()
        config.read("config.ini")
        autosys_trigger_config = config["AUTOSYS_TRIGGER"]

        # Read the event_success_states from the AUTOSYS_TRIGGER section and parse it
        event_success_states = dict(item.split(':') for item in autosys_trigger_config['event_success_states'].split(','))
        autosys_ref = autosys_trigger_config['autosys_job_table']

        conn = pyodbc.connect(Connection)  # Assuming Connection is defined in Constants
        cursor = conn.cursor()
        cursor.execute("SELECT * from " + autosys_ref)
        rows = cursor.fetchall()

        print("Starting AutoSys job execution...")
        execute_jobs_in_order(rows, event_success_states)
        print("AutoSys job execution completed.")
    except Exception as err:
        print(f"Error: {str(err)}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
