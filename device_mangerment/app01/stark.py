#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.utils.safestring import mark_safe
from django.shortcuts import HttpResponse, render
from django import forms
from stark.forms.widgets import DatePickerInput
from stark.service.stark import site, StarkConfig, get_choice_text, Option, StarkModelForm
from app01 import models
import app01.utils.ansible_check as ansible_check

from app01.utils import ssh_cmd
from django.conf.urls import url
from django.conf import settings
import os
import re


# # 业务线管理
class userconfig(StarkConfig):
    # 定制页面显示的列

    def display_user_role(self, row=None, header=False):
        if header:
            return "Role"
        s=[]
        for r in row.roles.all():
            s.append("<a href='/stark/app01/user/%s/role' style='padding:3px 6px'>%s</a>"%(r.pk,r.title))
        return mark_safe(" ".join(s))


    def role_info(self, request, nid):
        role_name=models.User.objects.filter(pk=nid).values_list("roles__title")
        role_group=models.User.objects.filter(pk=nid).values_list("roles__permissions__p_group__name")
        print(role_name, role_group)
        return render(request, 'host_group.html', locals())
        # return HttpResponse("ok")


    def user_role(self,row=None,header=False):
        if header:
            return 'check_details'
        return mark_safe("<a href='/stark/app01/user/%s/detail/'>check_details</a>" % row.id)

    def extra_url(self):
        """
        扩展URL
        :return:
        """
        from django.conf.urls import url
        patterns = [
            url(r'^(?P<nid>\d+)/detail/$', self.detail_view),
            url(r'^(?P<nid>\d+)/role/$', self.role_info),
        ]
        return patterns

    def detail_view(self, request, nid):
        """
        详细页面的视图函数
        :param request:
        :param nid:
        :return:
        """
        user_list = models.User.objects.filter(pk=nid)
        role_list = models.User.objects.filter(pk=nid).values_list("roles__title")
        print("role_list",role_list)

        context = {
            "user_list":user_list,
            'role_list':role_list,
        }
        return render(request, 'user_detail.html',context)

    list_display = [StarkConfig.display_checkbox, 'id', 'name',display_user_role,user_role]
    list_display_links = ["name"]
    # 定制模糊搜索
    search_list = ['name']
    # 排序
    order_by = ['-id', ]

    # 批量操作
    def multi_delete(self, request):
        pk_list = request.POST.getlist('pk')
        models.Role.objects.filter(id__in=pk_list).delete()
        # 无返回值，返回当前页面
        from django.shortcuts import redirect
        # 有返回值
        # return HttpResponse("ok")

    multi_delete.text = 'multi_delete'

    action_list = [multi_delete, ]


site.register(models.User, userconfig)



class roleconfig(StarkConfig):
    def display_role(self, row=None, header=False):
        if header:
            return "Role"
        s=[]
        for r in row.permissions.all():
            print(r)
            s.append("<a href='#' style='padding:3px 6px'>%s</a>"%(r.title))
        return mark_safe(" ".join(s))


    list_display = [StarkConfig.display_checkbox, "id", "title", display_role, ]
    list_display_links = ["title",]

    search_list = ['title',display_role]

    # 排序
    order_by = ['-id', ]

    # 批量操作
    def multi_delete(self, request):
        pk_list = request.POST.getlist('pk')
        models.Role.objects.filter(id__in=pk_list).delete()
        # 无返回值，返回当前页面
        from django.shortcuts import redirect
        # 有返回值
        # return HttpResponse("ok")

    multi_delete.text = 'multi_delete'

    action_list = [multi_delete, ]


site.register(models.Role, roleconfig)



