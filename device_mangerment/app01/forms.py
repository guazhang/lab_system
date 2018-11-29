#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'guazhang'
__mtime__ = '4/16/18'
"""


from app01 import models
from django.forms import Form
from django.forms import fields
from django.forms import widgets

from app01 import models

role_querset=models.Role.objects.values_list('id','title')



class LoginForm(Form):
    name = fields.CharField(
        label='用户名',
        required=True,
        error_messages={
            'required':'用户名不能为空'
        },
        widget=widgets.TextInput(attrs={'class':'form-control'})
    )
    pwd = fields.CharField(
        label='密码',
        required=True,
        error_messages={
            'required': '密码不能为空'
        },
        widget=widgets.PasswordInput(attrs={'class':'form-control'})
    )
    email = fields.EmailField(
        label="邮箱",
        required=True,
        error_messages={
            'required':"邮箱不能为空"
        },
        widget=widgets.EmailInput(attrs={'class':'form-control'})
    )
    roles = fields.MultipleChoiceField(
        label="组名",
        required=False,
        error_messages={
            'required':'组名不能为空'
        },
        choices=role_querset,#2,4
        widget=widgets.SelectMultiple(attrs={'class':'form-control'})
    )




