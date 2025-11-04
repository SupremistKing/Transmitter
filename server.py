#!/usr/bin/env python3
"""
server.py — Multi-client chat server with Cristian's clock sync.
"""
import socket, threading, json, time

HOST = "0.0.0.0"
PORT = 50000
clients_lock = threading.Lock()
clients = []  # (conn, addr, name)

def send_json(conn, obj):
    data = (json.dumps(obj) + "\n").encode()
    conn.sendall(data)

def broadcast(obj, exclude=None):
    data = (json.dumps(obj) + "\n").encode()
    with clients_lock:
        dead = []
        for c, a, n in clients:
            if c is exclude: 
                continue
            try:
                c.sendall(data)
            except:
                dead.append((c,a,n))
        for d in dead:
            clients.remove(d)

def handle_client(conn, addr):
    name, buf = None, ""
    try:
        while True:
            chunk = conn.recv(4096).decode()
            if not chunk:
                break
            buf += chunk
            while "\n" in buf:
                line, buf = buf.split("\n",1)
                if not line.strip():
                    continue
                obj = json.loads(line)
                t = obj.get("type")
                if t=="register":
                    name = obj.get("name", str(addr))
                    with clients_lock: clients.append((conn,addr,name))
                    broadcast({"type":"notice","text":f"{name} joined."})
                    send_json(conn,{"type":"register_ack","text":"Welcome!","server_time":time.time()})
                elif t=="message":
                    msg={"type":"message","from":name,"text":obj["text"],
                         "client_time":obj.get("client_time"),"server_time":time.time()}
                    broadcast(msg)
                elif t=="sync_request":
                    send_json(conn,{"type":"sync_response","server_time":time.time()})
    except Exception as e:
        print(f"{addr}: {e}")
    finally:
        conn.close()
        with clients_lock:
            clients[:] = [c for c in clients if c[0] is not conn]
        if name: broadcast({"type":"notice","text":f"{name} left."})

def main():
    print(f"Server running on {HOST}:{PORT}")
    s = socket.socket(); s.bind((HOST,PORT)); s.listen(50)
    try:
        while True:
            c,a = s.accept()
            threading.Thread(target=handle_client,args=(c,a),daemon=True).start()
    except KeyboardInterrupt:
        print("Server stopped.")
    finally:
        s.close()

if __name__=="__main__": main()
