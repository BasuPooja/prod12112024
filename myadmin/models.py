
# from django.db import models
# from django.db import models
# from django.contrib.auth.models import User
# from datetime import datetime
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.shortcuts import reverse
# from rest_framework.authtoken.models import Token
# from django.conf import settings

# from django import dispatch

# # Create your models here.

# class railwayLocationMaster(models.Model):
#     rly_unit_code = models.AutoField(primary_key=True)
#     location_code = models.CharField(max_length=10,null=True)
#     location_type = models.CharField(max_length=5,null=True)
#     location_description = models.CharField(max_length=100)
#     parent_location_code = models.CharField(max_length=10) 
#     parent_id = models.IntegerField(max_length=50,null=True) 
#     last_update = models.DateTimeField(auto_now=True)
#     modified_by = models.CharField(max_length=30,null=True)
#     station_code= models.CharField(max_length=5,null=True)
#     rstype= models.CharField(max_length=15,null=True)
#     location_type_desc= models.CharField(max_length=20,null=True)

# class departMast(models.Model):
    
#     department_code = models.CharField(primary_key=True, max_length =10)
#     department_name=models.CharField(null = True,max_length =50, blank=True,unique=True)
#     rly_unit_code=models.ForeignKey('railwayLocationMaster', on_delete=models.CASCADE, null=True)
#     delete_flag=models.NullBooleanField(default=False,null=True)
#     modified_by = models.CharField( max_length=20, blank=True, null=True)
#     modified_on=models.DateTimeField(auto_now=True, null=True)
#     created_on=models.DateTimeField(auto_now_add=True,null=True)


# class Post_master(models.Model):
#     post_id = models.AutoField(primary_key=True)
#     department_code=models.ForeignKey('departMast', on_delete=models.CASCADE, null=True)
#     post_desc= models.CharField(max_length=50, blank=True, null=True)
#     rly_unit_code=models.ForeignKey('railwayLocationMaster', on_delete=models.CASCADE, null=True)
#     delete_flag=models.BooleanField(default=False)
#     modified_by = models.CharField( max_length=20, blank=True, null=True)
#     modified_on=models.DateTimeField(auto_now=True, null=True)
#     created_on=models.DateTimeField(auto_now_add=True,null=True)


# class Level_Desig(models.Model):
#     designation_code=models.AutoField(primary_key=True)  
#     # cat_id=models.IntegerField(null=True)    
#     designation=models.CharField(max_length=100,null=True)  
#     department=models.CharField(max_length=50,null=True)   
#     effectdate=models.DateTimeField(auto_now=True, null=True)
#     # un_officer_id=models.IntegerField(null=True)
#     # level=models.CharField(max_length=2,null=True)
#     # designation_code = models.CharField(max_length=15,null=True)
#     parent_desig_code= models.CharField(max_length=15,null=True)
#     department_code=models.ForeignKey('departMast', on_delete=models.CASCADE, null=True)
#     rly_unit=models.ForeignKey('railwayLocationMaster', on_delete=models.CASCADE, null=True)
#     pc7_levelmin = models.IntegerField(null=True, blank=True)
#     pc7_levelmax = models.IntegerField(null=True, blank=True)
#     modified_by = models.CharField( max_length=20, blank=True, null=True)
#     desig_user = models.ForeignKey('inspects.MyUser', on_delete=models.CASCADE, null=True)
#     status= models.CharField( max_length=2, blank=True, null=True)
#     empno=models.ForeignKey('inspects.empmast', on_delete=models.CASCADE, blank=True, null=True)
#     d_level=models.CharField( max_length=10, blank=True, null=True)
#     contactnumber=models.CharField(max_length=10, blank=True, null=True)
#     official_email_ID=models.CharField(max_length=50, blank=True, null=True, unique=True)
#     head_flag = models.IntegerField(null=True, blank=True)

# class category(models.Model):
#     id = models.AutoField(primary_key=True)
#     category = models.CharField( max_length=10, blank=True, null=True) 


# class roless(models.Model):
#     role = models.CharField(primary_key=True, max_length=50)
#     parent = models.CharField(max_length=50, blank=True, null=True)
#     # department_id=models.ForeignKey('department_master', on_delete=models.CASCADE, null=True)
#     rly_unit=models.CharField(max_length=50, blank=True, null=True)
#     modified_by = models.CharField( max_length=20, blank=True, null=True)
#     modified_on=models.DateTimeField(auto_now=True,null=True,blank=True)
#     created_on=models.DateTimeField(auto_now_add=True,null=True,blank=True)
#     delete_flag=models.NullBooleanField(default=False,null=True)
#     department_code=models.ForeignKey('departMast', on_delete=models.CASCADE, null=True)
#     designation_code= models.CharField( max_length=20, blank=True, null=True)
#     role_code = models.CharField( max_length=5, blank=True, null=True)
#     shop_code=models.CharField(null = True,max_length =50)



# class Shop_section(models.Model):
    
#     section_code = models.CharField( max_length =10)
#     section_id = models.CharField(primary_key=True,max_length =10)
#     section_desc = models.CharField(null = True,max_length =150)
#     shop_code = models.CharField(null = True,max_length =50)
#     shop_id = models.CharField(null = True,max_length =50)
#     flag = models.CharField(null = True,max_length =1)
#     rly_unit_code=models.CharField(max_length =3,null=True,blank=True)
#     department_code=models.ForeignKey('departMast', on_delete=models.CASCADE, null=True)
#     modified_by = models.CharField( max_length=20, blank=True, null=True)
#     modified_on=models.DateTimeField(auto_now=True,null=True,blank=True)
#     created_on=models.DateTimeField(auto_now_add=True,null=True,blank=True)

# #     class Meta:
        
# #         db_table = 'myadmin_shop_section'


# class custom_menu(models.Model):
#     m_id=models.IntegerField(null=True)
#     menu=models.CharField(max_length=50,null=True)
#     url=models.CharField(max_length=100,null=True)
#     perent_id=models.IntegerField(null=True)
#     role=models.CharField(max_length=200,null=True)


# class empmastnew(models.Model):
#     sno = models.IntegerField(primary_key=True)
#     emp_id=models.CharField(max_length=100,null=True)
#     # models.ForeignKey('inspects.empmast', on_delete=models.CASCADE)
#     shop_section = models.CharField(null = True,max_length =50)


# class locationMaster(models.Model):
#     pincode = models.IntegerField(primary_key=True)
#     district = models.CharField(max_length=30)
#     state = models.CharField(max_length=20)
#     city  = models.CharField(max_length=50, default="NA")


#     class Meta:
#         db_table = 'locationMaster'


# class AdminMaster(models.Model):
#     code = models.BigAutoField(primary_key=True)
#     address = models.CharField(max_length=100,null=True)
#     pincode = models.ForeignKey(locationMaster, on_delete=models.CASCADE,null=True)
#     admin = models.CharField(max_length=30)
#     admin_mobile = models.BigIntegerField(unique=True)
#     admin_phone = models.CharField(max_length=12,null=True)
#     admin_email = models.EmailField(unique=True)
#     rly = models.ForeignKey(railwayLocationMaster, on_delete=models.CASCADE)
#     status = models.CharField(max_length=10)
#     created_on=models.DateTimeField(auto_now_add=True,null=True)
#     emp_name=models.CharField(max_length=150,null=True)
#     designation=models.CharField(max_length=300,null=True)
#     user_id=models.ImageField(max_length=10,null=True)


#     def _str_(self):
#         return self.admin_email

#     class Meta:
#         db_table = 'AdminMaster'


# class HRMS(models.Model):
#     ipas_employee_id=models.CharField(max_length=15,null=False)    
#     hrms_employee_id=models.CharField(primary_key=True,max_length=6,null=False)
#     employee_first_name=models.CharField(max_length=150,null=True)
#     employee_middle_name=models.CharField(max_length=150,null=True)
#     employee_last_name=models.CharField(max_length=150,null=True)
#     date_of_birth=models.DateField(null=True)
#     appointment_date=models.DateField(null=True)
#     superannuation_date=models.DateField(null=True)    
#     gender=models.CharField(max_length=1,null=True)
#     community_sr=models.CharField(max_length=3,null=True)
#     service_status=models.CharField(max_length=50,null=True)
#     billunit=models.CharField(max_length=7,null=True)
#     railway_group=models.CharField(max_length=1,null=True)
#     current_zone=models.CharField(max_length=10,null=True)
#     current_unit_division=models.CharField(max_length=80,null=True)
#     rltype=models.CharField(max_length=20,null=True)
#     current_place=models.CharField(max_length=100,null=True)
#     department=models.CharField(max_length=50,null=True)
#     sub_department=models.CharField(max_length=50,null=True)
#     designation=models.CharField(max_length=300,null=True) 
#     paylevel=models.CharField(max_length=4,null=True)
#     official_mobile_no=models.CharField(max_length=10,null=True)
#     official_email_id=models.CharField(max_length=50,null=True)
#     txn_timestamp=models.DateTimeField(null=True)


