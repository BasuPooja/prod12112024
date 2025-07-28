from tkinter import CASCADE
from asyncio.windows_events import NULL
from django.db import models
from django.contrib.auth.models import (    BaseUserManager, AbstractBaseUser)
from django.core.exceptions import ValidationError
import datetime
from django.utils import timezone
 
# Apeksha #
class do_upload(models.Model):
    id=models.AutoField(primary_key=True, unique= True)
    desig_id=models.ForeignKey('myadmin.Level_Desig',on_delete=models.CASCADE, null=False)
    created_by=models.ForeignKey('inspects.empmast',on_delete=models.CASCADE)  
    created_on=models.DateTimeField(auto_now_add=True)
    do_letter_no=models.CharField(null=False,max_length=200,blank=False)
    do_letter_date=models.DateField(null=False,blank=False)
    subject=models.CharField(max_length=300, blank=False)
    delete_flag=models.BooleanField()
    status_flag=models.PositiveSmallIntegerField(null=False, default=0)
    do_path=models.FileField(max_length=100,null=True,upload_to='do_letter/')
    do_text=models.CharField(null=True,max_length=300)

class do_act(models.Model):
    id=models.AutoField(primary_key=True, unique=True)
    id_upload=models.ForeignKey('do_upload', on_delete=models.CASCADE)
    desig_id=models.ForeignKey('myadmin.Level_Desig',on_delete=models.CASCADE, null=False)
    emp_no=models.ForeignKey('inspects.empmast',on_delete=models.CASCADE)
    remarks=models.TextField(null=True)
    reply_path=models.FileField(max_length=100, null= True, upload_to='do_letter/')
    date_of_reply=models.DateField(auto_now_add=True, null= True)
    status_flag=models.BooleanField(default=False)

class do_copy(models.Model):
    id=models.AutoField(primary_key=True, unique=True)
    do_upload=models.ForeignKey('do_upload', on_delete=models.CASCADE)
    desig_id=models.ForeignKey('myadmin.Level_Desig',on_delete=models.CASCADE, null=False)
    