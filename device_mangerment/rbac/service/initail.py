



def permission_session(user,request):
    # 将当前user的所有权限注入session中


    # # 方式1：
    # permissions = user.roles.all().values("permissions__url").distinct()
    # permission_list = []
    # for i in permissions:
    #     permission_list.append(i.get("permissions__url"))
    #
    # request.session["permission_list"] = permission_list

    # 方式2：
    permissions = user.roles.all().values("permissions__url","permissions__p_group_id","permissions__code").distinct()

    print("permission_session",permissions)
    """
        permission_session < QuerySet[
        {'permissions__code': 'list', 'permissions__url': '/users/', 'permissions__p_group_id': 1}, {
            'permissions__code': 'add', 'permissions__url': '/users/add/', 'permissions__p_group_id': 1}, {
            'permissions__code': 'edit', 'permissions__url': '/users/(\\d+)/change/', 'permissions__p_group_id': 1}, {
            'permissions__code': 'list', 'permissions__url': '/roles/', 'permissions__p_group_id': 2}] >

    """

    permission_dict={}
    for permission in permissions:
        p_group_id=permission.get("permissions__p_group_id")

        if p_group_id in permission_dict:
            permission_dict[p_group_id]["urls"].append(permission.get("permissions__url"))
            permission_dict[p_group_id]["codes"].append(permission.get("permissions__code"))
        else:
            permission_dict[p_group_id]={
                  "urls":[permission.get("permissions__url")],
                  "codes":[permission.get("permissions__code")],}

    print(permission_dict)

    request.session["permission_dict"]=permission_dict
    #######################################################################################

    # 用于菜单展示权限:
    permissions = user.roles.all().values("permissions__url","permissions__title","permissions__code").distinct()
    menu_permission_list=[]

    for item in permissions:
        if item["permissions__code"]=="list":
            menu_permission_list.append(item)
    print(menu_permission_list)

    request.session["menu_permission_list"]=menu_permission_list

