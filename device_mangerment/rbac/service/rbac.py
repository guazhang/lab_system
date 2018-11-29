from django.utils.deprecation import MiddlewareMixin

from django.shortcuts import HttpResponse,redirect,render

class PermissionValid(MiddlewareMixin):

    def process_request(self,request):

        valid_url=["/login/$","/reg/$","/admin/.*",
                   "/stark/app01/host/$",
                   "/get_valid_img/","/index/$",
                  "/logout/"]
        import re
        for url in valid_url:
            url="^%s$"%url
            ret=re.match(url,request.path_info)
            if ret:
                return None


        if not request.session.get("user_id"):
            return redirect("/login/")

        current_path = request.path_info

        # 方式1：
        # permission_list = request.session.get("permission_list")
        #
        # import re
        #
        # flag = False
        # for permission in permission_list:
        #     permission="^%s$"%permission
        #     ret = re.match(permission, current_path)
        #     if ret:
        #         flag = True
        #         break
        # if not flag:
        #     return HttpResponse("无权访问")

        # 方式2：

        permission_dict = request.session.get("permission_dict")
        print("PermissionValid",permission_dict)
        #PermissionValid
        #{'1': {'urls': ['/users/', '/users/add/', '/users/(\\d+)/change/'], 'codes': ['list', 'add', 'edit']},
        #'2': {'urls': ['/roles/'], 'codes': ['list']}}

        # PermissionValid
        # {'1': {'urls': ['/users/', '/users/add/', '/users/(\\d+)/change/'], 'codes': ['list', 'add', 'edit']},
        #  '2': {'urls': ['/roles/'], 'codes': ['list']}}



        # PermissionValid
        # {'3': {'urls': ['/stark/app01/switch/', '
        #               /stark/app01/switch/add'],
        #                'codes': ['list', 'add']},
        #  '1': {'urls': ['/stark/app01/user/',
        #                '/stark/app01/user/add/',
        #                '/stark/app01/user/(\\d+)/change/'],
        #                'codes': ['list', 'add', 'change']},
        #  '2': {'urls': ['/stark/app01/host/',
        #               '/stark/app01/host/add'],
        #               'codes': ['list', 'add']}}



        import re

        flag = False
        for item in permission_dict.values():
            urls=item["urls"]

            for permission in urls:
                 permission="^%s"%permission
                 print("rbac--path",permission,current_path)
                 ret = re.match(permission, current_path)
                 if ret:
                    print("codes",item.get("codes"))
                    request.codes=item.get("codes")
                    return None

        return HttpResponse("无权访问")