# class station_master(models.Model):
#     stnshortcode=models.CharField(primary_key=True,editable=False,unique=True,max_length=6)
#     rly_id_id=models.ForeignKey('railwayLocationMaster',on_delete=models.CASCADE,blank=True, null=True)
#     division_code = models.CharField(max_length=10,null=True)
#     railway_code = models.CharField(max_length=10,null=True)
#     station_cat = models.CharField(max_length=2,null=True)
#     station_cat_id = models.ForeignKey('stationcat_master', on_delete=models.CASCADE,null=True)
#     lastmodified_by= models.CharField( max_length=20, blank=True, null=True)
#     created_by=models.CharField( max_length=20, blank=True, null=True)
#     station_name=models.CharField(max_length=50)
#     created_on=models.DateTimeField(auto_now=True)
#     lastmodified_on=models.DateTimeField(auto_now=True)
#     delete_flag=models.BooleanField(default=False)


# class stationcat_master(models.Model):
#     stnid=models.AutoField(primary_key=True,editable=False,unique=True)
#     stn_category=models.CharField(max_length=50)
#     lastmodified_by=models.CharField( max_length=20, blank=True, null=True)
#     created_by=models.CharField( max_length=20, blank=True, null=True)
#     created_on=models.DateTimeField(auto_now=True)
#     lastmodified_on=models.DateTimeField(auto_now=True)
#     delete_flag=models.BooleanField(default=False)


# class runningroom_master(models.Model):
#     rrid=models.AutoField(primary_key=True)
#     rr_name=models.CharField(max_length=50)
#     rr_code=models.CharField(max_length=10, unique=True)
#     stnshortcode=models.ForeignKey('station_master', on_delete=models.CASCADE, blank=True, null=True)
#     division_code = models.CharField(max_length=10,null=True)
#     railway_code = models.CharField(max_length=10,null=True)
#     created_by=models.CharField( max_length=20, blank=True, null=True)
#     lastmodified_by=models.CharField( max_length=20, blank=True, null=True)
#     created_on=models.DateTimeField(auto_now=True)
#     lastmodified_on=models.DateTimeField(auto_now=True)
#     delete_flag=models.BooleanField(default=False)
#     rly_id_id=models.ForeignKey('railwaylocationmaster',on_delete=models.CASCADE,null=True)

# class traincat_master(models.Model):
#     tcatid=models.AutoField(primary_key=True,editable=False,unique=True)
#     tn_category=models.CharField(max_length=50)
#     code=models.CharField(max_length=6, unique=True)
#     created_by=models.CharField( max_length=20, blank=True, null=True)
#     lastmodified_by=models.CharField( max_length=20, blank=True, null=True)
#     created_on=models.DateTimeField(auto_now=True)
#     lastmodified_on=models.DateTimeField(auto_now=True)
#     delete_flag=models.BooleanField(default=False)


# class train_master(models.Model):
#     tnid=models.AutoField(primary_key=True, editable=False, unique=True)
#     train_no=models.CharField(max_length=6,unique=True)
#     train_name=models.CharField(max_length=50)
#     tn_category=models.CharField(max_length=20,blank=False,null=True)
#     division_code = models.CharField(max_length=10,null=True)
#     railway_code = models.CharField(max_length=10,null=True)
#     # ForeignKey('traincat_master',on_delete=models.CASCADE,null=False)
#     stnsource_code=models.ForeignKey('station_master',related_name='station_master_stnsource_code',on_delete=models.CASCADE,null=True)
#     stndest_code=models.ForeignKey('station_master',related_name='station_master_stndest_code',on_delete=models.CASCADE,null=True)
#     total_coach=models.IntegerField(max_length=2)
#     created_by=models.CharField( max_length=20, blank=True, null=True)
#     lastmodified_by=models.CharField( max_length=20, blank=True, null=True)
#     created_on=models.DateTimeField(auto_now=True)
#     lastmodified_on=models.DateTimeField(auto_now=True)
#     delete_flag=models.BooleanField(default=False)
#     trainowngrly2=models.ForeignKey('station_master',related_name='station_master_trainowngrly2', on_delete=models.CASCADE,null=True)


# class inspectiontype_master(models.Model):
#     instypeid=models.AutoField(primary_key=True, editable=False, unique=True)
#     name=models.CharField(max_length=50)
#     shortcode=models.CharField(max_length=10)
#     entity=models.CharField(max_length=50)
#     parent_id=models.CharField(max_length=10, unique=False)
#     statuschecklist=models.IntegerField(max_length=1,blank=False,null=True)
#     created_by=models.CharField( max_length=20, blank=True, null=True)
#     lastmodified_by=models.CharField( max_length=20, blank=True, null=True)
#     created_on=models.DateTimeField(auto_now=True)
#     lastmodified_on=models.DateTimeField(auto_now=True)
#     delete_flag=models.BooleanField(default=False)
#     inspection_image=models.ImageField(null=True, blank=True,upload_to='images11/')

# class section_master(models.Model):   
#     secid = models.AutoField(primary_key=True,editable=False,unique=True)
#     section_code=models.CharField(max_length=20,blank=False,null=True)
#     secstart_code = models.ForeignKey('station_master',related_name = 'station_master_secstart_code',on_delete=models.CASCADE,null=True)
#     secend_code = models.ForeignKey('station_master',related_name = 'station_master_secend_code',on_delete=models.CASCADE,null=True)
#     via =  models.CharField(max_length=100,null=True)
#    # models.ForeignKey('station_master',related_name = 'station_master_via',on_delete=models.CASCADE,null=True)
#     division_code = models.CharField(max_length=10,null=True)
#     railway_code = models.CharField(max_length=10,null=True)
#     startkm = models.IntegerField(max_length=5)
#     endkm = models.IntegerField(max_length=5)
#     rly_id_id=models.ForeignKey('railwaylocationmaster',on_delete=models.CASCADE,null=True)
#     created_by=models.CharField( max_length=20, blank=True, null=True)
#     lastmodified_by=models.CharField( max_length=20, blank=True, null=True)
#     created_on=models.DateTimeField(auto_now=True)
#     lastmodified_on=models.DateTimeField(auto_now=True)
#     delete_flag=models.BooleanField(default=False)



# class Level_Desig_temp(models.Model):
#     designation_code=models.AutoField(primary_key=True)  
#     # cat_id=models.IntegerField(null=True)    
#     designation=models.CharField(max_length=100,null=True)  
#     department=models.CharField(max_length=50,null=True)   
#     effectdate=models.DateTimeField(auto_now=True, null=True)
#     # un_officer_id=models.IntegerField(null=True)
#     # level=models.CharField(max_length=2,null=True)
#     # designation_code = models.CharField(max_length=15,null=True)
#     parent_desig_code= models.CharField(max_length=15,null=True)
#     department_code=models.CharField(max_length=15,null=True)
#     # ForeignKey('departMast', on_delete=models.CASCADE, null=True)
#     rly_unit=models.CharField(max_length=15,null=True)
#     # ForeignKey('railwayLocationMaster', on_delete=models.CASCADE, null=True)
#     pc7_levelmin = models.IntegerField(null=True, blank=True)
#     pc7_levelmax = models.IntegerField(null=True, blank=True)
#     modified_by = models.CharField( max_length=20, blank=True, null=True)
#     desig_user = models.CharField(max_length=15,null=True)
#     # ForeignKey('inspects.MyUser', on_delete=models.CASCADE, null=True)
#     status= models.CharField( max_length=2, blank=True, null=True)
#     empno=models.CharField(max_length=15,null=True)
#     # ForeignKey('inspects.empmast', on_delete=models.CASCADE, blank=True, null=True)
#     d_level=models.CharField( max_length=4, blank=True, null=True)





