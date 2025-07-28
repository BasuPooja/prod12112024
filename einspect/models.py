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

# class einsp_roster(models.Model):
#     erosterid=models.AutoField(primary_key=True,editable=False,unique=True)
#     fromdate=models.DateField(null=True, blank = True)
#     todate=models.DateField(null=True, blank = True)
#     status=models.IntegerField(max_length=1, blank=False,null=True) 
#     rly_id_id=models.ForeignKey('myadmin.railwaylocationmaster',related_name= 'railwaylocation_master_railways_einsp_roster',on_delete=models.CASCADE,null=True)
#     div_id_id=models.ForeignKey('myadmin.railwaylocationmaster',related_name= 'railwaylocation_master_division_einsp_roster',on_delete=models.CASCADE,null=True)
#     created_by=models.CharField( max_length=20, blank=True, null=True)
#     lastmodified_by=models.CharField( max_length=20, blank=True, null=True)
#     created_on=models.DateTimeField(null=True, blank = True)
#     lastmodified_on=models.DateTimeField(null=True, blank = True)
#     delete_flag=models.BooleanField(default=False)
#     designation=models.ForeignKey('myadmin.level_desig',on_delete=models.CASCADE, null=True)

# class roster_detail(models.Model):
#     rostdetailid=models.AutoField(primary_key=True,editable=False,unique=True)
#     roster_id=models.ForeignKey('einsp_roster',on_delete=models.CASCADE, null=True)
#     # inspection_officer_id=models.CharField(max_length=30,null=True) #designation
#     designation=models.ForeignKey('myadmin.level_desig',on_delete=models.CASCADE, null=True)
#     doi=models.DateField(null=True, blank = True) #date
#     inspectiontype_id=models.ForeignKey('myadmin.inspectiontype_master',on_delete=models.CASCADE, null=True)
#     inspectionof=models.CharField(max_length=30,null=True) #shortcode(fp,op,si)
#     section=models.CharField(max_length=30,null=True)#section code
#     # ForeignKey('section_master',on_delete=models.CASCADE, null=True)
#     detail=models.CharField(max_length=30,null=True)
#     # ForeignKey('station_master',on_delete=models.CASCADE,null=True)
#     # endstn=models.CharField(max_length=30)
#     # ForeignKey('station_master',on_delete=models.CASCADE,null=True)
#     status=models.IntegerField(max_length=1, blank=False,null=True) 
#     created_by=models.CharField( max_length=20, blank=True, null=True) 
#     lastmodified_by=models.CharField( max_length=20, blank=True, null=True)
#     created_on=models.DateTimeField(null=True, blank = True)
#     lastmodified_on=models.DateTimeField(null=True, blank = True)
#     delete_flag=models.BooleanField(default=False)


class einsp_multi_location(models.Model):
    location_no=models.BigAutoField(primary_key=True)
    einspno=models.ForeignKey('einspection_details',on_delete=models.CASCADE, null=True) 
    item=models.CharField(max_length=50,null=False)
    type=models.CharField(max_length=5, null=True)


class einspection_coach_details(models.Model):
    location_no=models.BigAutoField(primary_key=True)
    einspno=models.ForeignKey('einspection_details',on_delete=models.CASCADE, null=True) 
    item=models.CharField(max_length=50,null=False)
    type=models.CharField(max_length=10, null=True)
    startdate=models.DateField(null=True, blank = True)
    
