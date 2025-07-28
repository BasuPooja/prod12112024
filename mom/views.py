from array import array
from asyncio.windows_events import NULL
from datetime import datetime
import email
from django.shortcuts import render,redirect
from inspects.utils import render_to_pdf
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.db import models
from inspects import models as m1
from misiProject.settings import EMAIL_HOST_USER
# import apps
from myadmin import models
from inspects import models as m1
from einspect import models as m2
from mom import models as m3
from do_letters import models as m4
from budget import models as m5
from mails import models as m6

from django.db.models import Q
from django.db.models import Max
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.files.storage import FileSystemStorage
import json
import requests as req

from datetime import date,datetime,timedelta
from dateutil.relativedelta import relativedelta

user=m1.MyUser

def create_mom_form(request):
    try:
        user=request.user.username 
        if request.user.user_role == 'guest':
                user=request.user.guest_email
        desig_details=models.Level_Desig.objects.exclude(official_email_ID=None).filter(Q(official_email_ID=request.user)| Q(official_email_ID=request.user.guest_email) | Q(official_email_ID=request.user.email)).values()
        
       
        div_code = list(models.railwayLocationMaster.objects.filter(rly_unit_code=desig_details[0]['rly_unit_id']).values_list('parent_rly_unit_code', flat=True))
       
        type=''
        meeting=''
        if desig_details[0]['d_level']=='CRB' or desig_details[0]['d_level']=='BM' or desig_details[0]['d_level']=='Secy_RB':
            str1='RB'
            officer_prsnt=models.Level_Desig.objects.filter(Q(d_level='CRB')|Q(d_level='BM')|Q(d_level='Secy_RB')).values('designation','designation_code').order_by('designation')
            dealt_officer=models.Level_Desig.objects.exclude(designation_code=desig_details[0]['designation_code']).filter(Q(d_level='AM')|Q(d_level='PED')|Q(d_level='ED')).values('designation','designation_code').order_by('designation')
            officer_copy=models.Level_Desig.objects.filter(Q(d_level='CRB')|Q(d_level='BM')).values('designation','designation_code').order_by('designation')
            type='RB'

        elif desig_details[0]['d_level']=='GM' or desig_details[0]['d_level']=='PHOD' or desig_details[0]['d_level']=='AGM' or desig_details[0]['d_level']=='Secy_GM':
            str1='NoRB'
            officer_prsnt=models.Level_Desig.objects.filter((Q(d_level='GM')|Q(d_level='PHOD')|Q(d_level='AGM')|Q(d_level='Secy_GM')),(Q(rly_unit_id=desig_details[0]['rly_unit_id'])|Q(parent_desig_code=desig_details[0]['designation_code']))).values('designation','designation_code').order_by('designation')
            dealt_officer=models.Level_Desig.objects.exclude(designation_code=desig_details[0]['designation_code']).filter((Q(rly_unit_id=desig_details[0]['rly_unit_id'])|Q(rly_unit_id__in=div_code)|Q(rly_unit_id__parent_rly_unit_code=desig_details[0]['rly_unit_id'])|Q(parent_desig_code=desig_details[0]['designation_code']))).values('designation','designation_code').order_by('designation')
            officer_copy=models.Level_Desig.objects.exclude(designation_code=desig_details[0]['designation_code']).filter().values('designation','designation_code').order_by('designation')
 
            meeting=list(m3.meeting_typelist.objects.filter(default_flag=1).values('meeting_type').distinct().order_by('meeting_type'))
            meetings=(list(m3.meeting_typelist.objects.filter(default_flag=0,added_by=desig_details[0]['designation_code']).values('meeting_type').distinct().order_by('meeting_type')))
            for m in meetings:
                meeting.append({'meeting_type': m['meeting_type']})
            
        else:
            str1='NoRB'
            officer_prsnt=models.Level_Desig.objects.filter(Q(d_level='DRM')|Q(d_level='BO')).values('designation','designation_code').order_by('designation')
            dealt_officer=models.Level_Desig.objects.exclude(designation_code=desig_details[0]['designation_code']).filter(Q(rly_unit_id__in=div_code)| (Q(rly_unit_id=desig_details[0]['rly_unit_id'])) |Q(rly_unit_id__parent_rly_unit_code__in=div_code)).values('designation','designation_code').order_by('designation')
            officer_copy=models.Level_Desig.objects.exclude(designation_code=desig_details[0]['designation_code']).filter().values('designation','designation_code').order_by('designation')

            meeting=list(m3.meeting_typelist.objects.filter(default_flag=1).values('meeting_type').distinct().order_by('meeting_type'))
            meetings=(list(m3.meeting_typelist.objects.filter(default_flag=0,added_by=desig_details[0]['designation_code']).values('meeting_type').distinct().order_by('meeting_type')))
            for m in meetings:
                meeting.append({'meeting_type': m['meeting_type']})

        if str1=='NoRB':

            officer_prsnt=[]
            zone=desig_details[0]['rly_unit_id']
            l_id=list(models.railwayLocationMaster.objects.filter(Q(rly_unit_code=zone)).values('rly_unit_code','location_code'))
            if len(l_id)>0:
                desg=list(models.Level_Desig.objects.filter(designation__isnull=False,rly_unit=l_id[0]['rly_unit_code']).exclude(designation_code=desig_details[0]['designation_code']).values('designation','empno', 'designation_code').order_by('designation'))
                if len(desg)>0:
                    if desg not in officer_prsnt:
                         officer_prsnt.extend(desg)


            l_id=list(models.railwayLocationMaster.objects.filter(Q(parent_location_code=l_id[0]['location_code'])).values('rly_unit_code'))
            if len(l_id)>0:
                for x in range(len(l_id)):
                    desg=list(models.Level_Desig.objects.filter(designation__isnull=False,rly_unit=l_id[x]['rly_unit_code']).exclude(designation_code=desig_details[0]['designation_code']).values('designation','empno', 'designation_code').order_by('designation'))
                    if len(desg)>0:
                        if desg[0] not in officer_prsnt:
                                officer_prsnt.extend(desg)
        list_off=[]
        list_dea=[]
        list_cop=[]
        
        for i in officer_prsnt:
            temp={}
            temp['designation']=i['designation']
            temp['designation_code']=i['designation_code']
            list_off.append(temp)
     
        for i in dealt_officer:
            temp={}
            temp['designation']=i['designation']
            temp['designation_code']=i['designation_code']
            list_dea.append(temp)
      
        for i in officer_copy:
            temp={}
            temp['designation']=i['designation']
            temp['designation_code']=i['designation_code']
            list_cop.append(temp)
      
        
        list_mark=json.dumps(list_dea)
        mom_insp = request.GET.get('mom_no')
        if mom_insp != None:
            officer_copy=models.Level_Desig.objects.exclude(designation_code=desig_details[0]['designation_code']).filter().values('designation','designation_code').order_by('designation')
            mom_data= list(m3.Insp_details.objects.filter(insp_no=mom_insp).values().distinct().order_by('-insp_no'))
            des_no = list(m3.Item_details.objects.filter(insp_no=mom_insp).values_list('des_id', flat=True))
            mem_desig = m3.Insp_members.objects.filter(insp_no=mom_insp).values('member_desig__designation','other_members')
            mem=[]
            mems=[]
            for m in mem_desig:
                if m['member_desig__designation']:
                    mem.append(m['member_desig__designation'])
                else:
                    if {m['other_members']} not in mems:
                        mems.append(m['other_members']) 
                        mem.append(m['other_members'])
                        list_off.append({'designation':m['other_members'], 'designation_code':None})

            mem_desig = mem
            item_data = m3.Item_details.objects.filter(insp_no=mom_insp).values().order_by('item_no')

            length = 0
            head_length = m3.Item_details.objects.filter(insp_no=mom_insp, type="H").values()
            length += head_length.count()

            sh = []
            sh_1 = []
            dlis = []

            copy_to=[]
            copy_to_list=[]
            copy_to = list(m6.copyto_mails.objects.filter(doc_id=mom_insp, doc_table='m', area_flag=0).values('receiver_desig'))
            
            if copy_to:
                copy_to=copy_to[0]['receiver_desig']
                copy_to = copy_to.split(',')
            else:
                copy_to=[]

            if copy_to:
                copysss=[]
                for c in copy_to:
                    lvl=list(models.Level_Desig.objects.filter(designation=c).values('designation_code'))[0]['designation_code']
                    copysss.append({'designation':c,'designation_code':lvl})
                    copy_to_list.append(lvl)
                copy_to=copysss


            for x in range(len(head_length)):
                mid= str(x+1)+'.'
                itmdata = m3.Item_details.objects.filter(insp_no=mom_insp, type="SH", des_id__startswith=mid).values()
                sh.append(len(itmdata))
                for y in range(len(itmdata)):
                    nid= str(x+1)+'.'+ str(y+1)+'.'
                    itmdata1 = m3.Item_details.objects.filter(insp_no=mom_insp, type="D", des_id__startswith=nid).count()
                    
                    sh_1.append(itmdata1)
                    dlis.append(0)


            for i in item_data:
                offic = m3.Marked_Members.objects.filter(item_no=i['item_no']).values_list('marked_to__designation', flat=True)
                i.update({'mark_officer': offic})

                
                if i['type'] == 'H':
                    mark=m3.Marked_Members.objects.filter(item_no=i['item_no'])
                    if mark.exists():
                        if mark[0].marked_to is not None:
                
                            i.update({'chk_cts':'YES'})
                        else:
                            i.update({'chk_cts':'NO'})
                    else:
                        mid1= str(i['des_id'])+'.'
                        itmdata1 = list(m3.Item_details.objects.filter(insp_no=i['insp_no_id'], type="SH", des_id__startswith=mid1).values())
                        if len(itmdata1) == 0:
                            i.update({'chk_cts':'YES'})
                        else:
                            i.update({'chk_cts':'NO'})
                if i['type'] == 'SH' or i['type'] == 'D':
                    d_id = i['des_id'].replace('.', '')

                    i.update({'des_id_two': d_id})

            context={
                'officer':list_off,
                'dealt':list_mark,
                'copy':list_dea,
                'copy1':list_cop,
                'type':type,
                'str': str1,
                'meeting':meeting,
                'mom_data':mom_data,
                'mem_desig': mem_desig,
                'mems':mems,
                'item_data': item_data,
                'list_dea': list_dea,
                'des_no': json.dumps(des_no),
                'head_length': length,
                'sh_list': json.dumps(sh),
                'd_list': json.dumps(dlis),
                'mom_insp': mom_insp,
                'copy_to':copy_to,
                'sh_1':sh_1,
                'officer_copy':officer_copy,
                'copy_to_list':copy_to_list,
            }
            return render(request, 'edit_mom_form.html', context)
        else:
            context={
                'officer':list_off,
                'dealt':list_mark,
                'copy':list_dea,
                'copy1':list_cop,
                'type':type,
                'str':str1,
                'meeting':meeting,
            }
            
            return render(request,"create_mom_form.html",context)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="showDet",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "mom_errors.html", {})


def create_mom_details(request):
    try:
        print("I am here")
        if request.method == "POST" and request.is_ajax():
            user=request.user.username
            if request.user.user_role == 'guest':
                user=request.user.guest_email
            final=request.POST.get('final_partinspected')
            final_id=request.POST.get('id_partinspected')
            type1=request.POST.get('type')
            title=request.POST.get('titleMOM')
            present=json.loads(request.POST.get('present'))
            copyto=json.loads(request.POST.get('copyto'))
            mdate1=request.POST.get('mdate')
            mdate=datetime.strptime(mdate1, '%d/%m/%Y').strftime('%Y-%m-%d')
            designation=models.Level_Desig.objects.filter(official_email_ID=user,empno__isnull=False)


            if m3.meeting_typelist.objects.filter(meeting_type=type1).exists():
                xyz='xyz'
            else:
                empnox = models.Level_Desig.objects.filter(Q(official_email_ID=request.user)| Q(official_email_ID=request.user.guest_email) | Q(official_email_ID=request.user.email), empno__isnull=False)
                if empnox:
                    empno = empnox[0].empno_id
                    desig = empnox[0].designation_code
                    print(desig,empnox)
                m3.meeting_typelist.objects.create(meeting_type=type1,default_flag=0, added_by=empnox[0])

            if (designation[0].empno_id):
                empno=designation[0].empno_id
            else:
                empno=''
            desig=designation[0].designation
            desig_id=designation[0].designation_code
            level=designation[0].d_level

            finalval = json.loads(final)
            final_allid = json.loads(final_id)
            year = str(datetime.now().year)


            if level=='CRB' or level=='BM' or level=='Secy_RB':
                note_ = year+'/'
                last_note1 = m3.Insp_details.objects.filter(mom_note_no__istartswith=note_).aggregate(Max('note_last'))
                if last_note1['note_last__max'] == None:
                    last_note1 = 1
                    note_no = year+'/Secy/Bd. Mtg/'+ str(last_note1)  
                else:
                    last_note1 = int(last_note1['note_last__max']) +1
                    note_no = year+'/Secy/Bd. Mtg/'+ str(last_note1)
                title='MINUTES OF MEETING OF THE BOARD HELD ON '+ datetime.strptime(mdate1, '%d/%m/%Y').strftime("%d/%m/%y")
                m3.Insp_details.objects.create(created_on=datetime.now(),created_by=empno,mom_officer_id=desig_id,mom_title=title,mom_date=mdate,note_last=last_note1,mom_note_no=note_no,status_flag=4,type=0,meeting_type='Board Meeting')
           
            else:
                note_ = year+'/'+desig+'/'
                last_note1 = m3.Insp_details.objects.filter(mom_note_no__istartswith=note_).aggregate(Max('note_last'))
                if last_note1['note_last__max'] == None:
                    last_note1 = 1
                    note_no = year+'/'+desig+'/'+ str(last_note1)
                else:
                    last_note1 = int(last_note1['note_last__max']) +1
                    note_no = year+'/'+desig+'/'+ str(last_note1)
                if level=='GM' or level=='PHOD' or level=='AGM' or level=='Secy_GM':
                    m3.Insp_details.objects.create(created_on=datetime.now(),created_by=empno,mom_officer_id=desig_id,mom_title=title,mom_date=mdate,note_last=last_note1,mom_note_no=note_no,status_flag=4,type=1,meeting_type=type1)
                else:
                    m3.Insp_details.objects.create(created_on=datetime.now(),created_by=empno,mom_officer_id=desig_id,mom_title=title,mom_date=mdate,note_last=last_note1,mom_note_no=note_no,status_flag=4,type=2,meeting_type=type1)
           
            messages.info(request, 'MOM successfully saved with MOM Note No: ',note_no)
            insp_id=m3.Insp_details.objects.all().last().insp_no


            officer_email=[]
            for f, b in zip(finalval, final_allid):
                for x,y in zip(finalval[f], final_allid[b]):
                    s = y.split('.')
                    if len(s) == 1:
                        hed = 'heading'+y
                        pr = 'Hpriority'+y
                        trz = 'Htargetdate'+y
                        officm = 'Hofficer'+y
                        remark = 'remarks'+y
                        heading = finalval[f][hed]
                        priority = finalval[f][pr]
                        targetd = finalval[f][trz]
                        dealt = finalval[f][officm]
                        remarks = finalval[f][remark]
                        if targetd:
                            t_date = datetime.strptime(targetd, '%d/%m/%y').strftime('%Y-%m-%d')
                        else:
                            t_date = None

                        if dealt:
                            m3.Insp_details.objects.filter(insp_no=insp_id).update(status_flag=1)
                            m3.Item_details.objects.create(item_heading=heading, created_on=datetime.now(), created_by=empno, type='H', des_id=y, insp_no_id=insp_id, item_priority=priority, target_date=t_date, status_flag=1, remarks=remarks)
                            item_id=m3.Item_details.objects.all().last().item_no
                            for i in dealt:
                                Desig_mark=models.Level_Desig.objects.filter(designation__in=i.split(','))
                                email=models.Level_Desig.objects.filter(designation__in=i.split(','))[0].official_email_ID
                                officer_email.append(email)
                                if Desig_mark:
                                    Desig_mark_code=Desig_mark[0].designation_code
                                    if m3.Marked_Members.objects.all().last():
                                        marked_no_id=(m3.Marked_Members.objects.all().last().marked_no)+1
                                    else:
                                        marked_no_id = 1
                                    m3.Marked_Members.objects.create(created_on=datetime.now(),created_by=empno, marked_no=marked_no_id,status_flag=1, item_no_id=item_id,marked_to_id=int(Desig_mark_code))
                                else:
                                    pass
                        else:
                            m3.Item_details.objects.create(item_heading=heading, created_on=datetime.now(), created_by=empno, type='H', des_id=y, insp_no_id=insp_id, item_priority=priority, target_date=t_date, status_flag=4,remarks=remarks)
                            item_id=m3.Item_details.objects.all().last().item_no
                    elif len(s) == 2:
                        x1=y.split('.')[0]
                        x2=y.split('.')[1]
                        Pitem=x1+x2
                        shed = 'subheading'+y
                        shded= 'description'+y
                        pr = 'SHpriority'+Pitem
                        trz = 'SHtargetdate'+y
                        officm = 'SHofficer'+Pitem
                        remark='shremarks'+y
                        print(remark)
                        subheading = finalval[f][shed]
                        description= finalval[f][shded]
                        priority = finalval[f][pr]
                        targetd = finalval[f][trz]
                        dealt = finalval[f][officm]
                        remarks = finalval[f][remark]
                        if targetd:
                            t_date = datetime.strptime(targetd, '%d/%m/%y').strftime('%Y-%m-%d')
                        else:
                            t_date = None
                        if description!='':
                            pass
                        else:
                            description=None
                        if dealt:
                            m3.Insp_details.objects.filter(insp_no=insp_id).update(status_flag=1)
                            m3.Item_details.objects.create(item_subheading=subheading, created_on=datetime.now(), created_by=empno, type='SH', des_id=y, item_description=description,item_priority=priority, insp_no_id=insp_id, target_date=t_date, status_flag=1, remarks=remarks)
                            item_id=m3.Item_details.objects.all().last().item_no
                            for i in dealt:
                                Desig_mark=models.Level_Desig.objects.filter(designation__in=i.split(','))
                                if Desig_mark:
                                    Desig_mark_code=Desig_mark[0].designation_code
                                    if m3.Marked_Members.objects.all().last():
                                        marked_no_id=(m3.Marked_Members.objects.all().last().marked_no)+1
                                    else:
                                        marked_no_id = 1
                                    m3.Marked_Members.objects.create(created_on=datetime.now(),created_by=empno, marked_no=marked_no_id,status_flag=1, item_no_id=item_id,marked_to_id=int(Desig_mark_code))
                                else:
                                    pass
                        else:
                            m3.Item_details.objects.create(item_subheading=subheading, created_on=datetime.now(), created_by=empno, type='SH', des_id=y, item_description=description,item_priority=priority, insp_no_id=insp_id, target_date=t_date, status_flag=4,remarks=remarks)
                            item_id=m3.Item_details.objects.all().last().item_no
                    else:
                        x1=y.split('.')[0]
                        x2=y.split('.')[1]
                        x3=y.split('.')[2]
                        Pitem=x1+x2+x3
                        ded = 'decision'+y
                        pr = 'Dpriority'+Pitem
                        trz = 'Dtargetdate'+y
                        officm = 'Dofficer'+Pitem
                        remark = 'remarks'+y
                        decision = finalval[f][ded]
                        priority = finalval[f][pr]
                        targetd = finalval[f][trz]
                        dealt = finalval[f][officm]
                        remarks = finalval[f][remark]
                        if targetd:
                            t_date = datetime.strptime(targetd, '%d/%m/%y').strftime('%Y-%m-%d')
                        else:
                            t_date = None
                        if dealt:
                            m3.Insp_details.objects.filter(insp_no=insp_id).update(status_flag=1)
                            m3.Item_details.objects.create(item_decision=decision, created_on=datetime.now(), created_by=empno, type='D', des_id=y, insp_no_id=insp_id, item_priority=priority, target_date=t_date, status_flag=1, remarks=remarks)
                            item_id=m3.Item_details.objects.all().last().item_no
                            for i in dealt:
                                Desig_mark=models.Level_Desig.objects.filter(designation__in=i.split(','))
                         
                                if Desig_mark:
                                    Desig_mark_code=Desig_mark[0].designation_code
                                    if m3.Marked_Members.objects.all().last():
                                        marked_no_id=(m3.Marked_Members.objects.all().last().marked_no)+1
                                    else:
                                        marked_no_id = 1
                                    m3.Marked_Members.objects.create(created_on=datetime.now(),created_by=empno, marked_no=marked_no_id,status_flag=1, item_no_id=item_id,marked_to_id=int(Desig_mark_code))
                                else:
                                    pass
                                    print('ERROR-DECISION')
                        else:
                            m3.Item_details.objects.create(item_decision=decision, created_on=datetime.now(), created_by=empno, type='D', des_id=y, insp_no_id=insp_id, item_priority=priority, target_date=t_date, status_flag=4,remarks=remarks)
                            item_id=m3.Item_details.objects.all().last().item_no
       
        # storing member details
            present_email=[]  
            for o in present:
                member_desig=models.Level_Desig.objects.filter(designation=o)
                #print(member_desig,"heya",o)
                if len(member_desig)!=0:
                    member_desig=models.Level_Desig.objects.filter(designation=o)[0].designation_code

                    email=models.Level_Desig.objects.filter(designation=o)[0].official_email_ID
                    present_email.append(email)
                    m3.Insp_members.objects.create(member_desig_id=member_desig,insp_no_id=insp_id)
                else:
                    m3.Insp_members.objects.create(other_members=o,insp_no_id=insp_id)
           
        # mail to dealt officers
            if officer_email:
                try:
                    dealt_contact=[]
                    des=''
                    ids=''
                    count_dealt=len(officer_email)
                    countd=1
                    # #print(type(count_dealt),type(countd),'1234567890')
                    for i in officer_email:
                        # #print(count_dealt,countd,'1234567890')
                        a1=models.Level_Desig.objects.filter(official_email_ID=i).values('designation','designation_code','contactnumber')
                        if count_dealt==countd:
                            # #print('a')
                            des+=a1[0]['designation']
                            ids+=str(a1[0]['designation_code'])
                            # #print(des,'a',ids)
                        else:
                            # #print('b')
                            des+=a1[0]['designation']+', '
                            ids+=str(a1[0]['designation_code'])+', '
                            countd+=1
                            # #print(des,'b',ids)
                        if a1[0]['contactnumber']:
                            dealt_contact.append(a1[0]['contactnumber'])
                    # if len(dealt_contact) > 0:
                    #     for contact in dealt_contact:
                    #         MomSendSms(contact)
                    To=officer_email
                    details=m3.Insp_details.objects.filter(insp_no=insp_id).values('mom_title','insp_no','mom_officer__designation','meeting_type','mom_date')
                    subject=details[0]['mom_title']
                    context = {
                        'title': details[0]['mom_title'],
                        'meeting_type': details[0]['meeting_type'],
                        'mom_date': details[0]['mom_date'],
                        'insp_no': details[0]['insp_no'],
                        'mom_officer': details[0]['mom_officer__designation'],
                        'str': 'dealtby'            
                    }    
                    m3.copydealt_mail.objects.create(insp_no_id=insp_id,created_on=datetime.now(),created_by=empno,send_to=des,subject=subject,body=details[0]['mom_title'],area='DealtBy')
                    m6.copyto_mails.objects.create(created_on=datetime.now(),sender_id_id=desig_id,doc_id=insp_id,doc_table='m',receiver_id=ids,receiver_desig=des,
                        subject='MOM Report', body=details[0]['mom_title'],area_flag=2)
                    # MomSendMail(subject,To,context,details[0]['insp_no'])
                    # messages.success(request, 'E-mail has been send successfully to dealt officers.')  
                except:
                    #print("ERROR-DEALT-MAIL")
                    messages.error(request, 'Request to sent e-mail to dealt officers failed. Please Try Again.')
       
        # mail to copy-to officers
            if copyto:
                try:
                    copy_mail =[]
                    copy_desig=[]
                    copy_contact=[]
                    copy_desig_list=''
                    copy_id_list=''
                    count_copy=len(copyto)
                    countc=1
                    # #print(type(count_copy),type(countc),'1234567890')
                    for i in copyto:
                        mail_contact=models.Level_Desig.objects.filter(designation_code=i)
                        # #print(count_copy,countc,'1234567890')
                        if count_copy==countc:
                            # #print('c')
                            copy_desig_list+=mail_contact[0].designation
                            copy_id_list+=str(mail_contact[0].designation_code)
                            # #print(copy_desig_list,'c',copy_id_list)
                        else:
                            # #print('d')
                            copy_desig_list+=mail_contact[0].designation+','
                            copy_id_list+=str(mail_contact[0].designation_code)+','
                            countc+=1
                            # #print(copy_desig_list,'d',copy_id_list)
                        copy_desig.append(mail_contact[0].designation)
                        if mail_contact[0].official_email_ID:
                            copy_mail.append(mail_contact[0].official_email_ID)
                        if mail_contact[0].contactnumber:
                            copy_contact.append(mail_contact[0].contactnumber)
                    # if len(copy_contact) > 0:
                    #     for contact in copy_contact:
                    #         MomSendSms(contact)
                    To=copy_mail
                    details=m3.Insp_details.objects.filter(insp_no=insp_id).values('mom_title','insp_no','mom_officer__designation','meeting_type','mom_date')
                    subject=details[0]['mom_title']
                    context = {
                        'title': details[0]['mom_title'],
                        'meeting_type': details[0]['meeting_type'],
                        'mom_date': details[0]['mom_date'],
                        'insp_no': details[0]['insp_no'],
                        'mom_officer': details[0]['mom_officer__designation'],
                        'str': 'copyto'          
                    }  
                    m3.copydealt_mail.objects.create(insp_no_id=insp_id,created_on=datetime.now(),created_by=empno,send_to=copy_desig_list,subject=subject,body=title,area='CopyTo')
                    m6.copyto_mails.objects.create(created_on=datetime.now(),sender_id_id=desig_id,doc_id=insp_id,doc_table='m',receiver_id=copy_id_list,receiver_desig=copy_desig_list,
                            subject='MOM Report', body=details[0]['mom_title'],area_flag=0)
                    # MomSendMail(subject,To,context,details[0]['insp_no'])
                    # messages.success(request, 'E-mail has been send successfully to copy-to officers.')  
                except:
                    #print("ERROR-COPY-MAIL")
                    messages.error(request, 'Request to sent e-mail to dealt officers failed. Please Try Again.')
           
            return JsonResponse({"status": 1,"note_no":note_no })
        return JsonResponse({"success":False}, status=400)
    except Exception as e:
        try:
            m1.error_Table.objects.create(fun_name="create_mom_details",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "mom_errors.html", {})

def MomSendMail(subject,To,context,insp_no):
    html_message = render_to_string('mom_mail_template.html', context)
    plain_message = strip_tags(html_message)
    email=EmailMessage(subject,plain_message,EMAIL_HOST_USER,To)
    # if context['str']=='copyto':
    #     pdf=mom_ReportPdf(0,insp_no)
    #     email.attach('MOM_Report.pdf', pdf.getvalue(), 'application/pdf')
    email.send()

def MomSendSms(contact):
    try:
        message="Successfully registered"
        MOMsms(contact,message)    
    except Exception as e:
        print(e, "SMS not sent!!")

def MOMsms(phoneno,message):
    try:
        url = "http://enterprise.smsgupshup.com/GatewayAPI/rest?method=SendMessage&send_to=91"+str(phoneno)+"&msg="+message+" &msg_type=TEXT&userid=2000193787&auth_scheme=plain&password=TtyzCsbb&v=1.1&format=text"
        req.request("POST", url)
    except Exception as e:
        print(e, "SMS not sent!!")


def mom_pdf_ajax(request):
    try:
        if request.method == "GET" and request.is_ajax():
            insp_no=request.GET.get('insp_no') 
            insp_details=m3.Insp_details.objects.filter(insp_no=insp_no).values()
            marked_details=m3.Marked_Members.objects.filter(item_no__insp_no=insp_no,status_flag=3).values('item_no_id','reply_text','reply_file','reply_on','marked_to')
            #print(insp_no,'insp_no',insp_details,'insp_details',marked_details,'marked_details')
            list1=[]
            list2=[]
            for i in insp_details:
                temp={}
                temp['insp_no']=i['insp_no']
                temp['note_no']=i['mom_note_no']   
                temp['mdate']=i['mom_date'].strftime("%d/%m/%Y")
                temp['title']=i['mom_title']
            list1.append(temp)
            for i in marked_details:
                if(m3.Item_details.objects.filter(item_no=i['item_no_id'])):
                    list_item=m3.Item_details.objects.filter(item_no=i['item_no_id']).values()
                    temp={}
                    temp['item_db']=i['item_no_id']
                    temp['item_no']=list_item[0]['des_id']
                    temp['reply_on']=i['reply_on'].strftime("%d/%m/%y")
                    temp['text']=i['reply_text']
                    if(i['reply_file']):
                        temp['file']=i['reply_file']
                        #print(temp['file'])
                list2.append(temp)
            #print(list2,'1234')
            return JsonResponse({'insp_details':list1,'item_details':list2,},safe=False)
        return JsonResponse({"success":False}, status = 400)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="mom_pdf_ajax",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "mom_errors.html", {})
    
def filterdata_ajax(request):
    try:
        if request.method == "GET" and request.is_ajax():
            user=request.user.username
            if request.user.user_role == 'guest':
                user=request.user.guest_email
            desigid=models.Level_Desig.objects.exclude(official_email_ID=None).filter(Q(official_email_ID=request.user)| Q(official_email_ID=request.user.guest_email) | Q(official_email_ID=request.user.email))[0].designation_code  
            d_level=models.Level_Desig.objects.exclude(official_email_ID = None).filter(Q(official_email_ID=user) | Q(official_email_ID=request.user))[0].d_level
            str=request.GET.get('str')
            status=request.GET.get('status')
            startDate=request.GET.get('startDate')
            if startDate=='':
                startDate=date.today() - relativedelta(years = 50)
            else:
                 startDate = datetime.strptime(startDate,'%Y-%m-%d')
            startDate = datetime.strftime(startDate,'%Y-%m-%d')
            endDate=request.GET.get('endDate')
            if endDate=='':
                endDate=date.today()
            else:
                endDate = datetime.strptime(endDate,'%Y-%m-%d')
            endDate = datetime.strftime(endDate,'%Y-%m-%d')
            meeting_type=request.GET.get('meeting_type')
            print(meeting_type,user,desigid,status,str,startDate,endDate)
            list_filter=[]
            count=1

            if(str=='submit_filter'):
                if meeting_type=='All':
                    insp_details=m3.Insp_details.objects.filter(mom_date__gte=startDate,mom_date__lte=endDate).values().order_by('insp_no')
                else:
                    insp_details=m3.Insp_details.objects.filter(mom_date__gte=startDate,mom_date__lte=endDate,meeting_type=meeting_type).values().order_by('insp_no')
                for i in insp_details:
                    if m3.Marked_Members.objects.filter(item_no__insp_no=i['insp_no'],marked_to=desigid,status_flag=int(status)):
                        temp={}
                        temp['sr_no']=count
                        temp['insp_no']=i['insp_no']
                        temp['mom_note_no']=i['mom_note_no']
                        temp['mom_title']=i['mom_title']
                        temp['mom_date']=i['mom_date'].strftime("%d/%m/%y")
                        list_filter.append(temp)
                        count=count+1
            
            elif (str=='momdone_filter'):
                if (meeting_type=='All'):
                    if(int(status)==0):
                        insp_details=m3.Insp_details.objects.filter(mom_date__gte=startDate,mom_date__lte=endDate, mom_officer=desigid,status_flag__in=[1,2,3,4]).values().order_by('insp_no')
                    else:
                        insp_details=m3.Insp_details.objects.filter(mom_date__gte=startDate,mom_date__lte=endDate,status_flag=int(status),mom_officer=desigid).values().order_by('insp_no')
                else:
                    if(int(status)==0):
                        insp_details=m3.Insp_details.objects.filter(mom_date__gte=startDate,mom_date__lte=endDate, mom_officer=desigid,meeting_type=meeting_type,status_flag__in=[1,2,3,4]).values().order_by('insp_no')
                    else:
                        insp_details=m3.Insp_details.objects.filter(mom_date__gte=startDate,mom_date__lte=endDate,status_flag=int(status),mom_officer=desigid,meeting_type=meeting_type).values().order_by('insp_no')
                
                for i in insp_details:
                    temp={}
                    temp['sr_no']=count
                    temp['insp_no']=i['insp_no']
                    temp['mom_date']=i['mom_date'].strftime("%d/%m/%y")
                    temp['created_on']=i['created_on'].strftime("%d/%m/%y")
                    temp['mom_note_no']=i['mom_note_no']
                    temp['mom_title']=i['mom_title']
                    temp['meeting_type']=i['meeting_type']

                    if(i['status_flag']==1):
                        temp['status']='Pending'
                    elif(i['status_flag']==2):
                        temp['status']='Partial'
                    elif(i['status_flag']==3):
                        temp['status']='Completed'
                    elif(i['status_flag']==4):
                        temp['status']='Closed'
                    

                    if(m3.Marked_Members.objects.filter(item_no__insp_no_id=i['insp_no']).exists()):
                        temp['total_status']=m3.Marked_Members.objects.filter(item_no__insp_no_id=i['insp_no']).count()
                        temp['reply_status']=m3.Marked_Members.objects.filter(item_no__insp_no_id=i['insp_no'],status_flag=3).count()
                    else:
                        temp['total_status']=int(0)
                        temp['reply_status']=int(0)

                    list_filter.append(temp)
                    count=count+1
            print(len(list_filter))
            return JsonResponse({'list_filter':list_filter})
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="filterdata_ajax",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "mom_errors.html", {})
       
