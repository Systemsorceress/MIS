import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pyodbc

# Database connection parameters
server = '192.168.1.10'
database = 'MirzaSewtech'
username = 'SuperAdmin'
password = 'SuperAdmin'
table = 'Delivered'

# Directory to be monitored
directory_to_watch = r"C:\Users\Malaika\OneDrive\Desktop\Fscrd\Delivered"

# Database connection function
def connect_to_db():
    connection_string = (
        f'DRIVER={{SQL Server}};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'UID={username};'
        f'PWD={password}'
    )
    return pyodbc.connect(connection_string)

# Event Handler class
class WatcherHandler(FileSystemEventHandler):
    def __init__(self, connection):
        self.connection = connection

    def on_created(self, event):
        if not event.is_directory:
            file_name = os.path.basename(event.src_path)
            status_message = f"{file_name} is delivered"
            self.save_to_database(file_name, status_message)
            print(f"Stored {file_name} in database")  # Print statement when storing in database

    def save_to_database(self, file_name, status_message):
        cursor = self.connection.cursor()
        insert_query = f"""
        INSERT INTO {table} (LotNumber, Status) 
        VALUES (?, ?)
        """
        cursor.execute(insert_query, (file_name, status_message))
        self.connection.commit()

def monitor_directory():
    connection = connect_to_db()
    event_handler = WatcherHandler(connection)
    observer = Observer()
    observer.schedule(event_handler, directory_to_watch, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    monitor_directory()
