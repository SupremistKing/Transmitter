#!/usr/bin/env python3
"""
client.py — Tkinter chat client using Cristian's clock sync.
"""
import socket, threading, json, time, tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import simpledialog, messagebox

SERVER_HOST="127.0.0.1"; SERVER_PORT=50000
SYNC_INTERVAL=5; DRIFT=0.002  # 2 ms/sec drift

def now(): return time.time()

class ChatClient:
    def __init__(self,host,port,name):
        self.h,self.p,self.name=host,port,name
        self.sock=socket.socket(); self.running=True
        self.buf=""; self.corr=0; self.last_t0=None
        self.start_real=now(); self.last_sync=None
        self.root=tk.Tk(); self.root.title(f"Chat - {name}")
        self.txt=ScrolledText(self.root,state="disabled",width=80,height=20)
        self.txt.grid(row=0,column=0,columnspan=2,padx=5,pady=5)
        self.ent=tk.Entry(self.root,width=70); self.ent.grid(row=1,column=0,padx=5)
        self.ent.bind("<Return>",lambda e:self.send_msg())
        tk.Button(self.root,text="Send",command=self.send_msg).grid(row=1,column=1)
        self.lvar=tk.StringVar(); self.svar=tk.StringVar()
        tk.Label(self.root,textvariable=self.lvar).grid(row=2,column=0,sticky="w")
        tk.Label(self.root,textvariable=self.svar).grid(row=2,column=1,sticky="w")
        self.root.protocol("WM_DELETE_WINDOW",self.close)

    def local_time(self):
        elapsed=now()-self.start_real
        return now()+elapsed*DRIFT+self.corr

    def fmt(self,t): return time.strftime("%H:%M:%S",time.localtime(t))

    def log(self,msg):
        self.txt.config(state="normal"); self.txt.insert(tk.END,msg+"\n")
        self.txt.see(tk.END); self.txt.config(state="disabled")

    def connect(self):
        self.sock.connect((self.h,self.p))
        threading.Thread(target=self.listen,daemon=True).start()
        self.send({"type":"register","name":self.name})

    def send(self,obj):
        try:self.sock.sendall((json.dumps(obj)+"\n").encode())
        except Exception as e:self.log(f"[ERR] {e}")

    def send_msg(self):
        t=self.ent.get().strip()
        if not t:return
        self.send({"type":"message","from":self.name,"text":t,"client_time":self.local_time()})
        self.ent.delete(0,tk.END)

    def listen(self):
        try:
            while self.running:
                d=self.sock.recv(4096).decode()
                if not d: break
                self.buf+=d
                while "\n" in self.buf:
                    line,self.buf=self.buf.split("\n",1)
                    if not line:continue
                    self.handle(json.loads(line))
        except Exception as e:self.log(f"[ERR] {e}")
        self.running=False

    def handle(self,o):
        t=o.get("type")
        if t=="message":
            self.log(f"[{self.fmt(o['server_time'])}] {o['from']}: {o['text']}")
        elif t=="notice": self.log(f"* {o['text']}")
        elif t=="register_ack": self.log(f"[SERVER] {o['text']}")
        elif t=="sync_response":
            t1=now(); t0=self.last_t0 or t1
            rtt=t1-t0; est=o["server_time"]+rtt/2
            off=est-self.local_time(); self.corr+=off
            self.last_sync=(o["server_time"],t1)
            self.log(f"[SYNC] offset={off:.4f}s")
        else:self.log(str(o))

    def sync(self):
        self.last_t0=now(); self.send({"type":"sync_request"})
        self.root.after(int(SYNC_INTERVAL*1000),self.sync)

    def update(self):
        self.lvar.set("Local: "+self.fmt(self.local_time()))
        if self.last_sync:
            s,ts=self.last_sync; val=s+(now()-ts)
            self.svar.set("Synced: "+self.fmt(val))
        else:self.svar.set("Synced: --:--:--")
        self.root.after(200,self.update)

    def close(self):
        self.running=False; 
        try:self.sock.close()
        finally:self.root.destroy()

    def start(self):
        try:self.connect()
        except Exception as e:
            messagebox.showerror("Error",str(e)); return
        self.root.after(200,self.update)
        self.root.after(int(SYNC_INTERVAL*1000),self.sync)
        self.root.mainloop()

if __name__=="__main__":
    r=tk.Tk(); r.withdraw()
    name=simpledialog.askstring("Name","Enter your name:",parent=r)
    if not name:exit()
    ChatClient(SERVER_HOST,SERVER_PORT,name).start()
