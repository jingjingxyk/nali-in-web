#!/usr/bin/python

# -*- coding: UTF-8 -*-

import concurrent.futures
import os
import subprocess

import time
import re
import sqlite3


def get_cmd(line):
    ips=' '.join(line)
    return f'{project_dir}/tools/nali-linux-amd64-v0.4.2 {ips}'


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
    with concurrent.futures.ThreadPoolExecutor(max_workers=(os.cpu_count()-1)) as executor:
        to_do = []
        for line in lines:

            future = executor.submit(execute_one, line)
            to_do.append(future)

        for future in concurrent.futures.as_completed(to_do):
            res.append(future.result())
    return res


# https://www.sqlite.org/lang_UPSERT.html
# “excluded”列名的表限定符

def deal_chunk(lines):

    #二次分片
    new_lines=[]
    new_chunk=[]
    for line in lines:
        new_chunk.append(line)
        if len(new_chunk) == 1000:
            new_lines.append(new_chunk)
            new_chunk=[]

    output=execute_all(new_lines)

    new_dict=dict()
    str=''
    # sql='INSERT INTO ipv4 ("ip","address") values'
    for line in output:
        arr=line.split("]  ")
        arr=[(el+']') for el in arr]
        for line2 in arr:
            arr = line2.split(" [")
            arr[1] = '[' + arr[1]
            arr[1]=arr[1].lstrip('[').rstrip(']')
            str+=arr[0]+'_xn--3px_'+arr[1]+"\n"

    with open(project_dir + '/ipv4_all.log', "a+") as f:
        f.write(str)
    '''
    
        sql+=f'("{arr[0]}","{arr[1]}"),'
    sql=sql.strip(',')
    sql=sql+' ON CONFLICT ( ip ) DO UPDATE SET address = excluded.address '
    print(sql)
    '''

    '''
    DELETE FROM table_name
    DELETE FROM sqlitesequece WHERE name='table_name'
    '''



    '''
    
    with sqlite3.connect(project_dir + '/ipv4_all.db') as dbh:

        #dbh.execute('DELETE FROM ipv4')
        #dbh.execute("DELETE FROM sqlite_sequence WHERE name='ipv4'")
        dbh.execute(sql)
    print(new_dict)
    
    '''

def createIPv4TableSQL():
    sql = '''
    create table ipv4 (
        'id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,
        'ip' char(36) not NULL UNIQUE,
        'address' varchar(200)  DEFAULT NULL,
        'location' varchar(200) DEFAULT NULL,
        'country' varchar(200) DEFAULT NULL,
        'country_code' varchar(200) DEFAULT NULL,
        'province' varchar(200) DEFAULT NULL,
        'province_code' varchar(200) DEFAULT NULL, 
        'city'   varchar(200) DEFAULT NULL,
        'city_code'   varchar(200) DEFAULT NULL,
        'town'   varchar(200) DEFAULT NULL,
        'town_code'   varchar(200) DEFAULT NULL,
        'area'   varchar(200) DEFAULT NULL,
        'area_code'   varchar(200) DEFAULT NULL,
        'district_code' int default 0
    )
    '''
    return sql


if __name__ == '__main__':
    project_dir = os.path.abspath(os.path.dirname(__file__) + '/../')
    start_time = time.perf_counter()

    '''
    with sqlite3.connect(project_dir + '/ipv4_all.db') as dbh:
        # dbh.execute('drop table ipv4')
        # dbh.execute(createIPv4TableSQL())
        cursor = dbh.execute('select * from ipv4 where id limit 100 ')
        for line in cursor:
            print(line)
    '''
    '''
     IP地址分为A类，B类和C类 ，其地址范围如下：
                A类地址：10.0.0.0～10.255.255.255 ；
                B类地址：172.16.0.0～172.31.255.255 ；
                C类地址：192.168.0.0～192.168.255.255
                 127.0.0.0/8 loopback
                
                skip 0.0.0.0/8 reserved,
               # 224.0.0.0/4 multicast, 240.0.0.0/4 reserved
    '''
    data_dict = dict()
    chunk = list()
    for i1 in list(range(1, 224)):
        if i1 == 10:
            continue
        if i1 == 127:
            continue
        for i2 in list(range(255)):
            if i1 == 172 and (i2 >= 16 or i2 <= 31):
                continue
            if i1 == 192 and i2 == 168:
                continue
            for i3 in list(range(0, 255)):
                for i4 in list(range(0, 255)):
                    ip = f"{i1}.{i2}.{i3}.{i4}"
                    chunk.append(ip)
                    if len(chunk) >= 10000:
                        s_time = time.perf_counter()
                        print('10000个ip已经生成,开始生成ip信息')
                        deal_chunk(chunk)
                        print('生成IP信息花费时间 {} 秒'.format(time.perf_counter() - s_time))

                        exit(0)


    exit()

    end_time = time.perf_counter()
    print('花费时间 {} 秒'.format(end_time - start_time))