def chaser_view1(request):
    try:
        user=request.user.username
        if request.user.user_role == 'guest':
                cuser=request.user.guest_email
        desigid=models.Level_Desig.objects.exclude(official_email_ID=None).filter(Q(official_email_ID=request.user)| Q(official_email_ID=request.user.guest_email) | Q(official_email_ID=request.user.email))  
        context={}
        list1=[]
        if desigid[0].d_level=='CRB' or desigid[0].d_level=='BM' or desigid[0].d_level=='Secy_RB':
            insp_details=m3.Insp_details.objects.filter(type=0).values('insp_no','mom_date','mom_note_no','status_flag')
            for i in insp_details:
                temp={}
                temp['insp_no']=i['insp_no']
                temp['mom_date']=i['mom_date']
                temp['mom_note_no']=i['mom_note_no']
                temp['status_flag']=i['status_flag']
                item_list=m3.Item_details.objects.filter(insp_no__insp_no=i['insp_no']).values('item_no','des_id','item_heading','item_subheading','item_description','item_decision','type','status_flag')
                temp['item_details']=item_list  
                list1.append(temp)
            #print(list1,'list1list1')
            context={
                'insp_details':list1,
            }
        return render(request,"chaser_view1.html",context)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="chaser_view1",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "mom_errors.html", {})

def chaser_item_data1(request):
    try:
        if request.method == "GET" and request.is_ajax():
            item_no=request.GET.get('itemid')
            list3=list(m3.Item_details.objects.filter(item_no=item_no).values('item_no','insp_no_id','des_id','item_heading','item_subheading','item_description','item_decision','type'))
            list2=list(m3.Insp_details.objects.filter(insp_no=list3[0]['insp_no_id']).values('mom_date','mom_note_no','mom_title'))
            list1=[]
            if m3.Marked_Members.objects.filter(item_no=item_no).exists():
                marked_list=m3.Marked_Members.objects.filter(item_no=item_no).values()
                for i in marked_list:
                    #print('1234')
                    temp={}
                    employee=models.Level_Desig.objects.filter(designation_code=i['marked_to_id']).values('empno','designation')
                    #print(employee,'employeeemployee')
                    temp['marked_to']=employee[0]['designation']
                    temp['reply_text']=i['reply_text'] if i['reply_text'] != None else ''
                    temp['reply_file']=i['reply_file'] if i['reply_file'] != None else ''
                    if m3.Reject_remark.objects.filter(marked_no=i['marked_no']).exists():
                        temp['remark']=m3.Reject_remark.objects.filter(marked_no=i['marked_no'])[0].remark
                    else:
                        temp['remark']=''
                    # name=[]
                    # empfname=m1.empmast.objects.filter(empno=employee[0]['empno'])[0].empname
                    # empmname=m1.empmast.objects.filter(empno=employee[0]['empno'])[0].empmname
                    # emplname=m1.empmast.objects.filter(empno=employee[0]['empno'])[0].emplname
                    # if(empmname==None and emplname==None):
                    #     name=empfname
                    # elif(empmname==None):
                    #     name=empfname + " " + emplname
                    # elif(emplname==None):
                    #     name=empfname + " " + empmname   
                    # else:
                    #     name=empfname + " " + empmname + " " + emplname
                    # temp['officer_name']=str(name)
                    list1.append(temp)
            return JsonResponse({'marked_details':list1,'insp_details':list2,'item_details':list3,}, safe = False)
        return JsonResponse({"success":False}, status=400)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="chaser_item_data1",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "mom_errors.html", {})
    
def mom_received_action(request):
    try:
        user=request.user.username
        if request.user.user_role == 'guest':
                user=request.user.guest_email
        desigid=models.Level_Desig.objects.exclude(official_email_ID=None).filter(Q(official_email_ID=request.user)| Q(official_email_ID=request.user.guest_email) | Q(official_email_ID=request.user.email))[0].designation_code  
        #print(desigid)
        receive_reply=[]
        count=1
        insp_details=m3.Insp_details.objects.filter(mom_officer_id=desigid).values().order_by('-insp_no')
        #print(insp_details)
        for i in insp_details:
            temp={}
            if(m3.Marked_Members.objects.filter(item_no__insp_no_id=i['insp_no']).exists()):
                temp['total_status']=m3.Marked_Members.objects.filter(item_no__insp_no_id=i['insp_no']).count()
                temp['reply_status']=m3.Marked_Members.objects.filter(item_no__insp_no_id=i['insp_no'],status_flag=3).count()
                if temp['total_status']==temp['reply_status']:
                    temp['reply_status_flag']="True"
                else:
                    temp['reply_status_flag']="False"
            else:
                temp['total_status']=int(0)
                temp['reply_status']=int(0)
                temp['reply_status_flag']="False"
            if m3.Marked_Members.objects.filter(item_no__insp_no=i['insp_no'],status_flag=3):
                temp['sr_no']=count
                temp['insp_no']=i['insp_no']
                temp['status_flag']=i['status_flag']
                temp['mom_note_no']=i['mom_note_no']
                temp['mom_title']=i['mom_title']
                temp['mom_date']=i['mom_date']
                temp['created_on']=i['created_on']
                receive_reply.append(temp)
                count=count+1
        # #print("heelllo",receive_reply)
        context={'receive_reply':receive_reply,}
        return render(request,"mom_received_action.html",context)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="mom_received_action",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "mom_errors.html", {})
     
   
def reject_action_data(request):
    try:
        if request.method == "GET" and request.is_ajax():
            marked_no = request.GET.get('marked_no')
            reject_desig = list(m3.Marked_Members.objects.filter(marked_no=marked_no).values('marked_to__designation'))
            item_no=m3.Marked_Members.objects.filter(marked_no=marked_no)[0].item_no_id
            item_no_des=m3.Item_details.objects.filter(item_no=item_no)[0].des_id
            insp_no=m3.Item_details.objects.filter(item_no=item_no)[0].insp_no_id
            # #print(marked_no,'_____',reject_desig,'_____',item_no,'_____',item_no_des,'_____',insp_no)
            return JsonResponse({'item_no':item_no,'item_no_des':item_no_des,'insp_no':insp_no,'reject_desig':reject_desig})

    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="reject_action_data",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "mom_errors.html", {})
    
def reject_reply_ajax(request):
    try:
        if request.method == 'GET' or request.is_ajax:
            user=request.user.username
            if request.user.user_role == 'guest':
                cuser=request.user.guest_email
            designation=models.Level_Desig.objects.exclude(official_email_ID = None).filter(Q(official_email_ID=user) | Q(official_email_ID=request.user),empno__isnull=False)
            empno=designation[0].empno_id
            insp_no = request.GET.get('insp_no')
            item_no = request.GET.get('item_no')
            marked_no = request.GET.get('marked_no')
            remark_id = request.GET.get('remark_id')
            obj = m3.Marked_Members.objects.filter(marked_no=marked_no)
            # if m3.Reject_remark.objects.filter(marked_no_id=marked_no).exists():
            #     m3.Reject_remark.objects.filter(marked_no_id=marked_no,status_flag=0).update(status_flag=1)
            m3.Reject_remark.objects.create(marked_desig=obj[0].marked_to,marked_no=obj[0],created_on=datetime.now(),created_by=empno,reply_received=obj[0].reply_text,file_received=obj[0].reply_file,reply_on=obj[0].reply_on,remark=remark_id,reject_on=datetime.now())
            m3.Marked_Members.objects.filter(marked_no=marked_no).update(reply_on=None,reply_file='',reply_text=None,status_flag=1,status='R')
            
            m3.Item_details.objects.filter(item_no=item_no).update(status_flag=2)
            m3.Insp_details.objects.filter(insp_no=insp_no).update(status_flag=2)

            if m3.Marked_Members.objects.filter(item_no=item_no).exclude(status_flag=1).count()==0:
                m3.Item_details.objects.filter(item_no=item_no).update(status_flag=1)
            if m3.Item_details.objects.filter(insp_no=insp_no).exclude(status_flag=1).count()==0:
                m3.Insp_details.objects.filter(insp_no=insp_no).update(status_flag=1)

            return JsonResponse({},safe=False)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="reject_reply_ajax",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "mom_errors.html", {})

def mom_dash_ajax(request):
    try:
        if request.method == "GET" and request.is_ajax():
            insp_no=request.GET.get('insp_no') 
            insp_details=m3.Insp_details.objects.filter(insp_no=insp_no).values()
            marked_details=m3.Marked_Members.objects.filter(item_no__insp_no=insp_no).values('item_no_id','reply_text','reply_file','reply_on','marked_to__designation')
            list1=[]
            list2=[]
            for i in insp_details:
                temp={}
                temp['insp_no']=i['insp_no']
                temp['note_no']=i['mom_note_no']   
                temp['mdate']=i['mom_date'].strftime("%d/%m/%Y")
                temp['title']=i['mom_title']
            list1.append(temp)
            for i in marked_details:
                if(m3.Item_details.objects.filter(item_no=i['item_no_id'])):
                    list_item=m3.Item_details.objects.filter(item_no=i['item_no_id']).values()
                    temp={}
                    temp['item_db']=i['item_no_id']
                    temp['marked_to']=i['marked_to__designation']
                    temp['item_no']=list_item[0]['des_id']
                    if i['reply_on']:
                        temp['reply_on']=i['reply_on'].strftime("%d/%m/%y")
                    else:
                        temp['reply_on']=''
                    temp['text']=i['reply_text']
                    if(i['reply_file']):
                        temp['file']=i['reply_file']
                        #print(temp['file'])
                list2.append(temp)
            #print(list2,'1234')
            return JsonResponse({'insp_details':list1,'item_details':list2,},safe=False)
        return JsonResponse({"success":False}, status = 400) 
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="mom_dash_ajax",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "mom_errors.html", {})

def mom_dash_ajax_recd(request):
    try:
        if request.method == "GET" and request.is_ajax():
            insp_no=request.GET.get('insp_no') 
            user=request.user.username
            if request.user.user_role == 'guest':
                user=request.user.guest_email
            desig_id=models.Level_Desig.objects.exclude(official_email_ID = None).filter(Q(official_email_ID=user) | Q(official_email_ID=request.user)).values()
            insp_details=m3.Insp_details.objects.filter(insp_no=insp_no).values()
            marked_details=m3.Marked_Members.objects.filter(item_no__insp_no=insp_no,marked_to=desig_id[0]['designation_code']).values('item_no_id','reply_text','reply_file','reply_on','marked_to__designation')
            list1=[]
            list2=[]
            for i in insp_details:
                temp={}
                temp['insp_no']=i['insp_no']
                temp['note_no']=i['mom_note_no']   
                temp['mdate']=i['mom_date'].strftime("%d/%m/%Y")
                temp['title']=i['mom_title']
            list1.append(temp)
            for i in marked_details:
                if(m3.Item_details.objects.filter(item_no=i['item_no_id'])):
                    list_item=m3.Item_details.objects.filter(item_no=i['item_no_id']).values()
                    temp={}
                    temp['item_db']=i['item_no_id']
                    temp['marked_to']=i['marked_to__designation']
                    temp['item_no']=list_item[0]['des_id']
                    # if i['status_flag']==1 and i['status']=='R':
                    #     temp['reply_on']=''
                    # else:
                    if i['reply_on']:
                        temp['reply_on']=i['reply_on'].strftime("%d/%m/%y")
                    else:
                        temp['reply_on']=''
                    temp['text']=i['reply_text']
                    if(i['reply_file']):
                        temp['file']=i['reply_file']
                        #print(temp['file'])
                list2.append(temp)
            #print(list2,'1234')
            return JsonResponse({'insp_details':list1,'item_details':list2,},safe=False)
        return JsonResponse({"success":False}, status = 400) 
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="mom_dash_ajax_recd",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "errorspage.html", {})
        
def chaser_view(request):
    try:
        user=request.user.username
        if request.user.user_role == 'guest':
                user=request.user.guest_email
        desigid=models.Level_Desig.objects.exclude(official_email_ID=None).filter(Q(official_email_ID=request.user)| Q(official_email_ID=request.user.guest_email) | Q(official_email_ID=request.user.email))
        context={}
        list1=[]
        if desigid[0].d_level=='CRB' or desigid[0].d_level=='BM' or desigid[0].d_level=='Secy_RB':
            item_list=m3.Item_details.objects.values('insp_no_id','item_no','des_id','item_heading','item_subheading','item_description','item_decision','type','status_flag').order_by('item_no')
            for i in item_list:
                if m3.Marked_Members.objects.filter(item_no=i['item_no']).exists():
                    temp={}
                    mom_detail=m3.Insp_details.objects.filter(insp_no=i['insp_no_id']).values('insp_no','mom_date','mom_note_no','status_flag')
                    temp['insp_no']=mom_detail[0]['insp_no']
                    temp['mom_date']=mom_detail[0]['mom_date']
                    temp['mom_note_no']=mom_detail[0]['mom_note_no']
                    temp['status_flag']=mom_detail[0]['status_flag']
                    temp['item_no']=i['item_no']
                    temp['des_id']=i['des_id']
                    temp['item_heading']=i['item_heading']
                    temp['item_subheading']=i['item_subheading']
                    temp['item_description']=i['item_description']
                    temp['item_decision']=i['item_decision']
                    temp['type']=i['type']
                    temp['status_flag_item']=i['status_flag']
                    temp['marked']=m3.Marked_Members.objects.filter(item_no=i['item_no']).values('marked_to__designation','reply_text','reply_file')
                    #print(temp['marked'],'12345')
                    temp['remarks']=m3.Reject_remark.objects.filter(marked_no__item_no=i['item_no']).values('remark','reject_on')
                    #print(temp['remarks'],'12345')
                    list1.append(temp)
            context={
                'insp_details':list1,
            }
        return render(request,"chaser_view.html",context)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="chaser_view",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "mom_errors.html", {})

def mom_doneby_list1(request):
    try:
        user=request.user.username
        if request.user.user_role == 'guest':
                user=request.user.guest_email
        mom_desig=models.Level_Desig.objects.exclude(official_email_ID = None).filter(Q(official_email_ID=user) | Q(official_email_ID=request.user))
        context={}
        # RB
        # if m3.Insp_details.objects.filter(type=0).exists and (mom_desig[0].d_level=='CRB' or mom_desig[0].d_level=='BM' or mom_desig[0].d_level=='Secy_RB'):
        #     mom_data=m3.Insp_details.objects.filter(mom_officer_id=mom_desig[0].designation_code,type=0, status_flag__in=[1,2,3,4]).values().distinct().order_by('-insp_no')
        #     # #print(mom_data,'mom_data')
        #     # exclude(status_flag=1,status='R')
        #     list_mom_details=[]
        #     for i in mom_data:
        #         temp={}
        #         if(m3.Marked_Members.objects.filter(item_no__insp_no_id=i['insp_no']).exists()):
        #             temp['insp']=i['insp_no']
        #             temp['total_status']=m3.Marked_Members.objects.filter(item_no__insp_no_id=i['insp_no']).count()
        #             temp['reply_status']=m3.Marked_Members.objects.filter(item_no__insp_no_id=i['insp_no'],status_flag=3).count()
        #         else:
        #             temp['insp']=i['insp_no']
        #             temp['total_status']=int(0)
        #             temp['reply_status']=int(0)
        #         list_mom_details.append(temp)
        #     meeting=''
        #     context={'mom_data':mom_data,'str':'RB','meeting':meeting,'list_mom_details':list_mom_details}
        
        # GM
        if m3.Insp_details.objects.filter(type=1,mom_officer=mom_desig[0].designation_code).exists and (mom_desig[0].d_level=='GM' or mom_desig[0].d_level=='PHOD' or mom_desig[0].d_level=='AGM' or mom_desig[0].d_level=='Secy_GM' or mom_desig[0].d_level=='CRB' or mom_desig[0].d_level=='BM'):
            mom_data=m3.Insp_details.objects.filter(type=1,mom_officer_id=mom_desig[0].designation_code, status_flag__in=[1,2,3,4]).values().distinct().order_by('-insp_no')
            # #print(mom_data,'mom_data')
            list_mom_details=[]
            for i in mom_data:
                temp={}
                if(m3.Marked_Members.objects.filter(item_no__insp_no_id=i['insp_no']).exists()):
                    temp['insp']=i['insp_no']
                    temp['total_status']=m3.Marked_Members.objects.filter(item_no__insp_no_id=i['insp_no']).count()
                    temp['reply_status']=m3.Marked_Members.objects.filter(item_no__insp_no_id=i['insp_no'],status_flag=3).count()
                else:
                    temp['insp']=i['insp_no']
                    temp['total_status']=int(0)
                    temp['reply_status']=int(0)
                list_mom_details.append(temp)
            meeting=list(m3.meeting_typelist.objects.filter(default_flag=1).values('meeting_type').distinct().order_by('meeting_type'))
            meetings=(list(m3.meeting_typelist.objects.filter(default_flag=0,added_by=mom_desig[0].designation_code).values('meeting_type').distinct().order_by('meeting_type')))
            for m in meetings:
                meeting.append({'meeting_type': m['meeting_type']})
            context={'mom_data':mom_data,'str':'NoRB','meeting':meeting,'list_mom_details':list_mom_details}
        
        # OTHERS
        elif m3.Insp_details.objects.filter(type=2,mom_officer=mom_desig[0].designation_code).exists():
            mom_data=m3.Insp_details.objects.filter(type=2,mom_officer_id=mom_desig[0].designation_code,status_flag__in=[1,2,3,4]).values().distinct().order_by('-insp_no')
            # #print(mom_data,'mom_data')
            list_mom_details=[]
            for i in mom_data:
                temp={}
                if(m3.Marked_Members.objects.filter(item_no__insp_no_id=i['insp_no']).exists()):
                    temp['insp']=i['insp_no']
                    temp['total_status']=m3.Marked_Members.objects.filter(item_no__insp_no_id=i['insp_no']).count()
                    temp['reply_status']=m3.Marked_Members.objects.filter(item_no__insp_no_id=i['insp_no'],status_flag=3).count()
                else:
                    temp['insp']=i['insp_no']
                    temp['total_status']=int(0)
                    temp['reply_status']=int(0)
                list_mom_details.append(temp)
            meeting=list(m3.meeting_typelist.objects.filter(default_flag=1).values('meeting_type').distinct().order_by('meeting_type'))
            meetings=(list(m3.meeting_typelist.objects.filter(default_flag=0,added_by=mom_desig[0].designation_code).values('meeting_type').distinct().order_by('meeting_type')))
            for m in meetings:
                meeting.append({'meeting_type': m['meeting_type']})
            context={'mom_data':mom_data,'str':'NoRB','meeting':meeting,'list_mom_details':list_mom_details}
        
        return render(request,"mom_doneby_list1.html",context)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="mom_doneby_list1",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "mom_errors.html", {})

def mom_modal_ajax(request):
    try:
        if request.method == "GET" and request.is_ajax():
            insp_no=request.GET.get('insp_no')
            insp_details=m3.Insp_details.objects.filter(insp_no=insp_no).values()
            note_no=m3.Insp_details.objects.filter(insp_no=insp_no)[0].mom_note_no
            mdate=m3.Insp_details.objects.filter(insp_no=insp_no)[0].mom_date
            mom_date=mdate.strftime("%d/%m/%Y")
            #print(mom_date,'1234')
            marked_details=m3.Marked_Members.objects.filter(item_no__insp_no=insp_no).values('item_no_id','reply_text','reply_file','reply_on','marked_to__designation','status_flag')
            #print(insp_no,'insp_no',insp_details,'insp_details',marked_details,'marked_details')
            list1=[]
            list2=[]
            for i in insp_details:
                temp={}
                temp['insp_no']=i['insp_no']
                temp['note_no']=i['mom_note_no']   
                temp['mdate']=i['mom_date'].strftime("%d/%m/%Y")
                temp['title']=i['mom_title']
            list1.append(temp)
            for i in marked_details:
                if(m3.Item_details.objects.filter(item_no=i['item_no_id'])):
                    list_item=m3.Item_details.objects.filter(item_no=i['item_no_id']).values()
                    temp={}
                    temp['item_db']=i['item_no_id']
                    temp['item_no']=list_item[0]['des_id']
                    temp['marked_to']=i['marked_to__designation']
                    temp['status_flag']=i['status_flag']
                    if i['status_flag']==3:
                        temp['reply_on']=i['reply_on'].strftime("%d/%m/%y")
                        temp['text']=i['reply_text']
                        if(i['reply_file']):
                            temp['file']=i['reply_file']
                        else:
                            temp['file']=''
                    else:
                        temp['reply_on']=''
                        temp['text']=''
                        temp['file']=''
                list2.append(temp)
            #print(list2,'1234gunjan4321')
            return JsonResponse({'insp_details':list1,'item_details':list2,'note_no':note_no,'mom_date':mom_date}, safe = False)
        return JsonResponse({"success":False}, status=400)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="mom_modal_ajax",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "mom_errors.html", {})

def rbmins(request):
    try:
        user=request.user.username
        if request.user.user_role == 'guest':
                user=request.user.guest_email
        mom_desig=models.Level_Desig.objects.filter(Q(official_email_ID=user) | Q(official_email_ID=request.user)).exclude(official_email_ID=None)
        context={}

        all = m3.Insp_details.objects.filter(meeting_type="Board Meeting").count()
        partial=m3.Insp_details.objects.filter(status_flag=2,meeting_type="Board Meeting").count()
        closed=m3.Insp_details.objects.filter(status_flag=4,meeting_type="Board Meeting").count()
        pending=m3.Insp_details.objects.filter(status_flag=1,meeting_type="Board Meeting").count()
        # RB
        if m3.Insp_details.objects.filter(type=0).exists and (mom_desig[0].d_level=='CRB' or mom_desig[0].d_level=='BM' or mom_desig[0].d_level=='Secy_RB'):
            mom_data=m3.Insp_details.objects.filter(type=0).values().distinct().order_by('-insp_no')
            # #print(mom_data,'mom_data')
            list_mom_details=[]
            for i in mom_data:
                temp={}
                if(m3.Marked_Members.objects.filter(item_no__insp_no_id=i['insp_no']).exists()):
                    temp['insp']=i['insp_no']
                    temp['total_status']=m3.Marked_Members.objects.filter(item_no__insp_no_id=i['insp_no']).count()
                    temp['reply_status']=m3.Marked_Members.objects.filter(item_no__insp_no_id=i['insp_no'],status_flag=3).count()
                else:
                    temp['insp']=i['insp_no']
                    temp['total_status']=int(0)
                    temp['reply_status']=int(0)
                list_mom_details.append(temp)
            context={'mom_data':mom_data,'list_mom_details':list_mom_details,'all':all,'partial':partial,'closed':closed,'pending':pending}
        
        return render(request,"dash_mom_dobeby_list.html",context)
    except Exception as e:
        #print(e)
        try:
            m1.error_Table.objects.create(fun_name="mom_doneby_list1",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "mom_errors.html", {})
		
def filterdata_ajax_pr(request):		
	if request.method == "GET" and request.is_ajax():
            user=request.user.username
            if request.user.user_role == 'guest':
                user=request.user.guest_email
            desigid=models.Level_Desig.objects.exclude(official_email_ID=None).filter(Q(official_email_ID=request.user)| Q(official_email_ID=request.user.guest_email) | Q(official_email_ID=request.user.email))[0].designation_code  
            # d_level=models.Level_Desig.objects.filter(official_email_ID=user)[0].d_level
            # #print(user, desigid, d_level, 'EXTRA')
            # str=request.GET.get('str')
            status=request.GET.get('status')
            #print("status",type(status))
            # startDate=request.GET.get('startDate')
            # startDate = datetime.strptime(startDate,'%Y-%m-%d')
            # endDate=request.GET.get('endDate')
            # endDate = datetime.strptime(endDate,'%Y-%m-%d')
            # #print(str,'str',status,'status',startDate,'startDate',endDate,'endDate')
            # meeting_type=request.GET.get('meeting_type')
            # if(meeting_type==''):
            #     meeting_type=NULL
            # #print(meeting_type,'meeting_type')
            list_filter=[]
            count=1
            if(status=='0'):
                insp_details=m3.Insp_details.objects.filter(meeting_type='Board Meeting').values().order_by('insp_no')
                #print(insp_details,'12345')
            else:
                insp_details=m3.Insp_details.objects.filter(status_flag=int(status),meeting_type='Board Meeting').values().order_by('insp_no')
                #print(insp_details,'54321')
            for i in insp_details:
                    temp={}
                    temp['sr_no']=count
                    temp['insp_no']=i['insp_no']
                    temp['mom_date']=i['mom_date'].strftime("%d/%m/%y")
                    temp['mom_note_no']=i['mom_note_no']
                    temp['mom_title']=i['mom_title']
                    if(i['status_flag']==1):
                        temp['status']='Pending'
                    elif(i['status_flag']==2):
                        temp['status']='Partial'
                    elif(i['status_flag']==3):
                        temp['status']='Completed'
                    elif(i['status_flag']==4):
                        temp['status']='Closed'
                    temp['meeting_type']=i['meeting_type']
                    if(m3.Marked_Members.objects.filter(item_no__insp_no_id=i['insp_no']).exists()):
                        temp['total_status']=m3.Marked_Members.objects.filter(item_no__insp_no_id=i['insp_no']).count()
                        temp['reply_status']=m3.Marked_Members.objects.filter(item_no__insp_no_id=i['insp_no'],status_flag=3).count()
                    else:
                        temp['total_status']=int(0)
                        temp['reply_status']=int(0)
                    list_filter.append(temp)
                    count=count+1
            
            return JsonResponse({'list_filter':list_filter})

def filterReceivedata_ajax(request):
    try:
        if request.method == "GET" and request.is_ajax():
            user=request.user.username
            if request.user.user_role == 'guest':
                user=request.user.guest_email
            desigid=models.Level_Desig.objects.exclude(official_email_ID=None).filter(Q(official_email_ID=request.user)| Q(official_email_ID=request.user.guest_email) | Q(official_email_ID=request.user.email))[0].designation_code  
            d_level=models.Level_Desig.objects.exclude(official_email_ID = None).filter(Q(official_email_ID=user) | Q(official_email_ID=request.user))[0].d_level
            
            
            daterange=request.GET.get('date')
            #print('date1234',daterange)
            daterange1=daterange.split('-')
            #print('daterange1',daterange1[0],daterange1[1])
            
        
            date1=daterange1[0].split('/')
            date2=daterange1[1].split('/')
            #print("dates",date1,date2)
            date1=date1[2].strip()+'-'+date1[1].strip()+'-'+date1[0].strip()
            date2=date2[2].strip()+'-'+date2[1].strip()+'-'+date2[0].strip()
            #print("datesssss",date1,date2)
   
            receive_reply=[]
            count=1
            insp_details=m3.Insp_details.objects.filter(mom_officer_id=desigid).values().order_by('-insp_no')
            for i in insp_details:
                if m3.Marked_Members.objects.filter(item_no__insp_no=i['insp_no'],created_on__date__range=[date1,date2],status_flag=3):
                    temp={}
                    temp['sr_no']=count
                    temp['insp_no']=i['insp_no']
                    temp['mom_note_no']=i['mom_note_no']
                    temp['mom_title']=i['mom_title']
                    temp['mom_date']=i['mom_date'].strftime("%d/%m/%Y")
                    temp['created_on']=i['created_on'].strftime("%d/%m/%Y")
                    receive_reply.append(temp)
                    count=count+1
            #print(receive_reply,'filterReceivedata_ajax')
            context={'receive_reply':receive_reply,}
            return JsonResponse({'result':receive_reply},safe=False)
        return JsonResponse({'success':False},status=404)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="mom_received_action",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "mom_errors.html", {})