# class Level_Desig_temp1(models.Model):
#     designation_code=models.AutoField(primary_key=True)  
#     # cat_id=models.IntegerField(null=True)    
#     designation=models.CharField(max_length=100,null=True)  
#     department=models.CharField(max_length=50,null=True)   
#     effectdate=models.DateTimeField(auto_now=True, null=True)
#     # un_officer_id=models.IntegerField(null=True)
#     # level=models.CharField(max_length=2,null=True)
#     # designation_code = models.CharField(max_length=15,null=True)
#     parent_desig_code= models.CharField(max_length=15,null=True)
#     department_code=models.IntegerField(null=True)
#     # ForeignKey('departMast', on_delete=models.CASCADE, null=True)
#     rly_unit=models.IntegerField(null=True)
#     # ForeignKey('railwayLocationMaster', on_delete=models.CASCADE, null=True)
#     pc7_levelmin = models.IntegerField(null=True, blank=True)
#     pc7_levelmax = models.IntegerField(null=True, blank=True)
#     modified_by = models.CharField( max_length=20, blank=True, null=True)
#     #desig_user = models.ForeignKey('inspects.MyUser', on_delete=models.CASCADE, null=True)
#     desig_user=models.IntegerField(null=True)
#     status= models.CharField( max_length=2, blank=True, null=True)
#     #empno=models.ForeignKey('inspects.empmast', on_delete=models.CASCADE, blank=True, null=True)
#     empno= models.CharField( max_length=50, blank=True, null=True)
#     d_level=models.CharField( max_length=4, blank=True, null=True)
#     contactnumber=models.CharField(max_length=10, blank=True, null=True)
#     official_email_ID=models.CharField(max_length=50, blank=True, null=True, unique=True)



# class loco_master(models.Model):
#     loco_id = models.AutoField( primary_key=True) 
#     loco_cat = models.CharField(max_length=15, null=True)
#     loco_no = models.CharField(max_length=8, null=True)
#     mfg_name = models.CharField(max_length=10, null=True)
#     mfg_full_name = models.CharField(max_length=100, null=True)
#     loco_type = models.CharField(max_length=20, null=True)
#     loco_shed = models.CharField(max_length=10, null=True)
#     division_code = models.CharField(max_length=10, null=True)
#     railway_code = models.CharField(max_length=10, null=True)
#     gauge = models.CharField(max_length=2, null=True)
#     wheel_arr = models.CharField(max_length=10, null=True)
#     qty_built = models.IntegerField( null=True)
#     built_year = models.CharField(max_length=8, null=True)
#     turned_out_date = models.DateField(null=True)
#     shed_in_date = models.DateField(null=True)
#     doc_in_date = models.DateField(null=True)
#     power = models.CharField(max_length=10, null=True)
#     running_status = models.CharField(max_length=15, null=True)
#     Loco_description = models.CharField(max_length=30, null=True)
#     Loco_remarks = models.CharField(max_length=100, null=True)
#     max_capacity = models.CharField(max_length=100, null=True)
#     max_speed = models.IntegerField(null=True)
#     created_by = models.CharField(max_length=20, null=True)
#     lastmodified_by = models.CharField(max_length=20, null=True)
#     created_on = models.DateTimeField(auto_now=True, null=True)
#     lastmodified_on = models.DateTimeField(auto_now=True, null=True)
#     delete_flag = models.BooleanField(default=False)

    
################    27/09/22


from django.db import models
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import reverse
from rest_framework.authtoken.models import Token
from django.conf import settings

from django import dispatch

# Create your models here.

class railwayLocationMaster(models.Model):
    rly_unit_code = models.AutoField(primary_key=True)
    location_code = models.CharField(max_length=10,null=True)
    location_type = models.CharField(max_length=5,null=True)
    location_description = models.CharField(max_length=100)
    parent_location_code = models.CharField(max_length=10) 
    parent_id = models.IntegerField(max_length=50,null=True) 
    last_update = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=30,null=True)
    station_code= models.CharField(max_length=5,null=True)
    rstype= models.CharField(max_length=15,null=True)
    location_type_desc= models.CharField(max_length=20,null=True)
    delete_flag=models.BooleanField(default=False)
    deleted_flag=models.BooleanField(default=False)
    parent_rly_unit_code=models.CharField(max_length=10,null=True)


class Railwayunit(models.Model):
    Unit_description=models.CharField(null = True,max_length =100, blank=True,unique=True)
    Unit_shortcode = models.CharField(max_length=20,null=True)

class departMast(models.Model):
    
    department_code = models.CharField(primary_key=True, max_length =10)
    department_name=models.CharField(null = True,max_length =50, blank=True,unique=True)
    rly_unit_code=models.ForeignKey('railwayLocationMaster', on_delete=models.CASCADE, null=True)
    delete_flag=models.BooleanField(default=False,null=True)
    modified_by = models.CharField( max_length=20, blank=True, null=True)
    modified_on=models.DateTimeField(auto_now=True, null=True)
    created_on=models.DateTimeField(auto_now_add=True,null=True)
    department = models.CharField(null=True, max_length =10,blank=False)


class Post_master(models.Model):
    post_id = models.AutoField(primary_key=True)
    department_code=models.ForeignKey('departMast', on_delete=models.CASCADE, null=True)
    post_desc= models.CharField(max_length=100, blank=True, null=True)
    # rly_unit_code=models.ForeignKey('railwayLocationMaster', on_delete=models.CASCADE, null=True)
    delete_flag=models.BooleanField(default=False)
    modified_by = models.CharField( max_length=20, blank=True, null=True)
    modified_on=models.DateTimeField(auto_now=True, null=True)
    created_on=models.DateTimeField(auto_now_add=True,null=True)
    post_code=models.CharField(max_length=25,blank=True,null=True)
    category = models.CharField( max_length=10, blank=True, null=True)
    pc7_levelmin = models.IntegerField(null=True, blank=True)
    pc7_levelmax = models.IntegerField(null=True, blank=True)



class Level_Desig(models.Model):
    designation_code=models.AutoField(primary_key=True)  
    # cat_id=models.IntegerField(null=True)    
    designation=models.CharField(max_length=100,null=True)  
    department=models.CharField(max_length=50,null=True)   
    effectdate=models.DateTimeField(auto_now=True, null=True)
    # un_officer_id=models.IntegerField(null=True)
    # level=models.CharField(max_length=2,null=True)
    # designation_code = models.CharField(max_length=15,null=True)
    parent_desig_code= models.CharField(max_length=15,null=True)
    department_code=models.ForeignKey('departMast', on_delete=models.CASCADE, null=True)
    rly_unit=models.ForeignKey('railwayLocationMaster', on_delete=models.CASCADE, null=True)
    pc7_levelmin = models.IntegerField(null=True, blank=True)
    pc7_levelmax = models.IntegerField(null=True, blank=True)
    modified_by = models.CharField( max_length=20, blank=True, null=True)
    desig_user = models.ForeignKey('inspects.MyUser', on_delete=models.CASCADE, null=True, related_name='desig_user')
    status= models.CharField( max_length=2, blank=True, null=True)
    empno=models.ForeignKey('inspects.empmast', on_delete=models.CASCADE, blank=True, null=True)
    d_level=models.CharField( max_length=10, blank=True, null=True)
    contactnumber=models.CharField(max_length=10, blank=True, null=True)
    official_email_ID=models.CharField(max_length=50, blank=True, null=True, unique=True)
    head_flag = models.IntegerField(null=True, blank=True)
    user_role =models.CharField(max_length=20, null=True)
    delete_flag=models.BooleanField(default=False)
    my_guest=models.ForeignKey('inspects.MyUser', on_delete=models.CASCADE, null=True, related_name='my_guest')
    station_name = models.CharField(max_length=100,null=True)
    hq_id = models.ForeignKey('railwayLocationMaster',related_name="hq_id", on_delete=models.CASCADE, null=True)
    div_id = models.ForeignKey('railwayLocationMaster',related_name="div_id", on_delete=models.CASCADE, null=True)
    hierarchy_level = models.IntegerField(null=True)

#class category(models.Model):
    # id = models.AutoField(primary_key=True)
    # category = models.CharField( max_length=10, blank=True, null=True)
    # user_role =models.CharField(max_length=20, null=True) 


class roless(models.Model):
    role = models.CharField(primary_key=True, max_length=50)
    parent = models.CharField(max_length=50, blank=True, null=True)
    # department_id=models.ForeignKey('department_master', on_delete=models.CASCADE, null=True)
    rly_unit=models.CharField(max_length=50, blank=True, null=True)
    modified_by = models.CharField( max_length=20, blank=True, null=True)
    modified_on=models.DateTimeField(auto_now=True,null=True,blank=True)
    created_on=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    delete_flag=models.BooleanField(default=False,null=True)
    department_code=models.ForeignKey('departMast', on_delete=models.CASCADE, null=True)
    designation_code= models.CharField( max_length=20, blank=True, null=True)
    role_code = models.CharField( max_length=5, blank=True, null=True)
    shop_code=models.CharField(null = True,max_length =50)



