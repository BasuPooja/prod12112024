from array import array
from datetime import datetime
import email
from django.shortcuts import render,redirect
from inspects.utils import render_to_pdf
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.db import models
from myadmin import models
from inspects import models as m1
from einspect import models as m2
from mom import models as m3
from do_letters import models as m4
from mails import models as m6
from django.db.models import Q
from django.db.models import Max
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.files.storage import FileSystemStorage
import json


def copyto_mails(request):
    try:
        empnox = models.Level_Desig.objects.exclude(delete_flag=True).exclude(official_email_ID = None).filter(Q(official_email_ID=request.user)| Q(official_email_ID=request.user.guest_email) | Q(official_email_ID=request.user.email), empno__isnull=False)
        if empnox:
            empno = empnox[0].empno_id
            desig = empnox[0].designation_code

        else:
            messages.error(request, 'You are not authorize to view this page. Please contact admin')

        mails=[]
        temp_mails=list(m6.copyto_mails.objects.filter(area_flag=0).values('sender_id__designation','mail_no','created_on','sender_id','doc_id',
        'doc_table','receiver_id','subject','body','noted_flag','noted_by').distinct())
        # print(maaaa,"helllooooooo",desig)
        # temp_mails = list(m6.copyto_mails.objects.filter(receiver_id__contains=str(desig), area_flag=0).values('sender_id__designation','mail_no','created_on','sender_id','doc_id',
        # 'doc_table','receiver_id','subject','body','noted_flag','noted_by').distinct())
        
        doc_list={}
        
        for m in temp_mails:
            receivers=m['receiver_id'].split(',')
            # print(receivers)
            if str(desig) in receivers:
                m.update({'created_on':m['created_on'].strftime("%d/%m/%y")})
                m.update({'sender_desig':m['sender_id__designation']})
                if m['noted_flag']!=0:
                    if m6.copyto_mails.objects.filter(noted_by__contains=str(desig),mail_no=m['mail_no']):
                        m.update({'noted':'1'})
                    else:
                        m.update({'noted':'0'})
                else:
                    m.update({'noted':'0'})
                    
                if m['doc_table'] == 'i':
                    if m1.Inspection_details.objects.exclude(status_flag=0).filter(inspection_no=m['doc_id']):
                        doc_list['i']='Inspection Report'
                        note_no=m1.Inspection_details.objects.exclude(status_flag=0).filter(inspection_no=m['doc_id']).values('inspection_note_no')[0]['inspection_note_no']
                        m.update({'note_no':note_no})
                        if m not in mails:
                            mails.append(m)

                elif m['doc_table'] == 'd':
                    if m4.do_upload.objects.exclude(status_flag=0).filter(id=m['doc_id']):
                        doc_list['d'] ='D.O. Letters'
                        note_no=m4.do_upload.objects.exclude(status_flag=0).filter(id=m['doc_id']).values('do_letter_no')[0]['do_letter_no']
                        m.update({'note_no':note_no})
                        if m not in mails:
                            mails.append(m)
                    
                elif m['doc_table'] == 'm':
                    if m3.Insp_details.objects.exclude(status_flag=0).filter(insp_no=m['doc_id']):
                        doc_list['m']='MOM Report'
                        note_no=m3.Insp_details.objects.exclude(status_flag=0).filter(insp_no=m['doc_id']).values('mom_note_no')[0]['mom_note_no']
                        m.update({'note_no':note_no})
                        if m not in mails:
                            mails.append(m)
                    
                else:
                    pass
            
        
            # print(mails)
        
        doclist=[]
        doclist.append(doc_list)
        ofcs=[]

        for m in mails:
            if {'designation':m['sender_desig'], 'designation_code':m['sender_id']} not in ofcs:
                ofcs.append({'designation':m['sender_desig'], 'designation_code':m['sender_id']})

        context={'mails':mails, 'officers': ofcs, 'doc_list' : doclist}
        return render(request,'copyto_mails.html', context) 
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="copyto_mails",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "errors_mails.html", {})