#vivek
def draft_mom_details(request):
    try:
        if request.method == "POST" and request.is_ajax():
            user=request.user.username
            if request.user.user_role == 'guest':
                user=request.user.guest_email
            final=request.POST.get('final_partinspectedDt')
            final_id=request.POST.get('id_partinspectedDt')
            type1=request.POST.get('typeDt')
            title=request.POST.get('titleMOMDt')
            present=json.loads(request.POST.get('presentDt'))
            copyto=json.loads(request.POST.get('copytoDt'))
            mdate1=request.POST.get('mdateDt')
            mdate=datetime.strptime(mdate1, '%d/%m/%Y').strftime('%Y-%m-%d')
            designation=models.Level_Desig.objects.filter(official_email_ID=user,empno__isnull=False)

            if m3.meeting_typelist.objects.filter(meeting_type=type1).exists():
                xyz='xyz'
            else:
                empnox = models.Level_Desig.objects.filter(Q(official_email_ID=request.user)| Q(official_email_ID=request.user.guest_email) | Q(official_email_ID=request.user.email), empno__isnull=False)
                if empnox:
                    empno = empnox[0].empno_id
                    desig = empnox[0].designation_code
                    print(desig,empnox)
                m3.meeting_typelist.objects.create(meeting_type=type1,default_flag=0, added_by=empnox[0])

            if (designation[0].empno_id):
                empno=designation[0].empno_id

            else:
                empno=''
            desig=designation[0].designation
            desig_id=designation[0].designation_code
            level=designation[0].d_level

            finalval = json.loads(final)
            final_allid = json.loads(final_id)
            year = str(datetime.now().year)


            if level=='CRB' or level=='BM' or level=='Secy_RB':
                note_ = year+'/'
                last_note1 = m3.Insp_details.objects.filter(mom_note_no__istartswith=note_).aggregate(Max('note_last'))
                if last_note1['note_last__max'] == None:
                    last_note1 = 1
                    note_no = year+'/Secy/Bd. Mtg/'+ str(last_note1)  
                else:
                    last_note1 = int(last_note1['note_last__max']) +1
                    note_no = year+'/Secy/Bd. Mtg/'+ str(last_note1)
                title='MINUTES OF MEETING OF THE BOARD HELD ON '+ datetime.strptime(mdate1, '%d/%m/%Y').strftime("%d/%m/%y")           
                m3.Insp_details.objects.create(created_on=datetime.now(),created_by=empno,mom_officer_id=desig_id,mom_title=title,mom_date=mdate,status_flag=0,type=0,meeting_type='Board Meeting')
           
            else:
     
                if level=='GM' or level=='PHOD' or level=='AGM' or level=='Secy_GM':
                    m3.Insp_details.objects.create(created_on=datetime.now(),created_by=empno,mom_officer_id=desig_id,mom_title=title,mom_date=mdate,status_flag=0,type=1,meeting_type=type1)
                else:
                    m3.Insp_details.objects.create(created_on=datetime.now(),created_by=empno,mom_officer_id=desig_id,mom_title=title,mom_date=mdate,status_flag=0,type=2,meeting_type=type1)
           
            insp_id=m3.Insp_details.objects.all().last().insp_no


            # storing item details
            officer_email=[]
            for f, b in zip(finalval, final_allid):
                #print(finalval[f], final_allid[b])
                for x,y in zip(finalval[f], final_allid[b]):
                    s = y.split('.')
                    # for heading
                    if len(s) == 1:
                        hed = 'heading'+y
                        heading = finalval[f][hed]
                        #print('#########################################', heading, y)
                        m3.Item_details.objects.create(item_heading=heading, created_on=datetime.now(), created_by=empno, type='H', des_id=y, insp_no_id=insp_id, status_flag=0)
                        y2=str(y+'.1')
                        if y2 in final_allid[b]:
                            ##print('if',y2)
                            pass
                        else:
                       
                            pr = 'Hpriority'+y
                            trz = 'Htargetdate'+y
                            officm = 'Hofficer'+y
                            remark = 'remarks'+y
                            remarks = finalval[f][remark]
                            priority = finalval[f][pr]
                            targetd = finalval[f][trz]
                            dealt = finalval[f][officm]
                            #print(officm,'HEADING')
                            # dealtofficer = dealt.split(',')%d/%m/%Y
                            if targetd:
                                t_date = datetime.strptime(targetd, '%d/%m/%y').strftime('%Y-%m-%d')
                            else:
                                t_date = None
                            # if priority:
                            #     pass
                            # else:
                            #     priority=None
                            # item_priority=priority, target_date=t_date,


                            #print(officm,'HEADING',priority,t_date,targetd)
                            m3.Item_details.objects.filter(item_heading=heading, created_by=empno, type='H', des_id=y, insp_no_id=insp_id, status_flag=0).update(item_priority=priority, target_date=t_date,remarks=remarks)
                            if dealt:
                                #print(dealt)
                               
                                item_id=m3.Item_details.objects.all().last().item_no
                                for i in dealt:
                                    Desig_mark=models.Level_Desig.objects.filter(designation__in=i.split(','))


                                    email=models.Level_Desig.objects.filter(designation__in=i.split(','))[0].official_email_ID
                                    officer_email.append(email)
                                    if Desig_mark:
                                        Desig_mark_code=Desig_mark[0].designation_code
                                        if m3.Marked_Members.objects.all().last():
                                            marked_no_id=(m3.Marked_Members.objects.all().last().marked_no)+1
                                        else:
                                            marked_no_id = 1
                                        m3.Marked_Members.objects.create(created_on=datetime.now(),created_by=empno, marked_no=marked_no_id,status_flag=0, item_no_id=item_id,marked_to_id=int(Desig_mark_code))
                                    else:
                                        print('ERROR-HEADING')
                            # else:
                                # m3.Item_details.objects.create(item_heading=heading, created_on=datetime.now(), created_by=empno, type='H', des_id=y, insp_no_id=insp_id, item_priority=priority, target_date=t_date, status_flag=0)
                                # item_id=m3.Item_details.objects.all().last().item_no
                    # for sub heading
                    elif len(s) == 2:
                        x1=y.split('.')[0]
                        x2=y.split('.')[1]
                        Pitem=x1+x2
                        shed = 'subheading'+y
                        shded= 'description'+y
                        pr = 'SHpriority'+Pitem
                        trz = 'SHtargetdate'+y
                        officm = 'SHofficer'+Pitem
                        remark = 'shremarks'+y
                        remarks = finalval[f][remark]
                        subheading = finalval[f][shed]
                        description= finalval[f][shded]
                        priority = finalval[f][pr]
                        targetd = finalval[f][trz]
                        dealt = finalval[f][officm]
                        # #print(dealt,'SUBHEADING')
                        # dealtofficer = dealt.split(',')
                        if targetd:
                            t_date = datetime.strptime(targetd, '%d/%m/%y').strftime('%Y-%m-%d')
                        else:
                            t_date = None


                        if description!='':
                            pass
                        else:
                            description=None
                        if dealt:
                            m3.Insp_details.objects.filter(insp_no=insp_id).update(status_flag=0)
                            m3.Item_details.objects.create(item_subheading=subheading, created_on=datetime.now(), created_by=empno, type='SH', des_id=y, item_description=description,item_priority=priority, insp_no_id=insp_id, target_date=t_date, status_flag=0,remarks=remarks)
                            item_id=m3.Item_details.objects.all().last().item_no
                            for i in dealt:
                                Desig_mark=models.Level_Desig.objects.filter(designation__in=i.split(','))
                                if Desig_mark:
                                    Desig_mark_code=Desig_mark[0].designation_code
                                    if m3.Marked_Members.objects.all().last():
                                        marked_no_id=(m3.Marked_Members.objects.all().last().marked_no)+1
                                    else:
                                        marked_no_id = 1
                                    m3.Marked_Members.objects.create(created_on=datetime.now(),created_by=empno, marked_no=marked_no_id,status_flag=0, item_no_id=item_id,marked_to_id=int(Desig_mark_code))
                                else:
                                    print('ERROR-SUB-HEADING')
                        else:
                            m3.Item_details.objects.create(item_subheading=subheading, created_on=datetime.now(), created_by=empno, type='SH', des_id=y, item_description=description,item_priority=priority, insp_no_id=insp_id, target_date=t_date, status_flag=0,remarks=remarks)
                            item_id=m3.Item_details.objects.all().last().item_no
 
                    else:
                        x1=y.split('.')[0]
                        x2=y.split('.')[1]
                        x3=y.split('.')[2]
                        Pitem=x1+x2+x3
                        ded = 'decision'+y
                        pr = 'Dpriority'+Pitem
                        trz = 'Dtargetdate'+y
                        officm = 'Dofficer'+Pitem
                        remark = 'remarks'+y
                        remarks = finalval[f][remark]
                        decision = finalval[f][ded]
                        priority = finalval[f][pr]
                        targetd = finalval[f][trz]
                        dealt = finalval[f][officm]


                        if targetd:
                            t_date = datetime.strptime(targetd, '%d/%m/%y').strftime('%Y-%m-%d')
                        else:
                            t_date = None
 
                        if dealt:
                           
                            m3.Item_details.objects.create(item_decision=decision, created_on=datetime.now(), created_by=empno, type='D', des_id=y, insp_no_id=insp_id, item_priority=priority, target_date=t_date, status_flag=0, remarks=remarks)
                            item_id=m3.Item_details.objects.all().last().item_no
                            for i in dealt:
                                Desig_mark=models.Level_Desig.objects.filter(designation__in=i.split(','))


                                if Desig_mark:
                                    Desig_mark_code=Desig_mark[0].designation_code
                                    if m3.Marked_Members.objects.all().last():
                                        marked_no_id=(m3.Marked_Members.objects.all().last().marked_no)+1
                                    else:
                                        marked_no_id = 1
                                    m3.Marked_Members.objects.create(created_on=datetime.now(),created_by=empno, marked_no=marked_no_id,status_flag=0, item_no_id=item_id,marked_to_id=int(Desig_mark_code))
                                else:
                                    print('ERROR-DECISION')
                        else:
                            m3.Item_details.objects.create(item_decision=decision, created_on=datetime.now(), created_by=empno, type='D', des_id=y, insp_no_id=insp_id, item_priority=priority, target_date=t_date, status_flag=0, remarks=remarks)
                            item_id=m3.Item_details.objects.all().last().item_no
       
            # # storing member details
            present_email=[]  
            for o in present:
                member_desig=models.Level_Desig.objects.filter(designation=o)
                if len(member_desig)!=0:
                    member_desig=models.Level_Desig.objects.filter(designation=o)[0].designation_code

                    email=models.Level_Desig.objects.filter(designation=o)[0].official_email_ID
                    present_email.append(email)
                    m3.Insp_members.objects.create(member_desig_id=member_desig,insp_no_id=insp_id)
                else:
                    m3.Insp_members.objects.create(other_members=o,insp_no_id=insp_id)
           
            # mail to dealt officers
            if officer_email:
                try:
                    dealt_contact=[]
                    des=''
                    ids=''
                    count_dealt=len(officer_email)
                    countd=1
                    # #print(type(count_dealt),type(countd),'1234567890')
                    for i in officer_email:
                        # #print(count_dealt,countd,'1234567890')
                        a1=models.Level_Desig.objects.filter(official_email_ID=i).values('designation','designation_code','contactnumber')
                        if count_dealt==countd:
                            # #print('a')
                            des+=a1[0]['designation']
                            ids+=str(a1[0]['designation_code'])
                            # #print(des,'a',ids)
                        else:
                            #print('b')
                            des+=a1[0]['designation']+', '
                            ids+=str(a1[0]['designation_code'])+', '
                            countd+=1
                            # #print(des,'b',ids)
                        if a1[0]['contactnumber']:
                            dealt_contact.append(a1[0]['contactnumber'])
                    # if len(dealt_contact) > 0:
                    #     for contact in dealt_contact:
                    #         MomSendSms(contact)
                    To=officer_email
                    details=m3.Insp_details.objects.filter(insp_no=insp_id).values('mom_title','insp_no','mom_officer__designation','meeting_type','mom_date')
                    subject=details[0]['mom_title']
                    context = {
                        'title': details[0]['mom_title'],
                        'meeting_type': details[0]['meeting_type'],
                        'mom_date': details[0]['mom_date'],
                        'insp_no': details[0]['insp_no'],
                        'mom_officer': details[0]['mom_officer__designation'],
                        'str': 'dealtby'            
                    }    
                    m3.copydealt_mail.objects.create(insp_no_id=insp_id,created_on=datetime.now(),created_by=empno,send_to=des,subject=subject,body=details[0]['mom_title'],area='DealtBy')
                    m6.copyto_mails.objects.create(created_on=datetime.now(),sender_id_id=desig_id,doc_id=insp_id,doc_table='m',receiver_id=ids,receiver_desig=des, subject='MOM Report', body=details[0]['mom_title'],area_flag=2)
                  
                except:
                    print("ERROR-DEALT-MAIL")
                    # messages.error(request, 'Request to sent e-mail to dealt officers failed. Please Try Again.')
       
            # mail to copy-to officers
            if copyto:
                try:
                    copy_mail =[]
                    copy_desig=[]
                    copy_contact=[]
                    copy_desig_list=''
                    copy_id_list=''
                    count_copy=len(copyto)
                    countc=1
                    print(copyto,"copyto")
                    for i in copyto:
                        mail_contact=models.Level_Desig.objects.filter(designation_code=i)
                        if count_copy==countc:
                            copy_desig_list+=mail_contact[0].designation
                            copy_id_list+=str(mail_contact[0].designation_code)
                        else:
                            copy_desig_list+=mail_contact[0].designation+','
                            copy_id_list+=str(mail_contact[0].designation_code)+','
                            countc+=1
                        copy_desig.append(mail_contact[0].designation)
                        if mail_contact[0].official_email_ID:
                            copy_mail.append(mail_contact[0].official_email_ID)
                        if mail_contact[0].contactnumber:
                            copy_contact.append(mail_contact[0].contactnumber)

                    To=copy_mail
                    print(copy_desig_list,'d',copy_id_list)

                    details=m3.Insp_details.objects.filter(insp_no=insp_id).values('mom_title','insp_no','mom_officer__designation','meeting_type','mom_date')
                    subject=details[0]['mom_title']
                    m6.copyto_mails.objects.create(created_on=datetime.now(),sender_id_id=desig_id,doc_id=insp_id,doc_table='m',
                                                   receiver_id=copy_id_list,receiver_desig=copy_desig_list,
                            subject='MOM Report', body=details[0]['mom_title'],area_flag=0)
                    context = {
                        'title': details[0]['mom_title'],
                        'meeting_type': details[0]['meeting_type'],
                        'mom_date': details[0]['mom_date'],
                        'insp_no': details[0]['insp_no'],
                        'mom_officer': details[0]['mom_officer__designation'],
                        'str': 'copyto'          
                    }  
                    m3.copydealt_mail.objects.create(insp_no_id=insp_id,created_on=datetime.now(),created_by=empno,send_to=copy_desig_list,subject=subject,body=title,area='CopyTo')
                    
                    # MomSendMail(subject,To,context,details[0]['insp_no'])
                    # messages.success(request, 'E-mail has been send successfully to copy-to officers.')  
                except:
                    print("ERROR-COPY-MAIL")
                    # messages.error(request, 'Request to sent e-mail to dealt officers failed. Please Try Again.')
           
            return JsonResponse({"status": 1,})
        return JsonResponse({"success": False}, status=400)
    except Exception as e:
        try:
            m1.error_Table.objects.create(fun_name="create_mom_details",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "mom_errors.html", {})

def draft_mom_doneby_list(request):
    user=request.user.username
    if request.user.user_role == 'guest':
                user=request.user.guest_email
    mom_desig=models.Level_Desig.objects.exclude(official_email_ID = None).filter(Q(official_email_ID=user) | Q(official_email_ID=request.user))
    context={}

    # RB
    # if m3.Insp_details.objects.filter(type=0).exists() and (mom_desig[0].d_level=='CRB' or mom_desig[0].d_level=='BM' or mom_desig[0].d_level=='Secy_RB'):
    #     mom_data=m3.Insp_details.objects.filter(mom_officer_id=mom_desig[0].designation_code,status_flag=0, type=0).values().distinct().order_by('-insp_no')
    #     list_mom_details=[]
    #     for i in mom_data:
    #         temp={}
    #         if(m3.Marked_Members.objects.filter(item_no__insp_no_id=i['insp_no']).exists()):
    #             temp['insp']=i['insp_no']
    #             temp['total_status']=m3.Marked_Members.objects.filter(item_no__insp_no_id=i['insp_no']).count()
    #             temp['reply_status']=m3.Marked_Members.objects.filter(item_no__insp_no_id=i['insp_no'],status_flag=3).count()
    #         else:
    #             temp['insp']=i['insp_no']
    #             temp['total_status']=int(0)
    #             temp['reply_status']=int(0)
    #         list_mom_details.append(temp)
    #     meeting=''
    #     context={'mom_data':mom_data,'str':'RB','meeting':meeting,'list_mom_details':list_mom_details}
   
    # GM
    print(mom_desig[0].d_level, m3.Insp_details.objects.filter(mom_officer=mom_desig[0].designation_code).exists())
    if m3.Insp_details.objects.filter(type=1,mom_officer=mom_desig[0].designation_code).exists() and (mom_desig[0].d_level=='GM' or mom_desig[0].d_level=='PHOD' or mom_desig[0].d_level=='AGM' or mom_desig[0].d_level=='Secy_GM' or mom_desig[0].d_level=='CRB' or mom_desig[0].d_level=='BM'):
        mom_data=m3.Insp_details.objects.filter(type=1,status_flag=0, mom_officer_id=mom_desig[0].designation_code).values().distinct().order_by('-insp_no')
        print(mom_data,'mom_data')
        meeting=''
        list_mom_details=[]
        for i in mom_data:
            temp={}
            if(m3.Marked_Members.objects.filter(item_no__insp_no_id=i['insp_no']).exists()):
                temp['insp']=i['insp_no']
                temp['total_status']=m3.Marked_Members.objects.filter(item_no__insp_no_id=i['insp_no']).count()
                temp['reply_status']=m3.Marked_Members.objects.filter(item_no__insp_no_id=i['insp_no'],status_flag=3).count()
            else:
                temp['insp']=i['insp_no']
                temp['total_status']=int(0)
                temp['reply_status']=int(0)
            list_mom_details.append(temp)
            meeting=list(m3.meeting_typelist.objects.filter(default_flag=1).values('meeting_type').distinct().order_by('meeting_type'))
            meetings=(list(m3.meeting_typelist.objects.filter(default_flag=0,added_by=mom_desig[0].designation_code).values('meeting_type').distinct().order_by('meeting_type')))
            for m in meetings:
                meeting.append({'meeting_type': m['meeting_type']})
        context={'mom_data':mom_data,'str':'GM','meeting':meeting,'list_mom_details':list_mom_details}
   
    # OTHERS
    elif m3.Insp_details.objects.filter(type=2,mom_officer=mom_desig[0].designation_code).exists():
        mom_data=m3.Insp_details.objects.filter(type=2,status_flag=0,mom_officer_id=mom_desig[0].designation_code).values().distinct().order_by('-insp_no')
        print(mom_data,'mom_data',mom_desig[0].designation_code)
        list_mom_details=[]
        for i in mom_data:
            temp={}
            if(m3.Marked_Members.objects.filter(item_no__insp_no_id=i['insp_no']).exists()):
                temp['insp']=i['insp_no']
                temp['total_status']=m3.Marked_Members.objects.filter(item_no__insp_no_id=i['insp_no']).count()
                temp['reply_status']=m3.Marked_Members.objects.filter(item_no__insp_no_id=i['insp_no'],status_flag=3).count()
            else:
                temp['insp']=i['insp_no']
                temp['total_status']=int(0)
                temp['reply_status']=int(0)
            list_mom_details.append(temp)
            meeting=list(m3.meeting_typelist.objects.filter(default_flag=1).values('meeting_type').distinct().order_by('meeting_type'))
            meetings=(list(m3.meeting_typelist.objects.filter(default_flag=0,added_by=mom_desig[0].designation_code).values('meeting_type').distinct().order_by('meeting_type')))
            for m in meetings:
                meeting.append({'meeting_type': m['meeting_type']})        
            context={'mom_data':mom_data,'str':'NoRB','meeting':meeting,'list_mom_details':list_mom_details}
    return render(request , 'draft_mom_doneby_list.html', context)

def delete_mom_draft(request, insp_no):

    if insp_no:
        m3.Insp_details.objects.filter(insp_no=insp_no).delete()
        return redirect('/draft_mom_doneby_list')
    else:
        return HttpResponse('<center><h1 style="color: red;">OOPS Error</h1></center>')


def drft_filterdata_ajax(request):
    try:
        if request.method == "GET" and request.is_ajax():
            # user=request.user.username
            # desigid=models.Level_Desig.objects.filter(official_email_ID=user)[0].designation_code
            # d_level=models.Level_Desig.objects.filter(official_email_ID=user)[0].d_level
            user=request.user.username
            if request.user.user_role == 'guest':
                user=request.user.guest_email
            mom_desig=models.Level_Desig.objects.exclude(official_email_ID = None).filter(Q(official_email_ID=user) | Q(official_email_ID=request.user))
            str=request.GET.get('str')
            types=int(request.GET.get('types'))
            mon_title=request.GET.get('mon_title')
            startDate=request.GET.get('startDate')
            if startDate=='':
                startDate=date.today() - relativedelta(years = 50)
            else:
                 startDate = datetime.strptime(startDate,'%Y-%m-%d')
            startDate = datetime.strftime(startDate,'%Y-%m-%d')
            endDate=request.GET.get('endDate')
            if endDate=='':
                endDate=date.today()
            else:
                endDate = datetime.strptime(endDate,'%Y-%m-%d')
            endDate = datetime.strftime(endDate,'%Y-%m-%d')
            meeting_type=request.GET.get('meeting_type')

            # print(types,startDate,endDate,meeting_type,mon_title)
            list_filter=[]
           
            if meeting_type=='All':
                if mon_title=='':
                    list_filter=list(m3.Insp_details.objects.filter(type=types,status_flag=0,mom_date__range=[startDate, endDate], mom_officer_id=mom_desig[0].designation_code).values().distinct().order_by('-insp_no'))
                else:
                    list_filter=list(m3.Insp_details.objects.filter(type=types,status_flag=0,mom_date__range=[startDate, endDate],mom_title__icontains=mon_title, mom_officer_id=mom_desig[0].designation_code).values().distinct().order_by('-insp_no'))

                # if startDate != '' and endDate != '' and mon_title == '':
                #     list_filter=list(m3.Insp_details.objects.filter(mom_date__range=[startDate, endDate], status_flag=0).values().order_by('insp_no'))
                # elif startDate == '' and endDate == '' and mon_title != '':
                #     list_filter=list(m3.Insp_details.objects.filter(mom_title__icontains=mon_title, status_flag=0).values().order_by('insp_no'))
                # else:
                #     list_filter=list(m3.Insp_details.objects.filter(mom_date__range=[startDate, endDate], mom_title__icontains=mon_title, status_flag=0).values().order_by('insp_no'))

            else:
                if mon_title=='':
                    list_filter=list(m3.Insp_details.objects.filter(type=types,status_flag=0,mom_date__range=[startDate, endDate],meeting_type=meeting_type, mom_officer_id=mom_desig[0].designation_code).values().distinct().order_by('-insp_no'))
                else:
                    list_filter=list(m3.Insp_details.objects.filter(type=types,status_flag=0,mom_date__range=[startDate, endDate],meeting_type=meeting_type, mom_title__icontains=mon_title, mom_officer_id=mom_desig[0].designation_code).values().distinct().order_by('-insp_no'))

            # print(list_filter)
            # else:
            #     # list_filter=list(m3.Insp_details.objects.filter(mom_date__range=[startDate, endDate],meeting_type=meeting_type, mom_title__icontains=mon_title,status_flag=0).values().order_by('insp_no'))
           
            #     if startDate != '' and endDate != '' and mon_title == '':
            #         list_filter=list(m3.Insp_details.objects.filter(mom_date__range=[startDate, endDate],meeting_type=meeting_type, status_flag=0).values().order_by('insp_no'))
            #     elif startDate == '' and endDate == '' and mon_title != '':
            #         list_filter=list(m3.Insp_details.objects.filter(mom_title__icontains=mon_title,meeting_type=meeting_type, status_flag=0).values().order_by('insp_no'))
            #     else:
            #         list_filter=list(m3.Insp_details.objects.filter(mom_date__range=[startDate, endDate],meeting_type=meeting_type, mom_title__icontains=mon_title, status_flag=0).values().order_by('insp_no'))
            
            # for i in insp_details:
            #     if m3.Marked_Members.objects.filter(item_no__insp_no=i['insp_no'],marked_to=desigid,status_flag=0):
            #         temp={}
                   
            #         temp['insp_no']=i['insp_no']


            #         temp['mom_title']=i['mom_title']
            #         temp['mom_date']=i['mom_date'].strftime("%d/%m/%y")
            #         list_filter.append(temp)
                          
            return JsonResponse({'list_filter':list_filter})
        else:
            return JsonResponse({'list_filter':list_filter})
    except Exception as e:
        try:
            m1.error_Table.objects.create(fun_name="draft_filterdata_ajax",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "mom_errors.html", {})

