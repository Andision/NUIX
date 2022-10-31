from flask import Flask, request
import time
import random
import database
import utils
import json
import queue
import importlib
import threading
import socket

app = Flask(__name__)  # 在当前文件下创建应用

# ==========Configuration==========

IS_DEBUG = True

USER_NAME = 'username'
USER_ID = 'userid'
DEVICE_ID = 'deviceid'

TRANSFER_DATA_KEY_PERIOD = 60*10

DEVICE_PAIR_PIN_LOWER_BOUND = 0
DEVICE_PAIR_PIN_UPPER_BOUND = 999999

DATA_TRANSFER_INT_LOWER_BOUND = 0
DATA_TRANSFER_INT_UPPER_BOUND = 99999999

APP_TRIGGER_QUEUE_MAX_SIZE = 100

STATUS_CODE_DICT = {
    'DEVICE_PAIR_LIST_FIND_NONE': -1,
    'DEVICE_PAIR_VERIFY_SUCCESS': '1000',
    'DEVICE_PAIR_VERIFY_ERROR': '1001',
    'DEVICE_PAIR_VERIFY_FAIL': '1002',
    'TRANSFER_KEY_GENERATE_SUCCESS': '1000',
    'TRANSFER_KEY_GENERATE_ERROR': '1001',
    'TRANSFER_KEY_GENERATE_FAIL': '1002',
    'TRANSFER_DATA_SUCCESS': '1000',
    'TRANSFER_DATA_ERROR': '1001',
    'TRANSFER_DATA_FAIL': '1002',
}

# *****old*****
# PAIRED_DEVICE_LIST = {
#     'device_id': {
#         'add_timestamp' : 'timestamp',
#         'verified' : False,
#         'init_random_int' : 'str_int',

#     }
# }
# *****old*****

# ==========Utils==========


def printLog(log):
    if IS_DEBUG:
        print('*****DEBUG*****')
        print(log)
        print('-----DEBUG-----')


@app.route('/test', methods=['GET', 'POST'])
def test():
    l = database.sys_get_paired_device('test')
    print('l: ')
    print(l)
    print('l. ')
    return l


SOCKET_PORT = 60000


def broadcast():
    print('Start Receiving Broadcast on Port', SOCKET_PORT)
    sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # sk.settimeout(200000)
    sk.bind(('0.0.0.0', SOCKET_PORT))
    while True:
        msg, addr = sk.recvfrom(1024)
        print()
        if msg == b'NUIX connect request':
            print(
                f'[{time.strftime("%H:%M:%S")}] from {addr[0]}:{addr[1]}, msg: {msg}')
            sk.sendto('NUIX connect received'.encode('utf-8'), addr)

# ==========Device=========


@app.route('/device_pair_init', methods=['GET', 'POST'])
def device_pair_init():
    sub_device_id = request.args.get('device_id')
    # ======================================== MOCK
    # pin_code = str(random.randint(DEVICE_PAIR_PIN_LOWER_BOUND,
    #                DEVICE_PAIR_PIN_UPPER_BOUND)).zfill(6)
    # init_random_int = str(random.randint(0, 99999999)).zfill(8)
    pin_code = '123456'
    init_random_int = '12345678'
    # ======================================== MOCK

    encrypt_str = utils.AES_Encryption(
        content=init_random_int, key=pin_code)

    # # *****old*****
    # PAIRED_DEVICE_LIST[sub_device_id] = {
    #     'add_timestamp' : time.time(),
    #     'verified' : False,
    #     'init_random_int' : init_random_int,
    # }
    # # *****old*****
    database.sys_add_paired_device(
        sub_device_id, sub_device_id, time.time(), init_random_int, False)

    ret = {'code': '', 'encrypt_str': encrypt_str}

    printLog(ret)

    return ret