def do_pdf(request, do_id):
    try:
        template=list(m4.do_upload.objects.filter(id=do_id).values('do_path'))[0]['do_path']
        template='/media/'+template
        context={'template':template}
        return render(request,'do_pdf.html', context)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="do_pdf",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "errors_mails.html", {})


def filter_data_ajax(request):
    try:
        empnox = models.Level_Desig.objects.exclude(delete_flag=True).exclude(official_email_ID = None).filter(Q(official_email_ID=request.user)| Q(official_email_ID=request.user.guest_email) | Q(official_email_ID=request.user.email), empno__isnull=False)
        user_role=request.user.user_role
        if empnox:
            empno = empnox[0].empno_id
            desig = empnox[0].designation_code
        
        else:
            messages.error(request, 'You are not authorize to view this page. Please contact admin')
        

        if request.method == 'POST' and request.is_ajax():
            date_range=request.POST.get('date_range')
            doc_type=list(request.POST.get('subject'))
            action_by= request.POST.get('sender')
            marked_officers=action_by.split(',')
            

            if doc_type:
                pass
            else:
                docs=list(m6.copyto_mails.objects.filter(receiver_id__contains=str(desig)).values('doc_table'))
                for i in docs:
                    if i['doc_table'] not in doc_type:
                        doc_type.append(i['doc_table'])
            
            if action_by:
                for i in range(len(marked_officers)):
                    marked_officers[i]=int(marked_officers[i])        
            else:
                marked_officers=[]
                ofcs=list(m6.copyto_mails.objects.filter(receiver_id__contains=str(desig)).values('sender_id_id'))
                for i in ofcs:
                    if i['sender_id_id'] not in marked_officers:
                        marked_officers.append(i['sender_id_id'])

            
            if date_range:
                sp_date = date_range.split('-')
                start  = datetime.strptime(sp_date[0].strip(),"%d/%m/%Y").strftime("%Y-%m-%d")
                end  = datetime.strptime(sp_date[1].strip(),"%d/%m/%Y").strftime("%Y-%m-%d")
                temp_mails = list(m6.copyto_mails.objects.filter(receiver_id__contains=str(desig),area_flag=0, created_on__date__gte=start, created_on__date__lte=end, doc_table__in=doc_type, sender_id__in=marked_officers).values('sender_id__designation','mail_no','created_on','sender_id','doc_id',
                    'doc_table','receiver_id','subject','body','noted_flag','noted_by').distinct())
                print(len(temp_mails),temp_mails)
            
            else:
                temp_mails=list(m6.copyto_mails.objects.filter(receiver_id__contains=str(desig),area_flag=0, doc_table__in=doc_type, sender_id__in=marked_officers).values('sender_id__designation','mail_no','created_on','sender_id','doc_id',
                    'doc_table','receiver_id','subject','body','noted_flag','noted_by').distinct())
                print(len(temp_mails),temp_mails)
                
                
            mails=[]
            print(mails,len(temp_mails),temp_mails)

            for m in temp_mails:
                m.update({'created_on':m['created_on'].strftime("%d/%m/%y")})
                m.update({'sender_desig':m['sender_id__designation']})

                if m['noted_flag']!=0:
                    if m6.copyto_mails.objects.filter(noted_by__contains=str(desig),mail_no=m['mail_no']):
                        m.update({'noted':'1'})
                    else:
                        m.update({'noted':'0'})
                else:
                    m.update({'noted':'0'})

                if m['doc_table'] == 'i':
                    if m1.Inspection_details.objects.exclude(status_flag=0).filter(inspection_no=m['doc_id']):
                        note_no=m1.Inspection_details.objects.exclude(status_flag=0).filter(inspection_no=m['doc_id']).values('inspection_note_no')[0]['inspection_note_no']
                        m.update({'note_no':note_no})
                        if m not in mails:
                            mails.append(m)

                elif m['doc_table'] == 'd':
                    if m4.do_upload.objects.exclude(status_flag=0).filter(id=m['doc_id']):
                        note_no=m4.do_upload.objects.exclude(status_flag=0).filter(id=m['doc_id']).values('do_letter_no')[0]['do_letter_no']
                        m.update({'note_no':note_no})
                        if m not in mails:
                            mails.append(m)
                    
                elif m['doc_table'] == 'm':
                    if m3.Insp_details.objects.exclude(status_flag=0).filter(insp_no=m['doc_id']):
                        note_no=m3.Insp_details.objects.exclude(status_flag=0).filter(insp_no=m['doc_id']).values('mom_note_no')[0]['mom_note_no']
                        m.update({'note_no':note_no})
                        if m not in mails:
                            mails.append(m)
                    



            context={'mails':mails,'user_role':user_role}
            return JsonResponse(context, safe=False)
        return JsonResponse({'success': False}, status=400)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="filter_data_ajax",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "errors_mails.html", {})

