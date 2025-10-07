"""
SYSTEM STARTUP SIMULATION (Assignment 2)
Author : Ashmita
Course : Operating Systems Lab
File   : system_startup.py

Objective:
Simulate system startup, process creation, and termination using Python.
Processes log their start and end times to a log file using multiprocessing and logging modules.
"""

import multiprocessing
import time
import logging
import os
import platform

# ---------- Sub-Task 1: Initialize Logging ----------
# Log file will be created in the same directory
log_file = os.path.join(os.path.dirname(__file__), 'process_log.txt')

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(processName)s - %(message)s'
)

# ---------- Sub-Task 2: Define Dummy Process Task ----------
def system_process(task_name):
    """
    Simulates a system process task.
    Logs start and end with timestamps.
    """
    logging.info(f"{task_name} started")
    time.sleep(2)  # Simulate process workload
    logging.info(f"{task_name} ended")

# ---------- Sub-Task 3: Create and Start Processes ----------
if __name__ == '__main__':
    print("System Starting...\n")

    # Create multiple processes
    processes = []
    for i in range(1, 3):  # At least two processes
        p = multiprocessing.Process(target=system_process, args=(f'Process-{i}',))
        p.start()
        processes.append(p)

    # ---------- Sub-Task 4: Ensure Proper Termination ----------
    for p in processes:
        p.join()

    print("System Shutdown.\n")
    print(f"Process log created at: {log_file}")
