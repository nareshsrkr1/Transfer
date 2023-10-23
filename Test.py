import pyodbc
import subprocess
import configparser

def send_event(job_name, event_type):
    send_event_command = f"sendevent -E {event_type} -J {job_name}"
    subprocess.run(send_event_command, shell=True)

def execute_jobs_in_order(rows):
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
                    success_state = event_success_states.get(event, "SU")
                    if success_state not in executed_jobs:
                        ready_to_run = False
                        break

            if ready_to_run:
                for job, event in jobs:
                    send_event(job, event)
                    executed_jobs.add(job)
                del job_dict[order]
                break

if __name__ == "__main":
    try:
        config = configparser.ConfigParser()
        config.read("config.ini")
        get_config_file_data = config["AUTOSYS_TRIGGER"]
        autosys_ref = get_config_file_data['autosys_job_table']
        conn = pyodbc.connect(Connection)  # Assuming Connection is defined in Constants
        cursor = conn.cursor()
        cursor.execute("SELECT * from " + autosys_ref)
        rows = cursor.fetchall()

        execute_jobs_in_order(rows)
    except Exception as err:
        print(str(err))
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
