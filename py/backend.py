from flask import Flask, request
import time
import random

app = Flask(__name__)  # 在当前文件下创建应用

USER_NAME = "username"
USER_ID = "userid"
DEVICE_ID = 'deviceid'

DEVICE_PAIR_PIN_LOWER_BOUND = 0
DEVICE_PAIR_PIN_UPPER_BOUND = 999999

DATA_TRANSFER_INT_LOWER_BOUND = 0
DATA_TRANSFER_INT_UPPER_BOUND = 99999999


STATUS_CODE_DICT = {
    'DEVICE_PAIR_LIST_FIND_NONE': -1,
    'DEVICE_PAIR_VERIFY_SUCCESS': 1000,
    'DEVICE_PAIR_VERIFY_ERROR': 1001,
    'DEVICE_PAIR_VERIFY_FAIL': 1002,
    'TRANSFER_KEY_GENERATE_SUCCESS': 1000,
    'TRANSFER_KEY_GENERATE_ERROR': 1001,
    'TRANSFER_KEY_GENERATE_FAIL': 1002,

}

PAIRED_DEVICE_LIST = {
    'device_id': {
        'add_timestamp' : 'timestamp',
        'verified' : False,
        'init_random_int' : 'str_int',

    }
}


def AES_Encryption(content, key):
    return content+key


def AES_Decryption(content, key):
    pass

def Prefix_Verify(content,prefix):
    return True


@app.route("/device_pair_init", methods=["GET", "POST"])
def device_pair_init():
    sub_device_id = request.args.get('device_id')
    pin_code = str(random.randint(DEVICE_PAIR_PIN_LOWER_BOUND,
                   DEVICE_PAIR_PIN_UPPER_BOUND)).zfill(6)
    init_random_int = str(random.randint(0, 99999999)).zfill(8)

    encrypt_str = AES_Encryption(
        content='ADS::'+init_random_int, key=sub_device_id+pin_code)

    return {'code': '', "encrypt_str": encrypt_str}


@app.route("/device_pair_verify", methods=["GET", "POST"])
def device_pair_verify():
    sub_device_id = request.args.get('device_id')
    init_random_int_get = request.args.get('init_random_int')
    init_random_int_save = PAIRED_DEVICE_LIST.get(
        sub_device_id, STATUS_CODE_DICT['DEVICE_PAIR_LIST_FIND_NONE'])
    if init_random_int_save == STATUS_CODE_DICT['DEVICE_PAIR_LIST_FIND_NONE']:
        return {'code': STATUS_CODE_DICT['DEVICE_PAIR_VERIFY_ERROR']}
    elif init_random_int_save == init_random_int_get:
        return {'code': STATUS_CODE_DICT['DEVICE_PAIR_VERIFY_SUCCESS']}
    else:
        return {'code': STATUS_CODE_DICT['DEVICE_PAIR_VERIFY_FAIL']}


@app.route("/transfer_key_generate", methods=["GET", "POST"])
def transfer_key_generate():
    sub_device_id = request.args.get('device_id')
    encrypt_str = request.args.get('encrypt_str')

    random_int = str(random.randint(DATA_TRANSFER_INT_LOWER_BOUND,
                     DATA_TRANSFER_INT_UPPER_BOUND)).zfill(8)

    init_random_int_save = PAIRED_DEVICE_LIST.get(
        sub_device_id, STATUS_CODE_DICT['DEVICE_PAIR_LIST_FIND_NONE'])
    if init_random_int_save == STATUS_CODE_DICT['DEVICE_PAIR_LIST_FIND_NONE']:
        return {'code': STATUS_CODE_DICT['TRANSFER_KEY_GENERATE_ERROR']}
    else:
        init_random_int_get = AES_Decryption(encrypt_str,init_random_int_save)

        if init_random_int_get == init_random_int_save:
            encrypt_str = AES_Encryption( 
                content='ADS::'+random_int, key=sub_device_id+init_random_int_save)
            PAIRED_DEVICE_LIST[sub_device_id]
            pass
            return {'code': STATUS_CODE_DICT['TRANSFER_KEY_GENERATE_SUCCESS'], "encrypt_str": encrypt_str}

        else:
            return {'code': STATUS_CODE_DICT['TRANSFER_KEY_GENERATE_FAIL']}

def transfer_data():
    transfer_key = 'transfer_key'


APP_LIST = []

def install_app():
    pass

@app.route("/add_app", methods=["GET", "POST"])
def add_app():

    app_id = request.args.get('app_id')
    version, trigger = install_app(app_id)

    app_config = {
        'app_id':app_id,
        'version': version,
        'trigger':trigger,
    }

    APP_LIST[app_id] = app_config

@app.route("/receive_trigger", methods=["GET", "POST"])
def receive_trigger():
    pass

            


clip_list = []


@app.route("/")  # 装饰器，url，路由
def index():  # 试图函数
    return "ganggang"


@app.route("/say_hello/<name>")  # 装饰器，url，路由
def say_hello(name):  # 试图函数

    return "hello world,I am your friend %s" % name


@app.route("/new_clip/<name>")  # 装饰器，url，路由
def new_clip(name):  # 试图函数
    curtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    clip_list.append({'time': curtime, 'content': name})
    return "new_clip: %s" % name


@app.route("/get_clip/")  # 装饰器，url，路由
def get_clip():  # 试图函数

    ret = clip_list.copy()
    ret.reverse()

    return ret


if __name__ == "__main__":
    app.run(debug=True, port=50000)  # 运行app
