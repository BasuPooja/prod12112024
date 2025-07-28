from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.views.generic import View
from myadmin.models import *
from myadmin.views import*
from django.contrib import auth
from datetime import datetime
import datetime
from myadmin import models 
from inspects import models as m1
# from django.shortcuts import render,redirect,render_to_response
from django.contrib.auth.models import User,auth
from collections import defaultdict 
import json
import requests
import mimetypes
from tkinter import * 
from django.db.models import Max 
from tkinter import messagebox 
from django.db.models import Q
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.db.models.functions import Substr
from django.db.models import Subquery,Sum,Count
import re,uuid,copy
from copy import deepcopy
from django.db.models import Sum,Subquery
from django.utils import formats
from django.utils.dateformat import DateFormat
from decimal import *
from django.db import connection
cursor = connection.cursor()
from django.core.mail import EmailMessage
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mass_mail
import math
import shutil
nav=defaultdict()
subnav=defaultdict()
usermaster=defaultdict()
rolelist = []
navmenu=[] 
user = get_user_model()
from datetime import datetime,date
# Create your views here.

def filter(request):
    try:
        if request.method == "GET":
            rlycode=request.GET.get('rlycode')
            # print(rlycode,'rlycode')
            rlytype=request.GET.get('rlytype')
            # print(rlytype,'rlytype')
            parentrlycode=request.GET.get('parentrlycode')
            # print(parentrlycode,'parentrlycode')
            station1=request.GET.get('station1')
            # print(station1,'station1')
            dict2={}
            dict1 = {"location_code":rlycode,  "location_type":rlytype,"parent_location_code":parentrlycode,"station_code":station1}
            for key,val in dict1.items():
                # print(key, val)
                if val!='':
                    dict2[key] =val
                    
            # print(dict2,"dict2")        
            # print(len(dict2))
            data = []  
            a= len(dict2)
            
            for i in dict2.items():
                for k,v in dict2.items():
                    # print(k)
                    data2={k:v}
                    data1=list(railwayLocationMaster.objects.filter(**data2).values())
                    for j in data1:
                        if j not in data:
                            data.append(j)

                    # print(data1)
            
            return JsonResponse({'data':data},safe=False)
        return JsonResponse({"success":False},status=400)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="filter",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})


def fetch_details(request):
    try:
        empno=request.GET.get('empno')
        # print(empno)
        if(HRMS.objects.filter(empno=empno).exists()):
            # designation_id=m1.HRMS.objects.filter(empno=emp_id)[0].designation_id
            # designation=models.Designation_Master.objects.filter(designation_master_no=designation_id)[0].designation
            name=HRMS.objects.filter(empno=empno)[0].employee_first_name
            # empname=m1.HRMS.objects.filter(empno=emp_id)[0].empname
            # rly_id=m1.HRMS.objects.filter(empno=emp_id)[0].rly_id_id
            # div_id=m1.HRMS.objects.filter(empno=emp_id)[0].div_id_id
            # email_idd=m1.HRMS.objects.filter(empno=emp_id)[0].email
            # # print(rly_id,'___________')
            # # print(div_id,'___________')
            # # print(name,'first name')
            # desigg=models.Level_Desig.objects.filter(designation_code=designation)[0].designation
            # rly_code=models.railwayLocationMaster.objects.filter(rly_unit_code=rly_id)[0].location_code
            # if div_id!=None:
            #     div_code=models.railwayLocationMaster.objects.filter(rly_unit_code=div_id)[0].location_code
            # else:
            #     div_code=''
            context={
                'name':str(name),
                # 'empname':str(empname),
                # 'rly_code':str(rly_code),
                # 'div_code':str(div_code),
                # 'desigg':str(desigg),
                # 'email_idd':str(email_idd),
            }
            return JsonResponse(context)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="fetch_details",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})



def railwayMaster(request):
    try:
        station = station_master.objects.values('stnshortcode','station_name').distinct()
        # print(station)
        datatable=list(models.railwayLocationMaster.objects.filter(deleted_flag = False).values())
        # parent=list(railwayLocationMaster.objects.filter(location_type_desc=).values('parent_location_code').distinct())
        context={
            'station':station,
            'datatable':datatable,
            # 'parent':parent,
        }
        return render(request,'railwayMaster.html',context)   
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="railwayMaster",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})

def employeeList(request):
    try:
        current_user = request.user.user_role
        # print(current_user)
        if request.user.user_role == 'admin_super':
            employees=m1.empmast.objects.all().order_by('empname')
        elif request.user.user_role == 'admin_rly' or request.user.user_role == 'admin_div':
            rlyid = AdminMaster.objects.filter(user_id = request.user.username).values('rly_id')
            employees = m1.empmast.objects.filter(rly_id__in =rlyid).values().order_by('empname')
            
        emp=m1.empmast.objects.all() 
         
        rail=railwayLocationMaster.objects.filter(location_type='ZR').values('location_code')
        division=list(railwayLocationMaster.objects.filter(location_type='DIV').values('location_code').distinct('location_code'))
        
        # category = m1.empmast.objects.filter(decode_paycategory__isnull=False).values('decode_paycategory').distinct()
        department=departMast.objects.filter(delete_flag=False).values('department_name').order_by('department_name').distinct()
        designation=Level_Desig.objects.values('designation').order_by('designation').distinct()
        
        context={
            'emp':emp,
            'department':department,
            'employees':employees,
            'sub':0,
            # 'category':category,
            'rail':rail,
            'user':usermaster,
            'division':division,
            'designation':designation,
            
        }
        return render(request, 'employeeList.html',context)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="employeeList",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})


# def filter_employee(request):
#     try:
#         if request.method == "GET":
#             Employee=request.GET.get('Employee')
#             # print(Employee,'Employee')
#             paylevel=request.GET.get('paylevel')
#             # print(paylevel,'paylevel')
#             Designation=request.GET.get('Designation')
#             # print(Designation,'Designation')
#             Department=request.GET.get('Department')
#             # print(Department,'Department')
#             dict2={}
#             dict1 = {"empno":Employee, "pc7_level":paylevel,"desig_longdesc":Designation,"dept_desc":Department}
#             for key,val in dict1.items():
#                 # print(key, val)
#                 if val!='':
#                     dict2[key] =val
                   
#             # print(dict2,"dict2")        
#             # print(len(dict2))
#             data = []  
#             a= len(dict2)
           
#             for i in dict2.items():
#                 for k,v in dict2.items():
#                     # print(k)
#                     data2={k:v}
#                     data1=list(m1.empmast.objects.filter(**data2).values())
#                     for j in data1:
#                         if j not in data:
#                             data.append(j)
 
#                     # print(data1)
           
#             return JsonResponse({'data':data},safe=False)
#         return JsonResponse({"success":False},status=400)
#     except Exception as e:
#         try:
#             m1.error_Table.objects.create(fun_name="filter_employee",user_id=request.user,err_details=str(e))
#         except:
#             print("Internal Error!!!")
#         return render(request, "myadmin_errors.html", {})


def filter_employee(request):
    try:
        if request.method == "GET":
            Employee=request.GET.get('Employee')
            # print(Employee,'Employee')
            paylevel=request.GET.get('paylevel')
            # print(paylevel,'paylevel')
            Designation=request.GET.get('Designation')
            # print(Designation,'Designation')
            Department=request.GET.get('Department')
            # print(Department,'Department')
            current_user = request.user.user_role
            # print(current_user)
            dict2={}
            if request.user.user_role == 'admin_super':
                employees=m1.empmast.objects.all().order_by('empname')
                dict1 = {"empno":Employee, "pc7_level":paylevel,"desig_longdesc":Designation,"dept_desc":Department}
            elif request.user.user_role == 'admin_rly' or request.user.user_role == 'admin_div':
                rlyid = AdminMaster.objects.filter(user_id = request.user.username).values('rly_id')[0]['rly_id']
                dict1 = {"empno":Employee, "pc7_level":paylevel,"desig_longdesc":Designation,"dept_desc":Department, 'rly_id': rlyid }
                # employees = m1.empmast.objects.filter(rly_id__in =rlyid).values().order_by('empname')
           
            
            for key,val in dict1.items():
                # print(key, val)
                if val!='':
                    dict2[key] =val
                   
            # print(dict2,"dict2")        
            # print(len(dict2))
            data = []  
            a= len(dict2)
           
            for i in dict2.items():
                for k,v in dict2.items():
                    # print(k)
                    data2={k:v}
                    data1=list(m1.empmast.objects.filter(**data2).values())
                    for j in data1:
                        if j not in data:
                            data.append(j)
 
                    # print(data1)
           
            return JsonResponse({'data':data},safe=False)
        return JsonResponse({"success":False},status=400)
    except Exception as e:
        try:
            m1.error_Table.objects.create(fun_name="filter_employee",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})


def viewEmployee_Det(request):
    # try:
        if request.method == "GET":
            empno = request.GET.get('empno') 

            emp = m1.empmast.objects.filter(empno=empno)[0]
            if emp.empmname == None and emp.emplname == None:
                empname = emp.empname
            elif emp.empmname == None:
                empname = emp.empname + " " + emp.emplname
            elif emp.emplname == None:
                empname = emp.empname + " " + emp.empmname
            else:
                empname = emp.empname + " " + emp.empmname + " " + emp.emplname
            # print(empno,'empno')
            desig=[]
            if emp.pc7_level is not None:
                desig=list(Level_Desig.objects.filter(pc7_levelmin__lte=emp.pc7_level,pc7_levelmax__gte=emp.pc7_level).values('designation').order_by('designation').distinct())
                
                parentdesignation=list(Level_Desig.objects.filter(pc7_levelmin__gte =emp.pc7_level).values('designation').order_by('designation').distinct())
            if emp.rl_type=='PRODUCTION UNIT' or emp.rl_type=='OFFICE' or emp.rl_type=='HEAD QUATER':
                div=""
            else:
                div=emp.currentunitdivision
                
            if emp.subdepartment=='COMMON':
                dept=""
            else:
                dept=emp.subdepartment
            try:    
                pdc = Level_Desig.objects.filter(designation=emp.desig_longdesc).values('parent_desig_code')[0]['parent_desig_code']
            except:
                pdc = None
            # print(pdc,"parent deisg code")
            if pdc!=None:
                pod=Level_Desig.objects.filter(designation_code=pdc).values('designation')[0]['designation']
            else:
                pod= ''
            # print(pod)
            context={ 
            'pod' : pod,
            'desigall':desig, 
            'parentdesignation':parentdesignation,
            'empno':emp.empno,
            'empname':empname,
            'birthdate':emp.birthdate,
            'dateapp':emp.appointmentdate,
            'railway':emp.currentzone,
            'superdate':emp.superannuation_date,
            # 'division':emp.currentunitdivision,
            'division':div,
            'department':emp.dept_desc,
            'sub_depart':dept,
            'railwaytype':emp.rl_type,
            'stationdes':emp.station_des,
            # 'office_or':emp.office_orderno,
            'gender':emp.gender,
            # 'emp_inctype':emp.emp_inctype,
            # 'marital_status':emp.marital_status,
            'email':emp.email,
            'contactno':emp.contactno,
            'subdept':emp.subdepartment,
            'rltype':emp.rl_type,
            # 'ticket_no':emp.ticket_no,
            # 'idcard_no':emp.idcard_no,
            # 'emp_inctype':emp.emp_inctype,
            # 'inc_category':emp.inc_category,
            'desig':emp.desig_longdesc,
            
            # 'status':emp.emp_status,
            'dept':emp.dept_desc,
            # 'category':emp.decode_paycategory,
            # 'payband':emp.payband,
            # 'scalecode':emp.scalecode,
            'paylevel':emp.pc7_level,
            'station_dest':emp.station_des,
            # 'wau':emp.wau,
            'billunit':emp.billunit,
            'service':emp.service_status,
            # 'emptype':emp.emptype,
            # 'medicalcode':emp.medicalcode,
            # 'tradecode':emp.tradecode,
            'role':emp.role,
            # 'shop_section':emp.shop_section,

            
        
            }  
        
        
            return JsonResponse(context, safe = False)
        return JsonResponse({"success":False}, status=400)
    # except Exception as e: 
    #     try:
    #         m1.error_Table.objects.create(fun_name="viewEmployee_Det",user_id=request.user,err_details=str(e))
    #     except:
    #         print("Internal Error!!!")
    #     return render(request, "myadmin_errors.html", {})
 


def get_emp_detNew(request):
    try:
        if request.method == "GET" and request.is_ajax():
            empno = request.GET.get('empno') 
            obj = m1.empmast.objects.filter(empno=empno).all() 
            rno=len(obj)
            if rno==0:            
                context={            
                    'rno':rno ,
                }  
            else:          
                context={  
                    'rno':rno ,          
                    'empno':obj[0].empno,
                    'empname':obj[0].empname,
                    'birthdate':obj[0].birthdate,
                    'dateapp':obj[0].appointmentdate,
                    'office_orderno':obj[0].office_orderno,
                    'sex':obj[0].sex,
                    
                    'marital_status':obj[0].marital_status,
                    'email':obj[0].email,
                    'contactno':obj[0].contactno,
                    
                    'desig':obj[0].desig_longdesc,
                    'status':obj[0].emp_status,
                    'dept':obj[0].dept_desc,
                    # 'category':obj[0].decode_paycategory,
                    'payband':obj[0].payband,
                    'scalecode':obj[0].scalecode,
                    'paylevel':obj[0].pc7_level,
                    'gradepay':obj[0].payrate,
                    'joining_date':obj[0].date_of_joining,
                    'date_of_promotion':obj[0].date_of_promotion,
                    'station_dest':obj[0].station_des,
                    'wau':obj[0].wau,
                    'billunit':obj[0].billunit,
                    'service':obj[0].service_status,
                    'emptype':obj[0].emptype,
                    'ticket_no':obj[0].ticket_no,
                    'idcard_no':obj[0].idcard_no,
                    'emp_inctype':obj[0].emp_inctype,
                    'inc_category':obj[0].inc_category,
                    
            
                }  
            
            
            return JsonResponse(context, safe = False)
        return JsonResponse({"success":False}, status=400)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="viewEmployee_Det",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})


# def assign_role(request):
    
#     if request.method=='GET' or request.is_ajax():
#         # print('hiiiii')
#         empno1 = request.GET.get('empno1')
#         # print(empno1,'-------')
#         emprole = request.GET.get('emprole')
#         # print(emprole,'----ttttt---')
#         department = request.GET.get('department')
#         # print(department,'----uuuuuutt---')
#         designation = request.GET.get('designation')
#         # print(designation,'---5555555t---')
#         parentdesig = request.GET.get('parentdesig')
#         # print(parentdesig,'===================--------=========')
      
#         s_section = request.GET.get('s_section')
#         # print(s_section,'___________________________')
#         s_section = json.loads(s_section)
#         sop =''
#         for o in s_section:
#             sop=sop+o+", "

#         # print(sop,'---------', designation)
       
        
#         parent=Level_Desig.objects.filter(designation=parentdesig).values('designation_code')
#         # print(parent)
#         employeeUpdate=empmast.objects.filter(empno=empno1).first()
#         var1=Level_Desig.objects.filter(designation=designation).first()
#         # print(employeeUpdate,'----number')
#         var1.parent_desig_code=parent[0]['designation_code']
#         var1.save()
#         employeeUpdate.role=emprole
#         # print(employeeUpdate.role)
#         empl=empmast.objects.filter(empno=empno1).first()
#         # print(empl)
#         sno=empmastnew.objects.all().last().sno
        
#         empmastnew.objects.create(sno=sno+1,emp_id=empl,shop_section=sop)
#         employeeUpdate.parent=emprole 
#         employeeUpdate.dept_desc=department
       
#         employeeUpdate.desig_longdesc=designation
        
#         employeeUpdate.save()
       
#         messages.success(request, 'Successfully Activate!')
        
        
#     return JsonResponse({'saved':'save'})

def assign_role(request):
    # try:
        if request.method=='GET':
            # print('hiiiii')
            
            empno1 = request.GET.get('empno1')
            # print(empno1,'-------')
            rly = request.GET.get('rly')
            # print(rly,'-------')
            div = request.GET.get('div')
            # print(div,'-------')
        
            department = request.GET.get('department')
            # print(department,'----uuuuuutt---')
            designation = request.GET.get('designation')
            # print(designation,'---5555555t---')
            parentdesig = request.GET.get('parentdesig')
            # print(parentdesig,'===================--------=========')
            station=request.GET.get('station')
            # s_section = request.GET.get('s_section')
            # # print(s_section,'___________________________')
            # s_section = json.loads(s_section)
            # sop =''
            # for o in s_section:
            #     sop=sop+o+", "

            # # print(sop,'---------', designation)
            rly_id=""
            div_id=""
            if railwayLocationMaster.objects.filter(location_code=rly,location_type='ZR').exists():
                rly_id=railwayLocationMaster.objects.filter(location_code=rly,location_type='ZR')[0].rly_unit_code
            if railwayLocationMaster.objects.filter(location_code=div,parent_location_code=rly).exists():
                div_id=railwayLocationMaster.objects.filter(location_code=div,parent_location_code=rly)[0].rly_unit_code
            parent=Level_Desig.objects.filter(designation=parentdesig).values('designation_code')
            # print(parent)
            employeeUpdate=m1.empmast.objects.filter(empno=empno1).first()
            var1=Level_Desig.objects.filter(designation=designation).first()
            # print(employeeUpdate,'----number')
            if parent.count()>0:
                var1.parent_desig_code=parent[0]['designation_code']
            var1.save()
            
            employeeUpdate.rly_unit_code_id=rly_id
            employeeUpdate.division_id=div_id
            employeeUpdate.station_des=station
            # empl=m1.empmast.objects.filter(empno=empno1).first()
            # if m1.empmastnew.objects.all().exists():
            #     # print('----000000')

            #     sno=m1.empmastnew.objects.all().last().sno
            # else:
            #     sno=0
            
            # empmastnew.objects.create(sno=sno+1,emp_id=empl,shop_section=sop)
            
            employeeUpdate.dept_desc=department
        
            employeeUpdate.desig_longdesc=designation
            
            employeeUpdate.save()
            desig_id=Level_Desig.objects.filter(designation=designation).values('designation_code')[0]['designation_code']
            parent_id=Level_Desig.objects.filter(designation=parentdesig).values('designation_code')
            if parent_id.count()>0:
                parent_id=parent_id[0]['designation_code']
            else:
                parent_id=None
            m1.history_table.objects.create(empno=empno1,desig_id=desig_id,parent_id=parent_id,Assigned_by="admin_super",Assigned_on=datetime.now())
        
            messages.success(request, 'Successfully Updated!')
            
            
        return JsonResponse({'saved':'save'})
    # except Exception as e: 
    #     try:
    #         m1.error_Table.objects.create(fun_name="assign_role",user_id=request.user,err_details=str(e))
    #     except:
    #         print("Internal Error!!!")
    #     return render(request, "myadmin_errors.html", {})


def details(request):
    if request.method == "GET":
       flag=request.GET.get('_id')
       flag=flag.split('@')
       op=[]
       if(flag[0]=='Disable'):
          changes = models.railwayLocationMaster.objects.filter(rly_unit_code=flag[1]).update(delete_flag=True)
       elif(flag[0]=='Enable'):
          changes = models.railwayLocationMaster.objects.filter(rly_unit_code=flag[1]).update(delete_flag=False)
       elif(flag[0] == 'Deleted'):
           # print("deleting")
           changes = models.railwayLocationMaster.objects.filter(rly_unit_code=flag[1]).update(deleted_flag=True)
    return JsonResponse(op,safe=False)
    return JsonResponse({"success":False},status=400)



def getDesigbyDepartment(request):
    try:
        if request.method == "GET" and request.is_ajax():
            department = request.GET.get('department')
            # print(department)  
            
            obj=list(Level_Desig.objects.filter(department=department).values('designation').order_by('designation').distinct('designation'))
            # print(obj,'____________________________________')
            return JsonResponse(obj, safe = False)
        return JsonResponse({"success":False}, status=400)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="getDesigbyDepartment",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})

def division_by_rly(request):
    try:
        if request.method == "GET" and request.is_ajax():
            rly=request.GET.get('rly')
            # print(rly,'_________________________aaaaaa________________')
            
            division=list(railwayLocationMaster.objects.filter(location_type='DIV',parent_location_code=rly).order_by('location_code').values('location_code').distinct('location_code'))
            l=[]
            for i in division:
                l.append(i['location_code'])
            # print(l)    
            context={
                'division':l,
            } 
            return JsonResponse(context,safe = False)
        return JsonResponse({"success":False}, status = 400)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="division_by_rly",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})


def officer_bydiv(request):
    try:
        if request.method == "GET" and request.is_ajax():
            div_1 = request.GET.get('div_1')
            
            div_id=railwayLocationMaster.objects.filter(location_code=div_1)[0].rly_unit_code
            obj=list(m1.empmast.objects.filter(division_id=div_id).values('empname').order_by('empname'))
            context={
                'obj':obj,
            }
            return JsonResponse(context, safe = False)
        return JsonResponse({"success":False}, status=400)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="officer_bydiv",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})


 

def getsection_byshop1(request):
    try:
        if request.method == "GET" and request.is_ajax():
            shop = request.GET.get('shop')
            # print(shop)  
            
            shop_id=Shop_section.objects.filter(shop_code=shop).values('section_code')
            
        
            l=[]
            for i in shop_id:
                l.append(i['section_code'])
            # print(l)    
            context={
                'shop_id':l,
            } 
            return JsonResponse(context, safe = False)
        return JsonResponse({"success":False}, status=400)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="getsection_byshop1",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})


 
def getrole_bydesig(request):
    try:
        if request.method == "GET" and request.is_ajax():
            designation = request.GET.get('designation')
            # print(designation)  
            
            desig_id=Level_Desig.objects.filter(designation=designation)[0].designation_code
            # print(desig_id)
            role=list(roless.objects.filter(designation_code=desig_id).values('role').distinct('role'))
            # print(role)
            l=[]
            for i in role:
                l.append(i['role'])
            # print(l)    
            context={
                'role':l,
            } 
            return JsonResponse(context, safe = False)
        return JsonResponse({"success":False}, status=400)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="getrole_bydesig",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})

 



def get_parentdesig(request):
    try:
        if request.method == "GET" and request.is_ajax():
            department = request.GET.get('department')
            # print(department)  
            paylevel1 = request.GET.get('paylevel1')
            # print(paylevel1)  
            
            desig_id=Level_Desig.objects.filter(department=department,pc7_level__gte=paylevel1).values('designation')
            # print(desig_id,'------')
            #parent=models.Level_Desig.objects.filter(designation=desig_id).values('designation')
            l=[]
            for i in desig_id:
                l.append(i['designation'])
            # print(l)    
            context={
                'desig_id':l,
            } 
            return JsonResponse(context,safe = False)
        return JsonResponse({"success":False}, status=400)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="get_parentdesig",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})


 

def getshopcode_bydept(request):
    try:
        if request.method == "GET" and request.is_ajax():
            department = request.GET.get('department')
            # print(department)  
            
            dept_id=departMast.objects.filter(department_name=department)[0].department_code
            # print(dept_id)
            shop_code=list(shop_section.objects.filter(department_code_id=dept_id).values('shop_code').distinct('shop_code'))
            
            l=[]
            for i in shop_code:
                l.append(i['shop_code'])
            # print(l)    
            context={
                'shop_code':l,
            } 
            return JsonResponse(context, safe = False)
        return JsonResponse({"success":False}, status=400)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="getshopcode_bydept",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})


def empregistNew(request): 
    try:
        current_user = request.user
        emp=m1.empmast.objects.filter(pk=current_user.username)  
        
        empst=m1.empmast.objects.all().distinct('emp_status','dept_desc').distinct('emp_status') 
        depart=m1.empmast.objects.all().values('dept_desc').distinct('dept_desc').order_by('dept_desc')
        railway=railwayLocationMaster.objects.all().values('location_code').distinct('location_code').order_by('location_code') 
        # shop=shop_section.objects.all().order_by('section_code') 
        employees=m1.empmast.objects.all().order_by('empname')
        # shoplist=list(shop_section.objects.filter().values('shop_code','shop_id').order_by('shop_code').distinct()) 
        # category = m1.empmast.objects.filter(decode_paycategory__isnull=False).values('decode_paycategory').distinct()
        context={
            'emp':emp,
            'employees':employees,
            'sub':0,
            # 'category':category,
            'lenm' :2,
        
            'railway':railway,         
            'empst':empst,
            
            'user':usermaster,
            'depart':depart,
        }
        if request.method=="POST":
            Submit=request.POST.get('Submit')
            empno=request.POST.get('empno')
            # print(empno)
            empname=request.POST.get('empname')
            id_card=request.POST.get('id_card')
            ticket=request.POST.get('ticket')
            emp_inctype=request.POST.get('emp_inctype')
            inc_category=request.POST.get('inc_category')
            sex=request.POST.get('empsex')
            marital_status=request.POST.get('empmarital')            
            email=request.POST.get('empemail')            
            contactno=request.POST.get('empphone')
            shopno=request.POST.get('shop_sec')  
            sub_shop_sec=request.POST.get('sub_shop_sec')
            emp_inctype=request.POST.get('emptype') 
            empdesignation=request.POST.get('empdesignation') 
            emptdepartment=request.POST.get('emptdepartment') 
            empstatus=request.POST.get('empstatus') 
            office_orderno=request.POST.get('office_orderno') 
            birthdate=request.POST.get('dobdate')
            yj=birthdate[6:10]
            mj=birthdate[3:5]
            dj=birthdate[0:2]
            birthdate=yj+'-'+mj+'-'+dj
            dateapp=request.POST.get('dateapp')
            yj=dateapp[6:10]
            mj=dateapp[3:5]
            dj=dateapp[0:2]
            dateapp=yj+'-'+mj+'-'+dj
            gradepay=request.POST.get('gradepay') 
            paylevel=request.POST.get('paylevel')
            payband=request.POST.get('payband') 
            scalecode=request.POST.get('scalecode')
            category=request.POST.get('category')
            medicalcode=request.POST.get('medicalcode') 
            tradecode=request.POST.get('tradecode')
            joining_date=request.POST.get('joining_date')
            yj=joining_date[6:10]
            mj=joining_date[3:5]
            dj=joining_date[0:2]
            joining_date=yj+'-'+mj+'-'+dj
            date_of_promotion=request.POST.get('date_of_promotion')
            yj=date_of_promotion[6:10]
            mj=date_of_promotion[3:5]
            dj=date_of_promotion[0:2]
            date_of_promotion=yj+'-'+mj+'-'+dj
            station_dest=request.POST.get('station_dest') 
            wau=request.POST.get('wau')
            billunit=request.POST.get('billunit') 
            service=request.POST.get('service')
            emptype=request.POST.get('emptype')
            # try:
            #     if(dateapp != None):
            #         dateapp=datetime.datetime.strftime(dateapp, "%Y-%m-%d")
                
            #     if(birthdate != None):
            #         birthdate=datetime.datetime.strftime(birthdate, "%Y-%m-%d")

            #     if(joining_date != None):
            #         joining_date=datetime.datetime.strftime(joining_date, "%Y-%m-%d")
                
            #     if(date_of_promotion != None):
            #         date_of_promotion=datetime.datetime.strftime(date_of_promotion, "%Y-%m-%d")
            # except:
            #     messages.success(request,'Please enter valid date !')
            # print('Submit',Submit)
            import datetime
            cuser=request.user
            now = datetime.datetime.now()
            
            

            # p=str(now).split(' ')
            
            # s=p[0].split('-')
            # day2 = s[0]
            # month2 = s[1]
            # year2 = s[2]
            
            # date1 = year2+"-"+month2+"-"+day2
            # # print(date1)
            # time=str(p[1]).replace(':','')
            
            # if(cuser != None):
            #     uniquid= str(cuser)+""+date1+""+time[:6]
            password="dlw@123"
            if Submit=='Submit':
                if user.objects.filter(username=empno).exists():
                    messages.info(request, "User Already exists!")
                else:
                    
            
                    # m1.empmast.objects.create(decode_paycategory=category, empno=empno, empname=empname, birthdate=birthdate,
                    # appointmentdate=dateapp,sex=sex,marital_status=marital_status,email=email,contactno=contactno,emp_inctype=emp_inctype,
                    # inc_category=inc_category,desig_longdesc=empdesignation,emp_status=empstatus,dept_desc=emptdepartment,
                    # office_orderno=office_orderno, date_of_joining=joining_date, date_of_promotion=date_of_promotion, pc7_level=paylevel,
                    # payrate=gradepay,payband=payband, scalecode=scalecode,wau=wau, station_des=station_dest,billunit=billunit,
                    # service_status=service, emptype=emptype,idcard_no=id_card,ticket_no=ticket, 
                    # medicalcode=medicalcode,tradecode=tradecode)
                    m1.empmast.objects.create(empno=empno, empname=empname, birthdate=birthdate,
                    appointmentdate=dateapp,sex=sex,marital_status=marital_status,email=email,contactno=contactno,emp_inctype=emp_inctype,
                    inc_category=inc_category,desig_longdesc=empdesignation,emp_status=empstatus,dept_desc=emptdepartment,
                    office_orderno=office_orderno, date_of_joining=joining_date, date_of_promotion=date_of_promotion, pc7_level=paylevel,
                    payrate=gradepay,payband=payband, scalecode=scalecode,wau=wau, station_des=station_dest,billunit=billunit,
                    service_status=service, emptype=emptype,idcard_no=id_card,ticket_no=ticket, 
                    medicalcode=medicalcode,tradecode=tradecode)
                    ID=user.objects.filter().order_by('-id')[0].id
                    newuser = user.objects.create_user(id=ID+1,username=empno, password=password,email=email, first_name=empname)
                    newuser.is_staff= True
                    # newuser.is_superuser=True
                    newuser.save()
                    
                    messages.success(request,'Record has successfully inserted !')
            else:
                # m1.empmast.objects.filter(empno=empno).update(decode_paycategory=category, emp_status=empstatus, sex=sex,marital_status=marital_status,email=email,contactno=contactno,emp_inctype=emp_inctype,inc_category=inc_category,  date_of_joining=joining_date, date_of_promotion=date_of_promotion,  empname=empname, birthdate=birthdate,appointmentdate=dateapp, desig_longdesc=empdesignation,dept_desc=emptdepartment,office_orderno=office_orderno, pc7_level=paylevel, payrate=gradepay,payband=payband, scalecode=scalecode,wau=wau,  station_des=station_dest,billunit=billunit, service_status=service, emptype=emptype,idcard_no=id_card,ticket_no=ticket,medicalcode=medicalcode,tradecode=tradecode)
                m1.empmast.objects.filter(empno=empno).update(emp_status=empstatus, sex=sex,marital_status=marital_status,email=email,contactno=contactno,emp_inctype=emp_inctype,inc_category=inc_category,  date_of_joining=joining_date, date_of_promotion=date_of_promotion,  empname=empname, birthdate=birthdate,appointmentdate=dateapp, desig_longdesc=empdesignation,dept_desc=emptdepartment,office_orderno=office_orderno, pc7_level=paylevel, payrate=gradepay,payband=payband, scalecode=scalecode,wau=wau,  station_des=station_dest,billunit=billunit, service_status=service, emptype=emptype,idcard_no=id_card,ticket_no=ticket,medicalcode=medicalcode,tradecode=tradecode)

                messages.error(request,'Record has successfully updated ')

            
        return render(request, 'empRegistrationnew.html',context)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="empregistNew",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})


def open_empregistNew(request, empno):
    try:
        emplist=m1.empmast.objects.get(empno=empno)
        railway=railwayLocationMaster.objects.filter(location_code='ZR').values('location_code')
        context={
            'emplist':emplist,
            'empno':empno,
            'railway':railway,
        }
        return render(request, 'empRegistrationNew.html',context)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="open_empregistNew",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})


def add_designation(request):
    # try:
        unit=departMast.objects.filter(delete_flag=False).values('department_name').order_by('department_name').distinct('department_name')
        cat=category.objects.all().values('category').order_by('category').distinct('category')

        post=Post_master.objects.filter(~Q(post_code=None),Q(delete_flag=False)).values('post_code').order_by('post_code').distinct('post_code')
        rltype=railwayLocationMaster.objects.filter(~Q(location_type_desc=None)).values('location_type_desc').order_by('location_type_desc').distinct('location_type_desc')
        emp=m1.empmast.objects.all()
        datatable=datatable=Level_Desig.objects.all()
        all_railway = list(railwayLocationMaster.objects.filter(location_type__in =['RDSO','WS','DIV','RB','ZR','PSU','CTI','PU']).values('rly_unit_code','location_description','location_code','location_type').distinct().order_by('location_code'))
        
        level = ['8','9','10','11','12','13','14','15','16','17','18']

        context={
            'unit':unit,
            'post':post,
            'cat':cat,
            'all_railway':all_railway,
            'rltype':rltype,
            'datatable':datatable,
            'level':level,
            # 'railway':railway,
            # 'division':division,
        }
        # savedesig=request.POST.get('savedesig')
        #         if(savedesig=="savedesig"):
        #             Level_Desig.objects.create(designation_code=,designation=,department=,parent_desig_code=,rly_unit_id=,pc7_levelmax=,department_code_id=,pc7_levelmin=,d_level=,contactnumber=,official_email_ID=)
        
        return render(request,'add_designation.html', context)
    # except Exception as e: 
    #     try:
    #         m1.error_Table.objects.create(fun_name="add_designation",user_id=request.user,err_details=str(e))
    #     except:
    #         print("Internal Error!!!")
    #     return render(request, "myadmin_errors.html", {})

