"""
Used to access the current running processes.
"""
import psutil

def ps(**kwargs):
    """
    Used to access the current running processes.
"""
    print('/r')
    processes = []
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        try:
            
            process_info = proc.info
            processes.append(f"PID: {process_info['pid']}, Name: {process_info['name']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return "\n".join(processes)