class einspection_details(models.Model):
    einspno=models.AutoField(primary_key=True,editable=False,unique=True)
    instypeid=models.ForeignKey('myadmin.inspectiontype_master',on_delete=models.CASCADE,null=True)
    #inspection_officer_id=models.ForeignKey('inspects.empmast',on_delete=models.CASCADE,null=True)
    inspected_on=models.DateTimeField(null=True, blank = True)
    inspection_title=models.CharField(max_length=200,blank=False,null=True)
    designation=models.ForeignKey('myadmin.Level_Desig',on_delete=models.CASCADE,null=True)
    inspection_note_no=models.CharField(max_length=100,blank=True,null=True)
    status=models.IntegerField(max_length=1,blank=False,null=False)
    #dept=models.CharField(max_length=20, blank=False, null=True)
    dept=models.ForeignKey('myadmin.departMast', on_delete=models.CASCADE, null=True)
    report_path=models.CharField(max_length=50, blank=False, null=True)
    startstn=models.ForeignKey('myadmin.station_master',related_name= 'station_master_start',on_delete=models.CASCADE,null=True)
    endstn=models.ForeignKey('myadmin.station_master',related_name = 'station_master_end',on_delete=models.CASCADE,null=True)
    entitydetails=models.CharField(max_length=50,blank=False,null=True)
    entityid=models.CharField(max_length=50,null=True)
    masterTableFlag = models.CharField(max_length=1, default = 0)
    # rostetrdetail_id=models.CharField(max_length=50,blank=False,null=True )
    # ForeignKey('roster_details',on_delete=models.CASCADE,null=False)
    created_by=models.CharField( max_length=20, blank=True, null=True)
    lastmodified_by=models.CharField( max_length=20, blank=True, null=True)
    created_on=models.DateTimeField(null=True, blank = True)
    lastmodified_on=models.DateTimeField(null=True, blank = True)
    delete_flag=models.BooleanField(default=False)
    is_scheduled=models.BooleanField(default=True)
    section=models.ForeignKey('myadmin.section_master',on_delete=models.CASCADE, null=True)
    start_date=models.DateField(null=True, blank = True)
    end_date=models.DateField(null=True, blank = True)
    start_time=models.TimeField(auto_now=False,null=True)
    end_time=models.TimeField(auto_now=False,null=True)
    rly_id_id=models.ForeignKey('myadmin.railwaylocationmaster',related_name= 'railwaylocation_master_railways_einspection_details',on_delete=models.CASCADE,null=True)
    div_id_id=models.ForeignKey('myadmin.railwaylocationmaster',related_name= 'railwaylocation_master_division_einspection_details',on_delete=models.CASCADE,null=True)
    ratings=models.IntegerField(default=5,null=True,blank=True)
    abnormal=models.CharField(max_length=100,blank=False,null=True, default='No')
    documents=models.FileField(null=True, blank=True,upload_to='documents/')
    location = models.CharField(max_length=100,blank=False,null=True)
    priority = models.CharField(max_length=10,blank=False,null=True)
    drm = models.CharField(max_length=50,null=True)
    gm = models.CharField(max_length=50,null=True)
    inspection_type=models.IntegerField(max_length=1,blank=False,null=False,default=1)  # surprise - 1 , night - 2, surprise & night - 3, no surprise & night - 4
    commanDepartment = models.CharField(max_length=100,null=True)
    commanDesignation = models.CharField(max_length=100,null=True)
    finalizeStart = models.CharField(max_length=3,null=True)  
    finalizeEnd = models.CharField(max_length=3,null=True)
   


class einspection_item_detail(models.Model):
    eitemid=models.AutoField(primary_key=True,editable=False,unique=True)
    einspno=models.ForeignKey('einspection_details',on_delete=models.CASCADE,null=True)
    qid=models.ForeignKey('questionare_master',on_delete=models.CASCADE,null=True)
    qncat = models.ForeignKey('myadmin.inspectiontype_master',on_delete=models.CASCADE,null=True)
    value_id = models.ForeignKey('radio_options',on_delete=models.CASCADE,null=True)
    status=models.IntegerField(max_length=1,null=True)
    value=models.TextField(blank=False,null=True )

    remarks=models.TextField(blank=False,null=True )
    target_date=models.DateTimeField(null=True, blank = True)
    qtype=models.CharField(max_length=50,blank=False,null=True, default='E-Inspection' )
    created_by=models.CharField(max_length=50,blank=False,null=True )
    lastmodified_by=models.CharField(max_length=50,blank=False,null=True )
    created_on=models.DateTimeField(null=True, blank = True)
    lastmodified_on=models.DateTimeField(null=True, blank = True)
    delete_flag=models.BooleanField(default=False)
    location=models.CharField(max_length=500,blank=True,null=True)
    priority=models.CharField(max_length=1,blank=True,null=True)
    item_type_id=models.ForeignKey('myadmin.question_sub_category_master',on_delete=models.CASCADE,null=True)