def add_post(request):
    try:
        if request.method == 'POST' or request.is_ajax():
            current_user = request.user
            if str(request.user).startswith('admin'):
                actual_user = str(request.user).split('admin')[1]
            else:
                actual_user = request.user
            empnox = AdminMaster.objects.filter(Q(admin_email=actual_user), user_id__isnull=False).values('rly','user_id')            
            rly_unit_id=None
            cuser = None
            if empnox:
                rly_unit_id = empnox[0]['rly']
                cuser = empnox[0]['user_id']
            postname=request.POST.get('postname')
            postcode=request.POST.get('postcode')
            depart1=request.POST.get('depart1')
            category=request.POST.get('category')
            pc7_levelmax=request.POST.get('pc7_levelmax')
            pc7_levelmin=request.POST.get('pc7_levelmin')
            dept_id=departMast.objects.filter(department_name=depart1)[0].department_code
            if Post_master.objects.all().exists():
                id=Post_master.objects.all().last().post_id
            else:
                id=0
            Post_master.objects.create(post_id=id+1,modified_by=cuser,post_code=postcode,post_desc=postname,department_code_id=dept_id,category=category,pc7_levelmax=pc7_levelmax,pc7_levelmin=pc7_levelmin)
            # messages.success(request,'Data saved successfully') 
            messages.success(request,'Post added successfully as : '+postname)      
        return JsonResponse({'saved':'save'})
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="add_post",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})

def addPostAjax(request):
    if request.method == 'POST' or request.is_ajax():
        post_type=request.POST.get('post_type')
        if post_type == 'PostCode':
            postcode=request.POST.get('postcode')
            if Post_master.objects.filter(post_code=postcode).exists():
                msg = 'Exists'
            else:
                msg = 'Success'
            return JsonResponse(msg,safe=False)
        if post_type == 'station':
            rly_unit_id=request.POST.get('val')
            rly_unit_det=list(railwayLocationMaster.objects.filter( rly_unit_code= rly_unit_id).values('parent_rly_unit_code'))
            rly_unit_det = list(map( lambda x: int(x['parent_rly_unit_code']),rly_unit_det))
            rep_officer = list(models.Level_Desig.objects.filter(Q(rly_unit = rly_unit_id) | Q(rly_unit__in = rly_unit_det)).values('designation'))
            rep_officer = list(map( lambda x: x['designation'],rep_officer))
            all_station = list(models.station_master.objects.filter(Q(rly_id_id = rly_unit_id) | Q(div_id_id = rly_unit_id)).values('station_name').distinct().order_by('station_name'))
            context = {
                'rep_officer':rep_officer,
                'all_station':all_station,
            }
            return JsonResponse(context,safe=False)
        
        if post_type == 'checkRlyType':
            rly = request.POST.get('rly')
            post = request.POST.get('post')
            location_code = ''
            parent_location_code = ''
            location_type_desc = ''
            createdDesignation = post
            context = list(railwayLocationMaster.objects.filter(rly_unit_code=rly).values('location_code','parent_location_code','location_type_desc'))
            if len(context) > 0:
                location_code = context[0]['location_code']
                parent_location_code = context[0]['parent_location_code']
                location_type_desc = context[0]['location_type_desc']
            if location_type_desc in ['RAILWAY BOARD', 'PRODUCTION UNIT', 'HEAD QUATER', 'PSU', 'INSTITUTE']:
                createdDesignation = createdDesignation + '/' + location_code
            else:
                if post != 'DRM':
                    createdDesignation = createdDesignation + '/' + location_code + '/' + parent_location_code
                else:
                    createdDesignation = createdDesignation + '/' + location_code

            context = {
                'createdDesignation' : createdDesignation,
                
            }
            
            return JsonResponse(context, safe = False)
    return JsonResponse({"success":False},status=400)

def cal_desig(request):
    # try:
        if request.method == "GET":
            post=request.GET.get('post')
            desig=list(Level_Desig.objects.filter(designation__startswith = post).values())
            context={
                'desig':desig,
                'len':len(desig),
            }
            return JsonResponse(context, safe = False)
        return JsonResponse({"success":False}, status=400)
    # except Exception as e: 
    #     try:
    #         m1.error_Table.objects.create(fun_name="cal_desig",user_id=request.user,err_details=str(e))
    #     except:
    #         print("Internal Error!!!")
    #     return render(request, "myadmin_errors.html", {})


# def save_designation(request):
#     # try:
#         if request.method == 'POST':
#             post = request.POST.get('post')
#             designation = request.POST.get('designation')
#             contact = request.POST.get('contact')
#             email = request.POST.get('email')  
#             pre_reporting_officer = request.POST.get('reporting_officer')
#             station = request.POST.get('station')
#             rly = request.POST.get('rly')
#             div_id_id=list(railwayLocationMaster.objects.filter(rly_unit_code=rly,location_type_desc__in=rlyhead.objects.filter(rltype='HQ').values('rllongdesc')).values('parent_rly_unit_code','location_type'))
#             if len(div_id_id) > 0:
#                 hq_id_id = rly
#                 div_id_id = None
#             else:
#                 hq_id_id=list(railwayLocationMaster.objects.filter(rly_unit_code=rly).values('parent_rly_unit_code','location_type'))
                
#                 if hq_id_id[0]['location_type'] in ['DIV','WS']:
#                     div_id_id = rly
#                 else:
#                     div_id_id = None
#                 hq_id_id = hq_id_id[0]['parent_rly_unit_code']

#             if pre_reporting_officer is not None or pre_reporting_officer != '':
#                 reporting_officer = list(models.Level_Desig.objects.filter(designation = pre_reporting_officer).values('designation_code'))
#                 if len(reporting_officer) > 0:
#                     pre_reporting_officer = reporting_officer[0]['designation_code']
#                 else:
#                     pre_reporting_officer = None
#             else:
#                     pre_reporting_officer = None
#             if str(request.user).startswith('admin'):
#                 actual_user = str(request.user).split('admin')[1]
#             else:
#                 actual_user = request.user
#             empnox = AdminMaster.objects.filter(Q(admin_email=actual_user), user_id__isnull=False).values('rly','user_id')
#             #empnox = AdminMaster.objects.filter(Q(admin_email='admin'+str(request.user)) | Q(admin_email='admin'+str(request.user.email)), user_id__isnull=False).values('rly','user_id')
#             cuser = None
#             if empnox:
#                 cuser = empnox[0]['user_id']
            
#             if post != '':
#                 category = models.Post_master.objects.filter(post_code=post).values('category')[0]['category']
#                 paylevel_max = models.Post_master.objects.filter(post_code=post).values('pc7_levelmax')[0]['pc7_levelmax']
#                 paylevel_min = models.Post_master.objects.filter(post_code=post).values('pc7_levelmin')[0]['pc7_levelmin']
#                 hierarchy_level = models.category.objects.filter(category=category).values('hierarchy_level')[0]['hierarchy_level']
                
#                 dept_id = models.Post_master.objects.filter(post_code=post).values('department_code_id')[0]['department_code_id']
#                 if dept_id != '':
#                     department = models.departMast.objects.filter(department_code=dept_id).values('department_name')[0]['department_name']
#                 else:
#                     department = None
#             else:
#                 category =None
#                 paylevel_max=None
#                 paylevel_min=None
#                 dept_id=None
#                 department = None

#             if category == 'CRB':
#                 role = 'CRB'
#             else:
#                 role = 'user'
#             if email == '':
#                 email=None
#                 msg  = 'Email Address Required'
#             if contact == '':
#                 contact=None
#                 msg  = 'Contact Number Required'
#             if Level_Desig.objects.all().exists():
#                 id=Level_Desig.objects.all().last().designation_code
#             else:
#                 id=1
#             if Level_Desig.objects.filter(designation=designation).exists():
#                 msg =  'Designation already present'
#             elif Level_Desig.objects.filter(official_email_ID=email).exists():
#                 msg =  'Email Id already present'
#             # elif Level_Desig.objects.filter(contactnumber=contact,contactnumber__isnull = False).exists():
#             #     messages.error(request, 'Contact number already present')
#             elif email != None and contact != None:
#                 Level_Desig.objects.create(hq_id_id=hq_id_id,div_id_id=div_id_id,hierarchy_level=hierarchy_level,status='P',rly_unit_id=rly,parent_desig_code=pre_reporting_officer,station_name=station,modified_by=cuser,user_role=role,pc7_levelmax=paylevel_max,pc7_levelmin=paylevel_min,d_level=category,designation_code=id+1,department=department,designation=designation,department_code_id=dept_id,contactnumber=contact,official_email_ID=email)
#                 id = list(m1.MyUser.objects.values('id').order_by('-id'))
#                 if len(id)>0:
#                     id = id[0]['id'] + 1
#                 else:
#                     id = 1
#                 password = 'Admin@123'
#                 m1.MyUser.objects.filter(email=email).delete()
#                 newuser = m1.MyUser.objects.create_user(id = id,username=email, password=password,email=email,user_role=role)
#                 newuser.is_active= False
#                 newuser.is_admin=False
#                 newuser.save()
#                 myuser_id = list(m1.MyUser.objects.filter(email = email).values('id'))
#                 if len(myuser_id)>0:
#                     models.Level_Desig.objects.filter(designation = designation).update(desig_user_id = id)
#                 msg = 'Success'
            
            
#             return JsonResponse(msg, safe = False)
#         return JsonResponse({"success":False}, status=400)
#     # except Exception as e: 
#     #     try:
#     #         m1.error_Table.objects.create(fun_name="save_designation",user_id=request.user,err_details=str(e))
#     #     except:
#     #         print("Internal Error!!!")
#     #     return render(request, "myadmin_errors.html", {})

def save_designation(request):
    # try:
        if request.method == 'POST':
            post = request.POST.get('post')
            designation = request.POST.get('designation')
            contact = request.POST.get('contact')
            email = request.POST.get('email')  
            pre_reporting_officer = request.POST.get('reporting_officer')
            station = request.POST.get('station')
            rly = request.POST.get('rly')
            div_id_id=list(railwayLocationMaster.objects.filter(rly_unit_code=rly,location_type_desc__in=rlyhead.objects.filter(rltype='HQ').values('rllongdesc')).values('parent_rly_unit_code','location_type'))
            if len(div_id_id) > 0:
                hq_id_id = rly
                div_id_id = None
            else:
                hq_id_id=list(railwayLocationMaster.objects.filter(rly_unit_code=rly).values('parent_rly_unit_code','location_type'))
                
                if hq_id_id[0]['location_type'] in ['DIV','WS']:
                    div_id_id = rly
                else:
                    div_id_id = None
                hq_id_id = hq_id_id[0]['parent_rly_unit_code']

            if pre_reporting_officer is not None or pre_reporting_officer != '':
                reporting_officer = list(models.Level_Desig.objects.filter(designation = pre_reporting_officer).values('designation_code'))
                if len(reporting_officer) > 0:
                    pre_reporting_officer = reporting_officer[0]['designation_code']
                else:
                    pre_reporting_officer = None
            else:
                    pre_reporting_officer = None
            if str(request.user).startswith('admin'):
                actual_user = str(request.user).split('admin')[1]
            else:
                actual_user = request.user
            empnox = AdminMaster.objects.filter(Q(admin_email=actual_user), user_id__isnull=False).values('rly','user_id')
            #empnox = AdminMaster.objects.filter(Q(admin_email='admin'+str(request.user)) | Q(admin_email='admin'+str(request.user.email)), user_id__isnull=False).values('rly','user_id')
            cuser = None
            if empnox:
                cuser = empnox[0]['user_id']
            
            if post != '':
                category = models.Post_master.objects.filter(post_code=post).values('category')[0]['category']
                paylevel_max = models.Post_master.objects.filter(post_code=post).values('pc7_levelmax')[0]['pc7_levelmax']
                paylevel_min = models.Post_master.objects.filter(post_code=post).values('pc7_levelmin')[0]['pc7_levelmin']
                hierarchy_level = models.category.objects.filter(category=category).values('hierarchy_level')[0]['hierarchy_level']
                
                dept_id = models.Post_master.objects.filter(post_code=post).values('department_code_id')[0]['department_code_id']
                if dept_id != '':
                    department = models.departMast.objects.filter(department_code=dept_id).values('department_name')[0]['department_name']
                else:
                    department = None
            else:
                category =None
                paylevel_max=None
                paylevel_min=None
                dept_id=None
                department = None

            if category == 'CRB':
                role = 'CRB'
            else:
                role = 'user'
            if email == '':
                email=None
                msg  = 'Email Address Required'
            if contact == '':
                contact=None
                msg  = 'Success'
            msg_1 = ''  
            if Level_Desig.objects.all().exists():
                id=Level_Desig.objects.all().last().designation_code
            else:
                id=1
            if Level_Desig.objects.filter(designation=designation).exists():
                msg =  'Designation already present'
            elif Level_Desig.objects.filter(official_email_ID=email).exists():
                msg =  'Email Id already present'
            # elif Level_Desig.objects.filter(contactnumber=contact,contactnumber__isnull = False).exists():
            #     messages.error(request, 'Contact number already present')
            elif email != None:
                if Level_Desig.objects.filter(contactnumber=contact).exists():
                    contact=None
                    msg_1 = ' Contact number already exist, So contact is saved as blank'

                Level_Desig.objects.create(hq_id_id=hq_id_id,div_id_id=div_id_id,hierarchy_level=hierarchy_level,status='P',rly_unit_id=rly,parent_desig_code=pre_reporting_officer,station_name=station,modified_by=cuser,user_role=role,pc7_levelmax=paylevel_max,pc7_levelmin=paylevel_min,d_level=category,designation_code=id+1,department=department,designation=designation,department_code_id=dept_id,contactnumber=contact,official_email_ID=email)
                id = list(m1.MyUser.objects.values('id').order_by('-id'))
                if len(id)>0:
                    id = id[0]['id'] + 1
                else:
                    id = 1
                password = 'Admin@123'
                m1.MyUser.objects.filter(email=email).delete()
                newuser = m1.MyUser.objects.create_user(id = id,username=email, password=password,email=email,user_role=role)
                newuser.is_active= False
                newuser.is_admin=False
                newuser.save()
                myuser_id = list(m1.MyUser.objects.filter(email = email).values('id'))
                if len(myuser_id)>0:
                    models.Level_Desig.objects.filter(designation = designation).update(desig_user_id = id)
                msg = 'Success'
            
            
            return JsonResponse({'msg':msg,'msg_1':msg_1}, safe = False)
        return JsonResponse({"success":False}, status=400)
    # except Exception as e: 
    #     try:
    #         m1.error_Table.objects.create(fun_name="save_designation",user_id=request.user,err_details=str(e))
    #     except:
    #         print("Internal Error!!!")
    #     return render(request, "myadmin_errors.html", {})



def railwaytype(request):
    try:
        if request.method == "GET":
            railwaytype=request.GET.get('rltype')
            if railwaytype=='OFFICE':
                railway=list(railwayLocationMaster.objects.filter(location_type_desc='OFFICE').values('location_code').distinct('location_code'))
            elif railwaytype=='HEAD QUATER':
                railway=list(railwayLocationMaster.objects.filter(location_type_desc='HEAD QUATER').values('location_code').distinct('location_code'))
            elif railwaytype=='PRODUCTION UNIT':
                railway=list(railwayLocationMaster.objects.filter(location_type_desc='PRODUCTION UNIT').values('location_code').distinct('location_code'))
            elif railwaytype=='INSTITUTE':
                railway=list(railwayLocationMaster.objects.filter(location_type_desc='INSTITUTE').values('location_code').distinct('location_code'))
            elif(railwaytype=='DIVISION' or railwaytype=='WORKSHOP' or railwaytype=='STORE' or railwaytype=='CONSTRUCTION'):
                railwa=railwayLocationMaster.objects.filter(Q(location_type_desc='DIVISION')|Q(location_type_desc='WORKSHOP')|Q(location_type_desc='STORE')|Q(location_type_desc='CONSTRUCTION')).values('parent_location_code').distinct('parent_location_code')
                railway=[]
                for i in railwa:
                    railway.append({'location_code': i['parent_location_code']})
                # railway_val=request.GET.get('rly')
                # # print(railway_val)
                # division=list(railwayLocationMaster.objects.filter(Q(location_type_desc='DIVISION')|Q(location_type_desc='WORKSHOP')|Q(location_type_desc='STORE')|Q(location_type_desc='CONSTRUCTION')).values('location_code').distinct('location_code'))
                # division=list(railwayLocationMaster.objects.filter(parent_location_code=railway_val).values('location_code').distinct('location_code'))
            else:
                railway=[]
            context={
                'railway':railway,
                # 'division':division,
            }
            return JsonResponse(context, safe = False)
        return JsonResponse({"success":False}, status=400)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="railwaytype",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})


def divbyrly(request):
    try:
        if request.method == "GET":
            rly=request.GET.get('rly')
            division=list(railwayLocationMaster.objects.filter(parent_location_code=rly).values('location_code').distinct('location_code'))
            context={
                'division':division,
            }
            return JsonResponse(context, safe = False)
        return JsonResponse({"success":False}, status=400)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="divbyrly",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})



def getsection_byshop(request):
    try:
        if request.method == "GET" and request.is_ajax():
            shop = request.GET.get('shop')
            # print(shop)  
            
            shop=list(Shop_section.objects.filter(shop_code=shop).values('section_desc').distinct('section_code'))
            # print(shop)
        
            l=[]
            for i in shop:
                l.append(i['section_desc'])
            # print(l)    
            context={
                'shop':l,
            } 
            return JsonResponse(context, safe = False)
        return JsonResponse({"success":False}, status=400)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="getsection_byshop",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})


  

def getshop_bydept(request):
    try:
        if request.method == "GET" and request.is_ajax():
            dept = request.GET.get('dept')
            # print(dept)  
            
            dept_id=departMast.objects.filter(department_name=dept)[0].department_code
            # print(dept_id)
            shop=list(Shop_section.objects.filter(department_code_id=dept_id).values('shop_code').distinct('shop_code'))
            # print(shop)
            l=[]
            for i in shop:
                l.append(i['shop_code'])
            # print(l)    
            context={
                'shop':l,
            } 
            return JsonResponse(context, safe = False)
        return JsonResponse({"success":False}, status=400)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="getshop_bydept",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})



def post_bydept(request):
    try:
        if request.method == "GET" and request.is_ajax():
            dept1 = request.GET.get('dept1')
            # print(dept1)
            dept_id=departMast.objects.filter(department_name=dept1)[0].department_code
            # print(dept_id)
            post=list(Post_master.objects.filter(department_code_id=dept_id).values('post_desc').distinct('post_desc'))
            # print(post)
            context={
                'post':post,
            }
        
            
        
            return JsonResponse(context, safe = False)
        return JsonResponse({"success":False}, status=400)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="post_bydept",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})



def getpost_bydept(request):
    try:
        if request.method == "GET" and request.is_ajax():
            dept = request.GET.get('dept')
            # print(dept)  
            
            dept_id=departMast.objects.filter(department_name=dept)[0].department_code
            # print(dept_id)
            post=list(Post_master.objects.filter(department_code_id=dept_id).values('post_desc').distinct('post_desc'))
            # print(post)
            l=[]
            for i in post:
                l.append(i['post_desc'])
            # print(l)    
            context={
                'post':l,
            } 
            return JsonResponse(context, safe = False)
        return JsonResponse({"success":False}, status=400)

    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="getshop_bydept",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})




def details_desig(request):
    if request.method == "GET":
       flag=request.GET.get('_id')
       flag=flag.split('@')
       op=[]
       if(flag[0]=='Disable'):
          changes = models.Level_Desig.objects.filter(designation_code=flag[1]).update(delete_flag=True)
       elif(flag[0]=='Enable'):
          changes = models.Level_Desig.objects.filter(designation_code=flag[1]).update(delete_flag=False)
       elif(flag[0] == 'Deleted'):
           # print("deleting")
           changes = models.Level_Desig.objects.filter(designation_code=flag[1]).update(deleted_flag=True)
    return JsonResponse(op,safe=False)
    return JsonResponse({"success":False},status=400)



def div_by_rly(request):
    try:
        if request.method == "GET" or request.is_ajax():
            rly=request.GET.get('rly')
            # print(rly,'_________++++++++++++++++++++++________________')
            
            division=list(railwayLocationMaster.objects.filter(location_type='DIV',parent_location_code=rly).order_by('location_code').values('location_code').distinct('location_code'))
            l=[]
            for i in division:
                l.append(i['location_code'])
            # print(l)    
            context={
                'division':l,
            } 
            return JsonResponse(context,safe = False)
        return JsonResponse({"success":False}, status = 400)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="div_by_rly",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})




def shop_data(request):
    try:
        # # print('111111111111111111111111111111111111111')
        # # print(request.method)
        if request.method == 'POST' or request.is_ajax():
            # print('1')
            dept = request.POST.get('dept')
            shop = request.POST.get('shop')
            # print(',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',dept)
            # print(shop)
            dept_id=departMast.objects.filter(department_name=dept)[0].department_code
            # print(dept_id)
            count=1
            shopcode=Shop_section.objects.filter(department_code_id=dept_id).distinct('shop_id')
            # shopcode=list(shop_section.objects.filter(department_code_id=dept_id).distinct('shop_code')).last()
            # print(shopcode)
            shopcode=shopcode.count()
            shopcode+=1
            # print(shopcode,"+++++++++")
            c = ('%02d' % shopcode)
            shopcode1=c

            # for i in shopcode:
            #     c = ('%02d' % shopcode)
            #     shopcode1=c
            #     count+1
            #     # print(shopcode1)
        
            # print(shopcode1)
            
            shop_id=str(120)+str(dept_id)+str(shopcode1)
            # print(shop_id)
            section_id=shop_id+'00'
            # print(section_id)
            section_code=int(section_id[5:9])
            
            
            # print(section_code,'--------------__________--------------------')
            Shop_section.objects.create(department_code_id=dept_id,shop_code=shop,shop_id=shop_id,section_id=section_id,section_code=section_code)
            messages.success(request,'Data saved successfully')
            
                
        return JsonResponse({'saved':'save'})
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="shop_data",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})



def section_data(request):
    try:
        if request.method == 'POST' or request.is_ajax():
            
            dept1 = request.POST.get('dept1')
            ## print(dept1)
            sectiondept = request.POST.get('sectiondept')
            ## print(sectiondept)
            sec = request.POST.get('sec')
            ## print(sec)
            dept_id=departMast.objects.filter(department_name=dept1)[0].department_code
            ## print(dept_id)
            if Shop_section.objects.filter(department_code_id=dept_id,shop_code=sectiondept).exists():
                shopcode=Shop_section.objects.filter(department_code_id=dept_id,shop_code=sectiondept).last().section_id
            ## print(shopcode,'shopcode------')
            if Shop_section.objects.filter(department_code_id=dept_id,shop_code=sectiondept).exists():
                shopcode_id=Shop_section.objects.filter(department_code_id=dept_id,shop_code=sectiondept).last().shop_id
            ## print(shopcode_id,'shopcode_id------')

            if Shop_section.objects.filter(department_code_id=dept_id,shop_code=sectiondept).exists():

                section_code=Shop_section.objects.filter(department_code_id=dept_id,shop_code=sectiondept).last().section_code
            ## print(section_code,'section_code------')
            
            shop_id=int(shopcode)+1
            sec_code=int(section_code)+1
            if Shop_section.objects.filter(department_code_id=dept_id,shop_code=sectiondept).exists():

                Shop_section.objects.filter(department_code_id=dept_id,shop_code=sectiondept).create(section_id=shop_id,section_desc=sec,shop_code=sectiondept,department_code_id=dept_id,shop_id=shopcode_id,section_code=sec_code)
                messages.success(request,'Data saved successfully')
            
                
        return JsonResponse({'saved':'save'})
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="section_data",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})



def dept_data(request):
    try:
        if request.method == 'POST' or request.is_ajax():
            # current_user = request.user
            # emp=empmast.objects.get(pk=current_user.username).values('wau')
            # emp=models.empmast.objects.all()
            
            department = request.POST.get('department')
            # now = datetime.datetime.now()
            

            # p=str(now).split(' ')
            
            # s=p[0].split('-')
            # day2 = s[0]
            # month2 = s[1]
            # year2 = s[2]
            
            # date1 = year2+""+month2+""+day2
            
            # time=str(p[1]).replace(':','')
            obj=list(departMast.objects.filter(department_name=department).values('department_name').distinct())
            sc_1=int(departMast.objects.last().department_code)
            # print(sc_1)
            
            # print(obj,'obj')
            if len(obj)==0:
                # print('a')
                departMast.objects.create(department_name=department, department_code=sc_1+1)
                messages.success(request,'Data saved successfully')
            else:
                messages.error(request,'Department Already Exists!')
                # print('b')
                # railwayLocationMaster.objects.filter(location_code=location_code).update(location_type=location_type, location_description=desc, parent_location_code=ploco_code, location_type_desc=type_desc, rstype=rstype, station_code=st_code)
            
        return JsonResponse({'saved':'save'})
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="dept_data",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})


def shop_section(request):
    try:
        # current_user = request.user
        emp=m1.empmast.objects.all() 
        unit=departMast.objects.filter(delete_flag=False).values('department_name').order_by('department_name').distinct('department_name')
        list=[]
        cur= connection.cursor()
        cur.execute('''select department_name,shop_code,shop_id,section_code,section_id from myadmin_Shop_section a join myadmin_departMast b on
        a.department_code_id=b.department_code order by (b.department_name,a.shop_code,a.section_code) ''')
        d=cur.fetchall()
        # # print(d,'________________')
        for i in d:
            temp={}
            temp['department_name']=i[0]
            temp['shop_code']=i[1]
            temp['shop_id']=i[2]
            temp['section_code']=i[3]
            temp['section_id']=i[4]
            list.append(temp)
        # # print('list',list,'_____________________________')    
    
        cursor.close()    
    
        context={
            'emp':emp,
            'list':list,
            # 'val':val,
            'unit':unit,
        
        }
        
        return render(request, 'shop_section.html',context)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="shop_section",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})



def shop_bydept(request):
    try:
        if request.method == "GET" and request.is_ajax():
            dept = request.GET.get('dept')
            # # print("===================",dept)
            dept_id=departMast.objects.filter(department_name=dept)[0].department_code
            # # print("========id===========",dept_id)
            shop_code=list(Shop_section.objects.filter(department_code_id=dept_id).values('shop_code').distinct('shop_code'))
            # # print(shop_code)
            context={
                'shop_code':shop_code,
            }
        
            
        
            return JsonResponse(context, safe = False)
        return JsonResponse({"success":False}, status=400)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="shop_bydept",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})

def section_bydept(request):
    try:
        if request.method == "GET" and request.is_ajax():
            dept = request.GET.get('dept')
            sectiondept = request.GET.get('sectiondept')
            # print(sectiondept)
            dept_id=departMast.objects.filter(department_name=dept)[0].department_code
            # print(dept_id)
            section_desc=list(Shop_section.objects.filter(department_code_id=dept_id,shop_code=sectiondept).values('section_desc').distinct('section_desc'))
            # print(section_desc)
            context={
                'section_desc':section_desc,
            }
        
            
        
            return JsonResponse(context, safe = False)
        return JsonResponse({"success":False}, status=400)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="section_bydept",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})


def RoleAdd(request):
    try:
        # cuser=request.user
        # usermaster=empmast.objects.filter(empno=cuser).first()
        # current_user = request.user
        # emp=empmast.objects.filter(pk=current_user.username).values('wau')
    
        list=[]
        
        val = roless.objects.all().filter(delete_flag=False).values('role','parent','department_code_id').order_by('role').distinct() 
        for i in val:
            temp={}
            temp['role']=i['role']
            temp['parent']=i['parent']
            if departMast.objects.filter(department_code=i['department_code_id']).exists():
                temp['department_name']=departMast.objects.filter(department_code=i['department_code_id'])[0].department_name 
            else:
                temp['department_name']='None'     
            list.append(temp)
        role = roless.objects.all().filter(delete_flag=False).values('role').order_by('role').distinct()
        empdep = departMast.objects.all().values('department_name').order_by('department_name').distinct()
        # shop = shop_section.objects.values('shop_code').order_by('shop_code').distinct()
        # users = []
        if request.method=="POST":
            rolename = request.POST.get('roldel')
            # print(rolename)
            if rolename:
            
                custom_menu.objects.all().filter(role=rolename).delete()
                roless.objects.all().filter(role=rolename).update(delete_flag=True)
                userremove = m1.empmast.objects.all().values('empno').filter(role=rolename)
                for i in range(len(userremove)):
                    # users.append(userremove[i]['empno'])
                    m1.empmast.objects.filter(empno=userremove[i]['empno']).update(role=None,parent=None)
                # User.objects.filter(username__in=users).delete()
                messages.success(request, 'Successfully Deleted!')
            else:
                messages.error(request,"Error")
        context = {
        
            'roles' : role,
            'val':val,
            'empdep':empdep,
            # 'shop':shop,
            'list':list,
            # 'wau':emp[0]['wau'],
        }
        return render(request,'RoleAdd.html',context)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="RoleAdd",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})


def ajaxDeleteRoleUser(request):
    try:
        if request.method == 'POST' or request.is_ajax():

            rolename= request.POST.get('roledel')
            if rolename:
                perlist = custom_menu.objects.filter(role=rolename).values('url').distinct()   
                custom_menu.objects.all().filter(role=rolename).delete()
                roless.objects.all().filter(role=rolename).update(delete_flag=True)
                userremove = m1.empmast.objects.all().values('empno').filter(role=rolename)
                for i in range(len(userremove)):
                
                    m1.empmast.objects.filter(empno=userremove[i]['empno']).update(role=None,parent=None)
                
        
        return JsonResponse({'deleted':'delete'})

    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="ajaxDeleteRoleUser",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})




def ajaxRoleGen(request):
    try:
        if request.method=='POST' or request.is_ajax():
            
            # emp=models.empmast.objects.get(pk=current_user.username)  
            emp=m1.empmast.objects.all() 
            rolename = request.POST.get('rolename')
            department = request.POST.get('department')
            designation = request.POST.get('designation')
            shop = request.POST.get('shop1')
            shop1 = json.loads(shop)
            sop =''
            for o in shop1:
                sop=sop+o+", "

            # print(sop,'---------', designation)
            role=roless.objects.filter(role=rolename)
            desig_id=Level_Desig.objects.filter( designation= designation)[0].designation_code
            # print(desig_id)
            dept_id=departMast.objects.filter(department_name=department)[0].department_code
            # print(dept_id)
            if len(role)==0:
                roless.objects.create(role=rolename,parent=rolename,department_code_id=dept_id,modified_by=emp.empno, rly_unit=emp.wau,shop_code=sop, designation_code=desig_id)            
                messages.success(request,"succesfully added!")
            else:
                messages.error(request,"This role already exists")
        return JsonResponse({'saved':'save'})
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="ajaxRoleGen",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})

def getDepartmentbyroles(request):
    try:
        if request.method == "GET" and request.is_ajax():
            emptdepartment = request.GET.get('emptdepartment')
                
            if emptdepartment !=None: 
                obj=list(departMast.objects.filter(department=emptdepartment).values('designation').order_by('designation').distinct())
                
            return JsonResponse(obj, safe = False)
        return JsonResponse({"success":False}, status=400)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="getDepartmentbyroles",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})


def getDesigbyDepartment(request):
    try:
        if request.method == "GET" and request.is_ajax():
            department = request.GET.get('department')
            # print(department)  
            
            obj=list(Level_Desig.objects.filter(department=department).values('designation').order_by('designation').distinct('designation'))
            # print(obj,'____________________________________')
            return JsonResponse(obj, safe = False)
        return JsonResponse({"success":False}, status=400)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="getDesigbyDepartment",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})

def getshopcode_bydept(request):
    try:
        if request.method == "GET" and request.is_ajax():
            department = request.GET.get('department')
            # print(department)  
            
            dept_id=departMast.objects.filter(department_name=department)[0].department_code
            # print(dept_id)
            shop_code=list(Shop_section.objects.filter(department_code_id=dept_id).values('shop_code').distinct('shop_code'))
            
            l=[]
            for i in shop_code:
                l.append(i['shop_code'])
            # print(l)    
            context={
                'shop_code':l,
            } 
            return JsonResponse(context, safe = False)
        return JsonResponse({"success":False}, status=400)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="getshopcode_bydept",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})
    
def adminuserHome(request):
    try:
        return render(request,"adminuserHome.html")
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="adminuserHome",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})
    
def admin_logout(request):
    try:
        logout(request)
        return HttpResponseRedirect('/login')
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="admin_logout",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})
    
def inspect_logout(request):
    try:
        logout(request)
        return HttpResponseRedirect('/login')
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="inspect_logout",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})
       
def admin_changePassword(request):
    # print('jjjjj')
    try:
        if request.method == "POST":
            try:
                oldpass = request.POST.get('oldPassword').strip()
                newpass = request.POST.get('confirmNewPassword').strip()
                loguser = request.user.pk

                if len(str(newpass).strip()) < 8 or oldpass == None or newpass == None:
                    # make an error manually to go into except block
                    raise ValueError('Password must be 8 chars')

                loguser = user.objects.get(pk=loguser)
                if loguser.check_password(oldpass):
                    loguser.set_password(newpass)
                    loguser.save()
                    # print('jjjjj')
                    messages.success(request, "Password Changed successfully.")
                    return HttpResponseRedirect('/login')
                    # print('done')
                else:
                    messages.error(request, "Invalid Credentials.")

            except Exception as e: 
                # print(e,'aaaaaaaaaaaaaaa')
                messages.error(request, "Something went wrong.")
                return HttpResponseRedirect('/inspect_changePassword')
        return render(request, "inspect_changePassword.html")
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="admin_changePassword",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})

from collections import namedtuple