def edit_mom_details(request):
    try:
        if request.method == "POST" and request.is_ajax():
            user=request.user.username
            if request.user.user_role == 'guest':
                user=request.user.guest_email
            final=request.POST.get('final_partinspected')
            final_id=request.POST.get('id_partinspected')
            type1=request.POST.get('type')
            title=request.POST.get('titleMOM')
            insp_id=request.POST.get('momInsp')
            buttonValue=request.POST.get('buttonValue')

            present=json.loads(request.POST.get('present'))
            copyto=json.loads(request.POST.get('copyto'))
            mdate1=request.POST.get('mdate')
            mdate=datetime.strptime(mdate1, '%d/%m/%Y').strftime('%Y-%m-%d')
            # #print(final,'--',final_id,'--',present,'--',copyto,'--',mdate,'--',type1,'--','MOM-CREATE')
            designation=models.Level_Desig.objects.filter(official_email_ID=user,empno__isnull=False)

            if (designation[0].empno_id):
                empno=designation[0].empno_id
            else:
                empno=''
            desig=designation[0].designation
            desig_id=designation[0].designation_code
            level=designation[0].d_level

            # #print('level', level)


      
            finalval = json.loads(final)
            final_allid = json.loads(final_id)
            year = str(datetime.now().year)

            if buttonValue == 'Draft Submit':
                print('draft')
                if level=='CRB' or level=='BM' or level=='Secy_RB':
                    note_ = year+'/'
                    last_note1 = m3.Insp_details.objects.filter(mom_note_no__istartswith=note_).aggregate(Max('note_last'))
                    if last_note1['note_last__max'] == None:
                        last_note1 = 1
                        note_no = year+'/Secy/Bd. Mtg/'+ str(last_note1)  
                    else:
                        last_note1 = int(last_note1['note_last__max']) +1
                        note_no = year+'/Secy/Bd. Mtg/'+ str(last_note1)
                    title='MINUTES OF MEETING OF THE BOARD HELD ON '+ datetime.strptime(mdate1, '%d/%m/%Y').strftime("%d/%m/%y")

                    m3.Insp_details.objects.filter(insp_no=insp_id).update(mom_officer_id=desig_id,mom_title=title,mom_date=mdate,status_flag=0,type=0,meeting_type='Board Meeting')

                else:
                    if level=='GM' or level=='PHOD' or level=='AGM' or level=='Secy_GM':
                        m3.Insp_details.objects.filter(insp_no=insp_id).update(mom_officer_id=desig_id,mom_title=title,mom_date=mdate,status_flag=0,type=1,meeting_type=type1)
                    else:
                        m3.Insp_details.objects.filter(insp_no=insp_id).update(mom_officer_id=desig_id,mom_title=title,mom_date=mdate,status_flag=0,type=2,meeting_type=type1)

                obj = m3.Item_details.objects.filter(insp_no=insp_id)
                m3.Insp_details.objects.filter(insp_no=insp_id).update(status_flag=0)
                if obj.exists():
                    m3.Item_details.objects.filter(insp_no=insp_id).delete()
                    m6.copyto_mails.objects.filter(doc_table='m',doc_id=insp_id).delete()
                    m3.Insp_members.objects.filter(insp_no=insp_id).delete()
                    officer_email=[]
                    for f, b in zip(finalval, final_allid):
                        #print(finalval[f], final_allid[b])
                        for x,y in zip(finalval[f], final_allid[b]):
                            s = y.split('.')
                        # for heading
                            if len(s) == 1:
                                hed = 'heading'+y
                                heading = finalval[f][hed]

                                m3.Item_details.objects.create(item_heading=heading, created_on=datetime.now(), created_by=empno, type='H', des_id=y, insp_no_id=insp_id, status_flag=0)
                                y2=str(y+'.1')
                                if y2 in final_allid[b]:
                                    print('if',y2)
                                    pass
                                else:
                                
                                    pr = 'Hpriority'+y
                                    trz = 'Htargetdate'+y
                                    officm = 'Hofficer'+y
                                    remark = 'remarks'+y
                                    remarks = finalval[f][remark]
                                    priority = finalval[f][pr]
                                    targetd = finalval[f][trz]
                                    dealt = finalval[f][officm]
                                    # #print(officm,'HEADING')
                                    # dealtofficer = dealt.split(',')%d/%m/%Y
                                    if targetd:
                                        t_date = datetime.strptime(targetd, '%d/%m/%y').strftime('%Y-%m-%d')
                                    else:
                                        t_date = None
                                    # if priority:
                                    #     pass
                                    # else:
                                    #     priority=None
                                    # item_priority=priority, target_date=t_date,
                                    print(hed,'  ',priority,' ',t_date)
                                    m3.Item_details.objects.filter(item_heading=heading, created_by=empno, type='H', des_id=y, insp_no_id=insp_id, status_flag=0).update(item_priority=priority, target_date=t_date,remarks=remarks)
                                    # m3.Item_details.objects.create(item_heading=heading, created_on=datetime.now(), created_by=empno, type='H', des_id=y, insp_no_id=insp_id, item_priority=priority, target_date=t_date, status_flag=0)
                                    item_id=m3.Item_details.objects.all().last().item_no
                                    # m3.Item_details.objects.filter(item_heading=heading, created_on=datetime.now(), created_by=empno, type='H', des_id=y, insp_no_id=insp_id, status_flag=0).update(item_priority=priority, target_date=t_date,)
                                    if dealt:
                                        # #print(dealt)
                                        
                                        # item_id=m3.Item_details.objects.all().last().item_no
                                        for i in dealt:
                                            Desig_mark=models.Level_Desig.objects.filter(designation__in=i.split(','))

                                            email=models.Level_Desig.objects.filter(designation__in=i.split(','))[0].official_email_ID
                                            officer_email.append(email)
                                            if Desig_mark:
                                                Desig_mark_code=Desig_mark[0].designation_code
                                                if m3.Marked_Members.objects.all().last():
                                                    marked_no_id=(m3.Marked_Members.objects.all().last().marked_no)+1
                                                else:
                                                    marked_no_id = 1
                                                m3.Marked_Members.objects.create(created_on=datetime.now(),created_by=empno, marked_no=marked_no_id,status_flag=0, item_no_id=item_id,marked_to_id=int(Desig_mark_code))
                                            else:
                                                print('ERROR-HEADING')
                                    
                                        
                            # for sub heading
                            elif len(s) == 2:
                                x1=y.split('.')[0]
                                x2=y.split('.')[1]
                                Pitem=x1+x2
                                shed = 'subheading'+y
                                shded= 'description'+y
                                pr = 'SHpriority'+y
                                trz = 'SHtargetdate'+y
                                officm = 'SHofficer'+Pitem
                                remark = 'shremarks'+y
                                remarks = finalval[f][remark]
                                subheading = finalval[f][shed]
                                description= finalval[f][shded]
                                priority = finalval[f][pr]
                                targetd = finalval[f][trz]
                                dealt = finalval[f][officm]
                                # #print(dealt,'SUBHEADING')
                                # dealtofficer = dealt.split(',')
                                if targetd:
                                    t_date = datetime.strptime(targetd, '%d/%m/%y').strftime('%Y-%m-%d')
                                else:
                                    t_date = None

                                if description!='':
                                    pass
                                else:
                                    description=None
                                if dealt:
                                    m3.Insp_details.objects.filter(insp_no=insp_id).update(status_flag=0)
                                    m3.Item_details.objects.create(item_subheading=subheading, created_on=datetime.now(), created_by=empno, type='SH', des_id=y, item_description=description,item_priority=priority, insp_no_id=insp_id, target_date=t_date, status_flag=0, remarks=remarks)
                                    item_id=m3.Item_details.objects.all().last().item_no
                                    for i in dealt:
                                        Desig_mark=models.Level_Desig.objects.filter(designation__in=i.split(','))
                                        if Desig_mark:
                                            Desig_mark_code=Desig_mark[0].designation_code
                                            if m3.Marked_Members.objects.all().last():
                                                marked_no_id=(m3.Marked_Members.objects.all().last().marked_no)+1
                                            else:
                                                marked_no_id = 1
                                            m3.Marked_Members.objects.create(created_on=datetime.now(),created_by=empno, marked_no=marked_no_id,status_flag=0, item_no_id=item_id,marked_to_id=int(Desig_mark_code))
                                        else:
                                            print('ERROR-SUB-HEADING')
                                else:
                                    m3.Item_details.objects.create(item_subheading=subheading, created_on=datetime.now(), created_by=empno, type='SH', des_id=y, item_description=description,item_priority=priority, insp_no_id=insp_id, target_date=t_date, status_flag=0, remarks=remarks)
                                    item_id=m3.Item_details.objects.all().last().item_no
        
                            else:
                                x1=y.split('.')[0]
                                x2=y.split('.')[1]
                                x3=y.split('.')[2]
                                Pitem=x1+x2+x3
                                ded = 'decision'+y
                                pr = 'Dpriority'+y
                                trz = 'Dtargetdate'+y
                                officm = 'Dofficer'+Pitem
                                remark = 'remarks'+y
                                remarks = finalval[f][remark]
                                decision = finalval[f][ded]
                                priority = finalval[f][pr]
                                targetd = finalval[f][trz]
                                dealt = finalval[f][officm]

                                if targetd:
                                    t_date = datetime.strptime(targetd, '%d/%m/%y').strftime('%Y-%m-%d')
                                else:
                                    t_date = None
        
                                if dealt:
                                    
                                    m3.Item_details.objects.create(item_decision=decision, created_on=datetime.now(), created_by=empno, type='D', des_id=y, insp_no_id=insp_id, item_priority=priority, target_date=t_date, status_flag=0, remarks=remarks)
                                    item_id=m3.Item_details.objects.all().last().item_no
                                    for i in dealt:
                                        Desig_mark=models.Level_Desig.objects.filter(designation__in=i.split(','))

                                        if Desig_mark:
                                            Desig_mark_code=Desig_mark[0].designation_code
                                            if m3.Marked_Members.objects.all().last():
                                                marked_no_id=(m3.Marked_Members.objects.all().last().marked_no)+1
                                            else:
                                                marked_no_id = 1
                                            m3.Marked_Members.objects.create(created_on=datetime.now(),created_by=empno, marked_no=marked_no_id,status_flag=0, item_no_id=item_id,marked_to_id=int(Desig_mark_code))
                                        else:
                                            print('ERROR-DECISION')
                                else:
                                    m3.Item_details.objects.create(item_decision=decision, created_on=datetime.now(), created_by=empno, type='D', des_id=y, insp_no_id=insp_id, item_priority=priority, target_date=t_date, status_flag=0, remarks=remarks)
                                    item_id=m3.Item_details.objects.all().last().item_no
                
                    present_email=[]  
                    for o in present:
                        member_desig=models.Level_Desig.objects.filter(designation=o)
                        #print(member_desig,"heya",o)
                        if len(member_desig)!=0:
                            member_desig=models.Level_Desig.objects.filter(designation=o)[0].designation_code

                            email=models.Level_Desig.objects.filter(designation=o)[0].official_email_ID
                            present_email.append(email)
                            m3.Insp_members.objects.create(member_desig_id=member_desig,insp_no_id=insp_id)
                        else:
                            m3.Insp_members.objects.create(other_members=o,insp_no_id=insp_id)
                    # mail to dealt officers
                    if officer_email:
                        try:
                            dealt_contact=[]
                            des=''
                            ids=''
                            count_dealt=len(officer_email)
                            countd=1
                            # #print(type(count_dealt),type(countd),'1234567890')
                            for i in officer_email:
                                # #print(count_dealt,countd,'1234567890')
                                a1=models.Level_Desig.objects.filter(official_email_ID=i).values('designation','designation_code','contactnumber')
                                if count_dealt==countd:
                                    # #print('a')
                                    des+=a1[0]['designation']
                                    ids+=str(a1[0]['designation_code'])
                                    # #print(des,'a',ids)
                                else:
                                    #print('b')
                                    des+=a1[0]['designation']+', '
                                    ids+=str(a1[0]['designation_code'])+', '
                                    countd+=1
                                    # #print(des,'b',ids)
                                if a1[0]['contactnumber']:
                                    dealt_contact.append(a1[0]['contactnumber'])
                            # if len(dealt_contact) > 0:
                            #     for contact in dealt_contact:
                            #         MomSendSms(contact)
                            To=officer_email
                            details=m3.Insp_details.objects.filter(insp_no=insp_id).values('mom_title','insp_no','mom_officer__designation','meeting_type','mom_date')
                            subject=details[0]['mom_title']
                            context = {
                                'title': details[0]['mom_title'],
                                'meeting_type': details[0]['meeting_type'],
                                'mom_date': details[0]['mom_date'],
                                'insp_no': details[0]['insp_no'],
                                'mom_officer': details[0]['mom_officer__designation'],
                                'str': 'dealtby'            
                            }    
                            m3.copydealt_mail.objects.create(insp_no_id=insp_id,created_on=datetime.now(),created_by=empno,send_to=des,subject=subject,body=details[0]['mom_title'],area='DealtBy')
                            m6.copyto_mails.objects.create(created_on=datetime.now(),sender_id_id=desig_id,doc_id=insp_id,doc_table='m',receiver_id=ids,receiver_desig=des, subject='MOM Report', body=details[0]['mom_title'],area_flag=2)
                        
                        except:
                            print("ERROR-DEALT-MAIL")
                            # messages.error(request, 'Request to sent e-mail to dealt officers failed. Please Try Again.')
            
                    # mail to copy-to officers
                    if copyto:
                        try:
                            copy_mail =[]
                            copy_desig=[]
                            copy_contact=[]
                            copy_desig_list=''
                            copy_id_list=''
                            count_copy=len(copyto)
                            countc=1
                            print(copyto,"copyto")
                            for i in copyto:
                                mail_contact=models.Level_Desig.objects.filter(designation_code=i)
                                if count_copy==countc:
                                    copy_desig_list+=mail_contact[0].designation
                                    copy_id_list+=str(mail_contact[0].designation_code)
                                else:
                                    copy_desig_list+=mail_contact[0].designation+','
                                    copy_id_list+=str(mail_contact[0].designation_code)+','
                                    countc+=1
                                copy_desig.append(mail_contact[0].designation)
                                if mail_contact[0].official_email_ID:
                                    copy_mail.append(mail_contact[0].official_email_ID)
                                if mail_contact[0].contactnumber:
                                    copy_contact.append(mail_contact[0].contactnumber)

                            To=copy_mail
                            print(copy_desig_list,'d',copy_id_list)

                            details=m3.Insp_details.objects.filter(insp_no=insp_id).values('mom_title','insp_no','mom_officer__designation','meeting_type','mom_date')
                            subject=details[0]['mom_title']
                            m6.copyto_mails.objects.create(created_on=datetime.now(),sender_id_id=desig_id,doc_id=insp_id,doc_table='m',
                                                        receiver_id=copy_id_list,receiver_desig=copy_desig_list,
                                    subject='MOM Report', body=details[0]['mom_title'],area_flag=0)
                            context = {
                                'title': details[0]['mom_title'],
                                'meeting_type': details[0]['meeting_type'],
                                'mom_date': details[0]['mom_date'],
                                'insp_no': details[0]['insp_no'],
                                'mom_officer': details[0]['mom_officer__designation'],
                                'str': 'copyto'          
                            }  
                            m3.copydealt_mail.objects.create(insp_no_id=insp_id,created_on=datetime.now(),created_by=empno,send_to=copy_desig_list,subject=subject,body=title,area='CopyTo')
                            
                            # MomSendMail(subject,To,context,details[0]['insp_no'])
                            # messages.success(request, 'E-mail has been send successfully to copy-to officers.')  
                        except:
                            print("ERROR-COPY-MAIL")
                            # messages.error(request, 'Request to sent e-mail to dealt officers failed. Please Try Again.')
           
                else:
                    officer_email=[]
                    for f, b in zip(finalval, final_allid):
                        #print(finalval[f], final_allid[b])
                        for x,y in zip(finalval[f], final_allid[b]):
                            s = y.split('.')
                        # for heading
                            if len(s) == 1:
                                hed = 'heading'+y
                                heading = finalval[f][hed]

                                m3.Item_details.objects.create(item_heading=heading, created_on=datetime.now(), created_by=empno, type='H', des_id=y, insp_no_id=insp_id, status_flag=0)
                                y2=str(y+'.1')
                                if y2 in final_allid[b]:
                                    print('if',y2)
                                    pass
                                else:
                                
                                    pr = 'Hpriority'+y
                                    trz = 'Htargetdate'+y
                                    officm = 'Hofficer'+y
                                    remark = 'remarks'+y
                                    remarks = finalval[f][remark]
                                    priority = finalval[f][pr]
                                    targetd = finalval[f][trz]
                                    dealt = finalval[f][officm]
                                    # #print(officm,'HEADING')
                                    # dealtofficer = dealt.split(',')%d/%m/%Y
                                    if targetd:
                                        t_date = datetime.strptime(targetd, '%d/%m/%y').strftime('%Y-%m-%d')
                                    else:
                                        t_date = None
                                    # if priority:
                                    #     pass
                                    # else:
                                    #     priority=None
                                    # item_priority=priority, target_date=t_date,
                                    print(hed,'  ',priority,' ',t_date)
                                    m3.Item_details.objects.filter(item_heading=heading, created_by=empno, type='H', des_id=y, insp_no_id=insp_id, status_flag=0).update(item_priority=priority, target_date=t_date,remarks=remarks)
                                    # m3.Item_details.objects.create(item_heading=heading, created_on=datetime.now(), created_by=empno, type='H', des_id=y, insp_no_id=insp_id, item_priority=priority, target_date=t_date, status_flag=0)
                                    item_id=m3.Item_details.objects.all().last().item_no
                                    # m3.Item_details.objects.filter(item_heading=heading, created_on=datetime.now(), created_by=empno, type='H', des_id=y, insp_no_id=insp_id, status_flag=0).update(item_priority=priority, target_date=t_date,)
                                    if dealt:
                                        # #print(dealt)
                                        
                                        # item_id=m3.Item_details.objects.all().last().item_no
                                        for i in dealt:
                                            Desig_mark=models.Level_Desig.objects.filter(designation__in=i.split(','))

                                            email=models.Level_Desig.objects.filter(designation__in=i.split(','))[0].official_email_ID
                                            officer_email.append(email)
                                            if Desig_mark:
                                                Desig_mark_code=Desig_mark[0].designation_code
                                                if m3.Marked_Members.objects.all().last():
                                                    marked_no_id=(m3.Marked_Members.objects.all().last().marked_no)+1
                                                else:
                                                    marked_no_id = 1
                                                m3.Marked_Members.objects.create(created_on=datetime.now(),created_by=empno, marked_no=marked_no_id,status_flag=0, item_no_id=item_id,marked_to_id=int(Desig_mark_code))
                                            else:
                                                print('ERROR-HEADING')
                                    
                                        
                            # for sub heading
                            elif len(s) == 2:
                                x1=y.split('.')[0]
                                x2=y.split('.')[1]
                                Pitem=x1+x2
                                shed = 'subheading'+y
                                shded= 'description'+y
                                pr = 'SHpriority'+y
                                trz = 'SHtargetdate'+y
                                officm = 'SHofficer'+Pitem
                                remark = 'shremarks'+y
                                remarks = finalval[f][remark]
                                subheading = finalval[f][shed]
                                description= finalval[f][shded]
                                priority = finalval[f][pr]
                                targetd = finalval[f][trz]
                                dealt = finalval[f][officm]
                                # #print(dealt,'SUBHEADING')
                                # dealtofficer = dealt.split(',')
                                if targetd:
                                    t_date = datetime.strptime(targetd, '%d/%m/%y').strftime('%Y-%m-%d')
                                else:
                                    t_date = None

                                if description!='':
                                    pass
                                else:
                                    description=None
                                if dealt:
                                    m3.Insp_details.objects.filter(insp_no=insp_id).update(status_flag=0)
                                    m3.Item_details.objects.create(item_subheading=subheading, created_on=datetime.now(), created_by=empno, type='SH', des_id=y, item_description=description,item_priority=priority, insp_no_id=insp_id, target_date=t_date, status_flag=0, remarks=remarks)
                                    item_id=m3.Item_details.objects.all().last().item_no
                                    for i in dealt:
                                        Desig_mark=models.Level_Desig.objects.filter(designation__in=i.split(','))
                                        if Desig_mark:
                                            Desig_mark_code=Desig_mark[0].designation_code
                                            if m3.Marked_Members.objects.all().last():
                                                marked_no_id=(m3.Marked_Members.objects.all().last().marked_no)+1
                                            else:
                                                marked_no_id = 1
                                            m3.Marked_Members.objects.create(created_on=datetime.now(),created_by=empno, marked_no=marked_no_id,status_flag=0, item_no_id=item_id,marked_to_id=int(Desig_mark_code))
                                        else:
                                            print('ERROR-SUB-HEADING')
                                else:
                                    m3.Item_details.objects.create(item_subheading=subheading, created_on=datetime.now(), created_by=empno, type='SH', des_id=y, item_description=description,item_priority=priority, insp_no_id=insp_id, target_date=t_date, status_flag=0, remarks=remarks)
                                    item_id=m3.Item_details.objects.all().last().item_no
        
                            else:
                                x1=y.split('.')[0]
                                x2=y.split('.')[1]
                                x3=y.split('.')[2]
                                Pitem=x1+x2+x3
                                ded = 'decision'+y
                                pr = 'Dpriority'+Pitem
                                trz = 'Dtargetdate'+y
                                officm = 'Dofficer'+Pitem
                                remark = 'remarks'+y
                                remarks = finalval[f][remark]
                                decision = finalval[f][ded]
                                priority = finalval[f][pr]
                                targetd = finalval[f][trz]
                                dealt = finalval[f][officm]

                                if targetd:
                                    t_date = datetime.strptime(targetd, '%d/%m/%y').strftime('%Y-%m-%d')
                                else:
                                    t_date = None
        
                                if dealt:
                                    
                                    m3.Item_details.objects.create(item_decision=decision, created_on=datetime.now(), created_by=empno, type='D', des_id=y, insp_no_id=insp_id, item_priority=priority, target_date=t_date, status_flag=0, remarks=remarks)
                                    item_id=m3.Item_details.objects.all().last().item_no
                                    for i in dealt:
                                        Desig_mark=models.Level_Desig.objects.filter(designation__in=i.split(','))

                                        if Desig_mark:
                                            Desig_mark_code=Desig_mark[0].designation_code
                                            if m3.Marked_Members.objects.all().last():
                                                marked_no_id=(m3.Marked_Members.objects.all().last().marked_no)+1
                                            else:
                                                marked_no_id = 1
                                            m3.Marked_Members.objects.create(created_on=datetime.now(),created_by=empno, marked_no=marked_no_id,status_flag=0, item_no_id=item_id,marked_to_id=int(Desig_mark_code))
                                        else:
                                            print('ERROR-DECISION')
                                else:
                                    m3.Item_details.objects.create(item_decision=decision, created_on=datetime.now(), created_by=empno, type='D', des_id=y, insp_no_id=insp_id, item_priority=priority, target_date=t_date, status_flag=0, remarks=remarks)
                                    item_id=m3.Item_details.objects.all().last().item_no
                
                    # # storing member details
                    # present_email=[]   
                    # for o in present:
                    #     member_desig=models.Level_Desig.objects.filter(designation=o)[0].designation_code
                    #     email=models.Level_Desig.objects.filter(designation=o)[0].official_email_ID
                    #     present_email.append(email)
                    #     m3.Insp_members.objects.create(member_desig_id=member_desig,insp_no_id=insp_id)

                    present_email=[]  
                    for o in present:
                        member_desig=models.Level_Desig.objects.filter(designation=o)
                        #print(member_desig,"heya",o)
                        if len(member_desig)!=0:
                            member_desig=models.Level_Desig.objects.filter(designation=o)[0].designation_code

                            email=models.Level_Desig.objects.filter(designation=o)[0].official_email_ID
                            present_email.append(email)
                            m3.Insp_members.objects.create(member_desig_id=member_desig,insp_no_id=insp_id)
                        else:
                            m3.Insp_members.objects.create(other_members=o,insp_no_id=insp_id)
                    # mail to dealt officers
                    if officer_email:
                        try:
                            dealt_contact=[]
                            des=''
                            ids=''
                            count_dealt=len(officer_email)
                            countd=1
                            # #print(type(count_dealt),type(countd),'1234567890')
                            for i in officer_email:
                                # #print(count_dealt,countd,'1234567890')
                                a1=models.Level_Desig.objects.filter(official_email_ID=i).values('designation','designation_code','contactnumber')
                                if count_dealt==countd:
                                    # #print('a')
                                    des+=a1[0]['designation']
                                    ids+=str(a1[0]['designation_code'])
                                    # #print(des,'a',ids)
                                else:
                                    #print('b')
                                    des+=a1[0]['designation']+', '
                                    ids+=str(a1[0]['designation_code'])+', '
                                    countd+=1
                                    # #print(des,'b',ids)
                                if a1[0]['contactnumber']:
                                    dealt_contact.append(a1[0]['contactnumber'])
                            # if len(dealt_contact) > 0:
                            #     for contact in dealt_contact:
                            #         MomSendSms(contact)
                            To=officer_email
                            details=m3.Insp_details.objects.filter(insp_no=insp_id).values('mom_title','insp_no','mom_officer__designation','meeting_type','mom_date')
                            subject=details[0]['mom_title']
                            context = {
                                'title': details[0]['mom_title'],
                                'meeting_type': details[0]['meeting_type'],
                                'mom_date': details[0]['mom_date'],
                                'insp_no': details[0]['insp_no'],
                                'mom_officer': details[0]['mom_officer__designation'],
                                'str': 'dealtby'            
                            }    
                            m3.copydealt_mail.objects.create(insp_no_id=insp_id,created_on=datetime.now(),created_by=empno,send_to=des,subject=subject,body=details[0]['mom_title'],area='DealtBy')
                            m6.copyto_mails.objects.create(created_on=datetime.now(),sender_id_id=desig_id,doc_id=insp_id,doc_table='m',receiver_id=ids,receiver_desig=des, subject='MOM Report', body=details[0]['mom_title'],area_flag=2)
                        
                        except:
                            print("ERROR-DEALT-MAIL")
                            # messages.error(request, 'Request to sent e-mail to dealt officers failed. Please Try Again.')
            
                    # mail to copy-to officers
                    if copyto:
                        try:
                            copy_mail =[]
                            copy_desig=[]
                            copy_contact=[]
                            copy_desig_list=''
                            copy_id_list=''
                            count_copy=len(copyto)
                            countc=1
                            print(copyto,"copyto")
                            for i in copyto:
                                mail_contact=models.Level_Desig.objects.filter(designation_code=i)
                                if count_copy==countc:
                                    copy_desig_list+=mail_contact[0].designation
                                    copy_id_list+=str(mail_contact[0].designation_code)
                                else:
                                    copy_desig_list+=mail_contact[0].designation+','
                                    copy_id_list+=str(mail_contact[0].designation_code)+','
                                    countc+=1
                                copy_desig.append(mail_contact[0].designation)
                                if mail_contact[0].official_email_ID:
                                    copy_mail.append(mail_contact[0].official_email_ID)
                                if mail_contact[0].contactnumber:
                                    copy_contact.append(mail_contact[0].contactnumber)

                            To=copy_mail
                            print(copy_desig_list,'d',copy_id_list)

                            details=m3.Insp_details.objects.filter(insp_no=insp_id).values('mom_title','insp_no','mom_officer__designation','meeting_type','mom_date')
                            subject=details[0]['mom_title']
                            m6.copyto_mails.objects.create(created_on=datetime.now(),sender_id_id=desig_id,doc_id=insp_id,doc_table='m',
                                                        receiver_id=copy_id_list,receiver_desig=copy_desig_list,
                                    subject='MOM Report', body=details[0]['mom_title'],area_flag=0)
                            context = {
                                'title': details[0]['mom_title'],
                                'meeting_type': details[0]['meeting_type'],
                                'mom_date': details[0]['mom_date'],
                                'insp_no': details[0]['insp_no'],
                                'mom_officer': details[0]['mom_officer__designation'],
                                'str': 'copyto'          
                            }  
                            m3.copydealt_mail.objects.create(insp_no_id=insp_id,created_on=datetime.now(),created_by=empno,send_to=copy_desig_list,subject=subject,body=title,area='CopyTo')
                            
                            # MomSendMail(subject,To,context,details[0]['insp_no'])
                            # messages.success(request, 'E-mail has been send successfully to copy-to officers.')  
                        except:
                            print("ERROR-COPY-MAIL")
                            # messages.error(request, 'Request to sent e-mail to dealt officers failed. Please Try Again.')
                

                return JsonResponse({'status': 'Draft'})
                
            elif buttonValue == 'Submit':

                
                if level=='CRB' or level=='BM' or level=='Secy_RB':
                    note_ = year+'/'
                    last_note1 = m3.Insp_details.objects.filter(mom_note_no__istartswith=note_).aggregate(Max('note_last'))
                    if last_note1['note_last__max'] == None:
                        last_note1 = 1
                        note_no = year+'/Secy/Bd. Mtg/'+ str(last_note1)   
                    else:
                        last_note1 = int(last_note1['note_last__max']) +1
                        note_no = year+'/Secy/Bd. Mtg/'+ str(last_note1)
                    title='MINUTES OF MEETING OF THE BOARD HELD ON '+ datetime.strptime(mdate1, '%d/%m/%Y').strftime("%d/%m/%y")
                    m3.Insp_details.objects.filter(insp_no=insp_id).update(mom_officer_id=desig_id,mom_title=title,mom_date=mdate,note_last=last_note1,mom_note_no=note_no,status_flag=1,type=0,meeting_type='Board Meeting')
            
                else:
                    note_ = year+'/'+desig+'/'
                    last_note1 = m3.Insp_details.objects.filter(mom_note_no__istartswith=note_).aggregate(Max('note_last'))
                    if last_note1['note_last__max'] == None:
                        last_note1 = 1
                        note_no = year+'/'+desig+'/'+ str(last_note1)
                    else:
                        last_note1 = int(last_note1['note_last__max']) +1
                        note_no = year+'/'+desig+'/'+ str(last_note1)
                    # title='WEEKLY MINUTES OF MEETING HELD ON '+ datetime.strptime(mdate1, '%d/%m/%Y').strftime("%d/%m/%y")
                    # #print(title,"title of MOMoooooooooooooooooooooooooooooooooooooooooooo")
                    if level=='GM' or level=='PHOD' or level=='AGM' or level=='Secy_GM':
                        m3.Insp_details.objects.filter(insp_no=insp_id).update(mom_officer_id=desig_id,mom_title=title,mom_date=mdate,note_last=last_note1,mom_note_no=note_no,status_flag=1,type=1,meeting_type=type1)
                    # elif desig_details[0]['d_level']=='DRM' or desig_details[0]['d_level']=='BO':
                    else:
                        # #print(title,"title222222222222222222222 of MOMoooooooooooooooooooooooooooooooooooooooooooo")
                        m3.Insp_details.objects.filter(insp_no=insp_id).update(mom_officer_id=desig_id,mom_title=title,mom_date=mdate,note_last=last_note1,mom_note_no=note_no,status_flag=1,type=2,meeting_type=type1)
                
                    # #print('MOM CREATED',note_no)
                    messages.info(request, 'MOM successfully saved with MOM Note No: ',note_no)
            

                obj = m3.Item_details.objects.filter(insp_no=insp_id)
                m3.Insp_details.objects.filter(insp_no=insp_id).update(status_flag=1)
                if obj.exists():
                    m3.Item_details.objects.filter(insp_no=insp_id).delete()
                    m6.copyto_mails.objects.filter(doc_table='m',doc_id=insp_id).delete()
                    m3.Insp_members.objects.filter(insp_no=insp_id).delete()
                    officer_email=[]
                    for f, b in zip(finalval, final_allid):
                        # #print(finalval[f], final_allid[b])
                        for x,y in zip(finalval[f], final_allid[b]):
                            s = y.split('.')
                            # for heading
                            if len(s) == 1:
                                hed = 'heading'+y
                                heading = finalval[f][hed]

                                m3.Item_details.objects.create(item_heading=heading, created_on=datetime.now(), created_by=empno, type='H', des_id=y, insp_no_id=insp_id, status_flag=1)
                                y2=str(y+'.1')
                                if y2 in final_allid[b]:
                                    ##print('if',y2)
                                    pass
                                else:
                                
                                    pr = 'Hpriority'+y
                                    trz = 'Htargetdate'+y
                                    officm = 'Hofficer'+y
                                    remark = 'remarks'+y
                                    remarks = finalval[f][remark]
                                    priority = finalval[f][pr]
                                    targetd = finalval[f][trz]
                                    dealt = finalval[f][officm]
                                    # #print(officm,'HEADING')
                                    # dealtofficer = dealt.split(',')%d/%m/%Y
                                    if targetd:
                                        t_date = datetime.strptime(targetd, '%d/%m/%y').strftime('%Y-%m-%d')
                                    else:
                                        t_date = None
                                    # if priority:
                                    #     pass
                                    # else:
                                    #     priority=None
                                    # item_priority=priority, target_date=t_date,
                                    m3.Item_details.objects.filter(item_heading=heading, created_by=empno, type='H', des_id=y, insp_no_id=insp_id, status_flag=1).update(item_priority=priority, target_date=t_date,remarks=remarks)
                                    if dealt:
                                        item_id=m3.Item_details.objects.all().last().item_no
                                        for i in dealt:
                                            Desig_mark=models.Level_Desig.objects.filter(designation__in=i.split(','))

                                            email=models.Level_Desig.objects.filter(designation__in=i.split(','))[0].official_email_ID
                                            officer_email.append(email)
                                            if Desig_mark:
                                                Desig_mark_code=Desig_mark[0].designation_code
                                                if m3.Marked_Members.objects.all().last():
                                                    marked_no_id=(m3.Marked_Members.objects.all().last().marked_no)+1
                                                else:
                                                    marked_no_id = 1
                                                m3.Marked_Members.objects.create(created_on=datetime.now(),created_by=empno, marked_no=marked_no_id,status_flag=1, item_no_id=item_id,marked_to_id=int(Desig_mark_code))
                                            else:
                                                print('ERROR-HEADING')
                                    # else:
                                    #     m3.Item_details.objects.create(item_heading=heading, created_on=datetime.now(), created_by=empno, type='H', des_id=y, insp_no_id=insp_id, item_priority=priority, target_date=t_date, status_flag=1)
                                    #     # item_id=m3.Item_details.objects.all().last().item_no
                            # for sub heading
                            elif len(s) == 2:
                                x1=y.split('.')[0]
                                x2=y.split('.')[1]
                                Pitem=x1+x2
                                shed = 'subheading'+y
                                shded= 'description'+y
                                pr = 'SHpriority'+y
                                trz = 'SHtargetdate'+y
                                officm = 'SHofficer'+Pitem
                                remark = 'shremarks'+y
                                remarks = finalval[f][remark]
                                subheading = finalval[f][shed]
                                description= finalval[f][shded]
                                priority = finalval[f][pr]
                                targetd = finalval[f][trz]
                                dealt = finalval[f][officm]
                                # #print(dealt,'SUBHEADING')
                                # dealtofficer = dealt.split(',')
                                if targetd:
                                    t_date = datetime.strptime(targetd, '%d/%m/%y').strftime('%Y-%m-%d')
                                else:
                                    t_date = None

                                if description!='':
                                    pass
                                else:
                                    description=None
                                if dealt:
                                    m3.Insp_details.objects.filter(insp_no=insp_id).update(status_flag=1)
                                    m3.Item_details.objects.create(item_subheading=subheading, created_on=datetime.now(), created_by=empno, type='SH', des_id=y, item_description=description,item_priority=priority, insp_no_id=insp_id, target_date=t_date, status_flag=1, remarks= remarks)
                                    item_id=m3.Item_details.objects.all().last().item_no
                                    for i in dealt:
                                        Desig_mark=models.Level_Desig.objects.filter(designation__in=i.split(','))
                                        if Desig_mark:
                                            Desig_mark_code=Desig_mark[0].designation_code
                                            if m3.Marked_Members.objects.all().last():
                                                marked_no_id=(m3.Marked_Members.objects.all().last().marked_no)+1
                                            else:
                                                marked_no_id = 1
                                            m3.Marked_Members.objects.create(created_on=datetime.now(),created_by=empno, marked_no=marked_no_id,status_flag=1, item_no_id=item_id,marked_to_id=int(Desig_mark_code))
                                        else:
                                            print('ERROR-SUB-HEADING')
                                else:
                                    m3.Item_details.objects.create(item_subheading=subheading, created_on=datetime.now(), created_by=empno, type='SH', des_id=y, item_description=description,item_priority=priority, insp_no_id=insp_id, target_date=t_date, status_flag=1, remarks=remarks)
                                    item_id=m3.Item_details.objects.all().last().item_no
        
                            else:
                                x1=y.split('.')[0]
                                x2=y.split('.')[1]
                                x3=y.split('.')[2]
                                Pitem=x1+x2+x3
                                ded = 'decision'+y
                                pr = 'Dpriority'+y
                                trz = 'Dtargetdate'+y
                                officm = 'Dofficer'+Pitem
                                remark = 'remarks'+y
                                remarks = finalval[f][remark]
                                decision = finalval[f][ded]
                                priority = finalval[f][pr]
                                targetd = finalval[f][trz]
                                dealt = finalval[f][officm]

                                if targetd:
                                    t_date = datetime.strptime(targetd, '%d/%m/%y').strftime('%Y-%m-%d')
                                else:
                                    t_date = None
        
                                if dealt:
                                    
                                    m3.Item_details.objects.create(item_decision=decision, created_on=datetime.now(), created_by=empno, type='D', des_id=y, insp_no_id=insp_id, item_priority=priority, target_date=t_date, status_flag=1, remarks=remarks)
                                    item_id=m3.Item_details.objects.all().last().item_no
                                    for i in dealt:
                                        Desig_mark=models.Level_Desig.objects.filter(designation__in=i.split(','))

                                        if Desig_mark:
                                            Desig_mark_code=Desig_mark[0].designation_code
                                            if m3.Marked_Members.objects.all().last():
                                                marked_no_id=(m3.Marked_Members.objects.all().last().marked_no)+1
                                            else:
                                                marked_no_id = 1
                                            m3.Marked_Members.objects.create(created_on=datetime.now(),created_by=empno, marked_no=marked_no_id,status_flag=1, item_no_id=item_id,marked_to_id=int(Desig_mark_code))
                                        else:
                                            print('ERROR-DECISION')
                                else:
                                    m3.Item_details.objects.create(item_decision=decision, created_on=datetime.now(), created_by=empno, type='D', des_id=y, insp_no_id=insp_id, item_priority=priority, target_date=t_date, status_flag=4, remarks=remarks)
                                    item_id=m3.Item_details.objects.all().last().item_no
                
                    # # storing member details
                    present_email=[]   
                    for o in present:
                        member_desig=models.Level_Desig.objects.filter(designation=o)
                        #print(member_desig,"heya",o)
                        if len(member_desig)!=0:
                            member_desig=models.Level_Desig.objects.filter(designation=o)[0].designation_code

                            email=models.Level_Desig.objects.filter(designation=o)[0].official_email_ID
                            present_email.append(email)
                            m3.Insp_members.objects.create(member_desig_id=member_desig,insp_no_id=insp_id)
                        else:
                            m3.Insp_members.objects.create(other_members=o,insp_no_id=insp_id)
                    
                    # mail to dealt officers
                    if officer_email:
                        try:
                            dealt_contact=[]
                            des=''
                            ids=''
                            count_dealt=len(officer_email)
                            countd=1
                            # #print(type(count_dealt),type(countd),'1234567890')
                            for i in officer_email:
                                # #print(count_dealt,countd,'1234567890')
                                a1=models.Level_Desig.objects.filter(official_email_ID=i).values('designation','designation_code','contactnumber')
                                if count_dealt==countd:
                                    # #print('a')
                                    des+=a1[0]['designation']
                                    ids+=str(a1[0]['designation_code'])
                                    # #print(des,'a',ids)
                                else:
                                    #print('b')
                                    des+=a1[0]['designation']+', '
                                    ids+=str(a1[0]['designation_code'])+', '
                                    countd+=1
                                    # #print(des,'b',ids)
                                if a1[0]['contactnumber']:
                                    dealt_contact.append(a1[0]['contactnumber'])
                            # if len(dealt_contact) > 0:
                            #     for contact in dealt_contact:
                            #         MomSendSms(contact)
                            To=officer_email
                            details=m3.Insp_details.objects.filter(insp_no=insp_id).values('mom_title','insp_no','mom_officer__designation','meeting_type','mom_date')
                            subject=details[0]['mom_title']
                            context = {
                                'title': details[0]['mom_title'],
                                'meeting_type': details[0]['meeting_type'],
                                'mom_date': details[0]['mom_date'],
                                'insp_no': details[0]['insp_no'],
                                'mom_officer': details[0]['mom_officer__designation'],
                                'str': 'dealtby'            
                            }    
                            m3.copydealt_mail.objects.create(insp_no_id=insp_id,created_on=datetime.now(),created_by=empno,send_to=des,subject=subject,body=details[0]['mom_title'],area='DealtBy')
                            m6.copyto_mails.objects.create(created_on=datetime.now(),sender_id_id=desig_id,doc_id=insp_id,doc_table='m',receiver_id=ids,receiver_desig=des, subject='MOM Report', body=details[0]['mom_title'],area_flag=2)
                        
                        except:
                            print("ERROR-DEALT-MAIL")
                            # messages.error(request, 'Request to sent e-mail to dealt officers failed. Please Try Again.')
            
                    # mail to copy-to officers
                    if copyto:
                        try:
                            copy_mail =[]
                            copy_desig=[]
                            copy_contact=[]
                            copy_desig_list=''
                            copy_id_list=''
                            count_copy=len(copyto)
                            countc=1
                            print(copyto,"copyto")
                            for i in copyto:
                                mail_contact=models.Level_Desig.objects.filter(designation_code=i)
                                if count_copy==countc:
                                    copy_desig_list+=mail_contact[0].designation
                                    copy_id_list+=str(mail_contact[0].designation_code)
                                else:
                                    copy_desig_list+=mail_contact[0].designation+','
                                    copy_id_list+=str(mail_contact[0].designation_code)+','
                                    countc+=1
                                copy_desig.append(mail_contact[0].designation)
                                if mail_contact[0].official_email_ID:
                                    copy_mail.append(mail_contact[0].official_email_ID)
                                if mail_contact[0].contactnumber:
                                    copy_contact.append(mail_contact[0].contactnumber)

                            To=copy_mail
                            print(copy_desig_list,'d',copy_id_list)

                            details=m3.Insp_details.objects.filter(insp_no=insp_id).values('mom_title','insp_no','mom_officer__designation','meeting_type','mom_date')
                            subject=details[0]['mom_title']
                            m6.copyto_mails.objects.create(created_on=datetime.now(),sender_id_id=desig_id,doc_id=insp_id,doc_table='m',
                                                        receiver_id=copy_id_list,receiver_desig=copy_desig_list,
                                    subject='MOM Report', body=details[0]['mom_title'],area_flag=0)
                            context = {
                                'title': details[0]['mom_title'],
                                'meeting_type': details[0]['meeting_type'],
                                'mom_date': details[0]['mom_date'],
                                'insp_no': details[0]['insp_no'],
                                'mom_officer': details[0]['mom_officer__designation'],
                                'str': 'copyto'          
                            }  
                            m3.copydealt_mail.objects.create(insp_no_id=insp_id,created_on=datetime.now(),created_by=empno,send_to=copy_desig_list,subject=subject,body=title,area='CopyTo')
                            
                            # MomSendMail(subject,To,context,details[0]['insp_no'])
                            # messages.success(request, 'E-mail has been send successfully to copy-to officers.')  
                        except:
                            print("ERROR-COPY-MAIL")
                            # messages.error(request, 'Request to sent e-mail to dealt officers failed. Please Try Again.')
                
                
                return JsonResponse({"status": 'Submit', 'note_no':note_no})

           

            
            
        return JsonResponse({"success": False}, status=400)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="create_mom_details",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "mom_errors.html", {})


#APEKSHA CODE FOR SEARCH MOM
from datetime import date,datetime,timedelta
from dateutil.relativedelta import relativedelta
def fetch_mom_ajax_search(request):
    try:
        if request.method == 'GET' and request.is_ajax():
            # location_code=json.loads(request.GET.get("location_code"))
            # location_type=json.loads(request.GET.get("location_type"))
            meet_type=json.loads(request.GET.get("meet_type"))
            obser=request.GET.get("query")
            created_on=request.GET.get('created_on')
            designation=json.loads(request.GET.get("designation"))
            status=json.loads(request.GET.get('status'))
            newstatus=[]
            

            user=request.user.username
            if request.user.user_role == 'guest':
                user=request.user.guest_email
            desig_details=models.Level_Desig.objects.exclude(official_email_ID=None).filter(Q(official_email_ID=request.user)| Q(official_email_ID=request.user.guest_email) | Q(official_email_ID=request.user.email)).values()
            div_code = models.railwayLocationMaster.objects.filter(parent_rly_unit_code=desig_details[0]['rly_unit_id']).values('rly_unit_code')
                
            if status:
                for i in status:
                    if i=='Closed':
                        newstatus.append(4)
                    if i=='Pending':
                        newstatus.append(1)
                        newstatus.append(2)
                        newstatus.append(3)
            else:
                newstatus=[1,2,3,4]

            if len(meet_type)==0:
                   
                meet_type=list(m3.meeting_typelist.objects.filter(default_flag=1).values_list('meeting_type', flat=True).distinct().order_by('meeting_type'))
                meetings=(list(m3.meeting_typelist.objects.filter(default_flag=0,added_by=desig_details[0]['designation_code']).values('meeting_type').distinct().order_by('meeting_type')))
                for m in meetings:
                    meet_type.append(m['meeting_type'])

            # if len(location_code)==0:
            #     location_code=list(m1.Insp_multi_location.objects.filter(type='HQ').distinct('item').values_list('item',flat=True))
            
            # if len(location_type)==0:
            #     loc_name=list(models.railwayLocationMaster.objects.filter(Q(location_type_desc='DIVISION')|Q(location_type_desc='WORKSHOP')|Q(location_type_desc='INSTITUTE')|Q(location_type_desc='STORE')|Q(location_type_desc='CONSTRUCTION'),parent_location_code__in=location_code).values_list('location_code',flat=True).distinct('location_code'))
            #     loc_types=list(models.railwayLocationMaster.objects.filter(Q(location_type_desc='DIVISION')|Q(location_type_desc='WORKSHOP')|Q(location_type_desc='INSTITUTE')|Q(location_type_desc='STORE')|Q(location_type_desc='CONSTRUCTION'),parent_location_code__in=location_code).values_list('location_type',flat=True).distinct('location_type'))
            # else:
            #     loc_types=[]
            #     loc_name=[]
            #     for l in location_type:
            #         loc_types.append(l.split('-')[1])
            #         loc_name.append(l.split('-')[0])
            
            if len(designation)==0:
                designation=list(m3.Insp_details.objects.filter().distinct('mom_officer_id').values_list('mom_officer_id',flat=True)) 
            
            else:
                designation=list(models.Level_Desig.objects.filter(designation__in=designation).values_list('designation_code',flat=True).distinct('designation_code'))
            
            if created_on=='':
                startDate=date.today() - relativedelta(years = 50)
                endDate=date.today()
            else:
                startDate=created_on.split('to')[0].strip()
                startDate = datetime.strptime(startDate,'%d/%m/%Y')
                endDate=created_on.split('to')[1].strip()
                endDate = datetime.strptime(endDate,'%d/%m/%Y')
            startDate = datetime.strftime(startDate,'%Y-%m-%d')
            endDate = datetime.strftime(endDate,'%Y-%m-%d')
            
            # locations=list(m1.Insp_multi_location.objects.filter(Q(item__in=location_code)| Q(item__in=loc_name, type__in=loc_types)).values_list('inspection_no',flat=True).distinct('inspection_no'))
            # if len(location_type)!=0:
            #     locations=list(m1.Insp_multi_location.objects.filter( Q(item__in=loc_name, type__in=loc_types)).values_list('inspection_no',flat=True).distinct('inspection_no'))
            #     # print(locations)
            ins=list(m3.Insp_details.objects.filter(meeting_type__in=meet_type,mom_officer_id__in=designation,status_flag__in=newstatus,mom_date__gte=startDate,mom_date__lte=endDate).values())
            
            insp_filtered=[]
            for i in ins:
                ofc=list(models.Level_Desig.objects.filter(designation_code=i['mom_officer_id']).values('designation'))[0]['designation']
                i.update({'insp_ofc':ofc})
                insp_filtered.append(i['insp_no'])
                # locs=list(m1.Insp_multi_location.objects.filter(inspection_no=i['inspection_no']).values('item','type'))
                # rly=[]
                # div=[]
                # for l in locs:
                #     if l['type']=='HQ':
                #         rly.append(l['item'])
                #     else:
                #         d=l['item']+'-'+ l['type']
                #         div.append(d)
                # i.update({'rly':rly,'div':div})
                

            listsearch=[]
            
            if obser!='' and obser!='@@' :
                words=obser.split(' ')
                for w in words:
                    listsearch=list(m3.Item_details.objects.filter((Q(item_heading__icontains=w)|Q(item_description__icontains=w)|Q(item_subheading__icontains=w)|Q(item_decision__icontains=w)),insp_no__in=insp_filtered).values(
                        'item_no',
                        'item_heading','item_description','item_subheading','item_decision',
                        'insp_no__mom_date',
                        'insp_no','insp_no__mom_title',
                        'insp_no__mom_note_no','insp_no__created_on','insp_no__meeting_type',
                        'insp_no__mom_officer__designation',
                        'insp_no__status_flag','type').distinct('insp_no').exclude(insp_no__status_flag=0))
                
                for i in range(len(listsearch)):
                    if listsearch[i]['insp_no__mom_date']!=None:
                        x=listsearch[i]['insp_no__mom_date'].strftime('%d'+'/'+'%m'+'/'+'%Y')
                        listsearch[i].update({'insp_no__mom_date':x})
                    print(listsearch[i])
            
            return JsonResponse({'ins':ins,'listsearch':listsearch,}, safe=False)
        return JsonResponse({'success':False}, status=400)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="fetch_mom_ajax_search",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "errorspage.html", {})


