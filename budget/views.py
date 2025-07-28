from array import array
from datetime import datetime, timedelta
# futuredate = datetime.now() + timedelta(days=10)

import xlwt
# from xlwt import workbook

import email
from django.shortcuts import render,redirect
from inspects.utils import render_to_pdf
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.db import models
from inspects import models as m1
from myadmin import models
from mom import models as m3
from budget import models as m5
from django.db.models import Q
from django.db.models import Max
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.files.storage import FileSystemStorage
import json
user=m1.MyUser
from django.db import transaction

import copy
# from datetime import date

# PPT
# import aspose.slides as slides
# from pptx import Presentation
# from pptx.util import Inches


# Added by me
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect

# OTP
import random
import math
# from django.db.models import Subquery,Sum,Count
# from django.views.decorators.clickjacking import xframe_options_exempt
def generateOTP() :
     digits = "0123456789"
     OTP = ""
     for i in range(4) :
         OTP += digits[math.floor(random.random() * 10)]
     return OTP

#  Shubham Budget Form




def budget_implementation(request):
    try:
        financial_year=request.GET.get('financial_year')
        if financial_year:
            data=list(m5.budget_para.objects.filter(financial_year=financial_year).values().order_by('-budget_id'))
        else:    
            data=list(m5.budget_para.objects.values().order_by('-budget_id'))
        # data=list(m5.budget_para.objects.values().order_by('-budget_id'))
        # budget=list(m5.budget_specific_actions.objects.select_related('budget_id_id').values())
        totaldata=[]
        for i in range(len(data)):
            budget=list(m5.budget_specific_actions.objects.filter(budget_id=data[i]['budget_id'],specific_action__isnull=False).values().order_by('specific_action_id'))
            if len(budget) > 0:
               
               

                for j in range(len(budget)):
                    bud=list(m5.budget_specific_actions.objects.filter(budget_id=data[i]['budget_id'],specific_action_id__gt=budget[j]['specific_action_id'],specific_action__isnull=True).values().order_by('specific_action_id'))
                    sid=0
                    if len(bud) > 0:
                        sid=bud[0]['specific_action_id']
                    fid = budget[j]['specific_action_id'] + 1
                    total=[]
                    xyz=copy.deepcopy(data[i])
                    total.append(xyz)
                    lid=[]
                    sub=[]
                    submk=[]
                    if sid == 0:
                        data1=list(m5.budget_marked_officers.objects.filter(specific_action_id=budget[j]['specific_action_id']).values('marked_officer__designation'))
                        if len(data1)>0:
                            mk=''
                            for l in range(len(data1)):
                                if mk != '':
                                    mk += ', '
                                mk += data1[l]['marked_officer__designation']
                            sub.append([''])
                            submk.append([mk])
                            print(budget[j]['specific_action'],submk)
                    else:
                        for ii in range(fid,sid+1):
                            lid.append(ii)

                        bud11=list(m5.budget_specific_actions.objects.filter(budget_id=data[i]['budget_id'],specific_action_id__in=lid).values().order_by('specific_action_id'))
                        for k in range(len(bud11)):
                            data1=list(m5.budget_marked_officers.objects.filter(specific_action_id=bud11[k]['specific_action_id']).values('marked_officer__designation'))
                            mk=''
                            for l in range(len(data1)):
                                if mk != '':
                                    mk += ', '
                                mk += data1[l]['marked_officer__designation']
                            sub.append([bud11[k]['sub_specific_action']])
                            submk.append([mk])
                    total[0].update({'marked_officer':submk})
                    total[0].update({'specific_action':budget[j]['specific_action']})
                    total[0].update({'sub_specific_action':sub})
                    totaldata.extend(total)
        data=totaldata
        fin_year=m5.budget_para.objects.values('financial_year',"budget_specific_actions__specific_action").distinct('financial_year').order_by('financial_year')
        para_no=m5.budget_para.objects.values('para_no').distinct().order_by('para_no')

        action=m5.budget_para.objects.values('action').distinct().order_by('action')

        if request.method == 'POST':
            finyear=request.POST.get('year_id')
            parano=request.POST.get('para_id')
            # officer=request.POST.get('marked_officer')
           
            action=request.POST.get('action')
           

            print('ffffffffffffffff',finyear)
            print('pppppppp',parano)
            # print(officer)
            # print("heyy",psrs)
            # data=m5.budget_para.objects.filter(Q(financial_year=finyear)&Q(para_no=parano)).all()


            if action!="" and finyear==None and parano==None:
                print('first condition')
                data=list(m5.budget_para.objects.filter(action=action).values().order_by('-budget_id'))
                totaldata=[]
                for i in range(len(data)):
                    budget=list(m5.budget_specific_actions.objects.filter(budget_id=data[i]['budget_id'],specific_action__isnull=False).values().order_by('specific_action_id'))
                    if len(budget) > 0:
                       
                       

                        for j in range(len(budget)):
                            bud=list(m5.budget_specific_actions.objects.filter(budget_id=data[i]['budget_id'],specific_action_id__gt=budget[j]['specific_action_id'],specific_action__isnull=True).values().order_by('specific_action_id'))
                            sid=0
                            if len(bud) > 0:
                                sid=bud[0]['specific_action_id']
                            fid = budget[j]['specific_action_id'] + 1
                            total=[]
                            xyz=copy.deepcopy(data[i])
                            total.append(xyz)
                            lid=[]
                            sub=[]
                            submk=[]
                            if sid == 0:
                                data1=list(m5.budget_marked_officers.objects.filter(specific_action_id=budget[j]['specific_action_id']).values('marked_officer__designation'))
                                if len(data1)>0:
                                    mk=''
                                    for l in range(len(data1)):
                                        if mk != '':
                                            mk += ', '
                                        mk += data1[l]['marked_officer__designation']
                                    sub.append([''])
                                    submk.append([mk])
                                    print(budget[j]['specific_action'],submk)
                            else:
                                for ii in range(fid,sid+1):
                                    lid.append(ii)

                                bud11=list(m5.budget_specific_actions.objects.filter(budget_id=data[i]['budget_id'],specific_action_id__in=lid).values().order_by('specific_action_id'))
                                for k in range(len(bud11)):
                                    data1=list(m5.budget_marked_officers.objects.filter(specific_action_id=bud11[k]['specific_action_id']).values('marked_officer__designation'))
                                    mk=''
                                    for l in range(len(data1)):
                                        if mk != '':
                                            mk += ', '
                                        mk += data1[l]['marked_officer__designation']
                                    sub.append([bud11[k]['sub_specific_action']])
                                    submk.append([mk])
                            total[0].update({'marked_officer':submk})
                            total[0].update({'specific_action':budget[j]['specific_action']})
                            total[0].update({'sub_specific_action':sub})
                            totaldata.extend(total)
                data=totaldata

            elif action=="" and finyear!=None and parano==None:
                print('second condition')
                data=list(m5.budget_para.objects.filter(financial_year=finyear).values().order_by('-budget_id'))
                totaldata=[]
                for i in range(len(data)):
                    budget=list(m5.budget_specific_actions.objects.filter(budget_id=data[i]['budget_id'],specific_action__isnull=False).values().order_by('specific_action_id'))
                    if len(budget) > 0:
                       
                       

                        for j in range(len(budget)):
                            bud=list(m5.budget_specific_actions.objects.filter(budget_id=data[i]['budget_id'],specific_action_id__gt=budget[j]['specific_action_id'],specific_action__isnull=True).values().order_by('specific_action_id'))
                            sid=0
                            if len(bud) > 0:
                                sid=bud[0]['specific_action_id']
                            fid = budget[j]['specific_action_id'] + 1
                            total=[]
                            xyz=copy.deepcopy(data[i])
                            total.append(xyz)
                            lid=[]
                            sub=[]
                            submk=[]
                            if sid == 0:
                                data1=list(m5.budget_marked_officers.objects.filter(specific_action_id=budget[j]['specific_action_id']).values('marked_officer__designation'))
                                if len(data1)>0:
                                    mk=''
                                    for l in range(len(data1)):
                                        if mk != '':
                                            mk += ', '
                                        mk += data1[l]['marked_officer__designation']
                                    sub.append([''])
                                    submk.append([mk])
                                    print(budget[j]['specific_action'],submk)
                            else:
                                for ii in range(fid,sid+1):
                                    lid.append(ii)

                                bud11=list(m5.budget_specific_actions.objects.filter(budget_id=data[i]['budget_id'],specific_action_id__in=lid).values().order_by('specific_action_id'))
                                for k in range(len(bud11)):
                                    data1=list(m5.budget_marked_officers.objects.filter(specific_action_id=bud11[k]['specific_action_id']).values('marked_officer__designation'))
                                    mk=''
                                    for l in range(len(data1)):
                                        if mk != '':
                                            mk += ', '
                                        mk += data1[l]['marked_officer__designation']
                                    sub.append([bud11[k]['sub_specific_action']])
                                    submk.append([mk])
                            total[0].update({'marked_officer':submk})
                            total[0].update({'specific_action':budget[j]['specific_action']})
                            total[0].update({'sub_specific_action':sub})
                            totaldata.extend(total)
                data=totaldata

           
            elif action=="" and finyear==None and parano!=None:
                print('third condition')
                data=list(m5.budget_para.objects.filter(para_no=parano).values().order_by('-budget_id'))
                totaldata=[]
                for i in range(len(data)):
                    budget=list(m5.budget_specific_actions.objects.filter(budget_id=data[i]['budget_id'],specific_action__isnull=False).values().order_by('specific_action_id'))
                    if len(budget) > 0:
                       
                       

                        for j in range(len(budget)):
                            bud=list(m5.budget_specific_actions.objects.filter(budget_id=data[i]['budget_id'],specific_action_id__gt=budget[j]['specific_action_id'],specific_action__isnull=True).values().order_by('specific_action_id'))
                            sid=0
                            if len(bud) > 0:
                                sid=bud[0]['specific_action_id']
                            fid = budget[j]['specific_action_id'] + 1
                            total=[]
                            xyz=copy.deepcopy(data[i])
                            total.append(xyz)
                            lid=[]
                            sub=[]
                            submk=[]
                            if sid == 0:
                                data1=list(m5.budget_marked_officers.objects.filter(specific_action_id=budget[j]['specific_action_id']).values('marked_officer__designation'))
                                if len(data1)>0:
                                    mk=''
                                    for l in range(len(data1)):
                                        if mk != '':
                                            mk += ', '
                                        mk += data1[l]['marked_officer__designation']
                                    sub.append([''])
                                    submk.append([mk])
                                    print(budget[j]['specific_action'],submk)
                            else:
                                for ii in range(fid,sid+1):
                                    lid.append(ii)

                                bud11=list(m5.budget_specific_actions.objects.filter(budget_id=data[i]['budget_id'],specific_action_id__in=lid).values().order_by('specific_action_id'))
                                for k in range(len(bud11)):
                                    data1=list(m5.budget_marked_officers.objects.filter(specific_action_id=bud11[k]['specific_action_id']).values('marked_officer__designation'))
                                    mk=''
                                    for l in range(len(data1)):
                                        if mk != '':
                                            mk += ', '
                                        mk += data1[l]['marked_officer__designation']
                                    sub.append([bud11[k]['sub_specific_action']])
                                    submk.append([mk])
                            total[0].update({'marked_officer':submk})
                            total[0].update({'specific_action':budget[j]['specific_action']})
                            total[0].update({'sub_specific_action':sub})
                            totaldata.extend(total)
                data=totaldata


            elif action!="" and finyear!=None and parano==None:
                print('forth condition')
                data=list(m5.budget_para.objects.filter(action=action, financial_year=finyear).values().order_by('-budget_id'))
                totaldata=[]
                for i in range(len(data)):
                    budget=list(m5.budget_specific_actions.objects.filter(budget_id=data[i]['budget_id'],specific_action__isnull=False).values().order_by('specific_action_id'))
                    if len(budget) > 0:
                       
                       

                        for j in range(len(budget)):
                            bud=list(m5.budget_specific_actions.objects.filter(budget_id=data[i]['budget_id'],specific_action_id__gt=budget[j]['specific_action_id'],specific_action__isnull=True).values().order_by('specific_action_id'))
                            sid=0
                            if len(bud) > 0:
                                sid=bud[0]['specific_action_id']
                            fid = budget[j]['specific_action_id'] + 1
                            total=[]
                            xyz=copy.deepcopy(data[i])
                            total.append(xyz)
                            lid=[]
                            sub=[]
                            submk=[]
                            if sid == 0:
                                data1=list(m5.budget_marked_officers.objects.filter(specific_action_id=budget[j]['specific_action_id']).values('marked_officer__designation'))
                                if len(data1)>0:
                                    mk=''
                                    for l in range(len(data1)):
                                        if mk != '':
                                            mk += ', '
                                        mk += data1[l]['marked_officer__designation']
                                    sub.append([''])
                                    submk.append([mk])
                                    print(budget[j]['specific_action'],submk)
                            else:
                                for ii in range(fid,sid+1):
                                    lid.append(ii)

                                bud11=list(m5.budget_specific_actions.objects.filter(budget_id=data[i]['budget_id'],specific_action_id__in=lid).values().order_by('specific_action_id'))
                                for k in range(len(bud11)):
                                    data1=list(m5.budget_marked_officers.objects.filter(specific_action_id=bud11[k]['specific_action_id']).values('marked_officer__designation'))
                                    mk=''
                                    for l in range(len(data1)):
                                        if mk != '':
                                            mk += ', '
                                        mk += data1[l]['marked_officer__designation']
                                    sub.append([bud11[k]['sub_specific_action']])
                                    submk.append([mk])
                            total[0].update({'marked_officer':submk})
                            total[0].update({'specific_action':budget[j]['specific_action']})
                            total[0].update({'sub_specific_action':sub})
                            totaldata.extend(total)
                data=totaldata
           
               
            elif action=="" and finyear!=None and parano!=None:
                print('third condition')
                data=list(m5.budget_para.objects.filter(financial_year=finyear, para_no=parano).values().order_by('-budget_id'))
                totaldata=[]
                for i in range(len(data)):
                    budget=list(m5.budget_specific_actions.objects.filter(budget_id=data[i]['budget_id'],specific_action__isnull=False).values().order_by('specific_action_id'))
                    if len(budget) > 0:
                       
                       

                        for j in range(len(budget)):
                            bud=list(m5.budget_specific_actions.objects.filter(budget_id=data[i]['budget_id'],specific_action_id__gt=budget[j]['specific_action_id'],specific_action__isnull=True).values().order_by('specific_action_id'))
                            sid=0
                            if len(bud) > 0:
                                sid=bud[0]['specific_action_id']
                            fid = budget[j]['specific_action_id'] + 1
                            total=[]
                            xyz=copy.deepcopy(data[i])
                            total.append(xyz)
                            lid=[]
                            sub=[]
                            submk=[]
                            if sid == 0:
                                data1=list(m5.budget_marked_officers.objects.filter(specific_action_id=budget[j]['specific_action_id']).values('marked_officer__designation'))
                                if len(data1)>0:
                                    mk=''
                                    for l in range(len(data1)):
                                        if mk != '':
                                            mk += ', '
                                        mk += data1[l]['marked_officer__designation']
                                    sub.append([''])
                                    submk.append([mk])
                                    print(budget[j]['specific_action'],submk)
                            else:
                                for ii in range(fid,sid+1):
                                    lid.append(ii)

                                bud11=list(m5.budget_specific_actions.objects.filter(budget_id=data[i]['budget_id'],specific_action_id__in=lid).values().order_by('specific_action_id'))
                                for k in range(len(bud11)):
                                    data1=list(m5.budget_marked_officers.objects.filter(specific_action_id=bud11[k]['specific_action_id']).values('marked_officer__designation'))
                                    mk=''
                                    for l in range(len(data1)):
                                        if mk != '':
                                            mk += ', '
                                        mk += data1[l]['marked_officer__designation']
                                    sub.append([bud11[k]['sub_specific_action']])
                                    submk.append([mk])
                            total[0].update({'marked_officer':submk})
                            total[0].update({'specific_action':budget[j]['specific_action']})
                            total[0].update({'sub_specific_action':sub})
                            totaldata.extend(total)
                data=totaldata


            elif action!="" and finyear==None and parano!=None:
                print('third condition')
                data=list(m5.budget_para.objects.filter(action=action, para_no=parano).values().order_by('-budget_id'))
                totaldata=[]
                for i in range(len(data)):
                    budget=list(m5.budget_specific_actions.objects.filter(budget_id=data[i]['budget_id'],specific_action__isnull=False).values().order_by('specific_action_id'))
                    if len(budget) > 0:
                     
                       

                        for j in range(len(budget)):
                            bud=list(m5.budget_specific_actions.objects.filter(budget_id=data[i]['budget_id'],specific_action_id__gt=budget[j]['specific_action_id'],specific_action__isnull=True).values().order_by('specific_action_id'))
                            sid=0
                            if len(bud) > 0:
                                sid=bud[0]['specific_action_id']
                            fid = budget[j]['specific_action_id'] + 1
                            total=[]
                            xyz=copy.deepcopy(data[i])
                            total.append(xyz)
                            lid=[]
                            sub=[]
                            submk=[]
                            if sid == 0:
                                data1=list(m5.budget_marked_officers.objects.filter(specific_action_id=budget[j]['specific_action_id']).values('marked_officer__designation'))
                                if len(data1)>0:
                                    mk=''
                                    for l in range(len(data1)):
                                        if mk != '':
                                            mk += ', '
                                        mk += data1[l]['marked_officer__designation']
                                    sub.append([''])
                                    submk.append([mk])
                                    print(budget[j]['specific_action'],submk)
                            else:
                                for ii in range(fid,sid+1):
                                    lid.append(ii)

                                bud11=list(m5.budget_specific_actions.objects.filter(budget_id=data[i]['budget_id'],specific_action_id__in=lid).values().order_by('specific_action_id'))
                                for k in range(len(bud11)):
                                    data1=list(m5.budget_marked_officers.objects.filter(specific_action_id=bud11[k]['specific_action_id']).values('marked_officer__designation'))
                                    mk=''
                                    for l in range(len(data1)):
                                        if mk != '':
                                            mk += ', '
                                        mk += data1[l]['marked_officer__designation']
                                    sub.append([bud11[k]['sub_specific_action']])
                                    submk.append([mk])
                            total[0].update({'marked_officer':submk})
                            total[0].update({'specific_action':budget[j]['specific_action']})
                            total[0].update({'sub_specific_action':sub})
                            totaldata.extend(total)
                data=totaldata


            elif action!="" and finyear!=None and parano!=None:
                print('last condition')
                data=list(m5.budget_para.objects.filter(action=action, financial_year=finyear, para_no=parano).values().order_by('-budget_id'))
                totaldata=[]
                for i in range(len(data)):
                    budget=list(m5.budget_specific_actions.objects.filter(budget_id=data[i]['budget_id'],specific_action__isnull=False).values().order_by('specific_action_id'))
                    if len(budget) > 0:
                       
                       

                        for j in range(len(budget)):
                            bud=list(m5.budget_specific_actions.objects.filter(budget_id=data[i]['budget_id'],specific_action_id__gt=budget[j]['specific_action_id'],specific_action__isnull=True).values().order_by('specific_action_id'))
                            sid=0
                            if len(bud) > 0:
                                sid=bud[0]['specific_action_id']
                            fid = budget[j]['specific_action_id'] + 1
                            total=[]
                            xyz=copy.deepcopy(data[i])
                            total.append(xyz)
                            lid=[]
                            sub=[]
                            submk=[]
                            if sid == 0:
                                data1=list(m5.budget_marked_officers.objects.filter(specific_action_id=budget[j]['specific_action_id']).values('marked_officer__designation'))
                                if len(data1)>0:
                                    mk=''
                                    for l in range(len(data1)):
                                        if mk != '':
                                            mk += ', '
                                        mk += data1[l]['marked_officer__designation']
                                    sub.append([''])
                                    submk.append([mk])
                                    print(budget[j]['specific_action'],submk)
                            else:
                                for ii in range(fid,sid+1):
                                    lid.append(ii)

                                bud11=list(m5.budget_specific_actions.objects.filter(budget_id=data[i]['budget_id'],specific_action_id__in=lid).values().order_by('specific_action_id'))
                                for k in range(len(bud11)):
                                    data1=list(m5.budget_marked_officers.objects.filter(specific_action_id=bud11[k]['specific_action_id']).values('marked_officer__designation'))
                                    mk=''
                                    for l in range(len(data1)):
                                        if mk != '':
                                            mk += ', '
                                        mk += data1[l]['marked_officer__designation']
                                    sub.append([bud11[k]['sub_specific_action']])
                                    submk.append([mk])
                            total[0].update({'marked_officer':submk})
                            total[0].update({'specific_action':budget[j]['specific_action']})
                            total[0].update({'sub_specific_action':sub})
                            totaldata.extend(total)
                data=totaldata

        user=request.user.username
        desigid=models.Level_Desig.objects.filter(official_email_ID=user)[0].designation_code
        officer_prsnt=models.Level_Desig.objects.filter(Q(d_level='CRB')|Q(d_level='BM')|Q(designation='Secy. to DG')).values('designation').order_by('designation')
        dealt_officer=models.Level_Desig.objects.exclude(designation_code=desigid).filter(Q(d_level='AM')|Q(d_level='PED')|Q(d_level='ED')).values('designation').order_by('designation')
        list_off=[]
        list_dea=[]
        for i in officer_prsnt:
            list_off.append(i['designation'])
        for i in dealt_officer:
            list_dea.append(i['designation'])
       
        officer = list(m5.budget_marked_officers.objects.values('marked_officer','marked_officer__designation'))
        #print(data)
        context={
            'data':data,
            'fin_year':fin_year,
            'para_no':para_no,
            'list_off':list_off,
            'list_dea':list_dea,
            'officer':officer,
            # 'budget':budget,
        }
        print('ygju',list_off)
        return render(request, "budget_implementation.html",context)
    except Exception as e:
        try:
            m1.error_Table.objects.create(fun_name="budget_implementation",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "budgetapp_errors.html", {})

