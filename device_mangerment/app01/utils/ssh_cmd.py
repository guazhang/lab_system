#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'guazhang'
__mtime__ = '11/16/18'
"""

import paramiko
import re
from django.conf import settings


class SSHConnection(object):
    def __init__(self, host, port,username,password):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._client=None

    def exec_command(self, command):
        try:
            self._client = paramiko.SSHClient()
            self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self._client.connect(self._host,self._port,self._username,self._password)
            # private_key = paramiko.RSAKey.from_private_key_file("%s/id_rsa" % settings.KEY)
            # self._client.connect(self._host,self._port,self._username,pkey=private_key)
        except Exception as e:
            print("ssh %s@%s get %s" %(self._username,self._host,e))
            exit()
        stdin, stdout, stderr = self._client.exec_command(command)
        channel= stdout.channel
        status=channel.recv_exit_status()
        data = stdout.read().decode("utf-8")
        if len(data) > 0:
            print(data.strip())
            return (status,data)
        err = stderr.read()
        if len(err) > 0:
            print(err.strip())
            return (status,err)

    def close(self):
        if self._client:
            self._client.close()


def get_fc_host_wwpn(host):
    try:
        conn = SSHConnection(host, settings.PORT,"root",settings.PASSWD)
        s,host_str = conn.exec_command('ls /sys/class/fc_host')
    except Exception as e:
        print("wwpn get error %s" % e )
        return []
    # print(">>>>>,%s %s" %(s,host_str))
    if s != 0:
        return []
    host_wwpns = []
    host_list = host_str.replace("\n", " ").strip().split(" ")
    for host in host_list:
        s,wwpn_str=conn.exec_command(" cat /sys/class/fc_host/%s/port_name" % host)
        host_wwpns.append(wwpn_str)
    conn.close()

    host_wwpn = []
    for wwpn in host_wwpns:
        wwpn = wwpn.lower()
        wwpn = re.sub("0x", "", wwpn)
        # remove all : characters from the entry, later on they will be added in correct order
        wwpn = wwpn.replace("\n", "")
        # append ":" every 2nd character
        wwpn = ":".join(wwpn[i:i + 2] for i in range(0, len(wwpn), 2))
        print("get host %s wwpn %s" %(host,wwpn))
        host_wwpn.append(wwpn)
    return host_wwpn


def get_remote_python_version(host):
    conn = SSHConnection(host, settings.PORT,"root",settings.PASSWD)
    stas,result = conn.exec_command('which python3')
    conn.close()
    if stas != 0:
        return "python2"
    return "python3"


