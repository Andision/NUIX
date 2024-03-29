## 设备配对

参考蓝牙配对的模式进行设计。

> 由配对产生初始密钥Kint，然后产生链路密钥Kab，双方设备将Kab存储在各自的非易失性存储器中，这样以后的通迅不需要创建Kab，直接便能进入认证阶段。密钥和认证码的产生都有一套固定的算法，所以从数学角度来看，只要终端设备输入一致，在相同的算法下得出的结果也应该是一致的。


首先由PIN码、从设备蓝牙地址和一个主设备发给从设备的随机数共同产生初始密钥Kint。只要PIN码一致，产生的Kint便一致，当双方PIN码不匹配便配对失败。

> 链路密钥是由主从设备的蓝牙地址和主从设备各一随机数共同产生的，所以只要主从设备能互换该随机数便能得到一致的Kab，这点蓝牙是怎么做到的呢？主设备将随机数RandA与Kint异或的结果发给从设备，从设备将随机数RandB与Kint异或的结果发给主设备，由于双方已经有了一致的Kint，显然从设备只需( (RandA异或Kint）异或Kint)便能得到RandA，主设备亦然，这时双方输入一致了，便能产生一致的Kab。
> 
> 认证算法的输入是Kab、从设备地址和主设备发给从设备的随机数，结果一致则认证成功，显然只要Kab一致便能认证成功。认证成功便能建立链路级的连接了。
> 
> 显然：1、不配对是无法建立连接的，因为没有PIN码产生的Kint，便没有之后的Kab和认证；
> 2、设备的配对设备列表中存储的便是其物理地址及Kab（还有时钟信息），删除了该配对设备便删除了Kab，外部设备来连接时显然认证无法成功，这时是会触发再次配对的。

``` 
PAIRED_DEVICE_LIST={
    device_id :{
    timestamp = timestamp
    verified = bool
    init_random_int = str
    }
}

```

## 数据更新

设备检测到新的情景状态或产生新的感知数据，需要更新或触发特定的服务，向主机发送对应的数据或信号。

### 传输密钥交换

> 链路密钥是由主从设备的蓝牙地址和主从设备各一随机数共同产生的，所以只要主从设备能互换该随机数便能得到一致的Kab，这点蓝牙是怎么做到的呢？主设备将随机数RandA与Kint异或的结果发给从设备，从设备将随机数RandB与Kint异或的结果发给主设备，由于双方已经有了一致的Kint，显然从设备只需( (RandA异或Kint）异或Kint)便能得到RandA，主设备亦然，这时双方输入一致了，便能产生一致的Kab。

```

```

## 信号触发

在安装应用时，注册应用所需的信号类型。当收到信号时，通过各类型信号的应用需求列表和权限列表，使用消息队列维护各个应用所收到的触发信号。信号的应用列表是指所有可以被该类型信号所触发的应用的列表。权限列表指，对应可被触发的应用是否被用户允许使用当前信号触发。权限管理参考了安卓应用的权限管理模式

``` json
{
    "device_id":"device_id",
    "timestamp":TIME_STAMP,
    "data_type":DATA_TYPE,
    "payload":PAYLOAD
}
```

TODO

- 每个应用文件放一起，层次结构
- Socket.IO
- WIFI Direct