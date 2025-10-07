# process_management.py
# A script to demonstrate process management in Python using the os module.

import os
import sys
import time
import subprocess

# --- Task 1: Process Creation Utility ---
def create_child_processes(n):
    """
    Creates N child processes. Each child prints its PID and its parent's PID.
    The parent process waits for all children to complete.
    """
    print(f"\n--- Task 1: Creating {n} Child Processes ---")
    parent_pid = os.getpid()
    print(f"Parent Process PID: {parent_pid}")
    
    child_pids = []
    for i in range(n):
        pid = os.fork()
        
        if pid == 0:
            # This is the child process
            child_pid = os.getpid()
            parent_pid_from_child = os.getppid()
            print(
                f"  -> Child-{i+1} [PID: {child_pid}]: "
                f"My parent is [PID: {parent_pid_from_child}]. Hello! 👋"
            )
            os._exit(0) # Child must exit to avoid creating grandchildren
        else:
            # This is the parent process
            child_pids.append(pid)

    # Parent waits for all children to terminate
    print("Parent is waiting for all children to finish...")
    for pid in child_pids:
        finished_pid, status = os.waitpid(pid, 0)
        print(f"Parent observed child [PID: {finished_pid}] has finished with status: {status}.")
    print("All children have finished. Parent is done. ✅")

# --- Task 2: Command Execution Using exec() ---
def execute_commands_in_children(commands):
    """
    Creates a child process for each command and executes it using os.execvp().
    """
    print(f"\n--- Task 2: Executing Commands in Child Processes ---")
    parent_pid = os.getpid()
    print(f"Parent Process PID: {parent_pid}")
    
    for cmd in commands:
        pid = os.fork()
        
        if pid == 0:
            # Child process
            print(f"\n  -> Child [PID: {os.getpid()}] executing command: '{' '.join(cmd)}'")
            try:
                os.execvp(cmd[0], cmd)
            except FileNotFoundError:
                print(f"Error: Command not found: {cmd[0]}")
                os._exit(1)
        else:
            # Parent process waits for the child to finish
            os.waitpid(pid, 0)
    
    print("\nAll commands executed. Parent is done. ✅")

# --- Task 3: Zombie & Orphan Processes ---
def demonstrate_zombie_process():
    """
    Demonstrates a zombie process by having the parent not wait for the child.
    """
    print("\n--- Task 3a: Demonstrating a Zombie Process ---")
    pid = os.fork()
    
    if pid == 0:
        # Child process
        print(f"Child [PID: {os.getpid()}] is created and will exit immediately.")
        os._exit(0)
    else:
        # Parent process
        print(f"Parent [PID: {os.getpid()}] is NOT waiting for the child.")
        print("The child process has exited, but its entry remains in the process table.")
        print("Run 'ps -el | grep defunct' or 'ps aux | grep Z' in another terminal within 30s to see the zombie. 🧟")
        time.sleep(30) # Keep parent alive to observe zombie state
        os.wait() # Now, reap the child to clean it up
        print("Parent has now reaped the child. Zombie process is gone.")

def demonstrate_orphan_process():
    """
    Demonstrates an orphan process by having the parent exit before the child.
    """
    print("\n--- Task 3b: Demonstrating an Orphan Process ---")
    pid = os.fork()
    
    if pid == 0:
        # Child process
        original_parent_pid = os.getppid()
        print(f"Child [PID: {os.getpid()}] has parent [PID: {original_parent_pid}].")
        print("Child is going to sleep for 5 seconds...")
        time.sleep(5)
        new_parent_pid = os.getppid()
        print(f"Child [PID: {os.getpid()}] woke up.")
        print(f"My original parent [PID: {original_parent_pid}] has exited.")
        print(f"I am an orphan! My new parent is the 'init' process [PID: {new_parent_pid}]. 🧑‍👦")
        os._exit(0)
    else:
        # Parent process
        print(f"Parent [PID: {os.getpid()}] will exit in 1 second, orphaning the child.")
        time.sleep(1)
        # In a real script you'd just exit, but for demonstration, 
        # we use os._exit to avoid python's cleanup interfering.
        os._exit(0)