def noted_by(request):
    if request.method == 'GET' and request.is_ajax():
        empnox = models.Level_Desig.objects.exclude(delete_flag=True).exclude(official_email_ID = None).filter(Q(official_email_ID=request.user)| Q(official_email_ID=request.user.guest_email) | Q(official_email_ID=request.user.email), empno__isnull=False)
        if empnox:
            empno = empnox[0].empno_id
            desig = empnox[0].designation_code
        mail_id=request.GET.get('mail_id')
        print("hello apeksha",mail_id)
        noted_flag=list(m6.copyto_mails.objects.filter(mail_no=mail_id).values('noted_flag'))[0]['noted_flag']
        # print(noted_flag)
        if noted_flag==1:
            officers=list(m6.copyto_mails.objects.filter(mail_no=mail_id).values('noted_by'))[0]['noted_by']
            print(officers)
            officers=officers+','+str(desig)
        else:
            officers=str(desig)
        m6.copyto_mails.objects.filter(mail_no=mail_id).update(noted_flag=1,noted_by=officers)
        # print("I am here")
        context={'mails':mail_id}
        return JsonResponse(context, safe=False)
    return JsonResponse({'success': False}, status=400)

def copyto_mails_send(request):
    # try:
        empnox = models.Level_Desig.objects.exclude(delete_flag=True).exclude(official_email_ID = None).filter(Q(official_email_ID=request.user)| Q(official_email_ID=request.user.guest_email) | Q(official_email_ID=request.user.email), empno__isnull=False)
        print(empnox)
        if empnox:
            empno = empnox[0].empno_id
            desig = empnox[0].designation_code

        else:
            messages.error(request, 'You are not authorize to view this page. Please contact admin')
            # return(False)

        mails=[]
        

        temp_mails = list(m6.copyto_mails.objects.filter(sender_id=desig, area_flag=0).values('receiver_desig','mail_no','created_on','doc_id',
        'doc_table','receiver_id','subject','body','noted_flag','noted_by').distinct())

        doc_list={}
        notes=[]
        for m in temp_mails:
            m.update({'created_on':m['created_on'].strftime("%d/%m/%y")})
            
            if m['noted_flag']!=0:
                officers=m6.copyto_mails.objects.filter(mail_no=m['mail_no']).values('noted_by')[0]['noted_by']
                officers=list(officers.split(','))
                print(officers)
                ofc=list(models.Level_Desig.objects.exclude(delete_flag=True).filter(designation_code__in=officers).values_list('designation', flat=True))
                print(ofc)
                m.update({'officers':ofc})

            else:
                m.update({'officers':'NA'})

            receivers=list(m['receiver_desig'].split(','))
            recvd=[]
            for r in receivers:
                if r in m['officers']:
                    recvd.append({'desig_rcvd':r,'flag':1})
                else:
                    recvd.append({'desig_rcvd':r,'flag':0})
            m.update({'receiver_desigs':recvd})

                
            if m['doc_table'] == 'i':
                if m1.Inspection_details.objects.exclude(status_flag=0).filter(inspection_no=m['doc_id']):
                    doc_list['i']='Inspection Report'
                    note_no=m1.Inspection_details.objects.exclude(status_flag=0).filter(inspection_no=m['doc_id']).values('inspection_note_no')[0]['inspection_note_no']
                    m.update({'note_no':note_no})
                    if m not in mails:
                        mails.append(m)
                        notes.append(m['mail_no'])

            elif m['doc_table'] == 'd':
                if m4.do_upload.objects.exclude(status_flag=0).filter(id=m['doc_id']):
                    doc_list['d'] ='D.O. Letters'
                    note_no=m4.do_upload.objects.exclude(status_flag=0).filter(id=m['doc_id']).values('do_letter_no')[0]['do_letter_no']
                    m.update({'note_no':note_no})
                    if m not in mails:
                        mails.append(m)
                        notes.append(m['mail_no'])
                
            elif m['doc_table'] == 'm':
                if m3.Insp_details.objects.exclude(status_flag=0).filter(insp_no=m['doc_id']):
                    doc_list['m']='MOM Report'
                    note_no=m3.Insp_details.objects.exclude(status_flag=0).filter(insp_no=m['doc_id']).values('mom_note_no')[0]['mom_note_no']
                    m.update({'note_no':note_no})
                    if m not in mails:
                        mails.append(m)
                        notes.append(m['mail_no'])
                
            else:
                pass
        # print(mails)
        doclist=[]
        doclist.append(doc_list)
        # print(doclist)
        receivers = list(m6.copyto_mails.objects.filter(sender_id=desig, area_flag=0, mail_no__in=notes).values_list('receiver_id', flat=True))
        receiver=[]
        for r in receivers:
            rec=r.split(',')
            for rr in rec:
                if rr not in receiver and rr!='':
                    receiver.append(rr)

        receiverdesig = list(models.Level_Desig.objects.exclude(delete_flag=True).filter(designation_code__in=receiver).values('designation_code','designation'))
        context={'mails':mails,'receivers':receiverdesig,'doc_list':doclist}
        # print(context)
        return render(request,'copyto_mails_send.html', context) 
    # except Exception as e: 
    #     try:
    #         m1.error_Table.objects.create(fun_name="copyto_mails",user_id=request.user,err_details=str(e))
    #     except:
    #         print("Internal Error!!!")
    #     return render(request, "errors_mails.html", {})