class Shop_section(models.Model):
    
    section_code = models.CharField( max_length =10)
    section_id = models.CharField(primary_key=True,max_length =10)
    section_desc = models.CharField(null = True,max_length =150)
    shop_code = models.CharField(null = True,max_length =50)
    shop_id = models.CharField(null = True,max_length =50)
    flag = models.CharField(null = True,max_length =1)
    rly_unit_code=models.CharField(max_length =3,null=True,blank=True)
    department_code=models.ForeignKey('departMast', on_delete=models.CASCADE, null=True)
    modified_by = models.CharField( max_length=20, blank=True, null=True)
    modified_on=models.DateTimeField(auto_now=True,null=True,blank=True)
    created_on=models.DateTimeField(auto_now_add=True,null=True,blank=True)

#     class Meta:
        
#         db_table = 'myadmin_shop_section'


class custom_menu(models.Model):
    m_id=models.IntegerField(null=True)
    menu=models.CharField(max_length=50,null=True)
    url=models.CharField(max_length=100,null=True)
    perent_id=models.IntegerField(null=True)
    role=models.CharField(max_length=200,null=True)
    icons=models.CharField(max_length=100,null=True) 


class empmastnew(models.Model):
    sno = models.IntegerField(primary_key=True)
    emp_id=models.CharField(max_length=100,null=True)
    # models.ForeignKey('inspects.empmast', on_delete=models.CASCADE)
    shop_section = models.CharField(null = True,max_length =50)


class locationMaster(models.Model):
    pincode = models.IntegerField(primary_key=True)
    district = models.CharField(max_length=30)
    state = models.CharField(max_length=20)
    city  = models.CharField(max_length=50, default="NA")


    class Meta:
        db_table = 'locationMaster'


class AdminMaster(models.Model):
    code = models.BigAutoField(primary_key=True)
    address = models.CharField(max_length=100,null=True)
    pincode = models.ForeignKey(locationMaster, on_delete=models.CASCADE,null=True)
    admin = models.CharField(max_length=30)
    admin_mobile = models.BigIntegerField(unique=True)
    admin_phone = models.CharField(max_length=12,null=True)
    admin_email = models.EmailField(unique=True)
    rly = models.ForeignKey(railwayLocationMaster, on_delete=models.CASCADE)
    status = models.CharField(max_length=10)
    created_on=models.DateTimeField(auto_now_add=True,null=True)
    emp_name=models.CharField(max_length=150,null=True)
    designation=models.CharField(max_length=300,null=True)
    user_id=models.ImageField(max_length=10,null=True)


    def str(self):
        return self.admin_email

    class Meta:
        db_table = 'AdminMaster'


class HRMS(models.Model):
    ipas_employee_id=models.CharField(max_length=15,null=False)    
    hrms_employee_id=models.CharField(primary_key=True,max_length=6,null=False)
    employee_first_name=models.CharField(max_length=150,null=True)
    employee_middle_name=models.CharField(max_length=150,null=True)
    employee_last_name=models.CharField(max_length=150,null=True)
    date_of_birth=models.DateField(null=True)
    appointment_date=models.DateField(null=True)
    superannuation_date=models.DateField(null=True)    
    gender=models.CharField(max_length=1,null=True)
    community_sr=models.CharField(max_length=3,null=True)
    service_status=models.CharField(max_length=50,null=True)
    billunit=models.CharField(max_length=7,null=True)
    railway_group=models.CharField(max_length=1,null=True)
    current_zone=models.CharField(max_length=10,null=True)
    current_unit_division=models.CharField(max_length=80,null=True)
    rltype=models.CharField(max_length=20,null=True)
    current_place=models.CharField(max_length=100,null=True)
    department=models.CharField(max_length=50,null=True)
    sub_department=models.CharField(max_length=50,null=True)
    designation=models.CharField(max_length=300,null=True) 
    paylevel=models.CharField(max_length=4,null=True)
    official_mobile_no=models.CharField(max_length=10,null=True)
    official_email_id=models.CharField(max_length=50,null=True)
    txn_timestamp=models.DateTimeField(null=True)


class station_master(models.Model):
    stnshortcode=models.CharField(primary_key=True,editable=False,unique=True,max_length=6)
    division_code = models.CharField(max_length=10,null=True)
    railway_code = models.CharField(max_length=10,null=True)    
    rly_id_id=models.ForeignKey('railwaylocationmaster',related_name= 'railwaylocation_master_railways_station_master',on_delete=models.CASCADE,null=True)
    div_id_id=models.ForeignKey('railwaylocationmaster',related_name= 'railwaylocation_master_division_station_master',on_delete=models.CASCADE,null=True)
    station_cat = models.CharField(max_length=10,null=True)
    station_cat_id = models.ForeignKey('stationcat_master', on_delete=models.CASCADE,null=True)
    lastmodified_by= models.CharField( max_length=20, blank=True, null=True)
    created_by=models.CharField( max_length=20, blank=True, null=True)
    station_name=models.CharField(max_length=100)
    created_on=models.DateTimeField(null=True, blank=True)
    lastmodified_on=models.DateTimeField(null=True, blank=True)
    delete_flag=models.BooleanField(default=False)


class stationcat_master(models.Model):
    stnid=models.AutoField(primary_key=True,editable=False,unique=True)
    stn_category=models.CharField(max_length=50)
    lastmodified_by=models.CharField( max_length=20, blank=True, null=True)
    created_by=models.CharField( max_length=20, blank=True, null=True)
    created_on=models.DateTimeField(null=True, blank=True)
    lastmodified_on=models.DateTimeField(null=True, blank=True)
    delete_flag=models.BooleanField(default=False)


class runningroom_master(models.Model):
    rrid=models.AutoField(primary_key=True)
    rr_name=models.CharField(max_length=50)
    rr_code=models.CharField(max_length=10, unique=True)
    stnshortcode=models.ForeignKey('station_master', on_delete=models.CASCADE, blank=True, null=True)    
    rly_id_id=models.ForeignKey('railwaylocationmaster',related_name= 'railwaylocation_master_railways_runningroom_master',on_delete=models.CASCADE,null=True)
    div_id_id=models.ForeignKey('railwaylocationmaster',related_name= 'railwaylocation_master_division_runningroom_master',on_delete=models.CASCADE,null=True)
    division_code = models.CharField(max_length=10,null=True)
    railway_code = models.CharField(max_length=10,null=True)
    created_by=models.CharField( max_length=20, blank=True, null=True)
    lastmodified_by=models.CharField( max_length=20, blank=True, null=True)
    created_on=models.DateTimeField(null=True, blank=True)
    lastmodified_on=models.DateTimeField(null=True, blank=True)
    delete_flag=models.BooleanField(default=False)

class traincat_master(models.Model):
    tcatid=models.AutoField(primary_key=True,editable=False,unique=True)
    tn_category=models.CharField(max_length=50)
    code=models.CharField(max_length=6, unique=True)
    created_by=models.CharField( max_length=20, blank=True, null=True)
    lastmodified_by=models.CharField( max_length=20, blank=True, null=True)
    created_on=models.DateTimeField(null=True, blank=True)
    lastmodified_on=models.DateTimeField(null=True, blank=True)
    delete_flag=models.BooleanField(default=False)


class train_master(models.Model):
    tnid=models.AutoField(primary_key=True, editable=False, unique=True)
    train_no=models.CharField(max_length=6,unique=True)
    train_name=models.CharField(max_length=50)
    tn_category=models.CharField(max_length=20,blank=False,null=True)    
    rly_id_id=models.ForeignKey('railwaylocationmaster',related_name= 'railwaylocation_master_railways_train_master',on_delete=models.CASCADE,null=True)
    div_id_id=models.ForeignKey('railwaylocationmaster',related_name= 'railwaylocation_master_division_train_master',on_delete=models.CASCADE,null=True)
    division_code = models.CharField(max_length=10,null=True)
    railway_code = models.CharField(max_length=10,null=True)
    # ForeignKey('traincat_master',on_delete=models.CASCADE,null=False)
    stnsource_code=models.ForeignKey('station_master',related_name='station_master_stnsource_code',on_delete=models.CASCADE,null=True)
    stndest_code=models.ForeignKey('station_master',related_name='station_master_stndest_code',on_delete=models.CASCADE,null=True)
    total_coach=models.IntegerField(max_length=2)
    created_by=models.CharField( max_length=20, blank=True, null=True)
    lastmodified_by=models.CharField( max_length=20, blank=True, null=True)
    created_on=models.DateTimeField(null=True, blank=True)
    lastmodified_on=models.DateTimeField(null=True, blank=True)
    delete_flag=models.BooleanField(default=False)
    trainowngrly2=models.ForeignKey('station_master',related_name='station_master_trainowngrly2', on_delete=models.CASCADE,null=True)
    primary_maint_depot = models.CharField(max_length=50,blank=False,null=True)    
    secondary_maint_depot = models.CharField(max_length=50,blank=False,null=True)    
    passing_division=models.CharField( max_length=100, blank=True, null=True)
    passing_rly=models.CharField( max_length=100, blank=True, null=True)

