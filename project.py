import tkinter as tk
from tkinter import ttk
import psutil
import threading

def update_dashboard():
    cpu_label.config(text=f"CPU Usage: {psutil.cpu_percent()}%")
    memory_info = psutil.virtual_memory()
    memory_label.config(text=f"Memory Usage: {memory_info.percent}%")
    
    process_list.delete(*process_list.get_children())
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        process_list.insert("", "end", values=(proc.info['pid'], proc.info['name'], proc.info['cpu_percent']))
    
    root.after(2000, update_dashboard)

root = tk.Tk()
root.title("Real-Time Process Monitoring Dashboard")
root.geometry("600x400")

cpu_label = tk.Label(root, text="CPU Usage: Loading...", font=("Arial", 12))
cpu_label.pack()

memory_label = tk.Label(root, text="Memory Usage: Loading...", font=("Arial", 12))
memory_label.pack()

columns = ("PID", "Process Name", "CPU Usage (%)")
process_list = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    process_list.heading(col, text=col)
    process_list.column(col, width=180)
process_list.pack(expand=True, fill="both")

update_dashboard()
root.mainloop()