def getPara(request):
    try:
        if request.method=='GET':
            year_id=request.GET.get('year_id')
            print('year_id',year_id)
            result=[]
            result=list(m5.budget_para.objects.filter(financial_year=year_id).values())
            return JsonResponse(result,safe=False)
        return JsonResponse({'success':False},status=400)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="getPara",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "budgetapp_errors.html", {})
    
def getOfficer(request):
    try:
        para_id=request.GET.get('para_id')
        print('para_id',para_id)
        result=[]
        result=list(m5.budget_marked_officers.objects.filter(specific_action_id__budget_id__para_no=para_id).values('marked_officer__designation'))
        print('dffgdghhfh',result)
        return JsonResponse(result,safe=False)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="getofficer",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "budgetapp_errors.html", {})
    # return JsonResponse({'success':False}, status=400)

def validatePara_ajax(request):
    try:
        if request.method == 'GET':
            para_no = request.GET.get('para_no')
            
            # Inspection=list(inspectiontype_master.objects.filter(instypeid=instypeid).values())
            data=m5.budget_para.objects.filter(para_no=para_no)
            if data.exists():
                para = 'True'
            else:
                para = 'False'
            return JsonResponse(para, safe=False)
        return JsonResponse({'success':False},status=404)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="validatePara_ajax",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "budgetapp_errors.html", {})