def headquarterMaster(request):
    try:
        if request.method == "POST":
            hq_code = request.POST.get('headquarter_code')
            hq_empno = request.POST.get('empno')
            hq_name = request.POST.get('empname')
            hq_desig = request.POST.get('designation')
            hq_contact = request.POST.get('contact')
            hq_admin_mob = request.POST.get('admin_mobile')
            hq_admin_phn = str(request.POST.get('admin_phone'))
            hq_admin_email = request.POST.get('admin_email')
            hq_rly = request.POST.get('headquarter_rly')
            hq_status = request.POST.get('headquarter_status')
            if hq_code:
                try:
                    headquarter_rlyObj = models.railwayLocationMaster.objects.get(location_code=hq_rly)                   
                    val="admin "+headquarter_rlyObj.location_code
                    hqObj = models.AdminMaster.objects.get(pk=hq_code)
                    userObj = user.objects.filter(username=hqObj.user_id)[0]
                    try:
                                hqObj.admin_mobile = hq_admin_mob
                    except Exception as e:
                        # print(e)
                        messages.error(
                            request, "Can't Update mobile no, new mobile you entered already exists.")
                        return HttpResponseRedirect('/headquarterMaster')

                    try:
                        if userObj.email != hq_admin_email:

                                email_body = f'''
                               
                                   Hello {hq_desig},
                                   Your email for RKVY has been updated from {userObj.email} to {hq_admin_email}.
                                   Sincerely,
                                   RKVY Team
                                '''

                                try:
                                    subject="Login Credentials for RKVY"
                                    To=userObj.email
                                    email_body1='<p>'+email_body+'</p>'
                                    userObj.email = hq_admin_email
                                    userObj.save()
                                    hqObj.admin_email = hq_admin_email
                                except Exception as e:
                                    # print(e)
                                    messages.error(request, "Email failed.")
                                    return HttpResponseRedirect('/headquarterMaster')

                           
                    except Exception as e:
                        
                        messages.error(
                            request, "Can't Update email, new email you entered already exists.")
                        return HttpResponseRedirect('/headquarterMaster')

                    
                    hqObj.designation = hq_desig
                    hqObj.emp_name = hq_name
                  
                    hqObj.admin = hq_empno
                    if hq_admin_phn:
                        hqObj.admin_phone = hq_admin_phn
                    else:
                        hqObj.admin_phone= '' 
                    if hq_rly != "":
                        hqObj.rly = models.railwayLocationMaster.objects.get(location_code=hq_rly)
                    hqObj.status = hq_status
                    hqObj.save()

                    messages.success(request, "Successfully Updated the Headquarter")
                    return HttpResponseRedirect('/headquarterMaster')

                except Exception as e:
                    # print(e)
                    messages.error(request, "Something went wrong.")
                    return HttpResponseRedirect('/headquarterMaster')

            else:
                if models.AdminMaster.objects.filter(admin_email=hq_admin_email).exists():
                    messages.error(request, "Headquarter already exists with this email")
                elif models.AdminMaster.objects.filter(admin_mobile=hq_admin_mob).exists():
                    messages.error(request, "Headquarter already exists with this Mobile no")
                elif user.objects.filter(email='admin'+str(hq_admin_email)).exists():
                    messages.error(request, "email already exists in usermaster")
                else:
                    headquarter_rlyObj = models.railwayLocationMaster.objects.get(location_code=hq_rly)
                
                    import datetime

                    hqObj = models.AdminMaster(admin=hq_empno,admin_mobile=hq_admin_mob,admin_email=hq_admin_email,status=hq_status,designation=hq_desig,emp_name=hq_name, rly=headquarter_rlyObj,created_on=datetime.datetime.now())
                    if hq_admin_phn:
                        hqObj.admin_phone = hq_admin_phn
                    
                    # try:
                    hqObj.save()
                    uname=models.AdminMaster.objects.filter(rly_id=headquarter_rlyObj.rly_unit_code).count()
                    
                    cnt=('%03d' % uname)
                    val2=str(headquarter_rlyObj.rly_unit_code)+str(cnt)
                    
                    val="admin "+headquarter_rlyObj.location_code
                    obj=models.AdminMaster.objects.filter(admin_email=hq_admin_email).update(user_id=val2)
                    
                    _password = "Admin@123"
                    hq_admin_email = 'admin'+str(hq_admin_email)
                    id=user.objects.filter().order_by('-id')[0].id
                    id+=1
                    user.objects.create_user(id=id,username=val2, is_active=True,password=_password,email=hq_admin_email,is_admin=True,user_role="admin_rly")
                        
                        
                    # except Exception as e:
                    #     messages.error(
                    #         request, "Headquarter already exists with this email or mobile no.")
                    #     return HttpResponseRedirect('/headquarterMaster')

                    messages.success(request, "HeadQuarter added succesfully with username - "+val2)
                return HttpResponseRedirect('/headquarterMaster')

        cursor = connection.cursor()
        cursor.execute("""SELECT hq.code, hq.address, hq.designation, hq.emp_name,hq.user_id, hq.admin, hq.admin_mobile, hq.admin_phone, hq.admin_email, hq.status, r.location_code, r.location_type FROM "myadmin_railwaylocationmaster" r ,"AdminMaster" hq where r.location_type!='DIV' and  hq.rly_id=r.rly_unit_code order by hq.code""")

        data1=namedtuplefetchall(cursor)
        cursor.close()
       # type=railwayLocationMaster.objects.filter(Q(location_type_desc='INSTITUTE')|Q(location_type_desc='HEAD QUATER')|Q(location_type_desc='PRODUCTION UNIT')|Q(location_type_desc='PSU')|Q(location_type_desc='RAILWAY BOARD')).values('location_type').distinct().order_by('location_type','location_code')
        #Nishu Gupta 070324 done by manoj
        type=railwayLocationMaster.objects.filter(Q(location_type_desc='INSTITUTE')|Q(location_type_desc='HEAD QUATER')|Q(location_type_desc='TRAFFIC ACCOUNT')|Q(location_type_desc='OFFICE')|Q(location_type_desc='DIVISION')|Q(location_type_desc='WORKSHOP')|Q(location_type_desc='PRODUCTION UNIT')|Q(location_type_desc='')|Q(location_type_desc='PSU')|Q(location_type_desc='RAILWAY BOARD')).distinct('location_type').order_by('location_type','location_code')
        #Nishu Gupta  070324 done by manoj
        
        return render(request, "headquarter.html", {'headquarter': data1,'type':type})
        
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="headquarterMaster",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})
    


# def headquarterMaster(request):
#     try:
#         if request.method == "POST":
#             hq_code = request.POST.get('headquarter_code')
#             # # print(',,,,,,,,,,,',hq_code)
#             # # print('999999999999')
#             # hq_address = request.POST.get('headquarter_address')
#             # hq_pincode = request.POST.get('pincode')
#             hq_empno = request.POST.get('empno')
#             hq_name = request.POST.get('empname')
#             hq_desig = request.POST.get('designation')
#             hq_contact = request.POST.get('contact')
        

#             # hq_officialemail = request.POST.get('admin_email')
#             # pincodeObj = models.locationMaster.objects.get(pk=hq_pincode)
#             # hq_admin = request.POST.get('headquarter_admin')

#             hq_admin_mob = request.POST.get('admin_mobile')
#             # change25
#             hq_admin_phn = str(request.POST.get('admin_phone'))
#             hq_admin_email = request.POST.get('admin_email')
#             hq_rly = request.POST.get('headquarter_rly')
#             # print(hq_rly)
#             # # print(hq_rly,'///////////////')
#             hq_status = request.POST.get('headquarter_status')
#             # # print(hq_status,'//////_________///////')
            
            
#             # print(hq_code,hq_empno,hq_name,hq_desig,hq_contact,hq_admin_mob,hq_admin_phn,hq_admin_email,hq_rly,hq_status)
#             if hq_code:
#                 # update
#                 try:
#                     headquarter_rlyObj = models.railwayLocationMaster.objects.get(location_code=hq_rly)
                    
#                     # headquarter_rlyObj = models.railwayLocationMaster.objects.filter(location_code=hq_rly).values('location_code')
#                     # print(headquarter_rlyObj)
#                     val="admin "+headquarter_rlyObj.location_code
#                     # print(val)
#                     # val="admin "+headquarter_rlyObj
#                     hqObj = models.AdminMaster.objects.get(pk=hq_code)
#                     # print(hqObj)
#                     # userObj = user.objects.filter(first_name=val)[0]
#                     userObj = user.objects.filter(username=hqObj.user_id)[0]
#                     try:
#                         # if hq_admin_mob != userObj.official_mobileNo:
#                         #         userObj.official_mobileNo = hq_admin_mob
#                         #         userObj.save()
#                                 hqObj.admin_mobile = hq_admin_mob
                                
                    
                            
                            

#                     except Exception as e:
#                         # print(e)
#                         messages.error(
#                             request, "Can't Update mobile no, new mobile you entered already exists.")
#                         return HttpResponseRedirect('/headquarterMaster')

#                     try:
#                         if userObj.email != hq_admin_email:

#                                 email_body = f'''
                               
#                                    Hello {hq_desig},
#                                    Your email for RKVY has been updated from {userObj.email} to {hq_admin_email}.
#                                    Sincerely,
#                                    RKVY Team
#                                 '''

#                                 try:
                                    
#                                     # send_mail("Login Credentials for RKVY", email_body, 'crisdlwproject@gmail.com',
#                                     #           [f'{userObj.email}'], fail_silently=False)

#                                     #saud faisal (28-08-2021) -----
#                                     subject="Login Credentials for RKVY"
#                                     To=userObj.email
#                                     email_body1='<p>'+email_body+'</p>'
#                                     # MailSend(subject,email_body1,To)
#                                     #end here

#                                     userObj.email = hq_admin_email
#                                     userObj.save()
#                                     hqObj.admin_email = hq_admin_email
#                                 except Exception as e:
#                                     # print(e)
#                                     messages.error(request, "Email failed.")
#                                     return HttpResponseRedirect('/headquarterMaster')

                           
#                     except Exception as e:
#                         # print(e,'0000000')
#                         messages.error(
#                             request, "Can't Update email, new email you entered already exists.")
#                         return HttpResponseRedirect('/headquarterMaster')

                    
#                     # hqObj.address = hq_address
#                     # hqObj.pincode = pincodeObj
#                     hqObj.designation = hq_desig
#                     hqObj.emp_name = hq_name
#                     # hqObj.admin = hq_admin
#                     hqObj.admin = hq_empno
#                     # # print('1111111111')

#                     if hq_admin_phn:
#                         hqObj.admin_phone = hq_admin_phn
#                     # change25
#                     else:
#                         hqObj.admin_phone= '' 
#                     if hq_rly != "":
#                         hqObj.rly = models.railwayLocationMaster.objects.get(location_code=hq_rly)
#                     hqObj.status = hq_status
#                     hqObj.save()

#                     messages.success(request, "Successfully Updated the Headquarter")
#                     return HttpResponseRedirect('/headquarterMaster')

#                 except Exception as e:
#                     # print(e)
#                     messages.error(request, "Something went wrong.")
#                     return HttpResponseRedirect('/headquarterMaster')

#             else:
#                 # create new
#                 # # print('9')
#                 # print(hq_rly)


#                 headquarter_rlyObj = models.railwayLocationMaster.objects.get(location_code=hq_rly)
#                 # # print(headquarter_rlyObj,"this is railway object")
#                 import datetime

#                 # hqObj = models.AdminMaster( address=hq_address,admin=hq_admin,admin_mobile=hq_admin_mob,admin_email=hq_admin_email,status=hq_status, rly=headquarter_rlyObj,pincode=pincodeObj,created_on=datetime.datetime.now())
#                 hqObj = models.AdminMaster(admin=hq_empno,admin_mobile=hq_admin_mob,admin_email=hq_admin_email,status=hq_status,designation=hq_desig,emp_name=hq_name, rly=headquarter_rlyObj,created_on=datetime.datetime.now())
#                 # # print('00000000')
#                 if hq_admin_phn:
#                     hqObj.admin_phone = hq_admin_phn
                
#                 try:
#                     hqObj.save()
#                     # # print('99')
#                     uname=models.AdminMaster.objects.filter(rly_id=headquarter_rlyObj.rly_unit_code).count()
#                     # # print(uname,"uname")
#                     cnt=('%03d' % uname)
#                     # # print(cnt,"counttttt")
#                     val2=str(headquarter_rlyObj.rly_unit_code)+str(cnt)
#                     # # print(val2,"val2222222")
#                     val="admin "+headquarter_rlyObj.location_code
#                     obj=models.AdminMaster.objects.filter(admin_email=hq_admin_email).update(user_id=val2)
#                     # # print(val,"vallll")
#                     _password = "Admin@123"
#                     # if user.objects.filter(email=hq_admin_email).exists():
#                     #     obj=user.objects.get(email=hq_admin_email)
#                     #     obj.is_admin=True
#                     #     obj.first_name=val
#                     #     obj.username=val2
#                     #     obj.user_role="admin_rly"
#                     #     obj.save()

#                     # else:
#                     # user.objects.create_user(username=val2, is_active=True,password=_password,email=hq_admin_email, first_name=val,is_admin=True,user_role="admin_rly")
                    
#                     id=user.objects.filter().order_by('-id')[0].id
#                     id+=1
#                     user.objects.create_user(id=id,username=val2, is_active=True,password=_password,email=hq_admin_email, first_name=hq_name,is_admin=True,user_role="admin_rly")
#                     # userObj = models.AuthUser(email=hq_admin_email, password=_password,
#                     #                               first_name=hqObj.pk, last_name=str(hq_admin)[:30],username="admin"+"_"+hq_rly)
#                     # userObj.is_active = True
#                     # userObj.save()
#                     # email_context = {
                        
#                     #     'login_id': userObj.email,
#                     #     'password': _password,
#                     # }
#                     # # print('00/////////')
#                     # email_template_name = "accounts/email_headquarter_credentials.txt"
#                     # email_body = render_to_string(
#                     #     email_template_name, email_context)
#                     # try:
#                     #     # send_mail("Login Credentials for RKVY", email_body, 'crisdlwproject@gmail.com',
#                     #     #           [f'{userObj.email}'], fail_silently=False)
                        
#                     # #saud faisal (28-08-2021) -----
#                     #     subject="Login Credentials for RKVY"
#                     #     To=userObj.email
#                     #     email_body1='<p>'+email_body+'</p>'
#                     #     MailSend(subject,email_body1,To)
#                     #     #end here
                        
#                     # except Exception as e:
#                     #     # print(e)
#                     #     userObj.delete()
#                     #     hqObj.delete()
#                     #     messages.error(request, "Email failed.")
#                     #     return HttpResponseRedirect('/rkvy_headquarterMaster')
                    
#                 except Exception as e:
#                     # print(e,'999999999999999999999999999')
#                     messages.error(
#                         request, "Headquarter already exists with this email or mobile no.")
#                     return HttpResponseRedirect('/headquarterMaster')

#                 messages.success(request, "HeadQuarter added succesfully.")
#                 return HttpResponseRedirect('/headquarterMaster')

#         #changes 12-08 Ritika Garg
#         # headquarter = list(
#         #     models.rkvy_headquarterMaster.objects.all().order_by('headquarter_code'))

#         cursor = connection.cursor()
#         # cursor.execute("""SELECT hq.code, hq.address, hq.designation, hq.emp_name, hq.admin, hq.admin_mobile, hq.admin_phone, hq.admin_email, hq.status, r.location_code, hq.pincode_id, r.location_type, l.district, l.state FROM "myadmin_railwaylocationmaster" r ,"AdminMaster" hq, "locationMaster" l  where r.location_type!='DIV' and status='Active' and  hq.rly_id=r.rly_unit_code and hq.pincode_id=l.pincode order by hq.code""")
#         cursor.execute("""SELECT hq.code, hq.address, hq.designation, hq.emp_name,hq.user_id, hq.admin, hq.admin_mobile, hq.admin_phone, hq.admin_email, hq.status, r.location_code, r.location_type FROM "myadmin_railwaylocationmaster" r ,"AdminMaster" hq where r.location_type!='DIV' and  hq.rly_id=r.rly_unit_code order by hq.code""")

#         # cursor.execute("""SELECT hq.headquarter_code, hq.headquarter_address, hq.headquarter_admin, hq.admin_mobile, hq.admin_phone, hq.admin_email, hq.headquarter_status, r.location_code, hq.pincode_id, r.location_type, l.district, l.state FROM "myadmin_railwaylocationmaster" r ,"headquarterMaster" hq, "locationMaster" l  where hq.headquarter_rly_id=r.rly_unit_code and hq.pincode_id=l.pincode order by hq.headquarter_code""")
#         data1=namedtuplefetchall(cursor)
#         # cursor.execute("""SELECT hq.code, hq.address, hq.admin, hq.admin_mobile, hq.admin_phone, hq.admin_email, hq.status, r.location_code, hq.pincode_id, r.location_type, l.district, l.state FROM "myadmin_railwaylocationmaster" r ,"AdminMaster" hq, "locationMaster" l  where r.location_type!='DIV' and hq.rly_id=r.rly_unit_code and hq.pincode_id=l.pincode order by hq.code""")
        
#         type=railwayLocationMaster.objects.filter(Q(location_type_desc='INSTITUTE')|Q(location_type_desc='HEAD QUATER')|Q(location_type_desc='PRODUCTION UNIT')|Q(location_type_desc='OFFICE')).values('location_type').distinct()
#         # type=railwayLocationMaster.objects.filter(Q(location_type_desc='DIVISION')|Q(location_type_desc='WORKSHOP')|Q(location_type_desc='STORE')|Q(location_type_desc='CONSTRUCTION')).values('location_type').distinct()
#         return render(request, "headquarter.html", {'headquarter': data1,'type':type})
#         return render(request, "headquarter.html")
#     except Exception as e: 
#         try:
#             m1.error_Table.objects.create(fun_name="headquarterMaster",user_id=request.user,err_details=str(e))
#         except:
#             print("Internal Error!!!")
#         return render(request, "myadmin_errors.html", {})
 
def editHeadquarter(request):
    # try:
        if request.method == "POST":
            # print("yes")
            _id = int(request.POST.get("id"))
            # print(_id)

            headquarterData = models.AdminMaster.objects.filter(pk=_id)
            # print(headquarterData)
            # city =headquarterData[0].pincode.district
            # state = headquarterData[0].pincode.state
            location = headquarterData[0].rly.location_description
            # print(location)
            headquarterData = list(headquarterData.values())
            # print(headquarterData)
            # headquarterData[0]['headquarter_city'] = city
            # headquarterData[0]['headquarter_state'] = state
            headquarterData[0]['headquarter_rly'] = location
            # print(headquarterData)
            return JsonResponse(
                {
                    "status": 1,
                    "headquarterData": headquarterData,
                }
            )
        bono=[]
        return JsonResponse(
            {
                "status": 0,
                "bono":bono
            }
        )
    # except Exception as e: 
    #     try:
    #         m1.error_Table.objects.create(fun_name="editHeadquarter",user_id=request.user,err_details=str(e))
    #     except:
    #         print("Internal Error!!!")
    #     return render(request, "myadmin_errors.html", {})

def deleteHeadQuarter (request):
    try:
        if request.method == "POST":
            _id = int(request.POST.get("id"))
            obj = (models.AdminMaster.objects.filter(code=_id))[0]
            email=request.POST.get("admin_email")
            ## print(obj)
            # obj.status="InActive"
            # obj.save()

            # obj = user.objects.filter(email=email).update(is_admin=False)
            if obj.status=="InActive":
                obj.status="Active"
                obj.save()
                obj = user.objects.filter(email=email).update(is_admin=True)
            elif obj.status=="Active":
                obj.status="InActive"
                obj.save()
                obj = user.objects.filter(email=email).update(is_admin=False)

            return JsonResponse({
                "status": 1,
            }
            )
        return JsonResponse(
            {
                "status": 0,
            }
        )
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="deleteHeadQuarter",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})
    
def buildInstituteRly(request):
    # print('0')
    try:
        if request.method == "POST":
            zonetype = request.POST.get("zonetype")
            # print(zonetype)
            parentzone = request.POST.get("parentzone")

            location = []

            # print(',1111111111111111',parentzone)

           
            if zonetype == "OT":
                location = list(models.railwayLocationMaster.objects.filter().values('location_code', 'location_description').exclude(location_type__in=['PU','ZR']).distinct().order_by('location_description'))
                # print('o')
            elif parentzone == "":
                location = list(models.railwayLocationMaster.objects.filter(
                    location_type=zonetype).values('location_code', 'location_description').distinct().order_by('location_description'))
            else:
                location = list(models.railwayLocationMaster.objects.filter(
                    location_type=zonetype, parent_location_code=parentzone).values('location_code', 'location_description').distinct().order_by('location_description'))

            return JsonResponse({'location': location, })
        return JsonResponse({"success": False}, status=400)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="buildInstituteRly",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})

def getParentZones(request):
    print('0;;;;')


def fetchEmployee(request):
    # try:
        desc = request.GET.get('desc')
        # print(desc)
        employees = list(m1.empmast.objects.filter(
                        rly_id__location_code=desc).values('empno').distinct())
        # print(employees)
        return JsonResponse({'employees': employees, })
    # except Exception as e: 
    #     try:
    #         m1.error_Table.objects.create(fun_name="fetchEmployee",user_id=request.user,err_details=str(e))
    #     except:
    #         print("Internal Error!!!")
    #     return render(request, "myadmin_errors.html", {})

def fetchStateCity(request):
    try:
        if request.method == "POST":
            # print('11111111')
            pincode = request.POST.get('pincode')
            pincodedata = 'NULL'
            # print(pincode)
            # print('9999999999')
            if models.locationMaster.objects.filter(pincode=pincode).exists():
                pincodedata = list(models.locationMaster.objects.filter(
                    pincode=pincode).values('pincode', 'district', 'state'))[0]
            ## print(pincodedata)
            return JsonResponse({'status': 200, 'pincodedata': pincodedata})
        return JsonResponse({'status': 500, })
 
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="fetchStateCity",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})

def fetchData(request):
    try:
        empno = request.GET.get('empno')
        ## print(empno)
        details = list(m1.empmast.objects.filter(
                        empno=empno).values('contactno','email').distinct())
        ## print(details)
        return JsonResponse({'details': details, })
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="fetchData",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})

def namedtuplefetchall(cursor):
    try:
        "Return all rows from a cursor as a namedtuple"
        desc = cursor.description
        nt_result = namedtuple('Result', [col[0] for col in desc])
        return [nt_result(*row) for row in cursor.fetchall()]
    except Exception as e: 
        try:
            models.error_Table.objects.create(fun_name="namedtuplefetchall",user_id=request.user,err_details=str(e))
        except:
            # print(e)
            print("Internal Error!!!")

def DivisonMaster(request):
    # try:
        if request.method == "POST":
            hq_code = request.POST.get('divison_code')
            hq_empno = request.POST.get('empno')
            hq_name = request.POST.get('empname')
            hq_desig = request.POST.get('designation')
            hq_contact = request.POST.get('contact')
            hq_admin_mob = request.POST.get('admin_mobile')
            hq_admin_phn = str(request.POST.get('admin_phone'))
            hq_admin_email = request.POST.get('admin_email')
            hq_rly = request.POST.get('divison_rly')
            hq_status = request.POST.get('divison_status')
           

            if hq_code:
                try:
                    headquarter_rlyObj = models.railwayLocationMaster.objects.get(rly_unit_code=hq_rly)
                  
                    val="admin "+headquarter_rlyObj.location_code

                    hqObj = models.AdminMaster.objects.get(pk=hq_code)
                    userObj = user.objects.filter(username=hqObj.user_id)[0]
                    try:
                            hqObj.admin_mobile = hq_admin_mob
                    except Exception as e:
                        messages.error(
                            request, "Can't Update mobile no, new mobile you entered already exists.")
                        return HttpResponseRedirect('/DivisonMaster')

                    try:
                        if userObj.email != hq_admin_email:

                                email_body = f'''
                                   Hello {hq_desig},
                                   Your email for inspection has been updated from {userObj.email} to {hq_admin_email}.
                                   Sincerely,
                                   e-Inspection Team
                                '''

                                try:
                                    subject="Login Credentials for RKVY"
                                    To=userObj.email
                                    email_body1='<p>'+email_body+'</p>'
                                    userObj.email = hq_admin_email
                                    userObj.save()
                                    hqObj.admin_email = hq_admin_email
                                except Exception as e:
                                    messages.error(request, "Email failed.")
                                    return HttpResponseRedirect('/DivisonMaster')

                            
                    except Exception as e:
                        messages.error(
                            request, "Can't Update email, new email you entered already exists.")
                        return HttpResponseRedirect('/DivisonMaster')
                    hqObj.admin = hq_empno
                    hqObj.emp_name = hq_name
                    hqObj.designation = hq_desig
                    if hq_admin_phn:
                        hqObj.admin_phone = hq_admin_phn
                    else:
                        hqObj.admin_phone= '' 
                    if hq_rly != "":
                        hqObj.rly = models.railwayLocationMaster.objects.get(rly_unit_code=hq_rly)
                    hqObj.headquarter_status = hq_status
                    hqObj.save()

                    messages.success(request, "Successfully Updated the Divison")
                    return HttpResponseRedirect('/DivisonMaster')

                except Exception as e:
                    messages.error(request, "Something went wrong.")
                    return HttpResponseRedirect('/DivisonMaster')

            else:
                # if models.AdminMaster.objects.filter(admin_email=hq_admin_email).exists():
                #     messages.error(request, "Headquarter already exists with this email")
                # elif models.AdminMaster.objects.filter(admin_mobile=hq_admin_mob).exists():
                #     messages.error(request, "Headquarter already exists with this Mobile no")
                # elif user.objects.filter(email=hq_admin_email).exists():
                #     messages.error(request, "email already exists in usermaster")
                if models.AdminMaster.objects.filter(admin_email=hq_admin_email).exists():
                    messages.error(request, "Headquarter already exists with this email")
                elif models.AdminMaster.objects.filter(admin_mobile=hq_admin_mob).exists():
                    messages.error(request, "Headquarter already exists with this Mobile no")
                elif user.objects.filter(email='admin'+str(hq_admin_email)).exists():
                    messages.error(request, "email already exists in usermaster")
                else:
                    headquarter_rlyObj = models.railwayLocationMaster.objects.get(rly_unit_code=hq_rly, location_type__in=['DIV','WS','O'])
                    import datetime
                    hqObj = models.AdminMaster(admin=hq_empno,admin_mobile=hq_admin_mob,admin_email=hq_admin_email,status=hq_status,designation=hq_desig,emp_name=hq_name,rly=headquarter_rlyObj,created_on=datetime.datetime.now())
                    
                    if hq_admin_phn:
                        hqObj.admin_phone = hq_admin_phn
                    
                    hqObj.save()
                    uname=models.AdminMaster.objects.filter(rly_id=headquarter_rlyObj.rly_unit_code).count()
                    cnt=('%03d' % uname)
                    val2=str(headquarter_rlyObj.rly_unit_code)+str(cnt)
                    val="admin "+headquarter_rlyObj.location_code
                    obj=models.AdminMaster.objects.filter(admin_email=hq_admin_email).update(user_id=val2)
                    hq_admin_email = 'admin'+str(hq_admin_email)
                    _password = "Admin@123"
                    if user.objects.filter(email=hq_admin_email):
                        obj=user.objects.get(email=hq_admin_email)
                        obj.is_admin=True
                        obj.username=val2
                        obj.first_name=hq_name
                        obj.user_role="admin_div"
                        obj.save()
                    else:
                        id=user.objects.filter().order_by('-id')[0].id
                        id+=1
                        user.objects.create_user(id=id,username=val2, is_active=True,password=_password,email=hq_admin_email,is_admin=True,user_role="admin_div")
                    messages.success(request, "Divison added succesfully with username- "+val2)
                return HttpResponseRedirect('/DivisonMaster')

        cursor = connection.cursor()
        id=request.user.username
        id=id[0:len(id)-3]
        code=models.railwayLocationMaster.objects.filter(rly_unit_code=id)[0].location_code
        desc=models.railwayLocationMaster.objects.filter(rly_unit_code=id)[0].location_description
        div=list(models.railwayLocationMaster.objects.filter(parent_location_code=code,location_type__in=['DIV','WS','O']).values('location_code','rly_unit_code').order_by('location_type','location_code'))
 
        cursor.execute("""SELECT hq.code, hq.address, hq.designation, hq.emp_name,hq.user_id, hq.admin, hq.admin_mobile, hq.admin_phone, hq.admin_email, hq.status, r.location_code, r.location_type FROM "myadmin_railwaylocationmaster" r ,"AdminMaster" hq where r.location_type in ('DIV','WS','O') and  hq.rly_id=r.rly_unit_code and r.parent_location_code=%s order by hq.code""",[code])
        data1=namedtuplefetchall(cursor)
        cursor.close()
        context={
        'headquarter': data1,
        'div':div,
        'desc':desc,

        }

        return render(request, "divison.html", context)
    # except Exception as e: 
    #     try:
    #         m1.error_Table.objects.create(fun_name="DivisonMaster",user_id=request.user,err_details=str(e))
    #     except:
    #         print("Internal Error!!!")
    #     return render(request, "myadmin_errors.html", {})

# def DivisonMaster(request):
#     # try:
#         if request.method == "POST":
#             hq_code = request.POST.get('divison_code')
#             hq_empno = request.POST.get('empno')
#             hq_name = request.POST.get('empname')
#             hq_desig = request.POST.get('designation')
#             hq_contact = request.POST.get('contact')
#             hq_admin_mob = request.POST.get('admin_mobile')
#             hq_admin_phn = str(request.POST.get('admin_phone'))
#             hq_admin_email = request.POST.get('admin_email')
#             hq_rly = request.POST.get('divison_rly')
#             hq_status = request.POST.get('divison_status')

#             if hq_code:
#                 try:
#                     headquarter_rlyObj = models.railwayLocationMaster.objects.get(location_code=hq_rly)
                  
#                     val="admin "+headquarter_rlyObj.location_code

#                     hqObj = models.AdminMaster.objects.get(pk=hq_code)
#                     userObj = user.objects.filter(username=hqObj.user_id)[0]
#                     try:
#                             hqObj.admin_mobile = hq_admin_mob
#                     except Exception as e:
#                         messages.error(
#                             request, "Can't Update mobile no, new mobile you entered already exists.")
#                         return HttpResponseRedirect('/DivisonMaster')

#                     try:
#                         if userObj.email != hq_admin_email:

#                                 email_body = f'''
#                                    Hello {hq_desig},
#                                    Your email for RKVY has been updated from {userObj.email} to {hq_admin_email}.
#                                    Sincerely,
#                                    RKVY Team
#                                 '''

#                                 try:
#                                     subject="Login Credentials for RKVY"
#                                     To=userObj.email
#                                     email_body1='<p>'+email_body+'</p>'
#                                     userObj.email = hq_admin_email
#                                     userObj.save()
#                                     hqObj.admin_email = hq_admin_email
#                                 except Exception as e:
#                                     messages.error(request, "Email failed.")
#                                     return HttpResponseRedirect('/DivisonMaster')

                            
#                     except Exception as e:
#                         messages.error(
#                             request, "Can't Update email, new email you entered already exists.")
#                         return HttpResponseRedirect('/DivisonMaster')
#                     hqObj.admin = hq_empno
#                     hqObj.emp_name = hq_name
#                     hqObj.designation = hq_desig
#                     if hq_admin_phn:
#                         hqObj.admin_phone = hq_admin_phn
#                     else:
#                         hqObj.admin_phone= '' 
#                     if hq_rly != "":
#                         hqObj.rly = models.railwayLocationMaster.objects.get(location_code=hq_rly)
#                     hqObj.headquarter_status = hq_status
#                     hqObj.save()

#                     messages.success(request, "Successfully Updated the Divison")
#                     return HttpResponseRedirect('/DivisonMaster')

#                 except Exception as e:
#                     messages.error(request, "Something went wrong.")
#                     return HttpResponseRedirect('/DivisonMaster')

#             else:
#                 # if models.AdminMaster.objects.filter(admin_email=hq_admin_email).exists():
#                 #     messages.error(request, "Headquarter already exists with this email")
#                 # elif models.AdminMaster.objects.filter(admin_mobile=hq_admin_mob).exists():
#                 #     messages.error(request, "Headquarter already exists with this Mobile no")
#                 # elif user.objects.filter(email=hq_admin_email).exists():
#                 #     messages.error(request, "email already exists in usermaster")
#                 if models.AdminMaster.objects.filter(admin_email=hq_admin_email).exists():
#                     messages.error(request, "Headquarter already exists with this email")
#                 elif models.AdminMaster.objects.filter(admin_mobile=hq_admin_mob).exists():
#                     messages.error(request, "Headquarter already exists with this Mobile no")
#                 elif user.objects.filter(email='admin'+str(hq_admin_email)).exists():
#                     messages.error(request, "email already exists in usermaster")
#                 else:
#                     headquarter_rlyObj = models.railwayLocationMaster.objects.get(location_code=hq_rly,location_type = 'DIV')
#                     import datetime
#                     hqObj = models.AdminMaster(admin=hq_empno,admin_mobile=hq_admin_mob,admin_email=hq_admin_email,status=hq_status,designation=hq_desig,emp_name=hq_name,rly=headquarter_rlyObj,created_on=datetime.datetime.now())
                    
#                     if hq_admin_phn:
#                         hqObj.admin_phone = hq_admin_phn
                    