class inspectiontype_master(models.Model):
    instypeid=models.AutoField(primary_key=True, editable=False, unique=True)
    name=models.CharField(max_length=50, unique=False)    
    shortcode=models.CharField(max_length=10)
    sub_category = models.ForeignKey('sub_category_master', on_delete=models.CASCADE, null=True)
    entity=models.ForeignKey('einspect.dropdown_options', on_delete=models.CASCADE, null=True)
    concerned_dept = models.ForeignKey('departMast', on_delete=models.CASCADE, null=True)
    parent_id=models.CharField(max_length=10, unique=False)
    statuschecklist=models.IntegerField(max_length=1,blank=False,null=True)
    created_by=models.CharField( max_length=20, blank=True, null=True)
    lastmodified_by=models.CharField( max_length=20, blank=True, null=True)
    created_on=models.DateTimeField(null=True, blank=True, auto_now=True)
    lastmodified_on=models.DateTimeField(null=True, blank=True, auto_now=True)
    delete_flag=models.BooleanField(default=False)
    disable_flag=models.BooleanField(default=False)
    inspection_image=models.ImageField(null=True, blank=True,upload_to='images11/')
    version=models.IntegerField(default=1)
    desc = models.CharField( max_length=100, blank=True, null=True)  
    asset = models.ForeignKey('asset_master',on_delete=models.CASCADE, null=True)
    other_entity=models.CharField(max_length=50,null=True)


class section_master(models.Model):   
    secid = models.AutoField(primary_key=True,editable=False,unique=True)
    section_code=models.CharField(max_length=20,blank=False,null=True)
    section_name=models.CharField(max_length=100,blank=False,null=True)
    secstart_code = models.ForeignKey('station_master',related_name = 'station_master_secstart_code',on_delete=models.CASCADE,null=True)
    secend_code = models.ForeignKey('station_master',related_name = 'station_master_secend_code',on_delete=models.CASCADE,null=True)
    via =  models.CharField(max_length=100,null=True)
   # models.ForeignKey('station_master',related_name = 'station_master_via',on_delete=models.CASCADE,null=True)    
    rly_id_id=models.ForeignKey('railwaylocationmaster',related_name= 'railwaylocation_master_railways_section_master',on_delete=models.CASCADE,null=True)
    div_id_id=models.ForeignKey('railwaylocationmaster',related_name= 'railwaylocation_master_division_section_master',on_delete=models.CASCADE,null=True)
    division_code = models.CharField(max_length=10,null=True)
    railway_code = models.CharField(max_length=10,null=True)
    route = models.CharField(max_length=500,null=True)
    section_length=models.DecimalField(max_digits=6,decimal_places=2,null=True)
    # startkm = models.IntegerField(max_length=5)
    # endkm = models.IntegerField(max_length=5)
    created_by=models.CharField( max_length=20, blank=True, null=True)
    lastmodified_by=models.CharField( max_length=20, blank=True, null=True)
    created_on=models.DateTimeField(null=True, blank=True)
    lastmodified_on=models.DateTimeField(null=True, blank=True)
    delete_flag=models.BooleanField(default=False)

class Level_Desig_temp(models.Model):
    designation_code=models.AutoField(primary_key=True)  
    # cat_id=models.IntegerField(null=True)    
    designation=models.CharField(max_length=100,null=True)  
    department=models.CharField(max_length=50,null=True)   
    effectdate=models.DateTimeField(null=True, blank=True)
    # un_officer_id=models.IntegerField(null=True)
    # level=models.CharField(max_length=2,null=True)
    # designation_code = models.CharField(max_length=15,null=True)
    parent_desig_code= models.CharField(max_length=15,null=True)
    department_code=models.CharField(max_length=15,null=True)
    # ForeignKey('departMast', on_delete=models.CASCADE, null=True)
    rly_unit=models.CharField(max_length=15,null=True)
    # ForeignKey('railwayLocationMaster', on_delete=models.CASCADE, null=True)
    pc7_levelmin = models.IntegerField(null=True, blank=True)
    pc7_levelmax = models.IntegerField(null=True, blank=True)
    modified_by = models.CharField( max_length=20, blank=True, null=True)
    desig_user = models.CharField(max_length=15,null=True)
    # ForeignKey('inspects.MyUser', on_delete=models.CASCADE, null=True)
    status= models.CharField( max_length=2, blank=True, null=True)
    empno=models.CharField(max_length=15,null=True)
    # ForeignKey('inspects.empmast', on_delete=models.CASCADE, blank=True, null=True)
    d_level=models.CharField( max_length=4, blank=True, null=True)

class Level_Desig_temp1(models.Model):
    designation_code=models.AutoField(primary_key=True)  
    # cat_id=models.IntegerField(null=True)    
    designation=models.CharField(max_length=100,null=True)  
    department=models.CharField(max_length=50,null=True)   
    effectdate=models.DateTimeField(null=True, blank=True)
    # un_officer_id=models.IntegerField(null=True)
    # level=models.CharField(max_length=2,null=True)
    # designation_code = models.CharField(max_length=15,null=True)
    parent_desig_code= models.CharField(max_length=15,null=True)
    department_code=models.IntegerField(null=True)
    # ForeignKey('departMast', on_delete=models.CASCADE, null=True)
    rly_unit=models.IntegerField(null=True)
    # ForeignKey('railwayLocationMaster', on_delete=models.CASCADE, null=True)
    pc7_levelmin = models.IntegerField(null=True, blank=True)
    pc7_levelmax = models.IntegerField(null=True, blank=True)
    modified_by = models.CharField( max_length=20, blank=True, null=True)
    #desig_user = models.ForeignKey('inspects.MyUser', on_delete=models.CASCADE, null=True)
    desig_user=models.IntegerField(null=True)
    status= models.CharField( max_length=2, blank=True, null=True)
    #empno=models.ForeignKey('inspects.empmast', on_delete=models.CASCADE, blank=True, null=True)
    empno= models.CharField( max_length=50, blank=True, null=True)
    d_level=models.CharField( max_length=4, blank=True, null=True)
    contactnumber=models.CharField(max_length=10, blank=True, null=True)
    official_email_ID=models.CharField(max_length=50, blank=True, null=True, unique=True)

class loco_master(models.Model):
    loco_id = models.AutoField( primary_key=True) 
    loco_cat = models.CharField(max_length=15, null=True)
    loco_no = models.CharField(max_length=8, null=True)
    mfg_name = models.CharField(max_length=10, null=True)
    mfg_full_name = models.CharField(max_length=100, null=True)
    loco_type = models.CharField(max_length=20, null=True)
    loco_shed = models.CharField(max_length=10, null=True)       
    rly_id_id=models.ForeignKey('railwaylocationmaster',related_name= 'railwaylocation_master_railways_loco_master',on_delete=models.CASCADE,null=True)
    div_id_id=models.ForeignKey('railwaylocationmaster',related_name= 'railwaylocation_master_division_loco_master',on_delete=models.CASCADE,null=True)
    division_code = models.CharField(max_length=10, null=True)
    railway_code = models.CharField(max_length=10, null=True)
    gauge = models.CharField(max_length=2, null=True)
    wheel_arr = models.CharField(max_length=10, null=True)
    qty_built = models.IntegerField( null=True)
    built_year = models.CharField(max_length=8, null=True)
    turned_out_date = models.DateField(null=True)
    shed_in_date = models.DateField(null=True)
    doc_in_date = models.DateField(null=True)
    power = models.CharField(max_length=10, null=True)
    running_status = models.CharField(max_length=15, null=True)
    Loco_description = models.CharField(max_length=30, null=True)
    Loco_remarks = models.CharField(max_length=100, null=True)
    max_capacity = models.CharField(max_length=100, null=True)
    max_speed = models.IntegerField(null=True)
    created_by = models.CharField(max_length=20, null=True)
    lastmodified_by = models.CharField(max_length=20, null=True)
    created_on = models.DateTimeField(null=True, blank=True)
    lastmodified_on = models.DateTimeField(null=True, blank=True)
    delete_flag = models.BooleanField(default=False)

