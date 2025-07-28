# from django.db import models


# # Create your models here.
 
# class Insp_details(models.Model):
#     insp_no=models.BigAutoField(primary_key=True)
#     mom_officer=models.ForeignKey('myadmin.Level_Desig',on_delete=models.CASCADE, null=True)
#     created_on=models.DateTimeField(auto_now=False, null=True)
#     created_by=models.CharField(max_length=100, blank=False, null=True)
#     mom_note_no=models.CharField(max_length=40, blank=True, null=True)
#     note_last=models.IntegerField(blank=False, null=True,default=0)
#     mom_date=models.DateField(auto_now=False, null=True)
#     mom_title=models.TextField( blank=False, null=True)
#     type=models.IntegerField(blank=False, null=True,default=0)
#     meeting_type=models.TextField( null=True)
#     status_flag=models.IntegerField(default=0)
#     updated_on = models.DateTimeField(auto_now=False, null=True)
#     station_name=models.CharField(max_length=50, blank=False, null=True)
#     officer_name=models.CharField(max_length=100, blank=False, null=True)
#     officer_desig=models.CharField(max_length=50, blank=False, null=True)


# class Item_details(models.Model):
#     item_no=models.BigAutoField(primary_key=True)  
#     insp_no=models.ForeignKey('Insp_details', on_delete=models.CASCADE, null=True)
#     created_on=models.DateTimeField(auto_now=False, null=True)
#     updated_on = models.DateTimeField(auto_now=False, null=True)
#     created_by=models.CharField(max_length=100, blank=False, null=True)
#     item_heading=models.TextField(null=True)
#     remarks= models.TextField( blank=False, null=True)
#     item_subheading=models.TextField(null=True)
#     item_description=models.TextField(null=True)
#     item_decision=models.TextField(null=True)
#     target_date=models.DateField(null=True)
#     type=models.CharField(max_length=5, blank=False, null=True)
#     des_id=models.CharField(max_length=10, blank=False, null=True)
#     item_priority=models.CharField(max_length=1, blank=False, null=True)
#     status_flag=models.IntegerField(default=0)
#     slno = models.IntegerField(default = 1)
#     table_data = models.TextField(default='[]')
#     link_image = models.CharField(max_length=200,null=True) 
#     del_flag = models.IntegerField(default=0) 
    
 
# class Marked_Members(models.Model):
#     marked_no=models.BigAutoField(primary_key=True)
#     item_no=models.ForeignKey('Item_details', on_delete=models.CASCADE, null=True)
#     marked_to=models.ForeignKey('myadmin.Level_Desig', on_delete=models.CASCADE, null=True)
#     created_on=models.DateTimeField(auto_now=False, null=True)
#     updated_on = models.DateTimeField(auto_now=False, null=True)
#     created_by=models.CharField(max_length=100, blank=False, null=True)
#     reply_text=models.CharField(max_length=500, blank=False, null=True)
#     reply_file=models.FileField(upload_to='documents/')
#     reply_on=models.DateField(null=True)
#     status_flag=models.IntegerField(null=True)
#     status=models.CharField(max_length=1,blank=False, null=True)
#     target_date=models.DateField(null=True)
#     priority=models.CharField(max_length=1, blank=False, null=True)
#     action_type=models.IntegerField(default=0)   

# class copydealt_mail(models.Model):
#     mail_no=models.BigAutoField(primary_key=True)  
#     insp_no=models.ForeignKey('Insp_details', on_delete=models.CASCADE, null=True)
#     created_on=models.DateTimeField(auto_now=False, null=True)
#     created_by=models.CharField(max_length=100, blank=False, null=True)
#     send_to = models.TextField(null=True)
#     subject=models.CharField(max_length=100, blank=False, null=True)
#     body=models.CharField(max_length=500, blank=False, null=True)
#     area = models.CharField(max_length=10, blank=False, null=True)

# #######################  changed up 

# class Reject_remark(models.Model):
#     remark_no=models.BigAutoField(primary_key=True)
#     marked_desig=models.ForeignKey('myadmin.Level_Desig', on_delete=models.CASCADE, null=True)
#     marked_no=models.ForeignKey('Marked_Members', on_delete=models.CASCADE, null=True)
#     created_on=models.DateTimeField(auto_now=False, null=True)
#     created_by=models.CharField(max_length=100, blank=False, null=True)
#     reply_received=models.CharField(max_length=50, blank=False, null=True)
#     file_received=models.FileField(upload_to='documents/',null=True)
#     reply_on=models.DateTimeField(auto_now=False, null=True)
#     remark=models.CharField(max_length=200, blank=False, null=True)
#     reject_on=models.DateTimeField(auto_now=False, null=True)
#     status_flag = models.IntegerField(default=0)
 
# class Insp_members(models.Model):
#     member_no=models.BigAutoField(primary_key=True)
#     member_desig=models.ForeignKey('myadmin.Level_Desig', on_delete=models.CASCADE, null=True)
#     other_members=models.CharField(max_length=100, null=True)
#     insp_no=models.ForeignKey('Insp_details', on_delete=models.CASCADE, null=True)
#     status_flag = models.IntegerField(default=0)
 

# class meeting_typelist(models.Model):
#     type_no=models.BigAutoField(primary_key=True)
#     meeting_type=models.CharField(max_length=500,null=False)
#     default_flag=models.IntegerField(default=1)
#     added_by=models.ForeignKey('myadmin.Level_Desig', on_delete=models.CASCADE, null=True)



