from django.shortcuts import render
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "device_mangerment.settings")# project_name 项目名称
django.setup()
# Create your views here.
from django.shortcuts import render,HttpResponse,redirect

# Create your views here.
from django.contrib import auth
from app01.models import *
# from rbac.models import *
from app01.forms import LoginForm

from django.conf import settings# 仅用户自定义+内置
from app01.utils import dome_ping




class PermissionCode(object):
    def __init__(self,codes):
        self.codes=codes
    def list(self):
         return "list" in self.codes
    def add(self):
         return "add" in self.codes
    def edit(self):
         return "edit" in self.codes
    def delete(self):
         return "del" in self.codes


def users(request):

    user_list=User.objects.all()

    per=PermissionCode(request.codes)
    print("...users",per)
    menu_permission_list=request.session.get("menu_permission_list")

    print("menu_permission_list",menu_permission_list)
    return render(request,"users.html",locals())


def get_valid_img(request):

    from app01.utils import valid_code

    data=valid_code.get_valid_value(request)

    return HttpResponse(data)




def login(request):
    if request.method=="POST":
        user=request.POST.get("user")
        pwd=request.POST.get("pwd")
        input_valid_codes = request.POST.get("valid_code")
        keep_valid_codes = request.session.get("keep_valid_codes")
        login_response = {"user": None, "error_msg": ""}

        if keep_valid_codes.upper()==input_valid_codes.upper():
            users=User.objects.filter(name=user,pwd=pwd)[0]
            print(users)
            if users:
                print(">>>",users)

                request.session["user_id"]=users.pk
                login_response["user"] = users.name
                from rbac.service.initail import permission_session
                permission_session(users,request)

                # return redirect("/stark/app01/host/")
            else:
                login_response["error_msg"] = "username or password error!"
        else:
            login_response["error_msg"]="valid_code error!"
        import json
        return HttpResponse(json.dumps(login_response))

    return render(request,"login.html")




def login_without(request):
    if request.method=="POST":
        user=request.POST.get("user")
        pwd=request.POST.get("pwd")
        login_response = {"user": None, "error_msg": ""}

        users=User.objects.filter(name=user,pwd=pwd)[0]
        print(users)
        if users:
            print(">>>",users)

            request.session["user_id"]=users.pk
            login_response["user"] = users.name
            from rbac.service.initail import permission_session
            permission_session(users,request)

            # return redirect("/stark/app01/host/")
        else:
            login_response["error_msg"] = "username or password error!"
        import json
        return HttpResponse(json.dumps(login_response))

    return render(request,"login.html")












def register(request):

    if request.method== "POST":

        print("request.POST",request.POST)   # <QueryDict: {'user': ['123'], 'pwd': ['1231'], 'repeat_pwd': ['1231'], 'email': ['123'], 'csrfmiddlewaretoken': ['PjMKenIgrFYWY52U5EcYbkfmib2EiMzK19K5xv4qBon5XZbPDkuiMhMf2LqaV2wy']}>
        print("request.POST",request.POST.items)   # <QueryDict: {'user': ['123'], 'pwd': ['1231'], 'repeat_pwd': ['1231'], 'email': ['123'], 'csrfmiddlewaretoken': ['PjMKenIgrFYWY52U5EcYbkfmib2EiMzK19K5xv4qBon5XZbPDkuiMhMf2LqaV2wy']}>
        print("request.FILES",request.FILES) # request.FILES <MultiValueDict: {'avatar_img': [<InMemoryUploadedFile: linhaifeng.jpg (image/jpeg)>]}>
        reg_response = {"user": None, "error_mes": None}

        users= request.POST.get("user")
        pwd= request.POST.get("pwd")
        email = request.POST.get("email")
        teams = request.POST.get("team")
        import json
        teams=json.loads(teams)

        user_obj = User.objects.create(name=users, pwd=pwd, email=email)
        print(user_obj.id,user_obj)
        if user_obj and teams :
            reg_response["user"] = user_obj.name
            obj=User.objects.get(id=user_obj.id)
            # print(obj,obj)
            # print(obj.id)
            # print(teams)
            # for i in teams:
            obj.roles.add(*teams)
            # return redirect("/login/")

        else:
            reg_response["error_mes"]= "create failed"

        import json
        return HttpResponse(json.dumps(reg_response))

    else:
        roles = Role.objects.all()
        return render(request,"reg.html",locals())