#WAGON MASTER FOR E-DRISHTI
class wagon_master(models.Model):
    wagon_type = models.CharField(max_length=50, null=True)
    wagon_no = models.BigIntegerField( null=True)
    owner_id = models.CharField(max_length=40, null=True)
    category = models.CharField(max_length=40, null=True)
    dm_date = models.DateField(null=True, blank=True)
    ic_date = models.DateField(null=True, blank=True)
    manufacture_id = models.CharField(max_length=40, null=True)
    manufacture_date = models.DateField(null=True, blank=True)
    receiving_time = models.DateTimeField(null=True, blank=True)

class posting_History(models.Model):
    history_id = models.AutoField(primary_key=True)  
    empno = models.ForeignKey('inspects.empmast', on_delete=models.CASCADE, blank=True, null=True)
    done_by = models.CharField(max_length=25,null=True) 
    forwarded_to = models.CharField(max_length=25,null=True) 
    prev_desigination =models.CharField(max_length=100,null=True)  
    prev_parent_desig_code = models.CharField(max_length=15,null=True)
    prev_department_code =models.ForeignKey('departMast', on_delete=models.CASCADE, null=True, related_name='posting_History_prev_department_code')
    prev_rly_unit = models.ForeignKey('railwayLocationMaster', on_delete=models.CASCADE, null=True, related_name='posting_History_prev_rly_unit')
    prev_contactnumber =models.CharField(max_length=10, blank=True, null=True)
    prev_official_email_ID =models.CharField(max_length=50, blank=True, null=True)
    prev_station_name = models.CharField(max_length=100,null=True)
    current_desigination =models.CharField(max_length=100,null=True)  
    current_parent_desig_code = models.CharField(max_length=15,null=True)
    current_department_code =models.ForeignKey('departMast', on_delete=models.CASCADE, null=True, related_name='posting_History_current_department_code')
    current_rly_unit =models.ForeignKey('railwayLocationMaster', on_delete=models.CASCADE, null=True, related_name='posting_History_current_rly_unit')
    current_contactnumber =models.CharField(max_length=10, blank=True, null=True)
    current_official_email_ID =models.CharField(max_length=50, blank=True, null=True)
    current_station_name = models.CharField(max_length=100,null=True)
    charge_type = models.CharField(max_length=1, null=True)
    created_date = models.DateTimeField(null=True)
    accepted_date = models.DateTimeField(null=True)
    status = models.CharField(max_length=10, default='Forwarded') # Forwarded, Acceted, Rejected
    created_remarks = models.CharField(max_length=100, blank=True, null=True)
    accepted_remarks = models.CharField(max_length=100, blank=True, null=True)

class designation_Change_Request(models.Model):
    record_id = models.AutoField(primary_key=True) 
    request_by = models.CharField(max_length=25,null=True) 
    request_date = models.DateTimeField(null=True)
    request_remarks = models.CharField(max_length=100, blank=True, null=True)
    desigination =models.CharField(max_length=100,null=True)  
    
    prev_parent_desig_code = models.CharField(max_length=15,null=True)
    prev_department_code =models.ForeignKey('departMast', on_delete=models.CASCADE, null=True, related_name='designation_Change_Request_prev_department_code')
    prev_rly_unit = models.ForeignKey('railwayLocationMaster', on_delete=models.CASCADE, null=True, related_name='designation_Change_Request_prev_rly_unit')
    prev_contactnumber =models.CharField(max_length=10, blank=True, null=True)
    prev_official_email_ID =models.CharField(max_length=50, blank=True, null=True)
    prev_station_name = models.CharField(max_length=100,null=True)
    prev_maxlevel = models.IntegerField(null=True, blank=True)
    prev_minlevel = models.IntegerField(null=True, blank=True)
 
    current_parent_desig_code = models.CharField(max_length=15,null=True)
    current_department_code =models.ForeignKey('departMast', on_delete=models.CASCADE, null=True, related_name='designation_Change_Request_curr_department_code')
    current_rly_unit =models.ForeignKey('railwayLocationMaster', on_delete=models.CASCADE, null=True, related_name='designation_Change_Request_curr_rly_unit')
    current_contactnumber =models.CharField(max_length=10, blank=True, null=True)
    current_official_email_ID =models.CharField(max_length=50, blank=True, null=True)
    current_station_name = models.CharField(max_length=100,null=True)
    current_maxlevel = models.IntegerField(null=True, blank=True)
    current_minlevel = models.IntegerField(null=True, blank=True)
    
    action_by = models.CharField(max_length=25,null=True) 
    action_date = models.DateTimeField(null=True)
    action_remarks = models.CharField(max_length=100, blank=True, null=True)
    
    status = models.CharField(max_length=12, default='Forwarded') # Forwarded, Acceted, Rejected, Pulled Back
    request_type = models.CharField(max_length=12, null=True,default='Modification') # Modification , New
     
class iem_hospmstr(models.Model):
    iaihccid  = models.AutoField(primary_key=True)
    iavhcccode = models.CharField(max_length=8, blank=True, null=True)
    iavhccfullname = models.CharField(max_length=100, blank=True, null=True)
    iavhccshrtname = models.CharField(max_length=30, blank=True, null=True)
    iavhccdk = models.CharField(max_length=8, blank=True, null=True)
    iavhccsttncode = models.CharField(max_length=4, blank=True, null=True)
    iavhcctype = models.CharField(max_length=4, blank=True, null=True)
    iavhccdvsncode = models.CharField(max_length=10, blank=True, null=True)
    iavhcczonecode = models.CharField(max_length=4, blank=True, null=True)
    iavworkshopcode = models.CharField(max_length=8, blank=True, null=True)
    iairlyunitcode = models.IntegerField( null=True)
    iaidivunitcode = models.IntegerField( null=True)
    iavcrtdby = models.CharField(max_length=50, blank=True, null=True)
    iavmdfdby = models.CharField(max_length=50, blank=True, null=True)
    iatcrtdon =models.DateTimeField(null=True)
    iatmdfdon =models.DateTimeField(null=True)
    iavstate = models.CharField(max_length=20, blank=True, null=True)
    iavdist = models.CharField(max_length=30, blank=True, null=True)
    iavcntry = models.CharField(max_length=30, blank=True, null=True)
    iavpincode= models.CharField(max_length=6, blank=True, null=True)
   
class sub_category_master(models.Model):
    sub_id=models.AutoField(primary_key=True, editable=False, unique=True)
    sub_category=models.CharField(max_length=100,null=True)
    disable_flag=models.BooleanField(default=False)

class question_sub_category_master(models.Model):
    sub_id=models.AutoField(primary_key=True, editable=False, unique=True)
    sub_category=models.CharField(max_length=20,null=True)
    disable_flag=models.BooleanField(default=False)

class iem_tranprofmstr(models.Model):
    id =models.AutoField(primary_key=True)
    iaitranid = models.IntegerField( null=True)
    iavtranowngrly = models.CharField(max_length=4, blank=True, null=True)
    iavtrannumb = models.CharField(max_length=10, blank=True, null=True)
    iavtranname = models.CharField(max_length=25, blank=True, null=True)
    mavtrantype = models.CharField(max_length=4, blank=True, null=True)
    iavtranstyp = models.CharField(max_length=4, blank=True, null=True)
    iadvaldfrom =models.DateTimeField(null=True)
    iadvaldto =models.DateTimeField(null=True)
    iavdaysofsrvc = models.CharField(max_length=13, blank=True, null=True)
    iavorgn = models.CharField(max_length=7, blank=True, null=True)
    iavdstn = models.CharField(max_length=7, blank=True, null=True)
    iaideptime = models.IntegerField( null=True)
    iaiarvltime = models.IntegerField( null=True)
    iacgaug = models.CharField(max_length=1, blank=True, null=True)
    iacuknwvldty = models.CharField(max_length=1, blank=True, null=True)
    iacirctcflag = models.CharField(max_length=1, blank=True, null=True)
    iavsrcstt = models.CharField(max_length=4, blank=True, null=True)
    iavdstnstt = models.CharField(max_length=10, blank=True, null=True)
    iairsrvflag = models.IntegerField( null=True)
    iavhdayctgy = models.CharField(max_length=4, blank=True, null=True)
    iavresncode = models.CharField(max_length=8, blank=True, null=True)
    iacsrctrcn = models.CharField(max_length=1, blank=True, null=True)
    iacsliptranflag = models.CharField(max_length=1, blank=True, null=True)
    iacsliptype = models.CharField(max_length=1, blank=True, null=True)
    iainrmlload = models.IntegerField( null=True)
    iaimaxload = models.IntegerField( null=True)
    iaiintlflag = models.IntegerField( null=True)
    iaiftrbokgflag = models.IntegerField( null=True)
    iavmaintrannumb = models.CharField(max_length=10, blank=True, null=True)
    iavsliptrannumb = models.CharField(max_length=10, blank=True, null=True)
    iainewtrannumb = models.CharField(max_length=10, blank=True, null=True)
    iavnewtranname = models.CharField(max_length=30, blank=True, null=True)

