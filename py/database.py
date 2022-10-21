import time
import sqlite3

DATABSE_DIR = 'C:/Users/Andision/Documents/GitHub/NUIX/py/system.db'

# ==========INIT==========

TABLE_CONF = {
    'sys_paired_device': '(device_id primary key, device_name, init_time, init_key, init_verified, transfer_data_key,transfer_data_key_expire_time )',
    'app_airclip_clipboard': '(time primary key, content, device)'
}


def open_table(table):
    con = sqlite3.connect(DATABSE_DIR)
    con.execute('create table if not exists ' +
                table+TABLE_CONF[table])
    cur = con.cursor()

    return con, cur


def insert_item(con, cur, table, data):
    cur.execute('INSERT INTO '+table+TABLE_CONF[table]+' values(?,?,?)',)


def get_cur_search_result(cur):
    ret = []
    for row in cur:
        ret.append(row)

    return ret


# ==========SYSTEM==========


def sys_add_paired_device(device_id, device_name, init_time, init_key, init_verified=False):
    con, cur = open_table('sys_paired_device')
    cur.execute(
        'DELETE FROM sys_paired_device WHERE device_id="{}"'.format(device_id))
    cur.execute('INSERT INTO sys_paired_device(device_id, device_name,init_time, init_key, init_verified) values(?,?,?,?,?)',
                (device_id, device_name, init_time, init_key, init_verified))
    con.commit()


def sys_get_paired_device(device_id=None):
    '''Get paired device info in database.

    :param device_id: If given, this function will return the info of this device id. Else, this function will return all paired device.

    '''
    con, cur = open_table('sys_paired_device')
    # cur.execute('SELECT device_id, init_time, init_key, init_verified FROM sys_paired_device ')
    if device_id == None:
        cur.execute(
            'SELECT device_id, device_name, init_time, init_key, init_verified FROM sys_paired_device')
    else:
        cur.execute(
            'SELECT device_id, device_name, init_time, init_key, init_verified FROM sys_paired_device WHERE device_id="{}"'.format(device_id))
    return get_cur_search_result(cur)


def sys_verify_paired_device(device_id):
    con, cur = open_table('sys_paired_device')
    # cur.execute('SELECT device_id, init_time, init_key, init_verified FROM sys_paired_device ')
    cur.execute(
        'UPDATE sys_paired_device SET init_verified=1 WHERE device_id="{}"'.format(device_id))
    con.commit()


def sys_update_transfer_data_key(device_id, key, expired_time):
    con, cur = open_table('sys_paired_device')
    # cur.execute('SELECT device_id, init_time, init_key, init_verified FROM sys_paired_device ')
    print('UPDATE sys_paired_device SET transfer_data_key="{}",transfer_data_key_expire_time="{}" WHERE device_id="{}"'.format(key, expired_time, device_id))
    cur.execute(
        'UPDATE sys_paired_device SET transfer_data_key="{}",transfer_data_key_expire_time="{}" WHERE device_id="{}"'.format(key, expired_time, device_id))
    con.commit()


def sys_get_transfer_data_key(device_id):
    con, cur = open_table('sys_paired_device')
    # cur.execute('SELECT device_id, init_time, init_key, init_verified FROM sys_paired_device ')
    cur.execute(
        'SELECT transfer_data_key,transfer_data_key_expire_time FROM sys_paired_device WHERE device_id="{}"'.format(device_id))
    return get_cur_search_result(cur)

# ==========APP==========


def app_airclip_add_item(timestamp, content, device):
    # con=sqlite3.connect(DATABSE_DIR)
    # #创建表book:包含3列，id(主键，学号),name,tel
    # con.execute('create table if not exists clipboard(time primary key,content,device)')
    # #创建游标对象
    # cur=con.cursor()

    con, cur = open_table('app_airclip_clipboard')
    cur.execute('INSERT INTO app_airclip_clipboard(time,content,device) values(?,?,?)',
                (timestamp, content, device))
    con.commit()


