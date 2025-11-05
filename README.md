#  WhatsApp-like Chat App(Named TRANSMITTER) with Cristian Clock Synchronization

A Python-based multi-client chat system using sockets, threading, and Tkinter GUI.  
Implements **Cristian’s algorithm** to synchronize client clocks with the server.

# Features
- Multi-client server with message broadcasting  
- Cristian’s clock synchronization  
- Tkinter chat interface with local & synced time  
- Threaded concurrency for smooth chatting  
- Optional simulated clock drift  

# How to Run Locally
```bash
# Terminal 1 – start the server
python server.py

# Terminal 2+ – run multiple clients
python client.py
```

Enter a display name for each client and start chatting!  
You’ll see `[SYNC]` messages showing periodic clock adjustments.

#  Showcase
1. Server console with client connections

   <img width="640" height="257" alt="image" src="https://github.com/user-attachments/assets/0c78e45e-4ce3-4d5f-a0af-da282994dcba" />

   

2. Two chat windows exchanging messages
<img width="1087" height="407" alt="image" src="https://github.com/user-attachments/assets/a26b0ae6-e3e8-4700-80fa-0376f028fee7" />








   
3. `[SYNC]` offset logs
   <img width="911" height="81" alt="image" src="https://github.com/user-attachments/assets/b7c80f6d-f397-40be-bd0c-9d3aacf8fb99" />

