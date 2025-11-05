# Technical Report — TRANSMITTER(WhatsApp-like Chat with Cristian Clock Sync)

## 1. Server-Client Communication
- The system uses Python **sockets** for communication.
- **Server** listens for multiple client connections.
- Each **client** connects to the server and can send messages.
- The server **broadcasts** messages to all connected clients in real time.
- Example flow:
  1. Client sends message to server.
  2. Server receives message.
  3. Server forwards message to all other clients.

## 2. Threading / Concurrency
- The **server** uses Python **threading** to handle multiple clients simultaneously.
- Each client connection runs in a separate thread.
- Threading ensures that receiving and sending messages does not block other clients.
- The server can handle multiple messages at the same time.

## 3. Clock Synchronization (Cristian's Algorithm)
- Clients synchronize their clocks with the server periodically.
- **Cristian's algorithm** steps:
  1. Client sends a timestamp request to the server.
  2. Server responds with its current time.
  3. Client calculates the **offset** between its clock and the server's.
  4. Client adjusts its clock based on the offset.
- This ensures that all clients have a **reasonably synchronized time** for message timestamps.
- Example output:
  ```
  [SYNC] offset=-0.0100s
  ```
  Indicates the client clock is 10 milliseconds ahead of the server.

## 4. Graphical User Interface (Tkinter)
- Each client has a **Tkinter GUI**.
- Components:
  - Chat window showing messages.
  - Input box for typing messages.
  - Labels displaying **local time** and **synced server time**.
- Messages are displayed with timestamps based on the synchronized clock.

## 5. Testing / Multi-client Verification
- Multiple clients were run simultaneously.
- Messages appear in all clients in real time.
- Clock synchronization messages show small offsets, confirming accurate syncing.
- Both chat functionality and time synchronization were verified to work correctly.

## Conclusion
- The assignment objectives were successfully met:
  - Multi-client chat system with broadcasting.
  - Threaded server for concurrency.
  - Cristian’s clock synchronization implemented.
  - Tkinter GUI displaying messages and time.
