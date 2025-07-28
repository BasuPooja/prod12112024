from unittest.util import _MAX_LENGTH
from django.db import models
from asyncio.windows_events import NULL
from inspects import managers
from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django.core.exceptions import ValidationError
import datetime
from django.utils import timezone


#flag values:
                # 0 - copy to
                # 1 - mark officer
                # 2 - dealt by


                # doc_table:
                # i - Inspection_details
                # m - Insp_details (minutes)
                # d - do_upload
                # b - budget


class copyto_mails(models.Model):
    mail_no=models.BigAutoField(primary_key=True)  
    created_on=models.DateTimeField(auto_now_add=True, null=True)
    sender_id=models.ForeignKey('myadmin.Level_Desig',on_delete=models.CASCADE, null=False)
    # sender_desig=models.CharField(max_length=15, blank=False, null=True)
    doc_id= models.BigIntegerField(null=True)
    doc_table=models.CharField(max_length=10)
    receiver_id=models.CharField(max_length=6000, blank=False, null=True)
    receiver_desig = models.CharField(max_length=6000, blank=False, null=True)
    subject=models.CharField(max_length=500, blank=False, null=True)
    body=models.CharField(max_length=500, blank=False, null=True)
    area_flag = models.IntegerField(default=0)
    reminder_count = models.IntegerField(default=0)
    noted_flag = models.IntegerField(default=0)
    noted_by=models.CharField(max_length=6000, blank=False, null=True)

    #flag values: 
    # 0 - copy to
    # 1 - mark officer
    # 2 - dealt by

    # doc_table:
    # i - Inspection_details
    # m - Insp_details (minutes)
    # d - do_upload
    # b - budget

class deleted_data_copyto_mails(models.Model):
    mail_no=models.BigAutoField(primary_key=True)  
    created_on=models.DateTimeField(auto_now_add=True, null=True)
    sender_id=models.ForeignKey('myadmin.Level_Desig',on_delete=models.CASCADE, null=False)
    # sender_desig=models.CharField(max_length=15, blank=False, null=True)
    doc_id= models.BigIntegerField(null=True)
    doc_table=models.CharField(max_length=10)
    receiver_id=models.CharField(max_length=6000, blank=False, null=True)
    receiver_desig = models.CharField(max_length=6000, blank=False, null=True)
    subject=models.CharField(max_length=500, blank=False, null=True)
    body=models.CharField(max_length=500, blank=False, null=True)
    area_flag = models.IntegerField(default=0)
    reminder_count = models.IntegerField(default=0)
    noted_flag = models.IntegerField(default=0)
    noted_by=models.CharField(max_length=6000, blank=False, null=True)
