#!/bin/python3

# -*- Author: Ali -*-
# -*- Info: Task Manager with GPU Monitoring -*-

import psutil
import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
import py3nvml

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.theme = "light"  # Default theme is light

        self.create_menu()
        self.create_treeview()

        self.update_process_list()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        theme_menu = tk.Menu(menu_bar, tearoff=0)
        theme_menu.add_command(label="Dark Mode", command=self.switch_to_dark)
        theme_menu.add_command(label="Light Mode", command=self.switch_to_light)
        menu_bar.add_cascade(label="Theme", menu=theme_menu)

    def create_treeview(self):
        self.tree = ttk.Treeview(self.root, columns=("PID", "Name", "CPU (%)", "Memory (%)", "GPU (%)", "VRAM (MB)"))
        self.tree.heading("#1", text="PID")
        self.tree.heading("#2", text="Name", command=lambda: self.sort_by_column(1))
        self.tree.heading("#3", text="CPU (%)", command=lambda: self.sort_by_column(2))
        self.tree.heading("#4", text="Memory (%)", command=lambda: self.sort_by_column(3))
        self.tree.heading("#5", text="GPU (%)", command=lambda: self.sort_by_column(4))
        self.tree.heading("#6", text="VRAM (MB)", command=lambda: self.sort_by_column(5))
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.bind("<Button-3>", self.show_context_menu)

    def update_process_list(self):
        self.tree.delete(*self.tree.get_children())

        for process in psutil.process_iter(attrs=["pid", "name", "cpu_percent", "memory_percent"]):
            try:
                gpu_percent, vram = self.get_gpu_info(process.info["pid"])
            except Exception:
                gpu_percent, vram = 0.0, 0

            self.tree.insert("", "end", values=(
                process.info["pid"],
                process.info["name"],
                round(process.info["cpu_percent"], 2),
                round(process.info["memory_percent"], 2),
                round(gpu_percent, 2),
                vram
            ))

        self.root.after(1000, self.update_process_list)  # Update every second

    def get_gpu_info(self, pid):
        try:
            py3nvml.nvmlInit()
            device_count = py3nvml.nvmlDeviceGetCount()

            for i in range(device_count):
                device = py3nvml.nvmlDeviceGetHandleByIndex(i)
                process_info = py3nvml.nvmlDeviceGetComputeRunningProcesses(device)

                for process in process_info:
                    if process.pid == pid:
                        gpu_percent = process.usedGpu / 10.0
                        vram = py3nvml.nvmlDeviceGetMemoryInfo(device).used / 1024**2
                        py3nvml.nvmlShutdown()
                        return gpu_percent, vram
        except Exception:
            pass

        return 0.0, 0

    def show_context_menu(self, event):
        item = self.tree.selection()[0]
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Terminate", command=lambda: self.terminate_process(item))
        menu.post(event.x_root, event.y_root)

    def terminate_process(self, item):
        pid = self.tree.item(item, "values")[0]
        try:
            process = psutil.Process(pid)
            process.terminate()
        except psutil.NoSuchProcess:
            pass
        except psutil.AccessDenied:
            messagebox.showerror("Error", "Access denied: Unable to terminate the process.")

    def sort_by_column(self, col_idx):
        data = [(self.tree.set(child, col_idx), child) for child in self.tree.get_children("")]
        data.sort(reverse=True)
        for idx, item in enumerate(data):
            self.tree.move(item[1], "", idx)

    def switch_to_dark(self):
        self.theme = "dark"
        self.root.configure(bg="black")
        self.tree.configure(style="Dark.Treeview")
        self.root.option_add("*TButton*background", "black")
        self.root.option_add("*TButton*foreground", "white")

    def switch_to_light(self):
        self.theme = "light"
        self.root.configure(bg="white")
        self.tree.configure(style="Light.Treeview")
        self.root.option_add("*TButton*background", "white")
        self.root.option_add("*TButton*foreground", "black")

def main():
    root = tk.Tk()
    root.geometry("800x600")
    root.configure(bg="white")

    style = ttk.Style(root)
    style.configure("Dark.Treeview", background="black", foreground="white")
    style.configure("Light.Treeview", background="white", foreground="black")

    app = TaskManagerApp(root)
    root.protocol("WM_DELETE_WINDOW", root.destroy)

    title_font = font.Font(family="Helvetica", size=18, weight="bold")
    title_label = tk.Label(root, text="Task Manager", font=title_font, bg="white")
    title_label.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
