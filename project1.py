import psutil
import time

def get_system_data():
    """
    Fetch real-time system data including CPU usage, memory usage, and process details.
    """
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent

    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
        try:
            process_info = {
                'pid': proc.info['pid'],
                'name': proc.info['name'],
                'cpu_percent': proc.info['cpu_percent'],
                'memory_usage': proc.info['memory_info'].rss / (1024 * 1024)  # Convert to MB
            }
            processes.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    return {
        'cpu_usage': cpu_usage,
        'memory_usage': memory_usage,
        'processes': processes
    }

# Example usage
if __name__ == "__main__":
    while True:
        data = get_system_data()
        print("CPU Usage:", data['cpu_usage'])
        print("Memory Usage:", data['memory_usage'])
        print("Processes:", data['processes'])
        time.sleep(1)