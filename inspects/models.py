from django.db import models
from asyncio.windows_events import NULL
from inspects import managers
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.exceptions import ValidationError
import datetime
from django.utils import timezone
from .choices import INSPECTION_TYPE

# Create your models here.



class error_Table(models.Model):
    log_no=models.BigAutoField(primary_key=True)
    fun_name=models.CharField(max_length=255,null=True,blank=True)
    user_id=models.CharField(max_length=40,null=True,blank=True)
    err_details=models.TextField(null=True,blank=True)
    err_date=models.DateField(auto_now_add=True)

    class meta:
        db_table="error_Table"

  
class MyUser(AbstractBaseUser):

    username = models.CharField(
        max_length=50, blank=True, null=True,  unique=True)
    # first_name = models.CharField(max_length=50,blank=True,null=True)
    # last_name = models.CharField(max_length=50, blank=True,null=True)
    email = models.EmailField(verbose_name='email address', null=True)
    guest_to=models.ForeignKey('MyUser', on_delete=models.CASCADE, null=True)
    user_role = models.CharField(max_length=30)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    last_update = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    objects = managers.MyUserManager()
    phase_type=models.CharField(max_length=1,null=True,default="1")
    otp = models.PositiveIntegerField(null=True, blank=True)
    otp_created_on = models.DateTimeField(auto_now=True, null=True, blank=True)
    guest_email = models.EmailField(verbose_name='email address', null=True)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['mobile_no', ]

    def __str__(self):
        return self.email

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name



class Insp_multi_location(models.Model):
    location_no=models.BigAutoField(primary_key=True)
    inspection_no=models.ForeignKey('Inspection_details',on_delete=models.CASCADE, null=True) #on_delete=models.CASCADE
    item=models.CharField(max_length=50,null=False)
    item_code=models.CharField(max_length=10,null=True)
    type=models.CharField(max_length=5, null=True)
    d_flag=models.IntegerField(default=0)
    table_from=models.CharField(max_length=5,null=True)
    update_status = models.CharField(default='T',max_length=1)

class Insp_Accompany(models.Model):
    accompany_no=models.AutoField(primary_key=True)
    inspection_no=models.ForeignKey('Inspection_details',on_delete=models.CASCADE, null=True) #on_delete=models.CASCADE
    accompany=models.CharField(max_length=50,null=True)
    created_on=models.DateTimeField(auto_now=True)
    update_status = models.CharField(default='T',max_length=1)

class Inspection_details(models.Model):
    inspection_no=models.BigAutoField(primary_key=True)
    inspection_note_no=models.CharField(max_length=100, blank=True, null=True, unique=True)
    inspection_officer=models.ForeignKey('myadmin.Level_Desig',on_delete=models.CASCADE, null=True) #on_delete=models.CASCADE
    inspection_title=models.CharField(max_length=1500, blank=False, null=True)
    # zone=models.CharField(max_length=10, blank=False, null=False)
    # division=models.CharField(max_length=10, blank=False, null=False)
    # dept=models.CharField(max_length=20, blank=False, null=True)
    # location=models.CharField(max_length=20, blank=False, null=False)
    # inspected_on=models.DateField(auto_now=False, null=False)
    target_date=models.DateField(null=True)
    modified_on=models.DateTimeField(auto_now=False, null=True)
    created_on=models.DateTimeField(auto_now=False, null=True)
    report_path=models.CharField(max_length=50, blank=False, null=True)
    status_flag=models.IntegerField(default=0)
    send_to=models.CharField(max_length=100, blank=False, null=True)
    modified_by=models.CharField(max_length=100, blank=False, null=True)
    # ForeignKey('empmast',on_delete=models.CASCADE, null=True,related_name='modified_by')
    created_by=models.CharField(max_length=100, blank=False, null=True)
    # ForeignKey('empmast',on_delete=models.CASCADE, null=True,related_name='created_by')
    item_type=models.CharField(max_length=10, blank=False, null=True)
    status = models.CharField(max_length=10, blank=False, null=True)
    insp_last=models.IntegerField(blank=False, null=True)
    start_date=models.DateField(auto_now=False, null=True)
    # end_date=models.DateField(auto_now=False, null=True)
    inspected_on=models.DateField(auto_now=False, null=True)
    final_submit_on=models.DateField(null=True)
    station_name=models.CharField(max_length=50, blank=False, null=True)
    officer_name=models.CharField(max_length=100, blank=False, null=True)
    officer_desig=models.CharField(max_length=50, blank=False, null=True)
    item_sections = models.IntegerField(default=0, null=True)
    insp_type=models.IntegerField(default=0)
    good_work = models.BooleanField(default=False)
    delete_flag = models.IntegerField(default=0)
    approval_flag = models.IntegerField(default=0)

    #INSP TYPE FLAG VALUES
    #0 regular inspection
    #1 drive based inspection(issued by RB) 
    #2 night inspection
    #3 surprise inspection

    #item_sections values
    # 0:Sections not present
    # 1:sections present