class questionare_master(models.Model):
    qid=models.AutoField(primary_key=True)
    instypeid_id=models.ForeignKey('myadmin.inspectiontype_master', on_delete=models.CASCADE)
    activity=models.CharField(max_length=1000)
    choicetype = models.ForeignKey('choicetype_master',on_delete=models.CASCADE, null=True)
    roption1 = models.ForeignKey('radio_options', related_name = "firstOption", on_delete=models.CASCADE, null=True)
    roption2 = models.ForeignKey('radio_options', related_name = "secondOption" ,on_delete=models.CASCADE, null=True)
    doption = models.ForeignKey('dropdown_options',on_delete=models.CASCADE, null=True)
    created_by=models.CharField( max_length=20, blank=True, null=True)
    lastmodified_by=models.CharField( max_length=20, blank=True, null=True)
    created_on=models.DateTimeField(null=True, blank = True, auto_now=True)
    lastmodified_on=models.DateTimeField(null=True, blank = True, auto_now=True)
    delete_flag=models.BooleanField(default=False)
    option1 = models.CharField( max_length=50, blank=True, null=True)
    option2 = models.CharField( max_length=50, blank=True, null=True)
    option3 = models.CharField( max_length=50, blank=True, null=True)
    priority = models.CharField( max_length=10, blank=True, null=True)
    report_act=models.CharField(max_length=500,blank=True,null=True )
    location = models.ForeignKey('location_master',on_delete=models.CASCADE, null=True)
    depending_ques = models.CharField(max_length=50,blank=True,null=True )
    dependent_ques = models.IntegerField(blank=True,null=True )
    dependending_column = models.CharField(max_length=20,blank=True,null=True )
    disable_flag=models.BooleanField(default=False)
    compulsary=models.BooleanField(default=False)
    desc = models.CharField(max_length=100,blank=True,null=True )
    question_sub_id=models.ForeignKey('myadmin.question_sub_category_master', on_delete=models.CASCADE,null=True)
    actionBy = models.CharField(max_length=3,blank=True,null=True )
    mixedChoices  = models.CharField(max_length=1000,blank=True,null=True )
    weightage = models.IntegerField(default=1)



class choicetype_master(models.Model):
    cid = models.AutoField(primary_key=True)
    input_type = models.CharField(max_length=20, null=True)

class radio_options(models.Model):
    rid = models.AutoField(primary_key=True)
    rscore = models.IntegerField(max_length=1,null=True)
    rlabel = models.CharField(max_length=20, null=True)

class dropdown_options(models.Model):
    did = models.AutoField(primary_key=True)
    dmaster = models.CharField(max_length=20, null=True)
    table_name = models.CharField(max_length=30, null=True)
    column_name = models.CharField(max_length=200, null=True) ##  seperate with comma
    filterName = models.CharField(max_length=20,null=True) # only one fiter column
    filterValue = models.CharField(max_length=60,null=True)

class seperator_options(models.Model):
    sid = models.AutoField(primary_key=True)
    table_name = models.CharField(max_length=30, null=True)
    seperator_column = models.CharField(max_length=20, null=True)
    seperator = models.CharField(max_length=2, null=True)
    class Meta:
        unique_together = (('table_name', 'seperator_column'),)


class einsp_marked(models.Model):
    id=models.AutoField(primary_key=True, editable=False, unique=True)
    eitemid=models.ForeignKey('einspection_item_detail',on_delete=models.CASCADE,null=True,related_name="einspection_item_detail_fk")
    marked_to=models.ForeignKey('myadmin.level_desig',on_delete=models.CASCADE,null=True)
    department =models.ForeignKey('myadmin.departMast',on_delete=models.CASCADE,null=True)
    designation=models.CharField(max_length=100,null=True)
    designation_by=models.CharField(max_length=100,null=True)
    marked_emp_id=models.CharField(max_length=50,blank=False,null=True )
    compliance=models.CharField(max_length=500, blank=False, null=True)
    compliance_recieved_on=models.DateTimeField(null=True, blank = True)
    status_flag=models.IntegerField(max_length=1, blank=False,null=True)
    revert=models.IntegerField(blank=True,null=True )
    reverted_on=models.DateTimeField(null=True, blank = True)
    created_by=models.CharField( max_length=20, blank=True, null=True)
    lastmodified_by=models.CharField( max_length=20, blank=True, null=True)
    created_on=models.DateTimeField(null=True, blank = True)
    lastmodified_on=models.DateTimeField(null=True, blank = True)
    delete_flag=models.BooleanField(default=False)
    counter=models.IntegerField(null=True,blank=True)
    forward_count=models.IntegerField(null=True,blank=True)
    parent_mark=models.IntegerField(null=True,default=-1)
    target_date = models.DateField(null=True)
    target_date_given_on = models.DateField(null=True)
    reject=models.IntegerField(blank=True,null=True )

