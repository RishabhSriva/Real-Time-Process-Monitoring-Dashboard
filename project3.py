import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import tkinter as tk
from tkinter import ttk
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
class DashboardGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Real-Time Process Monitoring Dashboard")
        self.root.geometry("800x600")

        # CPU and Memory Usage Labels
        self.cpu_label = tk.Label(root, text="CPU Usage: N/A", font=("Arial", 12))
        self.cpu_label.pack(pady=10)

        self.memory_label = tk.Label(root, text="Memory Usage: N/A", font=("Arial", 12))
        self.memory_label.pack(pady=10)

        # Process Table
        self.process_table = ttk.Treeview(root, columns=("PID", "Name", "CPU %", "Memory (MB)"), show="headings")
        self.process_table.heading("PID", text="PID")
        self.process_table.heading("Name", text="Name")
        self.process_table.heading("CPU %", text="CPU %")
        self.process_table.heading("Memory (MB)", text="Memory (MB)")
        self.process_table.pack(fill=tk.BOTH, expand=True)

    def update_labels(self, cpu_usage, memory_usage):
        self.cpu_label.config(text=f"CPU Usage: {cpu_usage}%")
        self.memory_label.config(text=f"Memory Usage: {memory_usage}%")

    def update_process_table(self, processes):
        # Clear existing rows
        for row in self.process_table.get_children():
            self.process_table.delete(row)

        # Insert new rows
        for proc in processes:
            self.process_table.insert("", "end", values=(
                proc['pid'], proc['name'], f"{proc['cpu_percent']:.2f}", f"{proc['memory_usage']:.2f}"
            ))

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    dashboard = DashboardGUI(root)
    root.mainloop()
class DashboardGUIWithCharts(DashboardGUI):
    def __init__(self, root):
        super().__init__(root)

        # Add Matplotlib figure for CPU and Memory charts
        self.figure, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().pack(pady=10)

        self.cpu_data = []
        self.memory_data = []

    def update_charts(self, cpu_usage, memory_usage):
        # Update data
        self.cpu_data.append(cpu_usage)
        self.memory_data.append(memory_usage)

        # Limit data points to the last 20 seconds
        if len(self.cpu_data) > 20:
            self.cpu_data.pop(0)
            self.memory_data.pop(0)

        # Clear previous plot
        self.ax.clear()

        # Plot new data
        self.ax.plot(self.cpu_data, label="CPU Usage (%)", color="blue")
        self.ax.plot(self.memory_data, label="Memory Usage (%)", color="green")
        self.ax.legend()
        self.ax.set_ylim(0, 100)
        self.ax.set_title("System Resource Usage")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Usage (%)")

        # Redraw canvas
        self.canvas.draw()

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    dashboard = DashboardGUIWithCharts(root)
    root.mainloop()