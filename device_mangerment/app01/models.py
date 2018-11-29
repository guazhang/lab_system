from django.db import models

# Create your models here.
#
# class UserInfo(models.Model):
#     """
#     员工表
#     """
#
#     # auth=models.OneToOneField("")
#     name = models.CharField(verbose_name='员工姓名', max_length=16)
#     # username = models.CharField(verbose_name='用户名', max_length=32)
#     # password = models.CharField(verbose_name='密码', max_length=64)
#     email = models.EmailField(verbose_name='邮箱', max_length=64)
#     depart = models.ForeignKey(verbose_name='部门', to="Department", to_field="code")
#
#     def __str__(self):
#         return self.name






class User(models.Model):
    name=models.CharField(max_length=32,verbose_name='user_name')
    pwd=models.CharField(max_length=32)
    email = models.EmailField(verbose_name='email', max_length=64)
    roles= models.ManyToManyField("Role")
    def __str__(self):
        return self.name

class Role(models.Model):
    title=models.CharField(max_length=32)
    permissions=models.ManyToManyField("Permission")
    # users = models.ManyToManyField("User")
    def __str__(self):
        return self.title

class Permission(models.Model):
    url=models.CharField(max_length=32)
    title=models.CharField(max_length=32)
    p_group=models.ForeignKey("PermissionGroup",default=1)
    code=models.CharField(max_length=32,default="list",)
    def __str__(self):
        return "%s.%s"%(self.title,self.code)


class PermissionGroup(models.Model):
    name=models.CharField(max_length=32)

    def __str__(self):
        return self.name



#
# class Department(models.Model):
#     """
#     部门表
#     市场部     1000
#     销售       1001
#
#     """
#     title = models.CharField(verbose_name='部门名称', max_length=16)
#     code = models.IntegerField(verbose_name='部门编号', unique=True, null=False)
#
#     def __str__(self):
#         return self.title




class Headware(models.Model):
    host = models.ForeignKey(verbose_name='device_name',to="Host", max_length=128)
    details = models.CharField(verbose_name='details device name', max_length=128)

    def __str__(self):
        return self.host


class Protocol(models.Model):
    protocol_name = models.CharField(verbose_name='protocol_name', max_length=128)
    # device_name =  models.ManyToManyField(verbose_name="设备名称",to=Headware,max_length=60)

    def __str__(self):
        return self.protocol_name


class Switch(models.Model):
    switch_name= models.CharField(verbose_name='sw_name', max_length=128)
    ip = models.CharField(verbose_name='ip', max_length=64)
    user=models.CharField(verbose_name='switch_username', max_length=64)
    passwd = models.CharField(verbose_name='sw_passwd', max_length=64)
    protocol = models.ManyToManyField(verbose_name="sw_protocol",to="Protocol",max_length=60)
    license_start = models.DateField( auto_now_add=True,null=True,blank=True)
    license_end = models.DateField( auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return self.switch_name


class Storage(models.Model):
    name= models.CharField(verbose_name='st_name', max_length=128)
    ip = models.CharField(verbose_name='ip', max_length=64)
    protocol = models.ManyToManyField(verbose_name="protocol",to="Protocol",max_length=60)
    license_start = models.DateField(auto_now_add=True,null=True,blank=True)
    license_end = models.DateField(auto_now_add=True,null=True,blank=True)
    # port_name = models.CharField(verbose_name='端口名称', max_length=128)

    def __str__(self):
        return self.name



class Storage_Port(models.Model):
    storage_name=models.ForeignKey(verbose_name="st_name",to="Storage",max_length=64)
    storage_port_speed=models.CharField(verbose_name="port_speed",max_length=64)
    st_port_wwid=models.CharField(verbose_name="WWPN",max_length=128)
    st_port_protocol = models.ForeignKey(verbose_name="protocol", max_length=64, to="Protocol")
    slot = models.CharField(max_length=128, default=1)

    def __str__(self):
        return "%s.%s"%(self.storage_name,self.st_port_wwid)


class Host(models.Model):
    device_status_choices = (
        (1, 'PowerOn'),
        (2, 'PowerOff'),
        # (3, 'offline'),

    )
    hostname = models.CharField(verbose_name='host_name', max_length=128)
    nickname = models.CharField(verbose_name='nickname', max_length=32)
    ip = models.CharField(verbose_name='ip', max_length=64,null=True,blank=True)
    roles = models.ManyToManyField(verbose_name='dep', to="Role")
    license_start = models.DateField( auto_now_add=True,null=True,blank=True)
    license_end = models.DateField( auto_now_add=True,null=True,blank=True)
    cpus = models.CharField(verbose_name='cpu', max_length=128)
    mems = models.CharField(verbose_name='mem', max_length=128)
    disks = models.CharField(verbose_name='disks', max_length=128)
    CNAs = models.CharField(verbose_name='CNAs', max_length=128,blank=True, null=True)
    HBAs = models.CharField(verbose_name='HBAs', max_length=128,blank=True, null=True)
    boot_to = models.CharField(verbose_name='boot_to', max_length=128)
    sw=models.ManyToManyField(verbose_name="host connect swtich",to="Switch_Port",default="don't have sw")
    st = models.ManyToManyField(verbose_name="host connect storage", to="Storage_Port",default="don't have st")
    device_status_id = models.IntegerField(verbose_name='状态', choices=device_status_choices, default=1)
    comments = models.TextField(verbose_name='note', blank=True, null=True)

    def __str__(self):
        return self.hostname

class Switch_Port(models.Model):
    switch_name = models.ForeignKey(verbose_name="sw_name", max_length=64, to="Switch")
    port_speed= models.CharField(verbose_name='speed', max_length=128)
    # slot = models.CharField(max_length=128,)
    sw_port_num=models.CharField(verbose_name="sw_port",max_length=64)
    sw_port_protocol=models.ForeignKey(verbose_name="port_protocol",max_length=64,to="Protocol")
    slot = models.CharField(max_length=128, default=1)
    def __str__(self):
        return "%s.%s"%(self.switch_name,self.sw_port_num)
