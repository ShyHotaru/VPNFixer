import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys
import ctypes
from PIL import Image, ImageTk

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def run_network_reset():
    try:
        commands = [
            "ipconfig /release",
            "ipconfig /renew",
            "ipconfig /flushdns",
            "netsh winsock reset",
            "netsh int ip reset"
        ]
        
        for cmd in commands[:-1]:
            subprocess.run(cmd, shell=True, check=True)
            
        try:
            subprocess.run(commands[-1], shell=True, check=True)
        except subprocess.CalledProcessError:
            messagebox.showwarning("Warning", "TCP/IP reset failed. Proceeding anyway.")

        if messagebox.askyesno("Finished", "Network reset complete.\n\nWould you like to reboot now?"):
            subprocess.run("shutdown /r /t 0", shell=True)
        else:
            messagebox.showinfo("Exit", "You need to restart your computer to ensure proper operation.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def ensure_admin():
    """If not running as admin, relaunch as admin."""
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

ensure_admin()

root = tk.Tk()
root.title("VPN Error Fixer")
root.geometry("300x150")
root.iconphoto(True, ImageTk.PhotoImage(Image.open(resource_path("Fixer.ico"))))

label = tk.Label(root, text="Click the button to reset network.", pady=20)
label.pack()

reset_button = tk.Button(root, text="Reset Network", command=run_network_reset, height=2, width=20)
reset_button.pack()

root.mainloop()