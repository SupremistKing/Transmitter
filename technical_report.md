# Technical Report — WhatsApp-like Chat with Cristian Clock Sync

**Overview**
This project implements a multi-client chat system using Python sockets and threading.  
Each client has a Tkinter GUI that displays both the local and server-synchronized time.  
Cristian’s algorithm keeps all clients’ clocks consistent.

**Architecture**
- **Server:** Handles multiple clients via threads, broadcasts all messages, responds to time-sync requests.  
- **Client:** Connects via sockets, displays chat window, periodically requests server time.

**Threading**
- Each server client runs in a separate `threading.Thread`.  
- Each client runs a listener thread so the GUI (Tkinter mainloop) remains responsive.

**Cristian’s Algorithm**
1. Client notes `t0` (send time).  
2. Server replies with its current clock `ts`.  
3. Client notes `t1` (receive time).  
4. Estimated true time ≈ `ts + (t1 - t0)/2`.  
5. Client applies correction offset to its local simulated clock.

**Clock Drift Simulation**
Clients add a small drift per second to simulate hardware clock differences.  
Regular synchronization (every 5 s) corrects the drift automatically.

**Testing**
1. Run `server.py` → waits for clients.  
2. Run `client.py` in two terminals → exchange messages.  
3. Observe `[SYNC]` offsets adjusting periodically.  

**Files**
| File | Purpose |
|------|----------|
| `server.py` | Multi-client broadcast + clock responses |
| `client.py` | Tkinter GUI + Cristian sync |
| `technical_report.md` | Design summary |
