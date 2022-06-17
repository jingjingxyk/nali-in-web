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
    search = re.search("(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", message)
    result = {}
    if search is not None:
        ip = search.group(1)
        cmd = f"{project_dir}/tools/nali-linux-amd64-v0.4.2 {ip}"
        output = cmd_exec(cmd)
        addr = output.replace(ip, '')
        if output is not None:
            result['ip'] = ip
            result['addr'] = addr.strip()
            result['origin'] = output

    return result


def main():
    print("HTTP/1.1 200", end="\r\n")
    print("Content-Type:application/json;charset=utf-8", end="\r\n")
    # print("Content-Type:text/html;charset=utf-8", end="\r\n")
    print("", end="\r\n")

    req = sys.stdin.readline()
    # req='/?ip=8.8.8.8'
    message = req.strip()
    info = match(message)
    result = {
        'code': 404,
        "request_uri": message,
        "request_datetime": datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ"),
        "message": "no data"
    }
    if info:
        result["code"] = 200
        result["ip"] = info["ip"]
        result["addr"] = info["addr"]
        result['origin'] = info['origin']
        result["message"] = "ok"

    print(json.dumps(result, ensure_ascii=False), end="\r\n")


if __name__ == '__main__':
    project_dir = os.path.abspath(os.getcwd())
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
