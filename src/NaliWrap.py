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
        cmd = f"{project_dir}/tools/nali-linux-amd64-v0.4.2 {ip}"
        record_log(cmd)
        output = cmd_exec(cmd)
        arr = output.split("]  ")
        arr = [(el + ']') for el in arr]
        for el in arr:
            new_arr = el.split(" [")
            new_arr[1] = '[' + new_arr[1]
            new_arr[1] = new_arr[1].lstrip('[').rstrip(']')
            result.append({
                'ip': new_arr[0],
                "addr": new_arr[1].strip(),
                "origin": el
            })
    return result


def main():
    print("HTTP/1.0 200\r\n", end="")

    print("content-type: application/json; charset=utf-8\r\n", end="")
    # print("Content-Type:text/html;charset=utf-8", end="\r\n")
    print('\r\n\r\n', end='')
    req = sys.stdin.readline()
    # req='/?ip=8.8.8.8'
    message = req.strip()
    record_log(message)
    data = match(message)
    result = {
        "code": 200,
        "data": [],
        "request_uri": message,
        "request_datetime": datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ"),
        "message": "no data"
    }
    if data:
        result["data"] = data
        result["message"] = "ok"

    print(json.dumps(result, ensure_ascii=False)+"\r\n\r\n", end='')


if __name__ == '__main__':

    project_dir = os.path.abspath(os.path.dirname(__file__) + '/../')
    record_log(project_dir)
    try:
        process_ids = 'ppid:{},pid:{},uid:{}'.format(os.getppid(), os.getpid(), os.getuid())
        request_time = ":request_time:" + datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")
        record_log(process_ids + " " + request_time)
        main()
    except Exception as e:
        record_log(repr(e))
        with open(project_dir + "/naliwrap.log", "a+") as f:
            traceback.print_tb(sys.exc_info()[2], file=f)
        result = {
            'code': 500,
            "message": "process excetpion; show detail , please see naliwrap.log"
        }
        print(json.dumps(result, ensure_ascii=False), end="\r\n")
