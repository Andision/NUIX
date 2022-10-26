import threading
import time
import socketio
from aiohttp import web
from urllib import parse
import socket

import database
import utils
from utils import myPrintLog

DEVICE_PAIR_PIN_LOWER_BOUND = 0
DEVICE_PAIR_PIN_UPPER_BOUND = 999999

# TRANSFER_DATA_KEY_VALID_TIME = 10 *1000  # 10 minutes - 10 seconds
# (10 minutes - 10 seconds) unit=ms
TRANSFER_DATA_KEY_VALID_TIME = (10 * 60 - 10)*1000

STATUS_CODE_DICT = {
    "OK": 2000,
    "FAILED": 3000,
    "DEVICE_PAIR_VERIFY_DEVICE_NOT_FOUND": 3001,
    "DEVICE_PAIR_VERIFY_ID_NOT_MATCH": 3002,
    "DATA_TRANSFER_KEY_GENERATE_DEVICE_NOT_FOUND": 3003,
    "RECEIVE_DATA_KEY_EXPIRED": 3004,
    "RECEIVE_DATA_DEVICE_NOT_FOUND": 3005
}


def broadcast():
    PORT = 60000
    sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # sk.settimeout(200000)
    sk.bind(('0.0.0.0', PORT))
    while True:
        msg, addr = sk.recvfrom(1024)
        # print(time.strftime("%H:%M:%S"))
        # print(f'from {addr[0]}:{addr[1]}, msg: {msg}')
        if msg == b'NUIX connect request':
            myPrintLog('Broadcast', f'from {addr[0]}:{addr[1]}, msg: {msg}')
            sk.sendto('NUIX connect received'.encode('utf-8'), addr)


async def connect(sid, *arg):

    myPrintLog('connect', sid)


async def disconnect(sid, *arg):
    myPrintLog('disconnect', sid)


# async def pair(sid, *arg):
#     myPrintLog('pair', sid, arg)
#     return 'haha'

async def devicePairInit(sid, *args):
    '''Pair device, generate init key and add info to database

    :param device_id: The device id of client device.

    '''
    device_id = args[0]
    # ======================================== MOCK
    # pin_code = str(random.randint(DEVICE_PAIR_PIN_LOWER_BOUND,
    #                DEVICE_PAIR_PIN_UPPER_BOUND)).zfill(6)
    # init_random_int = str(random.randint(0, 99999999)).zfill(8)
    pin_code = '123456'
    init_key = 'init_key_mock'
    # ======================================== MOCK

    encrypt_str = utils.AES_Encryption(
        content=init_key, key=pin_code)

    database.sys_add_paired_device(
        device_id, device_id, time.time(), init_key, False)

    myPrintLog('devicePairInit', "OK")
    return STATUS_CODE_DICT["OK"], encrypt_str


async def devicePairVerify(sid, *args):
    '''Pair verify, verify the pin and update verify status in database

    :param device_id: The device id of client device.

    :param encrypt_str: Encrypted str, device id of client device encryped by init key.

    '''
    device_id = args[0]
    encrypt_str = args[1]

    get_from_database = database.sys_get_paired_device(device_id)

    init_key_save = get_from_database[0][3] if len(
        get_from_database) else None

    if init_key_save != None:
        device_id_get = utils.AES_Decryption(
            content=encrypt_str, key=init_key_save)
        if device_id_get == device_id:
            myPrintLog('devicePairVerify', 'device verify success')
            return STATUS_CODE_DICT["OK"]

        else:
            myPrintLog('devicePairVerify', 'device id not match get={get} save={save}'.format(
                get=device_id_get, save=device_id))
            return STATUS_CODE_DICT["DEVICE_PAIR_VERIFY_ID_NOT_MATCH"]
    else:
        myPrintLog('devicePairVerify', 'device not found in db')
        return STATUS_CODE_DICT["DEVICE_PAIR_VERIFY_DEVICE_NOT_FOUND"]


async def dataTransferKeyGen(sid, *args):
    '''Generate key for data transfer.

    :param device_id: The device id of client device.

    '''

    device_id = args[0]

    get_from_database = database.sys_get_paired_device(device_id)
    init_key = get_from_database[0][3] if len(
        get_from_database) else None

    if init_key != None:
        data_transfer_key = utils.keyGenerate()
        encrypt_str = utils.AES_Encryption(
            content=data_transfer_key, key=init_key)
        expired_time = str(time.time()*1000+TRANSFER_DATA_KEY_VALID_TIME)

        database.sys_update_transfer_data_key(
            device_id=device_id, key=data_transfer_key, expired_time=expired_time)

        myPrintLog('dataTransferKeyGen', 'data transfer key gen success')
        return STATUS_CODE_DICT["OK"], encrypt_str, expired_time

    else:
        myPrintLog('dataTransferKeyGen', 'device not found in db')
        return STATUS_CODE_DICT["DATA_TRANSFER_KEY_GENERATE_DEVICE_NOT_FOUND"]


async def receiveData(sid, *args):
    '''
    Receive data from client device.

    :param device_id: The device id of client device.

    :param encrypt_str: The encrypted data from client device, data encrypted by dataTransferKey.

    '''
    device_id = args[0]
    encrypt_str = args[1]

    get_from_database = database.sys_get_transfer_data_key(device_id)

    transfer_key = get_from_database[0][0] if len(
        get_from_database) else None

    if transfer_key != None:
        transfer_key_expired_time = float(get_from_database[0][1])
        current_time = time.time()

        if current_time > transfer_key_expired_time:
            myPrintLog("receiveData", "Key expired")
            return STATUS_CODE_DICT["RECEIVE_DATA_KEY_EXPIRED"]

        decrypt_str = utils.AES_Decryption(
            content=encrypt_str, key=transfer_key)

        myPrintLog("receiveData", decrypt_str)
        return STATUS_CODE_DICT["OK"]

    else:
        myPrintLog("receiveData", "Device not found")
        return STATUS_CODE_DICT["RECEIVE_DATA_DEVICE_NOT_FOUND"]


async def test(sid, *args):
    myPrintLog("pair", args)
    return "OK"


if __name__ == '__main__':
    app = web.Application()
    # logging.basicConfig(level=logging.DEBUG)
    # app.router.add_get('/chat_room', chat_room)
    # app.router.add_routes([web.post('/login', login)])
    # app.router.add_static('/static', 'static')

myPrintLog("System", 'socket broadcast init')
thread_broadcast = threading.Thread(target=broadcast)
thread_broadcast.start()

myPrintLog("System", 'socket.io init')
sio = socketio.AsyncServer()

sio.on('disconnect', disconnect)
sio.on('connect', connect)
sio.on('device pair init', devicePairInit)
sio.on('device pair verify', devicePairVerify)
sio.on('data transfer key', dataTransferKeyGen)
sio.on('receive data', receiveData)

sio.on('pair', test)
sio.attach(app)

web.run_app(app, host='0.0.0.0', port=8000)