#                     hqObj.save()
#                     uname=models.AdminMaster.objects.filter(rly_id=headquarter_rlyObj.rly_unit_code).count()
#                     cnt=('%03d' % uname)
#                     val2=str(headquarter_rlyObj.rly_unit_code)+str(cnt)
#                     val="admin "+headquarter_rlyObj.location_code
#                     obj=models.AdminMaster.objects.filter(admin_email=hq_admin_email).update(user_id=val2)
#                     hq_admin_email = 'admin'+str(hq_admin_email)
#                     _password = "Admin@123"
#                     if user.objects.filter(email=hq_admin_email):
#                         obj=user.objects.get(email=hq_admin_email)
#                         obj.is_admin=True
#                         obj.username=val2
#                         obj.first_name=hq_name
#                         obj.user_role="admin_div"
#                         obj.save()
#                     else:
#                         id=user.objects.filter().order_by('-id')[0].id
#                         id+=1
#                         user.objects.create_user(id=id,username=val2, is_active=True,password=_password,email=hq_admin_email,is_admin=True,user_role="admin_div")
#                     messages.success(request, "Divison added succesfully with username- "+val2)
#                 return HttpResponseRedirect('/DivisonMaster')

#         cursor = connection.cursor()
#         id=request.user.username
#         id=id[0:len(id)-3]
#         code=models.railwayLocationMaster.objects.filter(rly_unit_code=id)[0].location_code
#         desc=models.railwayLocationMaster.objects.filter(rly_unit_code=id)[0].location_description
#         div=list(models.railwayLocationMaster.objects.filter(parent_location_code=code,location_type__in=['DIV','WS','O']).values('location_code','rly_unit_code').order_by('location_type','location_code'))
 
#         cursor.execute("""SELECT hq.code, hq.address, hq.designation, hq.emp_name,hq.user_id, hq.admin, hq.admin_mobile, hq.admin_phone, hq.admin_email, hq.status, r.location_code, r.location_type FROM "myadmin_railwaylocationmaster" r ,"AdminMaster" hq where r.location_type='DIV' and  hq.rly_id=r.rly_unit_code and r.parent_location_code=%s order by hq.code""",[code])
#         data1=namedtuplefetchall(cursor)
      
#         context={
#         'headquarter': data1,
#         'div':div,
#         'desc':desc,

#         }

#         return render(request, "divison.html", context)
#     # except Exception as e: 
#     #     try:
#     #         m1.error_Table.objects.create(fun_name="DivisonMaster",user_id=request.user,err_details=str(e))
#     #     except:
#     #         print("Internal Error!!!")
#     #     return render(request, "myadmin_errors.html", {})


# def DivisonMaster(request):
#     try:
#         if request.method == "POST":
#             hq_code = request.POST.get('divison_code')
            
#             # print(',,,,,,,,,,,',hq_code)
#             # print('999999999999')
#             # hq_address = request.POST.get('divison_address')
#             # hq_pincode = request.POST.get('pincode')
#             # pincodeObj = models.locationMaster.objects.get(pk=hq_pincode)
#             # hq_admin = request.POST.get('divison_admin')
#             hq_empno = request.POST.get('empno')
#             hq_name = request.POST.get('empname')
#             hq_desig = request.POST.get('designation')
#             hq_contact = request.POST.get('contact')

#             hq_admin_mob = request.POST.get('admin_mobile')
#             # change25
#             hq_admin_phn = str(request.POST.get('admin_phone'))
#             hq_admin_email = request.POST.get('admin_email')
#             hq_rly = request.POST.get('divison_rly')
#             # print(hq_rly,'///////////////')
#             hq_status = request.POST.get('divison_status')

#             if hq_code:
#                 # update
#                 # print(hq_code,"ghedfvvvvvvvvvvvvvvvvvv")
#                 try:
#                     # print("yes")
#                     headquarter_rlyObj = models.railwayLocationMaster.objects.get(location_code=hq_rly)
#                     # print("yes")
#                     val="admin "+headquarter_rlyObj.location_code

#                     # # print('99999')
#                     # # print(hq_code)
#                     hqObj = models.AdminMaster.objects.get(pk=hq_code)
#                     userObj = user.objects.filter(username=hqObj.user_id)[0]
#                     # userObj = user.objects.filter(first_name=val)[0]
#                     # # print(userObj.official_mobileNo)
#                     # # print(hq_admin_mob)
#                     try:
#                         # if hq_admin_mob != userObj.official_mobileNo:
#                         #     userObj.official_mobileNo = hq_admin_mob
#                         #     userObj.save()
#                             hqObj.admin_mobile = hq_admin_mob

                                
                        
                            
                            

#                     except Exception as e:
#                         # print(e,'0088888888800000000000000')
#                         messages.error(
#                             request, "Can't Update mobile no, new mobile you entered already exists.")
#                         return HttpResponseRedirect('/DivisonMaster')

#                     try:
#                         # print('99999999999')
#                         if userObj.email != hq_admin_email:

#                                 email_body = f'''
#                                    Hello {hq_desig},
#                                    Your email for RKVY has been updated from {userObj.email} to {hq_admin_email}.
#                                    Sincerely,
#                                    RKVY Team
#                                 '''

#                                 try:
                                    
#                                     # send_mail("Login Credentials for RKVY", email_body, 'crisdlwproject@gmail.com',
#                                     #           [f'{userObj.email}'], fail_silently=False)

#                                     #saud faisal (28-08-2021) -----
#                                     subject="Login Credentials for RKVY"
#                                     To=userObj.email
#                                     email_body1='<p>'+email_body+'</p>'
#                                     # MailSend(subject,email_body1,To)
#                                     #end here

#                                     userObj.email = hq_admin_email
#                                     userObj.save()
#                                     hqObj.admin_email = hq_admin_email
#                                 except Exception as e:
#                                     # print(e)
#                                     messages.error(request, "Email failed.")
#                                     return HttpResponseRedirect('/DivisonMaster')

                            
#                     except Exception as e:
#                         # print(e,'0000000')
#                         messages.error(
#                             request, "Can't Update email, new email you entered already exists.")
#                         return HttpResponseRedirect('/DivisonMaster')

                    
#                     # hqObj.address = hq_address
#                     # hqObj.pincode = pincodeObj
#                     # hqObj.admin = hq_admin
#                     hqObj.admin = hq_empno
#                     hqObj.emp_name = hq_name
#                     hqObj.designation = hq_desig
#                     if hq_admin_phn:
#                         hqObj.admin_phone = hq_admin_phn
#                     # change25
#                     else:
#                         hqObj.admin_phone= '' 
#                     if hq_rly != "":
#                         hqObj.rly = models.railwayLocationMaster.objects.get(location_code=hq_rly)
#                     hqObj.headquarter_status = hq_status
#                     hqObj.save()

#                     messages.success(request, "Successfully Updated the Divison")
#                     return HttpResponseRedirect('/DivisonMaster')

#                 except Exception as e:
#                     # print(e)
#                     messages.error(request, "Something went wrong.")
#                     return HttpResponseRedirect('/DivisonMaster')

#             else:
#                 # create new
#                 # # print('9')
#                 # print(hq_rly,"let me check")


#                 # headquarter_rlyObj = models.railwayLocationMaster.objects.filter(location_code=hq_rly).values('rly_unit_code')[0]['rly_unit_code']
#                 headquarter_rlyObj = models.railwayLocationMaster.objects.get(location_code=hq_rly)
#                 # print(headquarter_rlyObj,"headquarter_rlyObj")
#                 # print(type(headquarter_rlyObj),"tyoe")
#                 import datetime
#                 hqObj = models.AdminMaster(admin=hq_empno,admin_mobile=hq_admin_mob,admin_email=hq_admin_email,status=hq_status,designation=hq_desig,emp_name=hq_name,rly=headquarter_rlyObj,created_on=datetime.datetime.now())
#                 # # print('00000000.')
#                 if hq_admin_phn:
#                     hqObj.admin_phone = hq_admin_phn
                
#                 try:
#                     hqObj.save()
#                     # # print('99')
#                     uname=models.AdminMaster.objects.filter(rly_id=headquarter_rlyObj.rly_unit_code).count()
#                     cnt=('%03d' % uname)
#                     val2=str(headquarter_rlyObj.rly_unit_code)+str(cnt)
#                     # # print(val2)
#                     val="admin "+headquarter_rlyObj.location_code
#                     obj=models.AdminMaster.objects.filter(admin_email=hq_admin_email).update(user_id=val2)

#                     _password = "Admin@123"
#                     if user.objects.filter(email=hq_admin_email):
#                         obj=user.objects.get(email=hq_admin_email)
#                         obj.is_admin=True
#                         # obj.username=headquarter_rlyObj.rly_unit_code
#                         obj.username=val2
#                         # obj.first_name=val
#                         obj.first_name=hq_name
#                         obj.user_role="admin_div"
#                         obj.save()
#                     else:
#                         # user.objects.create_user(username=val2, is_active=True,password=_password,email=hq_admin_email, first_name=val,is_admin=True,user_role="admin_div")
#                         id=user.objects.filter().order_by('-id')[0].id
#                         id+=1
#                         user.objects.create_user(id=id,username=val2, is_active=True,password=_password,email=hq_admin_email, first_name=hq_name,is_admin=True,user_role="admin_div")
#                     # userObj = models.AuthUser(email=hq_admin_email, password=_password,
#                     #                               first_name=hqObj.pk, last_name=str(hq_admin)[:30],username="admin"+"_"+hq_rly)
#                     # userObj.is_active = True
#                     # userObj.save()
#                     # email_context = {
                        
#                     #     'login_id': userObj.email,
#                     #     'password': _password,
#                     # }
#                     # email_template_name = "accounts/email_headquarter_credentials.txt"
#                     # email_body = render_to_string(
#                     #     email_template_name, email_context)
#                     # try:
#                     #     # send_mail("Login Credentials for RKVY", email_body, 'crisdlwproject@gmail.com',
#                     #     #           [f'{userObj.email}'], fail_silently=False)
                        
#                     # #saud faisal (28-08-2021) -----
#                     #     subject="Login Credentials for RKVY"
#                     #     To=userObj.email
#                     #     email_body1='<p>'+email_body+'</p>'
#                     #     MailSend(subject,email_body1,To)
#                     #     #end here
                        
#                     # except Exception as e:
#                     #     # print(e)
#                     #     userObj.delete()
#                     #     hqObj.delete()
#                     #     messages.error(request, "Email failed.")
#                     #     return HttpResponseRedirect('/rkvy_headquarterMaster')

#                 except Exception as e:
#                     # # print('lllll')


#                     # print(e,'999999999999999999999999999')
#                     messages.error(
#                         request, "Divison already exists with this email or mobile no.")
#                     return HttpResponseRedirect('/DivisonMaster')

#                 messages.success(request, "Divison added succesfully.")
#                 return HttpResponseRedirect('/DivisonMaster')

#         #changes 12-08 Ritika Garg
#         # headquarter = list(
#         #     models.rkvy_headquarterMaster.objects.all().order_by('headquarter_code'))

#         cursor = connection.cursor()
#         # cursor.execute("""SELECT hq.code, hq.address, hq.admin, hq.admin_mobile, hq.admin_phone, hq.admin_email, hq.status, r.location_code, hq.pincode_id, r.location_type, l.district, l.state FROM "myadmin_railwaylocationmaster" r ,"AdminMaster" hq, "locationMaster" l  where r.location_type='DIV' and status='Active' and hq.rly_id=r.rly_unit_code and hq.pincode_id=l.pincode order by hq.code""")
#         # cursor.execute("""SELECT hq.code, hq.address, hq.designation, hq.emp_name,hq.user_id, hq.admin, hq.admin_mobile, hq.admin_phone, hq.admin_email, hq.status, r.location_code, r.location_type FROM "myadmin_railwaylocationmaster" r ,"AdminMaster" hq where r.location_type='DIV' and  hq.rly_id=r.rly_unit_code order by hq.code""")
#         # data1=namedtuplefetchall(cursor)
#         id=request.user.username
#         id=id[0:len(id)-3]
#         # print(id)
#         code=models.railwayLocationMaster.objects.filter(rly_unit_code=id)[0].location_code
#         desc=models.railwayLocationMaster.objects.filter(rly_unit_code=id)[0].location_description
#         # print(desc)
#         # # print(data1)
#         div=list(models.railwayLocationMaster.objects.filter(parent_location_code=code,location_type='DIV').values('location_code','rly_unit_code'))
#         # print(div)
#         cursor.execute("""SELECT hq.code, hq.address, hq.designation, hq.emp_name,hq.user_id, hq.admin, hq.admin_mobile, hq.admin_phone, hq.admin_email, hq.status, r.location_code, r.location_type FROM "myadmin_railwaylocationmaster" r ,"AdminMaster" hq where r.location_type='DIV' and  hq.rly_id=r.rly_unit_code and r.parent_location_code=%s order by hq.code""",[code])
#         data1=namedtuplefetchall(cursor)
#         # # print(div)
#         context={
#         'headquarter': data1,
#         'div':div,
#         'desc':desc,

#         }

#         return render(request, "divison.html", context)
#     except Exception as e: 
#         try:
#             m1.error_Table.objects.create(fun_name="DivisonMaster",user_id=request.user,err_details=str(e))
#         except:
#             print("Internal Error!!!")
#         return render(request, "myadmin_errors.html", {})

def editDivison(request):
    try:
        if request.method == "POST":
            # print('sssssssssssss')
            # # print(request.POST.get("id"))
            _id = int(request.POST.get("id"))
            # print(_id)

            divisonData = models.AdminMaster.objects.filter(pk=_id)
            # print(divisonData)
            # city =divisonData[0].pincode.district
            # state = divisonData[0].pincode.state
            location = divisonData[0].rly.location_description
            # print(location)
            divisonData = list(divisonData.values())
            # print(divisonData)
            
            divisonData[0]['divison_rly'] = location
            # print(divisonData)
            # divisonData[0]['headquarter_rly'] = location
            # divisonData = list(divisonData.values())
            ## print(headquarterData)
            # divisonData[0]['divison_city'] = city
            # divisonData[0]['divison_state'] = state
            # divisonData[0]['divison_rly'] = location
            # # # print(divisonData)
            return JsonResponse(
                {
                    "status": 1,
                    "divisonData": divisonData,
                }
            )
        return JsonResponse(
            {
                "status": 0,
            }
        )
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="editDivison",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})



def deleteDivison (request):
    try:
        if request.method == "POST":
            # # print('1')
            _id = int(request.POST.get("id"))
            # # print(_id)
            obj = (models.AdminMaster.objects.filter(code=_id))[0]
            email=request.POST.get("admin_email")

            ## print(obj)
            if obj.status=="InActive":
                obj.status="Active"
                obj.save()
                obj = user.objects.filter(email=email).update(is_admin=True)
            elif obj.status=="Active":
                obj.status="InActive"
                obj.save()
                obj = user.objects.filter(email=email).update(is_admin=False)

            # obj = user.objects.filter(email=email).update(is_admin=False)

            return JsonResponse({
                "status": 1,
            }
            )
        return JsonResponse(
            {
                "status": 0,
            }
        )
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="deleteDivison",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "myadmin_errors.html", {})






# def user_list(request):
#     # try:
#         usermast=m1.MyUser.objects.filter(email=request.user).first()
#         rolelist=usermast.user_role
#         if str(request.user).startswith('admin'):
#             actual_user = str(request.user).split('admin')[1]
#         else:
#             actual_user = request.user
#         empnox = AdminMaster.objects.filter(Q(admin_email=actual_user), user_id__isnull=False).values('rly','user_id')
#         #empnox = AdminMaster.objects.filter(Q(admin_email='admin'+str(request.user)) | Q(admin_email='admin'+str(request.user.email)), user_id__isnull=False).values('rly','user_id')
        
#         rly_unit_id=None
#         cuser = None
#         parent_rly = []
#         if empnox:
#             rly_unit_id = empnox[0]['rly']
#             cuser = empnox[0]['user_id']
#             child_rly = list(railwayLocationMaster.objects.filter( parent_rly_unit_code  = str(rly_unit_id)).values('rly_unit_code'))
#             if len(child_rly)>0:
#                 child_rly = list(map(lambda x: x['rly_unit_code'], child_rly))
           

#         if request.method == 'POST' and request.is_ajax():
#             post_type = request.POST.get('post_type') 
#             if post_type == 'reject':
#                 reqno = request.POST.get('reqno')
#                 remarks = request.POST.get('remarks')
#                 posting_History.objects.filter(history_id=reqno).update(accepted_remarks=remarks,accepted_date=datetime.now(), forwarded_to=cuser, status = 'Rejected')
#                 msg = 'Successfuly Rejected'
#                 return JsonResponse(msg, safe = False) 
#             if post_type == 'accept':
#                 reqno = request.POST.get('reqno')
#                 remarks = request.POST.get('remarks')
#                 posting_History.objects.filter(history_id=reqno).update(accepted_remarks=remarks,accepted_date=datetime.now(), forwarded_to=cuser, status = 'Accepted')

#                 data = list(posting_History.objects.filter(history_id=reqno).values())
#                 prev_details =list(models.Level_Desig.objects.filter(designation = data[0]['current_desigination']).values())

#                 models.Level_Desig.objects.filter(designation = data[0]['current_desigination']).update(modified_by=cuser,empno_id = data[0]['empno_id'], department_code_id = data[0]['current_department_code_id'],parent_desig_code = data[0]['current_parent_desig_code'],rly_unit_id=data[0]['current_rly_unit_id'],status='P',contactnumber=data[0]['current_contactnumber'],official_email_ID=data[0]['current_official_email_ID'],station_name=data[0]['current_station_name'])
#                 password = 'Admin@123'

                
#                 if m1.MyUser.objects.filter(id = prev_details[0]['desig_user_id']).exists():
#                     forgetuser=m1.MyUser.objects.filter(id = prev_details[0]['desig_user_id']).first()
#                     if forgetuser:
#                         forgetuser.set_password(password)
#                         forgetuser.save()
#                         m1.MyUser.objects.filter(username=data[0]['current_official_email_ID']).update(username=None,is_active= False,email = None)
#                         m1.MyUser.objects.filter(id = prev_details[0]['desig_user_id']).update(username=data[0]['current_official_email_ID'],is_active= True,email = data[0]['current_official_email_ID'])
#                 else:
#                     id = list(m1.MyUser.objects.values('id').order_by('-id'))
#                     if len(id)>0:
#                         id = id[0]['id'] + 1
#                     else:
#                         id = 1
#                     newuser = m1.MyUser.objects.create_user(id = id,username=data[0]['current_official_email_ID'], password=password,email=data[0]['current_official_email_ID'],user_role='user')
#                     newuser.is_active= True
#                     newuser.is_admin=False
#                     newuser.save()
#                     myuser_id = list(m1.MyUser.objects.filter(email = data[0]['current_official_email_ID']).values('id'))
#                     if len(myuser_id)>0:
#                         models.Level_Desig.objects.filter(designation = data[0]['current_desigination']).update(desig_user_id = myuser_id[0]['id'])
                
#                 data1 = list(models.Level_Desig.objects.filter(empno_id = data[0]['empno_id'],designation = data[0]['prev_desigination']).values('official_email_ID'))
#                 if len(data1)>0:
#                     models.Level_Desig.objects.filter(empno = data[0]['empno_id'],designation = data[0]['prev_desigination']).update(empno = None, status = 'P')
#                     newuser = m1.MyUser.objects.filter(email=data1[0]['official_email_ID']).update(is_active= False)

#                 msg = 'Successfuly Accepted'
#                 return JsonResponse(msg, safe = False) 
#             if post_type == 'request_to_me':
#                 reqno = request.POST.get('reqno')
#                 p_reporting_officer = ''
#                 c_reporting_officer = ''
#                 emp_details = list(posting_History.objects.filter( history_id = reqno ).values('history_id','done_by',
#                     'empno_id' ,'prev_desigination','prev_parent_desig_code','prev_department_code_id__department_name','prev_rly_unit_id__location_code','prev_rly_unit_id__location_type','prev_contactnumber','prev_official_email_ID','prev_station_name',
#                     'current_desigination','current_parent_desig_code','current_department_code_id__department_name','current_rly_unit_id__location_code','current_rly_unit_id__location_type','current_contactnumber','current_official_email_ID','current_station_name',
#                     'empno_id__empname','empno_id__empmname','empno_id__emplname'
#                 ))
#                 if len(emp_details) > 0: 
#                     reporting_officer = list(models.Level_Desig.objects.filter(designation_code = emp_details[0]['prev_parent_desig_code']).values('designation'))
#                     if len(reporting_officer) > 0:
#                         p_reporting_officer = reporting_officer[0]['designation']
#                     else:
#                         p_reporting_officer = ''
#                     reporting_officer = list(models.Level_Desig.objects.filter(designation_code = emp_details[0]['current_parent_desig_code']).values('designation'))
#                     if len(reporting_officer) > 0:
#                         c_reporting_officer = reporting_officer[0]['designation']
#                     else:
#                         c_reporting_officer = ''
                
#                 context ={
#                     'emp_details':emp_details,
#                     'p_reporting_officer':p_reporting_officer,
#                     'c_reporting_officer':c_reporting_officer,
#                 }
                
#                 return JsonResponse(context, safe = False) 
#             if post_type == 'emp_details':
#                 empno = request.POST.get('empno')
#                 designation = request.POST.get('designation')
#                 reporting_officer = ''
#                 emp_details = list(models.Level_Desig.objects.filter(empno_id = empno, designation = designation).values('designation','rly_unit_id__location_code','rly_unit_id__location_type','empno_id','empno_id__empname','empno_id__empmname','empno_id__emplname','contactnumber','official_email_ID','department_code__department_name','station_name','empno_id__hrms_id_id','parent_desig_code','status').order_by('-status','designation'))
#                 if len(emp_details) > 0: 
#                     reporting_officer = list(models.Level_Desig.objects.filter(designation_code = emp_details[0]['parent_desig_code']).values('designation'))
#                     if len(reporting_officer) > 0:
#                         reporting_officer = reporting_officer[0]['designation']
#                     else:
#                         reporting_officer = ''
                
#                 context ={
#                     'emp_details':emp_details,
#                     'reporting_officer':reporting_officer,
#                 }
#                 return JsonResponse(context, safe = False)  
            
#             if post_type == 'emp_release':
#                 empno = request.POST.get('empno')
#                 charge_type = request.POST.get('charge_type')  
#                 designation = request.POST.get('designation')
#                 data = list(models.Level_Desig.objects.filter(empno_id = empno,designation = designation).values('official_email_ID'))
#                 msg = 'Operation Failed'
#                 if len(data)>0:
#                     models.Level_Desig.objects.filter(empno = empno,designation = designation).update(empno = None, status = 'P',modified_by=cuser)
#                     newuser = m1.MyUser.objects.filter(email=data[0]['official_email_ID']).update(is_active= False)
                    
#                     msg = 'Successfully relinquished'
#                 return JsonResponse(msg, safe = False)
#             if post_type == 'new_emp':
#                 empno = request.POST.get('empno')
#                 emp_no_details = list(m1.empmast.objects.filter(empno = empno).values())
#                 lev_desig_details = list(models.Level_Desig.objects.filter(empno_id = empno).values('designation','parent_desig_code','department_code__department_name','rly_unit_id__location_type','rly_unit_id__location_code','status','official_email_ID','contactnumber','station_name').order_by('-status'))
#                 if len(lev_desig_details) > 0: 
#                     for i in range(len(lev_desig_details)):
#                         reporting_officer = list(models.Level_Desig.objects.filter(designation_code = lev_desig_details[i]['parent_desig_code']).values('designation'))
#                         if len(reporting_officer) > 0:
#                             reporting_officer = reporting_officer[0]['designation']
#                         else:
#                             reporting_officer = ''
#                         lev_desig_details[i].update({'reporting_officer':reporting_officer})
#                 response = {
#                     'emp_no_details' : emp_no_details,
#                     'lev_desig_details' : lev_desig_details,
#                 }
#                 return JsonResponse(response, safe = False)
#             if post_type == 'desig_search':
#                 designation = request.POST.get('designation')
#                 lev_desig_details = list(models.Level_Desig.objects.filter(designation = designation).values('parent_desig_code','department_code','rly_unit_id','official_email_ID','contactnumber','station_name').order_by('status'))
#                 if len(lev_desig_details) > 0: 
#                     for i in range(len(lev_desig_details)):
#                         reporting_officer = ''
#                         if lev_desig_details[i]['parent_desig_code'] is not None:
#                             reporting_officer = list(models.Level_Desig.objects.filter(designation_code = lev_desig_details[i]['parent_desig_code']).values('designation'))
#                             if len(reporting_officer) > 0:
#                                 reporting_officer = reporting_officer[i]['designation']
#                             else:
#                                 reporting_officer = ''
#                         lev_desig_details[i].update({'reporting_officer':reporting_officer})
                    
#                     rly_unit_id = lev_desig_details[i]['rly_unit_id']
#                     rly_unit_det=list(railwayLocationMaster.objects.filter( rly_unit_code= rly_unit_id).values('parent_rly_unit_code'))
#                     rly_unit_det = list(map( lambda x: int(x['parent_rly_unit_code']),rly_unit_det))
#                     rep_officer = list(models.Level_Desig.objects.filter(Q(rly_unit = rly_unit_id) | Q(rly_unit__in = rly_unit_det)).values('designation'))
#                     rep_officer = list(map( lambda x: x['designation'],rep_officer))
#                     all_station = list(models.station_master.objects.filter(Q(rly_id_id = rly_unit_id) | Q(div_id_id = rly_unit_id)).values('station_name').distinct().order_by('station_name'))
#                     if lev_desig_details[0]['station_name'] is not None:
#                         all_station.append({'station_name':lev_desig_details[0]['station_name']})
                
#                 context = {
#                     'lev_desig_details' : lev_desig_details,
#                     'rep_officer':rep_officer,
#                     'all_station':all_station,
#                 }
#                 return JsonResponse(context, safe = False)
            
#             if post_type == 'new_joining':
#                 empno = request.POST.get('empno')
#                 txt_new_joining_designation = request.POST.get('txt_new_joining_designation')
#                 charge_type_new_joining = request.POST.get('charge_type_new_joining')
#                 department_new_joining = request.POST.get('department_new_joining')
#                 place_new_joining = request.POST.get('place_new_joining')
#                 reporting_officer_new_joining = request.POST.get('reporting_officer_new_joining')
#                 if reporting_officer_new_joining == '':
#                     reporting_officer_new_joining = None
#                 else:
#                     dt1 = list(models.Level_Desig.objects.filter(designation = reporting_officer_new_joining).values('designation_code'))
#                     reporting_officer_new_joining = dt1[0]['designation_code']
#                 contact_new_joining = request.POST.get('contact_new_joining')
#                 email_new_joining = request.POST.get('email_new_joining')
#                 station_new_joining = request.POST.get('station_new_joining')
#                 remarks_new_joining = request.POST.get('remarks_new_joining')
#                 msg = 'Not changed, please contact admin'
#                 password = 'Admin@123'
#                 if charge_type_new_joining == 'D':
#                     if models.Level_Desig.objects.filter(~Q(designation = txt_new_joining_designation), official_email_ID=email_new_joining).exists():
#                         msg = 'e-mail id is already used with another designation, Request cannot be processed'
#                     elif models.Level_Desig.objects.filter(designation = txt_new_joining_designation, empno = empno , status = 'D').exists():
#                         msg = 'Same user is already Exists as Dual charge for the same post'
#                     else:
#                         posting_History.objects.create(empno_id = empno,done_by = cuser,current_desigination = txt_new_joining_designation,current_parent_desig_code= reporting_officer_new_joining,current_department_code_id=department_new_joining,current_rly_unit_id=place_new_joining,
#                         current_contactnumber=contact_new_joining,current_official_email_ID=email_new_joining,current_station_name=station_new_joining,charge_type=charge_type_new_joining,created_date=datetime.now(),accepted_date=datetime.now(),status='Accepted',created_remarks=remarks_new_joining)
#                         prev_details =list(models.Level_Desig.objects.filter(designation = txt_new_joining_designation).values())
#                         models.Level_Desig.objects.filter(designation = txt_new_joining_designation).update(modified_by=cuser,empno_id = empno, department_code_id = department_new_joining,parent_desig_code = reporting_officer_new_joining,rly_unit_id=place_new_joining,status=charge_type_new_joining,contactnumber=contact_new_joining,official_email_ID=email_new_joining,station_name=station_new_joining)
#                         if m1.MyUser.objects.filter(id = prev_details[0]['desig_user_id']).exists():
#                             forgetuser=m1.MyUser.objects.filter(id = prev_details[0]['desig_user_id']).first()
#                             if forgetuser:
#                                 forgetuser.set_password(password)
#                                 forgetuser.save()
#                                 m1.MyUser.objects.filter(username=email_new_joining).update(username=None,is_active= False,email = None)
#                                 m1.MyUser.objects.filter(id = prev_details[0]['desig_user_id']).update(username=email_new_joining,is_active= True,email = email_new_joining)
#                         else:
#                             id = list(m1.MyUser.objects.values('id').order_by('-id'))
#                             if len(id)>0:
#                                 id = id[0]['id'] + 1
#                             else:
#                                 id = 1
#                             newuser = m1.MyUser.objects.create_user(id = id,username=email_new_joining, password=password,email=email_new_joining,user_role='user')
#                             newuser.is_active= True
#                             newuser.is_admin=False
#                             newuser.save()
#                             myuser_id = list(m1.MyUser.objects.filter(email = email_new_joining).values('id'))
#                             if len(myuser_id)>0:
#                                 models.Level_Desig.objects.filter(designation = txt_new_joining_designation).update(desig_user_id = myuser_id[0]['id'])
#                         msg = 'Dual charge is created successfully'
                
#                 if charge_type_new_joining == 'P':
#                     if str(request.user).startswith('admin'):
#                         actual_user = str(request.user).split('admin')[1]
#                     else:
#                         actual_user = request.user
#                     empnox_det = AdminMaster.objects.filter(Q(admin_email=actual_user), user_id__isnull=False).values('rly','user_id')
#                     #empnox_det = AdminMaster.objects.filter(Q(admin_email='admin'+str(request.user)) | Q(admin_email='admin'+str(request.user.email)), user_id__isnull=False).values('rly','user_id')
#                     rly_unit_id_det=None
#                     cuser_det = None
#                     if empnox_det:
#                         rly_unit_id_det = empnox_det[0]['rly']
#                         cuser_det = empnox_det[0]['user_id']
#                     if models.Level_Desig.objects.filter(~Q(designation = txt_new_joining_designation), official_email_ID=email_new_joining).exists():
#                         msg = 'e-mail id is already used with another designation, Request cannot be processed'

#                     elif models.Level_Desig.objects.filter(designation = txt_new_joining_designation, empno = empno , status = 'P').exists():
#                         msg = 'Same user is already Exists as Primary charge for the same post'

#                     elif models.Level_Desig.objects.filter(empno = empno , status = 'P', rly_unit = rly_unit_id_det).exists():
#                         prev_details =list(models.Level_Desig.objects.filter(empno = empno , status = 'P', rly_unit = rly_unit_id_det).values())
                
#                         if len(prev_details)>0:
#                             models.Level_Desig.objects.filter(empno_id = empno,designation = prev_details[0]['designation']).update(modified_by=cuser_det,empno_id = None, status = 'P')
#                             m1.MyUser.objects.filter(email=prev_details[0]['official_email_ID']).update(is_active= False)
                           
                        
#                         posting_History.objects.create(empno_id = empno,done_by = cuser,current_desigination = txt_new_joining_designation,current_parent_desig_code= reporting_officer_new_joining,current_department_code_id=department_new_joining,current_rly_unit_id=place_new_joining,
#                         prev_desigination=prev_details[0]['designation'],prev_parent_desig_code=prev_details[0]['parent_desig_code'],prev_department_code_id=prev_details[0]['department_code_id'],prev_rly_unit_id=prev_details[0]['rly_unit_id'],prev_contactnumber=prev_details[0]['contactnumber'],prev_official_email_ID=prev_details[0]['official_email_ID'],prev_station_name=prev_details[0]['station_name'],
#                         current_contactnumber=contact_new_joining,current_official_email_ID=email_new_joining,current_station_name=station_new_joining,charge_type=charge_type_new_joining,created_date=datetime.now(),accepted_date=datetime.now(),status='Accepted',created_remarks=remarks_new_joining)
                        
#                         models.Level_Desig.objects.filter(designation = txt_new_joining_designation).update(modified_by=cuser_det,empno_id = empno, department_code_id = department_new_joining,parent_desig_code = reporting_officer_new_joining,rly_unit_id=place_new_joining,status=charge_type_new_joining,contactnumber=contact_new_joining,official_email_ID=email_new_joining,station_name=station_new_joining)
#                         if m1.MyUser.objects.filter(id = prev_details[0]['desig_user_id']).exists():
#                             forgetuser=m1.MyUser.objects.filter(id = prev_details[0]['desig_user_id']).first()
#                             if forgetuser:
#                                 forgetuser.set_password(password)
#                                 forgetuser.save()
#                                 m1.MyUser.objects.filter(username=email_new_joining).update(username=None,is_active= False,email = None)
#                                 m1.MyUser.objects.filter(id = prev_details[0]['desig_user_id']).update(username=email_new_joining,is_active= True,email = email_new_joining)
#                         else:
#                             id = list(m1.MyUser.objects.values('id').order_by('-id'))
#                             if len(id)>0:
#                                 id = id[0]['id'] + 1
#                             else:
#                                 id = 1
#                             newuser = m1.MyUser.objects.create_user(id = id,username=email_new_joining, password=password,email=email_new_joining,user_role='user')
#                             newuser.is_active= True
#                             newuser.is_admin=False
#                             newuser.save()
#                             myuser_id = list(m1.MyUser.objects.filter(email = email_new_joining).values('id'))
#                             if len(myuser_id)>0:
#                                 models.Level_Desig.objects.filter(designation = txt_new_joining_designation).update(desig_user_id = myuser_id[0]['id'])
#                         msg = 'Primary charge is updated successfully'

