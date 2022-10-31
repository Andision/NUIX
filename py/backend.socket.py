# # 使用协程的方式运行 (推荐)
# import eventlet
# eventlet.monkey_patch()

# import socketio
# import eventlet.wsgi

# sio = socketio.Server(async_mode='eventlet')  # 指明在evenlet模式下
# app = socketio.Middleware(sio)
# eventlet.wsgi.server(eventlet.listen(('', 8000)), app)

import socketio
import eventlet

sio = socketio.Server()
app = socketio.Middleware(sio)
eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 8000)), app)


@sio.event
def connect(sid, environ, auth):
    print('connect ', sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

# 以字符串的形式表示一个自定义事件，事件的定义由前后端约定
@sio.on('pair')  
def pair(sid, data):
    """
    自定义事件消息的处理方法
    :param sid: string sid是发送此事件消息的客户端id
    :param data: data是客户端发送的消息数据
    """

    print('In Pair')
    print('sid=',sid)
    print('data=',data)

    callbacks

    return '{"status":"ok"}', 123