@app.route('/device_pair_verify', methods=['GET', 'POST'])
def device_pair_verify():
    sub_device_id = request.args.get('device_id')
    encrypt_str = request.args.get('encrypt_str')
    # init_random_int_get = request.args.get('init_random_int')

    # *****old*****
    # init_random_int_save = PAIRED_DEVICE_LIST.get(
    #     sub_device_id, {'init_random_int' :STATUS_CODE_DICT['DEVICE_PAIR_LIST_FIND_NONE']})['init_random_int']
    # *****old*****
    get_from_database = database.sys_get_paired_device(sub_device_id)
    init_random_int_save = get_from_database[0][3] if len(
        get_from_database) else STATUS_CODE_DICT['DEVICE_PAIR_LIST_FIND_NONE']

    if init_random_int_save == STATUS_CODE_DICT['DEVICE_PAIR_LIST_FIND_NONE']:
        ret = {'code': STATUS_CODE_DICT['DEVICE_PAIR_VERIFY_ERROR']}

        printLog('VERIFY')
        printLog(ret)

        return ret

    init_random_int_get = utils.AES_Decryption(
        content=encrypt_str, key=init_random_int_save)

    if init_random_int_save == init_random_int_get:
        ret = {'code': STATUS_CODE_DICT['DEVICE_PAIR_VERIFY_SUCCESS']}
        database.sys_verify_paired_device(sub_device_id)

        printLog('VERIFY')
        printLog(ret)

        return ret
    else:
        ret = {'code': STATUS_CODE_DICT['DEVICE_PAIR_VERIFY_FAIL']}

        printLog('VERIFY')
        printLog('=====DEBUG=====')
        printLog(get_from_database)
        printLog(init_random_int_get)
        printLog(init_random_int_save)
        printLog(ret)

        return ret


@app.route('/device_get_paired', methods=['GET', 'POST'])
def device_get_paired():
    get_from_database = database.sys_get_paired_device()
    printLog(get_from_database)
    return 'ok'


# ==========Transfer Data==========

@app.route('/transfer_key_generate', methods=['GET', 'POST'])
def transfer_key_generate():
    sub_device_id = request.args.get('device_id')
    # encrypt_str = request.args.get('encrypt_str')

    random_int = str(random.randint(DATA_TRANSFER_INT_LOWER_BOUND,
                     DATA_TRANSFER_INT_UPPER_BOUND)).zfill(8)

    # *****old*****
    # init_random_int_save = PAIRED_DEVICE_LIST.get(
    #     sub_device_id, {'init_random_int' :STATUS_CODE_DICT['DEVICE_PAIR_LIST_FIND_NONE']})['init_random_int']
    # *****old*****

    get_from_database = database.sys_get_paired_device(sub_device_id)
    init_random_int_save = get_from_database[0][3] if len(
        get_from_database) else STATUS_CODE_DICT['DEVICE_PAIR_LIST_FIND_NONE']

    if init_random_int_save == STATUS_CODE_DICT['DEVICE_PAIR_LIST_FIND_NONE']:
        return {'code': STATUS_CODE_DICT['TRANSFER_KEY_GENERATE_ERROR']}
    else:
        encrypt_str = utils.AES_Encryption(
            content=random_int, key=init_random_int_save)
        expired_time = time.time()+TRANSFER_DATA_KEY_PERIOD
        database.sys_update_transfer_data_key(
            device_id=sub_device_id, key=random_int, expired_time=expired_time)

        return {'code': STATUS_CODE_DICT['TRANSFER_KEY_GENERATE_SUCCESS'], 'encrypt_str': encrypt_str, 'expired_time': str(expired_time)}