#                     elif models.Level_Desig.objects.filter(empno = empno , status = 'P').exists():
#                         prev_details =list(models.Level_Desig.objects.filter(empno = empno , status = 'P').values())
#                         if posting_History.objects.filter(done_by = cuser,status='Forwarded',empno = empno).exists():
#                             msg = f"request already exists for the employee, To request again pull back the previous request"
#                         else:
#                             posting_History.objects.create(empno_id = empno,done_by = cuser,current_desigination = txt_new_joining_designation,current_parent_desig_code= reporting_officer_new_joining,current_department_code_id=department_new_joining,current_rly_unit_id=place_new_joining,
#                             prev_desigination=prev_details[0]['designation'],prev_parent_desig_code=prev_details[0]['parent_desig_code'],prev_department_code_id=prev_details[0]['department_code_id'],prev_rly_unit_id=prev_details[0]['rly_unit_id'],prev_contactnumber=prev_details[0]['contactnumber'],prev_official_email_ID=prev_details[0]['official_email_ID'],prev_station_name=prev_details[0]['station_name'],
#                             current_contactnumber=contact_new_joining,current_official_email_ID=email_new_joining,current_station_name=station_new_joining,charge_type=charge_type_new_joining,created_date=datetime.now(),status='Forwarded',created_remarks=remarks_new_joining)
#                             prev_details =list(models.Level_Desig.objects.filter(empno = empno , status = 'P').values('rly_unit__location_code'))
#                             msg = f"Request sent to {prev_details[0]['rly_unit__location_code']} for relinquished, once accepted primary charge will be updated"
                    
#                     else:
#                         posting_History.objects.create(empno_id = empno,done_by = cuser,current_desigination = txt_new_joining_designation,current_parent_desig_code= reporting_officer_new_joining,current_department_code_id=department_new_joining,current_rly_unit_id=place_new_joining,
#                         current_contactnumber=contact_new_joining,current_official_email_ID=email_new_joining,current_station_name=station_new_joining,charge_type=charge_type_new_joining,created_date=datetime.now(),accepted_date=datetime.now(),status='Accepted',created_remarks=remarks_new_joining)
#                         prev_details =list(models.Level_Desig.objects.filter(designation = txt_new_joining_designation).values())
#                         models.Level_Desig.objects.filter(designation = txt_new_joining_designation).update(modified_by=cuser_det,empno_id = empno, department_code_id = department_new_joining,parent_desig_code = reporting_officer_new_joining,rly_unit_id=place_new_joining,status=charge_type_new_joining,contactnumber=contact_new_joining,official_email_ID=email_new_joining,station_name=station_new_joining)
#                         if m1.MyUser.objects.filter(id = prev_details[0]['desig_user_id']).exists():
#                             forgetuser=m1.MyUser.objects.filter(id = prev_details[0]['desig_user_id']).first()
#                             if forgetuser:
#                                 forgetuser.set_password(password)
#                                 forgetuser.save()
#                                 m1.MyUser.objects.filter(username=email_new_joining).update(username=None,is_active= False,email = None)
#                                 m1.MyUser.objects.filter(id = prev_details[0]['desig_user_id']).update(username=email_new_joining,is_active= True,email = email_new_joining)
#                         else:
#                             id = list(m1.MyUser.objects.values('id').order_by('-id'))
#                             if len(id)>0:
#                                 id = id[0]['id'] + 1
#                             else:
#                                 id = 1
#                             newuser = m1.MyUser.objects.create_user(id = id,username=email_new_joining, password=password,email=email_new_joining,user_role='user')
#                             newuser.is_active= True
#                             newuser.is_admin=False
#                             newuser.save()
#                             myuser_id = list(m1.MyUser.objects.filter(email = email_new_joining).values('id'))
#                             if len(myuser_id)>0:
#                                 models.Level_Desig.objects.filter(designation = txt_new_joining_designation).update(desig_user_id = myuser_id[0]['id'])
#                         msg = 'Primary charge is created successfully'
#                 return JsonResponse(msg, safe = False)
            
#             if post_type == 'history':
#                 history_id = request.POST.get('history_id')
#                 history_data = list(posting_History.objects.filter(history_id=history_id).values())
#                 admin_1 = list(posting_History.objects.filter(history_id=history_id).values('current_rly_unit__location_code'))
#                 if len(admin_1)>0:
#                     admin_1 = 'Admin ' + str(admin_1[0]['current_rly_unit__location_code'])
#                 else:
#                     admin_1 = 'Admin'
#                 pending = []
#                 if history_data[0]['prev_rly_unit_id']  is not None:
#                     for i in range(len(history_data)):
#                         prev_rly_unit = history_data[i]['prev_rly_unit_id']
#                         if rly_unit_id == prev_rly_unit:
#                             if AdminMaster.objects.filter(status='Active',rly = prev_rly_unit).exists():
#                                 dt_list=list(AdminMaster.objects.filter(status='Active',rly = prev_rly_unit).values())
#                                 pending.extend(dt_list)
                        
#                         elif prev_rly_unit in child_rly:
#                             if AdminMaster.objects.filter(status='Active',rly = prev_rly_unit).exists():
#                                 dt_list=list(AdminMaster.objects.filter(status='Active',rly = prev_rly_unit).values())
#                                 pending.extend(dt_list)
#                     if len(pending) == 0:
#                         dt_list=list(AdminMaster.objects.filter(status='Active',user_id = '111111').values())
#                         pending.extend(dt_list)
                

#                 context = {
#                     'history_data':history_data,
#                     'pending':pending,
#                     'admin_1':admin_1,
#                 }
#                 # print(admin_1)
#                 return JsonResponse(context, safe = False) 
            
#             if post_type == 'pullback':
#                 history_id = request.POST.get('history_id')
#                 posting_History.objects.filter(history_id=history_id).delete()
#                 msg = 'Successfuly Pulled Back'
#                 return JsonResponse(msg, safe = False) 
            
#             if post_type == 'station':
#                 val = request.POST.get('val')
#                 all_station = list(models.station_master.objects.filter(Q(rly_id_id = val) | Q(div_id_id = val)).values('station_name').distinct().order_by('station_name'))
#                 return JsonResponse(all_station, safe = False) 
#             return JsonResponse({"success":False}, status=400)
        
#         details_data = list(models.Level_Desig.objects.filter((Q(rly_unit = rly_unit_id) | Q(rly_unit__in=railwayLocationMaster.objects.filter(parent_rly_unit_code = str(rly_unit_id)).values('rly_unit_code')))).values('designation','rly_unit_id__location_code','rly_unit_id__location_type','empno_id','empno_id__empname','empno_id__empmname','empno_id__emplname','contactnumber','official_email_ID').order_by('designation'))
#         rly_emp_designation = list(map(lambda x: x['designation'],details_data))
#         new_emp_no = list(m1.empmast.objects.values('empno','hrms_id' , 'empname', 'empmname', 'emplname').order_by('empname'))
#         all_department = list(models.departMast.objects.filter(delete_flag = False).values('department_code','department_name').order_by('department_name'))
#         all_railway = list(railwayLocationMaster.objects.filter((Q(parent_rly_unit_code = str(rly_unit_id)) | Q(rly_unit_code = rly_unit_id)),location_type__in =['RDSO','WS','DIV','RB','ZR','PSU','CTI','PU']).values('rly_unit_code','location_description','location_code','location_type').distinct().order_by('location_code'))
#         all_station = list(models.station_master.objects.filter(Q(rly_id_id = rly_unit_id) | Q(div_id_id = rly_unit_id)).values('station_name').distinct().order_by('station_name'))
#         requested = posting_History.objects.filter(done_by = cuser).all().order_by('-created_date')
#         pending = []
#         pending11 = list(posting_History.objects.filter(status='Forwarded').values().order_by('-created_date'))
        
#         if rolelist == 'admin_super':
#             for i in range(len(pending11)):
#                 pending.append(pending11[i])
#         else:
#             for i in range(len(pending11)):
#                 prev_rly_unit = pending11[i]['prev_rly_unit_id']
#                 if rly_unit_id == prev_rly_unit:
#                     if AdminMaster.objects.filter(status='Active',rly = prev_rly_unit).exists():
#                         pending.append(pending11[i])
                
#                 elif prev_rly_unit in child_rly:
#                     if AdminMaster.objects.filter(status='Active',rly = prev_rly_unit).exists():
#                         pending.append(pending11[i])

#         context ={
#             'details_data' : details_data,
#             'new_emp_no' : new_emp_no,
#             'rly_emp_designation' : rly_emp_designation,
#             'all_department':all_department,
#             'all_railway' : all_railway,
#             'all_station' : all_station,
#             'requested' : requested,
#             'pending':pending,

#         }
#         return render(request, "user_list.html", context)
    
#     # except Exception as e: 
#     #     try:
#     #         m1.error_Table.objects.create(fun_name="user_list",user_id=request.user,err_details=str(e))
#     #     except:
#     #         print("Internal Error!!!")
#     #     return render(request, "myadmin_errors.html", {})


def user_list(request):
    # try:
        usermast=m1.MyUser.objects.filter(email=request.user).first()
        rolelist=usermast.user_role
        if str(request.user).startswith('admin'):
            actual_user = str(request.user).split('admin')[1]
        else:
            actual_user = request.user
        empnox = AdminMaster.objects.filter(Q(admin_email=actual_user), user_id__isnull=False).values('rly','user_id')
        #empnox = AdminMaster.objects.filter(Q(admin_email='admin'+str(request.user)) | Q(admin_email='admin'+str(request.user.email)), user_id__isnull=False).values('rly','user_id')
        
        rly_unit_id=None
        cuser = None
        parent_rly = []
        if empnox:
            rly_unit_id = empnox[0]['rly']
            cuser = empnox[0]['user_id']
            child_rly = list(railwayLocationMaster.objects.filter( parent_rly_unit_code  = str(rly_unit_id)).values('rly_unit_code'))
            if len(child_rly)>0:
                child_rly = list(map(lambda x: x['rly_unit_code'], child_rly))
           

        if request.method == 'POST' and request.is_ajax():
            post_type = request.POST.get('post_type') 
            if post_type == 'reject':
                reqno = request.POST.get('reqno')
                remarks = request.POST.get('remarks')
                posting_History.objects.filter(history_id=reqno).update(accepted_remarks=remarks,accepted_date=datetime.now(), forwarded_to=cuser, status = 'Rejected')
                msg = 'Successfuly Rejected'
                return JsonResponse(msg, safe = False) 
            if post_type == 'accept':
                reqno = request.POST.get('reqno')
                remarks = request.POST.get('remarks')
                posting_History.objects.filter(history_id=reqno).update(accepted_remarks=remarks,accepted_date=datetime.now(), forwarded_to=cuser, status = 'Accepted')

                data = list(posting_History.objects.filter(history_id=reqno).values())
                prev_details =list(models.Level_Desig.objects.filter(designation = data[0]['current_desigination']).values())

                models.Level_Desig.objects.filter(designation = data[0]['current_desigination']).update(modified_by=cuser,empno_id = data[0]['empno_id'], department_code_id = data[0]['current_department_code_id'],parent_desig_code = data[0]['current_parent_desig_code'],rly_unit_id=data[0]['current_rly_unit_id'],status='P',contactnumber=data[0]['current_contactnumber'],official_email_ID=data[0]['current_official_email_ID'],station_name=data[0]['current_station_name'])
                password = 'Admin@123'

                
                if m1.MyUser.objects.filter(id = prev_details[0]['desig_user_id']).exists():
                    forgetuser=m1.MyUser.objects.filter(id = prev_details[0]['desig_user_id']).first()
                    if forgetuser:
                        forgetuser.set_password(password)
                        forgetuser.save()
                        m1.MyUser.objects.filter(username=data[0]['current_official_email_ID']).update(username=None,is_active= False,email = None)
                        m1.MyUser.objects.filter(id = prev_details[0]['desig_user_id']).update(username=data[0]['current_official_email_ID'],is_active= True,email = data[0]['current_official_email_ID'])
                else:
                    id = list(m1.MyUser.objects.values('id').order_by('-id'))
                    if len(id)>0:
                        id = id[0]['id'] + 1
                    else:
                        id = 1
                    newuser = m1.MyUser.objects.create_user(id = id,username=data[0]['current_official_email_ID'], password=password,email=data[0]['current_official_email_ID'],user_role='user')
                    newuser.is_active= True
                    newuser.is_admin=False
                    newuser.save()
                    myuser_id = list(m1.MyUser.objects.filter(email = data[0]['current_official_email_ID']).values('id'))
                    if len(myuser_id)>0:
                        models.Level_Desig.objects.filter(designation = data[0]['current_desigination']).update(desig_user_id = myuser_id[0]['id'])
                
                data1 = list(models.Level_Desig.objects.filter(empno_id = data[0]['empno_id'],designation = data[0]['prev_desigination']).values('official_email_ID'))
                if len(data1)>0:
                    models.Level_Desig.objects.filter(empno = data[0]['empno_id'],designation = data[0]['prev_desigination']).update(empno = None, status = 'P')
                    newuser = m1.MyUser.objects.filter(email=data1[0]['official_email_ID']).update(is_active= False)

                msg = 'Successfuly Accepted'
                return JsonResponse(msg, safe = False) 
            if post_type == 'request_to_me':
                reqno = request.POST.get('reqno')
                p_reporting_officer = ''
                c_reporting_officer = ''
                emp_details = list(posting_History.objects.filter( history_id = reqno ).values('history_id','done_by',
                    'empno_id' ,'prev_desigination','prev_parent_desig_code','prev_department_code_id__department_name','prev_rly_unit_id__location_code','prev_rly_unit_id__location_type','prev_contactnumber','prev_official_email_ID','prev_station_name',
                    'current_desigination','current_parent_desig_code','current_department_code_id__department_name','current_rly_unit_id__location_code','current_rly_unit_id__location_type','current_contactnumber','current_official_email_ID','current_station_name',
                    'empno_id__empname','empno_id__empmname','empno_id__emplname'
                ))
                if len(emp_details) > 0: 
                    reporting_officer = list(models.Level_Desig.objects.filter(designation_code = emp_details[0]['prev_parent_desig_code']).values('designation'))
                    if len(reporting_officer) > 0:
                        p_reporting_officer = reporting_officer[0]['designation']
                    else:
                        p_reporting_officer = ''
                    reporting_officer = list(models.Level_Desig.objects.filter(designation_code = emp_details[0]['current_parent_desig_code']).values('designation'))
                    if len(reporting_officer) > 0:
                        c_reporting_officer = reporting_officer[0]['designation']
                    else:
                        c_reporting_officer = ''
                
                context ={
                    'emp_details':emp_details,
                    'p_reporting_officer':p_reporting_officer,
                    'c_reporting_officer':c_reporting_officer,
                }
                
                return JsonResponse(context, safe = False) 
            if post_type == 'emp_details':
                empno = request.POST.get('empno')
                designation = request.POST.get('designation')
                reporting_officer = ''
                emp_details = list(models.Level_Desig.objects.filter(empno_id = empno, designation = designation).values('designation','rly_unit_id__location_code','rly_unit_id__location_type','empno_id','empno_id__empname','empno_id__empmname','empno_id__emplname','contactnumber','official_email_ID','department_code__department_name','station_name','empno_id__hrms_id_id','parent_desig_code','status').order_by('-status','designation'))
                if len(emp_details) > 0: 
                    reporting_officer = list(models.Level_Desig.objects.filter(designation_code = emp_details[0]['parent_desig_code']).values('designation'))
                    if len(reporting_officer) > 0:
                        reporting_officer = reporting_officer[0]['designation']
                    else:
                        reporting_officer = ''
                
                context ={
                    'emp_details':emp_details,
                    'reporting_officer':reporting_officer,
                }
                return JsonResponse(context, safe = False)  
            
            if post_type == 'emp_release':
                empno = request.POST.get('empno')
                charge_type = request.POST.get('charge_type')  
                designation = request.POST.get('designation')
                data = list(models.Level_Desig.objects.filter(empno_id = empno,designation = designation).values('official_email_ID'))
                msg = 'Operation Failed'
                if len(data)>0:
                    models.Level_Desig.objects.filter(empno = empno,designation = designation).update(empno = None, status = 'P',modified_by=cuser)
                    newuser = m1.MyUser.objects.filter(email=data[0]['official_email_ID']).update(is_active= False)
                    
                    msg = 'Successfully relinquished'
                return JsonResponse(msg, safe = False)
            if post_type == 'new_emp':
                empno = request.POST.get('empno')
                emp_no_details = list(m1.empmast.objects.filter(empno = empno).values())
                lev_desig_details = list(models.Level_Desig.objects.filter(empno_id = empno).values('designation','parent_desig_code','department_code__department_name','rly_unit_id__location_type','rly_unit_id__location_code','status','official_email_ID','contactnumber','station_name').order_by('-status'))
                if len(lev_desig_details) > 0: 
                    for i in range(len(lev_desig_details)):
                        reporting_officer = list(models.Level_Desig.objects.filter(designation_code = lev_desig_details[i]['parent_desig_code']).values('designation'))
                        if len(reporting_officer) > 0:
                            reporting_officer = reporting_officer[0]['designation']
                        else:
                            reporting_officer = ''
                        lev_desig_details[i].update({'reporting_officer':reporting_officer})
                response = {
                    'emp_no_details' : emp_no_details,
                    'lev_desig_details' : lev_desig_details,
                }
                return JsonResponse(response, safe = False)
            if post_type == 'desig_search':
                designation = request.POST.get('designation')
                lev_desig_details = list(models.Level_Desig.objects.filter(designation = designation).values('parent_desig_code','department_code','rly_unit_id','official_email_ID','contactnumber','station_name').order_by('status'))
                if len(lev_desig_details) > 0: 
                    for i in range(len(lev_desig_details)):
                        reporting_officer = ''
                        if lev_desig_details[i]['parent_desig_code'] is not None:
                            reporting_officer = list(models.Level_Desig.objects.filter(designation_code = lev_desig_details[i]['parent_desig_code']).values('designation'))
                            if len(reporting_officer) > 0:
                                reporting_officer = reporting_officer[i]['designation']
                            else:
                                reporting_officer = ''
                        lev_desig_details[i].update({'reporting_officer':reporting_officer})
                    
                    rly_unit_id = lev_desig_details[i]['rly_unit_id']
                    rly_unit_det=list(railwayLocationMaster.objects.filter( rly_unit_code= rly_unit_id).values('parent_rly_unit_code'))
                    rly_unit_det = list(map( lambda x: int(x['parent_rly_unit_code']),rly_unit_det))
                    rep_officer = list(models.Level_Desig.objects.filter(Q(rly_unit = rly_unit_id) | Q(rly_unit__in = rly_unit_det)).values('designation'))
                    rep_officer = list(map( lambda x: x['designation'],rep_officer))
                    all_station = list(models.station_master.objects.filter(Q(rly_id_id = rly_unit_id) | Q(div_id_id = rly_unit_id)).values('station_name').distinct().order_by('station_name'))
                    if lev_desig_details[0]['station_name'] is not None:
                        all_station.append({'station_name':lev_desig_details[0]['station_name']})
                
                context = {
                    'lev_desig_details' : lev_desig_details,
                    'rep_officer':rep_officer,
                    'all_station':all_station,
                }
                return JsonResponse(context, safe = False)
            
            if post_type == 'new_joining':
                empno = request.POST.get('empno')
                txt_new_joining_designation = request.POST.get('txt_new_joining_designation')
                charge_type_new_joining = request.POST.get('charge_type_new_joining')
                department_new_joining = request.POST.get('department_new_joining')
                place_new_joining = request.POST.get('place_new_joining')
                reporting_officer_new_joining = request.POST.get('reporting_officer_new_joining')
                if reporting_officer_new_joining == '':
                    reporting_officer_new_joining = None
                else:
                    dt1 = list(models.Level_Desig.objects.filter(designation = reporting_officer_new_joining).values('designation_code'))
                    reporting_officer_new_joining = dt1[0]['designation_code']
                contact_new_joining = request.POST.get('contact_new_joining')
                email_new_joining = request.POST.get('email_new_joining')
                station_new_joining = request.POST.get('station_new_joining')
                remarks_new_joining = request.POST.get('remarks_new_joining')
                msg = 'Not changed, please contact admin'
                password = 'Admin@123'
                if charge_type_new_joining == 'D':
                    if models.Level_Desig.objects.filter(~Q(designation = txt_new_joining_designation), official_email_ID=email_new_joining).exists():
                        msg = 'e-mail id is already used with another designation, Request cannot be processed'
                    elif models.Level_Desig.objects.filter(designation = txt_new_joining_designation, empno = empno , status = 'D').exists():
                        msg = 'Same user is already Exists as Dual charge for the same post'
                    elif Level_Desig.objects.filter(~Q( empno = empno), contactnumber = contact_new_joining).exists():
                        msg = 'Contact number already present, with some other designation, Request cannot be processed'
                    else:
                        posting_History.objects.create(empno_id = empno,done_by = cuser,current_desigination = txt_new_joining_designation,current_parent_desig_code= reporting_officer_new_joining,current_department_code_id=department_new_joining,current_rly_unit_id=place_new_joining,
                        current_contactnumber=contact_new_joining,current_official_email_ID=email_new_joining,current_station_name=station_new_joining,charge_type=charge_type_new_joining,created_date=datetime.now(),accepted_date=datetime.now(),status='Accepted',created_remarks=remarks_new_joining)
                        prev_details =list(models.Level_Desig.objects.filter(designation = txt_new_joining_designation).values())
                        models.Level_Desig.objects.filter(designation = txt_new_joining_designation).update(modified_by=cuser,empno_id = empno, department_code_id = department_new_joining,parent_desig_code = reporting_officer_new_joining,rly_unit_id=place_new_joining,status=charge_type_new_joining,contactnumber=contact_new_joining,official_email_ID=email_new_joining,station_name=station_new_joining)
                        if m1.MyUser.objects.filter(id = prev_details[0]['desig_user_id']).exists():
                            forgetuser=m1.MyUser.objects.filter(id = prev_details[0]['desig_user_id']).first()
                            if forgetuser:
                                forgetuser.set_password(password)
                                forgetuser.save()
                                m1.MyUser.objects.filter(username=email_new_joining).update(username=None,is_active= False,email = None)
                                m1.MyUser.objects.filter(id = prev_details[0]['desig_user_id']).update(username=email_new_joining,is_active= True,email = email_new_joining)
                        else:
                            id = list(m1.MyUser.objects.values('id').order_by('-id'))
                            if len(id)>0:
                                id = id[0]['id'] + 1
                            else:
                                id = 1
                            newuser = m1.MyUser.objects.create_user(id = id,username=email_new_joining, password=password,email=email_new_joining,user_role='user')
                            newuser.is_active= True
                            newuser.is_admin=False
                            newuser.save()
                            myuser_id = list(m1.MyUser.objects.filter(email = email_new_joining).values('id'))
                            if len(myuser_id)>0:
                                models.Level_Desig.objects.filter(designation = txt_new_joining_designation).update(desig_user_id = myuser_id[0]['id'])
                        msg = 'Dual charge is created successfully'
                

                if charge_type_new_joining == 'P':
                    if str(request.user).startswith('admin'):
                        actual_user = str(request.user).split('admin')[1]
                    else:
                        actual_user = request.user
                    empnox_det = AdminMaster.objects.filter(Q(admin_email=actual_user), user_id__isnull=False).values('rly','user_id')
                    #empnox_det = AdminMaster.objects.filter(Q(admin_email='admin'+str(request.user)) | Q(admin_email='admin'+str(request.user.email)), user_id__isnull=False).values('rly','user_id')
                    rly_unit_id_det=None
                    cuser_det = None
                    if empnox_det:
                        rly_unit_id_det = empnox_det[0]['rly']
                        cuser_det = empnox_det[0]['user_id']
                    if models.Level_Desig.objects.filter(~Q(designation = txt_new_joining_designation), official_email_ID=email_new_joining).exists():
                        msg = 'e-mail id is already used with another designation, Request cannot be processed'

                    elif models.Level_Desig.objects.filter(designation = txt_new_joining_designation, empno = empno , status = 'P').exists():
                        msg = 'Same user is already Exists as Primary charge for the same post'
                    
                    elif Level_Desig.objects.filter(~Q(designation = txt_new_joining_designation),contactnumber=contact_new_joining,status = 'P').exists():
                        msg = 'Contact number is already used with another designation, Request cannot be processed'

                    elif models.Level_Desig.objects.filter(empno = empno , status = 'P', rly_unit = rly_unit_id_det).exists():
                        prev_details =list(models.Level_Desig.objects.filter(empno = empno , status = 'P', rly_unit = rly_unit_id_det).values())
                
                        if len(prev_details)>0:
                            models.Level_Desig.objects.filter(empno_id = empno,designation = prev_details[0]['designation']).update(modified_by=cuser_det,empno_id = None, status = 'P')
                            m1.MyUser.objects.filter(email=prev_details[0]['official_email_ID']).update(is_active= False)
                           
                        
                        posting_History.objects.create(empno_id = empno,done_by = cuser,current_desigination = txt_new_joining_designation,current_parent_desig_code= reporting_officer_new_joining,current_department_code_id=department_new_joining,current_rly_unit_id=place_new_joining,
                        prev_desigination=prev_details[0]['designation'],prev_parent_desig_code=prev_details[0]['parent_desig_code'],prev_department_code_id=prev_details[0]['department_code_id'],prev_rly_unit_id=prev_details[0]['rly_unit_id'],prev_contactnumber=prev_details[0]['contactnumber'],prev_official_email_ID=prev_details[0]['official_email_ID'],prev_station_name=prev_details[0]['station_name'],
                        current_contactnumber=contact_new_joining,current_official_email_ID=email_new_joining,current_station_name=station_new_joining,charge_type=charge_type_new_joining,created_date=datetime.now(),accepted_date=datetime.now(),status='Accepted',created_remarks=remarks_new_joining)
                        
                        models.Level_Desig.objects.filter(designation = txt_new_joining_designation).update(modified_by=cuser_det,empno_id = empno, department_code_id = department_new_joining,parent_desig_code = reporting_officer_new_joining,rly_unit_id=place_new_joining,status=charge_type_new_joining,contactnumber=contact_new_joining,official_email_ID=email_new_joining,station_name=station_new_joining)
                        if m1.MyUser.objects.filter(id = prev_details[0]['desig_user_id']).exists():
                            forgetuser=m1.MyUser.objects.filter(id = prev_details[0]['desig_user_id']).first()
                            if forgetuser:
                                forgetuser.set_password(password)
                                forgetuser.save()
                                m1.MyUser.objects.filter(username=email_new_joining).update(username=None,is_active= False,email = None)
                                m1.MyUser.objects.filter(id = prev_details[0]['desig_user_id']).update(username=email_new_joining,is_active= True,email = email_new_joining)
                        else:
                            id = list(m1.MyUser.objects.values('id').order_by('-id'))
                            if len(id)>0:
                                id = id[0]['id'] + 1
                            else:
                                id = 1
                            newuser = m1.MyUser.objects.create_user(id = id,username=email_new_joining, password=password,email=email_new_joining,user_role='user')
                            newuser.is_active= True
                            newuser.is_admin=False
                            newuser.save()
                            myuser_id = list(m1.MyUser.objects.filter(email = email_new_joining).values('id'))
                            if len(myuser_id)>0:
                                models.Level_Desig.objects.filter(designation = txt_new_joining_designation).update(desig_user_id = myuser_id[0]['id'])
                        msg = 'Primary charge is updated successfully'

                    elif models.Level_Desig.objects.filter(empno = empno , status = 'P').exists():
                        prev_details =list(models.Level_Desig.objects.filter(empno = empno , status = 'P').values())
                        if posting_History.objects.filter(done_by = cuser,status='Forwarded',empno = empno).exists():
                            msg = f"request already exists for the employee, To request again pull back the previous request"
                        else:
                            posting_History.objects.create(empno_id = empno,done_by = cuser,current_desigination = txt_new_joining_designation,current_parent_desig_code= reporting_officer_new_joining,current_department_code_id=department_new_joining,current_rly_unit_id=place_new_joining,
                            prev_desigination=prev_details[0]['designation'],prev_parent_desig_code=prev_details[0]['parent_desig_code'],prev_department_code_id=prev_details[0]['department_code_id'],prev_rly_unit_id=prev_details[0]['rly_unit_id'],prev_contactnumber=prev_details[0]['contactnumber'],prev_official_email_ID=prev_details[0]['official_email_ID'],prev_station_name=prev_details[0]['station_name'],
                            current_contactnumber=contact_new_joining,current_official_email_ID=email_new_joining,current_station_name=station_new_joining,charge_type=charge_type_new_joining,created_date=datetime.now(),status='Forwarded',created_remarks=remarks_new_joining)
                            prev_details =list(models.Level_Desig.objects.filter(empno = empno , status = 'P').values('rly_unit__location_code'))
                            msg = f"Request sent to {prev_details[0]['rly_unit__location_code']} for relinquished, once accepted primary charge will be updated"
                    
                    else:
                        posting_History.objects.create(empno_id = empno,done_by = cuser,current_desigination = txt_new_joining_designation,current_parent_desig_code= reporting_officer_new_joining,current_department_code_id=department_new_joining,current_rly_unit_id=place_new_joining,
                        current_contactnumber=contact_new_joining,current_official_email_ID=email_new_joining,current_station_name=station_new_joining,charge_type=charge_type_new_joining,created_date=datetime.now(),accepted_date=datetime.now(),status='Accepted',created_remarks=remarks_new_joining)
                        prev_details =list(models.Level_Desig.objects.filter(designation = txt_new_joining_designation).values())
                        models.Level_Desig.objects.filter(designation = txt_new_joining_designation).update(modified_by=cuser_det,empno_id = empno, department_code_id = department_new_joining,parent_desig_code = reporting_officer_new_joining,rly_unit_id=place_new_joining,status=charge_type_new_joining,contactnumber=contact_new_joining,official_email_ID=email_new_joining,station_name=station_new_joining)
                        if m1.MyUser.objects.filter(id = prev_details[0]['desig_user_id']).exists():
                            forgetuser=m1.MyUser.objects.filter(id = prev_details[0]['desig_user_id']).first()
                            if forgetuser:
                                forgetuser.set_password(password)
                                forgetuser.save()
                                m1.MyUser.objects.filter(username=email_new_joining).update(username=None,is_active= False,email = None)
                                m1.MyUser.objects.filter(id = prev_details[0]['desig_user_id']).update(username=email_new_joining,is_active= True,email = email_new_joining)
                        else:
                            id = list(m1.MyUser.objects.values('id').order_by('-id'))
                            if len(id)>0:
                                id = id[0]['id'] + 1
                            else:
                                id = 1
                            newuser = m1.MyUser.objects.create_user(id = id,username=email_new_joining, password=password,email=email_new_joining,user_role='user')
                            newuser.is_active= True
                            newuser.is_admin=False
                            newuser.save()
                            myuser_id = list(m1.MyUser.objects.filter(email = email_new_joining).values('id'))
                            if len(myuser_id)>0:
                                models.Level_Desig.objects.filter(designation = txt_new_joining_designation).update(desig_user_id = myuser_id[0]['id'])
                        msg = 'Primary charge is created successfully'
                return JsonResponse(msg, safe = False)
            
            if post_type == 'history':
                history_id = request.POST.get('history_id')
                history_data = list(posting_History.objects.filter(history_id=history_id).values())
                admin_1 = list(posting_History.objects.filter(history_id=history_id).values('current_rly_unit__location_code'))
                if len(admin_1)>0:
                    admin_1 = 'Admin ' + str(admin_1[0]['current_rly_unit__location_code'])
                else:
                    admin_1 = 'Admin'
                pending = []
                if history_data[0]['prev_rly_unit_id']  is not None:
                    for i in range(len(history_data)):
                        prev_rly_unit = history_data[i]['prev_rly_unit_id']
                        if rly_unit_id == prev_rly_unit:
                            if AdminMaster.objects.filter(status='Active',rly = prev_rly_unit).exists():
                                dt_list=list(AdminMaster.objects.filter(status='Active',rly = prev_rly_unit).values())
                                pending.extend(dt_list)
                        
                        elif prev_rly_unit in child_rly:
                            if AdminMaster.objects.filter(status='Active',rly = prev_rly_unit).exists():
                                dt_list=list(AdminMaster.objects.filter(status='Active',rly = prev_rly_unit).values())
                                pending.extend(dt_list)
                    if len(pending) == 0:
                        dt_list=list(AdminMaster.objects.filter(status='Active',user_id = '111111').values())
                        pending.extend(dt_list)
                

                context = {
                    'history_data':history_data,
                    'pending':pending,
                    'admin_1':admin_1,
                }
                # print(admin_1)
                return JsonResponse(context, safe = False) 
            
            if post_type == 'pullback':
                history_id = request.POST.get('history_id')
                posting_History.objects.filter(history_id=history_id).delete()
                msg = 'Successfuly Pulled Back'
                return JsonResponse(msg, safe = False) 
            
            if post_type == 'station':
                val = request.POST.get('val')
                all_station = list(models.station_master.objects.filter(Q(rly_id_id = val) | Q(div_id_id = val)).values('station_name').distinct().order_by('station_name'))
                return JsonResponse(all_station, safe = False) 
            return JsonResponse({"success":False}, status=400)
        
        details_data = list(models.Level_Desig.objects.filter((Q(rly_unit = rly_unit_id) | Q(rly_unit__in=railwayLocationMaster.objects.filter(parent_rly_unit_code = str(rly_unit_id)).values('rly_unit_code')))).values('designation','rly_unit_id__location_code','rly_unit_id__location_type','empno_id','empno_id__empname','empno_id__empmname','empno_id__emplname','contactnumber','official_email_ID').order_by('designation'))
        rly_emp_designation = list(map(lambda x: x['designation'],details_data))
        new_emp_no = list(m1.empmast.objects.filter( railwaygroup__in=['A','B']).values('empno','hrms_id' , 'empname', 'empmname', 'emplname').order_by('empname'))
        all_department = list(models.departMast.objects.filter(delete_flag = False).values('department_code','department_name').order_by('department_name'))
        all_railway = list(railwayLocationMaster.objects.filter((Q(parent_rly_unit_code = str(rly_unit_id)) | Q(rly_unit_code = rly_unit_id)),location_type__in =['RDSO','WS','DIV','RB','ZR','PSU','CTI','PU']).values('rly_unit_code','location_description','location_code','location_type').distinct().order_by('location_code'))
        all_station = list(models.station_master.objects.filter(Q(rly_id_id = rly_unit_id) | Q(div_id_id = rly_unit_id)).values('station_name').distinct().order_by('station_name'))
        requested = posting_History.objects.filter(done_by = cuser).all().order_by('-created_date')
        pending = []
        pending11 = list(posting_History.objects.filter(status='Forwarded').values().order_by('-created_date'))
        # new_emp_no=[]
        if rolelist == 'admin_super':
            for i in range(len(pending11)):
                pending.append(pending11[i])
        else:
            for i in range(len(pending11)):
                prev_rly_unit = pending11[i]['prev_rly_unit_id']
                if rly_unit_id == prev_rly_unit:
                    if AdminMaster.objects.filter(status='Active',rly = prev_rly_unit).exists():
                        pending.append(pending11[i])
                
                elif prev_rly_unit in child_rly:
                    if AdminMaster.objects.filter(status='Active',rly = prev_rly_unit).exists():
                        pending.append(pending11[i])
        # print("Testing for admin user list")
        context ={
            'details_data' : details_data,
            'new_emp_no' : new_emp_no,
            'rly_emp_designation' : rly_emp_designation,
            'all_department':all_department,
            'all_railway' : all_railway,
            'all_station' : all_station,
            'requested' : requested,
            'pending':pending,

        }
        # print("Testing for admin user list LAST")
        return render(request, "user_list.html", context)
    
    # except Exception as e: 
    #     try:
    #         m1.error_Table.objects.create(fun_name="user_list",user_id=request.user,err_details=str(e))
    #     except:
    #         print("Internal Error!!!")
    #     return render(request, "myadmin_errors.html", {})