def app_airclip_show_item():
    # con=sqlite3.connect(DATABSE_DIR)
    # #创建表book:包含3列，id(主键，学号),name,tel
    # con.execute('create table if not exists clipboard(time primary key,content,device)')
    # #创建游标对象
    # cur=con.cursor()
    con, cur = open_table('app_airclip_clipboard')

    cur.execute('SELECT time,content,device FROM app_airclip_clipboard')
    return get_cur_search_result(cur)


# ==========OLD==========
# 打开数据库


def open_db():
    # 创建SQLite数据库
    con = sqlite3.connect('./system.db')
    # 创建表book:包含3列，id(主键，学号),name,tel
    con.execute('create table if not exists book(id primary key,name,tel)')
    # 创建游标对象
    cur = con.cursor()
    return con, cur

# 查询全部信息


def show_all_db():
    print('******通讯录现有数据******')
    cur_1 = open_db()[1]
    cur_1.execute('SELECT id,name,tel FROM book')
    for row in cur_1:
        print(row)

# 输入信息


def into():
    name = input('请输入姓名：')
    id = input('请输入学号：')
    tel = input('请输入电话号码：')
    return name, id, tel

# 向数据库中添加内容


def add_db():
    print('******数据添加功能******')
    one = into()
    cur_1 = open_db()
    cur_1[1].execute(
        'INSERT INTO book(id,name,tel) values(?,?,?)', (one[1], one[0], one[2]))
    cur_1[0].commit()
    print('******数据添加成功******')

# 删除数据库中的内容


def DELETE_db():
    print('******数据删除功能******')
    del_id = input('请输入删除的学号：')
    del_id = ''' + del_id + '''
    cur_1 = open_db()
    cur_1[1].execute('DELETE FROM book WHERE id='+del_id)
    cur_1[0].commit()
    print('******数据删除成功******')
    show_all_db()
    # 关闭游标对象
    cur_1[1].close()

# 修改数据库中的内容


def alter_db():
    print('******数据修改功能******')
    change_id = input('请输入修改数据对应的学号：')
    change_id = '''+change_id+'''
    cur_1 = open_db()
    person = into()
    # 更新数据使用 SQL 语句中的 update
    cur_1[1].execute('update book set name = ? ,tel = ? WHERE id =' +
                     change_id, (person[0], person[2]))
    # 游标事务提交
    cur_1[0].commit()
    show_all_db()
    cur_1[1].close()

# 查询数据


def query_data():

    print('******数据查询功能******')
    choice_id = input('请输入查询数据对应的学号：')
    choice_id = ''' + choice_id + '''
    cur_1 = open_db()
    cur_1[1].execute('SELECT id,name,tel FROM book WHERE id ='+choice_id)
    print('******查询结果如下******')
    for row in cur_1[1]:
        print(row)
    cur_1[1].close()

# 是否继续


def conti(a):
    choice = input('是否继续：(1 表示继续，0 表示退出)')
    if choice == '1':
        a = 1
    else:
        a = 0
    return a


'''
主函数菜单内容：
1.向数据库中添加内容
2.删除数据库中的内容
3.修改数据库中的内容
4.查询数据库中的内容
选择你想要的进行的操作：

'''
if __name__ == '__main__':
    start_clock = time.time()
    a = 1
    print('******数据库通讯录******')
    while a:
        content = '''
1.向数据库中添加内容
2.删除数据库中的内容
3.修改数据库中的内容
4.查询数据库中的内容
5.显示数据库中的内容
6.关闭   数据库系统
选择你想要的进行的操作：     
        '''
        choice = input(content)
        if choice == '1':
            add_db()
            conti(a)
        elif choice == '2':
            DELETE_db()
            conti(a)
        elif choice == '3':
            alter_db()
            conti(a)
        elif choice == '4':
            query_data()
            conti(a)
        elif choice == '5':
            show_all_db()
            conti(a)
        elif choice == '6':
            a = 0
        else:
            print('输入错误，请重新输入')

    end_clock = time.time()
    print('RUNNING TIME:%s s' % (end_clock-start_clock))
