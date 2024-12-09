import os
import time
import threading
from datetime import datetime
import json

# Path to save the snapshot file
snapshot_file_path = "snapshot.json"

def load_all_commits():
    """Load all commits from the snapshot file."""
    if os.path.exists(snapshot_file_path):
        try:
            with open(snapshot_file_path, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Error: Snapshot file is corrupted.")
            return []
    return []

def save_snapshot(last_snapshot_time, files_snapshot):
    """Save a new snapshot to the commit history."""
    commit_history = load_all_commits()
    new_commit = {
        "timestamp": last_snapshot_time,
        "files_snapshot": {
            filename: file.last_modified_date.isoformat()
            for filename, file in files_snapshot.items()
        }
    }
    commit_history.append(new_commit)
    with open(snapshot_file_path, 'w') as file:
        json.dump(commit_history, file, indent=4)

def scan_folder(folder_path):
    """Scan the folder and return a dictionary of files."""
    files = {}
    for entry in os.scandir(folder_path):
        if entry.is_file():
            ext = os.path.splitext(entry.name)[1]
            if ext in ['.png', '.jpg']:
                files[entry.name] = ImageFile(entry.path)
            elif ext == '.txt':
                files[entry.name] = TextFile(entry.path)
            elif ext in ['.py', '.java']:
                files[entry.name] = ProgramFile(entry.path)
            else:
                files[entry.name] = File(entry.path)
    return files

# Base File Class
class File:
    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.extension = os.path.splitext(filepath)[1]
        self.creation_date = datetime.fromtimestamp(os.path.getctime(filepath))
        self.last_modified_date = datetime.fromtimestamp(os.path.getmtime(filepath))

    def get_info(self):
        return f"Filename: {self.filename}, Extension: {self.extension}, " \
               f"Created: {self.creation_date}, Last Modified: {self.last_modified_date}"

class ImageFile(File):
    def get_info(self):
        dimensions = "1920x1080"  # Placeholder
        base_info = super().get_info()
        return f"{base_info}, Dimensions: {dimensions}"

class TextFile(File):
    def get_info(self):
        with open(self.filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            word_count = sum(len(line.split()) for line in lines)
            char_count = sum(len(line) for line in lines)
            line_count = len(lines)
        base_info = super().get_info()
        return f"{base_info}, Lines: {line_count}, Words: {word_count}, Characters: {char_count}"

class ProgramFile(File):
    def get_info(self):
        with open(self.filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            class_count = sum(1 for line in lines if "class " in line)
            method_count = sum(1 for line in lines if "def " in line)
            line_count = len(lines)
        base_info = super().get_info()
        return f"{base_info}, Lines: {line_count}, Classes: {class_count}, Methods: {method_count}"

# Global Variables
folder_path = "./save"
files_snapshot = scan_folder(folder_path)
monitoring_active = False
monitoring_event = threading.Event()

def commit():
    """Create a new snapshot."""
    global files_snapshot
    last_snapshot_time = datetime.now().isoformat()
    files_snapshot = scan_folder(folder_path)
    save_snapshot(last_snapshot_time, files_snapshot)
    print(f"Snapshot saved at {last_snapshot_time}")

def info(filename):
    """Print detailed info about a file."""
    file = files_snapshot.get(filename)
    if file:
        print(file.get_info())
    else:
        print(f"File '{filename}' not found.")

def status():
    """Check the status of files since the last snapshot."""
    current_files = scan_folder(folder_path)
    for filename, current_file in current_files.items():
        if filename not in files_snapshot:
            print(f"{filename} is a new file.")
        elif current_file.last_modified_date > files_snapshot[filename].last_modified_date:
            print(f"{filename} has been modified.")
        else:
            print(f"{filename} is unchanged.")
    for filename in files_snapshot:
        if filename not in current_files:
            print(f"{filename} was deleted.")

def history():
    """Display the history of all commits."""
    commits = load_all_commits()
    if not commits:
        print("No commits found.")
        return
    print("Commit History:")
    for index, commit in enumerate(commits, start=1):
        print(f"Commit {index}: {commit['timestamp']}")

def monitor_folder():
    """Monitor the folder for changes in real-time."""
    global monitoring_active
    while monitoring_active:
        time.sleep(5)
        print("\n[Real-Time Monitoring]")
        status()

def monitor_on():
    """Turn on real-time monitoring."""
    global monitoring_active
    if monitoring_active:
        print("Monitoring is already active.")
    else:
        monitoring_active = True
        threading.Thread(target=monitor_folder, daemon=True).start()
        print("Monitoring turned ON.")

def monitor_off():
    """Turn off real-time monitoring."""
    global monitoring_active
    if not monitoring_active:
        print("Monitoring is already inactive.")
    else:
        monitoring_active = False
        print("Monitoring turned OFF.")

def main():
    print("Document Change Detection System")
    print("Commands: commit, info <filename>, status, history, monitor_on, monitor_off, exit")
    while True:
        command = input("Enter command: ").strip().split()
        if not command:
            continue
        action = command[0]
        if action == "commit":
            commit()
        elif action == "info" and len(command) > 1:
            info(command[1])
        elif action == "status":
            status()
        elif action == "history":
            history()
        elif action == "monitor_on":
            monitor_on()
        elif action == "monitor_off":
            monitor_off()
        elif action == "exit":
            monitor_off()
            print("Exiting program.")
            break
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