# def designation_request(request):
#     # try:
#         usermast=m1.MyUser.objects.filter(email=request.user).first()
#         rolelist=usermast.user_role
#         if str(request.user).startswith('admin'):
#             actual_user = str(request.user).split('admin')[1]
#         else:
#             actual_user = request.user
#         empnox = AdminMaster.objects.filter(Q(admin_email=actual_user), user_id__isnull=False).values('rly','user_id')
#         rly_unit_id=None
#         cuser = None
#         parent_rly = []
#         if empnox:
#             rly_unit_id = empnox[0]['rly']
#             cuser = empnox[0]['user_id']
#             child_rly = list(railwayLocationMaster.objects.filter( parent_rly_unit_code  = str(rly_unit_id)).values('rly_unit_code'))
#             if len(child_rly)>0:
#                 child_rly = list(map(lambda x: x['rly_unit_code'], child_rly))
#         if request.method == 'POST' and request.is_ajax():
#             post_type = request.POST.get('post_type')
#             if post_type == 'similar':
#                 post = request.POST.get('post')
#                 current_user = request.user
#                 if str(request.user).startswith('admin'):
#                     actual_user = str(request.user).split('admin')[1]
#                 else:
#                     actual_user = request.user
#                 empnox = AdminMaster.objects.filter(Q(admin_email=actual_user), user_id__isnull=False).values('rly','user_id')            
#                 rly_unit_id=None
#                 if empnox:
#                     rly_unit_id = empnox[0]['rly']
#                 rep_officer = list(models.Level_Desig.objects.filter((Q(rly_unit = rly_unit_id)|Q(rly_unit_id__parent_rly_unit_code  = str(rly_unit_id))),designation__startswith= post+'/').values('designation'))
#                 rep_officer = list(map( lambda x: x['designation'],rep_officer))
#                 rep_officer = ', '.join(rep_officer)
#                 context = {
#                     'rep_officer':rep_officer,
#                 }
#                 return JsonResponse(context,safe=False)
        
#             if post_type == 'emp_details':
#                 designation = request.POST.get('designation')
#                 reporting_officer = ''
#                 emp_details = list(models.Level_Desig.objects.filter(designation = designation).values('d_level','designation','rly_unit_id__location_code','rly_unit_id__location_type','empno_id','empno_id__empname','empno_id__empmname','empno_id__emplname','contactnumber','official_email_ID','department_code__department_name','station_name','empno_id__hrms_id_id','parent_desig_code','status').order_by('-status','designation'))
#                 if len(emp_details) > 0: 
#                     reporting_officer = list(models.Level_Desig.objects.filter(designation_code = emp_details[0]['parent_desig_code']).values('designation'))
#                     if len(reporting_officer) > 0:
#                         reporting_officer = reporting_officer[0]['designation']
#                     else:
#                         reporting_officer = ''
#                 context ={
#                     'emp_details':emp_details,
#                     'reporting_officer':reporting_officer,
#                 }
#                 return JsonResponse(context, safe = False) 
#             if post_type == 'desig_search':
#                 designation = request.POST.get('designation')
#                 lev_desig_details = list(models.Level_Desig.objects.filter(designation = designation).values('pc7_levelmin','pc7_levelmax','parent_desig_code','department_code','rly_unit_id','official_email_ID','contactnumber','station_name').order_by('status'))
#                 if len(lev_desig_details) > 0: 
#                     for i in range(len(lev_desig_details)):
#                         reporting_officer = ''
#                         if lev_desig_details[i]['parent_desig_code'] is not None:
#                             reporting_officer = list(models.Level_Desig.objects.filter(designation_code = lev_desig_details[i]['parent_desig_code']).values('designation'))
#                             if len(reporting_officer) > 0:
#                                 reporting_officer = reporting_officer[i]['designation']
#                             else:
#                                 reporting_officer = ''
#                         lev_desig_details[i].update({'reporting_officer':reporting_officer})
                    
#                     rly_unit_id = lev_desig_details[i]['rly_unit_id']
#                     rly_unit_det=list(railwayLocationMaster.objects.filter( rly_unit_code= rly_unit_id).values('parent_rly_unit_code'))
#                     rly_unit_det = list(map( lambda x: int(x['parent_rly_unit_code']),rly_unit_det))
#                     rep_officer = list(models.Level_Desig.objects.filter(Q(rly_unit = rly_unit_id) | Q(rly_unit__in = rly_unit_det)).values('designation'))
#                     rep_officer = list(map( lambda x: x['designation'],rep_officer))
#                     all_station = list(models.station_master.objects.filter(Q(rly_id_id = rly_unit_id) | Q(div_id_id = rly_unit_id)).values('station_name').distinct().order_by('station_name'))
#                     if lev_desig_details[0]['station_name'] is not None:
#                         all_station.append({'station_name':lev_desig_details[0]['station_name']})
                
#                 context = {
#                     'lev_desig_details' : lev_desig_details,
#                     'rep_officer':rep_officer,
#                     'all_station':all_station,
#                 }
#                 return JsonResponse(context, safe = False)
#             if post_type == 'station':
#                 val = request.POST.get('val')
#                 all_station = list(models.station_master.objects.filter(Q(rly_id_id = val) | Q(div_id_id = val)).values('station_name').distinct().order_by('station_name'))
#                 return JsonResponse(all_station, safe = False)  
#             if post_type == 'saveDataChanged':
#                 msg = 'Please contact superadmin'

#                 # #designation,pre_email,pre_contact,pre_minlevel,pre_maxlevel,pre_station,pre_place,pre_department,pre_reporting_officer,pre_remarks
#                 # designation=designation,rly_unit=pre_place,department_code=pre_department,station_name=pre_station,contactnumber=pre_contact,official_email_ID=pre_email
#                 # ,pc7_levelmin=pre_minlevel,pc7_levelmax=pre_maxlevel,parent_desig_code=pre_reporting_officer
#                 designation = request.POST.get('designation')
#                 pre_email = request.POST.get('pre_email')
#                 pre_contact = request.POST.get('pre_contact')
#                 pre_minlevel = request.POST.get('pre_minlevel')
#                 pre_maxlevel = request.POST.get('pre_maxlevel')
#                 pre_station = request.POST.get('pre_station')
#                 pre_place = request.POST.get('pre_place')
#                 pre_department = request.POST.get('pre_department')
#                 pre_reporting_officer = request.POST.get('pre_reporting_officer')
#                 pre_remarks = request.POST.get('pre_remarks')

#                 if pre_reporting_officer is not None or pre_reporting_officer != '':
#                     reporting_officer = list(models.Level_Desig.objects.filter(designation = pre_reporting_officer).values('designation_code'))
#                     if len(reporting_officer) > 0:
#                         pre_reporting_officer = reporting_officer[0]['designation_code']
#                     else:
#                         pre_reporting_officer = None
#                 else:
#                         pre_reporting_officer = None

#                 if models.Level_Desig.objects.filter(~Q(designation = designation), official_email_ID=pre_email).exists():
#                     msg = 'e-mail id is already used with another designation, Request cannot be processed' 

#                 elif models.Level_Desig.objects.filter(designation=designation,rly_unit=pre_place,department_code=pre_department,station_name=pre_station,contactnumber=pre_contact,official_email_ID=pre_email,
#                             pc7_levelmin=pre_minlevel,pc7_levelmax=pre_maxlevel,parent_desig_code=pre_reporting_officer).exists():
#                     msg = 'All the field having the previous value only, Request cannot be processed'
                
#                 elif models.designation_Change_Request.objects.filter(status='Forwarded',request_type='Modification',desigination=designation).exists():
#                     msg = 'Request already exist, pull back the existing request to give new request' 
                
#                 else:
#                     prevData = list(models.Level_Desig.objects.filter(designation = designation).values())
#                     designation_Change_Request.objects.create(request_by=cuser,request_date=datetime.now(),request_remarks=pre_remarks,desigination=designation,status='Forwarded',request_type='Modification',
#                         prev_parent_desig_code=prevData[0]['parent_desig_code'],prev_department_code_id=prevData[0]['department_code_id'],prev_rly_unit_id=prevData[0]['rly_unit_id'],prev_contactnumber=prevData[0]['contactnumber'],prev_official_email_ID=prevData[0]['official_email_ID'],prev_station_name=prevData[0]['station_name'],prev_maxlevel=prevData[0]['pc7_levelmax'],prev_minlevel=prevData[0]['pc7_levelmin'],
#                         current_parent_desig_code=pre_reporting_officer,current_department_code_id=pre_department,current_rly_unit_id=pre_place,current_contactnumber=pre_contact,current_official_email_ID=pre_email,current_station_name=pre_station,current_maxlevel=pre_maxlevel,current_minlevel=pre_minlevel)
#                     msg = 'success'

#                 return JsonResponse(msg, safe = False)
#             if post_type == 'getRecord':
#                 record_id = request.POST.get('record_id')   
#                 record_data = list(models.designation_Change_Request.objects.filter(record_id=record_id).values(
#                     'record_id','request_by','request_date','request_remarks','desigination','status','request_type','action_by','action_date','action_remarks',
#                     'prev_parent_desig_code','prev_department_code__department_name','prev_rly_unit__location_code','prev_rly_unit__location_type','prev_rly_unit__location_description','prev_contactnumber','prev_official_email_ID','prev_station_name','prev_maxlevel','prev_minlevel',
#                     'current_parent_desig_code','current_department_code__department_name','current_rly_unit__location_code','current_rly_unit__location_type','current_rly_unit__location_description','current_contactnumber','current_official_email_ID','current_station_name','current_maxlevel','current_minlevel'
#                 ))
#                 if len(record_data) > 0: 
#                     reporting_officer = list(models.Level_Desig.objects.filter(designation_code = record_data[0]['prev_parent_desig_code']).values('designation'))
#                     if len(reporting_officer) > 0:
#                         prev_reporting_officer = reporting_officer[0]['designation']
#                     else:
#                         prev_reporting_officer = ''
                    
#                     reporting_officer = list(models.Level_Desig.objects.filter(designation_code = record_data[0]['current_parent_desig_code']).values('designation'))
#                     if len(reporting_officer) > 0:
#                         curr_reporting_officer = reporting_officer[0]['designation']
#                     else:
#                         curr_reporting_officer = ''
#                     record_data[0].update({'prev_parent_desig_code':prev_reporting_officer,'current_parent_desig_code':curr_reporting_officer})
                
#                 return JsonResponse(record_data, safe = False)  
#             if post_type == 'pullback':
#                 record_id = request.POST.get('record_id')
#                 pullBackRemark = request.POST.get('pullBackRemark')
#                 msg = ''
#                 if models.designation_Change_Request.objects.filter(record_id=record_id,status='Forwarded').exists():
#                     models.designation_Change_Request.objects.filter(record_id=record_id).update(action_by=cuser,action_date=datetime.now(),action_remarks=pullBackRemark,status='Pulled Back')
#                     msg = 'Successfully Pulled Back'
#                 else:
#                     msg = 'Failed to Pull Back'
#                 return JsonResponse(msg, safe = False)
#             if post_type == 'accept':
#                 record_id = request.POST.get('record_id')
#                 pullBackRemark = request.POST.get('pullBackRemark')
#                 msg = ''
#                 if models.designation_Change_Request.objects.filter(record_id=record_id,status='Forwarded').exists():
#                     password = 'Admin@123'
#                     act_data = list(models.designation_Change_Request.objects.filter(record_id=record_id).values())
                    
#                     if act_data[0]['request_type'] != 'New':
#                         if act_data[0]['current_parent_desig_code'] is not None:
#                             reporting_officer_new_joining = act_data[0]['current_parent_desig_code']
#                         else:
#                             reporting_officer_new_joining = None
#                         prev_details =list(models.Level_Desig.objects.filter(designation = act_data[0]['desigination']).values())
                        
#                         div_id_id=list(railwayLocationMaster.objects.filter(rly_unit_code=act_data[0]['current_rly_unit_id'],location_type_desc__in=rlyhead.objects.filter(rltype='HQ').values('rllongdesc')).values('parent_rly_unit_code','location_type'))
#                         if len(div_id_id) > 0:
#                             hq_id_id = act_data[0]['current_rly_unit_id']
#                             div_id_id = None
#                         else:
#                             hq_id_id=list(railwayLocationMaster.objects.filter(rly_unit_code=act_data[0]['current_rly_unit_id']).values('parent_rly_unit_code','location_type'))
                            
#                             if hq_id_id[0]['location_type'] in ['DIV','WS']:
#                                 div_id_id = act_data[0]['current_rly_unit_id']
#                             else:
#                                 div_id_id = None
#                             hq_id_id = hq_id_id[0]['parent_rly_unit_code']
                            
#                         models.Level_Desig.objects.filter(designation = act_data[0]['desigination']).update(modified_by=cuser,department_code_id = act_data[0]['current_department_code_id'],
#                         parent_desig_code = reporting_officer_new_joining,rly_unit_id=act_data[0]['current_rly_unit_id'],hq_id_id=hq_id_id,div_id_id=div_id_id,
#                         pc7_levelmin=act_data[0]['current_minlevel'],pc7_levelmax=act_data[0]['current_maxlevel'],
#                         contactnumber=act_data[0]['current_contactnumber'],official_email_ID=act_data[0]['current_official_email_ID'],station_name=act_data[0]['current_station_name'])
#                         if m1.MyUser.objects.filter(id = prev_details[0]['desig_user_id']).exists():
#                             forgetuser=m1.MyUser.objects.filter(id = prev_details[0]['desig_user_id']).first()
#                             if forgetuser:
#                                 forgetuser.set_password(password)
#                                 forgetuser.save()
#                                 m1.MyUser.objects.filter(username=act_data[0]['current_official_email_ID']).update(username=None,is_active= False,email = None)
#                                 m1.MyUser.objects.filter(id = prev_details[0]['desig_user_id']).update(username=act_data[0]['current_official_email_ID'],is_active= True,email = act_data[0]['current_official_email_ID'])
#                         else:
#                             id = list(m1.MyUser.objects.values('id').order_by('-id'))
#                             if len(id)>0:
#                                 id = id[0]['id'] + 1
#                             else:
#                                 id = 1
#                             newuser = m1.MyUser.objects.create_user(id = id,username=act_data[0]['current_official_email_ID'], password=password,email=act_data[0]['current_official_email_ID'],user_role='user')
#                             newuser.is_active= True
#                             newuser.is_admin=False
#                             newuser.save()
#                             myuser_id = list(m1.MyUser.objects.filter(email = act_data[0]['current_official_email_ID']).values('id'))
#                             if len(myuser_id)>0:
#                                 models.Level_Desig.objects.filter(designation = act_data[0]['desigination']).update(desig_user_id = myuser_id[0]['id'])
#                         models.designation_Change_Request.objects.filter(record_id=record_id).update(action_by=cuser,action_date=datetime.now(),action_remarks=pullBackRemark,status='Accepted')
#                         msg = 'Successfully Accepted the Modification'
#                     else:
#                         if models.Level_Desig.objects.filter(designation = act_data[0]['desigination']).exists():
#                             msg = 'Designation already present'
#                         else:
#                             if act_data[0]['current_parent_desig_code'] is not None:
#                                 reporting_officer_new_joining = act_data[0]['current_parent_desig_code']
#                             else:
#                                 reporting_officer_new_joining = None

#                             prev_details =list(models.Level_Desig.objects.filter(designation = act_data[0]['desigination']).values())
#                             st_post = act_data[0]['desigination'].split('/')[0]
#                             data = list(Post_master.objects.filter(post_code=st_post).values('category','pc7_levelmin','pc7_levelmax','department_code_id'))
#                             if len(data)>0:
#                                 category = data[0]['category']
#                             else:
#                                 category = None
#                             if category == 'CRB':
#                                 role = 'CRB'
#                             else:
#                                 role = 'user'
#                             id = list(models.Level_Desig.objects.values('designation_code').order_by('-designation_code'))
#                             if len(id)>0:
#                                 id = id[0]['designation_code'] + 1
#                             else:
#                                 id = 1

#                             get_department_name = list(models.departMast.objects.filter(delete_flag = False,department_code=act_data[0]['current_department_code_id']).values('department_name').order_by('department_name'))
#                             if len(get_department_name)>0:
#                                 get_department_name = get_department_name[0]['department_name']
#                             else:
#                                 get_department_name = None

#                             hierarchy_level = list(models.category.objects.filter(category=category).values('hierarchy_level'))
#                             if len(hierarchy_level) > 0:
#                                 hierarchy_level = hierarchy_level[0]['hierarchy_level']
#                             else:
#                                 hierarchy_level = None

#                             div_id_id=list(railwayLocationMaster.objects.filter(rly_unit_code=act_data[0]['current_rly_unit_id'],location_type_desc__in=rlyhead.objects.filter(rltype='HQ').values('rllongdesc')).values('parent_rly_unit_code','location_type'))
#                             if len(div_id_id) > 0:
#                                 hq_id_id = act_data[0]['current_rly_unit_id']
#                                 div_id_id = None
#                             else:
#                                 hq_id_id=list(railwayLocationMaster.objects.filter(rly_unit_code=act_data[0]['current_rly_unit_id']).values('parent_rly_unit_code','location_type'))
                                
#                                 if hq_id_id[0]['location_type'] in ['DIV','WS']:
#                                     div_id_id = act_data[0]['current_rly_unit_id']
#                                 else:
#                                     div_id_id = None
#                                 hq_id_id = hq_id_id[0]['parent_rly_unit_code']

#                             models.Level_Desig.objects.create(hq_id_id=hq_id_id,div_id_id=div_id_id,hierarchy_level=hierarchy_level,designation_code = id,effectdate=datetime.now(),status='P',d_level=category,user_role=role,designation = act_data[0]['desigination'],modified_by=cuser,department_code_id = act_data[0]['current_department_code_id'],department = get_department_name,
#                             parent_desig_code = reporting_officer_new_joining,rly_unit_id=act_data[0]['current_rly_unit_id'],
#                             pc7_levelmin=act_data[0]['current_minlevel'],pc7_levelmax=act_data[0]['current_maxlevel'],
#                             contactnumber=act_data[0]['current_contactnumber'],official_email_ID=act_data[0]['current_official_email_ID'],station_name=act_data[0]['current_station_name'])
                           
#                             id = list(m1.MyUser.objects.values('id').order_by('-id'))
#                             if len(id)>0:
#                                 id = id[0]['id'] + 1
#                             else:
#                                 id = 1
#                             m1.MyUser.objects.filter(email=act_data[0]['current_official_email_ID']).delete()
#                             newuser = m1.MyUser.objects.create_user(id = id,username=act_data[0]['current_official_email_ID'], password=password,email=act_data[0]['current_official_email_ID'],user_role='user')
#                             newuser.is_active= True
#                             newuser.is_admin=False
#                             newuser.save()
#                             myuser_id = list(m1.MyUser.objects.filter(email = act_data[0]['current_official_email_ID']).values('id'))
#                             if len(myuser_id)>0:
#                                 models.Level_Desig.objects.filter(designation = act_data[0]['desigination']).update(desig_user_id = id)
#                             models.designation_Change_Request.objects.filter(record_id=record_id).update(action_by=cuser,action_date=datetime.now(),action_remarks=pullBackRemark,status='Accepted')
#                             msg = 'Successfully Accepted the New Designation'

#                 else:
#                     msg = 'Failed to Accept'
#                 return JsonResponse(msg, safe = False)
#             if post_type == 'reject':
#                 record_id = request.POST.get('record_id')
#                 pullBackRemark = request.POST.get('pullBackRemark')
#                 msg = ''
#                 if models.designation_Change_Request.objects.filter(record_id=record_id,status='Forwarded').exists():
#                     models.designation_Change_Request.objects.filter(record_id=record_id).update(action_by=cuser,action_date=datetime.now(),action_remarks=pullBackRemark,status='Rejected')
#                     msg = 'Successfully Rejected'
#                 else:
#                     msg = 'Failed to Reject'
#                 return JsonResponse(msg, safe = False)
#             if post_type == 'getPostDetails':
#                 post = request.POST.get('post')
#                 context = list(Post_master.objects.filter(post_code=post).values('category','pc7_levelmin','pc7_levelmax','department_code_id__department_name'))
#                 return JsonResponse(context, safe = False)
#             if post_type == 'checkRlyType':
#                 rly = request.POST.get('rly')
#                 post = request.POST.get('post')
#                 location_code = ''
#                 parent_location_code = ''
#                 location_type_desc = ''
#                 createdDesignation = post
#                 context = list(railwayLocationMaster.objects.filter(rly_unit_code=rly).values('location_code','parent_location_code','location_type_desc'))
#                 if len(context) > 0:
#                     location_code = context[0]['location_code']
#                     parent_location_code = context[0]['parent_location_code']
#                     location_type_desc = context[0]['location_type_desc']
#                 if location_type_desc in ['RAILWAY BOARD', 'PRODUCTION UNIT', 'HEAD QUATER', 'PSU', 'INSTITUTE']:
#                     createdDesignation = createdDesignation + '/' + location_code
#                 else:
#                     if post != 'DRM':
#                         createdDesignation = createdDesignation + '/' + location_code + '/' + parent_location_code
#                     else:
#                         createdDesignation = createdDesignation + '/' + location_code

#                 data = list(models.Level_Desig.objects.filter(designation__startswith=createdDesignation).values('designation'))
#                 if len(data) > 0:
#                     data = list(map( lambda x: x['designation'],data))
#                     data = ', '.join(data)
#                 else:
#                     data = ''
#                 context = {
#                     'createdDesignation' : createdDesignation,
#                     'data' : data,
#                 }
#                 # print(context)
#                 return JsonResponse(context, safe = False)
#             if post_type == 'checkAvailability':
#                 designation = request.POST.get('designation')
#                 context = list(models.Level_Desig.objects.filter(designation__startswith=designation).values())
#                 if len(context)>0:
#                     msg = 'Designation Not Available'
#                     c = '0'
#                 else:
#                     msg = 'Designation Available'
#                     c = '1'
#                 context ={
#                     'msg' : msg,
#                     'color' : c,
#                 }
#                 return JsonResponse(context, safe = False)
#             if post_type == 'saveNewDesignation':
#                 #new_post,new_place,new_station,new_reporting_officer,new_designation,new_contact,new_email,new_remarks
#                 new_post = request.POST.get('new_post')
#                 new_place = request.POST.get('new_place')
#                 new_station = request.POST.get('new_station')
#                 new_reporting_officer = request.POST.get('new_reporting_officer')
#                 new_designation = request.POST.get('new_designation')
#                 if new_reporting_officer == '':
#                     new_reporting_officer = None
#                 else:
#                     reporting_officer = list(models.Level_Desig.objects.filter(designation = new_reporting_officer).values('designation_code'))
#                     if len(reporting_officer) > 0:
#                         new_reporting_officer = reporting_officer[0]['designation_code']
#                     else:
#                         new_reporting_officer = None
                
#                 new_contact = request.POST.get('new_contact')
#                 new_email = request.POST.get('new_email')
#                 new_remarks = request.POST.get('new_remarks')
#                 msg = 'Some Error Exist, contact superadmin'
#                 context = list(models.Level_Desig.objects.filter(designation__startswith=new_designation).values())
#                 if len(context)>0:
#                     msg = 'Designation Not Available'
#                 else:
#                     if models.Level_Desig.objects.filter(official_email_ID=new_email).exists():
#                         msg = 'e-mail id is already used with another designation, Request cannot be processed' 

#                     elif models.designation_Change_Request.objects.filter(status='Forwarded',request_type='New',desigination=new_designation).exists():
#                         msg = 'Request already exist, pull back the existing request to give new request'
#                     elif models.designation_Change_Request.objects.filter(status='Forwarded',request_type='New',current_official_email_ID=new_email).exists():
#                         msg = 'e-mail id is already used with another designation, Request cannot be processed'
#                     else:
#                         data = list(Post_master.objects.filter(post_code=new_post).values('category','pc7_levelmin','pc7_levelmax','department_code_id'))
                        
                        
#                         designation_Change_Request.objects.create(request_by=cuser,request_date=datetime.now(),request_remarks=new_remarks,desigination=new_designation,status='Forwarded',request_type='New',
#                             current_parent_desig_code=new_reporting_officer,current_department_code_id=data[0]['department_code_id'],current_rly_unit_id=new_place,
#                             current_contactnumber=new_contact,current_official_email_ID=new_email,current_station_name=new_station,
#                             current_maxlevel=data[0]['pc7_levelmax'],current_minlevel=data[0]['pc7_levelmin'])
#                         msg = 'success'
#                 return JsonResponse(msg, safe = False)
#             if post_type == 'reportingOfficer':
#                 rly_unit_id = request.POST.get('new_place')
                
#                 rly_unit_det=list(railwayLocationMaster.objects.filter( rly_unit_code= rly_unit_id).values('parent_rly_unit_code'))
#                 rly_unit_det = list(map( lambda x: int(x['parent_rly_unit_code']),rly_unit_det))
#                 rep_officer = list(models.Level_Desig.objects.filter(Q(rly_unit = rly_unit_id) | Q(rly_unit__in = rly_unit_det)).values('designation'))
#                 rep_officer = list(map( lambda x: x['designation'],rep_officer))
                
#                 return JsonResponse(rep_officer, safe = False)  
            
            
#             return JsonResponse({"success":False}, status=400)  

#         details_data = list(models.Level_Desig.objects.filter((Q(rly_unit = rly_unit_id) | Q(rly_unit__in=railwayLocationMaster.objects.filter(parent_rly_unit_code = str(rly_unit_id)).values('rly_unit_code')))).values('designation','rly_unit_id__location_code','rly_unit_id__location_type','empno_id','empno_id__empname','empno_id__empmname','empno_id__emplname','contactnumber','official_email_ID','department_code_id__department_name').order_by('designation'))
#         all_department = list(models.departMast.objects.filter(delete_flag = False).values('department_code','department_name').order_by('department_name'))
#         all_railway = list(railwayLocationMaster.objects.filter((Q(parent_rly_unit_code = str(rly_unit_id)) | Q(rly_unit_code = rly_unit_id)),location_type__in =['RDSO','WS','DIV','RB','ZR','PSU','CTI','PU']).values('rly_unit_code','location_description','location_code','location_type').distinct().order_by('location_code'))
#         level = ['8','9','10','11','12','13','14','15','16','17','18']
#         request_data = models.designation_Change_Request.objects.values().order_by('-request_date')
#         post=Post_master.objects.filter(delete_flag=False).values('post_code').order_by('post_code').distinct('post_code')
#         rly_emp_designation = list(map(lambda x: x['designation'],details_data))
#         pending =[]
#         action_taken=[]

#         if rolelist == 'admin_super':
#             pending = list(models.designation_Change_Request.objects.filter(status='Forwarded').values().order_by('-request_date'))
#             action_taken = list(models.designation_Change_Request.objects.filter(status__in=['Accepted', 'Rejected']).values().order_by('-request_date'))
#         context ={
#             'details_data' : details_data,
#             'all_department': all_department,
#             'all_railway': all_railway,
#             'level' : level,
#             'request_data': request_data,
#             'rolelist': rolelist,
#             'pending': pending,
#             'action_taken':action_taken,
#             'post':post,
#             'rly_emp_designation':rly_emp_designation,
#         }
#         return render(request, "designation_request.html", context)
    
#     # except Exception as e: 
#     #     try:
#     #         m1.error_Table.objects.create(fun_name="designation_request",user_id=request.user,err_details=str(e))
#     #     except:
#     #         print("Internal Error!!!")
#     #     return render(request, "myadmin_errors.html", {})