from django.forms import models as form_model
from django.forms import fields
from django.forms import widgets
# 主机管理
class ServerModelForm(StarkModelForm):
    class Meta:
        model = models.Host
        # fields = "__all__"
        exclude = ('sw',)
        # fields = ["hostname","nickname","ip","roles",
        #           "cpus","mems","disks","CNAs","HBAs","boot_to","comments"]
        widgets = {
            'latest_date': DatePickerInput(attrs={'class': 'date-picker'})
        }



    switch_name =  fields.ChoiceField(
    choices=models.Switch.objects.all().values_list('id','switch_name'),
    widget=widgets.Select(attrs={"class":"sw_name"}),
    initial=2
    )
    #
    # print(">>>>1",switch_name1.choices)
    # switch_id= models.Switch.objects.all().values("switch_name")
    # print(">>>2",switch_id)
    # slot  = fields.ChoiceField(
    #     choices=models.Switch_Port.objects.filter(switch_name_id=switch_name1.choices[0]).values_list('slot','sw_port_num'),
    #     widget=widgets.Select
    # )
    #
    #

# class MyForm(ServerModelForm):
#     sw_port = fields.ChoiceField(
#         choices=models.Switch.objects.all().values_list('id','switch_name'),
#
#         widget=widgets.Select
#     )
#
#
#     switch_name1 =  fields.ChoiceField(
#     choices=models.Switch.objects.all().values_list('id','switch_name'),
#     widget=widgets.Select,
#     )
#
#     print(">>>>,", sw_port.choices)
#     print(">>>>,", switch_name1.choices)
#
#     def __init__(self, *args, **kwargs):
#         super(ServerModelForm, self).__init__(*args, **kwargs)
#         # self.fields['user'].widget.choices = ((1, '上海'), (2, '北京'),)
#         # 或
#         # self.fields['slot'].widget.choices = models.Switch_Port.objects.filter(switch_name_id=self.fields['slot'].choices[0]).values_list('slot', 'sw_port_num')
#         self.fields['switch_name1'].widget.choices = models.Switch.objects.all().values_list('id', 'switch_name')
#         self.fields['sw_port'].widget.choices = models.Switch_Port.objects.filter(switch_name_id=self.fields['sw_port'].choices[0]).values_list('id', 'switch_name__switch_name')
#




