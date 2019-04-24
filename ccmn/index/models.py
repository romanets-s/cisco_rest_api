from django.db import models

class Users2(models.Model):
    macAddress = models.CharField(max_length=17)
    xlogin = models.CharField(max_length=8)
    FirstName = models.CharField
    LastName = models.CharField