class iem_transch(models.Model):
    id = models.AutoField(primary_key=True)
    iaitranid = models.IntegerField( null=True)
    iavtrannumb = models.CharField(max_length=6, blank=True, null=True)
    iaisqncnumb = models.IntegerField( null=True)
    iavzonecode = models.CharField(max_length=4, blank=True, null=True)
    iavdvsncode = models.CharField(max_length=4, blank=True, null=True)
    iavsttncode = models.CharField(max_length=4, blank=True, null=True)
    iacclsflag = models.CharField(max_length=1, blank=True, null=True)
    iaiwttarvl = models.IntegerField( null=True)
    iaiwttdprt = models.IntegerField( null=True)
    iachaltflag = models.CharField(max_length=1, blank=True, null=True)
    iaiwttdayofrun = models.IntegerField( null=True)
    iaipttdprt = models.IntegerField( null=True)
    iaipttarvl = models.IntegerField( null=True)
    iairuntime = models.IntegerField( null=True)
    iaiacctime = models.IntegerField( null=True)
    iaidectime = models.IntegerField( null=True)
    iaitrfcalwc = models.IntegerField( null=True)
    iaienggalwc = models.IntegerField( null=True)
    iaicstrtime = models.IntegerField( null=True)
    iavcstrresn = models.CharField(max_length=64, blank=True, null=True)
    iacxingflag = models.CharField(max_length=1, blank=True, null=True)
    iavxingtran = models.CharField(max_length=30, blank=True, null=True)
    iavxingtime = models.CharField(max_length=20, blank=True, null=True)
    iaiintrdist = models.FloatField( null=True)
    iavpltfnumb = models.CharField(max_length=80, blank=True, null=True)
    iaccrewchng = models.CharField(max_length=1, blank=True, null=True)
    iaclocochng = models.CharField(max_length=1, blank=True, null=True)
    iacrvslsttn = models.CharField(max_length=1, blank=True, null=True)
    iavtrcncode = models.CharField(max_length=20, blank=True, null=True)
    iavcrewchngcode = models.CharField(max_length=20, blank=True, null=True)
    iacgarbg = models.CharField(max_length=1, blank=True, null=True)
    iacwater = models.CharField(max_length=1, blank=True, null=True)


class trainMaster(models.Model):
    tnid=models.AutoField(primary_key=True, editable=False, unique=True)
    trainid=models.IntegerField( null=True)
    train_no=models.CharField(max_length=5,blank=True, null=True)
    train_name=models.CharField(max_length=25, blank=True, null=True)  
    org_rly_id=models.ForeignKey('railwayLocationMaster',related_name= 'railwaylocation_master_railwaystrainMaster',on_delete=models.CASCADE,null=True)
    org_railway_code = models.CharField(max_length=4, blank=True, null=True)
    created_on=models.DateTimeField(null=True, blank=True)
    lastmodified_on=models.DateTimeField(null=True, blank=True)
    delete_flag=models.BooleanField(default=False)
    passing_division=models.CharField( max_length=300, blank=True, null=True)
    passing_rly=models.CharField( max_length=300, blank=True, null=True)


#############  new used in phase2

class coach_master(models.Model):
    id = models.AutoField(primary_key=True) 
    coach_no = models.CharField(max_length=8,null=True) 
    coach_id = models.IntegerField(null=True)
    coach_type = models.CharField(max_length=15, blank=True, null=True)
    coach_owning_rly =models.CharField(max_length=4,null=True) 
    coach_owning_div = models.CharField(max_length=4,null=True) 
    base_depot = models.CharField(max_length=10,null=True) 
    nominated_workshop = models.CharField(max_length=10, blank=True, null=True)
    coach_category =models.CharField(max_length=20,null=True) 
    max_speed = models.IntegerField(null=True)
    manufacturer =models.CharField(max_length=15,null=True)


class Feedback_Report(models.Model):
    category=models.CharField(max_length=40,blank=False,null=True)
    sub_category=models.CharField(max_length=40,blank=False,null=True)
    feedback_type=models.CharField(max_length=40,blank=False,null=True)
    description=models.TextField(blank=False,null=True) 
    reported_date = models.DateTimeField(auto_now=True,blank=False,null=True)
    cris_remarks_date = models.DateTimeField(blank=False,null=True)
    cris_remarks = models.TextField(blank=False,null=True) 
    status = models.IntegerField(max_length=20,default = 0)
    images = models.ImageField(null=True, blank=True,upload_to='feedback_images/')
    level_desig = models.ForeignKey(Level_Desig,on_delete=models.CASCADE)
    cris_image = models.ImageField(null=True, blank=True,upload_to='cris_images/')
    # 0 : pending, 1 : Resolved, 2 : In Progress, 3 : Not Feasible



###  Actor Models
class actor_details(models.Model):
    actorId = models.AutoField(primary_key=True)
    actorName = models.CharField(max_length=20)
    tableName = models.CharField(max_length=30)
    colName = models.CharField(max_length=50)
    filterName = models.CharField(max_length=20,null=True) # only one fiter column
    filterValue = models.CharField(max_length=20,null=True)
    viewName = models.CharField(max_length=20,null=True) # only one fiter column
    viewColumn = models.CharField(max_length=100,null=True)# 5 fiter column
    viewFilter = models.CharField(max_length=20,null=True)
    color_code = models.CharField(max_length=10,null=True)
    viewactorName = models.CharField(max_length=50,null=True)



class actor_with_inspType(models.Model):
    slno = models.AutoField(primary_key=True)
    actorId = models.ForeignKey('actor_details', on_delete=models.CASCADE, null=True)
    inspType = models.ForeignKey('inspectiontype_master', on_delete=models.CASCADE, null=True)
    created_by=models.CharField( max_length=20, blank=True, null=True)
    lastmodified_by=models.CharField( max_length=20, blank=True, null=True)
    created_on=models.DateTimeField(null=True, blank=True, auto_now=True)
    lastmodified_on=models.DateTimeField(null=True, blank=True, auto_now=True)
    delete_flag=models.BooleanField(default=False)
    disable_flag=models.BooleanField(default=False)


class asset_master(models.Model):
    asset_id=models.AutoField(primary_key=True, editable=False, unique=True)
    asset_category=models.CharField(max_length=20,null=True)
    disable_flag=models.BooleanField(default=False)


class iem_crewmstr(models.Model):
    id=models.AutoField(primary_key=True, editable=False, unique=True)
    iachqcode = models.CharField(max_length = 4,null=True,blank = True)
    iavcrewid = models.CharField(max_length = 8,null=True,blank = True)
    iavname = models.CharField(max_length = 60,null=True,blank = True) 
    iavoff = models.CharField(max_length = 25,null=True,blank = True)  
    iavcrewdesg = models.CharField(max_length = 25,null=True,blank = True) 
    iabmoblnumb =models.BigIntegerField(max_length = 4,null=True,blank = True) 
    iavcrewtype = models.CharField(max_length = 4,null=True,blank = True)  
    iadapntdate = models.DateField(null=True,blank = True) 
    iacvisn = models.CharField(max_length = 4,null=True,blank = True)  
    iacalch = models.CharField(max_length = 1,null=True,blank = True)  
    iavinacstts = models.CharField(max_length = 10,null=True,blank = True) 
    iavtrctn = models.CharField(max_length = 50,null=True,blank = True)  
    iavliid = models.CharField(max_length = 10,null=True,blank = True)  
    iaclrdue = models.CharField(max_length = 1,null=True,blank = True)  
    iaccoch = models.CharField(max_length = 2,null=True,blank = True)  
    iavorgtype = models.CharField(max_length = 4,null=True,blank = True)  
    iadinitmed = models.DateField(null=True,blank = True) 
    iavempnumb = models.CharField(max_length = 30,null=True,blank = True)  
    iavcrewbaseid =models.CharField(max_length = 8,null=True,blank = True)
    rly_id_id=models.ForeignKey('railwaylocationmaster',related_name= 'railwaylocation_master_railways_crew_master',on_delete=models.CASCADE,null=True)
    div_id_id=models.ForeignKey('railwaylocationmaster',related_name= 'railwaylocation_master_division_crew_master',on_delete=models.CASCADE,null=True)
    division_code = models.CharField(max_length=10,null=True)
    railway_code = models.CharField(max_length=10,null=True)