def updateStatus_budget_ajax(request):
    try:
        if request.method == 'GET':
            budget_id = request.GET.get('budget_id')
            action = request.GET.get('view2')
            print(action,'fffffffffffffff  ', budget_id)
            
            # Inspection=list(inspectiontype_master.objects.filter(instypeid=instypeid).values())
            if m5.budget_para.objects.filter(budget_id=budget_id).exists():
                m5.budget_para.objects.filter(budget_id=budget_id).update(action=action)
                
            return JsonResponse({'success':True}, safe=False)
        return JsonResponse({'success':False},status=404)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="updateStatus_budget_ajax",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "budgetapp_errors.html", {})
    
def budgetReportPdf(request):
    try:
        today_date = datetime.now()

        data=list(m5.budget_para.objects.values().order_by('-budget_id')) 
        totaldata=[]
        for i in range(len(data)):
            budget=list(m5.budget_specific_actions.objects.filter(budget_id=data[i]['budget_id'],specific_action__isnull=False).values().order_by('specific_action_id'))
            if len(budget) > 0:
                
                for j in range(len(budget)):
                    bud=list(m5.budget_specific_actions.objects.filter(budget_id=data[i]['budget_id'],specific_action_id__gt=budget[j]['specific_action_id'],specific_action__isnull=True).values().order_by('specific_action_id'))
                    sid=0
                    if len(bud) > 0:
                        sid=bud[0]['specific_action_id']
                    fid = budget[j]['specific_action_id'] + 1
                    total=[]
                    xyz=copy.deepcopy(data[i])
                    total.append(xyz)
                    lid=[]
                    sub=[]
                    submk=[]
                    if sid == 0:
                        data1=list(m5.budget_marked_officers.objects.filter(specific_action_id=budget[j]['specific_action_id']).values('marked_officer__designation'))
                        if len(data1)>0:
                            mk=''
                            for l in range(len(data1)):
                                if mk != '':
                                    mk += ', '
                                mk += data1[l]['marked_officer__designation']
                            sub.append([''])
                            submk.append([mk])
                            print(budget[j]['specific_action'],submk)
                    else:
                        for ii in range(fid,sid+1):
                            lid.append(ii)

                        bud11=list(m5.budget_specific_actions.objects.filter(budget_id=data[i]['budget_id'],specific_action_id__in=lid).values().order_by('specific_action_id'))
                        for k in range(len(bud11)):
                            data1=list(m5.budget_marked_officers.objects.filter(specific_action_id=bud11[k]['specific_action_id']).values('marked_officer__designation'))
                            mk=''
                            for l in range(len(data1)):
                                if mk != '':
                                    mk += ', '
                                mk += data1[l]['marked_officer__designation']
                            sub.append([bud11[k]['sub_specific_action']])
                            submk.append([mk])
                    total[0].update({'marked_officer':submk})
                    total[0].update({'specific_action':budget[j]['specific_action']})
                    total[0].update({'sub_specific_action':sub})
                    totaldata.extend(total)


        data=totaldata
    

        fin_year=m5.budget_para.objects.values('financial_year',"budget_specific_actions__specific_action").distinct('financial_year').order_by('financial_year')
        para_no=m5.budget_para.objects.values('para_no').distinct().order_by('para_no')



        if request.method == 'POST':
            finyear=request.POST.get('year_id')
            parano=request.POST.get('para_id')
            # officer=request.POST.get('marked_officer')
            

            print('ffffffffffffffff',finyear)
            print('pppppppp',parano)
        
            
            if finyear!=None and para_no!=None:
                data=m5.budget_para.objects.filter(financial_year=finyear, para_no=parano).all()
                print('hell mu')
            if finyear!=None and parano==None:
                print('gvbhnjm')
                data=m5.budget_para.objects.filter(financial_year=finyear).all()
            if finyear==None and parano!=None:
                print('ghjkl')
                data=m5.budget_para.objects.filter(para_no=parano).all()
                print("Heyyyy",data)
            print(data,'ijjo')
            
        user=request.user.username
        desigid=models.Level_Desig.objects.filter(official_email_ID=user)[0].designation_code
        officer_prsnt=models.Level_Desig.objects.filter(Q(d_level='CRB')|Q(d_level='BM')|Q(designation='Secy. to DG')).values('designation').order_by('designation')
        dealt_officer=models.Level_Desig.objects.exclude(designation_code=desigid).filter(Q(d_level='AM')|Q(d_level='PED')|Q(d_level='ED')).values('designation').order_by('designation')
        list_off=[]
        list_dea=[]
        for i in officer_prsnt:
            list_off.append(i['designation'])
        for i in dealt_officer:
            list_dea.append(i['designation'])
        
        officer = list(m5.budget_marked_officers.objects.values('marked_officer','marked_officer__designation'))
        context={
            'data':data,
            'fin_year':fin_year,
            'para_no':para_no,
            'list_off':list_off,
            'list_dea':list_dea,
            'officer':officer,
            'today_date': today_date,
        }
        print('ygju',list_off)
        template_src='budgetReportPdf.html'
        return render_to_pdf(template_src, context)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="budgetReportPdf",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "budgetapp_errors.html", {})



