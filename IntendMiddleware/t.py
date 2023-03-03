key_value ={}     

# 初始化
key_value[2] = 56       
key_value[1] = 2 
key_value[5] = 12 
key_value[4] = 24
key_value[6] = 18      
key_value[3] = 323 

def get_top(d,top):
    ret=[]
    for i in sorted(d.items(), key = lambda kv:(kv[1], kv[0]),reverse=True):
        if top==0:
            break
        top-=1
        ret.append(i)

    return [i[0] for i in ret]

print(get_top(key_value,2))
print(len(key_value))