class rlyhead(models.Model):
#   location_code, location_description, location_type, d_level
    # rly_code=models.ForeignKey('railwayLocationMaster', on_delete=models.CASCADE, null=True)
    rllongdesc = models.CharField(max_length=30,null=True)
    rlshortcode= models.CharField(max_length=100,null=True)
    rltype = models.CharField(max_length=5,null=True)
    head_dlevel =  models.CharField(max_length=100,null=True)

class category(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField( max_length=10, blank=True, null=True)
    user_role = models.CharField(max_length=20, null=True) 
    hierarchy_level = models.IntegerField(null=True)


class user_preference_master(models.Model):
    id = models.AutoField(primary_key=True)
    parent_id = models.CharField( max_length=5,null=True)
    delete_flag=models.BooleanField(default=False)
    value = models.CharField( max_length=30,null=True)
    url = models.CharField( max_length=150,null=True)
    lastmodified = models.DateTimeField(null=True) 

class user_preferences(models.Model):
    id = models.AutoField(primary_key=True)
    myuser_id = models.ForeignKey('inspects.MyUser', on_delete=models.CASCADE, null=True)
    delete_flag=models.BooleanField(default=False)
    for_id = models.ForeignKey('user_preference_master', on_delete=models.CASCADE, null=True, related_name = 'preference_for') 
    value_id = models.ForeignKey('user_preference_master', on_delete=models.CASCADE, null=True, related_name = 'preference_value')
    lastmodified = models.DateTimeField(null=True) 


class pendency_dashboard_like_crb(models.Model):
    code=models.AutoField(primary_key=True)  
    delete_flag=models.BooleanField(default=False)    
    designation=models.CharField(max_length=100,null=True) 




class empmast_nonrly(models.Model):
    ref_no = models.CharField(max_length=15,primary_key=True)
    id = models.IntegerField()
    empno=models.CharField(max_length=20)
    orderid=models.CharField(max_length=20,null=True,blank=True)
    empname=models.CharField(max_length=50)
    empmname=models.CharField(max_length=50,null=True, blank=True)
    emplname=models.CharField(max_length=50,null=True, blank=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    contactno = models.CharField(max_length=10, blank=True, null=True)
    railwaygroup = models.CharField(max_length=1, blank=True, null=True)
    pc7_level=models.CharField(max_length=2,null=True)
    service_status=models.CharField(max_length=30,default='DEPUTATION OUTSIDE')
    designation=models.CharField(max_length=50,null=True)
    desig_longdesc=models.CharField(max_length=300,null=True)
    station_des=models.CharField(max_length=100,null=True)
    dept_desc=models.CharField(max_length=50,null=True)
    currentzone = models.CharField(max_length=50, blank=True, null=True)
    currentunitdivision = models.CharField(max_length=100, blank=True, null=True)
    rl_type = models.CharField(max_length=50, blank=True, null=True)
    rly_id=models.ForeignKey('myadmin.railwayLocationMaster', on_delete=models.CASCADE, null=True,related_name='empmast_nonrly_rly_id')
    profile_modified_by = models.CharField( max_length=20, blank=True, null=True,default='self')
    profile_modified_on=models.DateField(null=True,blank=True)  
    status = models.CharField(max_length = 1, default = '1')   # 1 - Data Saved by User , 2 - Rejected by admin , 4 - accepted by admin
    profile_accepted_by = models.CharField( max_length=20, blank=True, null=True)
    profile_accepted_on=models.DateField(null=True,blank=True)  
    remarks = models.CharField(max_length = 300, null=True,blank=True)
    link_designation_id =  models.ForeignKey(Level_Desig,on_delete=models.DO_NOTHING, null= True)
    link_designation =  models.CharField(max_length=100,null=True)  

class customized_panel(models.Model):
    panel_id=models.AutoField(primary_key=True)  
    panel_of=models.ForeignKey(Level_Desig,on_delete=models.CASCADE,related_name="panel_of")
    panel_member=models.ForeignKey(Level_Desig,on_delete=models.CASCADE,related_name="panel_member")
    delete_flag=models.BooleanField(default=False)
    modified_on=models.DateTimeField(auto_now=True,null=True,blank=True)
    created_on=models.DateTimeField(auto_now_add=True,null=True,blank=True)

    
class mdms_coach_master(models.Model):
    id=models.AutoField(primary_key=True)  
    coach_number =  models.CharField(max_length=20,null=True)  
    coach_id = models.IntegerField(null=False)
    owning_rly =  models.CharField(max_length=10,null=True)  
    owning_div =  models.CharField(max_length=10,null=True)  
    owning_depot =  models.CharField(max_length=10,null=True)  
    rfid_tag =  models.CharField(max_length=1,null=True)  
    coach_status =  models.CharField(max_length=30,null=True)  
    coach_gauge =  models.CharField(max_length=10,null=True)  
    tare_weight = models.DecimalField(max_digits=8, decimal_places=3)
    max_speed = models.DecimalField(max_digits=3, decimal_places=0)
    fitness_type =  models.CharField(max_length=10,null=True)  
    bio_toilet_fitted =  models.CharField(max_length=5,null=True)  
    coupling_type =  models.CharField(max_length=10,null=True)  
    manufacturer =  models.CharField(max_length=15,null=True)  
    built_date =  models.CharField(max_length=10,null=True)  
    commissioning_date =  models.CharField(max_length=10,null=True)  
    condemnation_date =  models.CharField(max_length=10,null=True)  
    seat_layout_variant_no =  models.CharField(max_length=20,null=True)  
    coach_type =  models.CharField(max_length=20,null=True)  
    coach_ac_flag =  models.CharField(max_length=1,null=True)  
    coach_category =  models.CharField(max_length=10,null=True)  
    factory_turnout_date =  models.CharField(max_length=10,null=True)  
    power_generation_type =  models.CharField(max_length=12,null=True)  
    nominated_workshop =  models.CharField(max_length=10,null=True)  
    temporary_unavailable =  models.CharField(max_length=1,null=True)  
    
class FeedBack_data(models.Model):
    inspection_accuracy = models.IntegerField(null=True, verbose_name="Accuracy of Inspection Data")
    ui_design = models.IntegerField(null=True, verbose_name="UI Design of the Application")
    performance_speed = models.IntegerField(null=True, verbose_name="Performance Speed")
    application_smoothness = models.IntegerField(null=True, verbose_name="Application Smoothness")

    dashboard = models.IntegerField(null=True, verbose_name="Dashboard")
    my_inspection = models.IntegerField(null=True, verbose_name="My Inspection")
    compliance_marked = models.IntegerField(null=True, verbose_name="Compliances (Marked to Me)")
    # forwarded_compliance = models.IntegerField(null=True, verbose_name="Forwarded Compliance")
    # help = models.IntegerField(null=True, verbose_name="Help")
    mom = models.IntegerField(null=True, verbose_name="Minutes of Meeting")
    search = models.IntegerField(null=True, verbose_name="Search")
    # tour_programme = models.IntegerField(null=True, verbose_name="Tour Programme")
    copy_to = models.IntegerField(null=True, verbose_name="COPY TO")
    # task_tracker = models.IntegerField(null=True, verbose_name="Task Tracker")
    reports = models.IntegerField(null=True, verbose_name="Reports")

    suggestions = models.CharField(max_length=1000, null=True, verbose_name="Suggestions for Improvement")
    overall_experience = models.IntegerField(null=True, verbose_name="Overall Experience")
    
    Designation = models.CharField(max_length=200, null=True)
    design_code = models.ForeignKey('myadmin.Level_Desig',on_delete=models.CASCADE)
    reported_date = models.DateTimeField(auto_now=True,blank=False,null=True)
    