from django.db import models

# Create your models here.
 
class Insp_details(models.Model):
    insp_no=models.BigAutoField(primary_key=True)
    mom_officer=models.ForeignKey('myadmin.Level_Desig',on_delete=models.CASCADE, null=True)
    created_on=models.DateTimeField(auto_now=False, null=True)
    created_by=models.CharField(max_length=100, blank=False, null=True)
    mom_note_no=models.CharField(max_length=40, blank=True, null=True)
    note_last=models.IntegerField(blank=False, null=True,default=0)
    mom_date=models.DateField(auto_now=False, null=True)
    mom_title=models.TextField( blank=False, null=True)
    type=models.IntegerField(blank=False, null=True,default=0)
    meeting_type=models.TextField( null=True)
    status_flag=models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=False, null=True)
    station_name=models.CharField(max_length=50, blank=False, null=True)
    officer_name=models.CharField(max_length=100, blank=False, null=True)
    officer_desig=models.CharField(max_length=50, blank=False, null=True)


class Item_details(models.Model):
    item_no=models.BigAutoField(primary_key=True)  
    insp_no=models.ForeignKey('Insp_details', on_delete=models.CASCADE, null=True)
    created_on=models.DateTimeField(auto_now=False, null=True)
    updated_on = models.DateTimeField(auto_now=False, null=True)
    created_by=models.CharField(max_length=100, blank=False, null=True)
    item_heading=models.TextField(null=True)
    remarks= models.TextField( blank=False, null=True)
    item_subheading=models.TextField(null=True)
    item_description=models.TextField(null=True)
    item_decision=models.TextField(null=True)
    target_date=models.DateField(null=True)
    type=models.CharField(max_length=5, blank=False, null=True)
    des_id=models.CharField(max_length=10, blank=False, null=True)
    item_priority=models.CharField(max_length=1, blank=False, null=True)
    status_flag=models.IntegerField(default=0)
    slno = models.IntegerField(default = 1)
    table_data = models.TextField(default='[]')
    link_image = models.CharField(max_length=200,null=True) 
    del_flag = models.IntegerField(default=0) 
    
 
class Marked_Members(models.Model):
    marked_no=models.BigAutoField(primary_key=True)
    item_no=models.ForeignKey('Item_details', on_delete=models.CASCADE, null=True)
    marked_to=models.ForeignKey('myadmin.Level_Desig', on_delete=models.CASCADE, null=True)
    created_on=models.DateTimeField(auto_now=False, null=True)
    updated_on = models.DateTimeField(auto_now=False, null=True)
    created_by=models.CharField(max_length=100, blank=False, null=True)
    reply_text=models.CharField(max_length=3000, blank=False, null=True)
    reply_file=models.FileField(upload_to='documents/')
    reply_on=models.DateField(null=True)
    status_flag=models.IntegerField(null=True)
    status=models.CharField(max_length=1,blank=False, null=True)
    target_date=models.DateField(null=True)
    priority=models.CharField(max_length=1, blank=False, null=True)
    action_type=models.IntegerField(default=0)   

class copydealt_mail(models.Model):
    mail_no=models.BigAutoField(primary_key=True)  
    insp_no=models.ForeignKey('Insp_details', on_delete=models.CASCADE, null=True)
    created_on=models.DateTimeField(auto_now=False, null=True)
    created_by=models.CharField(max_length=100, blank=False, null=True)
    send_to = models.TextField(null=True)
    subject=models.CharField(max_length=100, blank=False, null=True)
    body=models.CharField(max_length=500, blank=False, null=True)
    area = models.CharField(max_length=10, blank=False, null=True)


#######################  changed up 


class Reject_remark(models.Model):
    remark_no=models.BigAutoField(primary_key=True)
    marked_desig=models.ForeignKey('myadmin.Level_Desig', on_delete=models.CASCADE, null=True)
    marked_no=models.ForeignKey('Marked_Members', on_delete=models.CASCADE, null=True)
    created_on=models.DateTimeField(auto_now=False, null=True)
    created_by=models.CharField(max_length=100, blank=False, null=True)
    reply_received=models.CharField(max_length=50, blank=False, null=True)
    file_received=models.FileField(upload_to='documents/',null=True)
    reply_on=models.DateTimeField(auto_now=False, null=True)
    remark=models.CharField(max_length=200, blank=False, null=True)
    reject_on=models.DateTimeField(auto_now=False, null=True)
    status_flag = models.IntegerField(default=0)
 
class Insp_members(models.Model):
    member_no=models.BigAutoField(primary_key=True)
    member_desig=models.ForeignKey('myadmin.Level_Desig', on_delete=models.CASCADE, null=True)
    other_members=models.CharField(max_length=100, null=True)
    insp_no=models.ForeignKey('Insp_details', on_delete=models.CASCADE, null=True)
    status_flag = models.IntegerField(default=0)
 


class meeting_typelist(models.Model):
    type_no=models.BigAutoField(primary_key=True)
    meeting_type=models.CharField(max_length=500,null=False)
    default_flag=models.IntegerField(default=1)
    added_by=models.ForeignKey('myadmin.Level_Desig', on_delete=models.CASCADE, null=True)


