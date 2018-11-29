from django.contrib import admin

# Register your models here.

#
#
# from stark.service.stark import site,ModelStark
# from django.utils.safestring import mark_safe
# from .models import *
# from django.shortcuts import HttpResponse,redirect,render
# from django.conf.urls import url
#
#
# from stark.service.stark import site
#
# class userconfig(ModelStark):
#
#     def display_user_role(self,obj=None,is_header=False):
#         if is_header:
#             return "角色"
#         s=[]
#         for r in obj.roles.all():
#             s.append("<a href='/stark/app01/role/?id=%s' style='padding:3px 6px'>%s</a>"%(r.pk,r.title))
#         return mark_safe(" ".join(s))
#
#     def user_role(self,request,id):
#         customer_distrbute_list=Role.objects.filter(pk=id)[0]
#         print(customer_distrbute_list)
#         return render(request,"my_customers.html",locals())
#         # print(user_id)
#         # return HttpResponse("ok")
#
#
#     def extra_url(self):
#         temp=[]
#         temp.append(url("(?P<id>\d+)",self.user_role))
#         print("temp",temp)
#         return temp
#
#     list_display = ["id","name",display_user_role]
#     list_display_links = ["name"]
#
# site.register(User,userconfig)
#
# class roleconfig(ModelStark):
#     def display_role(self,obj=None,is_header=False):
#         if is_header:
#             return "角色权限"
#         s=[]
#         for r in obj.permissions.all():
#             print(r)
#             s.append("<a href='#' style='padding:3px 6px'>%s</a>"%(r.title))
#         return mark_safe(" ".join(s))
#
#     list_display = ["id","title",display_role]
#     list_display_links = ["title"]
# site.register(Role,roleconfig)
#
# class perconfig(ModelStark):
#     list_display = ["id","title","url","p_group","code"]
#     list_display_links = ["title"]
# site.register(Permission,perconfig)
#
# site.register(PermissionGroup)
#
# class hostconfig(ModelStark):
#
#     def host_dep(self,obj=None,is_header=False):
#         if is_header:
#             return "host_dep"
#         s=[]
#         for r in obj.roles.all():
#             print(r)
#             s.append("<a href='/stark/app01/role/?id=%s' style='padding:3px 6px'>%s</a>"%(r.pk,r.title))
#         return mark_safe(" ".join(s))
#
#     def user_role(self,request,id):
#         customer_distrbute_list=Role.objects.filter(pk=id)[0]
#         print(customer_distrbute_list)
#         return render(request,"my_customers.html",locals())
#         # print(user_id)
#         # return HttpResponse("ok")
#
#
#
#
#     def host_sw(self,obj=None,is_header=False):
#         if is_header:
#             return "host_sw"
#         s=[]
#         for r in obj.sw.all():
#             print(r)
#             s.append("<a href='stark/app01/switch_port/?id=%s' style='padding:3px 6px'>%s.%s</a>"%(r.pk,r.switch_name,r.sw_port_num))
#         return mark_safe(" ".join(s))
#     def host_switch(self,request,id):
#         customer_distrbute_list = Switch_Port.objects.filter(pk=id)[0]
#         print(customer_distrbute_list)
#         return render(request, "my_customers.html", locals())
#
#
#
#
#     def host_st(self,obj=None,is_header=False):
#         if is_header:
#             return "host_st"
#         s=[]
#         for r in obj.st.all():
#             print(r)
#             s.append("<a href='stark/app01/storage_port/?id=%s' style='padding:3px 6px'>%s.%s</a>"%(obj.pk,r.storage_name,r.st_port_wwid))
#         return mark_safe(" ".join(s))
#
#     def host_storage(self,request,id):
#         customer_distrbute_list = Storage_Port.objects.filter(pk=id)[0]
#         print(customer_distrbute_list)
#         return render(request, "my_customers.html", locals())
#
#
#     def extra_url(self):
#         temp=[]
#         temp.append(url("host_storage/(\d+)",self.host_storage))
#         temp.append(url("user_role/(?P<id>\d+)",self.user_role))
#         temp.append(url("host_switch/(?P<id>\d+)",self.host_switch))
#         print("temp",temp)
#         return temp
#
#
#     list_display = ["nickname",host_dep,"disks","CNAs","boot_to",host_sw,host_st]
#     list_display_links = ["nickname"]
#
# site.register(Host,hostconfig)
# site.register(Headware)
# site.register(Protocol)
# site.register(Switch)
# site.register(Storage)
# site.register(Switch_Port)
# site.register(Storage_Port)

# admin.site.register(sw_port)
# admin.site.register(st_port)
# admin.site.register(Storage)