class einsp_officers_remark(models.Model):
    remark_no=models.BigAutoField(primary_key=True)
    marked_no=models.ForeignKey('einsp_marked', on_delete=models.CASCADE, null=True)
    remark = models.CharField(max_length=200, blank=False, null=True)
    reply_received=models.CharField(max_length=3000, blank=False, null=True)
    rejected_on=models.DateTimeField(auto_now=False, null=True)
    reply_on=models.DateTimeField(auto_now=False, null=True)
    status = models.CharField(max_length=10, blank=False, null=True)
    status_flag = models.IntegerField(default=0)
    marked_no_forward=models.ForeignKey('einsp_forward_marked', on_delete=models.CASCADE, null=True)
    marked_desig_id=models.ForeignKey('myadmin.Level_Desig', on_delete=models.CASCADE, null=True)


class Siri_Report(models.Model):
    report_id=models.AutoField(primary_key=True)
    empno_report=models.CharField(max_length=20,null=False)
    designation_code_report=models.ForeignKey('myadmin.level_desig',on_delete=models.CASCADE, null=True)
    # empno_conc=models.CharField(max_length=20,null=False)
    # designation_code_conc=models.ForeignKey('myadmin.level_desig',on_delete=models.CASCADE, null=True)
    rly_unit_code = models.ForeignKey('myadmin.railwaylocationmaster', on_delete=models.CASCADE, null=True)
    # department_name=models.ForeignKey('departmast',on_delete=models.CASCADE, null=True)
    #rly_unit_code=models.IntegerField(null=False)
    department_name=models.CharField(max_length=50,null=False)
    zone=models.CharField(max_length=50,null=True)
    division=models.CharField(max_length=50,null=True)    
    rly_id_id=models.ForeignKey('myadmin.railwaylocationmaster',related_name= 'railwaylocation_master_railways_Siri_Report',on_delete=models.CASCADE,null=True)
    div_id_id=models.ForeignKey('myadmin.railwaylocationmaster',related_name= 'railwaylocation_master_division_Siri_Report',on_delete=models.CASCADE,null=True)
    location=models.CharField(max_length=20, blank=False, null=False)
    issue_title=models.CharField(max_length=20, blank=False, null=False)
    issue_descp=models.CharField(max_length=250, blank=False, null=False)
    priority=models.CharField(max_length=10,blank=False, null=False)
    image_path=models.CharField(max_length=150, blank=False, null=True)
    report_time=models.DateTimeField(null=True, blank = True)
    gm_flag=models.CharField(max_length=20,null=True) 
    drm_flag=models.CharField(max_length=20,null=True)
    status_flag=models.IntegerField(default=1,null=True)
    pri_index=models.IntegerField(default=0,null=True)
    remark=models.CharField(max_length=200,default="Pending" ,null=True)  

class siri_images(models.Model):
    image_id = models.AutoField(primary_key=True)
    report_it_id = models.ForeignKey('einspect.report_it', on_delete=models.CASCADE, null=True)
    imagepaths = models.FileField(upload_to='specification/',null=True)

class report_it(models.Model):
    id = models.AutoField(primary_key = True)
    rly_unit_code = models.CharField(max_length=10,null=True)
    empno_report=models.CharField(max_length=20,null=True)
    rlyorg = models.CharField(max_length=5 ,null=True)
    division = models.CharField(max_length=20,null=True)    
    rly_id_id=models.ForeignKey('myadmin.railwaylocationmaster',related_name= 'railwaylocation_master_railways_report_it',on_delete=models.CASCADE,null=True)
    div_id_id=models.ForeignKey('myadmin.railwaylocationmaster',related_name= 'railwaylocation_master_division_report_it',on_delete=models.CASCADE,null=True)
    department = models.CharField(max_length=50,null=True)
    issuetitle = models.CharField(max_length=20,blank=False,null=True)
    issuedescription = models.CharField(max_length=250,blank=False,null=True)
    location = models.CharField(max_length=100,blank=False,null=True)
    priority = models.CharField(max_length=10,blank=False,null=True)
    other = models.CharField(max_length=50,blank=False,null=True)
    reporttime =models.DateTimeField(null=True, blank = True)
    imagepath = models.FileField(upload_to='specification/',null=True)
    remarks = models.CharField(max_length=100,null=True,default="Pending")
    status_flag = models.IntegerField(default=1,null=True)
    designation_code_id = models.IntegerField(null=True,blank=False)
    # designation_code_drm = models.IntegerField(null=True,blank=False)
    gm = models.CharField(max_length=50,null=True)
    drm = models.CharField(max_length=50,null=True)
    pri_index=models.IntegerField(default=0,null=True) 
    rly_zone=models.IntegerField(null=True)
    delete_flag = models.BooleanField(default=False)  
    entity = models.CharField(max_length=10,null=True)
    entityDetails = models.CharField(max_length=20,null=True)

