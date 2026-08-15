import socket
import tkinter as tk
from threading import Thread
import winsound

PORT = 5005

class Dashboard:

    def __init__(self,root):

        self.root = root

        root.title("Hospital Alert System")
        root.geometry("600x400")

        self.status = tk.Label(root,text="SYSTEM NORMAL",font=("Arial",30),bg="green",fg="white")
        self.status.pack(fill="both",expand=True)

        self.msg = tk.Label(root,text="Waiting for alerts",font=("Arial",14))
        self.msg.pack(pady=20)

        Thread(target=self.listen,daemon=True).start()

    def listen(self):

        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        sock.bind(("0.0.0.0",PORT))

        while True:

            data,addr = sock.recvfrom(1024)

            message = data.decode()

            self.root.after(0,self.trigger,message)

    def trigger(self,message):

        winsound.Beep(2000,200)

        self.status.config(text="🚨 EMERGENCY 🚨",bg="red")

        self.msg.config(text=message)

        self.root.after(4000,self.reset)

    def reset(self):

        self.status.config(text="SYSTEM NORMAL",bg="green")

        self.msg.config(text="Patient OK")

root = tk.Tk()
Dashboard(root)
root.mainloop()