def log_out(request):
    auth.logout(request)
    return redirect("/login/")


def index(request):
    return redirect("/stark/app01/host/list/")
    # return render(request,"index.html")





def register1(request):
    if request.method == "GET":
        roles = Role.objects.all()
        form = LoginForm()
        return render(request,'reg.html',{'form':form,"roles":roles})
    else:
        form = LoginForm(request.POST)
        print(form)
        if form.is_valid():
            # form.cleaned_data # {'username':'alex','password':'xxxx'}
            # models.UserInfo.objects.filter(username=form.cleaned_data['user'],password=form.cleaned_data['pwd'])
            # models.UserInfo.objects.filter(**{'username':'alex','password':123})
            # form.cleaned_data['password'] = md5(form.cleaned_data['password'])
            user = User.objects.filter(**form.cleaned_data).first()
            print(">>>>",user)
            if user:
                # 将用户信息放置到session中
                request.session[settings.USER_SESSION_KEY] = {'id':user.pk,'username':user.username }
                return redirect('/login/')
            else:
                form.add_error('password', '用户名或密码错误')
        return render(request, 'reg.html',{'form':form})




import json
from django.core import serializers
from django.http import JsonResponse

def ajax_sw(request):
    sw_id = request.POST.get("num1")
    print(sw_id)
    # sw_name = "Cisco-5020"
    sw_port = Switch.objects.filter(id=sw_id).values_list("switch_port__id","switch_port__sw_port_num")
    # print(sw_port)

    data=sw_port[:]
    # data= json.dumps(sw_port)
    # data= serializers.serialize("json",sw_port)
    print(dict(data))

    return JsonResponse(dict(data),safe=False)




def ajax_sw_port(request):
    ret = {"status": 1, "error": None}

    sw_id=request.POST.get("sw_id")
    sw_port_nid=str(request.POST.get("sw_port_nid"))
    # sw_port_name=str(request.POST.get("sw_port_name"))
    hostname=request.POST.get("hostname")
    # print(sw_id,sw_port_nid,sw_port_name,hostname)

    host_obj= Host.objects.filter(hostname=hostname)[0]
    sw_port_obj=Switch_Port.objects.filter(id=sw_port_nid)

    # sw_port_obj=Switch_Port.objects.filter(id=sw_port_nid).update(sw_port_num=sw_port_name)
    host_obj.sw=sw_port_obj
    host_obj.save()
    print("host_obj",host_obj)
    # print("sw_port_obj",sw_port_obj)

    # print(Host.objects.filter(hostname=hostname).values_list())
    return HttpResponse(json.dumps(ret))


import time
def timer_ping(req):
    hosts=[]
    host_staus=[]
    host_list_quert = Host.objects.all().values()
    for h in host_list_quert:
        hosts.append(h["hostname"])
        host_staus.append({h["hostname"]:h["device_status_id"]})

    host_ping_result=dome_ping.demo_ping(hosts)
    for host_result in host_ping_result:
        for k, v in host_result.get().items():
            print("%s k is %s,v is %s" % (time.ctime(),k, v))
            if v:
                Host.objects.filter(hostname=k).update(device_status_id=1)
            else:
                Host.objects.filter(hostname=k).update(device_status_id=2)
    print(hosts)
    print(host_staus)
    return HttpResponse("ok")


# http://127.0.0.1:8010/timer_ping/