class Item_details(models.Model):
    item_no=models.BigAutoField(primary_key=True)   
    item_title=models.CharField(max_length=3000, blank=False, null=True)
    inspection_no=models.ForeignKey('Inspection_details', on_delete=models.CASCADE, null=True)
    status=models.CharField(max_length=10, blank=False, null=True)
    status_flag=models.IntegerField(default=0)
    observation=models.CharField(max_length=3000, blank=False, null=True)
    modified_on=models.DateTimeField(auto_now=False, null=True)
    created_on=models.DateTimeField(auto_now=False, null=True)
    modified_by=models.CharField(max_length=15, blank=False, null=True)
    created_by=models.CharField(max_length=15, blank=False, null=True)
    target_date=models.DateField(null=True)
    item_subtitle=models.CharField(max_length=3000, blank=False, null=True)
    type=models.CharField(max_length=3, blank=False, null=True)
    item_link=models.CharField(max_length=20, blank=False, null=True)
    des_id=models.CharField(max_length=8, blank=False, null=True)
    priority=models.IntegerField(default=0)
    del_flag = models.IntegerField(default=0)
    tbl_data = models.TextField(default='[]')
    link_image=models.CharField(max_length=200,null=True)
    action_type=models.IntegerField(default=0)
    update_status = models.CharField(default='T',max_length=1)
    sl_no =  models.IntegerField(null=True)
    markofcRemarks = models.CharField(max_length=500,null=True)
    item_type=models.IntegerField(default=0)
    location_table=models.CharField(max_length=50,null=True)
    location_code=models.CharField(max_length=10,null=True)
    location_val=models.CharField(max_length=100,null=True)
    hqid=models.ForeignKey('myadmin.railwayLocationMaster', on_delete=models.CASCADE, null=True,related_name='item_rly_id')
    divid=models.ForeignKey('myadmin.railwayLocationMaster', on_delete=models.CASCADE, null=True,related_name='item_div_id')


    # action_type values:
    # 0: For Action (compliance required)
    # 1: For Information

    #ITEM TYPE FLAG VALUES
    #0 Others 
    #1 Passenger Safety
    #2 Employee Safety 
    


class Insp_mail_details(models.Model):
    mail_no=models.BigAutoField(primary_key=True)   
    inspection_no=models.ForeignKey('Inspection_details', on_delete=models.CASCADE, null=True)
    subject=models.CharField(max_length=100, blank=False, null=True)
    body=models.CharField(max_length=500, blank=False, null=True)
    send_to = models.CharField(max_length=2000, blank=False, null=True)
    send_desig = models.CharField(max_length=2000, blank=False, null=True)
    created_on=models.DateTimeField(auto_now_add=True)
    area = models.CharField(max_length=10, blank=False, null=True)

class Marked_Officers(models.Model):
    marked_no=models.BigAutoField(primary_key=True)
    marked_to=models.ForeignKey('myadmin.Level_Desig', on_delete=models.CASCADE, null=True)
    marked_emp=models.CharField(max_length=100, blank=False, null=True)
    # ForeignKey('empmast', on_delete=models.CASCADE, null=True)
    item_no=models.ForeignKey('Item_details', on_delete=models.CASCADE, null=True)
    compliance=models.CharField(max_length=3000, blank=False, null=True)
    compliance_recieved_on=models.DateTimeField(auto_now=False, null=True)
    modified_on=models.DateTimeField(auto_now=False, null=True)
    created_on=models.DateTimeField(auto_now=True, null=True)
    modified_by=models.CharField(max_length=15, blank=False, null=True)
    created_by=models.CharField(max_length=15, blank=False, null=True)
    #new amisha
    myuser_id=models.ForeignKey('MyUser', on_delete=models.CASCADE, null=True)
    status_flag=models.IntegerField(null=True)
    reply_on=models.DateField(null=True)
    #gunjan
    revert=models.CharField(max_length=500,blank=False, null=True)
    reverted_on=models.DateField(null=True)
    status=models.CharField(max_length=1,blank=False, null=True)
    viewed_on=models.DateField(auto_now=False,null=True)
    target_flag=models.IntegerField(default=0)
    update_status = models.CharField(default='T',max_length=1)
    #apeksha
    priority=models.IntegerField(default=0)
    target_date=models.DateField(null=True)
    action_type=models.IntegerField(default=0)
    marked_on=models.DateTimeField(null=True)
    add_status=models.IntegerField(default=0)
#TARGET FLAG VALUES:
#0: NO TARGET GIVEN
#1: TARGET SET AND SAVED IN target_compliance

#add_status FLAG VALUES:
#0: NO addendum GIVEN
#1: addendum GIVEN 

class addendum(models.Model):
    add_id=models.BigAutoField(primary_key=True)
    marked_no=models.ForeignKey('Marked_Officers', on_delete=models.CASCADE, null=True)
    item_no=models.ForeignKey('Item_details', on_delete=models.CASCADE, null=True)
    compliance=models.CharField(max_length=3000, blank=False, null=True)
    created_on=models.DateTimeField(auto_now=True, null=True)
    status_flag=models.IntegerField(default=0)

class target_compliance(models.Model):
    target_id=models.BigAutoField(primary_key=True)
    target_date=models.DateField(auto_now=False,null=True)
    status_flag=models.IntegerField(null=True)
    marked_no=models.ForeignKey('Marked_Officers', on_delete=models.CASCADE, null=True)
    marked_einsp=models.ForeignKey('einspect.einsp_marked', on_delete=models.CASCADE, null=True)
    reply_sent=models.CharField(max_length=3000, blank=False, null=True)
    rejected_on=models.DateTimeField(auto_now=False, null=True)
    reply_on=models.DateTimeField(auto_now=False, null=True)
    remark = models.CharField(max_length=200, blank=False, null=True)
    pending_with=models.ForeignKey('myadmin.Level_Desig', related_name='pending',on_delete=models.CASCADE, null=True)
    assigned_by=models.ForeignKey('myadmin.Level_Desig', related_name='assigned', on_delete=models.CASCADE, null=True)
    task_type=models.CharField(max_length=20, blank=False, null=True)
    init_date=models.DateField(auto_now=False,null=True)
    task_flag=models.IntegerField(null=True,default=1)
    task_descp=models.CharField(max_length=3000, blank=False, null=True)