# --- Task 4: Inspecting Process Info from /proc ---
def inspect_proc_info(pid_to_inspect):
    """
    Reads and prints process information from the /proc filesystem.
    """
    print(f"\n--- Task 4: Inspecting /proc for PID: {pid_to_inspect} ---")
    try:
        # Read /proc/[pid]/status
        print("\n[+] From /proc/pid/status:")
        with open(f"/proc/{pid_to_inspect}/status") as f:
            for line in f:
                if line.startswith(("Name:", "State:", "VmSize:")):
                    print(f"  {line.strip()}")

        # Read executable path from /proc/[pid]/exe
        print("\n[+] From /proc/pid/exe:")
        exe_path = os.readlink(f"/proc/{pid_to_inspect}/exe")
        print(f"  Executable Path: {exe_path}")

        # List open file descriptors from /proc/[pid]/fd
        print("\n[+] From /proc/pid/fd:")
        fds = os.listdir(f"/proc/{pid_to_inspect}/fd")
        print(f"  Open File Descriptors: {', '.join(fds)}")
        
    except FileNotFoundError:
        print(f"Error: Process with PID {pid_to_inspect} does not exist.")
    except PermissionError:
        print(f"Error: Permission denied to access /proc/{pid_to_inspect}.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# --- Task 5: Process Prioritization ---
def demonstrate_prioritization():
    """
    Creates CPU-intensive children with different nice values to show scheduling impact.
    Lower nice value = higher priority.
    """
    print("\n--- Task 5: Demonstrating Process Prioritization with nice() ---")
    print("Creating three CPU-intensive children with different priorities...")
    
    priorities = {
        'High Priority': -10, # Requires sudo to set negative nice values
        'Normal Priority': 0,
        'Low Priority': 15
    }
    
    for name, nice_val in priorities.items():
        pid = os.fork()
        if pid == 0:
            # Child process
            try:
                os.nice(nice_val)
                current_nice = os.nice(0) # Get current nice value
                print(f"  -> Child ({name}) [PID: {os.getpid()}] started with nice value: {current_nice}. Starting CPU-bound work...")
                # Simple CPU-intensive task
                count = 0
                for _ in range(300_000_000):
                    count += 1
                print(f"  -> Child ({name}) [PID: {os.getpid()}] finished work. 🎉")
                os._exit(0)
            except PermissionError:
                print(f"  -> Child ({name}): Permission denied to set nice value to {nice_val}. "
                      "Try running the script with 'sudo'. Exiting.")
                os._exit(1)
    
    # Parent waits for all children
    for _ in priorities:
        os.wait()
    
    print("\nAll prioritized children have finished. Observe the finishing order. ✅")

# --- Main Menu ---
def main():
    """Main function to display menu and run tasks."""
    # Start a dummy process in the background to inspect with Task 4
    dummy_process = subprocess.Popen(["sleep", "300"])
    
    while True:
        print("\n" + "="*40)
        print("  Process Management Simulation Menu")
        print("="*40)
        print("1. Create N Child Processes (Task 1)")
        print("2. Execute Commands in Children (Task 2)")
        print("3. Demonstrate Zombie Process (Task 3a)")
        print("4. Demonstrate Orphan Process (Task 3b)")
        print(f"5. Inspect /proc Info (e.g., for dummy process PID: {dummy_process.pid})")
        print("6. Demonstrate Process Prioritization (Task 5)")
        print("7. Exit")
        print("-"*40)
        
        choice = input("Enter your choice [1-7]: ")
        
        if choice == '1':
            try:
                n = int(input("Enter the number of child processes to create: "))
                if n > 0:
                    create_child_processes(n)
                else:
                    print("Please enter a positive number.")
            except ValueError:
                print("Invalid input. Please enter an integer.")
        
        elif choice == '2':
            commands_to_run = [
                ["ls", "-l", "/"],
                ["date"],
                ["whoami"]
            ]
            execute_commands_in_children(commands_to_run)
            
        elif choice == '3':
            demonstrate_zombie_process()
            
        elif choice == '4':
            demonstrate_orphan_process()
            
        elif choice == '5':
            try:
                pid_str = input(f"Enter PID to inspect (default: {dummy_process.pid}): ")
                pid_to_check = int(pid_str) if pid_str else dummy_process.pid
                inspect_proc_info(pid_to_check)
            except ValueError:
                print("Invalid input. Please enter an integer PID.")
                
        elif choice == '6':
            print("Note: Setting high priority (negative nice value) may require root privileges ('sudo python3 process_management.py').")
            demonstrate_prioritization()

        elif choice == '7':
            print("Exiting program.")
            dummy_process.terminate() # Clean up the dummy process
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    if os.name != "posix":
        sys.exit("This script requires a POSIX-compliant OS (like Linux or macOS) and does not run on Windows.")
    main()