def budgetReportExcel(request):
    try:
        data=list(m5.budget_para.objects.values().order_by('-budget_id')) 
        totaldata=[]
        for i in range(len(data)):
            budget=list(m5.budget_specific_actions.objects.filter(budget_id=data[i]['budget_id'],specific_action__isnull=False).values().order_by('specific_action_id'))
            if len(budget) > 0:
                
                for j in range(len(budget)):
                    bud=list(m5.budget_specific_actions.objects.filter(budget_id=data[i]['budget_id'],specific_action_id__gt=budget[j]['specific_action_id'],specific_action__isnull=True).values().order_by('specific_action_id'))
                    sid=0
                    if len(bud) > 0:
                        sid=bud[0]['specific_action_id']
                    fid = budget[j]['specific_action_id'] + 1
                    total=[]
                    xyz=copy.deepcopy(data[i])
                    total.append(xyz)
                    lid=[]
                    sub=[]
                    submk=[]
                    if sid == 0:
                        data1=list(m5.budget_marked_officers.objects.filter(specific_action_id=budget[j]['specific_action_id']).values('marked_officer__designation'))
                        if len(data1)>0:
                            mk=''
                            for l in range(len(data1)):
                                if mk != '':
                                    mk += ', '
                                mk += data1[l]['marked_officer__designation']
                            sub.append([''])
                            submk.append([mk])
                            print(budget[j]['specific_action'],submk)
                    else:
                        for ii in range(fid,sid+1):
                            lid.append(ii)

                        bud11=list(m5.budget_specific_actions.objects.filter(budget_id=data[i]['budget_id'],specific_action_id__in=lid).values().order_by('specific_action_id'))
                        for k in range(len(bud11)):
                            data1=list(m5.budget_marked_officers.objects.filter(specific_action_id=bud11[k]['specific_action_id']).values('marked_officer__designation'))
                            mk=''
                            for l in range(len(data1)):
                                if mk != '':
                                    mk += ', '
                                mk += data1[l]['marked_officer__designation']
                            sub.append([bud11[k]['sub_specific_action']])
                            submk.append([mk])
                    total[0].update({'marked_officer':submk})
                    total[0].update({'specific_action':budget[j]['specific_action']})
                    total[0].update({'sub_specific_action':sub})
                    totaldata.extend(total)


        data=totaldata

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=budget_summary' + \
            str(datetime.now())+'.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('budget_summary')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['Sr No.', 'Year', 'Para No.', 'Ministry/Department', 'Test of Announcement', 'Stage of Implementation', 'Implementation Status',  'Remark, if any']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        font_style = xlwt.XFStyle()
        algn1=xlwt.Alignment()
        algn1.wrap =1
        font_style.alignment=algn1
        row_num += 1
        print(data)
        for i in range(len(data)):
            ws.write(row_num, 0, (i+1), font_style)
            ws.write(row_num, 1, data[i]['financial_year'], font_style)
            ws.write(row_num, 2, data[i]['para_no'], font_style)
            ws.write(row_num, 3, 'Railway', font_style)
            ws.write(row_num, 4, data[i]['specific_action'], font_style)
            ws.write(row_num, 5, data[i]['action'], font_style)
            str1=''
            for j in data[i]['sub_specific_action']:
                if str1 != '':
                    str1 += ','
                if j[0] is not None:
                    str1 += j[0]

            ws.write(row_num, 6,str1 , font_style)
            ws.write(row_num, 7, '', font_style)
            row_num += 1
            
        
        wb.save(response)

        return response
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="budgetReportExcel",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "budgetapp_errors.html", {})


def updateCompliance_ajax(request):
    print('ASDFGHJKL')
    if request.method == 'GET':
            budget_id = request.GET.get('budget_id')
            comp_id = request.GET.get('comp_id')
            print(comp_id,'fffffffffffffff  ', budget_id)
            if m5.budget_para.objects.filter(budget_id=budget_id).exists():
                # print(str(m5.budget_para.objects.filter(budget_id=budget_id)[0].compliance),'shubham')
                if str(m5.budget_para.objects.filter(budget_id=budget_id)[0].compliance)=='None':
                    print('1234')
                    data=str(comp_id)
                else:
                    print('4321')
                    compliance=str(m5.budget_para.objects.filter(budget_id=budget_id)[0].compliance)
                    data=str(compliance)+'/'+str(comp_id)
                print(data,'DATAdata')
                m5.budget_para.objects.filter(budget_id=budget_id).update(status_flag=0,compliance=data)
                print('123')
            result = list(m5.budget_para.objects.filter(budget_id=budget_id).values())
            data=result[0]['compliance'].split('/')
            result[0].update({'new_compliance':data})
            print(result,'result')
            return JsonResponse({'result':result}, safe=False)
    return JsonResponse({'success':True}, safe=False)


def updateCompliance_ajax1(request):
    print('ASDFGHJKL')
    if request.method == 'GET':
            budget_id = request.GET.get('budget_id1')
            comp_id = request.GET.get('comp_id1')
            print(comp_id,'fffffffffffffff  ', budget_id)
            if m5.budget_para.objects.filter(budget_id=budget_id).exists():
                # print(str(m5.budget_para.objects.filter(budget_id=budget_id)[0].compliance),'shubham')
                if str(m5.budget_para.objects.filter(budget_id=budget_id)[0].compliance)=='None':
                    print('1234')
                    data=str(comp_id)
                else:
                    print('4321')
                    compliance=str(m5.budget_para.objects.filter(budget_id=budget_id)[0].compliance)
                    data=str(compliance)+'/'+str(comp_id)
                print(data,'DATAdata')
                m5.budget_para.objects.filter(budget_id=budget_id).update(status_flag=0,compliance=data)
                print('123')
            result = list(m5.budget_para.objects.filter(budget_id=budget_id).values())
            data=result[0]['compliance'].split('/')
            result[0].update({'new_compliance':data})
            print(result,'result')
            return JsonResponse({'result':result}, safe=False)
    return JsonResponse({'success':True}, safe=False)

# Draft Compliance
def draftCompliance_ajax(request):
    if request.method == 'GET':
            budget_id = request.GET.get('budget_id')
            comp_id = request.GET.get('comp_id')
            print(comp_id,'fffffffffffffff  ', budget_id)
            if m5.budget_para.objects.filter(budget_id=budget_id).exists():
                # print(str(m5.budget_para.objects.filter(budget_id=budget_id)[0].compliance),'shubham')
                if str(m5.budget_para.objects.filter(budget_id=budget_id)[0].compliance)=='None':
                    print('1234')
                    data=str(comp_id)
                else:
                    print('4321')
                    compliance=str(m5.budget_para.objects.filter(budget_id=budget_id)[0].compliance)
                    data=str(compliance)+'/'+str(comp_id)
                print(data,'DATAdata')
                m5.budget_para.objects.filter(budget_id=budget_id).update(status_flag=0,compliance=data)
                print('123')
            result = list(m5.budget_para.objects.filter(budget_id=budget_id).values())
            data=result[0]['compliance'].split('/')
            result[0].update({'draft_compliance':data})
            print(result,'result')
            return JsonResponse({'result':result}, safe=False)
    return JsonResponse({'success':True}, safe=False)


