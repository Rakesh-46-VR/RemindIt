import sys
import time
import os
import subprocess
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import psutil

class CodeChangeHandler(FileSystemEventHandler):
    def __init__(self, main_file):
        self.main_file = main_file
        self.last_edit_time = None
        self.is_restarting = False
        self.current_process = None
        self.lock = threading.Lock()

        # Start monitoring in a separate thread
        self.monitor_thread = threading.Thread(target=self.monitor_changes, daemon=True)
        self.monitor_thread.start()

    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            with self.lock:
                self.last_edit_time = time.time()  # Update last edit time

    def monitor_changes(self):
        while True:
            time.sleep(1)
            with self.lock:
                if self.last_edit_time and time.time() - self.last_edit_time >= 4:
                    self.restart_application()
                    self.last_edit_time = None  # Reset after restart

    def restart_application(self):
        if self.is_restarting:
            return

        self.is_restarting = True
        try:
            # Kill current process and its children
            if self.current_process:
                parent = psutil.Process(self.current_process.pid)
                for child in parent.children(recursive=True):
                    child.kill()
                parent.kill()
                self.current_process = None

            # Start new process
            print("\n[Hot Reload] Starting application...")
            self.current_process = subprocess.Popen([sys.executable, self.main_file])

        finally:
            self.is_restarting = False

class HotReloader:
    def __init__(self, main_file, watch_directories=None):
        self.main_file = main_file
        self.watch_directories = watch_directories or [os.path.dirname(os.path.abspath(main_file))]
        self.event_handler = CodeChangeHandler(main_file)
        self.observer = Observer()

    def start(self):
        # Start file watcher
        for directory in self.watch_directories:
            self.observer.schedule(self.event_handler, directory, recursive=True)
        self.observer.start()

        # Start initial application
        self.event_handler.restart_application()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.observer.stop()
        if self.event_handler.current_process:
            self.event_handler.current_process.kill()
        self.observer.join()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python hot_reloader.py <main_python_file> [additional_watch_directories...]")
        sys.exit(1)

    main_file = sys.argv[1]
    watch_dirs = sys.argv[2:] if len(sys.argv) > 2 else None

    reloader = HotReloader(main_file, watch_dirs)
    reloader.start()