class siri_marked(models.Model):
    id=models.AutoField(primary_key=True, editable=False, unique=True)
    report_it_id = models.ForeignKey('report_it', on_delete=models.CASCADE, null=True)
    marked_to=models.ForeignKey('myadmin.level_desig',on_delete=models.CASCADE,null=True)
    marked_emp_id=models.CharField(max_length=50,blank=False,null=True )
    # ForeignKey('empmast',on_delete=models.CASCADE,null=False)
    compliance=models.CharField(max_length=200, blank=False, null=True)
    compliance_recieved_on=models.DateField(null=True, blank = True)
    status_flag=models.IntegerField(max_length=1, blank=False,null=True)
    revert=models.CharField(max_length=50,blank=False,null=True )
    reverted_on=models.DateTimeField(null=True, blank = True)
    created_by=models.CharField( max_length=20, blank=True, null=True)
    lastmodified_by=models.CharField( max_length=20, blank=True, null=True)
    created_on=models.DateTimeField(null=True, blank = True)
    lastmodified_on=models.DateTimeField(null=True, blank = True)
    delete_flag=models.BooleanField(default=False)

class IssueCategory(models.Model):
    category_id=models.AutoField(primary_key=True)   
    department_code=models.ForeignKey('myadmin.departmast',on_delete=models.CASCADE, null=True) 
    issue_category=models.CharField(max_length=100,null=True)
    delete_flag=models.BooleanField(default=False)
    modified_by = models.CharField( max_length=20, blank=True, null=True)
    modified_on=models.DateTimeField(null=True, blank = True)
    created_on=models.DateTimeField(null=True, blank = True)
    
class custom_menu(models.Model):
    id=models.AutoField(primary_key=True, editable=False, unique=True)
    m_id=models.IntegerField(null=True)
    menu=models.CharField(max_length=50,null=True)
    url=models.CharField(max_length=100,null=True)
    parent_id=models.IntegerField(null=True)
    role=models.CharField(max_length=200,null=True)
    icons=models.CharField(max_length=100,null=True)
    delete_flag = models.BooleanField(default=False)

class location_master(models.Model):
    lid = models.AutoField(primary_key=True)
    lmaster = models.CharField(max_length=20, null=True)


class einsp_forward_marked(models.Model):
    forwardId=models.BigAutoField(primary_key=True)
    forwardTo=models.ForeignKey('myadmin.Level_Desig', on_delete=models.CASCADE, null=True,related_name="einsp_forward_marked_forwardTo")
    forwardBy=models.ForeignKey('myadmin.Level_Desig', on_delete=models.CASCADE, null=True,related_name="einsp_forward_marked_forwardBy")
    designationTo=models.CharField(max_length=100,null=True)
    designationBy=models.CharField(max_length=100,null=True)
    marked_no=models.ForeignKey('einsp_marked', on_delete=models.CASCADE, null=True)
    remarks=models.CharField(max_length=500, null=True)
    created_date=models.DateTimeField(auto_now=False, null=True)
    created_by=models.CharField( max_length=20, blank=True, null=True)
    status_flag=models.IntegerField(null=True)
    reply_on=models.DateField(null=True)
    compliance=models.CharField(max_length=500, null=True)
    rejected_on=models.DateTimeField(auto_now=False, null=True)
    further_forward=models.IntegerField(null=True)
    parent_forward=models.ForeignKey('einsp_forward_marked', on_delete=models.CASCADE, null=True)





### added for actor link with category

class actor_with_question(models.Model):
    slno = models.BigAutoField(primary_key=True)
    questionId=models.ForeignKey('questionare_master', on_delete=models.CASCADE, null=True)
    actionId=models.ForeignKey('myadmin.actor_details', on_delete=models.CASCADE, null=True)
    created_by=models.CharField( max_length=20, blank=True, null=True)
    lastmodified_by=models.CharField( max_length=20, blank=True, null=True)
    created_on=models.DateTimeField(null=True, blank=True, auto_now=True)
    lastmodified_on=models.DateTimeField(null=True, blank=True, auto_now=True)
    disable_flag=models.BooleanField(default=False)


