# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 23:02:33 2023

@author: Ali Sadeghi
"""

import subprocess
import ctypes
import sys
import tkinter as tk
from tkinter import messagebox

class DNSChanger:
    def __init__(self, master):
        self.master = master
        master.title("DNS Changer")
        master.resizable(False, False)

        self.label = tk.Label(master, text="Click the button to change your DNS servers to 178.22.122.100 and 185.51.200.2.")
        self.label.pack(pady=10)

        self.button = tk.Button(master, text="Change DNS", command=self.set_dns)
        self.button.pack()

        self.close_button = tk.Button(master, text="Close", command=self.close)
        self.close_button.pack(pady=10)

    def set_dns(self):
        try:
            # Check if the script is running as an administrator
            if not ctypes.windll.shell32.IsUserAnAdmin():
                messagebox.showerror("Error", "Please run this script as an administrator.")
                return

            # Set the DNS servers
            command = 'netsh interface ip set dns "Ethernet" static 178.22.122.100 primary'
            subprocess.call(command, shell=True)
            command = 'netsh interface ip add dns "Ethernet" 185.51.200.2 index=2'
            subprocess.call(command, shell=True)

            messagebox.showinfo("Success", "DNS servers have been changed to 178.22.122.100 and 185.51.200.2.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def close(self):
        try:
            # Reset the DNS servers to their defaults
            command = 'netsh interface ip set dns "Ethernet" dhcp'
            subprocess.call(command, shell=True)

            messagebox.showinfo("Success", "DNS servers have been reset to their defaults.")
            self.master.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == '__main__':
    root = tk.Tk()
    app = DNSChanger(root)
    root.mainloop()
