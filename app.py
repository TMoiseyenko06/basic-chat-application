from web_socket_server import WebSocketServer, socketio, app
from flask import request, render_template, redirect
from flask_socketio import join_room, leave_room

app = WebSocketServer.create_app(True)

rooms = {}
users = {}

@socketio.on('connect')
def handle_connect():
    print(f'{request.sid} : Connected')

@socketio.on('disconnect')
def handle_disconnect():
    user = users[request.sid]
    users.pop(request.sid, None)
    current_room = None
    for room, userss in rooms.items():
        if user in userss:
            current_room = room
            break
    if current_room:
        rooms[current_room].remove(user)  
        socketio.emit('current_users', {'users': rooms[current_room]}, room=current_room)
        socketio.emit('receive_message', {'name': 'System', 'message': f'{user} has left the room.'}, room=current_room)

    print(f'{request.sid} : Disconnected')

@app.route('/')
def index():
    return render_template('join_room.html')

@socketio.on('join_room')
def handle_join_room(data):
    room = data['room']
    name = data['name']
    try:
        rooms[room].append(name)
    except:
        rooms[room] = []
        rooms[room].append(name)
    users[request.sid] = name
    print(rooms)
    join_room(room)
    socketio.emit('receive_message', {'name':'System', 'message':f'{name} has joined the room.'}, room=room)
    socketio.emit('current_users',{'users':rooms[room]}, room=room)
    
@socketio.on('send_message')
def handle_send_message(data):
    message = data['message']
    room = data['room']
    socketio.emit('receive_message',{'name': users[request.sid], 'message': message}, room=room)

@socketio.on("leave_room")
def handle_leave_room(data):
    print("Data received:", data)
    room = data['room']
    name = data['name']
    rooms[room].remove(name)
    leave_room(room)
    print(name,room)
    socketio.emit('current_users',{'users':rooms[room]}, room=room)
    socketio.emit('receive_message', {'name': 'System', 'message': f'{name} has left the room.'}, room=room)

socketio.run(app)