def search_locat_mom(request):
    try:
        user=request.user.username
        if request.user.user_role == 'guest':
                user=request.user.guest_email
        desig_details=models.Level_Desig.objects.exclude(official_email_ID=None).filter(Q(official_email_ID=request.user)| Q(official_email_ID=request.user.guest_email) | Q(official_email_ID=request.user.email)).values()
        div_code = models.railwayLocationMaster.objects.filter(parent_rly_unit_code=desig_details[0]['rly_unit_id']).values('rly_unit_code')
            
        meeting=list(m3.meeting_typelist.objects.filter(default_flag=1).values('meeting_type').distinct().order_by('meeting_type'))
        meetings=(list(m3.meeting_typelist.objects.filter(default_flag=0,added_by=desig_details[0]['designation_code']).values('meeting_type').distinct().order_by('meeting_type')))
        for m in meetings:
            meeting.append({'meeting_type': m['meeting_type']})
        
        list1=models.railwayLocationMaster.objects.filter(location_type_desc__in=['RAILWAY BOARD', 'PRODUCTION UNIT', 'HEAD QUATER','OFFICE', 'PSU', 'PRODUCTION UNIT', 'INSTITUTE']).values('location_code').order_by('location_code')
        list2=[]
        for i in list1:
            list2.append(i['location_code'])
        list3=models.railwayLocationMaster.objects.filter(location_type_desc__in=['DIVISION','WORKSHOP']).values('location_code', 'location_type').order_by('location_code')

        list4=[]
        for i in list3:
            list4.append({'location_code':i['location_code'],'location_type':i['location_type']})  

        list5=models.departMast.objects.all().values('department_name').order_by('department_name')
        list6=[]
        for i in list5:
            list6.append(i['department_name'])
        
        list7=models.Level_Desig.objects.all().values('designation').order_by('designation')
        list8=[]
        for i in list7:
            list8.append(i['designation'])

        if request.method== 'POST':
            query = request.POST['query']
            que=Q()
            for word in query.split():
                que &=Q(observation__icontains=word)
            
            des_location=m1.Item_details.objects.filter(que)
            return render(request,'keyword_location_search.html', {'des_location':des_location})
        else:
            query = False
        
        
        
        context={'zone':list2,'division':list4,'dept':list6, 'desi':list8,'meeting':meeting}
        return render(request, 'search_mom.html',context)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="search_mom",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "errorspage.html", {}) 





def all_phods(request):
    if request.method == "POST" and request.is_ajax():
        empnox = models.Level_Desig.objects.exclude(delete_flag=True).exclude(official_email_ID = None).filter(Q(official_email_ID=request.user)| Q(official_email_ID=request.user.guest_email) | Q(official_email_ID=request.user.email), empno__isnull=False)
        if empnox:
            desig_code = empnox[0].designation_code
            desig = empnox[0].designation
            rly_code=empnox[0].rly_unit.location_code
            rly_unit_code=empnox[0].rly_unit.rly_unit_code
            parent_loc=empnox[0].rly_unit.parent_location_code
            parent_loc_id=empnox[0].rly_unit.parent_rly_unit_code
            div_code=rly_code
            div_unit_code=rly_unit_code
            if parent_loc!='RB':
                div_code=rly_code
                rly_code=parent_loc
                rly_unit_code=parent_loc_id

        existing_officers=json.loads(request.POST.get('existing_officers'))
        allphods=list(models.Level_Desig.objects.exclude(delete_flag=True).exclude(Q(empno_id=None)|Q(designation_code=desig_code)|Q(delete_flag=True)).filter(rly_unit=rly_unit_code,d_level='PHOD').distinct().values_list('designation',flat=True).order_by('-designation'))
        alldesig=[]
        for x in allphods:
            if x not in existing_officers:
                alldesig.append(x)
        if len(alldesig)==0:
            msg='PHODs already present'
        else:
            msg='PHODs added'
        others=list(models.Level_Desig.objects.exclude(Q(designation__in=alldesig)|Q(designation__in=existing_officers)|Q(empno_id=None)|Q(designation_code=desig_code)|Q(delete_flag=True)).values_list('designation',flat=True).order_by('designation'))
        print(existing_officers,alldesig,rly_unit_code)

        context={
            'msg':msg,
            'alldesig':json.dumps(alldesig),
            'others':json.dumps(others)
        }
        return JsonResponse(context, safe=False)
    return JsonResponse({'success':False}, status=400)  



# def desig_changecode(request):
#     try:
#         if request.method == "POST" or request.is_ajax():
#             officer_id=request.POST.get('officer_id')
#             desig=[]
#             testempno = json.loads(officer_id)
#             for i in range(len(testempno)):
#                 xx=models.Level_Desig.objects.filter(designation_code=testempno[i]).values('designation', ).distinct('designation')
#                 if len(xx)>0:
#                     desig.append(xx[0]['designation'])
#             testdesig = desig
#             officer_id=testempno
#             testmarkofficer=''
#             lstdict=[]
            
#             alldesig = models.Level_Desig.objects.filter(designation_code__in=testempno).values('d_level').distinct('d_level')
            
#             for i in alldesig:
#                 if i['d_level'] == 'GM':
#                     lst1=models.Level_Desig.objects.filter(d_level=i['d_level']).exclude(designation_code__in=testempno).count()
#                     if lst1 == 0:
#                         lst2=list(models.Level_Desig.objects.filter(designation_code__in=testempno).exclude(d_level=i['d_level']).values('designation_code','designation').order_by('designation'))
#                         if testmarkofficer != '':
#                             testmarkofficer+=','
#                         testmarkofficer=testmarkofficer+"All GM's/ZR"
#                         interkey=set(testempno)-set(map(lambda d: d['designation_code'], lst2))
#                         testempno=list(map(lambda d: d['designation_code'], lst2))
#                         testdesig=list(map(lambda d: d['designation'], lst2))
#                         lstdict.append({"desig":"All GM's/ZR","designation_code":list(interkey)})

#                 elif i['d_level'] == 'BM':
#                     lst1=models.Level_Desig.objects.filter(d_level=i['d_level']).exclude(designation_code__in=testempno).count()
#                     if lst1 == 0:
#                         lst2=list(models.Level_Desig.objects.filter(designation_code__in=testempno).exclude(d_level=i['d_level']).values('designation_code','designation').order_by('designation'))
#                         if testmarkofficer != '':
#                             testmarkofficer+=','
#                         testmarkofficer=testmarkofficer+"All Board Member's"
#                         interkey=set(testempno)-set(map(lambda d: d['designation_code'], lst2))
#                         testempno=list(map(lambda d: d['designation_code'], lst2))
#                         testdesig=list(map(lambda d: d['designation'], lst2))
#                         lstdict.append({"desig":"All Board Member's","designation_code":list(interkey)})


#                 elif i['d_level'] == 'PHOD':
#                     lst1=models.Level_Desig.objects.filter(d_level=i['d_level']).exclude(designation_code__in=testempno).count()
#                     if lst1 == 0:
#                         lst2=list(models.Level_Desig.objects.filter(designation_code__in=testempno).exclude(d_level=i['d_level']).values('designation_code','designation').order_by('designation'))
#                         if testmarkofficer != '':
#                             testmarkofficer+=','
#                         testmarkofficer=testmarkofficer+"All PHOD's"
#                         interkey=set(testempno)-set(map(lambda d: d['designation_code'], lst2))
#                         testempno=list(map(lambda d: d['designation_code'], lst2))
#                         testdesig=list(map(lambda d: d['designation'], lst2))
#                         lstdict.append({"desig":"All PHOD's","designation_code":list(interkey)})
#                     else:
#                         hq=models.railwayLocationMaster.objects.filter(parent_location_code__isnull=False).values('parent_location_code').distinct()
#                         for ii in hq:
#                             rlyunit=models.railwayLocationMaster.objects.filter(parent_location_code=ii['parent_location_code']).values('rly_unit_code')
#                             if models.Level_Desig.objects.filter(d_level=i['d_level'],rly_unit__in=rlyunit).exists():
#                                 lst3=models.Level_Desig.objects.filter(d_level=i['d_level'],rly_unit__in=rlyunit).exclude(designation_code__in=testempno).count()
#                                 if lst3 == 0:
#                                     lst2=list(models.Level_Desig.objects.filter(designation_code__in=testempno).exclude(d_level=i['d_level'],rly_unit__in=rlyunit).values('designation_code','designation').order_by('designation'))
#                                     if testmarkofficer != '':
#                                         testmarkofficer+=','
#                                     testmarkofficer=testmarkofficer+"All PHOD's"+ii['parent_location_code']
#                                     interkey=set(testempno)-set(map(lambda d: d['designation_code'], lst2))
#                                     testempno=list(map(lambda d: d['designation_code'], lst2))
#                                     testdesig=list(map(lambda d: d['designation'], lst2))
#                                     lstdict.append({"desig":"All PHOD's/"+ii['parent_location_code'],"designation_code":list(interkey)})



#                 elif i['d_level'] == 'DRM':
#                     lst1=models.Level_Desig.objects.filter(d_level=i['d_level']).exclude(designation_code__in=testempno).count()
#                     if lst1 == 0:
#                         lst2=list(models.Level_Desig.objects.filter(designation_code__in=testempno).exclude(d_level=i['d_level']).values('designation_code','designation').order_by('designation'))
#                         if testmarkofficer != '':
#                             testmarkofficer+=','
#                         testmarkofficer=testmarkofficer+"All DRM's"
#                         interkey=set(testempno)-set(map(lambda d: d['designation_code'], lst2))
#                         testempno=list(map(lambda d: d['designation_code'], lst2))
#                         testdesig=list(map(lambda d: d['designation'], lst2))
#                         lstdict.append({"desig":"All DRM's","designation_code":list(interkey)})
#                     else:
#                         hq=models.railwayLocationMaster.objects.filter(parent_location_code__isnull=False).values('parent_location_code').distinct()
#                         for ii in hq:
#                             rlyunit=models.railwayLocationMaster.objects.filter(parent_location_code=ii['parent_location_code']).values('rly_unit_code')
#                             if models.Level_Desig.objects.filter(d_level=i['d_level'],rly_unit__in=rlyunit).exists():
#                                 lst3=models.Level_Desig.objects.filter(d_level=i['d_level'],rly_unit__in=rlyunit).exclude(designation_code__in=testempno).count()
#                                 if lst3 == 0:
#                                     lst2=list(models.Level_Desig.objects.filter(designation_code__in=testempno).exclude(d_level=i['d_level'],rly_unit__in=rlyunit).values('designation_code','designation').order_by('designation'))
#                                     if testmarkofficer != '':
#                                         testmarkofficer+=','
#                                     testmarkofficer=testmarkofficer+"All DRM's/"+ii['parent_location_code']
#                                     interkey=set(testempno)-set(map(lambda d: d['designation_code'], lst2))
#                                     testempno=list(map(lambda d: d['designation_code'], lst2))
#                                     testdesig=list(map(lambda d: d['designation'], lst2))
#                                     lstdict.append({"desig":"All DRM's/"+ii['parent_location_code'],"designation_code":list(interkey)})

#             for i in range(len(testdesig)):
#                 if testmarkofficer != '':
#                     testmarkofficer+=','
#                 testmarkofficer=testmarkofficer+testdesig[i]
#                 lstdict.append({"desig":testdesig[i],"designation_code":[testempno[i]]})
#             context={'marked_id': json.dumps(officer_id), 'marked_desig': testmarkofficer,'marked_key':json.dumps(lstdict)}
#             return JsonResponse(context,safe = False)
#         return JsonResponse({"success":False}, status = 400)

#     except Exception as e: 
#         try:
#             m1.error_Table.objects.create(fun_name="desig_changecode",user_id=request.user,err_details=str(e))
#         except:
#             print("Internal Error!!!")
#         return render(request, "errorspage.html", {})




#NEW MODIFIED SAVE MOM CODE

# create_rbmom.html
# mom_received_action.html
# mom_reply_form.html
# mom_ReportPdf.html
# receivemomreply.html


# def desig_changecode_edit(request,testempno):
#     desig=[]
#     for i in range(len(testempno)):
#         xx=models.Level_Desig.objects.filter(designation_code=testempno[i]).values('designation', ).distinct('designation')
#         if len(xx)>0:
#             desig.append(xx[0]['designation'])
#     testdesig = desig
#     officer_id=testempno
#     testmarkofficer=''
#     lstdict=[]
#     alldesig = models.Level_Desig.objects.filter(designation_code__in=testempno).values('d_level').distinct('d_level')
#     for i in alldesig:
#         if i['d_level'] == 'GM':
#             lst1=models.Level_Desig.objects.filter(d_level=i['d_level']).exclude(designation_code__in=testempno).count()
#             if lst1 == 0:
#                 lst2=list(models.Level_Desig.objects.filter(designation_code__in=testempno).exclude(d_level=i['d_level']).values('designation_code','designation').order_by('designation'))
#                 if testmarkofficer != '':
#                     testmarkofficer+=','
#                 testmarkofficer=testmarkofficer+"All GM's/ZR"
#                 interkey=set(testempno)-set(map(lambda d: d['designation_code'], lst2))
#                 testempno=list(map(lambda d: d['designation_code'], lst2))
#                 testdesig=list(map(lambda d: d['designation'], lst2))
#                 lstdict.append({"desig":"All GM's/ZR","designation_code":list(interkey)})

#         elif i['d_level'] == 'BM':
#             lst1=models.Level_Desig.objects.filter(d_level=i['d_level']).exclude(designation_code__in=testempno).count()
#             if lst1 == 0:
#                 lst2=list(models.Level_Desig.objects.filter(designation_code__in=testempno).exclude(d_level=i['d_level']).values('designation_code','designation').order_by('designation'))
#                 if testmarkofficer != '':
#                     testmarkofficer+=','
#                 testmarkofficer=testmarkofficer+"All Board Member's"
#                 interkey=set(testempno)-set(map(lambda d: d['designation_code'], lst2))
#                 testempno=list(map(lambda d: d['designation_code'], lst2))
#                 testdesig=list(map(lambda d: d['designation'], lst2))
#                 lstdict.append({"desig":"All Board Member's","designation_code":list(interkey)})


#         elif i['d_level'] == 'PHOD':
#             lst1=models.Level_Desig.objects.filter(d_level=i['d_level']).exclude(designation_code__in=testempno).count()
#             if lst1 == 0:
#                 lst2=list(models.Level_Desig.objects.filter(designation_code__in=testempno).exclude(d_level=i['d_level']).values('designation_code','designation').order_by('designation'))
#                 if testmarkofficer != '':
#                     testmarkofficer+=','
#                 testmarkofficer=testmarkofficer+"All PHOD's"
#                 interkey=set(testempno)-set(map(lambda d: d['designation_code'], lst2))
#                 testempno=list(map(lambda d: d['designation_code'], lst2))
#                 testdesig=list(map(lambda d: d['designation'], lst2))
#                 lstdict.append({"desig":"All PHOD's","designation_code":list(interkey)})
#             else:
#                 hq=models.railwayLocationMaster.objects.filter(parent_location_code__isnull=False).values('parent_location_code').distinct()
#                 for ii in hq:
#                     rlyunit=models.railwayLocationMaster.objects.filter(parent_location_code=ii['parent_location_code']).values('rly_unit_code')
#                     if models.Level_Desig.objects.filter(d_level=i['d_level'],rly_unit__in=rlyunit).exists():
#                         lst3=models.Level_Desig.objects.filter(d_level=i['d_level'],rly_unit__in=rlyunit).exclude(designation_code__in=testempno).count()
#                         if lst3 == 0:
#                             lst2=list(models.Level_Desig.objects.filter(designation_code__in=testempno).exclude(d_level=i['d_level'],rly_unit__in=rlyunit).values('designation_code','designation').order_by('designation'))
#                             if testmarkofficer != '':
#                                 testmarkofficer+=','
#                             testmarkofficer=testmarkofficer+"All PHOD's"+ii['parent_location_code']
#                             interkey=set(testempno)-set(map(lambda d: d['designation_code'], lst2))
#                             testempno=list(map(lambda d: d['designation_code'], lst2))
#                             testdesig=list(map(lambda d: d['designation'], lst2))
#                             lstdict.append({"desig":"All PHOD's/"+ii['parent_location_code'],"designation_code":list(interkey)})



#         elif i['d_level'] == 'DRM':
#             lst1=models.Level_Desig.objects.filter(d_level=i['d_level']).exclude(designation_code__in=testempno).count()
#             if lst1 == 0:
#                 lst2=list(models.Level_Desig.objects.filter(designation_code__in=testempno).exclude(d_level=i['d_level']).values('designation_code','designation').order_by('designation'))
#                 if testmarkofficer != '':
#                     testmarkofficer+=','
#                 testmarkofficer=testmarkofficer+"All DRM's"
#                 interkey=set(testempno)-set(map(lambda d: d['designation_code'], lst2))
#                 testempno=list(map(lambda d: d['designation_code'], lst2))
#                 testdesig=list(map(lambda d: d['designation'], lst2))
#                 lstdict.append({"desig":"All DRM's","designation_code":list(interkey)})
#             else:
#                 hq=models.railwayLocationMaster.objects.filter(parent_location_code__isnull=False).values('parent_location_code').distinct()
#                 for ii in hq:
#                     rlyunit=models.railwayLocationMaster.objects.filter(parent_location_code=ii['parent_location_code']).values('rly_unit_code')
#                     if models.Level_Desig.objects.filter(d_level=i['d_level'],rly_unit__in=rlyunit).exists():
#                         lst3=models.Level_Desig.objects.filter(d_level=i['d_level'],rly_unit__in=rlyunit).exclude(designation_code__in=testempno).count()
#                         if lst3 == 0:
#                             lst2=list(models.Level_Desig.objects.filter(designation_code__in=testempno).exclude(d_level=i['d_level'],rly_unit__in=rlyunit).values('designation_code','designation').order_by('designation'))
#                             if testmarkofficer != '':
#                                 testmarkofficer+=','
#                             testmarkofficer=testmarkofficer+"All DRM's/"+ii['parent_location_code']
#                             interkey=set(testempno)-set(map(lambda d: d['designation_code'], lst2))
#                             testempno=list(map(lambda d: d['designation_code'], lst2))
#                             testdesig=list(map(lambda d: d['designation'], lst2))
#                             lstdict.append({"desig":"All DRM's/"+ii['parent_location_code'],"designation_code":list(interkey)})

#     for i in range(len(testdesig)):
#         if testmarkofficer != '':
#             testmarkofficer+=','
#         testmarkofficer=testmarkofficer+testdesig[i]
#         lstdict.append({"desig":testdesig[i],"designation_code":[testempno[i]]})
#     context={'marked_id': json.dumps(officer_id), 'marked_desig': testmarkofficer,'marked_key':json.dumps(lstdict)}
#     return context
  
def rbmins_doneby_list(request):
    try:
        user=request.user.username
        if request.user.user_role == 'guest':
                user=request.user.guest_email
        mom_desig=models.Level_Desig.objects.exclude(official_email_ID = None).filter(Q(official_email_ID=user) | Q(official_email_ID=request.user))
        context={}
        if m3.Insp_details.objects.filter(type=0).exists():
            mom_data=m3.Insp_details.objects.filter(mom_officer_id=mom_desig[0].designation_code,type=0, status_flag__in=[1,2,3,4]).values().distinct().order_by('-insp_no')
            # #print(mom_data,'mom_data')
            # exclude(status_flag=1,status='R')
            list_mom_details=[]
            for i in mom_data:
                temp={}
                if(m3.Marked_Members.objects.filter(item_no__insp_no_id=i['insp_no']).exists()):
                    temp['insp']=i['insp_no']
                    temp['total_status']=m3.Marked_Members.objects.filter(item_no__insp_no_id=i['insp_no']).count()
                    temp['reply_status']=m3.Marked_Members.objects.filter(item_no__insp_no_id=i['insp_no'],status_flag=3).count()
                else:
                    temp['insp']=i['insp_no']
                    temp['total_status']=int(0)
                    temp['reply_status']=int(0)
                list_mom_details.append(temp)
            meeting=''
            context={'mom_data':mom_data,'str':'RB','meeting':meeting,'list_mom_details':list_mom_details}
            return render(request,"mom_doneby_list1.html",context)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="mom_doneby_list1",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "mom_errors.html", {})

def rbmins_draft_doneby_list(request):
    user=request.user.username
    if request.user.user_role == 'guest':
                user=request.user.guest_email
    mom_desig=models.Level_Desig.objects.exclude(official_email_ID = None).filter(Q(official_email_ID=user) | Q(official_email_ID=request.user))
    context={}
    if m3.Insp_details.objects.filter(type=0).exists() and (mom_desig[0].d_level=='CRB' or mom_desig[0].d_level=='BM' or mom_desig[0].d_level=='Secy_RB'):
        mom_data=m3.Insp_details.objects.filter(mom_officer_id=mom_desig[0].designation_code,status_flag=0, type=0).values().distinct().order_by('-insp_no')
        list_mom_details=[]
        for i in mom_data:
            temp={}
            if(m3.Marked_Members.objects.filter(item_no__insp_no_id=i['insp_no']).exists()):
                temp['insp']=i['insp_no']
                temp['total_status']=m3.Marked_Members.objects.filter(item_no__insp_no_id=i['insp_no']).count()
                temp['reply_status']=m3.Marked_Members.objects.filter(item_no__insp_no_id=i['insp_no'],status_flag=3).count()
            else:
                temp['insp']=i['insp_no']
                temp['total_status']=int(0)
                temp['reply_status']=int(0)
            list_mom_details.append(temp)
        meeting=''
        context={'mom_data':mom_data,'str':'RB','meeting':meeting,'list_mom_details':list_mom_details, 'types':'rb_minutes'}
        return render(request , 'draft_mom_doneby_list.html', context)



import base64 
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad

def encryptWithAes(data):
    key = 'AAAAAAAAAAAAAAAA'
    iv =  'BBBBBBBBBBBBBBBB'.encode('utf-8')
    data= pad(data.encode(),16)
    cipher = AES.new(key.encode('utf-8'),AES.MODE_CBC,iv)
    encrypted = base64.b64encode(cipher.encrypt(data))
    return encrypted.decode("utf-8", "ignore")


def decryptWithAes(enc):
    key = 'AAAAAAAAAAAAAAAA'
    iv =  'BBBBBBBBBBBBBBBB'.encode('utf-8')
    enc = base64.b64decode(enc)
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(enc),16)
    return decrypted.decode("utf-8", "ignore")


def officertask_mom(request):
    desigs=json.loads(request.POST.get('desigs'))
    id=request.POST.get('id')
    designations=list(models.Level_Desig.objects.filter(designation_code__in=desigs).values('designation','designation_code').order_by('designation'))
    context={
      'designations':designations,  
      'id':id,
    }
    return JsonResponse(context,safe=False)

def create_rbmom(request):
    # try:
        

        user=request.user.username 
        if request.user.user_role == 'guest':
                user=request.user.guest_email
        desig_details=models.Level_Desig.objects.exclude(official_email_ID=None).filter(Q(official_email_ID=request.user)| Q(official_email_ID=request.user.guest_email) | Q(official_email_ID=request.user.email)).values()
        div_code = list(models.railwayLocationMaster.objects.filter(rly_unit_code=desig_details[0]['rly_unit_id']).values_list('parent_rly_unit_code', flat=True))
        Zone11=models.Level_Desig.objects.filter(Q(official_email_ID=request.user)| Q(official_email_ID=request.user.guest_email) | Q(official_email_ID=request.user.email)).values('rly_unit')[0]['rly_unit']

        officer_prsnt=models.Level_Desig.objects.filter().values('designation','designation_code').order_by('designation')
        dealt_officer=models.Level_Desig.objects.exclude(designation_code=desig_details[0]['designation_code']).filter(Q(rly_unit_id__in=div_code)| (Q(rly_unit_id=desig_details[0]['rly_unit_id'])) |Q(rly_unit_id__parent_rly_unit_code__in=div_code )| Q(rly_unit_id__parent_rly_unit_code = desig_details[0]['rly_unit_id']),delete_flag=False).values('designation','designation_code').order_by('designation')
        officer_copy=models.Level_Desig.objects.exclude(designation_code=desig_details[0]['designation_code']).filter().values('designation','designation_code').order_by('designation')
        meeting=list(m3.meeting_typelist.objects.filter(default_flag=1).values('meeting_type').distinct().order_by('meeting_type'))
        meetings=(list(m3.meeting_typelist.objects.filter(default_flag=0,added_by=desig_details[0]['designation_code']).values('meeting_type').distinct().order_by('meeting_type')))
        for m in meetings:
            meeting.append({'meeting_type': m['meeting_type']})

        list1=models.railwayLocationMaster.objects.filter(location_type_desc__in=['RAILWAY BOARD', 'PRODUCTION UNIT', 'HEAD QUATER','OFFICE', 'PSU', 'PRODUCTION UNIT', 'INSTITUTE']).values('location_code').order_by('location_code')
        list2=[]
        for i in list1:
            list2.append(i['location_code'])
        list3=models.railwayLocationMaster.objects.filter(location_type_desc__in=['DIVISION','WORKSHOP']).values('location_code', 'location_type').order_by('location_code')
        list4=[]
        list5 =[]
        for i in list3:
            list4.append({'location_code':i['location_code'],'location_type':i['location_type']}) 
        try:
            
            list5=list(models.Level_Desig.objects.all().values('designation','designation_code'))  
        except Exception as e:
            pass  
        list6=models.departMast.objects.all().values('department_name').order_by('department_name')
        alldesig=models.Level_Desig.objects.values('designation').distinct().order_by('designation')

        str1='NoRB'
        if str1=='NoRB':

            officer_prsnt=[]
            zone=desig_details[0]['rly_unit_id']
            l_id=list(models.railwayLocationMaster.objects.filter(Q(rly_unit_code=zone)).values('rly_unit_code','location_code'))
            if len(l_id)>0:
                desg=list(models.Level_Desig.objects.filter(designation__isnull=False,rly_unit=l_id[0]['rly_unit_code']).exclude(designation_code=desig_details[0]['designation_code']).values('designation','empno', 'designation_code').order_by('designation'))
                if len(desg)>0:
                    if desg not in officer_prsnt:
                         officer_prsnt.extend(desg)


            l_id=list(models.railwayLocationMaster.objects.filter(Q(parent_location_code=l_id[0]['location_code'])).values('rly_unit_code'))
            if len(l_id)>0:
                for x in range(len(l_id)):
                    desg=list(models.Level_Desig.objects.filter(designation__isnull=False,rly_unit=l_id[x]['rly_unit_code']).exclude(designation_code=desig_details[0]['designation_code']).values('designation','empno', 'designation_code').order_by('designation'))
                    if len(desg)>0:
                        if desg[0] not in officer_prsnt:
                                officer_prsnt.extend(desg)
        list_off=[]
        list_dea=[]
        list_cop=[]
        
        for i in officer_prsnt:
            temp={}
            temp['designation']=i['designation']
            temp['designation_code']=i['designation_code']
            list_off.append(temp)
     
        for i in dealt_officer:
            temp={}
            temp['designation']=i['designation']
            temp['designation_code']=i['designation_code']
            list_dea.append(temp)
      
        for i in officer_copy:
            temp={}
            temp['designation']=i['designation']
            temp['designation_code']=i['designation_code']
            list_cop.append(temp)
      
        
        list_mark=json.dumps(list_dea)
        
        mom_insp = request.GET.get('mom_no')


        if mom_insp != None:
            if not m3.Insp_details.objects.filter(status_flag = 0,insp_no=mom_insp).exists():
                return redirect('/create_rbmom')
            officer_copy=models.Level_Desig.objects.exclude(designation_code=desig_details[0]['designation_code']).filter().values('designation','designation_code').order_by('designation')
            mom_data= list(m3.Insp_details.objects.filter(insp_no=mom_insp).values().distinct().order_by('-insp_no'))
            des_no = list(m3.Item_details.objects.filter(insp_no=mom_insp).values_list('des_id', flat=True))
            mem_desig = m3.Insp_members.objects.filter(insp_no=mom_insp).values('member_desig__designation','other_members')
            mem=[]
            mems=[]
            for m in mem_desig:
                if m['member_desig__designation']:
                    mem.append(m['member_desig__designation'])
                else:
                    if {'designation':m['other_members']} not in mems:
                        mems.append({'designation':m['other_members']}) 
            
            mem_desig = list(mem)
            
            item_data = m3.Item_details.objects.filter(insp_no=mom_insp).values().order_by('item_no')

            length = 0
            head_length = m3.Item_details.objects.filter(insp_no=mom_insp, type="H").values()
            length += head_length.count()

            sh = []
            sh_1 = []
            dlis = []

            new_mail_desig_code=[]
            new_mail_desig_code = list(m6.copyto_mails.objects.filter(doc_id=mom_insp, doc_table='m', area_flag=0).values('receiver_id'))
            
            if new_mail_desig_code:
                new_mail_desig_code=new_mail_desig_code[0]['receiver_id']
                new_mail_desig_code = new_mail_desig_code.split(',')
            else:
                new_mail_desig_code=[]
            

            if new_mail_desig_code!=[]:
                copysss=[]
                for c in new_mail_desig_code :
                    if c!='':
                        copysss.append(c)
                        # lvl=list(models.Level_Desig.objects.filter(designation=c).values('designation_code'))[0]['designation_code']
                        # copysss.append({'designation':c,'designation_code':lvl})
                new_mail_desig_code=copysss
            
            desg_no=list(models.Level_Desig.objects.filter(designation__isnull=False).values('designation','empno', 'designation_code').order_by('designation'))
            for i in range(len(desg_no)):
                    if '/' in desg_no[i]['designation']:
                        r_des=desg_no[i]['designation'].replace('/',' ')
                    elif '.' in desg_no[i]['designation']:
                        r_des=desg_no[i]['designation'].replace('.',' ')
                    else:
                        r_des=desg_no[i]['designation']
                    desg_no[i].update({'empnoser':r_des,'designation_code1':str(desg_no[i]['designation_code'])})

            for i in range(len(list_cop)):
                    if '/' in list_cop[i]['designation']:
                        r_des=list_cop[i]['designation'].replace('/',' ')
                    elif '.' in list_cop[i]['designation']:
                        r_des=list_cop[i]['designation'].replace('.',' ')
                    else:
                        r_des=list_cop[i]['designation']
                    list_cop[i].update({'empnoser':r_des,'designation_code1':str(list_cop[i]['designation_code'])})


            for x in range(len(head_length)):
                mid= str(x+1)+'.'
                itmdata = m3.Item_details.objects.filter(insp_no=mom_insp, type="SH", des_id__startswith=mid).values()
                sh.append(len(itmdata))
                for y in range(len(itmdata)):
                    nid= str(x+1)+'.'+ str(y+1)+'.'
                    itmdata1 = m3.Item_details.objects.filter(insp_no=mom_insp, type="D", des_id__startswith=nid).count()
                    
                    sh_1.append(itmdata1)
                    dlis.append(0)



            
            detailsdata = list(m3.Item_details.objects.filter(insp_no=mom_insp).values().order_by('slno'))
            for i in range(len(detailsdata)):
                created_on =  detailsdata[i]['created_on'].strftime('%Y-%m-%d') if  detailsdata[i]['created_on'] is not None else ''
                updated_on =  detailsdata[i]['updated_on'].strftime('%Y-%m-%d') if  detailsdata[i]['updated_on'] is not None else ''
                target_date = detailsdata[i]['target_date'].strftime('%d/%m/%y') if  detailsdata[i]['target_date'] is not None else ''
                item_priority = detailsdata[i]['item_priority'] if detailsdata[i]['item_priority'] is not None else '0'
                if detailsdata[i]['remarks'] is not None:
                    remarks = detailsdata[i]['remarks'] if len(detailsdata[i]['remarks']) != 0 else None
                else:
                    remarks = None
                detailsdata[i].update({'remarks':remarks,'created_on':created_on,'updated_on':updated_on,'target_date':target_date,'item_priority':item_priority})
                Marked_MembersData = list(m3.Marked_Members.objects.filter(item_no=detailsdata[i]['item_no']).values('marked_to_id','priority','target_date','marked_to_id__designation','action_type'))
                
                marked_key = []
                marked_desig = ''
                marked_id = '[]'
                custom_info = []
                d_id = []
                d_id_str = []
                for j in Marked_MembersData:
                    d_id.append(j['marked_to_id'])
                    d_id_str.append(str(j['marked_to_id']))
                    action_type = 'action'
                    if j['action_type'] == 1:
                        action_type ='info'
                    custom_info.append({'DesignationCode':j['marked_to_id'],'selected_action':action_type,  'priority':0,  'tddate':'','Designation':j['marked_to_id__designation']}) 
                    
                returnData = desig_changecode_office(d_id)
                _tbl_tbl = []
                if detailsdata[i]['table_data'] != '[]':
                        res = eval(detailsdata[i]['table_data'])
                        for k1 in range(len(res)):
                            d2 = []
                            for k2 in range(len(res[k1])):
                                d2.append(res[k1][k2])
                            _tbl_tbl.append(d2)
                else:
                    _tbl_tbl = []
                detailsdata[i].update({'_tbl_tbl':_tbl_tbl,'d_id_str':d_id_str,'custom_info':json.dumps(custom_info), 'marked_key':returnData.get('marked_key'),'marked_desig':returnData.get('marked_desig'),'marked_id':returnData.get('marked_id')})
            
            returnData = []
            if len(new_mail_desig_code)>0:
                returnData = desig_changecode_office(new_mail_desig_code)
            detailsdata = encryptWithAesEinspect(json.dumps(detailsdata))

            item_details_img= list(m3.Item_details.objects.filter(insp_no=mom_insp,link_image__isnull=False).values('link_image','des_id').order_by('slno'))
            img_path = []
            for i5 in range(len(item_details_img)):
                img = item_details_img[i5]['link_image'].split('@#@')
                id = item_details_img[i5]['des_id']
                for i6 in range(len(img)):
                    img_path.append({'id':id,'path':img[i6]})
            

            insp_ofc_name = mom_data[0]['officer_name'] if mom_data[0]['officer_name'] != None else ''
            station_name = mom_data[0]['station_name'] if mom_data[0]['station_name'] != None else ''
            insp_desig = mom_data[0]['officer_desig'] if mom_data[0]['officer_desig'] != None else ''
            context={
                'returnData':json.dumps(returnData),
                'officer':list_off,
                'dealt':list_mark,
                'copy':list_dea,
                'copy1':list_cop,
                'type':type,
                'str': str1,
                'meeting':meeting,
                'mom_data':mom_data,
                'mem_desig': mem_desig,
                'mems':mems,
                'item_data': item_data,
                'list_dea': list_dea,
                'des_no': json.dumps(des_no),
                'head_length': length,
                'sh_list': json.dumps(sh),
                'd_list': json.dumps(dlis),
                'mom_insp': mom_insp,
                'copy_to':list_cop,
                'sh_1':sh_1,
                'officer_copy':officer_copy,
                'option_val':'edit',
                'desg_no':desg_no,
              
               
                'mom_no':mom_insp,
                
                'new_mail_desig_code': new_mail_desig_code,
                'Zone':list2 ,
                'division':list4,
                'marked_to':list5,
                'department':list6,
                'alldesig':alldesig,
                'Zone11':Zone11,
                'detailsdata':json.dumps(detailsdata),
                'img_path':json.dumps(img_path),
                'officer_desig':desig_details[0]['designation'],
                'insp_ofc_name':insp_ofc_name,
                'station_name':station_name,
                'insp_desig':insp_desig,
            }
            
            return render(request, 'create_rbmom.html', context)
        else:
            empdata = models.Level_Desig.objects.exclude(delete_flag=True).filter(official_email_ID=request.user).values('designation', 'station_name','empno','empno__empname','empno__empmname','empno__emplname')
            insp_ofc_name=''
            if empdata:
                employee_fname =empdata[0]['empno__empname']
                if employee_fname:
                    insp_ofc_name = employee_fname + " "


                employee_mname = empdata[0]['empno__empmname']
                if employee_mname:
                    insp_ofc_name += employee_mname + " "


                employee_lname = empdata[0]['empno__emplname']
                if employee_lname:
                    insp_ofc_name += employee_lname
            else:
                insp_ofc_name = 'NA'


            
            if empdata:
                desig_longdesc = empdata[0]['designation']
                station_name = empdata[0]['station_name']
            else:
                desig_longdesc ='NA'
                station_name='NA'
            insp_desig=desig_longdesc
            context={
                'insp_ofc_name':insp_ofc_name,
                'station_name':station_name,
                'insp_desig':insp_desig,

                'officer':list_off,
                'dealt':list_mark,
                'copy':list_dea,
                'copy_to':list_cop,
                'type':type,
                'str':str1,
                'meeting':meeting,
                'Zone':list2 ,
                'division':list4,
                'marked_to':list5,
                'department':list6,
                'alldesig':alldesig,
                'Zone11':Zone11,
                
            }
            
            return render(request,"create_rbmom.html",context)
    # except Exception as e: 
    #     try:
    #         m1.error_Table.objects.create(fun_name="showDet",user_id=request.user,err_details=str(e))
    #     except:
    #         print("Internal Error!!!")
    #     return render(request, "mom_errors.html", {})