def designation_request(request):
    # try:
        usermast=m1.MyUser.objects.filter(email=request.user).first()
        user_email = request.user.email
        
        username_admin = list(m1.MyUser.objects.filter(email=request.user, is_admin = True).values('username'))
        if len(username_admin)>0:
            username_admin = username_admin[0]['username']

        rolelist=usermast.user_role
        if str(request.user).startswith('admin'):
            actual_user = str(request.user).split('admin')[1]
        else:
            actual_user = request.user
        
        empnox = AdminMaster.objects.filter(Q(admin_email=actual_user), user_id__isnull=False).values('rly','user_id')
        rly_unit_id=None
        cuser = None
        parent_rly = []
        if empnox:
            rly_unit_id = empnox[0]['rly']
            cuser = empnox[0]['user_id']
            child_rly = list(railwayLocationMaster.objects.filter( parent_rly_unit_code  = str(rly_unit_id)).values('rly_unit_code'))
            if len(child_rly)>0:
                child_rly = list(map(lambda x: x['rly_unit_code'], child_rly))
        if request.method == 'POST' and request.is_ajax():
            post_type = request.POST.get('post_type')
            if post_type == 'similar':
                post = request.POST.get('post')
                current_user = request.user
                if str(request.user).startswith('admin'):
                    actual_user = str(request.user).split('admin')[1]
                else:
                    actual_user = request.user
                empnox = AdminMaster.objects.filter(Q(admin_email=actual_user), user_id__isnull=False).values('rly','user_id')            
                rly_unit_id=None
                if empnox:
                    rly_unit_id = empnox[0]['rly']
                rep_officer = list(models.Level_Desig.objects.filter((Q(rly_unit = rly_unit_id)|Q(rly_unit_id__parent_rly_unit_code  = str(rly_unit_id))),designation__startswith= post+'/').values('designation'))
                rep_officer = list(map( lambda x: x['designation'],rep_officer))
                rep_officer = ', '.join(rep_officer)
                context = {
                    'rep_officer':rep_officer,
                }
                return JsonResponse(context,safe=False)
        
            if post_type == 'emp_details':
                designation = request.POST.get('designation')
                reporting_officer = ''
                emp_details = list(models.Level_Desig.objects.filter(designation = designation).values('d_level','designation','rly_unit_id__location_code','rly_unit_id__location_type','empno_id','empno_id__empname','empno_id__empmname','empno_id__emplname','contactnumber','official_email_ID','department_code__department_name','station_name','empno_id__hrms_id_id','parent_desig_code','status').order_by('-status','designation'))
                if len(emp_details) > 0: 
                    reporting_officer = list(models.Level_Desig.objects.filter(designation_code = emp_details[0]['parent_desig_code']).values('designation'))
                    if len(reporting_officer) > 0:
                        reporting_officer = reporting_officer[0]['designation']
                    else:
                        reporting_officer = ''
                context ={
                    'emp_details':emp_details,
                    'reporting_officer':reporting_officer,
                }
                return JsonResponse(context, safe = False) 
            if post_type == 'desig_search':
                designation = request.POST.get('designation')
                lev_desig_details = list(models.Level_Desig.objects.filter(designation = designation).values('pc7_levelmin','pc7_levelmax','parent_desig_code','department_code','rly_unit_id','official_email_ID','contactnumber','station_name').order_by('status'))
                if len(lev_desig_details) > 0: 
                    for i in range(len(lev_desig_details)):
                        reporting_officer = ''
                        if lev_desig_details[i]['parent_desig_code'] is not None:
                            reporting_officer = list(models.Level_Desig.objects.filter(designation_code = lev_desig_details[i]['parent_desig_code']).values('designation'))
                            if len(reporting_officer) > 0:
                                reporting_officer = reporting_officer[i]['designation']
                            else:
                                reporting_officer = ''
                        lev_desig_details[i].update({'reporting_officer':reporting_officer})
                    
                    rly_unit_id = lev_desig_details[i]['rly_unit_id']
                    rly_unit_det=list(railwayLocationMaster.objects.filter( rly_unit_code= rly_unit_id).values('parent_rly_unit_code'))
                    rly_unit_det = list(map( lambda x: int(x['parent_rly_unit_code']),rly_unit_det))
                    rep_officer = list(models.Level_Desig.objects.filter(Q(rly_unit = rly_unit_id) | Q(rly_unit__in = rly_unit_det)).values('designation'))
                    rep_officer = list(map( lambda x: x['designation'],rep_officer))
                    all_station = list(models.station_master.objects.filter(Q(rly_id_id = rly_unit_id) | Q(div_id_id = rly_unit_id)).values('station_name').distinct().order_by('station_name'))
                    if lev_desig_details[0]['station_name'] is not None:
                        all_station.append({'station_name':lev_desig_details[0]['station_name']})
                
                context = {
                    'lev_desig_details' : lev_desig_details,
                    'rep_officer':rep_officer,
                    'all_station':all_station,
                }
                return JsonResponse(context, safe = False)
            if post_type == 'station':
                val = request.POST.get('val')
                all_station = list(models.station_master.objects.filter(Q(rly_id_id = val) | Q(div_id_id = val)).values('station_name').distinct().order_by('station_name'))
                return JsonResponse(all_station, safe = False)  
            if post_type == 'saveDataChanged':
                msg = 'Please contact superadmin'

                # #designation,pre_email,pre_contact,pre_minlevel,pre_maxlevel,pre_station,pre_place,pre_department,pre_reporting_officer,pre_remarks
                # designation=designation,rly_unit=pre_place,department_code=pre_department,station_name=pre_station,contactnumber=pre_contact,official_email_ID=pre_email
                # ,pc7_levelmin=pre_minlevel,pc7_levelmax=pre_maxlevel,parent_desig_code=pre_reporting_officer
                designation = request.POST.get('designation')
                pre_email = request.POST.get('pre_email')
                pre_contact = request.POST.get('pre_contact')
                pre_minlevel = request.POST.get('pre_minlevel')
                pre_maxlevel = request.POST.get('pre_maxlevel')
                pre_station = request.POST.get('pre_station')
                pre_place = request.POST.get('pre_place')
                pre_department = request.POST.get('pre_department')
                pre_reporting_officer = request.POST.get('pre_reporting_officer')
                pre_remarks = request.POST.get('pre_remarks')

                if pre_reporting_officer is not None or pre_reporting_officer != '':
                    reporting_officer = list(models.Level_Desig.objects.filter(designation = pre_reporting_officer).values('designation_code'))
                    if len(reporting_officer) > 0:
                        pre_reporting_officer = reporting_officer[0]['designation_code']
                    else:
                        pre_reporting_officer = None
                else:
                        pre_reporting_officer = None

                if models.Level_Desig.objects.filter(~Q(designation = designation), official_email_ID=pre_email).exists():
                    msg = 'e-mail id is already used with another designation, Request cannot be processed' 

                elif models.Level_Desig.objects.filter(~Q(designation = designation),contactnumber=pre_contact).exists():
                    msg = 'Contact number is already used with another designation, Request cannot be processed'

                elif models.Level_Desig.objects.filter(designation=designation,rly_unit=pre_place,department_code=pre_department,station_name=pre_station,contactnumber=pre_contact,official_email_ID=pre_email,
                            pc7_levelmin=pre_minlevel,pc7_levelmax=pre_maxlevel,parent_desig_code=pre_reporting_officer).exists():
                    msg = 'All the field having the previous value only, Request cannot be processed'
                
                elif models.designation_Change_Request.objects.filter(status='Forwarded',request_type='Modification',desigination=designation).exists():
                    msg = 'Request already exist, pull back the existing request to give new request' 
                
                else:
                    prevData = list(models.Level_Desig.objects.filter(designation = designation).values())
                    designation_Change_Request.objects.create(request_by=cuser,request_date=datetime.now(),request_remarks=pre_remarks,desigination=designation,status='Forwarded',request_type='Modification',
                        prev_parent_desig_code=prevData[0]['parent_desig_code'],prev_department_code_id=prevData[0]['department_code_id'],prev_rly_unit_id=prevData[0]['rly_unit_id'],prev_contactnumber=prevData[0]['contactnumber'],prev_official_email_ID=prevData[0]['official_email_ID'],prev_station_name=prevData[0]['station_name'],prev_maxlevel=prevData[0]['pc7_levelmax'],prev_minlevel=prevData[0]['pc7_levelmin'],
                        current_parent_desig_code=pre_reporting_officer,current_department_code_id=pre_department,current_rly_unit_id=pre_place,current_contactnumber=pre_contact,current_official_email_ID=pre_email,current_station_name=pre_station,current_maxlevel=pre_maxlevel,current_minlevel=pre_minlevel)
                    msg = 'success'

                return JsonResponse(msg, safe = False)
            if post_type == 'getRecord':
                record_id = request.POST.get('record_id')   
                record_data = list(models.designation_Change_Request.objects.filter(record_id=record_id).values(
                    'record_id','request_by','request_date','request_remarks','desigination','status','request_type','action_by','action_date','action_remarks',
                    'prev_parent_desig_code','prev_department_code__department_name','prev_rly_unit__location_code','prev_rly_unit__location_type','prev_rly_unit__location_description','prev_contactnumber','prev_official_email_ID','prev_station_name','prev_maxlevel','prev_minlevel',
                    'current_parent_desig_code','current_department_code__department_name','current_rly_unit__location_code','current_rly_unit__location_type','current_rly_unit__location_description','current_contactnumber','current_official_email_ID','current_station_name','current_maxlevel','current_minlevel'
                ))
                if len(record_data) > 0: 
                    reporting_officer = list(models.Level_Desig.objects.filter(designation_code = record_data[0]['prev_parent_desig_code']).values('designation'))
                    if len(reporting_officer) > 0:
                        prev_reporting_officer = reporting_officer[0]['designation']
                    else:
                        prev_reporting_officer = ''
                    
                    reporting_officer = list(models.Level_Desig.objects.filter(designation_code = record_data[0]['current_parent_desig_code']).values('designation'))
                    if len(reporting_officer) > 0:
                        curr_reporting_officer = reporting_officer[0]['designation']
                    else:
                        curr_reporting_officer = ''
                    record_data[0].update({'prev_parent_desig_code':prev_reporting_officer,'current_parent_desig_code':curr_reporting_officer})
                
                return JsonResponse(record_data, safe = False)  
            if post_type == 'pullback':
                record_id = request.POST.get('record_id')
                pullBackRemark = request.POST.get('pullBackRemark')
                msg = ''
                if models.designation_Change_Request.objects.filter(record_id=record_id,status='Forwarded').exists():
                    models.designation_Change_Request.objects.filter(record_id=record_id).update(action_by=cuser,action_date=datetime.now(),action_remarks=pullBackRemark,status='Pulled Back')
                    msg = 'Successfully Pulled Back'
                else:
                    msg = 'Failed to Pull Back'
                return JsonResponse(msg, safe = False)
            if post_type == 'accept':
                record_id = request.POST.get('record_id')
                pullBackRemark = request.POST.get('pullBackRemark')
                msg = ''
                if models.designation_Change_Request.objects.filter(record_id=record_id,status='Forwarded').exists():
                    password = 'Admin@123'
                    act_data = list(models.designation_Change_Request.objects.filter(record_id=record_id).values())
                    
                    if act_data[0]['request_type'] != 'New':
                        if act_data[0]['current_parent_desig_code'] is not None:
                            reporting_officer_new_joining = act_data[0]['current_parent_desig_code']
                        else:
                            reporting_officer_new_joining = None
                        prev_details =list(models.Level_Desig.objects.filter(designation = act_data[0]['desigination']).values())
                        
                        div_id_id=list(railwayLocationMaster.objects.filter(rly_unit_code=act_data[0]['current_rly_unit_id'],location_type_desc__in=rlyhead.objects.filter(rltype='HQ').values('rllongdesc')).values('parent_rly_unit_code','location_type'))
                        if len(div_id_id) > 0:
                            hq_id_id = act_data[0]['current_rly_unit_id']
                            div_id_id = None
                        else:
                            hq_id_id=list(railwayLocationMaster.objects.filter(rly_unit_code=act_data[0]['current_rly_unit_id']).values('parent_rly_unit_code','location_type'))
                            
                            if hq_id_id[0]['location_type'] in ['DIV','WS']:
                                div_id_id = act_data[0]['current_rly_unit_id']
                            else:
                                div_id_id = None
                            hq_id_id = hq_id_id[0]['parent_rly_unit_code']
                            
                        models.Level_Desig.objects.filter(designation = act_data[0]['desigination']).update(modified_by=cuser,department_code_id = act_data[0]['current_department_code_id'],
                        parent_desig_code = reporting_officer_new_joining,rly_unit_id=act_data[0]['current_rly_unit_id'],hq_id_id=hq_id_id,div_id_id=div_id_id,
                        pc7_levelmin=act_data[0]['current_minlevel'],pc7_levelmax=act_data[0]['current_maxlevel'],
                        contactnumber=act_data[0]['current_contactnumber'],official_email_ID=act_data[0]['current_official_email_ID'],station_name=act_data[0]['current_station_name'])
                        if m1.MyUser.objects.filter(id = prev_details[0]['desig_user_id']).exists():
                            forgetuser=m1.MyUser.objects.filter(id = prev_details[0]['desig_user_id']).first()
                            if forgetuser:
                                forgetuser.set_password(password)
                                forgetuser.save()
                                m1.MyUser.objects.filter(username=act_data[0]['current_official_email_ID']).update(username=None,is_active= False,email = None)
                                m1.MyUser.objects.filter(id = prev_details[0]['desig_user_id']).update(username=act_data[0]['current_official_email_ID'],is_active= True,email = act_data[0]['current_official_email_ID'])
                        else:
                            id = list(m1.MyUser.objects.values('id').order_by('-id'))
                            if len(id)>0:
                                id = id[0]['id'] + 1
                            else:
                                id = 1
                            newuser = m1.MyUser.objects.create_user(id = id,username=act_data[0]['current_official_email_ID'], password=password,email=act_data[0]['current_official_email_ID'],user_role='user')
                            newuser.is_active= True
                            newuser.is_admin=False
                            newuser.save()
                            myuser_id = list(m1.MyUser.objects.filter(email = act_data[0]['current_official_email_ID']).values('id'))
                            if len(myuser_id)>0:
                                models.Level_Desig.objects.filter(designation = act_data[0]['desigination']).update(desig_user_id = myuser_id[0]['id'])
                        models.designation_Change_Request.objects.filter(record_id=record_id).update(action_by=cuser,action_date=datetime.now(),action_remarks=pullBackRemark,status='Accepted')
                        msg = 'Successfully Accepted the Modification'
                    else:
                        if models.Level_Desig.objects.filter(designation = act_data[0]['desigination']).exists():
                            msg = 'Designation already present'
                        else:
                            if act_data[0]['current_parent_desig_code'] is not None:
                                reporting_officer_new_joining = act_data[0]['current_parent_desig_code']
                            else:
                                reporting_officer_new_joining = None

                            prev_details =list(models.Level_Desig.objects.filter(designation = act_data[0]['desigination']).values())
                            st_post = act_data[0]['desigination'].split('/')[0]
                            data = list(Post_master.objects.filter(post_code=st_post).values('category','pc7_levelmin','pc7_levelmax','department_code_id'))
                            # if len(data)>0:
                            #     category = data[0]['category']
                            # else:
                            #     category = None

                            if len(data)>0:
                                category = data[0]['category']
                            else:
                                if st_post == 'SSE':
                                    category = 'SSE'
                                else:
                                    category = None
                                    
                            if category == 'SSE':
                                if reporting_officer_new_joining is not None:
                                    if models.Level_Desig.objects.filter(delete_flag = False, d_level = category, parent_desig_code = reporting_officer_new_joining).count() > 10:
                                        return JsonResponse('Maximum limit Reached for adding supervisor.', safe = False)


                            if category == 'CRB':
                                role = 'CRB'
                            else:
                                role = 'user'
                            id = list(models.Level_Desig.objects.values('designation_code').order_by('-designation_code'))
                            if len(id)>0:
                                id = id[0]['designation_code'] + 1
                            else:
                                id = 1

                            get_department_name = list(models.departMast.objects.filter(delete_flag = False,department_code=act_data[0]['current_department_code_id']).values('department_name').order_by('department_name'))
                            if len(get_department_name)>0:
                                get_department_name = get_department_name[0]['department_name']
                            else:
                                get_department_name = None

                            hierarchy_level = list(models.category.objects.filter(category=category).values('hierarchy_level'))
                            if len(hierarchy_level) > 0:
                                hierarchy_level = hierarchy_level[0]['hierarchy_level']
                            else:
                                hierarchy_level = None

                            div_id_id=list(railwayLocationMaster.objects.filter(rly_unit_code=act_data[0]['current_rly_unit_id'],location_type_desc__in=rlyhead.objects.filter(rltype='HQ').values('rllongdesc')).values('parent_rly_unit_code','location_type'))
                            if len(div_id_id) > 0:
                                hq_id_id = act_data[0]['current_rly_unit_id']
                                div_id_id = None
                            else:
                                hq_id_id=list(railwayLocationMaster.objects.filter(rly_unit_code=act_data[0]['current_rly_unit_id']).values('parent_rly_unit_code','location_type'))
                                
                                if hq_id_id[0]['location_type'] in ['DIV','WS']:
                                    div_id_id = act_data[0]['current_rly_unit_id']
                                else:
                                    div_id_id = None
                                hq_id_id = hq_id_id[0]['parent_rly_unit_code']

                            models.Level_Desig.objects.create(hq_id_id=hq_id_id,div_id_id=div_id_id,hierarchy_level=hierarchy_level,designation_code = id,effectdate=datetime.now(),status='P',d_level=category,user_role=role,designation = act_data[0]['desigination'],modified_by=cuser,department_code_id = act_data[0]['current_department_code_id'],department = get_department_name,
                            parent_desig_code = reporting_officer_new_joining,rly_unit_id=act_data[0]['current_rly_unit_id'],
                            pc7_levelmin=act_data[0]['current_minlevel'],pc7_levelmax=act_data[0]['current_maxlevel'],
                            contactnumber=act_data[0]['current_contactnumber'],official_email_ID=act_data[0]['current_official_email_ID'],station_name=act_data[0]['current_station_name'])
                           
                            id = list(m1.MyUser.objects.values('id').order_by('-id'))
                            if len(id)>0:
                                id = id[0]['id'] + 1
                            else:
                                id = 1
                            m1.MyUser.objects.filter(email=act_data[0]['current_official_email_ID']).delete()
                            newuser = m1.MyUser.objects.create_user(id = id,username=act_data[0]['current_official_email_ID'], password=password,email=act_data[0]['current_official_email_ID'],user_role='user')
                            newuser.is_active= True
                            newuser.is_admin=False
                            newuser.save()
                            myuser_id = list(m1.MyUser.objects.filter(email = act_data[0]['current_official_email_ID']).values('id'))
                            if len(myuser_id)>0:
                                models.Level_Desig.objects.filter(designation = act_data[0]['desigination']).update(desig_user_id = id)
                            models.designation_Change_Request.objects.filter(record_id=record_id).update(action_by=cuser,action_date=datetime.now(),action_remarks=pullBackRemark,status='Accepted')
                            msg = 'Successfully Accepted the New Designation'

                else:
                    msg = 'Failed to Accept'
                return JsonResponse(msg, safe = False)
            if post_type == 'reject':
                record_id = request.POST.get('record_id')
                pullBackRemark = request.POST.get('pullBackRemark')
                msg = ''
                if models.designation_Change_Request.objects.filter(record_id=record_id,status='Forwarded').exists():
                    models.designation_Change_Request.objects.filter(record_id=record_id).update(action_by=cuser,action_date=datetime.now(),action_remarks=pullBackRemark,status='Rejected')
                    msg = 'Successfully Rejected'
                else:
                    msg = 'Failed to Reject'
                return JsonResponse(msg, safe = False)
            if post_type == 'getPostDetails':
                post = request.POST.get('post')
                context = list(Post_master.objects.filter(post_code=post).values('category','pc7_levelmin','pc7_levelmax','department_code_id__department_name'))
                return JsonResponse(context, safe = False)
            if post_type == 'checkRlyType':
                rly = request.POST.get('rly')
                post = request.POST.get('post')
                location_code = ''
                parent_location_code = ''
                location_type_desc = ''
                createdDesignation = post
                context = list(railwayLocationMaster.objects.filter(rly_unit_code=rly).values('location_code','parent_location_code','location_type_desc'))
                if len(context) > 0:
                    location_code = context[0]['location_code']
                    parent_location_code = context[0]['parent_location_code']
                    location_type_desc = context[0]['location_type_desc']
                if location_type_desc in ['RAILWAY BOARD', 'PRODUCTION UNIT', 'HEAD QUATER', 'PSU', 'INSTITUTE']:
                    createdDesignation = createdDesignation + '/' + location_code
                else:
                    if post != 'DRM':
                        createdDesignation = createdDesignation + '/' + location_code + '/' + parent_location_code
                    else:
                        createdDesignation = createdDesignation + '/' + location_code

                data = list(models.Level_Desig.objects.filter(designation__startswith=createdDesignation).values('designation'))
                if len(data) > 0:
                    data = list(map( lambda x: x['designation'],data))
                    data = ', '.join(data)
                else:
                    data = ''
                context = {
                    'createdDesignation' : createdDesignation,
                    'data' : data,
                }
                # print(context)
                return JsonResponse(context, safe = False)
            if post_type == 'checkAvailability':
                designation = request.POST.get('designation')
                context = list(models.Level_Desig.objects.filter(designation__startswith=designation).values())
                if len(context)>0:
                    msg = 'Designation Not Available'
                    c = '0'
                else:
                    msg = 'Designation Available'
                    c = '1'
                context ={
                    'msg' : msg,
                    'color' : c,
                }
                return JsonResponse(context, safe = False)
            if post_type == 'saveNewDesignation':
                #new_post,new_place,new_station,new_reporting_officer,new_designation,new_contact,new_email,new_remarks
                new_post = request.POST.get('new_post')
                new_place = request.POST.get('new_place')
                new_station = request.POST.get('new_station')
                new_reporting_officer = request.POST.get('new_reporting_officer')
                new_designation = request.POST.get('new_designation')
                if new_reporting_officer == '':
                    new_reporting_officer = None
                else:
                    reporting_officer = list(models.Level_Desig.objects.filter(designation = new_reporting_officer).values('designation_code'))
                    if len(reporting_officer) > 0:
                        new_reporting_officer = reporting_officer[0]['designation_code']
                    else:
                        new_reporting_officer = None
                
                new_contact = request.POST.get('new_contact')
                new_email = request.POST.get('new_email')
                new_remarks = request.POST.get('new_remarks')
                msg = 'Some Error Exist, contact superadmin'
                context = list(models.Level_Desig.objects.filter(designation__startswith=new_designation).values())
                if len(context)>0:
                    msg = 'Designation Not Available'
                else:
                    if models.Level_Desig.objects.filter(official_email_ID=new_email).exists():
                        msg = 'e-mail id is already used with another designation, Request cannot be processed' 

                    elif models.designation_Change_Request.objects.filter(status='Forwarded',request_type='New',desigination=new_designation).exists():
                        msg = 'Request already exist, pull back the existing request to give new request'
                    elif models.designation_Change_Request.objects.filter(status='Forwarded',request_type='New',current_official_email_ID=new_email).exists():
                        msg = 'e-mail id is already used with another designation, Request cannot be processed'
                    else:
                        data = list(Post_master.objects.filter(post_code=new_post).values('category','pc7_levelmin','pc7_levelmax','department_code_id'))
                        
                        
                        designation_Change_Request.objects.create(request_by=cuser,request_date=datetime.now(),request_remarks=new_remarks,desigination=new_designation,status='Forwarded',request_type='New',
                            current_parent_desig_code=new_reporting_officer,current_department_code_id=data[0]['department_code_id'],current_rly_unit_id=new_place,
                            current_contactnumber=new_contact,current_official_email_ID=new_email,current_station_name=new_station,
                            current_maxlevel=data[0]['pc7_levelmax'],current_minlevel=data[0]['pc7_levelmin'])
                        msg = 'success'
                return JsonResponse(msg, safe = False)
            if post_type == 'reportingOfficer':
                rly_unit_id = request.POST.get('new_place')
                
                rly_unit_det=list(railwayLocationMaster.objects.filter( rly_unit_code= rly_unit_id).values('parent_rly_unit_code'))
                rly_unit_det = list(map( lambda x: int(x['parent_rly_unit_code']),rly_unit_det))
                rep_officer = list(models.Level_Desig.objects.filter(Q(rly_unit = rly_unit_id) | Q(rly_unit__in = rly_unit_det)).values('designation'))
                rep_officer = list(map( lambda x: x['designation'],rep_officer))
                
                return JsonResponse(rep_officer, safe = False)  
            
            
            return JsonResponse({"success":False}, status=400)  

        details_data = list(models.Level_Desig.objects.filter((Q(rly_unit = rly_unit_id) | Q(rly_unit__in=railwayLocationMaster.objects.filter(parent_rly_unit_code = str(rly_unit_id)).values('rly_unit_code')))).values('designation','rly_unit_id__location_code','rly_unit_id__location_type','empno_id','empno_id__empname','empno_id__empmname','empno_id__emplname','contactnumber','official_email_ID','department_code_id__department_name').order_by('designation'))
        all_department = list(models.departMast.objects.filter(delete_flag = False).values('department_code','department_name').order_by('department_name'))
        all_railway = list(railwayLocationMaster.objects.filter((Q(parent_rly_unit_code = str(rly_unit_id)) | Q(rly_unit_code = rly_unit_id)),location_type__in =['RDSO','WS','DIV','RB','ZR','PSU','CTI','PU']).values('rly_unit_code','location_description','location_code','location_type').distinct().order_by('location_code'))
        level = ['8','9','10','11','12','13','14','15','16','17','18']
        request_data = list(models.designation_Change_Request.objects.values().order_by('-request_date'))
        post=Post_master.objects.filter(delete_flag=False).values('post_code').order_by('post_code').distinct('post_code')
        rly_emp_designation = list(map(lambda x: x['designation'],details_data))
        pending =[]
        action_taken=[]
        if username_admin:
            request_data = list(models.designation_Change_Request.objects.filter(Q(request_by=username_admin)).order_by('-request_date'))

        if rolelist == 'admin_super':
            pending = list(models.designation_Change_Request.objects.filter(status='Forwarded').values().order_by('-request_date'))
            action_taken = list(models.designation_Change_Request.objects.filter(status__in=['Accepted', 'Rejected']).values().order_by('-request_date'))
        context ={
            'details_data' : details_data,
            'all_department': all_department,
            'all_railway': all_railway,
            'level' : level,
            'request_data': request_data,
            'rolelist': rolelist,
            'pending': pending,
            'action_taken':action_taken,
            'post':post,
            'rly_emp_designation':rly_emp_designation,
        }
        return render(request, "designation_request.html", context)
    
    # except Exception as e: 
    #     try:
    #         m1.error_Table.objects.create(fun_name="designation_request",user_id=request.user,err_details=str(e))
    #     except:
    #         print("Internal Error!!!")
    #     return render(request, "myadmin_errors.html", {})



def feedback_report(request):
    

    if request.method == 'GET' and request.is_ajax():
        ajaxname = request.GET.get('ajaxname')
        category = request.GET.get('category')
        user = models.Level_Desig.objects.get(official_email_ID=request.user)
        sub_category = tuple(m1.custom_menu.objects.filter(role=user.user_role,perent_id = category).values_list('menu',flat = True))
        # print(sub_category)
        return JsonResponse({'sub_category':sub_category},safe=False)
    if request.method == 'GET':
        
        if models.Level_Desig.objects.filter(official_email_ID=request.user).exists():
            # print('inside get')
            user = models.Level_Desig.objects.get(official_email_ID=request.user)

            data = m1.custom_menu.objects.filter(role=user.user_role,perent_id = 0).order_by('m_id')
            category = list(data.values('menu','m_id'))
 
            rly = ['RAILWAY BOARD','HEAD QUATER','PRODUCTION UNIT','PSU','INSTITUTE','RDSO']
            if user.rly_unit.location_type_desc in rly:
                rly = user.rly_unit.location_code
                div = ''
            else:
                rly = user.rly_unit.parent_location_code
                div = user.rly_unit.location_code
            # print("LKS;LDKF;E",rly,div)
            models.railwayLocationMaster.objects.filter(parent_location_code = user.rly_unit_id)
            '''SHOW DATA ON TABLE'''
            pending_feedback_data = models.Feedback_Report.objects.filter(status = 0, level_desig = user).order_by('-reported_date')
            resolved_feedback_data = models.Feedback_Report.objects.filter(status = 1, level_desig = user).order_by('-reported_date')
            inprogress_feedback_data = models.Feedback_Report.objects.filter(status = 2, level_desig = user).order_by('-reported_date')
            notfeasible_feedback_data = models.Feedback_Report.objects.filter(status = 3, level_desig = user).order_by('-reported_date')
            # print('pending_feedback_data',pending_feedback_data)
            # print('resolved_feedback_data',resolved_feedback_data)
            context = {
                'email':user.official_email_ID,
                'desig':user.designation,
                'desig_code':user.designation_code,
                'category':category,
                "pending_feedback_data":pending_feedback_data,
                "resolved_feedback_data":resolved_feedback_data,
                "inprogress_feedback_data":inprogress_feedback_data,
                "notfeasible_feedback_data":notfeasible_feedback_data,
                'rly':rly,
                'div':div,
            }
            return render(request, "feedback_report.html",context)

        else:
            messages.info(request,'User Does Not Exists')
            return render(request, "myadmin_errors.html", {}) 
    
    if request.method == 'POST':
        category = request.POST.get('category')
        sub_category = request.POST.get('sub_category')
        issue_detials = request.POST.get('issue_detials')
        desig_code = request.POST.get('desig')
        feedbackType = request.POST.get('feedbackType')
        desig = models.Level_Desig.objects.get(designation_code=desig_code)
        # image = request.POST.get('image')
        
        if request.FILES.get('image'):
            image = request.FILES.get('image')
        else:
            image = None
        category = m1.custom_menu.objects.get(role=desig.user_role,m_id = category).menu
        models.Feedback_Report.objects.create(category = category,sub_category =sub_category, description = issue_detials,
            images = image,level_desig = desig,feedback_type = feedbackType)
        # print(image)
        messages.info(request,'Data saved successfully.')
        return redirect('feedback_report')

        # models.Feedback_Report.obejcts.create()


# def CrisFeedbackReport(request):
#     if request.method == 'GET' and request.is_ajax():
#         ajaxname = request.GET.get('ajaxname')
#         if ajaxname == 'viewfeedback':
#             id = request.GET.get('id')
#             data = list(models.Feedback_Report.objects.filter(id = id).values('id','category','sub_category',
#                         'description','reported_date','images','level_desig__rly_unit__location_type_desc',
#                         'level_desig__rly_unit__parent_location_code','level_desig__rly_unit__location_code',
#                         'level_desig__official_email_ID','level_desig__designation','level_desig__contactnumber',
#                         'status','feedback_type'))
#             # print(data)
#             rly = ['RAILWAY BOARD','HEAD QUATER','PRODUCTION UNIT','PSU','INSTITUTE','RDSO']
#             if data[0]['level_desig__rly_unit__location_type_desc'] in rly:
#                 rly = data[0]['level_desig__rly_unit__location_code']
#                 div = ''
#             else:
#                 rly = data[0]['level_desig__rly_unit__parent_location_code']
#                 div = data[0]['level_desig__rly_unit__location_code']
            
#             return JsonResponse({'data':data,'rly':rly,'div':div},safe = False)
#     if request.method == 'POST':
#         hiddenId = request.POST.get('hiddenId')
#         cris_remarks = request.POST.get('cris_remarks')
#         status = request.POST.get('status')
        
#         models.Feedback_Report.objects.filter(id = hiddenId).update(cris_remarks = cris_remarks,status = status, cris_remarks_date=datetime.now())
#         return redirect('CrisFeedbackReport')
    
#     # data to show in datatable
#     # data = models.Feedback_Report.objects.all().order_by('-reported_date')
#     pending_feedback_data = models.Feedback_Report.objects.filter(status = 0).order_by('-reported_date')
#     resolved_feedback_data = models.Feedback_Report.objects.filter(status = 1).order_by('-reported_date')
#     inprogress_feedback_data = models.Feedback_Report.objects.filter(status = 2).order_by('-reported_date')
#     notfeasible_feedback_data = models.Feedback_Report.objects.filter(status = 3).order_by('-reported_date')
#     context = {
#         # "data":data,
#         'pending_feedback_data':pending_feedback_data,
#         'resolved_feedback_data':resolved_feedback_data,
#         'inprogress_feedback_data':inprogress_feedback_data,
#         'notfeasible_feedback_data':notfeasible_feedback_data
#     }
#     return render(request, "cris_feedback_form.html",context)



# def CrisFeedbackReport(request):
#     if request.method == 'GET' and request.is_ajax():
#         ajaxname = request.GET.get('ajaxname')
#         if ajaxname == 'viewfeedback':
#             id = request.GET.get('id')
#             data = list(models.Feedback_Report.objects.filter(id = id).values('id','category','sub_category',
#                         'description','reported_date','images','level_desig__rly_unit__location_type_desc',
#                         'level_desig__rly_unit__parent_location_code','level_desig__rly_unit__location_code',
#                         'level_desig__official_email_ID','level_desig__designation','level_desig__contactnumber',
#                         'status','feedback_type'))
#             # print(data)
#             rly = ['RAILWAY BOARD','HEAD QUATER','PRODUCTION UNIT','PSU','INSTITUTE','RDSO']
#             if data[0]['level_desig__rly_unit__location_type_desc'] in rly:
#                 rly = data[0]['level_desig__rly_unit__location_code']
#                 div = ''
#             else:
#                 rly = data[0]['level_desig__rly_unit__parent_location_code']
#                 div = data[0]['level_desig__rly_unit__location_code']
            
#             return JsonResponse({'data':data,'rly':rly,'div':div},safe = False)
#     if request.method == 'POST':
#         hiddenId = request.POST.get('hiddenId')
#         cris_remarks = request.POST.get('cris_remarks')
#         status = request.POST.get('status')
#         models.Feedback_Report.objects.filter(id = hiddenId).update(cris_remarks = cris_remarks,status = status)
#         return redirect('CrisFeedbackReport')
    
#     # data to show in datatable
#     # data = models.Feedback_Report.objects.all().order_by('-reported_date')
#     rly = ['RAILWAY BOARD','HEAD QUATER','PRODUCTION UNIT','PSU','INSTITUTE','RDSO']

#     ''' pending feedback '''
#     pending_feedback_data = list(models.Feedback_Report.objects.filter(status = 0).values('id','category','sub_category'
#                             ,'feedback_type','description','reported_date','cris_remarks','status','images',
#                             'level_desig__rly_unit__location_type_desc',
#                             'level_desig__rly_unit__parent_location_code','level_desig__rly_unit__location_code').order_by('-reported_date'))
    
#     for data in range(len(pending_feedback_data)):
#         # print("data",pending_feedback_data[data])
#         if pending_feedback_data[data]['level_desig__rly_unit__location_type_desc'] in rly:
#             pending_feedback_data[data]['rly'] = pending_feedback_data[data]['level_desig__rly_unit__location_code']
#             pending_feedback_data[data]['div'] = ''
#         else:
#             pending_feedback_data[data]['rly'] = pending_feedback_data[data]['level_desig__rly_unit__parent_location_code']
#             pending_feedback_data[data]['div'] = pending_feedback_data[data]['level_desig__rly_unit__location_code']

#     ''' RESOLVED FEEDBACK '''
#     resolved_feedback_data = list(models.Feedback_Report.objects.filter(status = 1).values('id','category','sub_category'
#                             ,'feedback_type','description','reported_date','cris_remarks','status','images',
#                             'level_desig__rly_unit__location_type_desc',
#                             'level_desig__rly_unit__parent_location_code','level_desig__rly_unit__location_code').order_by('-reported_date'))
#     for data in range(len(resolved_feedback_data)):
#         # print("data",resolved_feedback_data[data])
#         if resolved_feedback_data[data]['level_desig__rly_unit__location_type_desc'] in rly:
#             resolved_feedback_data[data]['rly'] = resolved_feedback_data[data]['level_desig__rly_unit__location_code']
#             resolved_feedback_data[data]['div'] = ''
#         else:
#             resolved_feedback_data[data]['rly'] = resolved_feedback_data[data]['level_desig__rly_unit__parent_location_code']
#             resolved_feedback_data[data]['div'] = resolved_feedback_data[data]['level_desig__rly_unit__location_code']

#     ''' IN PROGRESS FEEDBACK '''
#     inprogress_feedback_data = list(models.Feedback_Report.objects.filter(status = 2).values('id','category','sub_category'
#                             ,'feedback_type','description','reported_date','cris_remarks','status','images',
#                             'level_desig__rly_unit__location_type_desc',
#                             'level_desig__rly_unit__parent_location_code','level_desig__rly_unit__location_code').order_by('-reported_date'))
#     for data in range(len(inprogress_feedback_data)):
#         # print("data",inprogress_feedback_data[data])
#         if inprogress_feedback_data[data]['level_desig__rly_unit__location_type_desc'] in rly:
#             inprogress_feedback_data[data]['rly'] = inprogress_feedback_data[data]['level_desig__rly_unit__location_code']
#             inprogress_feedback_data[data]['div'] = ''
#         else:
#             inprogress_feedback_data[data]['rly'] = inprogress_feedback_data[data]['level_desig__rly_unit__parent_location_code']
#             inprogress_feedback_data[data]['div'] = inprogress_feedback_data[data]['level_desig__rly_unit__location_code']
    
