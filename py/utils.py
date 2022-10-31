import time

def myPrintLog(tag, *args,type="info"):
    if type=="info":
        color = "1;30;47"
    elif type=="error":
        color = "1;30;41"

    for i in args:
        print("[{time}]  \033[{color}m{type}\033[0m{tag}    {msg}".format(
            time=time.strftime("%H:%M:%S"), msg=i, tag=tag.rjust(20),color=color,type=type.upper()))


def AES_Encryption(content, key):
    return content+'#'+key


def AES_Decryption(content, key):
    return content.split('#')[0]

def keyGenerate(len=32):
    '''Generate key for encryption. Default length is 32 bytes (256 bits).

    :param len: The length of key, default length is 32 bytes (256 bits).

    '''
    return "key_gen_for_data_transfer"+time.strftime("%H:%M:%S")
