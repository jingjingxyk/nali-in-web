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
  "data": [
    {
      "ip": "101.36.109.208",
      "addr": "湖北省 教育网", 
      "origin": "101.36.109.208 [湖北省 教育网]"
    }, 
    {
      "ip": "100.1.1.1", "addr": "印度]",
      "origin": "100.1.1.1 [印度]]"
    }
  ], 
  "request_uri": "GET /nali-ip/101.36.109.208,100.1.1.1 HTTP/1.1", 
  "request_datetime": "2022-06-25T12:03:13Z", "message": "ok"
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