class actor_with_inspection_details(models.Model):
    slno = models.BigAutoField(primary_key=True)
    einspno=models.ForeignKey('einspection_details',on_delete=models.CASCADE,null=True)
    actorId=models.ForeignKey('myadmin.actor_details',on_delete=models.CASCADE,null=True)
    value=models.CharField( max_length=200, null=True)
    details = models.TextField(null=True)



class einsp_roster(models.Model):
    erosterid=models.AutoField(primary_key=True,editable=False,unique=True)
    fromdate=models.DateField(null=True, blank = True)
    todate=models.DateField(null=True, blank = True)
    inspection_type = models.CharField(max_length=100,null=True)
    status=models.IntegerField(max_length=1, blank=False,null=True, default=1) 
    roster_number = models.CharField(max_length=100,null=True)
    created_by = models.ForeignKey('myadmin.AdminMaster', related_name='created_by', on_delete=models.CASCADE, null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    lastmodified_on=models.DateTimeField(auto_now_add=True, null=True)
    delete_flag=models.BooleanField(default=False)


class custom_sections(models.Model):
    id = models.BigAutoField(primary_key=True)
    section_name = models.CharField(max_length=100, null=True)
    admin_user = models.ForeignKey('myadmin.AdminMaster', related_name='admin_user', on_delete=models.CASCADE, null=True)
    existing_section = models.ForeignKey('myadmin.section_master',on_delete=models.CASCADE, related_name='roster_section',null=True)
    from_station = models.ForeignKey('myadmin.station_master',on_delete=models.CASCADE,related_name='from_station', null=True)
    to_station = models.ForeignKey('myadmin.station_master',on_delete=models.CASCADE,related_name='to_station', null=True)
    is_used = models.BooleanField(default=False)
    added_on=models.DateTimeField(auto_now_add=True, null=True)    
    delete_flag = models.BooleanField(default=False)

class custom_desig(models.Model):
    id = models.BigAutoField(primary_key=True)
    admin_user = models.ForeignKey('myadmin.AdminMaster', related_name='admin_user_desig', on_delete=models.CASCADE, null=True)
    desig_name = models.ForeignKey('myadmin.level_desig',on_delete=models.CASCADE, null=True)
    is_used = models.BooleanField(default=False)
    added_on=models.DateTimeField(auto_now_add=True, null=True)    
    disable_flag = models.BooleanField(default=False)

class custom_inspection(models.Model):
    id = models.BigAutoField(primary_key=True)
    inspection_name = models.CharField(max_length=100, null=True)
    admin_user = models.ForeignKey('myadmin.AdminMaster', related_name='admin_user_insp', on_delete=models.CASCADE, null=True)
    is_used = models.BooleanField(default=False)
    added_on=models.DateTimeField(auto_now_add=True, null=True)    
    disable_flag = models.BooleanField(default=False)

class roster_detail(models.Model):
    rostdetailid=models.AutoField(primary_key=True,editable=False,unique=True)
    roster_id=models.ForeignKey('einsp_roster',on_delete=models.CASCADE, null=True)
    # inspection_officer_id=models.CharField(max_length=30,null=True) #designation
    
    doi=models.DateField(null=True, blank = True) #date
    custom_inspection=models.ForeignKey('custom_inspection',on_delete=models.CASCADE, null=True)
    custom_designation=models.ForeignKey('custom_desig',on_delete=models.CASCADE, null=True)
    add_data_insp = models.CharField(max_length=30,null=True) #shortcode(fp,op,si)
    custom_section=models.ForeignKey('custom_sections',on_delete=models.CASCADE, null=True)#section code
    status=models.IntegerField(max_length=1, blank=False,null=True) 
    created_on=models.DateTimeField(auto_now_add=True, null=True)
    close_date=models.DateTimeField(null=True)
    close_Remark=models.CharField(max_length=2000,null=True, blank=True)    
    delete_flag=models.BooleanField(default=False)




class einspection_department_display(models.Model):
    disp_no=models.AutoField(primary_key=True,editable=False,unique=True)
    dept=models.ForeignKey('myadmin.departMast', on_delete=models.CASCADE, null=True)
    instypeid=models.ForeignKey('myadmin.inspectiontype_master',on_delete=models.CASCADE,null=True)
    lastmodified_on=models.DateField(null=True)
    delete_flag=models.BooleanField(default=False)




