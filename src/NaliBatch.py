#!/usr/bin/python

# -*- coding: UTF-8 -*-

import concurrent.futures
import os
import subprocess

import time
import re


def get_cmd(line):
    result = re.search('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line)
    cmd = None
    if result is not None:
        ip = result.group(1)
        if ip is not None:
            cmd = f'{project_dir}/tools/nali-linux-amd64-v0.4.2 {ip}'
    return cmd


def execute_one(line):
    cmd = get_cmd(line)
    res = ''
    if cmd:
        ret = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8",
                             timeout=30)
        if ret.returncode == 0 and ret.stdout:
            res = ret.stdout.strip()
        else:
            print("error:", ret.stderr)
    return res


# 并发编程
def execute_all(lines):
    res = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        to_do = []
        for line in lines:
            future = executor.submit(execute_one, line)
            to_do.append(future)

        for future in concurrent.futures.as_completed(to_do):
            res.append(future.result())
    return res


if __name__ == '__main__':
    project_dir = os.path.abspath(os.path.dirname(__file__) + "/../")
    start_time = time.perf_counter()
    ips = [
        "114.114.114.114",
        "1.1.1.11",
        "2.114.114.112",
        "2.114.114.113",
        "114.3.114.115",
        "229.3.114.116",
        "3.34.114.117",
        "104.114.4.118",
        "2.114.4.119",
        "9.114.44.120",
        "114.114.5.121",
        "8.3.114.122",
        "2.114.1.123",
        "5.114.1.123",
        "3.14.1.123",
    ]
    print(len(ips))
    result = execute_all(ips)
    print('\n'.join(result))
    end_time = time.perf_counter()
    print('花费时间 {} 秒'.format(end_time - start_time))
