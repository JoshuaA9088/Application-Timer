import time
import subprocess
import psutil
import tkinter as tk
import os
import configparser
import csv
import datetime


fields = ('Name', 'Department')
FMT = "%H:%M:%S"


def makeform(root, fields):
    entries = {}
    for field in fields:
        row = tk.Frame(root)
        lab = tk.Label(row, width=22, text=field + ": ", anchor='w')
        ent = tk.Entry(row)
        # ent.insert(0, "0")
        row.pack(side=tk.TOP,
                 fill=tk.X,
                 padx=5,
                 pady=5)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT,
                 expand=tk.YES,
                 fill=tk.X)
        entries[field] = ent
    return entries


def center(toplevel):
    toplevel.update_idletasks()

    # Tkinter way to find the screen resolution
    screen_width = toplevel.winfo_screenwidth()
    screen_height = toplevel.winfo_screenheight()

    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = screen_width / 2 - size[0] / 2
    y = screen_height / 2 - size[1] / 2

    toplevel.geometry("+%d+%d" % (x, y))
    toplevel.title("Application Timer")


def load_static_vars():
    global ExecutablePath, OutputLogPath, ConfigPath
    config = configparser.ConfigParser()
    home = os.environ["USERPROFILE"]
    my_docs = os.path.join(home, "My Documents")
    my_docs = os.path.join(my_docs, "Timer")
    # ConfigPath = my_docs
    if not os.path.exists(my_docs):
        os.mkdir(my_docs)
    config['DEFAULT'] = {'ExecutablePath': r"C:\Windows\System32\notepad.exe",
                         'OutputLogPath': os.path.join(my_docs, "timer_log.csv")}

    if os.path.exists(os.path.join(my_docs, "timer.ini")):
        config.read(os.path.join(my_docs, "timer.ini"))
        ExecutablePath = config["DEFAULT"]["ExecutablePath"]
        OutputLogPath = config["DEFAULT"]["OutputLogPath"]
    else:
        ExecutablePath = r"C:\Windows\System32\notepad.exe " + os.path.join(my_docs, "timer.ini")
        OutputLogPath = os.path.join(my_docs, "timer_log.csv")
        f = open(os.path.join(my_docs, "timer.ini"), "w+")
        config.write(f)
        f.close()


def write_log(name, dept, start_time, end_time):
    global ExecutablePath, OutputLogPath
    if os.path.exists(OutputLogPath):
        csvData = []
    else:
        csvData = [["Date", "Name", "Department", "Start Time", "End Time", "Elapsed"]]

    date = datetime.datetime.today()
    date = date.strftime('%m-%d-%Y')
    date = str(date)

    elapsed = datetime.datetime.strptime(end_time, FMT) - datetime.datetime.strptime(start_time, FMT)
    elapsed = str(elapsed)

    csvData.append([date, name, dept, start_time, end_time, elapsed])

    f = open(OutputLogPath, "a", newline="")
    writer = csv.writer(f)
    writer.writerows(csvData)
    f.close()


def time_app(ents):
    global ExecutablePath, OutputLogPath
    # Get username field
    name = ents["Name"].get()
    dept = ents["Department"].get()
    # Kill the main window and run in background
    global root
    root.destroy()
    # Kill all prior instances of the program.
    for proc in psutil.process_iter():
        if proc.name() == os.path.basename(ExecutablePath):
            proc.kill()
    # Open the specified program from ini.
    p = subprocess.Popen(ExecutablePath, shell=True)
    time.sleep(5)

    start_time = datetime.datetime.now()
    start_time = start_time.strftime(FMT)
    while p.poll() is None:
        time.sleep(5)
    end_time = datetime.datetime.now()
    end_time = end_time.strftime(FMT)

    write_log(name, dept, start_time, end_time)


if __name__ == '__main__':
    load_static_vars()

    root = tk.Tk()
    center(root)
    ents = makeform(root, fields)
    ents["Name"].icursor(0)
    start_button = tk.Button(root, text='Start', command=(lambda e=ents: time_app(e)))
    start_button.pack(side=tk.RIGHT, padx=5, pady=5)
    quit_button = tk.Button(root, text='Quit', command=root.quit)
    quit_button.pack(side=tk.RIGHT, padx=5, pady=5)
    root.mainloop()