class ServerConfig(StarkConfig):
    # def display_status(self, row=None, header=False):
    #     if header:
    #         return '状态'
    #     from django.utils.safestring import mark_safe
    #     data = row.get_device_status_id_display()
    #     tpl = "<span style='color:green'>%s</span>" % data
    #     return mark_safe(tpl)


    def host_dep(self,row=None,header=False):
        if header:
            return "host_dep"
        s=[]
        for r in row.roles.all():
            print(r)
            s.append("<a href='/stark/app01/host/%s/role' style='padding:3px 6px'>%s</a>"%(row.pk,r.title))
        return mark_safe(" ".join(s))

    def host_role(self,request,nid):
        # role_list=models.Role.objects.filter(pk=id)[0]
        role_name=models.Host.objects.filter(pk=nid).values_list("roles__title")[0]
        role_group=models.Host.objects.filter(pk=nid).values_list("roles__permissions__p_group__name")
        print(role_name,role_group)

        return render(request, 'host_group.html', locals())


        # return HttpResponse("ok")



    def host_sw(self,row=None,header=False):
        if header:
            return "host_sw"
        s=[]
        for r in row.sw.all():
            print(r)
            # s.append("<a href='stark/app01/switch_port/?id=%s' style='padding:3px 6px'>%s.%s</a>"%(r.pk,r.switch_name,r.sw_port_num))
            s.append("<span style='padding:3px 6px'>%s.%s</apan>"%(r.switch_name,r.sw_port_num))
        return mark_safe(" ".join(s))

    # def host_switch(self,request,id):
    #     customer_distrbute_list = models.Switch_Port.objects.filter(pk=id)[0]
    #     print(customer_distrbute_list)
    #     return render(request, "my_customers.html", locals())



    def host_st(self,row=None,header=False):
        if header:
            return "host_st"
        s=[]
        for r in row.st.all():
            print(r)
            s.append("<a href='/stark/app01/host/%s/host_storage' style='padding:3px 6px'>%s.%s</a>"%(row.pk,r.storage_name,r.st_port_wwid))
            # s.append("<a href='/stark/app01/host/%s/host_storage' style='padding:3px 6px'>%s</a>"%(row.pk,r.storage_name))
        return mark_safe(" ".join(s))

    def host_storage(self,request,nid):

        st_name=models.Host.objects.filter(pk=nid).values_list("st__storage_name__name")[0]
        sw_name=models.Host.objects.filter(pk=nid).values_list("sw__switch_name__switch_name")[0]
        st_port= models.Host.objects.filter(pk=nid).values_list("st__st_port_wwid")[0]
        sw_port= models.Host.objects.filter(pk=nid).values_list("sw__sw_port_num")[0]
        sw_port_protocol= models.Host.objects.filter(pk=nid).values_list("sw__sw_port_protocol__protocol_name")[0]
        # for n in storage_port:
        #     print(n)

        context = {
            "st_name": st_name,
            "sw_name":sw_name,
            "st_port":st_port,
            "sw_port":sw_port,
            "sw_port_protocol":sw_port_protocol
        }
        print(context)
        return render(request, 'host_storage.html', locals())

        # return render(request, "my_customers.html", locals())



    def extra_url(self):
        # temp=[]
        # # temp.append(url("host_storage/(\d+)",self.host_storage))
        # temp.append(url("user_role/(?P<id>\d+)",self.user_role))
        # temp.append(url("host_switch/(?P<id>\d+)",self.host_switch))
        # temp.append(url("^(?P<nid>\d+)/host_storage/$", self.host_storage))
        # # temp.append(url(r'^(?P<nid>\d+)$', self.detail_view)),
        # print("temp",temp)
        # return temp

        patterns = [
            url(r'^(?P<nid>\d+)/host_storage/$', self.host_storage),
            url(r'^(?P<nid>\d+)/role/$', self.host_role),
            url(r'^(?P<nid>\d+)/detail/$', self.display_detail),
            url(r'^(?P<nid>\d+)/scan/$', self.display_scan),
        ]
        return patterns


    def scan(self,row=None,header=False):
        if header:
            return 'Scan'
        s = []

        # s.append("<a href='/stark/app01/host/%s/scan' style='padding:3px 6px'>%s</a>" % (
        s.append("<a href='/stark/app01/host/%s/scan' style='padding:3px 6px'><input id=id_scan type='button' value=%s></a>" % (
        row.pk, "scan" ))
        return mark_safe(" ".join(s))

    def display_scan(self,request, nid):

        host_obj= models.Host.objects.filter(pk=nid).values()[0]

        if os.path.exists("%s/%s.html" % (settings.SERVER_HTML[0],host_obj["nickname"])):
            print("retrun the before one ")
            return render(request, "%s.html" % host_obj["nickname"], locals())

        error = "the server %s can not connect with ansible " % host_obj["hostname"]

        CNA_info=host_obj["CNAs"]
        regex = re.compile(r'(((([a-z])?([0-9])?)+:)){1,}')
        print(">>>",CNA_info)

        if not ansible_check.scan_ping(host_obj["hostname"]):
            return HttpResponse(error)
        print("finish ping ")
        if CNA_info :
            print("get into wwpn")
            if not regex.search(CNA_info) :
                CNA_info += " ,".join([wwpn for wwpn in ssh_cmd.get_fc_host_wwpn(host_obj["hostname"])])
                models.Host.objects.filter(pk=nid).update(CNAs=CNA_info)
        print(host_obj, settings.SERVER_HTML[0])
        # wwpn_list=ssh_cmd.get_fc_host_wwpn(host_obj["hostname"])

        result_html=ansible_check.format_html(host_obj["hostname"],settings.SERVER_HTML[0],host_obj["nickname"])
        print(result_html)
        if not result_html:
            return HttpResponse(error)
        return render(request, result_html, locals())


    def nick_name(self,row=None,header=False):
        if header:
            return 'nick_name'
        s = []

        s.append("<a href='/stark/app01/host/%s/detail' style='padding:3px 6px'>%s</a>" % (
        row.pk, row.nickname))
        return mark_safe(" ".join(s))
        # return mark_safe("<a href='/stark/app01/user/%s/detail/'>%s</a>" % (row.id,))

    def display_detail(self, request, nid):
        """
        详细页面的视图函数
        :param request:
        :param nid:
        :return:
        """
        host_info = models.Host.objects.filter(pk=nid).values()
        st= models.Host.objects.filter(pk=nid).values("st__storage_name__name")
        sw= models.Host.objects.filter(pk=nid).values("sw__switch_name__switch_name")
        print("host_name",host_info,st,sw)

        return render(request, 'server_detail.html',locals())




    list_display = [
        StarkConfig.display_checkbox,
        # display_status,
        nick_name,
        host_dep,
        "disks",
        "CNAs",
        "boot_to",
        host_sw,
        host_st,
        get_choice_text('device_status_id', 'status'),
        scan]

    search_list = ['nickname', 'CNAs', 'host_sw',]
    list_display_links = ["nickname", ]
    # list_filter = [
    #     # Option('business_unit',condition={'id__gt':0},is_choice=False,text_func=lambda x:x.name,value_func=lambda x:x.id,is_multi=True),
    #     Option('business_unit', condition={'id__gt': 0}, is_choice=False, text_func=lambda x: x.name,
    #            value_func=lambda x: x.id),
    #     Option('device_status_id', is_choice=True, text_func=lambda x: x[1], value_func=lambda x: x[0]),
    # ]

    # 自定义ModelForm
    model_form_class = ServerModelForm


    # def extra_url(self):
    #     """
    #     扩展URL
    #     :return:
    #     """
    #     from django.conf.urls import url
    #     patterns = [
    #         url(r'^(?P<nid>\d+)/detail/$', self.detail_view),
    #     ]
    #     return patterns

    # def detail_view(self, request, nid):
    #     """
    #     详细页面的视图函数
    #     :param request:
    #     :param nid:
    #     :return:
    #     """
    #     nic_list = models.NIC.objects.filter(server_id=nid)
    #     memory_list = models.Memory.objects.filter(server_id=nid)
    #     disk_list = models.Disk.objects.filter(server_id=nid)
    #
    #     context = {
    #         'nic_list':nic_list,
    #         'memory_list':memory_list,
    #         'disk_list':disk_list,
    #     }
    #     return render(request, 'server_detail.html',context)
    def multi_delete(self, request):
        pk_list = request.POST.getlist('pk')
        models.Role.objects.filter(id__in=pk_list).delete()
        # 无返回值，返回当前页面
        from django.shortcuts import redirect
        # 有返回值
        # return HttpResponse("ok")

    multi_delete.text = 'multi_delete'

    action_list = [multi_delete, ]

