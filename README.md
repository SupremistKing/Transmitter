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
Add screenshots of:
1. Server console with client connections
   <img width="400" height="150" alt="image" src="https://github.com/user-attachments/assets/b9fb764f-8f45-44f7-a07b-cb214ef654d0" />

3. Two chat windows exchanging messages  
4. `[SYNC]` offset logs  