def desig_changecode_office(testempno):
            desig=[]
            for i in range(len(testempno)):
                xx=models.Level_Desig.objects.exclude(delete_flag=True).filter(designation_code=testempno[i]).values('designation', ).distinct('designation')
                if len(xx)>0:
                    desig.append(xx[0]['designation'])
            testdesig = desig
            officer_id=testempno
            testmarkofficer=''
            lstdict=[]
            
            alldesig = models.Level_Desig.objects.exclude(delete_flag=True).filter(designation_code__in=testempno).values('d_level').distinct('d_level')
            
            for i in alldesig:
                if i['d_level'] == 'GM':
                    lst1=models.Level_Desig.objects.exclude(delete_flag=True).filter(d_level=i['d_level']).exclude(designation_code__in=testempno).count()
                    if lst1 == 0:
                        lst2=list(models.Level_Desig.objects.exclude(delete_flag=True).filter(designation_code__in=testempno).exclude(d_level=i['d_level']).values('designation_code','designation').order_by('designation'))
                        if testmarkofficer != '':
                            testmarkofficer+=','
                        testmarkofficer=testmarkofficer+"All GM's/ZR"
                        interkey=set(testempno)-set(map(lambda d: d['designation_code'], lst2))
                        testempno=list(map(lambda d: d['designation_code'], lst2))
                        testdesig=list(map(lambda d: d['designation'], lst2))
                        lstdict.append({"desig":"All GM's/ZR","designation_code":list(interkey)})

                elif i['d_level'] == 'BM':
                    lst1=models.Level_Desig.objects.exclude(delete_flag=True).filter(d_level=i['d_level']).exclude(designation_code__in=testempno).count()
                    if lst1 == 0:
                        lst2=list(models.Level_Desig.objects.exclude(delete_flag=True).filter(designation_code__in=testempno).exclude(d_level=i['d_level']).values('designation_code','designation').order_by('designation'))
                        if testmarkofficer != '':
                            testmarkofficer+=','
                        testmarkofficer=testmarkofficer+"All Board Member's"
                        interkey=set(testempno)-set(map(lambda d: d['designation_code'], lst2))
                        testempno=list(map(lambda d: d['designation_code'], lst2))
                        testdesig=list(map(lambda d: d['designation'], lst2))
                        lstdict.append({"desig":"All Board Member's","designation_code":list(interkey)})


                elif i['d_level'] == 'PHOD':
                    lst1=models.Level_Desig.objects.exclude(delete_flag=True).filter(d_level=i['d_level']).exclude(designation_code__in=testempno).count()
                    if lst1 == 0:
                        lst2=list(models.Level_Desig.objects.exclude(delete_flag=True).filter(designation_code__in=testempno).exclude(d_level=i['d_level']).values('designation_code','designation').order_by('designation'))
                        if testmarkofficer != '':
                            testmarkofficer+=','
                        testmarkofficer=testmarkofficer+"All PHOD's"
                        interkey=set(testempno)-set(map(lambda d: d['designation_code'], lst2))
                        testempno=list(map(lambda d: d['designation_code'], lst2))
                        testdesig=list(map(lambda d: d['designation'], lst2))
                        lstdict.append({"desig":"All PHOD's","designation_code":list(interkey)})
                    else:
                        hq=models.railwayLocationMaster.objects.filter(parent_location_code__isnull=False).values('parent_location_code').distinct()
                        for ii in hq:
                            rlyunit=models.railwayLocationMaster.objects.filter(location_code=ii['parent_location_code']).values('rly_unit_code')
                            if models.Level_Desig.objects.exclude(delete_flag=True).filter(d_level=i['d_level'],rly_unit__in=rlyunit).exists():
                                lst3=models.Level_Desig.objects.exclude(delete_flag=True).filter(d_level=i['d_level'],rly_unit__in=rlyunit).exclude(designation_code__in=testempno).count()
                                if lst3 == 0:
                                    lst2=list(models.Level_Desig.objects.exclude(delete_flag=True).filter(designation_code__in=testempno).exclude(d_level=i['d_level'],rly_unit__in=rlyunit).values('designation_code','designation').order_by('designation'))
                                    if testmarkofficer != '':
                                        testmarkofficer+=','
                                    testmarkofficer=testmarkofficer+"All PHOD's"+ii['parent_location_code']
                                    interkey=set(testempno)-set(map(lambda d: d['designation_code'], lst2))
                                    testempno=list(map(lambda d: d['designation_code'], lst2))
                                    testdesig=list(map(lambda d: d['designation'], lst2))
                                    lstdict.append({"desig":"All PHOD's/"+ii['parent_location_code'],"designation_code":list(interkey)})



                elif i['d_level'] == 'DRM':
                    lst1=models.Level_Desig.objects.exclude(delete_flag=True).filter(d_level=i['d_level']).exclude(designation_code__in=testempno).count()
                    if lst1 == 0:
                        lst2=list(models.Level_Desig.objects.exclude(delete_flag=True).filter(designation_code__in=testempno).exclude(d_level=i['d_level']).values('designation_code','designation').order_by('designation'))
                        if testmarkofficer != '':
                            testmarkofficer+=','
                        testmarkofficer=testmarkofficer+"All DRM's"
                        interkey=set(testempno)-set(map(lambda d: d['designation_code'], lst2))
                        testempno=list(map(lambda d: d['designation_code'], lst2))
                        testdesig=list(map(lambda d: d['designation'], lst2))
                        lstdict.append({"desig":"All DRM's","designation_code":list(interkey)})
                    else:
                        hq=models.railwayLocationMaster.objects.filter(parent_location_code__isnull=False).values('parent_location_code').distinct()
                        for ii in hq:
                            rlyunit=models.railwayLocationMaster.objects.filter(parent_location_code=ii['parent_location_code']).values('rly_unit_code')
                            if models.Level_Desig.objects.exclude(delete_flag=True).filter(d_level=i['d_level'],rly_unit__in=rlyunit).exists():
                                lst3=models.Level_Desig.objects.exclude(delete_flag=True).filter(d_level=i['d_level'],rly_unit__in=rlyunit).exclude(designation_code__in=testempno).count()
                                if lst3 == 0:
                                    lst2=list(models.Level_Desig.objects.exclude(delete_flag=True).filter(designation_code__in=testempno).exclude(d_level=i['d_level'],rly_unit__in=rlyunit).values('designation_code','designation').order_by('designation'))
                                    if testmarkofficer != '':
                                        testmarkofficer+=','
                                    testmarkofficer=testmarkofficer+"All DRM's/"+ii['parent_location_code']
                                    interkey=set(testempno)-set(map(lambda d: d['designation_code'], lst2))
                                    testempno=list(map(lambda d: d['designation_code'], lst2))
                                    testdesig=list(map(lambda d: d['designation'], lst2))
                                    lstdict.append({"desig":"All DRM's/"+ii['parent_location_code'],"designation_code":list(interkey)})

            for i in range(len(testdesig)):
                if testmarkofficer != '':
                    testmarkofficer+=','
                testmarkofficer=testmarkofficer+testdesig[i]
                lstdict.append({"desig":testdesig[i],"designation_code":[testempno[i]]})
                
            context={'marked_id': json.dumps(officer_id), 'marked_desig': testmarkofficer,'marked_key':json.dumps(lstdict)}
            return context


# from django.db import transaction
# @transaction.atomic
def draft_rbmom_details(request):
    try:
        if request.method == "POST" and request.is_ajax():
            user=request.user.username
            if request.user.user_role == 'guest':
                user=request.user.guest_email

            inspection_no = request.POST.get('inspection_no')
            final=decryptWithAesEinspect(request.POST.get('final_partinspected'))
            final_id=request.POST.get('id_partinspected')
            type1=request.POST.get('type')
            title=decryptWithAesEinspect(request.POST.get('titleMOM'))
            present=json.loads(request.POST.get('present'))
            copyto=request.POST.get('send_to')
            mdate1=request.POST.get('mdate')
            mdate=datetime.strptime(mdate1, '%d/%m/%Y').strftime('%Y-%m-%d')
            del_array_data = json.loads(request.POST.get('del_array_data'))
            final_img=json.loads(request.POST.get('final_img'))
            
            sttninsp = request.POST.get('sttninsp')
            desiginsp = request.POST.get('desiginsp')
            ofcnameinsp = request.POST.get('ofcnameinsp')
            
            

            designation=models.Level_Desig.objects.filter(Q(official_email_ID=user)|Q(official_email_ID=request.user.email),empno__isnull=False)
            if m3.meeting_typelist.objects.filter(meeting_type=type1).exists():
                pass
            else:
                empnox = models.Level_Desig.objects.filter(Q(official_email_ID=request.user)| Q(official_email_ID=request.user.guest_email) | Q(official_email_ID=request.user.email), empno__isnull=False)
                if empnox:
                    empno = empnox[0].empno_id
                    desig = empnox[0].designation_code
                m3.meeting_typelist.objects.create(meeting_type=type1,default_flag=0, added_by=empnox[0])
          
            if len(designation):
                empno=designation[0].empno_id
            else:
                empno=''
            desig=designation[0].designation
            desig_id=designation[0].designation_code
            level=designation[0].d_level

            finalval = json.loads(final)
            final_allid = json.loads(final_id)
            year = str(datetime.now().year)
            
            
            if level=='CRB' or level=='BM' or level=='Secy_RB':
                title='MINUTES OF MEETING OF THE BOARD HELD ON '+ datetime.strptime(mdate1, '%d/%m/%Y').strftime("%d/%m/%y")
                if inspection_no != '':
                    m3.Insp_details.objects.filter(insp_no = inspection_no).update(station_name=sttninsp,officer_name=ofcnameinsp,officer_desig=desiginsp,updated_on = datetime.now(),mom_officer_id=desig_id,mom_title=title,mom_date=mdate,status_flag=0,type=1,meeting_type=type1)
                else:
                    m3.Insp_details.objects.create(station_name=sttninsp,officer_name=ofcnameinsp,officer_desig=desiginsp,updated_on = datetime.now(),created_on=datetime.now(),created_by=empno,mom_officer_id=desig_id,mom_title=title,mom_date=mdate,status_flag=0,type=1,meeting_type=type1)
           
            else:
                # note_ = year+'/'+desig+'/'
                # last_note1 = m3.Insp_details.objects.filter(mom_note_no__istartswith=note_).aggregate(Max('note_last'))
                # if last_note1['note_last__max'] == None:
                #     last_note1 = 1
                #     note_no = year+'/'+desig+'/'+ str(last_note1)
                # else:
                #     last_note1 = int(last_note1['note_last__max']) +1
                #     note_no = year+'/'+desig+'/'+ str(last_note1)
                if level=='GM' or level=='PHOD' or level=='AGM' or level=='Secy_GM':
                    if inspection_no != '':
                        m3.Insp_details.objects.filter(insp_no = inspection_no).update(station_name=sttninsp,officer_name=ofcnameinsp,officer_desig=desiginsp,updated_on = datetime.now(),mom_officer_id=desig_id,mom_title=title,mom_date=mdate,status_flag=0,type=1,meeting_type=type1)

                    else:
                        m3.Insp_details.objects.create(station_name=sttninsp,officer_name=ofcnameinsp,officer_desig=desiginsp,updated_on = datetime.now(),created_on=datetime.now(),created_by=empno,mom_officer_id=desig_id,mom_title=title,mom_date=mdate,status_flag=0,type=1,meeting_type=type1)
                else:
                    if inspection_no != '':
                        m3.Insp_details.objects.filter(insp_no = inspection_no).update(station_name=sttninsp,officer_name=ofcnameinsp,officer_desig=desiginsp,updated_on = datetime.now(),mom_officer_id=desig_id,mom_title=title,mom_date=mdate,status_flag=0,type=2,meeting_type=type1)
                    else:
                        m3.Insp_details.objects.create(station_name=sttninsp,officer_name=ofcnameinsp,officer_desig=desiginsp,updated_on = datetime.now(),created_on=datetime.now(),created_by=empno,mom_officer_id=desig_id,mom_title=title,mom_date=mdate,status_flag=0,type=2,meeting_type=type1)
           
            # messages.info(request, 'MOM successfully saved')
            if inspection_no != '':
                insp_id = inspection_no
            else:
                insp_id=m3.Insp_details.objects.all().last().insp_no
            allkeyid = [ j for i in final_allid.values() for j in i]
            
            

            # storing item details
            officer_email=[]
            serial_no = 1
            marked_officer_list = []
            for f, b in zip(finalval, final_allid):
                for x,y in zip(finalval[f], final_allid[b]):
                    s = y.split('.')
                    if len(s) == 1:
                        hed = 'heading'+y
                        pr = 'check'+y
                        trz = 'targetdate'+y
                        officm = 'markeofficer'+y
                        remark = 'remarks'+y
                        heading = finalval[f][hed]
                        table_data = 'table'+y
                        action_info = 'myinfo' + y 
                        try:
                            table_data = finalval[f][table_data]
                        except:
                            table_data = '[]'
                        y2=str(y+'.1')
                        if y2 in final_allid[b]:
                            if m3.Item_details.objects.filter(des_id=y, insp_no_id=insp_id).exists():
                                m3.Item_details.objects.filter(des_id=y, insp_no_id=insp_id).update(table_data = table_data,slno = serial_no,updated_on=datetime.now(),item_heading=heading, type='P', status_flag=0)
                                serial_no += 1
                            else:
                                m3.Item_details.objects.create(table_data = table_data,slno = serial_no,updated_on=datetime.now(),item_heading=heading, created_on=datetime.now(), created_by=empno, type='P', des_id=y, insp_no_id=insp_id,status_flag=0)
                                serial_no += 1
                        else:
                            priority = finalval[f][pr]
                            targetd = finalval[f][trz]
                            dealt = finalval[f][officm]
                            remarks = finalval[f][remark]
                            try:
                                action_info = finalval[f][action_info]
                            except:
                                action_info = []
                        
                            if targetd:
                                t_date = datetime.strptime(targetd, '%d/%m/%y').strftime('%Y-%m-%d')
                            else:
                                t_date = None
                            if dealt:
                                dealt=list(dealt.split(','))
                                dealt=list(models.Level_Desig.objects.filter(designation_code__in=dealt).values_list('designation_code',flat=True))
                                
                                if m3.Item_details.objects.filter(des_id=y, insp_no_id=insp_id).exists():
                                    m3.Item_details.objects.filter(des_id=y, insp_no_id=insp_id).update(table_data = table_data, slno = serial_no, item_heading = heading, type='P', item_priority = priority, target_date = t_date, status_flag=0, remarks = remarks)
                                    serial_no += 1
                                    item_id=m3.Item_details.objects.filter(des_id=y, insp_no_id=insp_id).all().last().item_no
                                   
                                
                                else:
                                    m3.Item_details.objects.create(table_data = table_data,slno = serial_no, updated_on=datetime.now(), item_heading=heading, created_on=datetime.now(), created_by=empno, type='P', des_id=y, insp_no_id=insp_id, item_priority=priority, target_date=t_date, status_flag=0, remarks=remarks)
                                    serial_no += 1
                                    item_id=m3.Item_details.objects.all().last().item_no
                                
                                
                                
                                ac_count = 0
                                for i in dealt:
                                    if len(action_info) == 0:
                                        action_type = 0
                                    else:
                                        action_type = action_info[ac_count]
                                        ac_count += 1
                                        if action_type == 'info':
                                            action_type = 1
                                        else:
                                            action_type = 0

                                    Desig_mark=models.Level_Desig.objects.filter(designation_code=i)
                                    email=Desig_mark[0].official_email_ID
                                    officer_email.append(email)
                                    if Desig_mark:
                                        Desig_mark_code=Desig_mark[0].designation_code
                                        if m3.Marked_Members.objects.all().last():
                                            marked_no_id=(m3.Marked_Members.objects.all().last().marked_no)+1
                                        else:
                                            marked_no_id = 1
                                        marked_officer_list.append(int(Desig_mark_code))
                                        if m3.Marked_Members.objects.filter(item_no_id=item_id, marked_to_id=int(Desig_mark_code)).exists():
                                            m3.Marked_Members.objects.filter(item_no_id=item_id, marked_to_id=int(Desig_mark_code)).update(priority = priority, target_date = t_date , action_type = action_type,updated_on = datetime.now(),status_flag=0)
                                        else:
                                            m3.Marked_Members.objects.create(priority = priority, target_date = t_date , action_type = action_type,updated_on = datetime.now(),created_on=datetime.now(),created_by=empno, marked_no=marked_no_id,status_flag=0, item_no_id=item_id,marked_to_id=int(Desig_mark_code))
                                    else:
                                        pass
                                        print('ERROR-HEADING')
                            else:
                                if m3.Item_details.objects.filter(des_id=y, insp_no_id=insp_id).exists():
                                    m3.Item_details.objects.filter(des_id=y, insp_no_id=insp_id).update(table_data = table_data,slno = serial_no, updated_on=datetime.now(), item_heading=heading, type='P', item_priority=priority, target_date=t_date, status_flag=0,remarks=remarks)
                                    serial_no += 1
                                else:
                                    m3.Item_details.objects.create(table_data = table_data,slno = serial_no, updated_on=datetime.now(), item_heading=heading, created_on=datetime.now(), created_by=empno, type='P', des_id=y, insp_no_id=insp_id, item_priority=priority, target_date=t_date, status_flag=0,remarks=remarks)
                                    serial_no += 1
                                    
                
                    elif len(s) == 2:
                        x1=y.split('.')[0]
                        x2=y.split('.')[1]
                        Pitem=x1+x2
                        shed = 'observation'+y
                        shded= 'description'+y
                        pr = 'check'+y
                        trz = 'targetdate'+y
                        officm = 'markeofficer'+y
                        remark='remarks'+y
                        table_data = 'table'+y
                        action_info = 'myinfo' + y
                        try:
                            table_data = finalval[f][table_data]
                        except:
                            table_data = '[]'
                        subheading = finalval[f][shed]
                        description= finalval[f][shded]
                        priority = finalval[f][pr]
                        targetd = finalval[f][trz]
                        dealt = finalval[f][officm]
                        remarks = finalval[f][remark]
                        try:
                            action_info = finalval[f][action_info]
                        except:
                            action_info = []

                        if targetd:
                            t_date = datetime.strptime(targetd, '%d/%m/%y').strftime('%Y-%m-%d')
                        else:
                            t_date = None
                 
                        if description!='':
                            pass
                        else:
                            description=None
                        if dealt:
                            dealt=list(dealt.split(','))
                            dealt=list(models.Level_Desig.objects.filter(designation_code__in=dealt).values_list('designation_code',flat=True))
                            
                            if m3.Item_details.objects.filter(des_id=y, insp_no_id=insp_id).exists():
                                m3.Item_details.objects.filter(des_id=y, insp_no_id=insp_id).update(table_data = table_data,slno = serial_no, updated_on=datetime.now(),item_subheading=subheading, type='SP',item_description=description,item_priority=priority,target_date=t_date, status_flag=0, remarks=remarks)
                                serial_no += 1
                                item_id=m3.Item_details.objects.filter(des_id=y, insp_no_id=insp_id).all().last().item_no
                            else:
                                m3.Item_details.objects.create(table_data = table_data,slno = serial_no, updated_on=datetime.now(),item_subheading=subheading, created_on=datetime.now(), created_by=empno, type='SP', des_id=y, item_description=description,item_priority=priority, insp_no_id=insp_id, target_date=t_date, status_flag=0, remarks=remarks)
                                serial_no += 1
                                item_id=m3.Item_details.objects.all().last().item_no

                                
                            
                            ac_count = 0
                            for i in dealt:
                                if len(action_info) == 0:
                                    action_type = 0
                                else:
                                    action_type = action_info[ac_count]
                                    ac_count += 1
                                    if action_type == 'info':
                                        action_type = 1
                                    else:
                                        action_type = 0

                                Desig_mark=models.Level_Desig.objects.filter(designation_code=i)
                                email=Desig_mark[0].official_email_ID
                                officer_email.append(email)
                                if Desig_mark:
                                    Desig_mark_code=Desig_mark[0].designation_code
                                    if m3.Marked_Members.objects.all().last():
                                        marked_no_id=(m3.Marked_Members.objects.all().last().marked_no)+1
                                    else:
                                        marked_no_id = 1
                                    marked_officer_list.append(int(Desig_mark_code))
                                    if m3.Marked_Members.objects.filter(item_no_id=item_id, marked_to_id=int(Desig_mark_code)).exists():
                                        m3.Marked_Members.objects.filter(item_no_id=item_id, marked_to_id=int(Desig_mark_code)).update(priority = priority, target_date = t_date , action_type = action_type,updated_on = datetime.now(),status_flag=0)
                                    else:
                                        m3.Marked_Members.objects.create(priority = priority, target_date = t_date , action_type = action_type,updated_on = datetime.now(),created_on=datetime.now(),created_by=empno, marked_no=marked_no_id,status_flag=0, item_no_id=item_id,marked_to_id=int(Desig_mark_code))
                                else:
                                    pass
                                    print('ERROR-SUB-HEADING')
                        else:
                            if m3.Item_details.objects.filter(des_id=y, insp_no_id=insp_id).exists():
                                m3.Item_details.objects.filter(des_id=y, insp_no_id=insp_id).update(table_data = table_data,slno = serial_no, updated_on=datetime.now(),item_subheading=subheading, type='SP', item_description=description,item_priority=priority,  target_date=t_date, status_flag=0,remarks=remarks)
                                serial_no += 1
                            else:
                                m3.Item_details.objects.create(table_data = table_data,slno = serial_no, updated_on=datetime.now(),item_subheading=subheading, created_on=datetime.now(), created_by=empno, type='SP', des_id=y, item_description=description,item_priority=priority, insp_no_id=insp_id, target_date=t_date, status_flag=0,remarks=remarks)
                                serial_no += 1
                 
                    else:
                        ded = 'subdes'+y
                        pr = 'check'+y
                        trz = 'targetdate'+y
                        officm = 'markeofficer'+y
                        remark = 'remarks'+y
                        table_data = 'table'+y
                        action_info = 'myinfo' + y
                        try:
                            table_data = finalval[f][table_data]
                        except:
                            table_data = '[]'
                        decision = finalval[f][ded]
                        priority = finalval[f][pr]
                        targetd = finalval[f][trz]
                        dealt = finalval[f][officm]
                        remarks = finalval[f][remark]
                        try:
                            action_info = finalval[f][action_info]
                        except:
                            action_info = []

                        if targetd:
                            t_date = datetime.strptime(targetd, '%d/%m/%y').strftime('%Y-%m-%d')
                        else:
                            t_date = None
                      
                        if dealt:
                            dealt=list(dealt.split(','))
                            dealt=list(models.Level_Desig.objects.filter(designation_code__in=dealt).values_list('designation_code',flat=True))
                            if m3.Item_details.objects.filter(des_id=y, insp_no_id=insp_id).exists():
                                m3.Item_details.objects.filter(des_id=y, insp_no_id=insp_id).update(table_data = table_data,slno = serial_no, updated_on=datetime.now(),item_decision=decision,  type='SSP', item_priority=priority, target_date=t_date, status_flag=0, remarks=remarks)
                                serial_no += 1
                                item_id=m3.Item_details.objects.filter(des_id=y, insp_no_id=insp_id).all().last().item_no
                            else:
                                m3.Item_details.objects.create(table_data = table_data,slno = serial_no, updated_on=datetime.now(),item_decision=decision, created_on=datetime.now(), created_by=empno, type='SSP', des_id=y, insp_no_id=insp_id, item_priority=priority, target_date=t_date, status_flag=0, remarks=remarks)
                                serial_no += 1
                                item_id=m3.Item_details.objects.all().last().item_no
                            
                            ac_count = 0
                            for i in dealt:
                                if len(action_info) == 0:
                                    action_type = 0
                                else:
                                    action_type = action_info[ac_count]
                                    ac_count += 1
                                    if action_type == 'info':
                                        action_type = 1
                                    else:
                                        action_type = 0

                                Desig_mark=models.Level_Desig.objects.filter(designation_code=i)
                                email=Desig_mark[0].official_email_ID
                                officer_email.append(email)
                                if Desig_mark:
                                    Desig_mark_code=Desig_mark[0].designation_code
                                    if m3.Marked_Members.objects.all().last():
                                        marked_no_id=(m3.Marked_Members.objects.all().last().marked_no)+1
                                    else:
                                        marked_no_id = 1
                                    marked_officer_list.append(int(Desig_mark_code))
                                    if m3.Marked_Members.objects.filter(item_no_id=item_id, marked_to_id=int(Desig_mark_code)).exists():
                                        m3.Marked_Members.objects.filter(item_no_id=item_id, marked_to_id=int(Desig_mark_code)).update(priority = priority, target_date = t_date , action_type = action_type,updated_on = datetime.now(),status_flag=0)
                                    else:
                                        m3.Marked_Members.objects.create(priority = priority, target_date = t_date , action_type = action_type,updated_on = datetime.now(),created_on=datetime.now(),created_by=empno, marked_no=marked_no_id,status_flag=0, item_no_id=item_id,marked_to_id=int(Desig_mark_code))
                                else:
                                    pass
                                    print('ERROR-DECISION')
                        else:
                            if m3.Item_details.objects.filter(des_id=y, insp_no_id=insp_id).exists():
                                m3.Item_details.objects.filter(des_id=y, insp_no_id=insp_id).update(table_data = table_data,slno = serial_no, updated_on=datetime.now(),item_decision=decision,type='SSP', status_flag=0)
                                serial_no += 1
                            else:
                                m3.Item_details.objects.create(table_data = table_data,slno = serial_no, updated_on=datetime.now(),item_decision=decision, created_on=datetime.now(), created_by=empno, type='SSP', des_id=y, insp_no_id=insp_id, status_flag=0)
                                serial_no += 1

            m3.Item_details.objects.filter(insp_no_id=insp_id).update(link_image = None)
            for i in range(len(final_img)):
                ref = final_img[i][0]
                path = (final_img[i][1])[1:]
                data = list(m3.Item_details.objects.filter(insp_no_id=insp_id,des_id=ref).values('link_image'))
                if len(data) > 0:
                    data = data[0]['link_image']
                    if data != None:
                        path = data +'@#@'+path
                m3.Item_details.objects.filter(insp_no_id=insp_id,des_id=ref).update(link_image = path)
            
            m3.Marked_Members.objects.filter(~Q(marked_to_id__in = marked_officer_list),item_no_id__in=m3.Item_details.objects.filter(insp_no_id=insp_id).values('item_no')).delete()
            m3.Item_details.objects.filter(~Q(des_id__in=allkeyid),insp_no_id=insp_id).delete()
            
            # storing member details
            present_email=[]  
            present_list = []
            present_list1 = []
            other_list = []
            
            for o in present:
                member_desig=models.Level_Desig.objects.filter(designation=o)
                
                if len(member_desig)!=0:
                    
                    member_desig=models.Level_Desig.objects.filter(designation=o)[0].designation_code
                    email=models.Level_Desig.objects.filter(designation=o)[0].official_email_ID
                    present_email.append(email)
                    present_list.append(member_desig)
                    if not m3.Insp_members.objects.filter(member_desig_id=member_desig,insp_no_id=insp_id).exists():
                        m3.Insp_members.objects.create(member_desig_id=member_desig,insp_no_id=insp_id)
                else:
                    
                    present_list1.append(o)
                    if not m3.Insp_members.objects.filter(other_members=o,insp_no_id=insp_id).exists():
                        m3.Insp_members.objects.create(other_members=o,insp_no_id=insp_id)
            
            m3.Insp_members.objects.filter(~Q(member_desig_id__in=present_list),insp_no_id=insp_id,other_members__isnull = True).delete()
            m3.Insp_members.objects.filter(~Q(other_members__in=present_list1),insp_no_id=insp_id,member_desig_id__isnull = True).delete()
            
            
            copydealt_mail_list = []
            copyto_mails_list = []
           
            if officer_email:
                try:
                    dealt_contact=[]
                    des=''
                    ids=''
                    count_dealt=len(officer_email)
                    countd=1
                    for i in officer_email:
                        a1=models.Level_Desig.objects.filter(official_email_ID=i).values('designation','designation_code','contactnumber')
                        if count_dealt==countd:
                            des+=a1[0]['designation']
                            ids+=str(a1[0]['designation_code'])
                        else:
                            des+=a1[0]['designation']+', '
                            ids+=str(a1[0]['designation_code'])+', '
                        if a1[0]['contactnumber']:
                            dealt_contact.append(a1[0]['contactnumber'])
                    To=officer_email
                    details=m3.Insp_details.objects.filter(insp_no=insp_id).values('mom_title','insp_no','mom_officer__designation','meeting_type','mom_date')
                    subject=details[0]['mom_title']
                    context = {
                        'title': details[0]['mom_title'],
                        'meeting_type': details[0]['meeting_type'],
                        'mom_date': details[0]['mom_date'],
                        'insp_no': details[0]['insp_no'],
                        'mom_officer': details[0]['mom_officer__designation'],
                        'str': 'dealtby'            
                    } 
                    if m3.copydealt_mail.objects.filter(send_to=des,insp_no_id=insp_id,area='DealtBy').exists():
                        copydealt_mail_list.append(des)
                        m3.copydealt_mail.objects.filter(send_to=des,insp_no_id=insp_id,area='DealtBy').update(subject=subject,body=details[0]['mom_title'],area='DealtBy')
                    else:
                        copydealt_mail_list.append(des)
                        m3.copydealt_mail.objects.create(insp_no_id=insp_id,created_on=datetime.now(),created_by=empno,send_to=des,subject=subject,body=details[0]['mom_title'],area='DealtBy')

                    if m6.copyto_mails.objects.filter(doc_id=insp_id,doc_table='m',receiver_id=ids,subject='MOM Report',area_flag=2).exists():
                        copyto_mails_list.append(ids)
                        m6.copyto_mails.objects.filter(doc_id=insp_id,doc_table='m',receiver_id=ids,subject='MOM Report').update(receiver_desig=des, subject='MOM Report', body=details[0]['mom_title'],area_flag=2)
                    else:
                        copyto_mails_list.append(ids)
                        m6.copyto_mails.objects.create(created_on=datetime.now(),sender_id_id=desig_id,doc_id=insp_id,doc_table='m',receiver_id=ids,receiver_desig=des,
                            subject='MOM Report', body=details[0]['mom_title'],area_flag=2)
                     
                except:
                    pass

            
            if copyto:
                try:
                    copy_mail =[]
                    copy_desig=[]
                    copy_contact=[]
                    copy_desig_list=''
                    copy_id_list=''
                    count_copy=len(copyto)
                    countc=1
                    copyto=list(copyto.split(','))
                    for i in copyto:
                        mail_contact=models.Level_Desig.objects.filter(designation_code=i)
                        if count_copy==countc:
                            copy_desig_list+=mail_contact[0].designation
                            copy_id_list+=str(mail_contact[0].designation_code)
                        else:
                            copy_desig_list+=mail_contact[0].designation+','
                            copy_id_list+=str(mail_contact[0].designation_code)+','
                            countc+=1
                        copy_desig.append(mail_contact[0].designation)
                        if mail_contact[0].official_email_ID:
                            copy_mail.append(mail_contact[0].official_email_ID)
                        if mail_contact[0].contactnumber:
                            copy_contact.append(mail_contact[0].contactnumber)
                   
                    To=copy_mail
                    details=m3.Insp_details.objects.filter(insp_no=insp_id).values('mom_title','insp_no','mom_officer__designation','meeting_type','mom_date')
                    subject=details[0]['mom_title']
                    context = {
                        'title': details[0]['mom_title'],
                        'meeting_type': details[0]['meeting_type'],
                        'mom_date': details[0]['mom_date'],
                        'insp_no': details[0]['insp_no'],
                        'mom_officer': details[0]['mom_officer__designation'],
                        'str': 'copyto'          
                    } 
                    if m3.copydealt_mail.objects.filter(send_to=copy_desig_list,insp_no_id=insp_id,area='CopyTo').exists(): 
                        copydealt_mail_list.append(copy_desig_list)
                        m3.copydealt_mail.objects.filter(send_to=copy_desig_list,insp_no_id=insp_id,area='CopyTo').update(subject=subject,body=title,area='CopyTo')
                    else:
                        copydealt_mail_list.append(copy_desig_list)
                        m3.copydealt_mail.objects.create(insp_no_id=insp_id,created_on=datetime.now(),created_by=empno,send_to=copy_desig_list,subject=subject,body=title,area='CopyTo')

                    if m6.copyto_mails.objects.filter(doc_id=insp_id,doc_table='m',receiver_id=copy_id_list,subject='MOM Report',area_flag=0).exists():
                        copyto_mails_list.append(copy_id_list)
                        m6.copyto_mails.objects.filter(doc_id=insp_id,doc_table='m',receiver_id=copy_id_list,subject='MOM Report').update(receiver_desig=copy_desig_list,
                            subject='MOM Report', body=details[0]['mom_title'],area_flag=0)
                    else:
                        copyto_mails_list.append(copy_id_list)
                        m6.copyto_mails.objects.create(created_on=datetime.now(),sender_id_id=desig_id,doc_id=insp_id,doc_table='m',receiver_id=copy_id_list,receiver_desig=copy_desig_list,
                            subject='MOM Report', body=details[0]['mom_title'],area_flag=0)
                   
                except:
                    pass
            
            m3.Item_details.objects.filter(insp_no_id=insp_id).update(del_flag = 0)
            m3.Item_details.objects.filter(des_id__in=del_array_data, insp_no_id=insp_id).update(del_flag = 1)
            m3.copydealt_mail.objects.filter(~Q(send_to__in=copydealt_mail_list),insp_no_id=insp_id,area__in=['CopyTo','DealtBy']).delete()
            m6.copyto_mails.objects.filter(~Q(receiver_id__in=copyto_mails_list),doc_id=insp_id,doc_table='m',subject='MOM Report',area_flag__in=[0,2]).delete()
            return JsonResponse({"status": 1,"note_no":insp_id })
        return JsonResponse({"success":False}, status=400)
    except Exception as e:
        # transaction.set_rollback(True)  # ✅ Correct way to handle rollback inside atomic()
        print(f"Error: {e}")
        raise e 
        try:
            m1.error_Table.objects.create(fun_name="create_mom_details",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "mom_errors.html", {})