site.register(models.Host, ServerConfig)











class Headwareconfig(StarkConfig):
    list_display = ["id", "host","details"]
    list_display_links = ["host",]

    search_list = ['host',]

    # 排序
    order_by = ['-id', ]

    # 批量操作
    def multi_delete(self, request):
        pk_list = request.POST.getlist('pk')
        models.Role.objects.filter(id__in=pk_list).delete()
        # 无返回值，返回当前页面
        from django.shortcuts import redirect
        # 有返回值
        # return HttpResponse("ok")

    multi_delete.text = '批量操作'

    action_list = [multi_delete, ]


site.register(models.Headware,Headwareconfig)


class Protocolconfig(StarkConfig):
    list_display = ["id", "protocol_name",
                    ]
    list_display_links = ["protocol_name",]

    search_list = ['protocol_name',]

    # 排序
    order_by = ['-id', ]

    # 批量操作
    def multi_delete(self, request):
        pk_list = request.POST.getlist('pk')
        models.Role.objects.filter(id__in=pk_list).delete()
        # 无返回值，返回当前页面
        from django.shortcuts import redirect
        # 有返回值
        # return HttpResponse("ok")

    multi_delete.text = '批量操作'

    action_list = [multi_delete, ]


site.register(models.Protocol,Protocolconfig)



class Switchconfig(StarkConfig):
    def display_protocol(self, row=None, header=False):
        if header:
            return "protocol"
        s=[]
        for r in row.protocol.all():
            s.append("<span  style='padding:3px 6px'>%s</span>"%(r.protocol_name))
        return mark_safe(" ".join(s))


    list_display = ["id", "switch_name",
                    "ip",
                    "user","passwd",
                    display_protocol,
                    "license_start","license_end"]
    list_display_links = ["name",]

    search_list = ['name',]

    # 排序
    order_by = ['-id', ]

    # 批量操作
    def multi_delete(self, request):
        pk_list = request.POST.getlist('pk')
        models.Role.objects.filter(id__in=pk_list).delete()
        # 无返回值，返回当前页面
        from django.shortcuts import redirect
        # 有返回值
        # return HttpResponse("ok")

    multi_delete.text = '批量操作'

    action_list = [multi_delete, ]