#status_flag of target_compliance table VALUES:
#0: compliance pending
#1: compliance saved as draft
#2: compliance rejected
#3: task completed
#4: compliance sent & accepted

#task_flag of target_compliance table VALUES:
#1: Inspection
#2: Others
#3: Phase 2

class target_status(models.Model):
    status_id=models.BigAutoField(primary_key=True)
    target_no=models.ForeignKey('target_compliance', on_delete=models.CASCADE, null=True)
    status_flag=models.IntegerField(null=True)
    reply_sent=models.CharField(max_length=3000, blank=False, null=True)
    reply_on=models.DateTimeField(auto_now=False, null=True)
    rejected_on=models.DateTimeField(auto_now=False, null=True)
    remark = models.CharField(max_length=200, blank=False, null=True)
#status_flag of target_status table VALUES:
#0: Not yet Started
#1: started
#2: on track
#3: partially completed
#4: delayed
#5: completed





    


class Marked_Officers_forward(models.Model):
    marked_no_forward=models.BigAutoField(primary_key=True)
    marked_to_forward=models.ForeignKey('myadmin.Level_Desig', on_delete=models.CASCADE, null=True)
    marked_no=models.ForeignKey('Marked_Officers', on_delete=models.CASCADE, null=True)
    compliance_forward=models.CharField(max_length=3000, null=True)
    compliance_recieved_on_forward=models.DateTimeField(auto_now=False, null=True)
    modified_on_forward=models.DateTimeField(auto_now=False, null=True)
    created_on_forward=models.DateTimeField(auto_now=False, null=True)
    modified_by_forward=models.CharField(max_length=10, blank=False, null=True)
    created_by_forward=models.CharField(max_length=10, blank=False, null=True)
    myuser_id=models.ForeignKey('MyUser', on_delete=models.CASCADE, null=True)
    #gunjan
    status_flag=models.IntegerField(null=True)
    reply_on=models.DateField(null=True)
    viewed_on=models.DateField(auto_now=False,null=True)
    level=models.IntegerField(default=0)
    further_forward=models.ForeignKey('Marked_Officers_forward', on_delete=models.CASCADE, null=True)

class Officers_Remark(models.Model):
    remark_no=models.BigAutoField(primary_key=True)
    marked_no=models.ForeignKey('Marked_Officers', on_delete=models.CASCADE, null=True)
    remark = models.CharField(max_length=200, blank=False, null=True)
    reply_received=models.CharField(max_length=3000, blank=False, null=True)
    rejected_on=models.DateTimeField(auto_now=False, null=True)
    reply_on=models.DateTimeField(auto_now=False, null=True)
    status = models.CharField(max_length=10, blank=False, null=True)
    status_flag = models.IntegerField(default=0)
    myuser_id=models.ForeignKey('MyUser', on_delete=models.CASCADE, null=True)
    #gunjan
    marked_no_forward=models.ForeignKey('Marked_Officers_forward', on_delete=models.CASCADE, null=True)
    marked_desig_id=models.ForeignKey('myadmin.Level_Desig', on_delete=models.CASCADE, null=True)


class Corrigendum_Report(models.Model):
    report_no=models.BigAutoField(primary_key=True)
    marked_no=models.ForeignKey('Marked_Officers', on_delete=models.CASCADE, null=True)
    old_value = models.CharField(max_length=50, blank=False, null=True)
    new_value = models.CharField(max_length=50, blank=False, null=True)
    created_on=models.DateTimeField(auto_now=True, null=True)
    created_by = models.CharField(max_length=10, blank=False, null=True)
    status_flag = models.PositiveIntegerField(default=0)
    remark = models.CharField(max_length=200, blank=False, null=True)

class roles(models.Model):
    role = models.CharField(primary_key=True, max_length=50)
    parent = models.CharField(max_length=50, blank=True, null=True)
    # department_id=models.ForeignKey('department_master', on_delete=models.CASCADE, null=True)
    rly_unit=models.CharField(max_length=50, blank=True, null=True)
    modified_by = models.CharField( max_length=20, blank=True, null=True)
    modified_on=models.DateTimeField(auto_now=True,null=True,blank=True)
    created_on=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    delete_flag=models.BooleanField(default=False)
    department_code=models.ForeignKey('myadmin.departMast', on_delete=models.CASCADE, null=True)
    designation_code= models.CharField( max_length=20, blank=True, null=True)
    role_code = models.CharField( max_length=5, blank=True, null=True)
    shop_code=models.CharField(null = True,max_length =50)
    class Meta:
        
        db_table = 'dlw_roles'