import os
# from django.db import transaction
# @transaction.atomic
def create_rbmom_details(request):
    try:
        if request.method == "POST" and request.is_ajax():
            user=request.user.username
            if request.user.user_role == 'guest':
                user=request.user.guest_email

            inspection_no = request.POST.get('inspection_no')
            final=decryptWithAesEinspect(request.POST.get('final_partinspected'))
            final_id=request.POST.get('id_partinspected')
            type1=request.POST.get('type')
            title=decryptWithAesEinspect(request.POST.get('titleMOM'))
            present=json.loads(request.POST.get('present'))
            copyto=request.POST.get('send_to')
            mdate1=request.POST.get('mdate')
            mdate=datetime.strptime(mdate1, '%d/%m/%Y').strftime('%Y-%m-%d')
            del_array_data = json.loads(request.POST.get('del_array_data'))
            final_img=json.loads(request.POST.get('final_img'))

            sttninsp = request.POST.get('sttninsp')
            desiginsp = request.POST.get('desiginsp')
            ofcnameinsp = request.POST.get('ofcnameinsp')
            
            

            designation=models.Level_Desig.objects.filter(Q(official_email_ID=user)|Q(official_email_ID=request.user.email),empno__isnull=False)
            if m3.meeting_typelist.objects.filter(meeting_type=type1).exists():
                pass
            else:
                empnox = models.Level_Desig.objects.filter(Q(official_email_ID=request.user)| Q(official_email_ID=request.user.guest_email) | Q(official_email_ID=request.user.email), empno__isnull=False)
                if empnox:
                    empno = empnox[0].empno_id
                    desig = empnox[0].designation_code
                m3.meeting_typelist.objects.create(meeting_type=type1,default_flag=0, added_by=empnox[0])
          
            if len(designation):
                empno=designation[0].empno_id
            else:
                empno=''
            desig=designation[0].designation
            desig_id=designation[0].designation_code
            level=designation[0].d_level

            finalval = json.loads(final)
            final_allid = json.loads(final_id)
            year = str(datetime.now().year)
            

            if level=='CRB' or level=='BM' or level=='Secy_RB':
                note_ = year+'/'
                last_note1 = m3.Insp_details.objects.filter(mom_note_no__istartswith=note_).aggregate(Max('note_last'))
                if last_note1['note_last__max'] == None:
                    last_note1 = 1
                    note_no = year+'/Secy/Bd. Mtg/'+ str(last_note1)  
                else:
                    last_note1 = int(last_note1['note_last__max']) +1
                    note_no = year+'/Secy/Bd. Mtg/'+ str(last_note1)
                title='MINUTES OF MEETING OF THE BOARD HELD ON '+ datetime.strptime(mdate1, '%d/%m/%Y').strftime("%d/%m/%y")
                
                if inspection_no != '':
                    m3.Insp_details.objects.filter(insp_no = inspection_no).update(station_name=sttninsp,officer_name=ofcnameinsp,officer_desig=desiginsp,note_last = last_note1,mom_note_no=note_no,updated_on = datetime.now(),mom_officer_id=desig_id,mom_title=title,mom_date=mdate,status_flag=1,type=1,meeting_type=type1)
                else:
                    m3.Insp_details.objects.create(station_name=sttninsp,officer_name=ofcnameinsp,officer_desig=desiginsp,note_last = last_note1,mom_note_no=note_no,updated_on = datetime.now(),created_on=datetime.now(),created_by=empno,mom_officer_id=desig_id,mom_title=title,mom_date=mdate,status_flag=1,type=1,meeting_type=type1)
           
            else:
                note_ = year+'/'+desig+'/'
                
                last_note1 = m3.Insp_details.objects.filter(mom_note_no__istartswith=note_).aggregate(Max('note_last'))
                
                if last_note1['note_last__max'] == None:
                    last_note1 = 1
                    note_no = year+'/'+desig+'/'+ str(last_note1)
                else:
                    last_note1 = int(last_note1['note_last__max']) +1
                    note_no = year+'/'+desig+'/'+ str(last_note1)

                if level=='GM' or level=='PHOD' or level=='AGM' or level=='Secy_GM':
                    if inspection_no != '':
                        m3.Insp_details.objects.filter(insp_no = inspection_no).update(station_name=sttninsp,officer_name=ofcnameinsp,officer_desig=desiginsp,note_last = last_note1,mom_note_no=note_no,updated_on = datetime.now(),mom_officer_id=desig_id,mom_title=title,mom_date=mdate,status_flag=1,type=1,meeting_type=type1)

                    else:
                        m3.Insp_details.objects.create(station_name=sttninsp,officer_name=ofcnameinsp,officer_desig=desiginsp,note_last = last_note1,mom_note_no=note_no,updated_on = datetime.now(),created_on=datetime.now(),created_by=empno,mom_officer_id=desig_id,mom_title=title,mom_date=mdate,status_flag=1,type=1,meeting_type=type1)
                else:
                    if inspection_no != '':
                        m3.Insp_details.objects.filter(insp_no = inspection_no).update(station_name=sttninsp,officer_name=ofcnameinsp,officer_desig=desiginsp,updated_on = datetime.now(),mom_officer_id=desig_id,mom_title=title,mom_date=mdate,status_flag=1,type=2,meeting_type=type1,note_last = last_note1,mom_note_no=note_no)
                    else:
                        m3.Insp_details.objects.create(station_name=sttninsp,officer_name=ofcnameinsp,officer_desig=desiginsp,note_last = last_note1,mom_note_no=note_no,updated_on = datetime.now(),created_on=datetime.now(),created_by=empno,mom_officer_id=desig_id,mom_title=title,mom_date=mdate,status_flag=1,type=2,meeting_type=type1)
           
            # messages.info(request, 'MOM successfully saved')
            if inspection_no != '':
                insp_id = inspection_no
            else:
                insp_id=m3.Insp_details.objects.all().last().insp_no
            allkeyid = [ j for i in final_allid.values() for j in i]
            
            

            # storing item details
            officer_email=[]
            serial_no = 1
            marked_officer_list = []
            for f, b in zip(finalval, final_allid):
                for x,y in zip(finalval[f], final_allid[b]):
                    s = y.split('.')
                    if len(s) == 1:
                        hed = 'heading'+y
                        pr = 'check'+y
                        trz = 'targetdate'+y
                        officm = 'markeofficer'+y
                        remark = 'remarks'+y
                        heading = finalval[f][hed]
                        table_data = 'table'+y
                        action_info = 'myinfo' + y 
                        try:
                            table_data = finalval[f][table_data]
                        except:
                            table_data = '[]'
                        y2=str(y+'.1')
                        if y2 in final_allid[b]:
                            if m3.Item_details.objects.filter(des_id=y, insp_no_id=insp_id).exists():
                                m3.Item_details.objects.filter(des_id=y, insp_no_id=insp_id).update(table_data = table_data,slno = serial_no,updated_on=datetime.now(),item_heading=heading, type='P', status_flag=4)
                                serial_no += 1
                            else:
                                m3.Item_details.objects.create(table_data = table_data,slno = serial_no,updated_on=datetime.now(),item_heading=heading, created_on=datetime.now(), created_by=empno, type='P', des_id=y, insp_no_id=insp_id,status_flag=4)
                                serial_no += 1
                        else:
                            priority = finalval[f][pr]
                            targetd = finalval[f][trz]
                            dealt = finalval[f][officm]
                            remarks = finalval[f][remark]
                            try:
                                action_info = finalval[f][action_info]
                            except:
                                action_info = []
                        
                            if targetd:
                                t_date = datetime.strptime(targetd, '%d/%m/%y').strftime('%Y-%m-%d')
                            else:
                                t_date = None
                            if dealt:
                                dealt=list(dealt.split(','))
                                dealt=list(models.Level_Desig.objects.filter(designation_code__in=dealt).values_list('designation_code',flat=True))
                                
                                if m3.Item_details.objects.filter(des_id=y, insp_no_id=insp_id).exists():
                                    m3.Item_details.objects.filter(des_id=y, insp_no_id=insp_id).update(table_data = table_data, slno = serial_no, item_heading = heading, type='P', item_priority = priority, target_date = t_date, status_flag=1, remarks = remarks)
                                    serial_no += 1
                                    item_id=m3.Item_details.objects.filter(des_id=y, insp_no_id=insp_id).all().last().item_no
                                   
                                
                                else:
                                    m3.Item_details.objects.create(table_data = table_data,slno = serial_no, updated_on=datetime.now(), item_heading=heading, created_on=datetime.now(), created_by=empno, type='P', des_id=y, insp_no_id=insp_id, item_priority=priority, target_date=t_date, status_flag=1, remarks=remarks)
                                    serial_no += 1
                                    item_id=m3.Item_details.objects.all().last().item_no
                                
                                
                                
                                ac_count = 0
                                for i in dealt:
                                    if len(action_info) == 0:
                                        action_type = 0
                                    else:
                                        action_type = action_info[ac_count]
                                        ac_count += 1
                                        if action_type == 'info':
                                            action_type = 1
                                        else:
                                            action_type = 0

                                    Desig_mark=models.Level_Desig.objects.filter(designation_code=i)
                                    email=Desig_mark[0].official_email_ID
                                    officer_email.append(email)
                                    if Desig_mark:
                                        Desig_mark_code=Desig_mark[0].designation_code
                                        if m3.Marked_Members.objects.all().last():
                                            marked_no_id=(m3.Marked_Members.objects.all().last().marked_no)+1
                                        else:
                                            marked_no_id = 1
                                        marked_officer_list.append(int(Desig_mark_code))
                                        if m3.Marked_Members.objects.filter(item_no_id=item_id, marked_to_id=int(Desig_mark_code)).exists():
                                            m3.Marked_Members.objects.filter(item_no_id=item_id, marked_to_id=int(Desig_mark_code)).update(priority = priority, target_date = t_date , action_type = action_type,updated_on = datetime.now(),status_flag=1)
                                        else:
                                            m3.Marked_Members.objects.create(priority = priority, target_date = t_date , action_type = action_type,updated_on = datetime.now(),created_on=datetime.now(),created_by=empno, marked_no=marked_no_id,status_flag=1, item_no_id=item_id,marked_to_id=int(Desig_mark_code))
                                    else:
                                        pass
                                        print('ERROR-HEADING')
                            else:
                                if m3.Item_details.objects.filter(des_id=y, insp_no_id=insp_id).exists():
                                    m3.Item_details.objects.filter(des_id=y, insp_no_id=insp_id).update(table_data = table_data,slno = serial_no, updated_on=datetime.now(), item_heading=heading, type='P', item_priority=priority, target_date=t_date, status_flag=4,remarks=remarks)
                                    serial_no += 1
                                else:
                                    m3.Item_details.objects.create(table_data = table_data,slno = serial_no, updated_on=datetime.now(), item_heading=heading, created_on=datetime.now(), created_by=empno, type='P', des_id=y, insp_no_id=insp_id, item_priority=priority, target_date=t_date, status_flag=4,remarks=remarks)
                                    serial_no += 1
                                    
                
                    elif len(s) == 2:
                        x1=y.split('.')[0]
                        x2=y.split('.')[1]
                        Pitem=x1+x2
                        shed = 'observation'+y
                        shded= 'description'+y
                        pr = 'check'+y
                        trz = 'targetdate'+y
                        officm = 'markeofficer'+y
                        remark='remarks'+y
                        table_data = 'table'+y
                        action_info = 'myinfo' + y
                        try:
                            table_data = finalval[f][table_data]
                        except:
                            table_data = '[]'
                        subheading = finalval[f][shed]
                        description= finalval[f][shded]
                        priority = finalval[f][pr]
                        targetd = finalval[f][trz]
                        dealt = finalval[f][officm]
                        remarks = finalval[f][remark]
                        try:
                            action_info = finalval[f][action_info]
                        except:
                            action_info = []

                        if targetd:
                            t_date = datetime.strptime(targetd, '%d/%m/%y').strftime('%Y-%m-%d')
                        else:
                            t_date = None
                 
                        if description!='':
                            pass
                        else:
                            description=None
                        if dealt:
                            dealt=list(dealt.split(','))
                            dealt=list(models.Level_Desig.objects.filter(designation_code__in=dealt).values_list('designation_code',flat=True))
                            
                            if m3.Item_details.objects.filter(des_id=y, insp_no_id=insp_id).exists():
                                m3.Item_details.objects.filter(des_id=y, insp_no_id=insp_id).update(table_data = table_data,slno = serial_no, updated_on=datetime.now(),item_subheading=subheading, type='SP',item_description=description,item_priority=priority,target_date=t_date, status_flag=1, remarks=remarks)
                                serial_no += 1
                                item_id=m3.Item_details.objects.filter(des_id=y, insp_no_id=insp_id).all().last().item_no
                            else:
                                m3.Item_details.objects.create(table_data = table_data,slno = serial_no, updated_on=datetime.now(),item_subheading=subheading, created_on=datetime.now(), created_by=empno, type='SP', des_id=y, item_description=description,item_priority=priority, insp_no_id=insp_id, target_date=t_date, status_flag=1, remarks=remarks)
                                serial_no += 1
                                item_id=m3.Item_details.objects.all().last().item_no

                                
                            
                            ac_count = 0
                            for i in dealt:
                                if len(action_info) == 0:
                                    action_type = 0
                                else:
                                    action_type = action_info[ac_count]
                                    ac_count += 1
                                    if action_type == 'info':
                                        action_type = 1
                                    else:
                                        action_type = 0

                                Desig_mark=models.Level_Desig.objects.filter(designation_code=i)
                                email=Desig_mark[0].official_email_ID
                                officer_email.append(email)
                                if Desig_mark:
                                    Desig_mark_code=Desig_mark[0].designation_code
                                    if m3.Marked_Members.objects.all().last():
                                        marked_no_id=(m3.Marked_Members.objects.all().last().marked_no)+1
                                    else:
                                        marked_no_id = 1
                                    marked_officer_list.append(int(Desig_mark_code))
                                    if m3.Marked_Members.objects.filter(item_no_id=item_id, marked_to_id=int(Desig_mark_code)).exists():
                                        m3.Marked_Members.objects.filter(item_no_id=item_id, marked_to_id=int(Desig_mark_code)).update(priority = priority, target_date = t_date , action_type = action_type,updated_on = datetime.now(),status_flag=1)
                                    else:
                                        m3.Marked_Members.objects.create(priority = priority, target_date = t_date , action_type = action_type,updated_on = datetime.now(),created_on=datetime.now(),created_by=empno, marked_no=marked_no_id,status_flag=1, item_no_id=item_id,marked_to_id=int(Desig_mark_code))
                                else:
                                    pass
                                    print('ERROR-SUB-HEADING')
                        else:
                            if m3.Item_details.objects.filter(des_id=y, insp_no_id=insp_id).exists():
                                m3.Item_details.objects.filter(des_id=y, insp_no_id=insp_id).update(table_data = table_data,slno = serial_no, updated_on=datetime.now(),item_subheading=subheading, type='SP', item_description=description,item_priority=priority,  target_date=t_date, status_flag=4,remarks=remarks)
                                serial_no += 1
                            else:
                                m3.Item_details.objects.create(table_data = table_data,slno = serial_no, updated_on=datetime.now(),item_subheading=subheading, created_on=datetime.now(), created_by=empno, type='SP', des_id=y, item_description=description,item_priority=priority, insp_no_id=insp_id, target_date=t_date, status_flag=4,remarks=remarks)
                                serial_no += 1
                 
                    else:
                        ded = 'subdes'+y
                        pr = 'check'+y
                        trz = 'targetdate'+y
                        officm = 'markeofficer'+y
                        remark = 'remarks'+y
                        table_data = 'table'+y
                        action_info = 'myinfo' + y
                        try:
                            table_data = finalval[f][table_data]
                        except:
                            table_data = '[]'
                        decision = finalval[f][ded]
                        priority = finalval[f][pr]
                        targetd = finalval[f][trz]
                        dealt = finalval[f][officm]
                        remarks = finalval[f][remark]
                        try:
                            action_info = finalval[f][action_info]
                        except:
                            action_info = []

                        if targetd:
                            t_date = datetime.strptime(targetd, '%d/%m/%y').strftime('%Y-%m-%d')
                        else:
                            t_date = None
                      
                        if dealt:
                            dealt=list(dealt.split(','))
                            dealt=list(models.Level_Desig.objects.filter(designation_code__in=dealt).values_list('designation_code',flat=True))
                            if m3.Item_details.objects.filter(des_id=y, insp_no_id=insp_id).exists():
                                m3.Item_details.objects.filter(des_id=y, insp_no_id=insp_id).update(table_data = table_data,slno = serial_no, updated_on=datetime.now(),item_decision=decision,  type='SSP', item_priority=priority, target_date=t_date, status_flag=1, remarks=remarks)
                                serial_no += 1
                                item_id=m3.Item_details.objects.filter(des_id=y, insp_no_id=insp_id).all().last().item_no
                            else:
                                m3.Item_details.objects.create(table_data = table_data,slno = serial_no, updated_on=datetime.now(),item_decision=decision, created_on=datetime.now(), created_by=empno, type='SSP', des_id=y, insp_no_id=insp_id, item_priority=priority, target_date=t_date, status_flag=1, remarks=remarks)
                                serial_no += 1
                                item_id=m3.Item_details.objects.all().last().item_no
                            
                            ac_count = 0
                            for i in dealt:
                                if len(action_info) == 0:
                                    action_type = 0
                                else:
                                    action_type = action_info[ac_count]
                                    ac_count += 1
                                    if action_type == 'info':
                                        action_type = 1
                                    else:
                                        action_type = 0

                                Desig_mark=models.Level_Desig.objects.filter(designation_code=i)
                                email=Desig_mark[0].official_email_ID
                                officer_email.append(email)
                                if Desig_mark:
                                    Desig_mark_code=Desig_mark[0].designation_code
                                    if m3.Marked_Members.objects.all().last():
                                        marked_no_id=(m3.Marked_Members.objects.all().last().marked_no)+1
                                    else:
                                        marked_no_id = 1
                                    marked_officer_list.append(int(Desig_mark_code))
                                    if m3.Marked_Members.objects.filter(item_no_id=item_id, marked_to_id=int(Desig_mark_code)).exists():
                                        m3.Marked_Members.objects.filter(item_no_id=item_id, marked_to_id=int(Desig_mark_code)).update(priority = priority, target_date = t_date , action_type = action_type,updated_on = datetime.now(),status_flag=1)
                                    else:
                                        m3.Marked_Members.objects.create(priority = priority, target_date = t_date , action_type = action_type,updated_on = datetime.now(),created_on=datetime.now(),created_by=empno, marked_no=marked_no_id,status_flag=1, item_no_id=item_id,marked_to_id=int(Desig_mark_code))
                                else:
                                    pass
                                    print('ERROR-DECISION')
                        else:
                            if m3.Item_details.objects.filter(des_id=y, insp_no_id=insp_id).exists():
                                m3.Item_details.objects.filter(des_id=y, insp_no_id=insp_id).update(table_data = table_data,slno = serial_no, updated_on=datetime.now(),item_decision=decision,type='SSP', status_flag=4)
                                serial_no += 1
                            else:
                                m3.Item_details.objects.create(table_data = table_data,slno = serial_no, updated_on=datetime.now(),item_decision=decision, created_on=datetime.now(), created_by=empno, type='SSP', des_id=y, insp_no_id=insp_id, status_flag=4)
                                serial_no += 1

            m3.Item_details.objects.filter(insp_no_id=insp_id).update(link_image = None)
            for i in range(len(final_img)):
                ref = final_img[i][0]
                path = (final_img[i][1])[1:]
                data = list(m3.Item_details.objects.filter(insp_no_id=insp_id,des_id=ref).values('link_image'))
                if len(data) > 0:
                    data = data[0]['link_image']
                    if data != None:
                        path = data +'@#@'+path
                m3.Item_details.objects.filter(insp_no_id=insp_id,des_id=ref).update(link_image = path)
            m3.Marked_Members.objects.filter(~Q(marked_to_id__in = marked_officer_list),item_no_id__in=m3.Item_details.objects.filter(insp_no_id=insp_id).values('item_no')).delete()
            m3.Item_details.objects.filter(~Q(des_id__in=allkeyid),insp_no_id=insp_id).delete()
            
            # storing member details
            present_email=[]  
            present_list = []
            present_list1 = []
            other_list = []
            
            for o in present:
                member_desig=models.Level_Desig.objects.filter(designation=o)
                
                if len(member_desig)!=0:
                    member_desig=models.Level_Desig.objects.filter(designation=o)[0].designation_code
                    email=models.Level_Desig.objects.filter(designation=o)[0].official_email_ID
                    present_email.append(email)
                    present_list.append(member_desig)
                    if not m3.Insp_members.objects.filter(member_desig_id=member_desig,insp_no_id=insp_id).exists():
                        m3.Insp_members.objects.create(member_desig_id=member_desig,insp_no_id=insp_id)
                else:
                    present_list1.append(o)
                    if not m3.Insp_members.objects.filter(other_members=o,insp_no_id=insp_id).exists():
                        m3.Insp_members.objects.create(other_members=o,insp_no_id=insp_id)

            m3.Insp_members.objects.filter(~Q(member_desig_id__in=present_list),insp_no_id=insp_id,other_members__isnull = True).delete()
            m3.Insp_members.objects.filter(~Q(other_members__in=present_list1),insp_no_id=insp_id,member_desig_id__isnull = True).delete()

            
            copydealt_mail_list = []
            copyto_mails_list = []
           
            if officer_email:
                try:
                    dealt_contact=[]
                    des=''
                    ids=''
                    count_dealt=len(officer_email)
                    countd=1
                    for i in officer_email:
                        a1=models.Level_Desig.objects.filter(official_email_ID=i).values('designation','designation_code','contactnumber')
                        if count_dealt==countd:
                            des+=a1[0]['designation']
                            ids+=str(a1[0]['designation_code'])
                        else:
                            des+=a1[0]['designation']+', '
                            ids+=str(a1[0]['designation_code'])+', '
                        if a1[0]['contactnumber']:
                            dealt_contact.append(a1[0]['contactnumber'])
                    To=officer_email
                    details=m3.Insp_details.objects.filter(insp_no=insp_id).values('mom_title','insp_no','mom_officer__designation','meeting_type','mom_date')
                    subject=details[0]['mom_title']
                    context = {
                        'title': details[0]['mom_title'],
                        'meeting_type': details[0]['meeting_type'],
                        'mom_date': details[0]['mom_date'],
                        'insp_no': details[0]['insp_no'],
                        'mom_officer': details[0]['mom_officer__designation'],
                        'str': 'dealtby'            
                    } 
                    if m3.copydealt_mail.objects.filter(send_to=des,insp_no_id=insp_id,area='DealtBy').exists():
                        copydealt_mail_list.append(des)
                        m3.copydealt_mail.objects.filter(send_to=des,insp_no_id=insp_id,area='DealtBy').update(subject=subject,body=details[0]['mom_title'],area='DealtBy')
                    else:
                        copydealt_mail_list.append(des)
                        m3.copydealt_mail.objects.create(insp_no_id=insp_id,created_on=datetime.now(),created_by=empno,send_to=des,subject=subject,body=details[0]['mom_title'],area='DealtBy')

                    if m6.copyto_mails.objects.filter(doc_id=insp_id,doc_table='m',receiver_id=ids,subject='MOM Report',area_flag=2).exists():
                        copyto_mails_list.append(ids)
                        m6.copyto_mails.objects.filter(doc_id=insp_id,doc_table='m',receiver_id=ids,subject='MOM Report').update(receiver_desig=des, subject='MOM Report', body=details[0]['mom_title'],area_flag=2)
                    else:
                        copyto_mails_list.append(ids)
                        m6.copyto_mails.objects.create(created_on=datetime.now(),sender_id_id=desig_id,doc_id=insp_id,doc_table='m',receiver_id=ids,receiver_desig=des,
                            subject='MOM Report', body=details[0]['mom_title'],area_flag=2)
                        # MomSendMail(subject,To,context,details[0]['insp_no'])
                     
                except:
                    pass

            
            if copyto:
                try:
                    copy_mail =[]
                    copy_desig=[]
                    copy_contact=[]
                    copy_desig_list=''
                    copy_id_list=''
                    count_copy=len(copyto)
                    countc=1
                    copyto=list(copyto.split(','))
                    for i in copyto:
                        mail_contact=models.Level_Desig.objects.filter(designation_code=i)
                        if count_copy==countc:
                            copy_desig_list+=mail_contact[0].designation
                            copy_id_list+=str(mail_contact[0].designation_code)
                        else:
                            copy_desig_list+=mail_contact[0].designation+','
                            copy_id_list+=str(mail_contact[0].designation_code)+','
                            countc+=1
                        copy_desig.append(mail_contact[0].designation)
                        if mail_contact[0].official_email_ID:
                            copy_mail.append(mail_contact[0].official_email_ID)
                        if mail_contact[0].contactnumber:
                            copy_contact.append(mail_contact[0].contactnumber)
                   
                    To=copy_mail
                    details=m3.Insp_details.objects.filter(insp_no=insp_id).values('mom_title','insp_no','mom_officer__designation','meeting_type','mom_date')
                    subject=details[0]['mom_title']
                    context = {
                        'title': details[0]['mom_title'],
                        'meeting_type': details[0]['meeting_type'],
                        'mom_date': details[0]['mom_date'],
                        'insp_no': details[0]['insp_no'],
                        'mom_officer': details[0]['mom_officer__designation'],
                        'str': 'copyto'          
                    } 
                    if m3.copydealt_mail.objects.filter(send_to=copy_desig_list,insp_no_id=insp_id,area='CopyTo').exists(): 
                        copydealt_mail_list.append(copy_desig_list)
                        m3.copydealt_mail.objects.filter(send_to=copy_desig_list,insp_no_id=insp_id,area='CopyTo').update(subject=subject,body=title,area='CopyTo')
                    else:
                        copydealt_mail_list.append(copy_desig_list)
                        m3.copydealt_mail.objects.create(insp_no_id=insp_id,created_on=datetime.now(),created_by=empno,send_to=copy_desig_list,subject=subject,body=title,area='CopyTo')

                    if m6.copyto_mails.objects.filter(doc_id=insp_id,doc_table='m',receiver_id=copy_id_list,subject='MOM Report',area_flag=0).exists():
                        copyto_mails_list.append(copy_id_list)
                        m6.copyto_mails.objects.filter(doc_id=insp_id,doc_table='m',receiver_id=copy_id_list,subject='MOM Report').update(receiver_desig=copy_desig_list,
                            subject='MOM Report', body=details[0]['mom_title'],area_flag=0)
                    else:
                        copyto_mails_list.append(copy_id_list)
                        m6.copyto_mails.objects.create(created_on=datetime.now(),sender_id_id=desig_id,doc_id=insp_id,doc_table='m',receiver_id=copy_id_list,receiver_desig=copy_desig_list,
                            subject='MOM Report', body=details[0]['mom_title'],area_flag=0)
                        # MomSendMail(subject,To,context,details[0]['insp_no'])
                   
                except:
                    pass
            
            
            m3.Item_details.objects.filter(insp_no_id=insp_id).update(del_flag = 0)
            m3.copydealt_mail.objects.filter(~Q(send_to__in=copydealt_mail_list),insp_no_id=insp_id,area__in=['CopyTo','DealtBy']).delete()
            m6.copyto_mails.objects.filter(~Q(receiver_id__in=copyto_mails_list),doc_id=insp_id,doc_table='m',subject='MOM Report',area_flag__in=[0,2]).delete()
            return JsonResponse({"status": 1,"note_no":note_no })
        return JsonResponse({"success":False}, status=400)

    except Exception as e:
        try:
            m1.error_Table.objects.create(fun_name="create_mom_details",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "mom_errors.html", {})