def budgetReportPPT(request):
    today_date = datetime.now()
    data=list(m5.budget_para.objects.values().order_by('-budget_id')) 
    totaldata=[]
    for i in range(len(data)):
        budget=list(m5.budget_specific_actions.objects.filter(budget_id=data[i]['budget_id'],specific_action__isnull=False).values().order_by('specific_action_id'))
        if len(budget) > 0:
            
            for j in range(len(budget)):
                bud=list(m5.budget_specific_actions.objects.filter(budget_id=data[i]['budget_id'],specific_action_id__gt=budget[j]['specific_action_id'],specific_action__isnull=True).values().order_by('specific_action_id'))
                sid=0
                if len(bud) > 0:
                    sid=bud[0]['specific_action_id']
                fid = budget[j]['specific_action_id'] + 1
                total=[]
                xyz=copy.deepcopy(data[i])
                total.append(xyz)
                lid=[]
                sub=[]
                submk=[]
                if sid == 0:
                    data1=list(m5.budget_marked_officers.objects.filter(specific_action_id=budget[j]['specific_action_id']).values('marked_officer__designation'))
                    if len(data1)>0:
                        mk=''
                        for l in range(len(data1)):
                            if mk != '':
                                mk += ', '
                            mk += data1[l]['marked_officer__designation']
                        sub.append([''])
                        submk.append([mk])
                        print(budget[j]['specific_action'],submk)
                else:
                    for ii in range(fid,sid+1):
                        lid.append(ii)

                    bud11=list(m5.budget_specific_actions.objects.filter(budget_id=data[i]['budget_id'],specific_action_id__in=lid).values().order_by('specific_action_id'))
                    for k in range(len(bud11)):
                        data1=list(m5.budget_marked_officers.objects.filter(specific_action_id=bud11[k]['specific_action_id']).values('marked_officer__designation'))
                        mk=''
                        for l in range(len(data1)):
                            if mk != '':
                                mk += ', '
                            mk += data1[l]['marked_officer__designation']
                        sub.append([bud11[k]['sub_specific_action']])
                        submk.append([mk])
                total[0].update({'marked_officer':submk})
                total[0].update({'specific_action':budget[j]['specific_action']})
                total[0].update({'sub_specific_action':sub})
                totaldata.extend(total)


    data=totaldata


    fin_year=m5.budget_para.objects.values('financial_year',"budget_specific_actions__specific_action").distinct('financial_year').order_by('financial_year')
    para_no=m5.budget_para.objects.values('para_no').distinct().order_by('para_no')
        
    user=request.user.username
    desigid=models.Level_Desig.objects.filter(official_email_ID=user)[0].designation_code
    officer_prsnt=models.Level_Desig.objects.filter(Q(d_level='CRB')|Q(d_level='BM')|Q(designation='Secy. to DG')).values('designation').order_by('designation')
    dealt_officer=models.Level_Desig.objects.exclude(designation_code=desigid).filter(Q(d_level='AM')|Q(d_level='PED')|Q(d_level='ED')).values('designation').order_by('designation')
    list_off=[]
    list_dea=[]
    for i in officer_prsnt:
        list_off.append(i['designation'])
    for i in dealt_officer:
        list_dea.append(i['designation'])
    
    officer = list(m5.budget_marked_officers.objects.values('marked_officer','marked_officer__designation'))
    print('ssfdddssssssssss', data)
    context={
        'data':data,
        'fin_year':fin_year,
        'para_no':para_no,
        'list_off':list_off,
        'list_dea':list_dea,
        'officer':officer,
        'today_date': today_date,
    }
    print('ygju',list_off)
    template_src='budgetReportPPT.html'
    return render_to_pdf(template_src,context_dict=context)
    # X = Presentation()

    # Layout = X.slide_layouts[0]
    # first_slide = X.slides.add_slide(Layout)

    # first_slide.shapes.title.text = "Creating a budget powerpoint using Python" 
    # first_slide.placeholders[1].text = "Created by CRIS"

    # X.save("First_presentation.pptx")

    # Second_Layout = X.slide_layouts[5]
    # second_slide = X.slides.add_slide(Second_Layout)
    # second_slide.shapes.title.text = "Second slide"

    # textbox = second_slide.shapes.add_textbox(Inches(3), Inches(1.5),Inches(3), Inches(1)) 
    # textframe = textbox.text_frame
    # paragraph = textframe.add_paragraph()
    # paragraph.text = "This is a paragraph in the second slide!"
    # # return X
    # return HttpResponse(X.save("First_presentation.pptx"))
    # # return redirect('budget_implementation')


def budgetSaveOtp_ajax(request):
    # try:
        if request.method == 'GET':
            newotp = generateOTP()
            print('saved otp===>', newotp, request.user.id, datetime.now())
            # now = datetime.now()
            now= datetime.now() + timedelta(minutes=3)
            empnox = models.Level_Desig.objects.filter(Q(official_email_ID=request.user) | Q(official_email_ID=request.user.email))
            if empnox:
                empno = empnox[0].designation_code
            if m5.budget_otp.objects.filter(user_id=empno).exists():
                m5.budget_otp.objects.filter(user_id=empno).update(created_on=now, otp=newotp)
            else:
                m5.budget_otp.objects.create(user_id=empno ,created_on=now, otp=newotp)
            # var='12345678asd'
            # message="Successfully registered with Username: "+var+" and Password: "+var+" CRIS/RKVY"
            # sms(phoneno,message)
            timer_count = 180 #for 3 minitus

            return JsonResponse({'timer': timer_count, 'newotp': newotp}, safe = False)
        return JsonResponse({'success': False}, status=404)
    # except Exception as e: 
    #     try:
    #         m1.error_Table.objects.create(fun_name="saveByOtp_ajax",user_id=request.user,err_details=str(e))
    #     except:
    #         print("Internal Error!!!")
    #     return render(request, "errorspage.html", {})


def budget_verify_my_otp_ajax(request):
    # try:
        if request.method == 'POST':
            newotp = request.POST.get('myotp')
            empnox = models.Level_Desig.objects.filter(Q(official_email_ID=request.user) | Q(official_email_ID=request.user.email))
            if empnox:
                empno = empnox[0].designation_code
            dte=datetime.now()
            print(dte)
            x = m5.budget_otp.objects.filter(user_id=empno)
            # print(type(newotp))
            # print(x[0].otp_created_on, ':----')
            # print(x[0].otp_created_on >= dte)

            if int(newotp) == x[0].otp and x[0].created_on >= dte:
                ret = 'True'
            else:
                ret='False'

    
            return JsonResponse({'ret': ret}, safe = False)
        return JsonResponse({'success': False}, status=404)
    # except Exception as e: 
    #     try:
    #         m1.error_Table.objects.create(fun_name="verify_my_otp_ajax",user_id=request.user,err_details=str(e))
    #     except:
    #         print("Internal Error!!!")
    #     return render(request, "errorspage.html", {})



