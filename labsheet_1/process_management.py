# -------------------------------------------------------------
# EXPERIMENT TITLE: Process Creation and Management Using Python OS Module
# COURSE CODE: ENCS351 - Operating System
# PROGRAM: B.Tech CSE 
# AUTHOR: Lavya Kumar
# -------------------------------------------------------------

import os
import time
import subprocess

# --------------------------- TASK 1 ---------------------------
# Process Creation Utility

def task1_create_processes(n=3):
    print("\n--- TASK 1: Process Creation Utility ---\n")
    for i in range(n):
        pid = os.fork()
        if pid == 0:
            print(f"Child {i+1}: PID={os.getpid()}, Parent PID={os.getppid()}")
            print(f"Custom Message: Hello from Child {i+1}!")
            os._exit(0)
    for _ in range(n):
        os.wait()
    print("All child processes have finished.\n")


# --------------------------- TASK 2 ---------------------------
# Command Execution Using exec()

def task2_exec_commands():
    print("\n--- TASK 2: Command Execution Using exec() ---\n")
    commands = [["ls"], ["date"], ["ps"]]
    for cmd in commands:
        pid = os.fork()
        if pid == 0:
            print(f"\nExecuting '{cmd[0]}' in child PID={os.getpid()}")
            os.execvp(cmd[0], cmd)
        else:
            os.wait()
    print("All commands executed successfully.\n")


# --------------------------- TASK 3 ---------------------------
# Zombie and Orphan Process Simulation

def task3_zombie_orphan():
    print("\n--- TASK 3: Zombie and Orphan Processes ---\n")

    # ZOMBIE
    pid = os.fork()
    if pid == 0:
        print("Child (Zombie) exiting immediately...")
        os._exit(0)
    else:
        print(f"Parent PID={os.getpid()} sleeping (not waiting)... Check 'ps -el | grep defunct'")
        time.sleep(5)
        os.wait()

    # ORPHAN
    pid = os.fork()
    if pid == 0:
        time.sleep(5)
        print(f"Orphan child running. New Parent PID={os.getppid()}")
        os._exit(0)
    else:
        print("Parent exiting early, child will become orphan...")
        os._exit(0)


# --------------------------- TASK 4 ---------------------------
# Inspecting Process Info from /proc

def task4_proc_inspection():
    print("\n--- TASK 4: Inspecting Process Info from /proc ---\n")
    pid = input("Enter a PID to inspect: ").strip()
    try:
        with open(f"/proc/{pid}/status") as f:
            lines = f.readlines()
            print("Process Info (first 10 lines):")
            print("".join(lines[:10]))

        exe_path = os.readlink(f"/proc/{pid}/exe")
        print(f"\nExecutable Path: {exe_path}")

        fds = os.listdir(f"/proc/{pid}/fd")
        print(f"Open File Descriptors: {fds}\n")

    except Exception as e:
        print(f"Error reading process info: {e}")


# --------------------------- TASK 5 ---------------------------
# Process Prioritization using nice()

def cpu_intensive_task():
    x = 0
    for i in range(10**7):
        x += i

def task5_priority():
    print("\n--- TASK 5: Process Prioritization (nice values) ---\n")
    nice_values = [0, 5, 10]
    for val in nice_values:
        pid = os.fork()
        if pid == 0:
            os.nice(val)
            print(f"Child PID={os.getpid()} running with nice value={val}")
            start = time.time()
            cpu_intensive_task()
            end = time.time()
            print(f"Child PID={os.getpid()} finished in {end - start:.2f}s")
            os._exit(0)
    for _ in range(len(nice_values)):
        os.wait()
    print("\nAll child processes with different priorities have completed.\n")


# --------------------------- MAIN ---------------------------
if __name__ == "__main__":
    print("=== OS LAB EXPERIMENT: PROCESS MANAGEMENT ===")
    print("Select a Task to Run:")
    print("1. Process Creation")
    print("2. Command Execution")
    print("3. Zombie & Orphan Simulation")
    print("4. /proc Inspection")
    print("5. Process Prioritization\n")

    choice = input("Enter task number (1-5): ")

    if choice == "1":
        task1_create_processes()
    elif choice == "2":
        task2_exec_commands()
    elif choice == "3":
        task3_zombie_orphan()
    elif choice == "4":
        task4_proc_inspection()
    elif choice == "5":
        task5_priority()
    else:
        print("Invalid choice.")
