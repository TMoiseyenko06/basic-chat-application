# Chat App

This is a basic chat app built in python using flask and the SocketIO library.

## Installation

Use Git to clone the reponsity to your machine.

```
git clone https://github.com/TMoiseyenko06/basic-chat-application.git
```
## Description

This is a simple chat room project that has different rooms and users, it was made to show the understanding of basic websocket connections and basic data-structures.

## Usage

```python

# handle connection
@socketio.on('connect')

# handle disconection
@socketio.on('disconnect')

# handles room join
@socketio.on('join_room')

#handles message sending
@socketio.on('send_message')

# handles room leaving 
@socketio.on("leave_room")
```




