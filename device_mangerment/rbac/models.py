from django.db import models

# Create your models here.


class User(models.Model):
    name=models.CharField(max_length=32)
    pwd=models.CharField(max_length=32)
    roles=models.ManyToManyField("Role")

    def __str__(self):
        return self.name

class Role(models.Model):
    title=models.CharField(max_length=32)
    permissions=models.ManyToManyField("Permission")
    def __str__(self):
        return self.title

class Permission(models.Model):
    url=models.CharField(max_length=32)
    title=models.CharField(max_length=32,default="")
    p_group=models.ForeignKey("PermissionGroup",default=1)
    code=models.CharField(max_length=32,default="list",)
    def __str__(self):
        return self.title


class PermissionGroup(models.Model):
    name=models.CharField(max_length=32)
    def __str__(self):
        return self.name



