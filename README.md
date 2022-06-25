# 简易 nali web 工具


## 启动
```shell
sh start-web-server.sh

```
## http 请求例子
```
http://127.0.0.1:8080/?ip=2.2.2.2

# response
{
    code: 200,
    request_uri: "GET /?ip=2.2.2.2 HTTP/1.1",
    request_datetime: "2022-06-17T03:09:45Z",
    message: "ok",
    ip: "2.2.2.2",
    addr: "[法国 Orange]",
    origin: "2.2.2.2 [法国 Orange] "
}
```

## 批量获取 ip地址信息

```
python3 src/NaliBatch.py

```
## 更新 IP 数据库
```shell 
nali-linux-amd64-v0.4.2 update 
```


## 使用 supervisor 或者  systemd 或者 docker 守护运行 


## 参考
1. [nali](https://github.com/zu1k/nali.git)
2. [ip-database](https://github.com/itbdw/ip-database.git)