#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import json
import os
import sys
import subprocess
import re
import fileinput
import traceback
from datetime import datetime
import asyncio
import tornado.web
import urllib


def record_log(log):
    with open(project_dir + "/naliwrap.log", "a+") as f:
        f.write(log + "\n")


def cmd_exec(cmd):
    ret = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8",
                         timeout=30)
    res = None
    if ret.returncode == 0:
        # print("success:", ret.stdout)
        res = ret.stdout
    else:
        record_log("cmd error: ---" + cmd + "------" + ret.stderr)
    return res


def match(message):
    search = re.findall("(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", message)
    result = []
    if search:
        ip = ' '.join(search)
        cmd = f"{project_dir}/tools/nali-linux-amd64-v0.5.3 {ip}"
        record_log(cmd)
        print('===============')
        output = cmd_exec(cmd)
        print(output)
        print('===============')
        arr = output.split("  ")
        print(arr)
        print('===============')
        arr = [(el.strip()) for el in arr]
        for el in arr:
            new_arr = el.split(" [")
            print(new_arr)
            new_arr[1] = new_arr[1].rstrip(']')
            result.append({
                'ip': new_arr[0],
                "addr": new_arr[1].strip(),
                "origin": el.strip()
            })
    return result


class MainHandler(tornado.web.RequestHandler):
    def options(self):
        self.set_status(200)
        self.set_header('Access-Control-Allow-Credentials', 'true')
        origin = ''
        if 'Origin' in self.request.headers:
            origin = self.request.headers['Origin']
        self.set_header('Access-Control-Allow-Origin', origin)
        self.set_header('Access-Control-Allow-Methods', 'GET,HEAD,POST,PUT,DELETE,CONNECT,OPTIONS,TRACE,PATCH')
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type")

    def get(self):
        print(self.request)
        print(self.request.headers)
        self.set_status(200)
        self.set_header("Content-type", "application/json")
        self.set_header('Access-Control-Allow-Credentials', 'true')
        origin = ''
        if 'Origin' in self.request.headers:
            origin = self.request.headers['Origin']
        self.set_header('Access-Control-Allow-Origin', origin)
        self.set_header('Access-Control-Allow-Methods', 'GET,HEAD,POST,PUT,DELETE,CONNECT,OPTIONS,TRACE,PATCH')
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type")
        response = {
            "code": 200,
            "message": "no data",
            "data": [],
            "request_uri": self.request.path + self.request.query,
            "request_datetime": datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ"),
        }

        print(self.request.path)
        print(self.request.query)

        if len(self.request.path) > 4:  # 如果带有参数
            params = urllib.parse.parse_qs(self.request.query)
            print(params)
            namespace = params["namespace"][0] if "namespace" in params else None
            print(namespace)
            response['data'] = match(self.request.path)

        self.write(json.dumps(response, ensure_ascii=False))


def make_app():
    return tornado.web.Application([
        (r"/.*", MainHandler)
    ])


async def main():
    app = make_app()
    app.listen(8080)
    await asyncio.Event().wait()


if __name__ == '__main__':

    project_dir = os.path.abspath(os.path.dirname(__file__) + '/../')
    record_log(project_dir)
    try:
        process_ids = 'ppid:{},pid:{},uid:{}'.format(os.getppid(), os.getpid(), os.getuid())
        request_time = ":request_time:" + datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")
        record_log(process_ids + " " + request_time)
        asyncio.run(main())
    except Exception as e:
        record_log(repr(e))
        with open(project_dir + "/naliwrap.log", "a+") as f:
            traceback.print_tb(sys.exc_info()[2], file=f)
            # logger.error(msg, exc_info=True) / logging.error(msg, exc_info=True)
            # logger.info(f'exception: {traceback.format_exc()}')
        result = {
            'code': 500,
            "message": "process excetpion; show detail , please see naliwrap.log"
        }
        print(json.dumps(result, ensure_ascii=False), end="\r\n")