def filter_data_ajax_send(request):
    try:
        empnox = models.Level_Desig.objects.exclude(delete_flag=True).exclude(official_email_ID = None).filter(Q(official_email_ID=request.user)| Q(official_email_ID=request.user.guest_email) | Q(official_email_ID=request.user.email), empno__isnull=False)
        if empnox:
            empno = empnox[0].empno_id
            desig = empnox[0].designation_code

        else:
            messages.error(request, 'You are not authorize to view this page. Please contact admin')
        

        if request.method == 'POST' and request.is_ajax():
            date_range=request.POST.get('date_range')
            doc_type=list(request.POST.get('subject'))
            action_by= request.POST.get('sender')
            marked_officers=action_by.split(',')
            
            print(action_by)

            if doc_type:
                pass
            else:
                docs=list(m6.copyto_mails.objects.filter(sender_id=desig, area_flag=0).values('doc_table'))
                for i in docs:
                    if i['doc_table'] not in doc_type:
                        doc_type.append(i['doc_table'])
            
            notes=[]
            if action_by:
                for i in range(len(marked_officers)):
                    mail_nos=list(m6.copyto_mails.objects.filter(sender_id=desig, area_flag=0,receiver_id__contains=marked_officers[i]).values_list('mail_no', flat=True))  
                    for m in mail_nos:
                        if m not in notes:
                            notes.append(m)
            else:
                notes = list(m6.copyto_mails.objects.filter(sender_id=desig, area_flag=0).values_list('mail_no', flat=True))
                
            # print(notes)
            
            if date_range:
                sp_date = date_range.split('-')
                start  = datetime.strptime(sp_date[0].strip(),"%d/%m/%Y").strftime("%Y-%m-%d")
                end  = datetime.strptime(sp_date[1].strip(),"%d/%m/%Y").strftime("%Y-%m-%d")
                temp_mails = list(m6.copyto_mails.objects.filter(sender_id=desig, mail_no__in=notes, created_on__date__gte=start, created_on__date__lte=end, doc_table__in=doc_type,area_flag=0).values('receiver_desig','mail_no','created_on','doc_id',
                                'doc_table','receiver_id','subject','body','noted_flag','noted_by').distinct())
                
            else:
                temp_mails = list(m6.copyto_mails.objects.filter(sender_id=desig, mail_no__in=notes, doc_table__in=doc_type,area_flag=0).values('receiver_desig','mail_no','created_on','doc_id',
                                'doc_table','receiver_id','subject','body','noted_flag','noted_by').distinct())
                
                
            doc_list={}
            doclist=[]
            ofcs=[]
            mails=[]
            

            for m in temp_mails:
                m.update({'created_on':m['created_on'].strftime("%d/%m/%y")})
                

                if m['noted_flag']!=0:
                    officers=m6.copyto_mails.objects.filter(mail_no=m['mail_no']).values('noted_by')[0]['noted_by']
                    officers=list(officers.split(','))
                    ofc=list(models.Level_Desig.objects.exclude(delete_flag=True).filter(designation_code__in=officers).values_list('designation', flat=True))
                    m.update({'officers':ofc})

                else:
                    m.update({'officers':'NA'})

                receivers=list(m['receiver_desig'].split(','))
                recvd=[]
                for r in receivers:
                    if r in m['officers']:
                        recvd.append({'desig_rcvd':r,'flag':1})
                    else:
                        recvd.append({'desig_rcvd':r,'flag':0})
                m.update({'receiver_desigs':recvd})

                if m['doc_table'] == 'i':
                    if m1.Inspection_details.objects.exclude(status_flag=0).filter(inspection_no=m['doc_id']):
                        doc_list['i']='Inspection Report'
                        note_no=m1.Inspection_details.objects.exclude(status_flag=0).filter(inspection_no=m['doc_id']).values('inspection_note_no')[0]['inspection_note_no']
                        m.update({'note_no':note_no})
                        if m not in mails:
                            mails.append(m)

                elif m['doc_table'] == 'd':
                    if m4.do_upload.objects.exclude(status_flag=0).filter(id=m['doc_id']):
                        doc_list['d'] ='D.O. Letters'
                        note_no=m4.do_upload.objects.exclude(status_flag=0).filter(id=m['doc_id']).values('do_letter_no')[0]['do_letter_no']
                        m.update({'note_no':note_no})
                        if m not in mails:
                            mails.append(m)
                    
                elif m['doc_table'] == 'm':
                    if m3.Insp_details.objects.exclude(status_flag=0).filter(insp_no=m['doc_id']):
                        doc_list['m']='MOM Report'
                        note_no=m3.Insp_details.objects.exclude(status_flag=0).filter(insp_no=m['doc_id']).values('mom_note_no')[0]['mom_note_no']
                        m.update({'note_no':note_no})
                        if m not in mails:
                            mails.append(m)
                    
                else:
                    pass

            
            
            doclist.append(doc_list)
            # print(mails)


            context={'mails':mails}
            return JsonResponse(context, safe=False)
        return JsonResponse({'success': False}, status=400)
    except Exception as e: 
        try:
            m1.error_Table.objects.create(fun_name="filter_data_ajax",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "errors_mails.html", {})
