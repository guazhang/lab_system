#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'guazhang'
__mtime__ = '11/21/18'
"""


import multiprocessing
import subprocess

def fun_ping(host):
    status=True
    cmd="ping -c 1 -w 3 %s" % host
    print(cmd)
    p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p.wait()
    # print(p.returncode)
    if p.returncode != 0:
        print("the host %s ping failed ,%s" % (host,subprocess.PIPE))
        # p.kill()
        status=False
        return {host:status}
    return {host:status}


def demo_ping(host_list):
    result = []
    pool=multiprocessing.Pool(20)
    for host in host_list:
        result.append(pool.apply_async(fun_ping,(host,)))

    pool.close()
    pool.join()
    # for ret in result:
    #     print(">>>",ret.get())
    print("all done")
    return result