class empmast(models.Model):
    hrms_id=models.ForeignKey('myadmin.hrms', on_delete=models.CASCADE, null=True)
    empno=models.CharField(max_length=20,primary_key=True)
    empname=models.CharField(max_length=50,null=True)
    empmname=models.CharField(max_length=50,null=True)
    emplname=models.CharField(max_length=50,null=True)
    birthdate=models.DateField(null=True)
    appointmentdate=models.DateField(null=True) 
    superannuation_date=models.DateField(null=True)
    gender=models.CharField(max_length=10,null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    contactno = models.CharField(max_length=10, blank=True, null=True)
    railwaygroup = models.CharField(max_length=50, blank=True, null=True)
    pc7_level=models.CharField(max_length=10,null=True)
    billunit=models.CharField(max_length=50,null=True)
    service_status=models.CharField(max_length=50,null=True)
    desig_longdesc=models.CharField(max_length=300,null=True)
    # desig_id=models.CharField(max_length=50,null=True)
    station_des=models.CharField(max_length=100,null=True)
    dept_desc=models.CharField(max_length=50,null=True)
    subdepartment = models.CharField(max_length=50, blank=True, null=True)    
    currentzone = models.CharField(max_length=50, blank=True, null=True)
    currentunitdivision = models.CharField(max_length=100, blank=True, null=True)
    rl_type = models.CharField(max_length=50, blank=True, null=True)
    # myuser_id=models.ForeignKey('MyUser', on_delete=models.CASCADE, null=True)
    role = models.CharField(max_length=500, blank=True, null=True)    
    rly_id=models.ForeignKey('myadmin.railwayLocationMaster', on_delete=models.CASCADE, null=True,related_name='empmast_rly_id')
    profile_modified_by = models.CharField( max_length=20, blank=True, null=True)
    profile_modified_on=models.DateField(null=True,blank=True)    
    #redundant columns birthdate,billunit,desig_id,myuser_id,role
    
    SessionId = models.CharField(max_length=50,blank=True,null=True)
    SSOUid = models.CharField(max_length=50,blank=True,null=True)




class user_request(models.Model):
    rly_id=models.ForeignKey('myadmin.railwayLocationMaster', on_delete=models.CASCADE, null=True,related_name='empmast_rly_id1')
    myuser_id=models.ForeignKey('MyUser', on_delete=models.CASCADE, null=True)
    empno=models.CharField(max_length=12, null=True)
    requestDate=models.DateField(null=True)
    remarks=models.CharField(max_length=200, null=True)
    request_type=models.CharField(max_length=50, null=True)
    status=models.CharField(max_length=20, null=True)
    designation_id=models.CharField(max_length=10, null=True)
    old_value=models.CharField(max_length=200, null=True)
    empnumber=models.CharField(max_length=20,null=True)
    designation=models.CharField(max_length=100,null=True)




class Inspection_Checklist(models.Model):
    checklist_id=models.AutoField(primary_key=True)  
    checklist_title=models.CharField(max_length=100, blank=False, null=False)
    inspection_type=models.CharField(max_length=15, choices=INSPECTION_TYPE, default = '1' )
    status=models.CharField(max_length=10, blank=False, null=False)
    delete_flag=models.BooleanField(default=False)
    created_by=models.CharField(max_length=12, blank=False, null=True)
    created_on=models.DateTimeField(auto_now_add=True,null=True)
    last_modified_by=models.CharField(max_length=12, blank=False, null=True)
    last_modified_on=models.DateTimeField(auto_now_add=True, null=True)
    version = models.IntegerField(default= "1", max_length = 5,null=True)
    department=models.ForeignKey('myadmin.departMast', on_delete=models.CASCADE,blank=True, null=True)

    
class category_add(models.Model):
    sno=models.AutoField(primary_key=True)
    category_name=models.CharField(max_length=40,null=True,blank=True)
    # department_name=models.CharField(max_length=80,null=True,blank=True)
    department_name=models.ForeignKey('myadmin.departMast', on_delete=models.CASCADE,blank=True, null=True)
    modified_on=models.DateTimeField(auto_now=True, null=True)
    created_on=models.DateTimeField(auto_now=True, null=True)
    modified_by=models.CharField(max_length=15, blank=False, null=True)
    created_by=models.CharField(max_length=15, blank=False, null=True)

class Safety_drive(models.Model):
    drive_id = models.BigAutoField(primary_key = True)
    email = models.EmailField(verbose_name='email address')
    mobile = models.CharField(max_length=15)
    officer_name=models.CharField(max_length=50)
    officer_desig=models.CharField(max_length=50)
    officer_post_grade=models.CharField(max_length=50)
    officer_posted_in=models.CharField(max_length=50)
    insp_date = models.DateTimeField()
    place_of_insp=models.CharField(max_length=200)
    hqid=models.CharField(max_length=10,null=True)
    divid=models.CharField(max_length=10,null=True)
    type_of_insp=models.CharField(max_length=500)
    shortcomings=models.CharField(max_length=5000)
    action_taken=models.CharField(max_length=2000)
    comments=models.CharField(max_length=2000)
    status_flag=models.CharField(max_length=1, blank=True, null=False, default=1)
    delete_flag=models.BooleanField(default=False)
    created_on=models.DateTimeField(auto_now_add=True,null=True)
    


class Inspection_Activity(models.Model):
    activity_id=models.AutoField(primary_key=True)  
    checklist_id=models.ForeignKey('Inspection_Checklist', on_delete=models.CASCADE)
    activities=models.CharField(max_length=200, blank=False, null=False)
    delete_flag=models.BooleanField(default=False)
    created_by=models.CharField(max_length=12, blank=False, null=True)
    created_on=models.DateTimeField(auto_now_add=True, null=True)
    last_modified_by=models.CharField(max_length=12, blank=False, null=True)
    last_modified_on=models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.checklist_id

class Events(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_title = models.CharField(max_length=50,null=True)
    description = models.CharField(max_length=250,null=True,blank=True)
    status=models.CharField(max_length=10, default=0,blank=False, null=False)
    delete_flag=models.BooleanField(default=False)
    created_by=models.CharField(max_length=50, blank=False, null=True)
    created_on=models.DateTimeField(auto_now_add=True,null=True)
    last_modified_by=models.CharField(max_length=12, blank=False, null=True)
    last_modified_on=models.DateTimeField(auto_now_add=True, null=True)
 
    
class Event_activty(models.Model):
    activity_id = models.AutoField(primary_key=True)
    event_id = models.ForeignKey('Events',on_delete=models.CASCADE,null=True)
    Railways_act = models.CharField(max_length=30,null=True)
    Division_act = models.CharField(max_length=30,null=True)
    location3_act = models.CharField(max_length=30,null=True)
    date_to_act = models.DateField(null=True)
    status=models.CharField(max_length=10,default=0, blank=False, null=True)
    delete_flag=models.BooleanField(default=False)
    created_by=models.CharField(max_length=50, blank=False, null=True)
    created_on=models.DateTimeField(auto_now_add=True,null=True)
    last_modified_by=models.CharField(max_length=12, blank=False, null=True)
    last_modified_on=models.DateTimeField(auto_now_add=True, null=True)
    #location3_act max_length =50 replace by 30 and also status default=”Pending”

 

class custom_menu(models.Model):
    m_id=models.IntegerField(null=True)
    menu=models.CharField(max_length=50,null=True)
    url=models.CharField(max_length=100,null=True)
    perent_id=models.IntegerField(null=True)
    role=models.CharField(max_length=200,null=True)
    icons=models.CharField(max_length=100,null=True)  

class history_table(models.Model):
    # desig_id=models.IntegerField(max_length=5,null=True)
    desig=models.ForeignKey('myadmin.Level_Desig',related_name='succdesig_id', on_delete=models.CASCADE, null=True)
    # parent_id=models.IntegerField(max_length=5,null=True)
    parent=models.ForeignKey('myadmin.Level_Desig',related_name='predparent_id', on_delete=models.CASCADE, null=True)
    empno=models.CharField(max_length=12, null=True)
    Assigned_on=models.DateTimeField(auto_now=True, null=True)
    Relieved_on=models.DateTimeField(auto_now=True, null=True)
    Relieved_by=models.CharField(max_length=50, null=True)
    Assigned_by=models.CharField(max_length=50, null=True)

class email_request(models.Model):
    empno=models.CharField(max_length=50, null=True)
    designation=models.CharField(max_length=100,null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    file=models.FileField(upload_to='document/',null=True)
    requestDate=models.DateField(null=True)
    status=models.CharField(max_length=20, null=True)  
    rly_id=models.ForeignKey('myadmin.railwayLocationMaster', on_delete=models.CASCADE, null=True,related_name='emailrequestrailid')


#sidhi
class schedule_marked1(models.Model):
    marked_no=models.BigAutoField(primary_key=True)
    marked_to=models.ForeignKey('myadmin.Level_Desig', on_delete=models.CASCADE, null=True)
    marked_emp=models.CharField(max_length=100, blank=False, null=True)
    act_id=models.ForeignKey('Event_activty',on_delete=models.CASCADE,null=True)
    event_id = models.ForeignKey('Events',on_delete=models.CASCADE,null=True)
    created_on=models.DateTimeField(auto_now=False, null=True) 


class commanlogin(models.Model):
    sno=models.BigAutoField(primary_key=True)
    user=models.CharField(max_length=50, blank=False, null=True)
    sites=models.CharField(max_length=20, blank=False, null=True)
    auth=models.CharField(max_length=50, blank=False, null=True)
    pwd=models.CharField(max_length=50, blank=False, null=True)



class Sso_Session_Key(models.Model):
    s_id = models.CharField(primary_key=True, max_length=15)
    user_id = models.CharField(max_length=50)
    pub_key = models.CharField( max_length=10,  null=True)
    pri_key = models.CharField( max_length=10,  null=True)
    application = models.CharField( max_length=5, null=True)
    value = models.CharField( max_length=15,  null=True)

class Sso_User_Details(models.Model):
    u_id = models.IntegerField(primary_key=True)
    sso_user = models.CharField(max_length=50)
    application = models.CharField( max_length=5, null=True)
    app_user = models.CharField(max_length=40)
    date = models.DateTimeField(null=True)
    


class irpsm_workplan_mstr(models.Model):    
    uwid = models.IntegerField(primary_key=True)
    curr_cost = models.FloatField(null=True)
    expenditure_curr_finyear = models.FloatField(null=True)
    fin_progress = models.FloatField(null=True)
    phy_progress = models.FloatField(null=True)
    plan_head = models.CharField(max_length=50,null=True)
    work_category = models.CharField(max_length=50,null=True)
    yearmonth = models.IntegerField()
    updatedate = models.DateTimeField(null=True)
    receiving_time = models.DateTimeField(null=True)


#added for inspection schedule start here
class schedule_detail(models.Model):
    id = models.BigAutoField(primary_key=True)  # Autoincreamenting primary key field
    
    inspecting_officer = models.ForeignKey('myadmin.Level_Desig', related_name='inspecting_officer', on_delete=models.CASCADE, null=True)
    tour_description = models.CharField(max_length=1000,blank=False, null=True)
    accompanied_by = models.CharField(max_length=1000, blank=False, null=True)
    recommending_officer = models.ForeignKey('myadmin.Level_Desig', related_name='recommending_officer', on_delete=models.CASCADE, null=True)
    approving_officer = models.ForeignKey('myadmin.Level_Desig', related_name='approving_officer', on_delete=models.CASCADE, null=True)
    forwarded_to_officer = models.ForeignKey('myadmin.Level_Desig', related_name='forwarded_to_officer', on_delete=models.CASCADE, null=True)
    looking_after_officer = models.ForeignKey('myadmin.Level_Desig', related_name='looking_after_officer', on_delete=models.CASCADE, null=True)
    document = models.FileField(upload_to='static/document_upload/', null=True, max_length=1000)
    created_by = models.ForeignKey('empmast',related_name='created_by', on_delete=models.CASCADE, null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    last_modified_by = models.ForeignKey('empmast',related_name='last_modified_by', on_delete=models.CASCADE, null=True)
    last_modified_on = models.DateTimeField(auto_now=True, null=True)
    letter_no = models.CharField(max_length=1000,blank=False, null=True)
    status_flag = models.IntegerField(null=True, default=0)
    delete_flag = models.BooleanField(default=False)
    is_modified = models.BooleanField(default=False)
    modified_new_schedule = models.ForeignKey('self', on_delete=models.CASCADE, null=True, default=None)
    

class tour_detail(models.Model):
    id = models.BigAutoField(primary_key=True)  # Autoincreamenting primary key field
    schedule_detail = models.ForeignKey('schedule_detail', on_delete=models.CASCADE, null=True)
    date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    mode = models.CharField(max_length=100, blank=False, null=True)
    trans_detail = models.CharField(max_length=100, blank=False, null=True)
    arr_time = models.TimeField(null=True)
    dep_time = models.TimeField(null=True)
    from_location = models.CharField(max_length=100, blank=False, null=True)
    to = models.CharField(max_length=100, blank=False, null=True)
    purpose = models.CharField(max_length=100, blank=False, null=True)
    delete_flag = models.BooleanField(default=False)

class schedule_marked(models.Model):
    id = models.BigAutoField(primary_key=True)  # Autoincreamenting primary key field
    schedule_detail = models.ForeignKey('schedule_detail', on_delete=models.CASCADE, null=True)
    created_on = models.DateField(auto_now_add=True, null=True)
    created_by = models.ForeignKey('empmast',related_name='created_by_marked', on_delete=models.CASCADE, null=True)
    marked_to = models.ForeignKey('myadmin.Level_Desig', on_delete=models.CASCADE, null=True)
    view_flag = models.BooleanField(default=False)
    remarks = models.CharField(max_length=500, blank=False, null=True)

class schedule_remarks(models.Model):
    id = models.BigAutoField(primary_key=True)  # Autoincreamenting primary key field
    schedule_detail = models.ForeignKey('schedule_detail', on_delete=models.CASCADE, null=True)
    action_taken = models.IntegerField(null = False, default = 0)
    rem_date = models.DateField(auto_now_add=True, null=True)
    remarks = models.CharField(max_length=500, blank=False, null=True)
    given_by = models.ForeignKey('myadmin.Level_Desig',related_name='given_by', on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey('empmast',related_name='created_by_remarks', on_delete=models.CASCADE, null=True)
    letter_no = models.CharField(max_length=1000,blank=False, null=True)
    remarks_by_officer = models.CharField(max_length=1000,blank=False, null=True)
    

class schedule_location(models.Model):
    id = models.BigAutoField(primary_key=True)  # Autoincreamenting primary key field
    schedule_detail = models.ForeignKey('schedule_detail', on_delete=models.CASCADE, null=True)
    type = models.CharField(max_length=10, blank=False, null=True)
    value = models.CharField(max_length=1000,blank=False, null=True)
    created_on = models.DateField(auto_now_add=True, null=True)
    created_by = models.ForeignKey('empmast',related_name='created_by_location', on_delete=models.CASCADE, null=True)
    last_mod_on = models.DateField(auto_now=True, null=True)
    last_mod_by = models.ForeignKey('empmast',related_name='last_mod_by_location', on_delete=models.CASCADE, null=True)

    #added for inspection schedule end here


class hrms_logs(models.Model):
    empno=models.CharField(max_length=200,null=True)
    hrmsid=models.CharField(max_length=20,null=True)
    token=models.CharField(max_length=500,null=True)
    SessionId = models.CharField(max_length=500,blank=True,null=True)
    SSOUid = models.CharField(max_length=500,blank=True,null=True)
    purpose = models.CharField(max_length=100,blank=True,null=True)
    remarks = models.CharField(max_length=300,blank=True,null=True)
    last_modified = models.DateTimeField(auto_now=True,blank=True)

########### login history and session mgmt table
class login_history(models.Model):
    id = models.BigAutoField(primary_key = True) 
    username = models.CharField(max_length = 100,null = True)
    session_key = models.CharField(max_length = 50, null = True)
    browser_type = models.CharField(max_length = 100,null = True)
    os_type = models.CharField(max_length = 100,null = True)
    ip_address = models.CharField(max_length = 20,null = True)
    login_date_time = models.DateTimeField(auto_now = True)
    logout_date_time = models.DateTimeField(null = True)

class session_mgmt(models.Model):
    username = models.CharField(primary_key=True,max_length=100)
    session_key = models.CharField(max_length=50, null=True)


class August_safety_drive(models.Model):
    id = models.BigAutoField(primary_key = True)
    system_id=models.CharField(max_length=50, blank=False, null=True)
    inspection_id=models.CharField(max_length=50, blank=True, null=True)
    officer_name=models.CharField(max_length=500, blank=True, null=True)
    officer_desig=models.CharField(max_length=1000, blank=True, null=True)
    officer_post_grade=models.CharField(max_length=50, blank=True, null=True)
    officer_grade_code=models.CharField(max_length=50, blank=True, null=True)
    officer_posted_in=models.CharField(max_length=50, blank=True, null=True)
    officer_email=models.CharField(max_length=200, blank=True, null=True)
    officer_mobile=models.CharField(max_length=50, blank=True, null=True)
    insp_date=models.CharField(max_length=50, blank=True, null=True)
    insp_date_field = models.DateTimeField(blank=True, null=True)
    place_of_insp=models.CharField(max_length=1000, blank=True, null=True)
    zone_of_insp=models.CharField(max_length=50, blank=True, null=True)
    div_of_insp=models.CharField(max_length=200, blank=True, null=True)
    divcode_of_insp=models.CharField(max_length=50, blank=True, null=True)
    type_of_insp=models.CharField(max_length=200, blank=True, null=True)
    shortcomings=models.CharField(max_length=5000, blank=True, null=True)
    action_taken=models.CharField(max_length=2000, blank=True, null=True)
    comments=models.CharField(max_length=2000, blank=True, null=True)
    trx_timestamp = models.DateTimeField(auto_now = True)
    system_division_name=models.CharField(max_length=25, blank=True, null=True)
    system_division_code=models.CharField(max_length=5, blank=True, null=True)
    insp_date_actual = models.DateTimeField(blank=True, null=True)

class Sept_safety_drive(models.Model):
    id = models.BigAutoField(primary_key = True)
    system_id=models.CharField(max_length=50, blank=False, null=True)
    inspection_id=models.CharField(max_length=50, blank=True, null=True)
    officer_email=models.CharField(max_length=200, blank=True, null=True)
    officer_mobile=models.CharField(max_length=50, blank=True, null=True)
    officer_name=models.CharField(max_length=500, blank=True, null=True)
    officer_desig=models.CharField(max_length=1000, blank=True, null=True)
    officer_post_grade=models.CharField(max_length=50, blank=True, null=True)
    officer_grade_code=models.CharField(max_length=50, blank=True, null=True)
    officer_posted_in=models.CharField(max_length=50, blank=True, null=True)
    insp_date=models.CharField(max_length=50, blank=True, null=True)
    insp_date_field = models.DateTimeField(blank=True, null=True)
    place_of_insp=models.CharField(max_length=1000, blank=True, null=True)
    zone_of_insp=models.CharField(max_length=50, blank=True, null=True)
    div_of_insp=models.CharField(max_length=200, blank=True, null=True)
    divcode_of_insp=models.CharField(max_length=50, blank=True, null=True)
    type_of_insp=models.CharField(max_length=200, blank=True, null=True)
    shortcomings=models.CharField(max_length=10000, blank=True, null=True)
    action_taken=models.CharField(max_length=2000, blank=True, null=True)
    comments=models.CharField(max_length=2000, blank=True, null=True)
    trx_timestamp = models.DateTimeField(auto_now = True, null=True)
    system_division_name=models.CharField(max_length=25, blank=True, null=True)
    system_division_code=models.CharField(max_length=5, blank=True, null=True)
    insp_date_actual = models.DateTimeField(blank=True, null=True)

# Pooja

class deleted_data_inspection_details(models.Model):
    inspection_no=models.BigAutoField(primary_key=True)
    inspection_note_no=models.CharField(max_length=100, blank=True, null=True, unique=True)
    inspection_officer=models.ForeignKey('myadmin.Level_Desig',on_delete=models.CASCADE, null=True) #on_delete=models.CASCADE
    inspection_title=models.CharField(max_length=1500, blank=False, null=True)
    target_date=models.DateField(null=True)
    # modified_on=models.DateTimeField(auto_now=False, null=True)
    # created_on=models.DateTimeField(auto_now=False, null=True)
    # report_path=models.CharField(max_length=100, blank=False, null=True)
    # status_flag=models.IntegerField(default=0)
    send_to=models.CharField(max_length=100, blank=False, null=True)
    modified_by=models.CharField(max_length=100, blank=False, null=True)
    created_by=models.CharField(max_length=100, blank=False, null=True)
    item_type=models.CharField(max_length=10, blank=False, null=True)
    status = models.CharField(max_length=10, blank=False, null=True)
    insp_last=models.IntegerField(blank=False, null=True)
    start_date=models.DateField(auto_now=False, null=True)
    inspected_on=models.DateField(auto_now=False, null=True)
    final_submit_on=models.DateField(null=True)
    station_name=models.CharField(max_length=50, blank=False, null=True)
    officer_name=models.CharField(max_length=100, blank=False, null=True)
    officer_desig=models.CharField(max_length=50, blank=False, null=True)
    item_sections = models.IntegerField(default=0, null=True)
    insp_type=models.IntegerField(default=0)
    deleted_on = models.DateTimeField(auto_now_add=True)

class deleted_data_Item_details(models.Model):
    item_no=models.BigAutoField(primary_key=True)   
    item_title=models.CharField(max_length=3000, blank=False, null=True)
    inspection_no=models.ForeignKey('Inspection_details', on_delete=models.CASCADE, null=True)
    status=models.CharField(max_length=10, blank=False, null=True)
    status_flag=models.IntegerField(default=0)
    observation=models.CharField(max_length=3000, blank=False, null=True)
    modified_on=models.DateTimeField(auto_now=False, null=True)
    created_on=models.DateTimeField(auto_now=False, null=True)
    modified_by=models.CharField(max_length=15, blank=False, null=True)
    created_by=models.CharField(max_length=15, blank=False, null=True)
    target_date=models.DateField(null=True)
    item_subtitle=models.CharField(max_length=3000, blank=False, null=True)
    type=models.CharField(max_length=3, blank=False, null=True)
    item_link=models.CharField(max_length=20, blank=False, null=True)
    des_id=models.CharField(max_length=8, blank=False, null=True)
    priority=models.IntegerField(default=0)
    del_flag = models.IntegerField(default=0)
    tbl_data = models.TextField(default='[]')
    link_image=models.CharField(max_length=200,null=True)
    action_type=models.IntegerField(default=0)
    update_status = models.CharField(default='T',max_length=1)
    sl_no =  models.IntegerField(null=True)
    markofcRemarks = models.CharField(max_length=500,null=True)
    item_type=models.IntegerField(default=0)
    location_table=models.CharField(max_length=50,null=True)
    location_code=models.CharField(max_length=10,null=True)
    location_val=models.CharField(max_length=100,null=True)
    # hqid=models.ForeignKey('myadmin.railwayLocationMaster', on_delete=models.CASCADE, null=True,related_name='item_rly_id')
    # divid=models.ForeignKey('myadmin.railwayLocationMaster', on_delete=models.CASCADE, null=True,related_name='item_div_id')

class deleted_data_Mrked_Officers(models.Model):
    marked_no=models.BigAutoField(primary_key=True)
    marked_to=models.ForeignKey('myadmin.Level_Desig', on_delete=models.CASCADE, null=True)
    marked_emp=models.CharField(max_length=100, blank=False, null=True)
    # ForeignKey('empmast', on_delete=models.CASCADE, null=True)
    item_no=models.ForeignKey('Item_details', on_delete=models.CASCADE, null=True)
    compliance=models.CharField(max_length=3000, blank=False, null=True)
    compliance_recieved_on=models.DateTimeField(auto_now=False, null=True)
    modified_on=models.DateTimeField(auto_now=False, null=True)
    created_on=models.DateTimeField(auto_now=True, null=True)
    modified_by=models.CharField(max_length=15, blank=False, null=True)
    created_by=models.CharField(max_length=15, blank=False, null=True)
    myuser_id=models.ForeignKey('MyUser', on_delete=models.CASCADE, null=True)
    status_flag=models.IntegerField(null=True)
    reply_on=models.DateField(null=True)
    revert=models.CharField(max_length=500,blank=False, null=True)
    reverted_on=models.DateField(null=True)
    status=models.CharField(max_length=1,blank=False, null=True)
    viewed_on=models.DateField(auto_now=False,null=True)
    target_flag=models.IntegerField(default=0)
    update_status = models.CharField(default='T',max_length=1)
    priority=models.IntegerField(default=0)
    target_date=models.DateField(null=True)
    action_type=models.IntegerField(default=0)
    marked_on=models.DateTimeField(null=True)
    add_status=models.IntegerField(default=0)

class deleted_data_target_compliance(models.Model):
    target_id=models.BigAutoField(primary_key=True)
    target_date=models.DateField(auto_now=False,null=True)
    status_flag=models.IntegerField(null=True)
    marked_no=models.ForeignKey('Marked_Officers', on_delete=models.CASCADE, null=True)
    marked_einsp=models.ForeignKey('einspect.einsp_marked', on_delete=models.CASCADE, null=True)
    reply_sent=models.CharField(max_length=3000, blank=False, null=True)
    rejected_on=models.DateTimeField(auto_now=False, null=True)
    reply_on=models.DateTimeField(auto_now=False, null=True)
    remark = models.CharField(max_length=200, blank=False, null=True)
    # pending_with=models.ForeignKey('myadmin.Level_Desig', related_name='pending',on_delete=models.CASCADE, null=True)
    # assigned_by=models.ForeignKey('myadmin.Level_Desig', related_name='assigned', on_delete=models.CASCADE, null=True)
    task_type=models.CharField(max_length=20, blank=False, null=True)
    init_date=models.DateField(auto_now=False,null=True)
    task_flag=models.IntegerField(null=True,default=1)
    task_descp=models.CharField(max_length=3000, blank=False, null=True)

class deleted_data_target_status(models.Model):
    status_id=models.BigAutoField(primary_key=True)
    target_no=models.ForeignKey('target_compliance', on_delete=models.CASCADE, null=True)
    status_flag=models.IntegerField(null=True)
    reply_sent=models.CharField(max_length=3000, blank=False, null=True)
    reply_on=models.DateTimeField(auto_now=False, null=True)
    rejected_on=models.DateTimeField(auto_now=False, null=True)
    remark = models.CharField(max_length=200, blank=False, null=True)

class deleted_data_Marked_Officers_forward(models.Model):
    marked_no_forward=models.BigAutoField(primary_key=True)
    marked_to_forward=models.ForeignKey('myadmin.Level_Desig', on_delete=models.CASCADE, null=True)
    marked_no=models.ForeignKey('Marked_Officers', on_delete=models.CASCADE, null=True)
    compliance_forward=models.CharField(max_length=3000, null=True)
    compliance_recieved_on_forward=models.DateTimeField(auto_now=False, null=True)
    modified_on_forward=models.DateTimeField(auto_now=False, null=True)
    created_on_forward=models.DateTimeField(auto_now=False, null=True)
    modified_by_forward=models.CharField(max_length=10, blank=False, null=True)
    created_by_forward=models.CharField(max_length=10, blank=False, null=True)
    myuser_id=models.ForeignKey('MyUser', on_delete=models.CASCADE, null=True)
    status_flag=models.IntegerField(null=True)
    reply_on=models.DateField(null=True)
    viewed_on=models.DateField(auto_now=False,null=True)
    level=models.IntegerField(default=0)
    further_forward=models.ForeignKey('Marked_Officers_forward', on_delete=models.CASCADE, null=True)

class deleted_data_Insp_multi_location(models.Model):
    location_no=models.BigAutoField(primary_key=True)
    inspection_no=models.ForeignKey('Inspection_details',on_delete=models.CASCADE, null=True) #on_delete=models.CASCADE
    item=models.CharField(max_length=50,null=False)
    item_code=models.CharField(max_length=10,null=True)
    type=models.CharField(max_length=5, null=True)
    d_flag=models.IntegerField(default=0)
    table_from=models.CharField(max_length=5,null=True)
    update_status = models.CharField(default='T',max_length=1)

class deleted_data_Insp_Accompany(models.Model):
    accompany_no=models.AutoField(primary_key=True)
    inspection_no=models.ForeignKey('Inspection_details',on_delete=models.CASCADE, null=True) #on_delete=models.CASCADE
    accompany=models.CharField(max_length=50,null=True)
    created_on=models.DateTimeField(auto_now=True)
    update_status = models.CharField(default='T',max_length=1)

    