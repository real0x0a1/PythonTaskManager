# Task Manager App

This is a simple Task Manager application built with Python and Tkinter. It displays information about running processes on your system, including CPU and memory usage, GPU usage, and VRAM usage. The application updates the process list every second.

## Features

- Displays process information including PID, name, CPU usage, memory usage, GPU usage, and VRAM usage
- Sorts the process list by column when column headers are clicked
- Allows termination of processes by right-clicking on a process and selecting "Terminate"
- Supports both light and dark themes

## Prerequisites

Before running the application, make sure you have the following dependencies installed:

- `psutil`
- `py3nvml`
- `tkinter` (usually comes pre-installed with Python)

## Installation

1. Clone the repository: `git clone https://github.com/real0x0a2/PythonTaskManager.git`
2. Change into the project directory: `cd PythonTaskManager`
3. Install the dependencies: `pip3 install -r requirements.txt`

## Usage

To run the application, execute the following command in the project directory:

```bash
python3 TaskManager.py
```

## Themes

The application supports two themes: light and dark. You can switch between themes using the "Theme" menu in the application menu bar.

## Contributions

Contributions are welcome! If you have any ideas or suggestions to improve the application, feel free to open an issue or submit a pull request.

## Author

- Ali (Real0x0a1)

---