def budget_dashboard(request):
    cur_yr= datetime.today().year
    cur_yr=int(cur_yr)-10
    budget_list_yr=[]
    budget_list_data=[]
    xAxis = []
    Bar =[]
    Bar2 =[]
    for i in range(10):
        budget_list_yr.append(str(cur_yr)[2:4]+"-"+str(cur_yr+1)[2:4])
        make_yr=str(cur_yr)+"-"+str(cur_yr+1)[2:4]
        data=m5.budget_para.objects.filter(financial_year=make_yr).values_list('budget_id',flat=True)
        budget=m5.budget_specific_actions.objects.filter(budget_id__in=data,specific_action__isnull=False).values().count()
        dataimplemented=m5.budget_para.objects.filter(financial_year=make_yr,status_flag=3).values_list('budget_id',flat=True)
        budgetimplemented=m5.budget_specific_actions.objects.filter(budget_id__in=dataimplemented,specific_action__isnull=False).values().count()
        budget_list_data.append({'make_yr':make_yr,'data':budget,'implemented':budgetimplemented})
        cur_yr+=1
    for i in budget_list_data:
        xAxis.append('<b>'+" "+i['make_yr']+ '</b>')
        Bar.append(i['data'])
        Bar2.append(i['implemented'])
    data=list(m5.budget_para.objects.values().order_by('-budget_id'))
    totaldata=[]
    for i in range(len(data)):
        budget=list(m5.budget_specific_actions.objects.filter(budget_id=data[i]['budget_id'],specific_action__isnull=False).values().order_by('specific_action_id'))
        if len(budget) > 0:
            for j in range(len(budget)):
                bud=list(m5.budget_specific_actions.objects.filter(budget_id=data[i]['budget_id'],specific_action_id__gt=budget[j]['specific_action_id'],specific_action__isnull=True).values().order_by('specific_action_id'))
                sid=0
                if len(bud) > 0:
                    sid=bud[0]['specific_action_id']
                fid = budget[j]['specific_action_id'] + 1
                total=[]
                xyz=copy.deepcopy(data[i])
                total.append(xyz)
                lid=[]
                sub=[]
                submk=[]
                if sid == 0:
                    data1=list(m5.budget_marked_officers.objects.filter(specific_action_id=budget[j]['specific_action_id']).values('marked_officer__designation'))
                    if len(data1)>0:
                        mk=''
                        for l in range(len(data1)):
                            if mk != '':
                                mk += ', '
                            mk += data1[l]['marked_officer__designation']
                        sub.append([''])
                        submk.append([mk])
                else:
                    for ii in range(fid,sid+1):
                        lid.append(ii)

                    bud11=list(m5.budget_specific_actions.objects.filter(budget_id=data[i]['budget_id'],specific_action_id__in=lid).values().order_by('specific_action_id'))
                    for k in range(len(bud11)):
                        data1=list(m5.budget_marked_officers.objects.filter(specific_action_id=bud11[k]['specific_action_id']).values('marked_officer__designation'))
                        mk=''
                        for l in range(len(data1)):
                            if mk != '':
                                mk += ', '
                            mk += data1[l]['marked_officer__designation']
                        sub.append([bud11[k]['sub_specific_action']])
                        submk.append([mk])
                total[0].update({'marked_officer':submk})
                total[0].update({'specific_action':budget[j]['specific_action']})
                total[0].update({'sub_specific_action':sub})
                totaldata.extend(total)
    data=totaldata
    fin_year=m5.budget_para.objects.values('financial_year',"budget_specific_actions__specific_action").distinct('financial_year').order_by('financial_year')
    para_no=m5.budget_para.objects.values('para_no').distinct().order_by('para_no')
    action=m5.budget_para.objects.values('action').distinct().order_by('action')
    # actioninitiated=m5.budget_para.objects.filter(action='Action Initiated').values().count()
    # dropped=m5.budget_para.objects.filter(action='Dropped').values().count()
    # actionnot=m5.budget_para.objects.filter(action='Action Not Initiated').values().count()
    # imp=m5.budget_para.objects.filter(action='Implemented').values().count()
    # needsmon=m5.budget_para.objects.filter(action='Needs Monitoring').values().count()
    # subimp=m5.budget_para.objects.filter(action='Substantially Implemented').values().count()
    # underrec=m5.budget_para.objects.filter(action='Under Reconsideration').values().count()
    act=0
    drop=0
    notin=0
    impl=0
    subimpl=0
    undrec=0
    monn=0
    for i in data:
        if i['action']=='Action Initiated':
            act=act+1
        elif i['action']=='Dropped':
            drop=drop+1
        elif i['action']=='Action Not Initiated':
            notin=notin+1
        elif i['action']=='Implemented':
            impl=impl+1
        elif i['action']=='Needs Monitoring':
            monn=monn+1
        elif i['action']=='Substantially Implemented':
            subimpl=subimpl+1
        elif i['action']=='Under Reconsideration':
            undrec=undrec+1
    context={
        'budget_list_data':budget_list_data,
        'xAxis':xAxis,
        'Bar':Bar,
        'data':data,
        'fin_year':fin_year,
        'para_no':para_no,
        'action':action,
        'actioninitiated': act,
        'dropped':drop,
        'actionnot':notin,
        'imp':impl,
        'needsmon':monn,
        'subimp':subimpl,
        'underrec':undrec,
    }
    return render(request,"budget_dashboard.html",context)

def budget_draft(request):
    try:
        data=m5.budget_para.objects.filter(status_flag=0).values().order_by('-budget_id')
       
        dataList=list(m5.budget_marked_officers.objects.filter(specific_action_id__budget_id__status_flag=0).values('budget_marked_officers_id',
        'specific_action_id','marked_officer_id__designation','specific_action_id__sub_specific_action',
        'specific_action_id__specific_action','specific_action_id__budget_id__para_no',
        'specific_action_id__budget_id__financial_year','specific_action_id__budget_id__title',
        'specific_action_id__budget_id__action', 'specific_action_id__budget_id_id').order_by('-budget_marked_officers_id'))
        print('DATAList',dataList[0])
        for i in range(len(dataList)):
            try:
                specificAction = m5.budget_specific_actions.objects.filter(budget_id_id=dataList[i]['specific_action_id__budget_id_id'],specific_action__isnull=False)[0]
                dataList[i].update({'specificAction':specificAction.specific_action})
            except:
                specificAction=''
                dataList[i].update({'specificAction':''})
        return render(request, "budget_draft.html",{'data':data,'dataList':dataList})
    except Exception as e:
        try:
            m1.error_Table.objects.create(fun_name="draftschedule",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "errorspage.html", {})  
def delete_budget_fun(request):
    try:
        if request.method == 'GET':
            budget_id = request.GET.get('budget_id')
           
            if m5.budget_para.objects.filter(budget_id=budget_id).exists():
                m5.budget_para.objects.filter(budget_id=budget_id).delete()
               
            return JsonResponse({'success': 'del'}, safe = False)
        return JsonResponse({'success': False}, status=404)
    except Exception as e:
        try:
            m1.error_Table.objects.create(fun_name="deletionFunction",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "errorspage.html", {})

def budget_draft_submission(request):
   

    if request.method == "POST" and request.is_ajax():
        user=request.user.username
        print(user)
        action=request.POST.get('action')
        fin_yr=request.POST.get('fin_yr')
        para_no=request.POST.get('para_no')
        p_title=request.POST.get('p_title')
        final=json.loads(request.POST.get('final_partinspected'))
        final_id=json.loads(request.POST.get('id_partinspected'))
        budget_id=request.POST.get('budget_id')
        marked_officer=request.POST.get('Hofficer')
       
        print(final)
        print(final_id)
        print(action)
        # print(fin_yr, para_no, p_title, final, final_id, 'fin_yr', 'para_no', 'p_title', 'final', 'final_id', '123456789......')
        # print("final['1']['Htargetdate1']",final['1']['Htargetdate1'])
       
        print("budget_id: ")
        if m5.budget_para.objects.filter(budget_id=budget_id).exists():
            m5.budget_para.objects.create(action=action, para_no = para_no, financial_year = fin_yr, title = p_title, status_flag=1)
            print("budget tttttttt")

        else:
            m5.budget_para.objects.create(action=action, para_no = para_no, financial_year = fin_yr, title = p_title, status_flag=1)
       
        data_from_budget_para = m5.budget_para.objects.last()
        # print(data_from_budget_para)

        for f, b in zip(final, final_id):
            print(final[f], final_id[b])
            for x,y in zip(final[f], final_id[b]):
                s = y.split('.')
                print('len:', len(s))
            # for heading
                if len(s) == 1:
                    hed = 'heading'+y
                    trz = 'Htargetdate'+y
                    officm = 'Hofficer'+y
                    heading = final[f][hed]
                    targetd = final[f][trz]
                    dealt = final[f][officm]
                    if targetd:
                        target_date = datetime.strptime(targetd,'%d/%m/%Y')
                    else:
                        target_date = None
                    print('11111', heading, targetd, dealt)
                    m5.budget_specific_actions.objects.create(
                        specific_action = heading,
                        target_date = target_date,
                        budget_id_id=data_from_budget_para.budget_id
                        )
                    itemh = m5.budget_specific_actions.objects.last().specific_action_id
                    if dealt:
                        m5.budget_marked_officers.objects.filter()
                        for i in dealt:
                            Desig_mark=models.Level_Desig.objects.filter(designation__in=i.split(','))
                         
                            if Desig_mark:
                                Desig_mark_code=Desig_mark[0].designation_code
                                m5.budget_marked_officers.objects.create(specific_action_id_id=itemh, marked_officer_id=Desig_mark_code)
                            else:
                                print('ERROR-HEADING')
                elif len(s) == 2:
                    x1=y.split('.')[0]
                    x2=y.split('.')[1]
                    Pitem=x1+x2
                    shed = 'subheading'+y
                    trz = 'SHtargetdate'+y
                    officm = 'SHofficer'+Pitem
                    subheading = final[f][shed]
                    targetd = final[f][trz]
                    dealt = final[f][officm]
                    print('2222', subheading, targetd, dealt)
                    if targetd:
                        target_date = datetime.strptime(targetd,'%d/%m/%Y')
                    else:
                        target_date = None
                    m5.budget_specific_actions.objects.create(
                        sub_specific_action = subheading,
                        target_date = target_date,
                        budget_id_id=data_from_budget_para.budget_id
                        )
                    item = m5.budget_specific_actions.objects.last().specific_action_id
                    if dealt:
                        m5.budget_marked_officers.objects.filter()
                        for i in dealt:
                            Desig_mark=models.Level_Desig.objects.filter(designation__in=i.split(','))
                         
                            if Desig_mark:
                                Desig_mark_code=Desig_mark[0].designation_code
                                m5.budget_marked_officers.objects.create(specific_action_id_id=item, marked_officer_id=Desig_mark_code)
                            else:
                                print('ERROR-HEADING')
       

        return JsonResponse({"status": 1 })
    

