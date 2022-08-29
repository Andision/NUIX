from flask import Flask
import time
 
app = Flask(__name__) #在当前文件下创建应用

clip_list=[]
 
@app.route("/") #装饰器，url，路由
def index(): #试图函数
    return "hello world"
 
@app.route("/say_hello/<name>") #装饰器，url，路由
def say_hello(name): #试图函数
 
    return "hello world,I am your friend %s"%name

@app.route("/new_clip/<name>") #装饰器，url，路由
def new_clip(name): #试图函数
    curtime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    clip_list.append({'time':curtime,'content':name})
    return "new_clip: %s"%name

@app.route("/get_clip/") #装饰器，url，路由
def get_clip(): #试图函数

    ret = clip_list.copy()
    ret.reverse()
 
    return ret
 
if __name__ == "__main__":
    app.run(debug=True,port=5000) #运行app