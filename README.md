# 简易 nali web 工具
> 为[`nali`](https://github.com/zu1k/nali.git)增加 基于python3 的 http 查询接口

## 启动

```shell
sh start-web-server.sh

```
## [http request ](http://localhost:8080/nali-ip/101.36.109.208,100.1.1.1)
```text
http://localhost:8080/nali-ip/101.36.109.208,100.1.1.1
```

## response
```json
{
    "code": 200,
    "message": "no data",
    "data": [
        {
            "ip": "101.36.109.208",
            "addr": "香港 UCloud",
            "origin": "101.36.109.208 [香港 UCloud]"
        },
        {
            "ip": "100.1.1.1",
            "addr": "印度",
            "origin": "100.1.1.1 [印度]"
        }
    ],
    "request_uri": "/nali-ip/101.36.109.208,100.1.1.1",
    "request_datetime": "2022-10-09T09:38:22Z"
}
```

## 批量获取 ip地址信息

```
python3 src/NaliBatch.py

```
## 更新 IP 数据库
```shell 
nali-linux-amd64-v0.5.3 update 
```


## 使用 supervisor 或者  systemd 或者 docker 守护运行 


## 参考
1. [nali](https://github.com/zu1k/nali.git)
2. [ip-database](https://github.com/itbdw/ip-database.git)
3. [IP地址批量查询](http://www.1234i.com/)

```text
/venv/bin/python3 /venv/bin/gunicorn --timeout 86400 --bind [::]:80 -w 1 --threads 25 --access-logfile - -c gunicorn_config.py
```