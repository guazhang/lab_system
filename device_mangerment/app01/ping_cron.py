#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'guazhang'
__mtime__ = '11/22/18'
"""



from app01.views import timer_ping

def task():
    print("begin to exe ping")
    timer_ping("req")
    return True
