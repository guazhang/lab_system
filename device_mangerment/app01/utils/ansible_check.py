#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'guazhang'
__mtime__ = '11/14/18'
"""

import os
from .cmdline import run
from django.conf import settings
from .ssh_cmd import get_remote_python_version


def install_ansible():
    print("check if install ansibel package")
    if not run("which ansible"):
        return True
    print("will install ansible package")
    ret,out=run("yum install ansible",True,True)
    if ret != 0:
        print("FAIL: install ansible, and out is [%s]" % out)
        return False
    return True

def install_ansible_cmdb():
    if not run("which ansible-cmdb"):
        print("check if have installed")
        return True
    run("pip install ansible-cmdb  ")
    if run("which ansible-cmdb"):
        return False
    return True


def cfg_ansible():
    if not install_ansible():
        return False
    if not os.path.isfile("ansible.cfg"):
        print("FAIL : the cfg is not here")
        return False
    ret,out=run("cp ansible.cfg  ~/.ansibel.cfg", True,True)
    if ret:
        print("FAIL: cp cfg, out is [%s]" % out)
        return False
    return True

def scan_ping(host):
    if not cfg_ansible():
        return False
    print("the scan host is %s" % host)
    with open("host_cfg","w") as f:
        f.write(host)
    # cmd="ansible all -i host_cfg -u root -m ping"
    cmd="ping -w 2 -c 1 %s" % host
    ret,out=run(cmd,True,True,True)
    if ret:
        print("FAIL: ping out is [%s]" % out)
        return False
    args = "-oUserKnownHostsFile=/dev/null -oStrictHostKeyChecking=no -oConnectTimeout=3 -oConnectionAttempts=3"
    cmd="sshpass -p  %s ssh-copy-id %s -i %s/id_rsa.pub root@%s" % (settings.PASSWD,args,settings.KEY ,host)
    ret,out=run(cmd,True,True)
    if ret :
        print("FAIL to copy ssh pub key to host %s " % host)
        return False
    return True


def get_info(host):
    print("the info in server %s" %(host))
    with open("host_cfg","w") as f:
        f.write(host)
    if not os.path.exists("cmdb_out_bak"):
        run("mkdir cmdb_out_bak")
    if os.path.exists("cmdb_out"):
        run("mv cmdb_out/* cmdb_out_bak/")
    run("mkdir cmdb_out")
    key=" --private-key=%s/id_rsa" % settings.KEY
    python_v=get_remote_python_version(host)
    interpreter="-e 'ansible_python_interpreter=/usr/bin/%s'" % python_v
    cmd="ansible all -i host_cfg -u root -m setup --tree cmdb_out/ %s %s " % (key,interpreter)
    ret,out=run(cmd,True,)
    if ret :
        print("FAIL: Can not exe ansibel cmd %s and out is %s" % (cmd,out))
        return False
    return True


def format_html(host,path,name):
    print("check ansible-cmdb cmd")
    if not get_info(host):
        print("can not get info from %s" % host)
        return False
    ret,out=run("ansible-cmdb cmdb_out/ > %s/%s.html" %(path,name),True,False)
    if ret :
        print("FAIL : Can not get the html with ansible-cmdb,out is %s" % out)
        return False
    print("get the html %s/%s.html" %(path,name))
    return "%s/%s.html" %(path,name)