# def mom_ReportPdf(request, insp_no):
    
#     insp_details=list(m3.Insp_details.objects.filter(insp_no=insp_no).values())
#     mom_officer_name=m3.Insp_details.objects.filter(insp_no=insp_no).values('mom_officer__designation')[0]['mom_officer__designation']
#     present_list=m3.Insp_members.objects.filter(insp_no=insp_no).values()
#     user=request.user.username
#     if request.user.user_role == 'guest':
#         user=request.user.guest_email
#     login_desig=models.Level_Desig.objects.exclude(official_email_ID = None).filter(Q(official_email_ID=user) | Q(official_email_ID=request.user)).values()
#     item_details= m3.Item_details.objects.filter(insp_no_id=insp_no).values().order_by('item_no')

#     present=[]
#     dealt=[]
#     name=''
    
#     for i in present_list:
        
#         temp={}
#         if i['member_desig_id']!=None:
#             desig=models.Level_Desig.objects.filter(designation_code=i['member_desig_id'])[0].designation
#             if(models.Level_Desig.objects.filter(designation_code=i['member_desig_id'])[0].empno_id):
#                 empno=models.Level_Desig.objects.filter(designation_code=i['member_desig_id'])[0].empno_id
#                 empfname=m1.empmast.objects.filter(empno=empno)[0].empname
#                 empmname=m1.empmast.objects.filter(empno=empno)[0].empmname
#                 emplname=m1.empmast.objects.filter(empno=empno)[0].emplname
#                 if(empmname==None and emplname==None):
#                     name=empfname
#                 elif(empmname==None):
#                     name=empfname + " " + emplname
#                 elif(emplname==None):
#                     name=empfname + " " + empmname   
#                 else:
#                     name=empfname + " " + empmname + " " + emplname
#         else:
#             desig=i['other_members']
#             # desig="NA"
#             name=i['other_members']

#         temp['desig']=desig
#         temp['name']=name
#         temp['status_flag']=i['status_flag']
#         present.append(temp)
    
#     # for i in item_details:
#     #     if insp_details[0]['type']==0:
#     #         # print(i['item_heading'],i['item_subheading'],i['remarks'],i['item_description'],i['item_decision'])
#     #         i['item_heading']=decryptWithAes(i['item_heading']) if i['item_heading']!=None else 'NA'
#     #         i['item_subheading']=decryptWithAes(i['item_subheading']) if i['item_subheading']!=None else 'NA'
#     #         i['remarks']=decryptWithAes(i['remarks']) if m3.Marked_Members.objects.filter(item_no_id=i['item_no']).exists() else 'NA'
#     #         i['item_description']=decryptWithAes(i['item_description']) if i['item_description']!=None else 'NA'
#     #         i['item_decision']=decryptWithAes(i['item_decision']) if i['item_decision']!=None else 'NA'
#     #         # if i['item_heading']!=None:
#     #         #     i['item_heading']=decryptWithAes(i['item_heading'])
#     #         # else:
#     #         #     i['item_heading']='NA'
            
#     #         # if i['item_subheading']!=None:
#     #         #     print("hello",i['item_subheading'])
#     #         #     i['item_subheading']=decryptWithAes(i['item_subheading'])
#     #         # else:
#     #         #     print("not hello")
#     #         #     i['item_subheading']='NA'

#     #         # if i['remarks']!=None:
#     #         #     i['remarks']=decryptWithAes(i['remarks'])
#     #         # else:
#     #         #     i['remarks']='NA'
#     #     else:
#     #         print(i['remarks'])
#     #         i['remarks']=i['remarks'] if i['remarks'] else 'NA'
            
           
#     #     temp={}
#     #     if m3.Marked_Members.objects.filter(item_no_id=i['item_no']).exists():
#     #         # if login_desig[0]['d_level']=='CRB' or login_desig[0]['d_level']=='BM' or login_desig[0]['d_level']=='Secy_RB':
#     #         mark=m3.Marked_Members.objects.filter(item_no_id=i['item_no']).values()
#     #         desig_longdesc1 =''
#     #         count_mark=len(mark)
#     #         countm=1
#     #         for x in mark:
#     #             marked=models.Level_Desig.objects.filter(designation_code=x['marked_to_id'])
#     #             #print('yyyyyyyy', marked[0].designation)
#     #             if  marked[0].designation and count_mark!=countm:
#     #                 desig_longdesc1 += marked[0].designation+', '
#     #                 countm+=1
#     #             else:
#     #                 desig_longdesc1 += marked[0].designation
#     #             #print(desig_longdesc1,'desig_longdesc1')
#     #         temp['dealt']=desig_longdesc1
#     #         temp['item_no']=i['des_id']
#     #     dealt.append(temp)
#     # print(item_details,'dealtdealt')
    

    
#     detailsdata = list(m3.Item_details.objects.filter(insp_no=insp_no).values().order_by('slno'))
    
#     for i in range(len(detailsdata)):
#         created_on =  detailsdata[i]['created_on'].strftime('%Y-%m-%d') if  detailsdata[i]['created_on'] is not None else ''
#         updated_on =  detailsdata[i]['updated_on'].strftime('%Y-%m-%d') if  detailsdata[i]['updated_on'] is not None else ''
#         target_date = detailsdata[i]['target_date'].strftime('%d/%m/%y') if  detailsdata[i]['target_date'] is not None else ''
#         item_priority = detailsdata[i]['item_priority'] if detailsdata[i]['item_priority'] is not None else '0'
#         if detailsdata[i]['remarks'] is not None:
#             remarks = detailsdata[i]['remarks'] if len(detailsdata[i]['remarks']) != 0 else None
#         else:
#             remarks = None
#         link_image  = []
#         if detailsdata[i]['link_image'] is not None:
#             l1 = detailsdata[i]['link_image'].split('@#@')
#             for img1 in l1:
#                 link_image.append(os.path.abspath(img1))
        
        
#         detailsdata[i].update({'remarks':remarks,'created_on':created_on,'updated_on':updated_on,'target_date':target_date,'item_priority':item_priority,'link_image':link_image})
#         Marked_MembersData = list(m3.Marked_Members.objects.filter(item_no=detailsdata[i]['item_no']).values('marked_to_id','priority','target_date','marked_to_id__designation','action_type'))
        
#         marked_key = []
#         marked_desig = ''
#         marked_id = '[]'
#         custom_info = []
#         d_id = []
#         d_id_str = []
#         ac_co = -1
#         in_co = -1
#         for j in Marked_MembersData:
#             d_id.append(j['marked_to_id'])
#             d_id_str.append(str(j['marked_to_id']))
            
#             if j['action_type'] == 0:
#                 action_type ='info'
#                 in_co += 1
#             else:
#                 action_type = 'action'
#                 ac_co += 1
                

                
#             custom_info.append({'selected_action':action_type,'Designation':j['marked_to_id__designation'],'in_co': in_co, 'ac_co':ac_co}) 
#         if len(custom_info) > 0:
#             custom_info = sorted(custom_info , key = lambda x: x['selected_action'])    
#         _tbl_tbl = []
#         if detailsdata[i]['table_data'] != '[]':
#                 res = eval(detailsdata[i]['table_data'])
#                 for k1 in range(len(res)):
#                     d2 = []
#                     for k2 in range(len(res[k1])):
#                         d2.append(res[k1][k2])
#                     _tbl_tbl.append(d2)
#         else:
#             _tbl_tbl = []
#         detailsdata[i].update({'tbl_tbl':_tbl_tbl,'tbllen':len(_tbl_tbl),'custom_info':custom_info})
    
   
    
#     if(m3.copydealt_mail.objects.filter(insp_no=insp_no, area='CopyTo')):
#         copyto = m3.copydealt_mail.objects.filter(insp_no=insp_no, area='CopyTo')[0].send_to
#     else:
#         copyto=''
#     copy_to=[]
#     copy_to = list(m6.copyto_mails.objects.filter(doc_id=insp_no, doc_table='m', area_flag=0).values('receiver_desig'))
#     if len(copy_to):
#         copy_to=copy_to[0]['receiver_desig']
#     if len(copy_to) > 0:
#         copy_to = copy_to.split(',')
#     else:
#         copy_to = []
#     insp_ofc_name = insp_details[0]['officer_name'] if insp_details[0]['officer_name'] != None else ''
#     station_name = insp_details[0]['station_name'] if insp_details[0]['station_name'] != None else ''
#     insp_desig = insp_details[0]['officer_desig'] if insp_details[0]['officer_desig'] != None else ''
#     context={
#         'copyto':copy_to,
#         'insp_details':insp_details,
#         # 'item_details':item_details,
#         'present':present,
#         'dealt':dealt,
#         'detailsdata':detailsdata,
#         'mom_officer_name':mom_officer_name,
#         'insp_ofc_name':insp_ofc_name,
#         'station_name':station_name,  
#         'insp_desig':insp_desig,
#     }
    
#     template_src='mom_ReportPdf.html'
#     return render_to_pdf(template_src, context)

def mom_ReportPdf(request, insp_no):
    
    insp_details=list(m3.Insp_details.objects.filter(insp_no=insp_no).values())
    mom_officer_name=m3.Insp_details.objects.filter(insp_no=insp_no).values('mom_officer__designation')[0]['mom_officer__designation']
    present_list=m3.Insp_members.objects.filter(insp_no=insp_no).values()
    user=request.user.username
    if request.user.user_role == 'guest':
        user=request.user.guest_email
    login_desig=models.Level_Desig.objects.exclude(official_email_ID = None).filter(Q(official_email_ID=user) | Q(official_email_ID=request.user)).values()
    item_details= m3.Item_details.objects.filter(insp_no_id=insp_no).values().order_by('item_no')

    present=[]
    dealt=[]
    name=''
    
    for i in present_list:
        
        temp={}
        if i['member_desig_id']!=None:
            desig=models.Level_Desig.objects.filter(designation_code=i['member_desig_id'])[0].designation
            if(models.Level_Desig.objects.filter(designation_code=i['member_desig_id'])[0].empno_id):
                empno=models.Level_Desig.objects.filter(designation_code=i['member_desig_id'])[0].empno_id
                empfname=m1.empmast.objects.filter(empno=empno)[0].empname
                empmname=m1.empmast.objects.filter(empno=empno)[0].empmname
                emplname=m1.empmast.objects.filter(empno=empno)[0].emplname
                if(empmname==None and emplname==None):
                    name=empfname
                elif(empmname==None):
                    name=empfname + " " + emplname
                elif(emplname==None):
                    name=empfname + " " + empmname   
                else:
                    name=empfname + " " + empmname + " " + emplname
        else:
            desig=i['other_members']
            # desig="NA"
            name=i['other_members']

        temp['desig']=desig
        temp['name']=name
        temp['status_flag']=i['status_flag']
        present.append(temp)
    
    # for i in item_details:
    #     if insp_details[0]['type']==0:
    #         # print(i['item_heading'],i['item_subheading'],i['remarks'],i['item_description'],i['item_decision'])
    #         i['item_heading']=decryptWithAes(i['item_heading']) if i['item_heading']!=None else 'NA'
    #         i['item_subheading']=decryptWithAes(i['item_subheading']) if i['item_subheading']!=None else 'NA'
    #         i['remarks']=decryptWithAes(i['remarks']) if m3.Marked_Members.objects.filter(item_no_id=i['item_no']).exists() else 'NA'
    #         i['item_description']=decryptWithAes(i['item_description']) if i['item_description']!=None else 'NA'
    #         i['item_decision']=decryptWithAes(i['item_decision']) if i['item_decision']!=None else 'NA'
    #         # if i['item_heading']!=None:
    #         #     i['item_heading']=decryptWithAes(i['item_heading'])
    #         # else:
    #         #     i['item_heading']='NA'
            
    #         # if i['item_subheading']!=None:
    #         #     print("hello",i['item_subheading'])
    #         #     i['item_subheading']=decryptWithAes(i['item_subheading'])
    #         # else:
    #         #     print("not hello")
    #         #     i['item_subheading']='NA'

    #         # if i['remarks']!=None:
    #         #     i['remarks']=decryptWithAes(i['remarks'])
    #         # else:
    #         #     i['remarks']='NA'
    #     else:
    #         print(i['remarks'])
    #         i['remarks']=i['remarks'] if i['remarks'] else 'NA'
            
           
    #     temp={}
    #     if m3.Marked_Members.objects.filter(item_no_id=i['item_no']).exists():
    #         # if login_desig[0]['d_level']=='CRB' or login_desig[0]['d_level']=='BM' or login_desig[0]['d_level']=='Secy_RB':
    #         mark=m3.Marked_Members.objects.filter(item_no_id=i['item_no']).values()
    #         desig_longdesc1 =''
    #         count_mark=len(mark)
    #         countm=1
    #         for x in mark:
    #             marked=models.Level_Desig.objects.filter(designation_code=x['marked_to_id'])
    #             #print('yyyyyyyy', marked[0].designation)
    #             if  marked[0].designation and count_mark!=countm:
    #                 desig_longdesc1 += marked[0].designation+', '
    #                 countm+=1
    #             else:
    #                 desig_longdesc1 += marked[0].designation
    #             #print(desig_longdesc1,'desig_longdesc1')
    #         temp['dealt']=desig_longdesc1
    #         temp['item_no']=i['des_id']
    #     dealt.append(temp)
    # print(item_details,'dealtdealt')
    

    
    detailsdata = list(m3.Item_details.objects.filter(insp_no=insp_no).values().order_by('slno'))
    
    for i in range(len(detailsdata)):
        created_on =  detailsdata[i]['created_on'].strftime('%Y-%m-%d') if  detailsdata[i]['created_on'] is not None else ''
        updated_on =  detailsdata[i]['updated_on'].strftime('%Y-%m-%d') if  detailsdata[i]['updated_on'] is not None else ''
        target_date = detailsdata[i]['target_date'].strftime('%d/%m/%y') if  detailsdata[i]['target_date'] is not None else ''
        item_priority = detailsdata[i]['item_priority'] if detailsdata[i]['item_priority'] is not None else '0'
        if detailsdata[i]['remarks'] is not None:
            remarks = detailsdata[i]['remarks'] if len(detailsdata[i]['remarks']) != 0 else None
        else:
            remarks = None
        link_image  = []
        if detailsdata[i]['link_image'] is not None:
            l1 = detailsdata[i]['link_image'].split('@#@')
            for img1 in l1:
                link_image.append(os.path.abspath(img1))
        
        
        detailsdata[i].update({'remarks':remarks,'created_on':created_on,'updated_on':updated_on,'target_date':target_date,'item_priority':item_priority,'link_image':link_image})
        Marked_MembersData = list(m3.Marked_Members.objects.filter(item_no=detailsdata[i]['item_no']).values('marked_to_id','priority','target_date','marked_to_id__designation','action_type'))
        
        marked_key = []
        marked_desig = ''
        marked_id = '[]'
        custom_info = []
        d_id = []
        d_id_str = []
        ac_co = -1
        in_co = -1
        for j in Marked_MembersData:
            d_id.append(j['marked_to_id'])
            d_id_str.append(str(j['marked_to_id']))
            
            if j['action_type'] == 1:
                action_type ='info'
                in_co += 1
            else:
                action_type = 'action'
                ac_co += 1
                

                
            custom_info.append({'selected_action':action_type,'Designation':j['marked_to_id__designation'],'in_co': in_co, 'ac_co':ac_co}) 
        if len(custom_info) > 0:
            custom_info = sorted(custom_info , key = lambda x: x['selected_action'])    
        _tbl_tbl = []
        if detailsdata[i]['table_data'] != '[]':
                res = eval(detailsdata[i]['table_data'])
                for k1 in range(len(res)):
                    d2 = []
                    for k2 in range(len(res[k1])):
                        d2.append(res[k1][k2])
                    _tbl_tbl.append(d2)
        else:
            _tbl_tbl = []
        detailsdata[i].update({'tbl_tbl':_tbl_tbl,'tbllen':len(_tbl_tbl),'custom_info':custom_info})
    
   
    
    if(m3.copydealt_mail.objects.filter(insp_no=insp_no, area='CopyTo')):
        copyto = m3.copydealt_mail.objects.filter(insp_no=insp_no, area='CopyTo')[0].send_to
    else:
        copyto=''
    copy_to=[]
    copy_to = list(m6.copyto_mails.objects.filter(doc_id=insp_no, doc_table='m', area_flag=0).values('receiver_desig'))
    if len(copy_to):
        copy_to=copy_to[0]['receiver_desig']
    if len(copy_to) > 0:
        copy_to = copy_to.split(',')
    else:
        copy_to = []
    insp_ofc_name = insp_details[0]['officer_name'] if insp_details[0]['officer_name'] != None else ''
    station_name = insp_details[0]['station_name'] if insp_details[0]['station_name'] != None else ''
    insp_desig = insp_details[0]['officer_desig'] if insp_details[0]['officer_desig'] != None else ''
    context={
        'copyto':copy_to,
        'insp_details':insp_details,
        # 'item_details':item_details,
        'present':present,
        'dealt':dealt,
        'detailsdata':detailsdata,
        'mom_officer_name':mom_officer_name,
        'insp_ofc_name':insp_ofc_name,
        'station_name':station_name,  
        'insp_desig':insp_desig,
    }
    
    template_src='mom_ReportPdf.html'
    return render_to_pdf(template_src, context)


def mom_reply_form(request):
    try:

        #print('reply_form')
        user=request.user.username
        if request.user.user_role == 'guest':
                user=request.user.guest_email
        desigid=models.Level_Desig.objects.exclude(official_email_ID=None).filter(Q(official_email_ID=request.user)| Q(official_email_ID=request.user.guest_email) | Q(official_email_ID=request.user.email))
        dealt_reply=[]
        count=1
        insp_details=m3.Insp_details.objects.values().order_by('insp_no')
        if desigid[0].d_level=='CRB' or desigid[0].d_level=='BM' or desigid[0].d_level=='Secy_RB' or desigid[0].d_level=='ED' or desigid[0].d_level=='AM' or desigid[0].d_level=='PED':
            meeting=''
            str='RB'
        else:
           
            meeting=list(m3.meeting_typelist.objects.filter(default_flag=1).values('meeting_type').distinct().order_by('meeting_type'))
            meetings=(list(m3.meeting_typelist.objects.filter(default_flag=0,added_by=desigid[0].designation_code).values('meeting_type').distinct().order_by('meeting_type')))
            for m in meetings:
                meeting.append({'meeting_type': m['meeting_type']})
            str='NoRB'
        for i in insp_details:
            if (m3.Marked_Members.objects.filter(item_no__insp_no=i['insp_no'],marked_to=desigid[0].designation_code,status_flag=1).exists()) or (m3.Marked_Members.objects.filter(item_no__insp_no=i['insp_no'],marked_to=desigid[0].designation_code,status_flag=1,status='R').exists()):
                temp={}
                temp['sr_no']=count
                temp['insp_no']=i['insp_no']
                temp['mom_note_no']=i['mom_note_no']
                temp['mom_title']=i['mom_title']
                temp['mom_date']=i['mom_date']
                temp['created_on']=i['created_on']
                dealt_reply.append(temp)
                count=count+1
        
        context={'dealt_reply':dealt_reply,'str':str,'meeting':meeting}
        return render(request,"mom_reply_form.html",context)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="mom_reply_form",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "mom_errors.html", {})


def mom_reply_ajax(request):
    #data for reply modal  
    try:
        if request.method == "GET" and request.is_ajax():
            str=request.GET.get('str')
            cuser=request.user.username
            if request.user.user_role == 'guest':
                cuser=request.user.guest_email
            desigid=models.Level_Desig.objects.exclude(official_email_ID=None).filter(Q(official_email_ID=request.user)| Q(official_email_ID=request.user.guest_email) | Q(official_email_ID=request.user.email))[0].designation_code  

            if(str=='pending') and (request.GET.get('insp_no')):
                final_list=[]
                insp_no=request.GET.get('insp_no')
                list_pending=m3.Marked_Members.objects.filter(Q(item_no__insp_no=insp_no,marked_to_id=desigid,status_flag=1)|Q(item_no__insp_no=insp_no,marked_to_id=desigid,status_flag=1,status='R')).values('item_no_id','action_type')
                for i in list_pending:
                    if(m3.Item_details.objects.filter(item_no=i['item_no_id'])):
                        list_item=m3.Item_details.objects.filter(item_no=i['item_no_id']).values()
                        temp={}
                        temp['item_db']=i['item_no_id']
                        temp['type']=list_item[0]['type']
                        temp['item_no']=list_item[0]['des_id']
                        temp['item_heading']=list_item[0]['item_heading']
                        temp['item_subheading']=list_item[0]['item_subheading']
                        temp['item_description']=list_item[0]['item_description'] 
                        temp['item_decision']=list_item[0]['item_decision']
                        temp['action_type']=i['action_type']  
                        temp['target_date'] = list_item[0]['target_date'].strftime('%d/%m/%y') if  list_item[0]['target_date'] is not None else ''
                        temp['item_priority'] = list_item[0]['item_priority'] if list_item[0]['item_priority'] is not None else '1'
                        temp['remarks']=list_item[0]['remarks']

                        _tbl_tbl = []
                        if list_item[0]['table_data'] != '[]':
                                res = eval(list_item[0]['table_data'])
                                for k1 in range(len(res)):
                                    d2 = []
                                    for k2 in range(len(res[k1])):
                                        d2.append(res[k1][k2])
                                    _tbl_tbl.append(d2)
                        else:
                            _tbl_tbl = []
                        link_image  = []
                        if list_item[0]['link_image'] is not None:
                            l1 = list_item[0]['link_image'].split('@#@')
                            for img1 in l1:
                                link_image.append(img1)
                        temp['tbl_tbl'] = _tbl_tbl
                        temp['link_image'] = link_image
                        
                    final_list.append(temp)
                
                return JsonResponse({'itemdetails':final_list,})
            
            elif(str=='accept') and (request.GET.get('insp_no')):
                final_list=[]
                insp_no=request.GET.get('insp_no')
                list_accept=m3.Marked_Members.objects.filter(item_no__insp_no=insp_no,marked_to_id=desigid,status_flag=3).values('item_no_id','reply_text','reply_file')
                #print(list_accept,'list_accept')
                for i in list_accept:
                    if(m3.Item_details.objects.filter(item_no=i['item_no_id'])):
                        list_item=m3.Item_details.objects.filter(item_no=i['item_no_id']).values()
                        temp={}
                        temp['note_no']=m3.Insp_details.objects.filter(insp_no=list_item[0]['insp_no_id'])[0].mom_note_no
                        temp['item_db']=i['item_no_id']
                        temp['type']=list_item[0]['type']
                        temp['item_no']=list_item[0]['des_id']
                        temp['item_heading']=list_item[0]['item_heading']
                        temp['item_subheading']=list_item[0]['item_subheading']
                        temp['item_description']=list_item[0]['item_description']
                        temp['item_decision']=list_item[0]['item_decision']
                        temp['remark']=i['reply_text']
                        if(i['reply_file']):
                            temp['file_remark']=i['reply_file']
                        else:
                            temp['file_remark']=''
                    final_list.append(temp)
                #print(final_list,'final_list')
                return JsonResponse({'itemdetails':final_list,})
            
            elif(str=='save_text'):
                #print('EFGH')
                insp_no=request.GET.get('insp_no')
                item_no=request.GET.get('item_no')
                reply_text=request.GET.get('reply_text')
                item_no_list=m3.Item_details.objects.filter(insp_no_id=insp_no).values('item_no')
                marked_no=m3.Marked_Members.objects.filter(item_no__insp_no_id=insp_no,item_no_id=item_no).values('marked_no')
                #print(insp_no,'--',item_no,'--',reply_text)
                if(reply_text==''):
                    bono=[]
                    return JsonResponse(bono, safe = False)
                m3.Marked_Members.objects.filter(item_no__insp_no_id=insp_no,item_no_id=item_no,marked_to_id=desigid,status_flag=1).update(reply_text=reply_text,status_flag=3,reply_on=datetime.now())
                if m3.Marked_Members.objects.filter(marked_no__in=marked_no,status_flag=3).exists():
                    flag=0
                    #print('11')
                    for i in m3.Marked_Members.objects.filter(marked_no__in=marked_no).values('status_flag'):
                        if(i['status_flag']!=3):
                            flag=1
                    if(flag==0):
                        m3.Item_details.objects.filter(item_no=item_no,insp_no_id=insp_no).update(status_flag=4)
                    else:
                        m3.Item_details.objects.filter(item_no=item_no,insp_no_id=insp_no).update(status_flag=2)
                # if m3.Marked_Members.objects.filter(marked_no__in=marked_no)[0].status_flag!=3:
                #     #print('22')
                #     m3.Item_details.objects.filter(item_no=item_no,insp_no_id=insp_no).update(status_flag=2)
                if m3.Item_details.objects.filter(item_no__in=item_no_list):
                    flag=0
                    #print('33')
                    for i in m3.Item_details.objects.filter(item_no__in=item_no_list).values('status_flag'):
                        if(i['status_flag']!=4):
                            flag=1
                    if(flag==0):
                        m3.Insp_details.objects.filter(insp_no=insp_no).update(status_flag=4)
                    else:
                        m3.Insp_details.objects.filter(insp_no=insp_no).update(status_flag=2)
                # if m3.Item_details.objects.filter(item_no__in=item_no_list)[0].status_flag!=4:
                #     #print('44')
                #     m3.Insp_details.objects.filter(insp_no=insp_no).update(status_flag=2)
                return JsonResponse({"status": 1 })
        
        # save reply
        if request.method == "POST" and request.is_ajax():
            #print('ABCD')
            cuser=request.user.username
            desigid=models.Level_Desig.objects.exclude(official_email_ID=None).filter(Q(official_email_ID=request.user)| Q(official_email_ID=request.user.guest_email) | Q(official_email_ID=request.user.email))[0].designation_code  
            insp_no=request.POST.get('insp_no')
            item_no=request.POST.get('item_no')
            reply_text=request.POST.get('reply_text')
            reply_file=request.FILES.get('file')
            # insp_no=request.POST['insp_no']
            # item_no=request.POST['item_no']
            # reply_text=request.POSt['reply_text']
            # reply_file=request.FILES['file']
            item_no_list=m3.Item_details.objects.filter(insp_no_id=insp_no).values('item_no')
            marked_no=m3.Marked_Members.objects.filter(item_no__insp_no_id=insp_no,item_no_id=item_no).values('marked_no')
            file=FileSystemStorage()
            filename=file.save(reply_file.name,reply_file)
            url=file.url(filename)
            #print(insp_no,'--',item_no,'--',reply_text,'--',url)
            if(reply_text!='' and url!=None):
                m3.Marked_Members.objects.filter(item_no__insp_no_id=insp_no,item_no_id=item_no,marked_to_id=desigid,status_flag=1).update(reply_text=reply_text,reply_file=url,status_flag=3,reply_on=datetime.now())
            elif(reply_text!='' and url==None):
                m3.Marked_Members.objects.filter(item_no__insp_no_id=insp_no,item_no_id=item_no,marked_to_id=desigid,status_flag=1).update(reply_text=reply_text,status_flag=3,reply_on=datetime.now())
            elif(reply_text=='' and url!=None):
                m3.Marked_Members.objects.filter(item_no__insp_no_id=insp_no,item_no_id=item_no,marked_to_id=desigid,status_flag=1).update(reply_file=url,status_flag=3,reply_on=datetime.now())
            elif(reply_text=='' and url==None):
                bono=[]
                return JsonResponse(bono, safe = False)
            if m3.Marked_Members.objects.filter(marked_no__in=marked_no,status_flag=3).exists():
                flag=0
                #print('11')
                for i in m3.Marked_Members.objects.filter(marked_no__in=marked_no).values('status_flag'):
                    if(i['status_flag']!=3):
                        flag=1
                if(flag==0):
                    m3.Item_details.objects.filter(item_no=item_no,insp_no_id=insp_no).update(status_flag=4)
                else:
                    m3.Item_details.objects.filter(item_no=item_no,insp_no_id=insp_no).update(status_flag=2)
            # if m3.Marked_Members.objects.filter(marked_no__in=marked_no)[0].status_flag!=3:
            #     #print('22')
            #     m3.Item_details.objects.filter(item_no=item_no,insp_no_id=insp_no).update(status_flag=2)
            if m3.Item_details.objects.filter(item_no__in=item_no_list):
                flag=0
                #print('33')
                for i in m3.Item_details.objects.filter(item_no__in=item_no_list).values('status_flag'):
                    if(i['status_flag']!=4):
                        flag=1
                if(flag==0):
                    m3.Insp_details.objects.filter(insp_no=insp_no).update(status_flag=4)
                else:
                    m3.Insp_details.objects.filter(insp_no=insp_no).update(status_flag=2)
            # if m3.Item_details.objects.filter(item_no__in=item_no_list)[0].status_flag!=4:
            #     #print('44')
            #     m3.Insp_details.objects.filter(insp_no=insp_no).update(status_flag=2)
            return JsonResponse({"status": 1 })
        
        return JsonResponse({"success":False},status=400)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="mom_replay_ajax",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "mom_errors.html", {})  

def receivemomreply(request, insp_no):
    try:
        mom_title=m3.Insp_details.objects.filter(insp_no=insp_no).values('mom_title','mom_date','insp_no','mom_note_no')
        final_list=[]
        list_accept=m3.Marked_Members.objects.exclude(item_no_id__status_flag=1).filter(item_no__insp_no=insp_no).values('action_type','item_no_id','reply_text','marked_to_id','reply_on','marked_no').distinct('item_no_id')
        for i in list_accept:
           
            if(m3.Item_details.objects.exclude(status_flag=1).filter(item_no=i['item_no_id'])):
                list_item=m3.Item_details.objects.exclude(status_flag=1).filter(item_no=i['item_no_id']).values()
                temp={}
                temp['item_db']=i['item_no_id']
                temp['type']=list_item[0]['type']
                temp['item_no']=list_item[0]['des_id']
                temp['item_heading']=list_item[0]['item_heading']
                temp['item_subheading']=list_item[0]['item_subheading']
                temp['item_description']=list_item[0]['item_description']  if list_item[0]['item_description'] is not None else ''
                temp['item_decision']=list_item[0]['item_decision']
                temp['marked_no']=i['marked_no']
                if(i['marked_to_id']):
                    temp['chk']='YES'
                    temp['marked']=m3.Marked_Members.objects.filter(item_no_id=i['item_no_id'],status_flag=3).values('action_type','marked_no','marked_to__designation','reply_text','reply_file','reply_on')
                else:
                    temp['chk']='NO'
                temp['mdate']=mom_title[0]['mom_date'].strftime("%d/%m/%y")  

                temp['action_type']=i['action_type']  if list_item[0]['item_description'] is not None else 0
                temp['target_date'] = list_item[0]['target_date'].strftime('%d/%m/%y') if  list_item[0]['target_date'] is not None else ''
                temp['item_priority'] = list_item[0]['item_priority'] if list_item[0]['item_priority'] is not None else '1'
                temp['remarks']=list_item[0]['remarks']
                _tbl_tbl = []
                if list_item[0]['table_data'] != '[]':
                        res = eval(list_item[0]['table_data'])
                        for k1 in range(len(res)):
                            d2 = []
                            for k2 in range(len(res[k1])):
                                d2.append(res[k1][k2])
                            _tbl_tbl.append(d2)
                else:
                    _tbl_tbl = []
                link_image  = []
                if list_item[0]['link_image'] is not None:
                    l1 = list_item[0]['link_image'].split('@#@')
                    for img1 in l1:
                        link_image.append(img1)
                temp['tbl_tbl'] = _tbl_tbl
                temp['tbl_tbl_len'] = len(_tbl_tbl)
                temp['link_image'] = link_image  
                temp['link_image_len'] = len(link_image)  

            final_list.append(temp)
        print('final_list  ',final_list)
        context={
            'mom_title':mom_title,
            'final_list':final_list}
        return render(request,"receivemomreply.html",context)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="receivememreply",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "mom_errors.html", {})
    
####  with library encrypt hindi fint also
import base64 
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad

def encryptWithAesEinspect(data):
        key = 'AAAAAAAAAAAAAAAA'
        iv =  'BBBBBBBBBBBBBBBB'.encode('utf-8')
        data= pad(data.encode(),16)
        cipher = AES.new(key.encode('utf-8'),AES.MODE_CBC,iv)
        encrypted = base64.b64encode(cipher.encrypt(data))
        return encrypted.decode("utf-8", "ignore")


def decryptWithAesEinspect(enc):
        key = 'AAAAAAAAAAAAAAAA'
        iv =  'BBBBBBBBBBBBBBBB'.encode('utf-8')
        enc = base64.b64decode(enc)
        cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(enc),16)
        return decrypted.decode("utf-8", "ignore")