##########  changed

def create_budget_form(request):
    # try:
        year = int(datetime.now().strftime('%Y'))+1
        year1 = year - 10
        budget_id=request.GET.get('budget_id')
        fin_year=[]
        for i in range(year1,year):
            fin_year.append(str(i)+'-'+str(i+1)[2:])
        user=request.user.username
        desigid=models.Level_Desig.objects.filter(official_email_ID=user)[0].designation_code
        officer_prsnt=models.Level_Desig.objects.filter(Q(d_level='CRB')|Q(d_level='BM')|Q(designation='Secy. to DG')).values('designation').order_by('designation')
        dealt_officer=models.Level_Desig.objects.exclude(designation_code=desigid).filter(Q(d_level='AM')|Q(d_level='PED')|Q(d_level='ED')).values('designation', 'designation_code').order_by('designation')
        list_off=[]
        list_dea=[]
        for i in officer_prsnt:
            list_off.append(i['designation'])
        for i in dealt_officer:
            list_dea.append(i['designation'])
        list_mark=json.dumps(list_dea)

        if budget_id:
            plist = []
            splist = []
            Nlist = 0
            dataList= m5.budget_para.objects.filter(budget_id=budget_id).values()
            full_array = list(m5.budget_specific_actions.objects.filter(budget_id=budget_id).values('data_id').order_by('specific_action_id'))
            full_array = list(map(lambda x: x['data_id'],full_array))
            for i in full_array:
                data_id = i.split('.')
                if len(data_id) == 1:
                    Nlist += 1
                    chk_string = data_id[0]+'.'
                    plen = list(filter(lambda x: x.startswith(chk_string),full_array))
                    plist.append(len(plen))
                    for j in plen:
                        splist.append(0)

            full_array = json.dumps(full_array)
            plist = json.dumps(plist)
            splist = json.dumps(splist)
            List1=m5.budget_specific_actions.objects.filter(budget_id=budget_id).values().order_by('specific_action_id')
            for j in List1:
                List2=m5.budget_marked_officers.objects.filter(specific_action_id=j['specific_action_id']).values('marked_officer__designation_code')
                List2 = list(map(lambda x: x['marked_officer__designation_code'],List2))
                j.update({'marked_officer':List2})
                if j['data_type'] == 'SH':
                    d_id = j['data_id'].replace('.', '')
                    j.update({'des_id_two': d_id})
                if j['data_type'] == 'H':
                    mid1= str(j['data_id'])+'.'
                    itmdata1 = m5.budget_specific_actions.objects.filter(budget_id=budget_id,data_id__startswith=mid1).values()
                    if len(itmdata1) == 0:
                        j.update({'chk_cts':'YES'})
                    else:
                        j.update({'chk_cts':'NO'})
                    
            
            context={'budget_id':budget_id,'plist':plist,'Nlist':Nlist,'splist':splist,'dataList':dataList, 'List1':List1, 'fin_year': fin_year, 'dealt':list_mark, 'dealt_officer': dealt_officer,'full_array':full_array}
            print(List1)
            return render(request, "editbudget_draft.html", context)
        else:
           
           
            context={'officer':list_off,'dealt':list_mark,'fin_year':fin_year}
            return render(request, "budget_form.html", context)
    # except Exception as e:
    #     try:
    #         m1.error_Table.objects.create(fun_name="create_budget_form",user_id=request.user,err_details=str(e))
    #     except:
    #         print("Internal Error!!!")
    #     return render(request, "budgetapp_errors.html", {})
    

def create_budget_draft_details(request):
    # try:
        if request.method == "POST":
            user=request.user.username
            action=request.POST.get('action')
            fin_yr=request.POST.get('fin_yr')
            para_no=request.POST.get('para_no')
            p_title=request.POST.get('p_title')
            final=json.loads(request.POST.get('final_partinspected'))
            final_id=json.loads(request.POST.get('id_partinspected'))
            budget_id = request.POST.get('budget_id')
            if budget_id is None:
                m5.budget_para.objects.create(action=action, para_no = para_no, financial_year = fin_yr, title = p_title, status_flag=0)
                data_from_budget_para = m5.budget_para.objects.last()
                for f, b in zip(final, final_id):
                    for x,y in zip(final[f], final_id[b]):
                        s = y.split('.')
                    # for heading
                        if len(s) == 1:
                            hed = 'heading'+y
                            trz = 'Htargetdate'+y
                            officm = 'Hofficer'+y
                            heading = final[f][hed]
                            targetd = final[f][trz]
                            dealt = final[f][officm]
                            if targetd:
                                target_date = datetime.strptime(targetd,'%d/%m/%Y').strftime('%Y-%m-%d')
                            else:
                                target_date = None
                            m5.budget_specific_actions.objects.create(
                                specific_action = heading,
                                target_date = target_date,
                                budget_id_id=data_from_budget_para.budget_id,
                                data_id = y,
                                data_type='H',


                                )
                            itemh = m5.budget_specific_actions.objects.last().specific_action_id
                            if dealt:
                                for i in dealt:
                                    Desig_mark=models.Level_Desig.objects.filter(designation_code=i)
                            
                                    if Desig_mark:
                                        Desig_mark_code=Desig_mark[0].designation_code
                                        m5.budget_marked_officers.objects.create(specific_action_id_id=itemh, marked_officer_id=Desig_mark_code)
                                    else:
                                        print('ERROR-HEADING')
                        elif len(s) == 2:
                            x1=y.split('.')[0]
                            x2=y.split('.')[1]
                            Pitem=x1+x2
                            shed = 'subheading'+y
                            trz = 'SHtargetdate'+y
                            officm = 'SHofficer'+Pitem
                            subheading = final[f][shed]
                            targetd = final[f][trz]
                            dealt = final[f][officm]
                            print('2222', subheading, targetd, dealt)
                            if targetd:
                                target_date = datetime.strptime(targetd,'%d/%m/%Y').strftime('%Y-%m-%d')    #Changed by Shubham
                            else:
                                target_date = None
                            m5.budget_specific_actions.objects.create(
                                sub_specific_action = subheading,
                                target_date = target_date,
                                budget_id_id=data_from_budget_para.budget_id,
                                data_id = y,
                                data_type='SH',

                                )
                            item = m5.budget_specific_actions.objects.last().specific_action_id
                            if dealt:
                                m5.budget_marked_officers.objects.filter()
                                for i in dealt:
                                    Desig_mark=models.Level_Desig.objects.filter(designation_code=i)
                            
                                    if Desig_mark:
                                        Desig_mark_code=Desig_mark[0].designation_code
                                        m5.budget_marked_officers.objects.create(specific_action_id_id=item, marked_officer_id=Desig_mark_code)
                                    else:
                                        print('ERROR-HEADING')

            else:
                m5.budget_para.objects.filter(budget_id=budget_id).update(action=action, para_no = para_no, financial_year = fin_yr, title = p_title, status_flag=0)
                data_from_budget_para = m5.budget_para.objects.filter(budget_id=budget_id).last()
                m5.budget_marked_officers.objects.filter(specific_action_id__in=m5.budget_specific_actions.objects.filter(budget_id=budget_id).values('specific_action_id')).delete()
                m5.budget_specific_actions.objects.filter(budget_id=budget_id).delete()
                for f, b in zip(final, final_id):
                    for x,y in zip(final[f], final_id[b]):
                        s = y.split('.')
                    # for heading
                        if len(s) == 1:
                            hed = 'heading'+y
                            trz = 'Htargetdate'+y
                            officm = 'Hofficer'+y
                            heading = final[f][hed]
                            targetd = final[f][trz]
                            dealt = final[f][officm]
                            if targetd:
                                target_date = datetime.strptime(targetd,'%d/%m/%Y').strftime('%Y-%m-%d')
                            else:
                                target_date = None
                            m5.budget_specific_actions.objects.create(
                                specific_action = heading,
                                target_date = target_date,
                                budget_id_id=data_from_budget_para.budget_id,
                                data_id = y,
                                data_type='H',


                                )

                            itemh = m5.budget_specific_actions.objects.last().specific_action_id
                            if dealt:
                                for i in dealt:
                                    Desig_mark=models.Level_Desig.objects.filter(designation_code=i)
                                    if Desig_mark:
                                        Desig_mark_code=Desig_mark[0].designation_code
                                        m5.budget_marked_officers.objects.create(specific_action_id_id=itemh, marked_officer_id=Desig_mark_code)
                                    else:
                                        print('ERROR-HEADING')
                        elif len(s) == 2:
                            x1=y.split('.')[0]
                            x2=y.split('.')[1]
                            Pitem=x1+x2
                            shed = 'subheading'+y
                            trz = 'SHtargetdate'+y
                            officm = 'SHofficer'+Pitem
                            subheading = final[f][shed]
                            targetd = final[f][trz]
                            dealt = final[f][officm]
                            if targetd:
                                target_date = datetime.strptime(targetd,'%d/%m/%Y').strftime('%Y-%m-%d')    #Changed by Shubham
                            else:
                                target_date = None
                            m5.budget_specific_actions.objects.create(
                                sub_specific_action = subheading,
                                target_date = target_date,
                                budget_id_id=data_from_budget_para.budget_id,
                                data_id = y,
                                data_type='SH',

                                )
                            item = m5.budget_specific_actions.objects.last().specific_action_id
                            if dealt:
                                for i in dealt:
                                    Desig_mark=models.Level_Desig.objects.filter(designation_code=i)                            
                                    if Desig_mark:
                                        Desig_mark_code=Desig_mark[0].designation_code
                                        m5.budget_marked_officers.objects.create(specific_action_id_id=item, marked_officer_id=Desig_mark_code)
                                    else:
                                        print('ERROR-HEADING')

            return JsonResponse({"status": 1 })
        return JsonResponse({"success":False}, status=400)
    # except Exception as e:
    #     try:
    #         m1.error_Table.objects.create(fun_name="create_budget_draft_details",user_id=request.user,err_details=str(e))
    #     except:
    #         print("Internal Error!!!")
    #     return render(request, "budgetapp_errors.html", {})
    