site.register(models.Switch,Switchconfig)




class Storageconfig(StarkConfig):

    def display_protocol(self, row=None, header=False):
        if header:
            return "protocol"
        s=[]
        for r in row.protocol.all():
            s.append("<span  style='padding:3px 6px'>%s</span>"%(r.protocol_name))
        return mark_safe(" ".join(s))



    list_display = ["id", "name",
                    display_protocol,
                    "ip","license_start",
                    "license_end"]
    list_display_links = ["name",]

    search_list = ['name',]

    # 排序
    order_by = ['-id', ]

    # 批量操作
    def multi_delete(self, request):
        pk_list = request.POST.getlist('pk')
        models.Role.objects.filter(id__in=pk_list).delete()
        # 无返回值，返回当前页面
        from django.shortcuts import redirect
        # 有返回值
        # return HttpResponse("ok")

    multi_delete.text = '批量操作'

    action_list = [multi_delete, ]



site.register(models.Storage,Storageconfig)


class Switch_Portconfig(StarkConfig):

    list_display = ["id", "switch_name",
                    "port_speed",
                    "sw_port_num","sw_port_protocol",
                    "slot"]
    list_display_links = ["switch_name",]

    search_list = ['switch_name',]

    # 排序
    order_by = ['-id', ]

    # 批量操作
    def multi_delete(self, request):
        pk_list = request.POST.getlist('pk')
        models.Role.objects.filter(id__in=pk_list).delete()
        # 无返回值，返回当前页面
        from django.shortcuts import redirect
        # 有返回值
        # return HttpResponse("ok")

    multi_delete.text = '批量操作'

    action_list = [multi_delete, ]

    # def extra_url(self):
        # temp=[]
        # # temp.append(url("host_storage/(\d+)",self.host_storage))
        # temp.append(url("user_role/(?P<id>\d+)",self.user_role))
        # temp.append(url("host_switch/(?P<id>\d+)",self.host_switch))
        # temp.append(url("^(?P<nid>\d+)/host_storage/$", self.host_storage))
        # # temp.append(url(r'^(?P<nid>\d+)$', self.detail_view)),
        # print("temp",temp)
        # return temp

        # patterns = [
        #     url(r'^sw_multi_add/$', self.multi_add),
        #     # url(r'^(?P<nid>\d+)/detail/$', self.display_detail),
        # ]
        # return patterns


    # def multi_add(self,m):
    #     for i in range(1,17):
    #         models.Switch_Port.objects.create(switch_name_id=2,
    #                                           port_speed="10Ge",
    #                                           sw_port_num="Eth3/%s" %i,
    #                                           sw_port_protocol_id=2,
    #                                           slot="3")
    #     return HttpResponse("ok")


site.register(models.Switch_Port,Switch_Portconfig)




class Storage_Portconfig(StarkConfig):
    # def display_role(self, row=None, header=False):
    #     if header:
    #         return "角色权限"
    #     s=[]
    #     for r in row.permissions.all():
    #         print(r)
    #         s.append("<a href='#' style='padding:3px 6px'>%s</a>"%(r.title))
    #     return mark_safe(" ".join(s))


    list_display = ["id", "storage_name",
                    "storage_port_speed",
                    "st_port_wwid","st_port_protocol",
                    "slot"]
    list_display_links = ["storage_name",]

    search_list = ['storage_name',]

    # 排序
    order_by = ['-id', ]

    # 批量操作
    def multi_delete(self, request):
        pk_list = request.POST.getlist('pk')
        models.Role.objects.filter(id__in=pk_list).delete()
        # 无返回值，返回当前页面
        from django.shortcuts import redirect
        # 有返回值
        # return HttpResponse("ok")

    multi_delete.text = '批量操作'

    action_list = [multi_delete, ]

site.register(models.Storage_Port,Storage_Portconfig)