@app.route('/transfer_data', methods=['GET', 'POST'])
def transfer_data():
    sub_device_id = request.args.get('device_id')
    encrypt_str = request.args.get('encrypt_str')
    get_key = database.sys_get_transfer_data_key(sub_device_id)
    transfer_key = ''
    transfer_key_expired_time = ''
    current_time = time.time()

    print("get_key = ", get_key)
    if len(get_key) and get_key[0][0] != None:
        transfer_key = get_key[0][0]
        transfer_key_expired_time = float(get_key[0][1])

        if current_time > transfer_key_expired_time:
            ret = {'code': STATUS_CODE_DICT['DEVICE_PAIR_VERIFY_FAIL']}
            return ret
    else:
        ret = {'code': STATUS_CODE_DICT['DEVICE_PAIR_VERIFY_ERROR']}
        return ret

    printLog(transfer_key + transfer_key_expired_time)

    decrypt_str = utils.AES_Decryption(encrypt_str, transfer_key)
    # ADS DEBUG!
    # data = json.loads(decrypt_str)
    data = decrypt_str

    printLog("In Transfer_Data data="+data)

    if data == "NUIXTEST":
        ret = {'code': STATUS_CODE_DICT['DEVICE_PAIR_VERIFY_SUCCESS']}
    else:
        ret = {'code': STATUS_CODE_DICT['DEVICE_PAIR_VERIFY_FAIL']}

    return ret


    # ADS DEBUG!
    # res, exc = handleData(data)

    # if res:
    #     ret = {'code': STATUS_CODE_DICT['DEVICE_PAIR_VERIFY_SUCCESS']}
    # else:
    #     ret = {
    #         'code': STATUS_CODE_DICT['DEVICE_PAIR_VERIFY_FAIL'], 'log': str(exc)}

    # return ret

sub_device_clipboard_list = ['haha']
mutex = threading.Lock()


@app.route('/get_data', methods=['GET', 'POST'])
def get_data():
    t = random.randint(0, 10)
    ret = ''
    global sub_device_clipboard_list
    mutex.acquire()
    if t < 5:
        ret = "new_clip"+str(t)
        sub_device_clipboard_list.append(t)
    printLog(t)
    sub_device_clipboard_list = []
    mutex.release()

    return ret


# ==========Trigger==========


class AppPermissionConfiguration:
    app_id = ''
    permission = False
    trigger_type = ''

    def __init__(self, app_id, trigger_type, permission) -> None:
        self.app_id = app_id
        self.trigger_type = trigger_type
        self.permission = permission


PERMISSION_TRIGGER_LIST = {
    'clipboard': [
        AppPermissionConfiguration('air_clip_app_id', 'clipboard', True)
    ]
}

APP_TRIGGER_LIST = {
    'air_clip_app_id': queue.Queue(maxsize=APP_TRIGGER_QUEUE_MAX_SIZE)
}


def handleData(data):
    data_type = data['data_type']
    data_payload = data['payload']
    app_list = PERMISSION_TRIGGER_LIST.get(data_type, [])

    for my_app in app_list:
        if not my_app.permission:
            continue

        try:
            APP_TRIGGER_LIST[my_app.app_id].put(data_payload)
        except Exception as e:
            return False, e

        return True, None

# ==========APP==========


APP_LIST = [
    {
        'app_id': 'air_clip_app_id',
        'app_name': 'airclip',
        'app_show_name': 'AirClip',
        'script_list': [
            {
                'name': 'airclip',
                'prefix': '/airclip'
            }
        ]
    },
]


def install_app():
    pass


@app.route('/add_app', methods=['GET', 'POST'])
def add_app():

    app_id = request.args.get('app_id')
    version, trigger = install_app(app_id)

    app_config = {
        'app_id': app_id,
        'version': version,
        'trigger': trigger,
    }

    APP_LIST[app_id] = app_config


# ==========Sensor==========

def handleClipboardChange(args):
    while (True):
        print("我是线程%s" % args)
        time.sleep(2)

# t1 = threading.Thread(target=handleClipboardChange, args=(1,))
# t2 = threading.Thread(target=handleClipboardChange, args=(2,))
# t1.start()
# t2.start()


# ==========Init==========
# =====Add Router=====
for my_app in APP_LIST:
    for script in my_app['script_list']:
        module = importlib.import_module('app.{}'.format(script['name']))
        app.register_blueprint(module.app, url_prefix='/app'+script['prefix'])

# =====Broadcast=====
# thread_broadcast = threading.Thread(target=broadcast)
# thread_broadcast.start()

# =====Start Flask=====
app.run(debug=IS_DEBUG, host='0.0.0.0', port=5000)  # 运行app