def create_budget_details(request):
    try:
        if request.method == "POST":
            user=request.user.username
            
            action=request.POST.get('action')
            fin_yr=request.POST.get('fin_yr')
            para_no=request.POST.get('para_no')
            p_title=request.POST.get('p_title')
            final=json.loads(request.POST.get('final_partinspected'))
            final_id=json.loads(request.POST.get('id_partinspected'))
            budget_id = request.POST.get('budget_id')
            if budget_id is None:
                m5.budget_para.objects.create(action=action, para_no = para_no, financial_year = fin_yr, title = p_title, status_flag=1)
            
                data_from_budget_para = m5.budget_para.objects.last()
                for f, b in zip(final, final_id):
                    print(final[f], final_id[b])
                    for x,y in zip(final[f], final_id[b]):
                        s = y.split('.')
                        print('len:', len(s))
                    # for heading
                        if len(s) == 1:
                            hed = 'heading'+y
                            trz = 'Htargetdate'+y
                            officm = 'Hofficer'+y
                            heading = final[f][hed]
                            targetd = final[f][trz]
                            dealt = final[f][officm]
                            if targetd:
                                target_date = datetime.strptime(targetd,'%d/%m/%Y').strftime('%Y-%m-%d')
                            else:
                                target_date = None
                            m5.budget_specific_actions.objects.create(
                                specific_action = heading,
                                target_date = target_date,
                                budget_id_id=data_from_budget_para.budget_id,
                                data_id = y,
                                data_type='H',
                                )
                            itemh = m5.budget_specific_actions.objects.last().specific_action_id
                            if dealt:
                                for i in dealt:
                                    Desig_mark=models.Level_Desig.objects.filter(designation_code=i)
                            
                                    if Desig_mark:
                                        Desig_mark_code=Desig_mark[0].designation_code
                                        m5.budget_marked_officers.objects.create(specific_action_id_id=itemh, marked_officer_id=Desig_mark_code)
                                    else:
                                        print('ERROR-HEADING')
                        elif len(s) == 2:
                            x1=y.split('.')[0]
                            x2=y.split('.')[1]
                            Pitem=x1+x2
                            shed = 'subheading'+y
                            trz = 'SHtargetdate'+y
                            officm = 'SHofficer'+Pitem
                            subheading = final[f][shed]
                            targetd = final[f][trz]
                            dealt = final[f][officm]
                            if targetd:
                                target_date = datetime.strptime(targetd,'%d/%m/%Y').strftime('%Y-%m-%d')    #Changed by Shubham
                            else:
                                target_date = None
                            m5.budget_specific_actions.objects.create(
                                sub_specific_action = subheading,
                                target_date = target_date,
                                budget_id_id=data_from_budget_para.budget_id,
                                data_id = y,
                                data_type='SH',

                                )
                            item = m5.budget_specific_actions.objects.last().specific_action_id
                            if dealt:
                                for i in dealt:
                                    Desig_mark=models.Level_Desig.objects.filter(designation_code=i)
                            
                                    if Desig_mark:
                                        Desig_mark_code=Desig_mark[0].designation_code
                                        m5.budget_marked_officers.objects.create(specific_action_id_id=item, marked_officer_id=Desig_mark_code)
                                    else:
                                        print('ERROR-HEADING')
           
            else:

                m5.budget_para.objects.filter(budget_id=budget_id).update(action=action, para_no = para_no, financial_year = fin_yr, title = p_title, status_flag=1)
                data_from_budget_para = m5.budget_para.objects.last()
                m5.budget_marked_officers.objects.filter(specific_action_id__in=m5.budget_specific_actions.objects.filter(budget_id=budget_id).values('specific_action_id')).delete()
                m5.budget_specific_actions.objects.filter(budget_id=budget_id).delete()
                for f, b in zip(final, final_id):
                    print(final[f], final_id[b])
                    for x,y in zip(final[f], final_id[b]):
                        s = y.split('.')
                        print('len:', len(s))
                    # for heading
                        if len(s) == 1:
                            hed = 'heading'+y
                            trz = 'Htargetdate'+y
                            officm = 'Hofficer'+y
                            heading = final[f][hed]
                            targetd = final[f][trz]
                            dealt = final[f][officm]
                            if targetd:
                                target_date = datetime.strptime(targetd,'%d/%m/%Y').strftime('%Y-%m-%d')
                            else:
                                target_date = None
                            m5.budget_specific_actions.objects.create(
                                specific_action = heading,
                                target_date = target_date,
                                budget_id_id=data_from_budget_para.budget_id,
                                data_id = y,
                                data_type='H',
                                )
                            itemh = m5.budget_specific_actions.objects.last().specific_action_id
                            if dealt:
                                for i in dealt:
                                    Desig_mark=models.Level_Desig.objects.filter(designation_code=i)
                            
                                    if Desig_mark:
                                        Desig_mark_code=Desig_mark[0].designation_code
                                        m5.budget_marked_officers.objects.create(specific_action_id_id=itemh, marked_officer_id=Desig_mark_code)
                                    else:
                                        print('ERROR-HEADING')
                        elif len(s) == 2:
                            x1=y.split('.')[0]
                            x2=y.split('.')[1]
                            Pitem=x1+x2
                            shed = 'subheading'+y
                            trz = 'SHtargetdate'+y
                            officm = 'SHofficer'+Pitem
                            subheading = final[f][shed]
                            targetd = final[f][trz]
                            dealt = final[f][officm]
                            if targetd:
                                target_date = datetime.strptime(targetd,'%d/%m/%Y').strftime('%Y-%m-%d')    #Changed by Shubham
                            else:
                                target_date = None
                            m5.budget_specific_actions.objects.create(
                                sub_specific_action = subheading,
                                target_date = target_date,
                                budget_id_id=data_from_budget_para.budget_id,
                                data_id = y,
                                data_type='SH',

                                )
                            item = m5.budget_specific_actions.objects.last().specific_action_id
                            if dealt:
                                for i in dealt:
                                    Desig_mark=models.Level_Desig.objects.filter(designation_code=i)
                            
                                    if Desig_mark:
                                        Desig_mark_code=Desig_mark[0].designation_code
                                        m5.budget_marked_officers.objects.create(specific_action_id_id=item, marked_officer_id=Desig_mark_code)
                                    else:
                                        print('ERROR-HEADING')
            return JsonResponse({"status": 1 })
        return JsonResponse({"success":False}, status=400)
    except Exception as e:
        try:
            m1.error_Table.objects.create(fun_name="create_budget_details",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "budgetapp_errors.html", {})




def UpdateBudget(request):
    try:
        if request.method == 'GET':
            budget_id = request.GET.get('budget_id')
            
            # Inspection=list(inspectiontype_master.objects.filter(instypeid=instypeid).values())
            data=list(m5.budget_para.objects.filter(budget_id=budget_id).values())
            print(data)
            return JsonResponse(data, safe=False)
        return JsonResponse({'success':False},status=404)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="updateBudget",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "budgetapp_errors.html", {})
    