#     ''' NOT FEASIBLE FEEDBACK '''
#     notfeasible_feedback_data = list(models.Feedback_Report.objects.filter(status = 3).values('id','category','sub_category'
#                             ,'feedback_type','description','reported_date','cris_remarks','status','images',
#                             'level_desig__rly_unit__location_type_desc',
#                             'level_desig__rly_unit__parent_location_code','level_desig__rly_unit__location_code').order_by('-reported_date'))
#     for data in range(len(notfeasible_feedback_data)):
#         # print("data",notfeasible_feedback_data[data])
#         if notfeasible_feedback_data[data]['level_desig__rly_unit__location_type_desc'] in rly:
#             notfeasible_feedback_data[data]['rly'] = notfeasible_feedback_data[data]['level_desig__rly_unit__location_code']
#             notfeasible_feedback_data[data]['div'] = ''
#         else:
#             notfeasible_feedback_data[data]['rly'] = notfeasible_feedback_data[data]['level_desig__rly_unit__parent_location_code']
#             notfeasible_feedback_data[data]['div'] = notfeasible_feedback_data[data]['level_desig__rly_unit__location_code']

#     context = {
#         # "data":data,
#         'pending_feedback_data':pending_feedback_data,
#         'resolved_feedback_data':resolved_feedback_data,
#         'inprogress_feedback_data':inprogress_feedback_data,
#         'notfeasible_feedback_data':notfeasible_feedback_data
#     }
#     return render(request, "cris_feedback_form.html",context)



def CrisFeedbackReport(request):

    if request.method == 'GET' and request.is_ajax():
        ajaxname = request.GET.get('ajaxname')

        
        if ajaxname == 'viewfeedback':
            id = request.GET.get('id')
            data = list(models.Feedback_Report.objects.filter(id = id).values('id','category','sub_category',
                        'description','reported_date','images','level_desig__rly_unit__location_type_desc',
                        'level_desig__rly_unit__parent_location_code','level_desig__rly_unit__location_code',
                        'level_desig__official_email_ID','level_desig__designation','level_desig__contactnumber',
                        'status','feedback_type'))
            # # print(data)
            rly = ['RAILWAY BOARD','HEAD QUATER','PRODUCTION UNIT','PSU','INSTITUTE','RDSO']
            if data[0]['level_desig__rly_unit__location_type_desc'] in rly:
                rly = data[0]['level_desig__rly_unit__location_code']
                div = ''
            else:
                rly = data[0]['level_desig__rly_unit__parent_location_code']
                div = data[0]['level_desig__rly_unit__location_code']
            
            return JsonResponse({'data':data,'rly':rly,'div':div},safe = False)

        if ajaxname == 'filterpending':
            location_code = request.GET.get('location_code')
            location_type = request.GET.get('location_type')
            category = request.GET.get('category')
            created_on = request.GET.get("created_on")
            # # print("dsfasdfsd",location_code,location_type,category,created_on)
            datefrom = datetime.strptime(created_on.split('to')[0].strip(),'%d/%m/%y')
            dateto = datetime.strptime(created_on.split('to')[1].strip(),'%d/%m/%y')
            if location_type:
                # print('if data')
                filter_data = tuple(models.Feedback_Report.objects.filter(
                                    level_desig__rly_unit__rly_unit_code = location_type,      
                                     category__in = category,status = 0,
                                    reported_date__date__range = [datefrom,dateto]).values('id','level_desig__designation','feedback_type',
                                                                'category','sub_category','description','images','cris_remarks','reported_date',
                                                                'status'))
                
            else:
                filter_data = tuple(models.Feedback_Report.objects.filter(
                Q(level_desig__rly_unit__parent_rly_unit_code = location_code)|Q(level_desig__rly_unit__rly_unit_code = location_code),
                                category__in =  category,status = 0,
                                reported_date__date__range = [datefrom,dateto]).values('id','level_desig__designation','feedback_type',
                                                            'category','sub_category','description','images','cris_remarks','reported_date',
                                                            'status'))
            
            # if location_type:
            #     filter_data = tuple(models.Feedback_Report.objects.filter(
            #                         level_desig__rly_unit = location_type,      
            #                          category = category,status = 0,
            #                         reported_date__date__range = [datefrom,dateto]).values('id','level_desig__designation','feedback_type',
            #                                                     'category','sub_category','description','images','cris_remarks','reported_date',
            #                                                     'status'))
            # else:
            #     filter_data = tuple(models.Feedback_Report.objects.filter(
            #     (Q(level_desig__rly_unit__parent_rly_unit_code = location_code)|Q(level_desig__rly_unit = location_code)),
            #                     category = category,status = 0,
            #                     reported_date__date__range = [datefrom,dateto]).values('id','level_desig__designation','feedback_type',
            #                                                 'category','sub_category','description','images','cris_remarks','reported_date',
            #                                                 'status'))
            #     # print('filter_data',filter_data)
            return JsonResponse({'filter_data':filter_data},safe = False)


    if request.method == 'POST':
        hiddenId = request.POST.get('hiddenId')
        cris_remarks = request.POST.get('cris_remarks')
        status = request.POST.get('status')
        image = request.POST.get('image')
        models.Feedback_Report.objects.filter(id = hiddenId).update(cris_image = image,cris_remarks = cris_remarks,status = status)
        return redirect('CrisFeedbackReport')
    
    # data to show in datatable
    # data = models.Feedback_Report.objects.all().order_by('-reported_date')
    rly = ['RAILWAY BOARD','HEAD QUATER','PRODUCTION UNIT','PSU','INSTITUTE','RDSO']

    ''' pending feedback '''
    pending_feedback_data = list(models.Feedback_Report.objects.filter(status = 0).values('id','category','sub_category'
                            ,'feedback_type','description','reported_date','cris_remarks','status','images',
                            'level_desig__rly_unit__location_type_desc','level_desig__designation',
                            'level_desig__rly_unit__parent_location_code','level_desig__rly_unit__location_code').order_by('-reported_date'))
    
    for data in range(len(pending_feedback_data)):
        # print("data",pending_feedback_data[data])
        if pending_feedback_data[data]['level_desig__rly_unit__location_type_desc'] in rly:
            pending_feedback_data[data]['rly'] = pending_feedback_data[data]['level_desig__rly_unit__location_code']
            pending_feedback_data[data]['div'] = ''
        else:
            pending_feedback_data[data]['rly'] = pending_feedback_data[data]['level_desig__rly_unit__parent_location_code']
            pending_feedback_data[data]['div'] = pending_feedback_data[data]['level_desig__rly_unit__location_code']

    ''' RESOLVED FEEDBACK '''
    resolved_feedback_data = list(models.Feedback_Report.objects.filter(status = 1).values('id','category','sub_category'
                            ,'feedback_type','description','reported_date','cris_remarks','status','images',
                            'level_desig__rly_unit__location_type_desc','level_desig__designation',
                            'level_desig__rly_unit__parent_location_code','level_desig__rly_unit__location_code').order_by('-reported_date'))
    for data in range(len(resolved_feedback_data)):
        # print("data",resolved_feedback_data[data])
        if resolved_feedback_data[data]['level_desig__rly_unit__location_type_desc'] in rly:
            resolved_feedback_data[data]['rly'] = resolved_feedback_data[data]['level_desig__rly_unit__location_code']
            resolved_feedback_data[data]['div'] = ''
        else:
            resolved_feedback_data[data]['rly'] = resolved_feedback_data[data]['level_desig__rly_unit__parent_location_code']
            resolved_feedback_data[data]['div'] = resolved_feedback_data[data]['level_desig__rly_unit__location_code']

    ''' IN PROGRESS FEEDBACK '''
    inprogress_feedback_data = list(models.Feedback_Report.objects.filter(status = 2).values('id','category','sub_category'
                            ,'feedback_type','description','reported_date','cris_remarks','status','images',
                            'level_desig__rly_unit__location_type_desc','level_desig__designation',
                            'level_desig__rly_unit__parent_location_code','level_desig__rly_unit__location_code').order_by('-reported_date'))
    for data in range(len(inprogress_feedback_data)):
        # print("data",inprogress_feedback_data[data])
        if inprogress_feedback_data[data]['level_desig__rly_unit__location_type_desc'] in rly:
            inprogress_feedback_data[data]['rly'] = inprogress_feedback_data[data]['level_desig__rly_unit__location_code']
            inprogress_feedback_data[data]['div'] = ''
        else:
            inprogress_feedback_data[data]['rly'] = inprogress_feedback_data[data]['level_desig__rly_unit__parent_location_code']
            inprogress_feedback_data[data]['div'] = inprogress_feedback_data[data]['level_desig__rly_unit__location_code']
    
    ''' NOT FEASIBLE FEEDBACK '''
    notfeasible_feedback_data = list(models.Feedback_Report.objects.filter(status = 3).values('id','category','sub_category'
                            ,'feedback_type','description','reported_date','cris_remarks','status','images',
                            'level_desig__rly_unit__location_type_desc','level_desig__designation',
                            'level_desig__rly_unit__parent_location_code','level_desig__rly_unit__location_code').order_by('-reported_date'))
    for data in range(len(notfeasible_feedback_data)):
        # print("data",notfeasible_feedback_data[data])
        if notfeasible_feedback_data[data]['level_desig__rly_unit__location_type_desc'] in rly:
            notfeasible_feedback_data[data]['rly'] = notfeasible_feedback_data[data]['level_desig__rly_unit__location_code']
            notfeasible_feedback_data[data]['div'] = ''
        else:
            notfeasible_feedback_data[data]['rly'] = notfeasible_feedback_data[data]['level_desig__rly_unit__parent_location_code']
            notfeasible_feedback_data[data]['div'] = notfeasible_feedback_data[data]['level_desig__rly_unit__location_code']


    ''' RLY, DIV, CATEGORY AND DATE FOR FILTER '''
    list1=models.railwayLocationMaster.objects.filter(Q(location_type_desc='RAILWAY BOARD')|Q(location_type_desc='HEAD QUATER')|Q(location_type_desc='PRODUCTION UNIT')|Q(location_type_desc='PSU')|Q(location_type_desc='INSTITUTE')).values('location_code','rly_unit_code').order_by('location_code')
    list2=[]
    for i in list1:
        # # print(i['location_code'],'_________')
        list2.append({'location_code':i['location_code'],'rly_unit_code':i['rly_unit_code']})

    list3=models.railwayLocationMaster.objects.filter(Q(location_type_desc='DIVISION')|Q(location_type_desc='WORKSHOP')|Q(location_type_desc='OFFICE')|Q(location_type_desc='STORE')|Q(location_type_desc='CONSTRUCTION')).values('location_code','location_type','rly_unit_code').order_by('location_code')
    list4=[]
    for i in list3:
        # # print(i['location_code'],'_________')
        list4.append({'location_code':i['location_code'],'location_type':i['location_type'],'rly_unit_code':i['rly_unit_code']})  

    category = m1.custom_menu.objects.filter(perent_id = 0).values_list('menu').distinct('menu').order_by('menu')

    app_date = date(2022,9,11)
    app_date = app_date.strftime('%d/%m/%y')
    curr_date = date.today()
    curr_date = curr_date.strftime('%d/%m/%y')
    # print(app_date,curr_date)
    new_date = app_date+' to '+curr_date
    context = {
        'zone':list2,
        'division':list4,
        'category':category,
        'new_date':new_date,
        'pending_feedback_data':pending_feedback_data,
        'resolved_feedback_data':resolved_feedback_data,
        'inprogress_feedback_data':inprogress_feedback_data,
        'notfeasible_feedback_data':notfeasible_feedback_data
        
    }
    return render(request, "cris_feedback_form.html",context)

        
  
from django.db import transaction
@transaction.atomic       
def nonrly_signup(request):

    if request.method == 'POST' and request.is_ajax():
        typ = request.POST.get('typ')
        if typ == 'checkemp':
            empno = request.POST.get('empno')
            check = m1.empmast.objects.filter(empno = empno).exists()
            return JsonResponse(check, safe = False)
        if typ == 'otp':
            import random
            from django.core.mail import send_mail
            digits = "0123456789"
            OTP = ""
            for i in range(6) :
                OTP += digits[math.floor(random.random() * 10)]

            email = request.POST.get('email')
            htmlgen = 'Your OTP is ' + OTP

            
            send_mail(
                        'OTP request for Non-Railway User', 
                        htmlgen,
                        'mfgcris@cris.org.in', 
                        [email],
                        fail_silently=False,   
                    )  
            first = email[:5] + '****@'
            email = email.split('@')
            last = email[len(email) - 1]
            context = {
                'first' : first,
                'last' : last,
                'otp':OTP,
            }
            return JsonResponse(context, safe = False)
        if typ == 'details':
            railway = request.POST.get('railway')
            division = request.POST.get('division')
            department = request.POST.get('department')  
            selectType = request.POST.get('selectType')
            all_division = []
            all_designation = []
            all_station = []
            if selectType in ['railway']:
                if railway != 'RB':
                    all_division = list(railwayLocationMaster.objects.filter(parent_location_code = railway).values_list('location_code', flat = True))  #rly_unit_code
                if department == '':
                    department=list(departMast.objects.filter(delete_flag = False).values_list('department_code'))
                else:
                    department=list(departMast.objects.filter(department_name = department).values_list('department_code'))
                
                division = list(railwayLocationMaster.objects.filter(Q(parent_location_code = railway) | Q(location_code = railway)).values_list('rly_unit_code', flat = True))
                all_designation = list(Level_Desig.objects.filter(rly_unit__in = division, department_code__in = department).values_list('designation', flat = True))
                all_station = list(models.station_master.objects.filter(Q(rly_id_id__in = division) | Q(div_id_id__in = division)).values_list('station_name', flat = True).distinct().order_by('station_name'))
                
            elif selectType in ['division']:
                if department == '':
                    department=list(departMast.objects.filter(delete_flag = False).values_list('department_code'))
                else:
                    department=list(departMast.objects.filter(department_name = department).values_list('department_code'))
                
                division = list(railwayLocationMaster.objects.filter(Q(location_code = division)).values_list('rly_unit_code', flat = True))
                all_designation = list(Level_Desig.objects.filter(rly_unit__in = division, department_code__in = department).values_list('designation', flat = True))
                all_station = list(models.station_master.objects.filter(Q(rly_id_id__in = division) | Q(div_id_id__in = division)).values_list('station_name', flat = True).distinct().order_by('station_name'))

            else:
                if department == '':
                    department=list(departMast.objects.filter(delete_flag = False).values_list('department_code'))
                else:
                    department=list(departMast.objects.filter(department_name = department).values_list('department_code'))
                if division == '':
                    division = list(railwayLocationMaster.objects.filter(Q(parent_location_code = railway) | Q(location_code = railway)).values_list('rly_unit_code', flat = True))
                else:
                    division = list(railwayLocationMaster.objects.filter(Q(location_code = division)).values_list('rly_unit_code', flat = True))

                all_designation = list(Level_Desig.objects.filter(rly_unit__in = division, department_code__in = department).values_list('designation', flat = True))
                all_station = list(models.station_master.objects.filter(Q(rly_id_id__in = division) | Q(div_id_id__in = division)).values_list('station_name', flat = True).distinct().order_by('station_name'))

            context = {
                'all_division' : all_division,
                'all_designation' : all_designation,
                'all_station' : all_station,

            }
            return JsonResponse(context, safe=False)
        return JsonResponse({"success":False}, status=400)
    if request.method == 'POST':
        email = request.POST.get('email')
        mobno = request.POST.get('mobno')
        empno = request.POST.get('empno')

        fname = request.POST.get('fname')
        mname = request.POST.get('mname')
        if mname == '':
            mname = None
        lname = request.POST.get('lname')
        if lname == '':
            lname = None

        rly = request.POST.get('rly')
        division = request.POST.get('division')
        department=request.POST.get('department')
       
        desig1 = request.POST.get('desig1')
        desig2 = request.POST.get('desig2')
        station = request.POST.get('station')
         

        orderid = request.POST.get('orderid')
        if orderid == '':
            orderid = None
        rlygroup = request.POST.get('rlygroup')
        paylevel = request.POST.get('paylevel')

        import random
        import string
        import datetime
        ref_no = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        id = empmast_nonrly.objects.aggregate(Max('id'))
        if id['id__max'] is None:
            id = 1
        else:
            if id['id__max'] > 99999:
                id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
            else:
                id = id['id__max'] + 1
        
        currentzone = None
        currentunitdivision = None
        rl_type = None
        rly_id = None
        d1 = list(railwayLocationMaster.objects.filter(location_code = rly).values('location_code','rly_unit_code','location_type_desc'))
        if len(d1) > 0:
            currentzone = d1[0]['location_code']
            rl_type = d1[0]['location_type_desc']
            rly_id = d1[0]['rly_unit_code']
        if division != '' :
            d1 = list(railwayLocationMaster.objects.filter(location_code = division).values('location_code','rly_unit_code','location_type_desc'))
            if len(d1) > 0:
                currentunitdivision = d1[0]['location_code']
                rl_type = d1[0]['location_type_desc']
                rly_id = d1[0]['rly_unit_code']



        ref_no = ref_no + (str(id).zfill(5))
        empmast_nonrly.objects.create(
            ref_no = ref_no,id = id,orderid = orderid,empno = empno,empname = fname,empmname = mname,emplname = lname,email = email,contactno = mobno,
            railwaygroup = rlygroup,pc7_level = paylevel,designation = desig1 ,desig_longdesc = desig2,station_des = station, dept_desc = department
            ,currentzone = currentzone, currentunitdivision = currentunitdivision,rl_type = rl_type, rly_id_id = rly_id,profile_modified_on = datetime.datetime.now()
        )

        htmlgen = 'Your Refrence Number ' + ref_no
        from django.core.mail import send_mail
        # print(htmlgen)
        send_mail(
                    'Non-Railway User registration Refrence number', 
                    htmlgen,
                    'mfgcris@cris.org.in', 
                    [email],
                    fail_silently=False,   
                )  
        
        messages.success(request, 'Registered Successfully, Refrence number is sent on email.')

    
    level = [i for i in range(1,19)]
    all_railway=railwayLocationMaster.objects.filter(location_type_desc__in=['HEAD QUATER', 'RAILWAY BOARD', 'RDSO', 'PRODUCTION UNIT', 'OFFICE', 'PSU']).values('location_code')
    all_department=departMast.objects.filter(delete_flag=False).values('department_name').order_by('department_name').distinct()
    
    context = {
        'all_railway':all_railway,
        'all_department':all_department,
        'level':level,
    }
    return render(request, 'nonrly_signup.html',context)


def nonrly_signup_accept(request):
    import datetime
    if 'AnonymousUser' == str(request.user):
        messages.error(request, 'Please login...')
        return render(request, "errorspage_pendency.html", {})
    usermast=m1.MyUser.objects.filter(email=request.user).first()
    rolelist=usermast.user_role
    if str(request.user).startswith('admin'):
        actual_user = str(request.user).split('admin')[1]
    else:
        actual_user = request.user
    empnox = AdminMaster.objects.filter(Q(admin_email=actual_user), user_id__isnull=False).values('rly','user_id')
    
    rly_unit_id=None
    cuser = None
    parent_rly = []
    if empnox:
        rly_unit_id = empnox[0]['rly']
        cuser = empnox[0]['user_id']
        child_rly = list(railwayLocationMaster.objects.filter( parent_rly_unit_code  = str(rly_unit_id)).values('rly_unit_code'))
        if len(child_rly) > 0:
            child_rly = list(map(lambda x: x['rly_unit_code'], child_rly))
    
    if request.method == 'POST' and request.is_ajax():
        post_type = request.POST.get('post_type')
        if post_type == 'getDetails':
            ref_no = request.POST.get('ref_no')
            data = list(empmast_nonrly.objects.filter(ref_no = ref_no).values())
            designation = list(Level_Desig.objects.filter(delete_flag = False).values('designation_code','designation').order_by('hierarchy_level','designation').distinct())
            if len(data) > 0:
                emp = empmast_nonrly.objects.filter(ref_no = ref_no)[0]
                if emp.empmname == None and emp.emplname == None:
                    empname = emp.empname
                elif emp.empmname == None:
                    empname = emp.empname + " " + emp.emplname
                elif emp.emplname == None:
                    empname = emp.empname + " " + emp.empmname
                else:
                    empname = emp.empname + " " + emp.empmname + " " + emp.emplname
                
                data[0].update({'empname':empname , 'currentunitdivision': emp.currentunitdivision if emp.currentunitdivision is not None else '-'})
                if rolelist == 'admin_super':
                    pass
                else:
                    if len(child_rly) > 0:
                        designation = list(Level_Desig.objects.filter(Q(rly_unit__in = child_rly) | Q(rly_unit = rly_unit_id), delete_flag = False ).values('designation_code','designation').order_by('hierarchy_level','designation').distinct())
                    else:
                        designation = list(Level_Desig.objects.filter(Q(rly_unit = rly_unit_id), delete_flag = False ).values('designation_code','designation').order_by('hierarchy_level','designation').distinct())

            context = {
                'data':data,
                'designation':designation,
            }
            return JsonResponse(context, safe = False)
        
        if post_type == 'showmodal':
            ref_no = request.POST.get('ref_no')
            data = list(empmast_nonrly.objects.filter(ref_no = ref_no).values())
            if len(data) > 0:
                emp = empmast_nonrly.objects.filter(ref_no = ref_no)[0]
                if emp.empmname == None and emp.emplname == None:
                    empname = emp.empname
                elif emp.empmname == None:
                    empname = emp.empname + " " + emp.emplname
                elif emp.emplname == None:
                    empname = emp.empname + " " + emp.empmname
                else:
                    empname = emp.empname + " " + emp.empmname + " " + emp.emplname
                
                data[0].update({'empname':empname , 'currentunitdivision': emp.currentunitdivision if emp.currentunitdivision is not None else '-'})
            context = {
                'data':data,
            }
            return JsonResponse(context, safe = False)
        
        if post_type == 'reject':
            remarks = request.POST.get('remarks')
            ref_no = request.POST.get('ref_no')
            empmast_nonrly.objects.filter(ref_no = ref_no).update(status = 2, profile_accepted_by = cuser, profile_accepted_on = datetime.datetime.now(), remarks=remarks)
            return JsonResponse('Request Rejected Successfully', safe = False)
        if post_type == 'accept':
            remarks = request.POST.get('remarks')
            ref_no = request.POST.get('ref_no')
            designation = request.POST.get('designation')
            designation_details = list(Level_Desig.objects.filter(designation_code = designation).values('designation_code','designation','desig_user').order_by('hierarchy_level','designation').distinct())
            if len(designation_details) > 0:
                if Level_Desig.objects.filter(designation_code = designation, empno_id__isnull = False).exists():
                    return JsonResponse('Request Cannot be Accepted because Designation already have Employee number linked, Relinquish the employee First.', safe = False)
                
                designation_code = designation_details[0]['designation_code']
                designation = designation_details[0]['designation']
                desig_user = designation_details[0]['desig_user']
                empmast_nonrly.objects.filter(ref_no = ref_no).update(link_designation_id_id = designation_code, link_designation = designation,status = 3, profile_accepted_by = cuser, profile_accepted_on = datetime.datetime.now(), remarks=remarks)
                
                user_details = list(empmast_nonrly.objects.filter(ref_no = ref_no).values())

                m1.empmast.objects.create(empno = user_details[0]['empno'], empname = user_details[0]['empname'],empmname = user_details[0]['empmname'],emplname = user_details[0]['emplname'],
                email = user_details[0]['email'],contactno = user_details[0]['contactno'],railwaygroup = user_details[0]['railwaygroup'],
                pc7_level = user_details[0]['pc7_level'],desig_longdesc = user_details[0]['desig_longdesc'],
                station_des = user_details[0]['station_des'],dept_desc = user_details[0]['dept_desc'],rly_id_id = user_details[0]['rly_id_id'],
                currentzone = user_details[0]['currentzone'],currentunitdivision = user_details[0]['currentunitdivision'],rl_type = user_details[0]['rl_type'],
                role = 'nonrly',profile_modified_by = cuser,profile_modified_on = datetime.datetime.now())
                
                Level_Desig.objects.filter(designation_code = designation_code).update(empno_id = user_details[0]['empno'])
                m1.MyUser.objects.filter(id = desig_user).update(is_active = True, user_role = 'nonrly')

                return JsonResponse('Request Accepted Successfully', safe = False)
            else:   
                return JsonResponse('Some error exist, please contact admin', safe = False)
        
        
        return JsonResponse({'success':False}, status = 400)
    pending = []
    pending11 = list(empmast_nonrly.objects.filter(status = 1).values())
    if rolelist == 'admin_super':
        for i in range(len(pending11)):
            pending.append(pending11[i])
    else:
        for i in range(len(pending11)):
            prev_rly_unit = pending11[i]['rly_id_id']
            if rly_unit_id == prev_rly_unit:
                if AdminMaster.objects.filter(status='Active',rly = prev_rly_unit).exists():
                    pending.append(pending11[i])
            
            elif prev_rly_unit in child_rly:
                if AdminMaster.objects.filter(status='Active',rly = prev_rly_unit).exists():
                    pending.append(pending11[i])
    accepted = list(empmast_nonrly.objects.filter(status = 3, profile_accepted_by = cuser).values())
    rejected = list(empmast_nonrly.objects.filter(status = 2, profile_accepted_by = cuser).values())
    messages.success(request,'')
    context ={
        'pending':pending,
        'accepted':accepted,
        'rejected':rejected,

    }
    return render(request,'nonrly_signup_accept.html',context)


from apscheduler.schedulers.background import BackgroundScheduler

def update_db():
    cursor = connection.cursor()
    cursor.execute("""SELECT public.create_insp_marked_summary();""")

    cursor.execute("""update inspects_empmast
    set dept_desc = myadmin_level_desig.department
    from myadmin_level_desig
    where inspects_empmast.empno=myadmin_level_desig.empno_id
    and myadmin_level_desig.department <> inspects_empmast.dept_desc;""")
    
    cursor.execute("""update inspects_empmast
    set 
    rl_type = myadmin_rlyhead.rllongdesc,
    rly_id_id = myadmin_level_desig.rly_unit_id
    from myadmin_level_desig, myadmin_railwaylocationmaster,myadmin_rlyhead
    where inspects_empmast.empno=myadmin_level_desig.empno_id and 
    myadmin_level_desig.rly_unit_id = myadmin_railwaylocationmaster.rly_unit_code and
    location_type = myadmin_rlyhead.rlshortcode
    ;""")

    cursor.execute("""update inspects_empmast
    set currentzone = myadmin_railwaylocationmaster.location_code,
    currentunitdivision = myadmin_railwaylocationmaster.location_description
    from myadmin_level_desig, myadmin_railwaylocationmaster
    where inspects_empmast.empno=myadmin_level_desig.empno_id and 
    myadmin_level_desig.rly_unit_id = myadmin_railwaylocationmaster.rly_unit_code and
    location_type in ('ZR','PU');""")
    
    cursor.execute("""update inspects_empmast
    set 
    currentzone = myadmin_railwaylocationmaster.parent_location_code,
    currentunitdivision = myadmin_railwaylocationmaster.location_description
    from myadmin_level_desig, myadmin_railwaylocationmaster
    where inspects_empmast.empno=myadmin_level_desig.empno_id and 
    myadmin_level_desig.rly_unit_id = myadmin_railwaylocationmaster.rly_unit_code and
    location_type in ('DIV','WS')
    ;""")

    cursor.execute("""update myadmin_level_desig
    set div_id_id = rly_unit_id::integer
    from inspects_empmast, myadmin_railwaylocationmaster
    where inspects_empmast.empno = myadmin_level_desig.empno_id and
    myadmin_level_desig.rly_unit_id = myadmin_railwaylocationmaster.rly_unit_code and
    location_type in ('DIV','WS');""")

    cursor.execute("""update myadmin_level_desig
    set hq_id_id = rly_unit_id::integer
    from inspects_empmast, myadmin_railwaylocationmaster
    where inspects_empmast.empno = myadmin_level_desig.empno_id and
    myadmin_level_desig.rly_unit_id = myadmin_railwaylocationmaster.rly_unit_code and
    location_type in ('ZR','PU');""")

    cursor.execute("""update myadmin_level_desig
    set department_code_id = myadmin_departmast.department_code
    from myadmin_departmast
    where myadmin_departmast.department_name=myadmin_level_desig.department;""")

    cursor.close()
    
    print("DB updated!")        
    return

scheduler = BackgroundScheduler()
scheduler.start()
ob = scheduler.add_job(update_db, 'cron', year='*', month='*', day='*', hour=8, minute=0, second=0)
ob = scheduler.add_job(update_db, 'cron', year='*', month='*', day='*', hour=18, minute=0, second=0)

# Pooja

from collections import Counter
from django.utils import timezone

def feedback_form(request):
    # Get current month and year
    current_month = timezone.now().month
    current_year = timezone.now().year

    # Get logged-in user's email
    user = request.user
    cuser = str(user)

    # Find user's designation
    empnox = Level_Desig.objects.exclude(delete_flag=True).filter(
        Q(official_email_ID=cuser) | Q(official_email_ID=user)
    ).first()

    if empnox:
        empno = empnox.designation_code
        desig = empnox.designation

        # Check if feedback already submitted by this designation this month
        already_submitted = FeedBack_data.objects.filter(
            design_code=empno,
            reported_date__year=current_year,
            reported_date__month=current_month
        ).exists()

        if already_submitted:
            return render(request, "Feedback_allreadysubmit.html", {"message": f"Feedback has already been submitted this month for the designation: {desig}."})
        else:
            return render(request, "Feedback_Form.html", {"designation": desig})
    else:
        return render(request, "Feedback_allreadysubmit.html", {"message": "Your designation is not found. Please contact admin."})

def feedback_submit(request):
    if request.method == 'POST':
        try:
            user = request.user
            if user.user_role == 'guest':
                cuser = user.guest_email
                user.email = user.guest_email
            else:
                cuser = user.username
            
            empnox = Level_Desig.objects.exclude(delete_flag=True).filter(Q(official_email_ID=cuser) | Q(official_email_ID=user)).first()        
            
            if empnox:
                empno = empnox.designation_code
                desig = empnox.designation

            FeedBack_data.objects.create(
                inspection_accuracy = request.POST.get('inspection_accuracy_rating'),
                ui_design = request.POST.get('ui_design_rating'),
                performance_speed = request.POST.get('performance_speed_rating'),
                application_smoothness = request.POST.get('application_smoothness_rating'),
                dashboard = request.POST.get('dashboard_rating'),
                my_inspection = request.POST.get('my_inspection_rating'),
                compliance_marked = request.POST.get('compliance_marked_rating'),
                mom = request.POST.get('mom_rating'),
                search = request.POST.get('search_rating'),
                copy_to = request.POST.get('copy_to_rating'),
                reports= request.POST.get('reports_rating'),
                suggestions = request.POST.get('suggestions'),
                overall_experience = request.POST.get('stars'),
                Designation = desig,
                design_code_id = empno,
            )
            
            success_message = f"Feedback successfully submitted for the month under Designation: {desig}."
            messages.success(request, success_message)

            redirect_url = reverse('feedback_already_submit')
            return JsonResponse({'redirect_url': redirect_url})
        
            # redirect_url = reverse('feedback_already_submit') + f"?message=Feedback successfully submitted for the month under Designation: {desig}."
            # return JsonResponse({'redirect_url': redirect_url})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def feedback_confirmation(request):
    message = request.GET.get('message', '')
    return render(request, "Feedback_allreadysubmit.html", {"message": message})

def feedback_dashbord(request):
    try:
        user = request.user
        if user.user_role == 'guest':
            cuser = user.guest_email
            user.email = user.guest_email
        else:
            cuser = user.username
        
        mydata = list(FeedBack_data.objects.all().values())
        empnox = models.Level_Desig.objects.exclude(delete_flag=True).filter(Q(official_email_ID=cuser) | Q(official_email_ID=user)).first()        
        if empnox:
            empno = empnox.designation_code
            desig = empnox.designation

            mydata = list(FeedBack_data.objects.all().values())

            context={
                'mydata':mydata,
            }
            return render(request,"Feedback_dashbord.html",context)
        else:
            return render(request,"Feedback_dashbord.html")        
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="Feedback_form_data checklist",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "errorspage.html", {})

def feedback_chart_data(request):
    fields = [
        'overall_experience','inspection_accuracy', 'ui_design', 'performance_speed', 'application_smoothness',
        'dashboard', 'my_inspection', 'compliance_marked','mom', 'search', 'copy_to', 'reports'
    ]
    
    response_data = {}
    for field in fields:
        values = list(FeedBack_data.objects.values_list(field, flat=True))
        counter = Counter(values)
        counts = [counter.get(i, 0) for i in range(1, 6)]
        response_data[field] = counts

    return JsonResponse(response_data)

def feedback_chart_load(request):
    designation = request.GET.get('designation', None)
    # print(designation)

    if not designation:
        # print("No designation provided")
        return JsonResponse({'error': 'No designation provided'}, status=400)

    feedbacks = FeedBack_data.objects.filter(Designation=designation)

    rating_fields = [
        'inspection_accuracy', 'ui_design', 'performance_speed', 'application_smoothness',
        'dashboard', 'my_inspection', 'compliance_marked','mom', 'search', 'copy_to', 'reports', 'overall_experience'
    ]

    data = []
    for idx, fb in enumerate(feedbacks):
        entry = {
            'label': f'Entry {idx+1}',
            'data': [getattr(fb, field) for field in rating_fields],
            'desig' : designation
        }
        data.append(entry)

    return JsonResponse({
    'designation': designation,
    'datasets': data
    })