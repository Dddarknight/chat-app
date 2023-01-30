import aiohttp
import logging
import os
import socketio


logger = logging.getLogger("chat_app")

sio = socketio.AsyncServer(async_mode='asgi')
sio_app = socketio.ASGIApp(sio, static_files={
    '/': 'chat_app/templates/chat.html',
})
background_task_started = False

count = 0


HOST = os.getenv('HOST')
API_PORT = os.getenv('API_PORT')
MESSAGE_URL = f'http://{HOST}:{API_PORT}/create-message'
USERS_URL = f'http://{HOST}:{API_PORT}/users/'
USER_URL = f'http://{HOST}:{API_PORT}/user/'


@sio.on('connect_event')
async def connect_event(sid, message):
    username = message['username']
    global count
    count += 1
    reply_message = f'Connected {username}, count: {count}'
    logger.info(reply_message)
    await sio.emit('response',
                   {'data': reply_message})


@sio.on('join')
async def join(sid, message):
    room = message['room']
    username = message['username']

    sio.enter_room(sid, room)
    logger.info(f'Session_id {sid}, username {username} joined room {room}')

    sid_data = {'sid': sid, 'username': username}
    sid_url = f'{USER_URL}sid'

    room_data = {'room': room, 'username': username}
    room_url = f'{USER_URL}room'

    async with aiohttp.ClientSession() as session:
        logger.info(f'Request to {sid_url}, sid: {sid}, username: {username}')
        async with session.post(
                sid_url,
                json=sid_data) as response:
            await response.json()
        logger.info(f'Response status {response.status}')

        logger.info(
            f'Request to {room_url}, room: {room}, username: {username}')
        async with session.post(
                room_url,
                json=room_data) as response:
            await response.json()
        logger.info(f'Response status {response.status}')

    await sio.emit('response',
                   {'data': f'Entered room: {room}'},
                   room=room)


@sio.on('left')
async def leave(sid, message):
    room = message['room']
    username = message['username']

    sio.leave_room(sid, room)
    logger.info(f'Session_id {sid}, username {username} left room {room}')

    room_data = {'room': room, 'username': username}
    room_url = f'{USER_URL}room'

    async with aiohttp.ClientSession() as session:
        logger.info(
            f'Request to {room_url}, method: DELETE, '
            f'room: {room}, username: {username}')
        async with session.delete(
                room_url,
                json=room_data) as response:
            await response.json()
        logger.info(f'Response status {response.status}')

    await sio.emit('response',
                   {'data': f'Left room: {room}'},
                   room=sid)


@sio.on('message')
async def message(sid, message):
    content = message['data']
    room = message['room']

    message_scheme = {'content': content,
                      'room': room,
                      'sid': sid}
    logger.info(
        f'Received message, sid: {sid}, room: {room}, content: {content}')

    async with aiohttp.ClientSession() as session:
        logger.info(f'Request to {MESSAGE_URL}')
        async with session.post(
                MESSAGE_URL,
                json=message_scheme) as response:
            db_message = await response.json()
        logger.info(f'Response status {response.status}')

        user_url = f'{USERS_URL}{db_message.get("author_id")}'
        logger.info(f'Request to {user_url}')
        async with session.get(user_url) as response:
            user = await response.json()
        logger.info(f'Response status {response.status}')

    username = user.get('username')
    await sio.emit('chat',
                   {'data': message['data'], 'username': username},
                   room=message['room'])


@sio.on('close room')
async def close(sid, message):
    await sio.emit('response',
                   {'data': f'Room {message["room"]} is closing.'},
                   room=message['room'])
    await sio.close_room(message['room'])


@sio.on('disconnect')
def disconnect(sid):
    global count
    count -= 1
    print('Client disconnected')
