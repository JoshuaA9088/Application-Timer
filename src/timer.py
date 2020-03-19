import configparser
import csv
import datetime
import os
import subprocess
import time
import tkinter as tk
from pathlib import Path

import psutil

FMT = "%H:%M:%S"


class ApplicationTimer(object):
    def __init__(self):
        super().__init__()
        self.fields = ("Name", "Department")
        self.title = "Application Timer"

        self.load_config()
        self.makeform()
        self.center()
        self.entries["Name"].icursor(0)
        start_button = tk.Button(
            self.root, text="Start", command=(lambda e=self.entries: self.time_app(e))
        )
        start_button.pack(side=tk.RIGHT, padx=5, pady=5)
        quit_button = tk.Button(self.root, text="Quit", command=self.root.quit)
        quit_button.pack(side=tk.RIGHT, padx=5, pady=5)
        self.root.mainloop()

    def load_config(self):
        config = configparser.ConfigParser()
        home = os.environ["USERPROFILE"]
        my_docs = os.path.join(home, "My Documents")
        my_docs = os.path.join(my_docs, "Timer")
        # ConfigPath = my_docs
        if not os.path.exists(my_docs):
            os.mkdir(my_docs)
        config["DEFAULT"] = {
            "ExecutablePath": r"C:\Windows\System32\notepad.exe",
            "OutputLogPath": os.path.join(my_docs, "timer_log.csv"),
        }

        if os.path.exists(os.path.join(my_docs, "timer.ini")):
            config.read(os.path.join(my_docs, "timer.ini"))
            self.exe_path = config["DEFAULT"]["ExecutablePath"]
            self.log_path = config["DEFAULT"]["OutputLogPath"]
        else:
            self.exe_path = r"C:\Windows\System32\notepad.exe " + os.path.join(
                my_docs, "timer.ini"
            )
            self.log_path = os.path.join(my_docs, "timer_log.csv")
            # f = open(os.path.join(my_docs, "timer.ini"), "w+")
            with open(Path(my_docs, "timer.ini"), "w+") as f:
                config.write(f)

    def makeform(self):
        self.entries = {}
        self.root = tk.Tk()

        for field in self.fields:
            row = tk.Frame(self.root)
            lab = tk.Label(row, width=22, text=field + ": ", anchor="w")
            ent = tk.Entry(row)
            # ent.insert(0, "0")
            row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
            lab.pack(side=tk.LEFT)
            ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
            self.entries[field] = ent

    def center(self):
        self.root.update_idletasks()

        # Tkinter way to find the screen resolution
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        size = tuple(int(_) for _ in self.root.geometry().split("+")[0].split("x"))
        x = screen_width / 2 - size[0] / 2
        y = screen_height / 2 - size[1] / 2

        self.root.geometry("+%d+%d" % (x, y))
        self.root.title(self.title)

    def write_log(self, name, dept):
        if os.path.exists(self.log_path):
            csvData = []
        else:
            csvData = [
                ["Date", "Name", "Department", "Start Time", "End Time", "Elapsed"]
            ]

        date = datetime.datetime.today()
        date = date.strftime("%m-%d-%Y")
        date = str(date)

        elapsed = datetime.datetime.strptime(
            self.end_time, FMT
        ) - datetime.datetime.strptime(self.start_time, FMT)
        elapsed = str(elapsed)

        csvData.append([date, name, dept, self.start_time, self.end_time, elapsed])

        with open(self.log_path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(csvData)

    def time_app(self, ents):
        # Get username field
        name = self.entries["Name"].get()
        dept = self.entries["Department"].get()

        # Kill the main window and run in background
        self.root.destroy()

        # Kill all prior instances of the program.
        for proc in psutil.process_iter():
            if proc.name() == os.path.basename(self.exe_path):
                proc.kill()

        # Open the specified program from ini.
        p = subprocess.Popen(self.exe_path, shell=True)
        time.sleep(5)

        self.start_time = datetime.datetime.now()
        self.start_time = self.start_time.strftime(FMT)
        while p.poll() is None:
            time.sleep(5)
        self.end_time = datetime.datetime.now()
        self.end_time = self.end_time.strftime(FMT)

        self.write_log(name, dept)


if __name__ == "__main__":
    timer = ApplicationTimer()
