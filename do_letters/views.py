from datetime import datetime
from multiprocessing import context
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from inspects.models import Marked_Officers, empmast, error_Table
from myadmin.models import Level_Desig
# from .forms import UploadForm
from .models import do_upload, do_act, do_copy
from django.db.models import Q
import json
from inspects.utils import render_to_pdf
# Create your views here.
from inspects import models as m1
from mails import models as m6
def upload_do(request):
    # try:
   
        empnox = Level_Desig.objects.exclude(delete_flag=True).filter(Q(official_email_ID=request.user)| Q(official_email_ID=request.user.guest_email) | Q(official_email_ID=request.user.email), empno__isnull=False)
        if empnox:
            empno = empnox[0].empno_id
            desig = empnox[0].designation_code

        else:
            pass
            # messages.error(request, 'You are not authorize to create DO letters. Please contact to admin')
        # officers=Level_Desig.objects.exclude(delete_flag=True).filter().values('designation')   

        officers=Level_Desig.objects.exclude(delete_flag=True).exclude(designation_code=desig).values('designation', 'designation_code')
        if request.method == 'POST':  
            do_letter_no=request.POST.get('do_letter_no')
            date111=request.POST.get('date')
            if date111:
                new_date = datetime.strptime(date111, '%d/%m/%y').strftime('%Y-%m-%d')
            subject=request.POST.get('subject')
            action_by= request.POST.get('action_by_test')
            copy_to= request.POST.get('copy_to_test')
            do_text=request.POST.get('do_text')
            fail=0

            if action_by:
                marked_officers=action_by.split(',')
                copy_to=copy_to.split(',')
                if len(do_text)>0:
                    do_file=None
                else:
                    do_text=None
                    do_file=request.FILES['do_file']
                
                values=do_upload.objects.create(do_text=do_text, created_by_id = empno, desig_id_id= desig, status_flag=4, do_letter_no = do_letter_no,  do_letter_date=new_date, subject=subject, do_path= do_file, delete_flag=0 )

                if len(marked_officers[0])>0:
                    for i in marked_officers:
                        marked_officers_list = Level_Desig.objects.exclude(delete_flag=True).get(designation_code=i)
                        empnos=(Level_Desig.objects.exclude(delete_flag=True).filter(designation_code = i).values('empno'))[0]
                        if empnos['empno']:
                            marked_officers_id= m1.empmast.objects.get(empno=empnos['empno'])
                            action= do_act.objects.create(id_upload=values, desig_id=marked_officers_list, status_flag=False,  emp_no = marked_officers_id )  
                        else:
                            fail=1
                            do_upload.objects.filter(id=values.id).delete()
                            # messages.error(request,"upload unsuccessful")
                
                if copy_to != [''] and fail==0:
                    try:
                        copy_mail =[]
                        copy_desig=[]
                        copy_contact=[]
                        copy_desig_list=''
                        copy_id_list=''
                        count_copy=len(copy_to)
                        countc=1
                        for i in copy_to:
                            mail_contact=Level_Desig.objects.exclude(delete_flag=True).filter(designation_code=i)
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
                        # if len(copy_contact) > 0:
                        #     for contact in copy_contact:
                        #         MomSendSms(contact)
                        To=copy_mail
                        subject=values.subject
                        context = {
                            'title': values.subject,
                            'do_date': values.do_letter_date,
                            'insp_no': values.id,
                            'do_officer': values.desig_id,
                            'str': 'copyto'          
                        }  
                        if m6.copyto_mails.objects.filter(sender_id_id=desig, doc_id=values.id, area_flag=0, doc_table='d').exists():
                            do_mails=m6.copyto_mails.objects.filter(sender_id_id=desig, doc_id=values.id, area_flag=0, doc_table='d').update(created_on=datetime.now(),sender_id_id=desig,doc_id=values.id,doc_table='d',receiver_id=copy_id_list,receiver_desig=copy_desig_list,
                                subject='D.O. Letter', body=values.subject,area_flag=0)
                        else:
                            do_mails=m6.copyto_mails.objects.create(created_on=datetime.now(),sender_id_id=desig,doc_id=values.id,doc_table='d',receiver_id=copy_id_list,receiver_desig=copy_desig_list,
                                subject='D.O. Letter', body=values.subject,area_flag=0)
                        # MomSendMail(subject,To,context,values.insp_no)
                        # messages.success(request, 'E-mail has been send successfully to copy-to officers.')  
                    except:
                        fail=2
                        #print("ERROR-COPY-MAIL")
                        do_upload.objects.filter(id=values.id).delete()
                        do_act.objects.filter(id_upload=values).delete()
                        messages.error(request, 'Request to sent e-mail to dealt officers failed. Please Try Again.')
                
                if fail!=2:
                    return redirect('/view_previous')
            
                
                # if copy_to != [''] and fail==0:
                #     copy_to_list_str=''
                #     copy_to_list=list(Level_Desig.objects.exclude(delete_flag=True).filter(designation_code__in=copy_to).values_list('designation',flat=True))
                #     for copies in copy_to_list:
                #         copy_to_list_str+=

                #     print(copy_to_list)
                #     for i in copy_to:
                        
                #         marked_officers_list = Level_Desig.objects.exclude(delete_flag=True).get(designation_code=i)
                #         do_copy.objects.create(do_upload=values, desig_id=marked_officers_list)
                #     copy_to=(str(copy_to).strip('[')).strip(']')
                #     if m6.copyto_mails.objects.filter(sender_id_id=desig, doc_id=values.id, area_flag=0, doc_table='d').exists():
                #         m6.copyto_mails.objects.filter(sender_id_id=desig, doc_id=values.id, area_flag=0, doc_table='d').update(receiver_id=copy_to,receiver_desig=copy_to_list)
                #     else:
                #         m6.copyto_mails.objects.create(sender_id_id=desig, doc_id=values.id, area_flag=0, doc_table='d', receiver_id=copy_to, receiver_desig=copy_to_list)
                
                # else:
                #     # do_upload.objects.filter(id=values).delete()
                #     # do_act.objects.filter(id_upload=values).delete()
                #     messages.error(request,"upload unsuccessful")
        
        context = {'officers':officers}
        return render(request,'do_upload.html',context)
    # except Exception as e: 
    #     try:
    #         error_Table.objects.create(fun_name="do_upload",user_id=request.user,err_details=str(e))
    #     except:
    #         print("Internal Error!!!")
    #     return render(request, "doletters_errors.html", {})

def reply_status(request):
    try:
        empnox = Level_Desig.objects.exclude(delete_flag=True).filter(Q(official_email_ID=request.user)| Q(official_email_ID=request.user.guest_email) | Q(official_email_ID=request.user.email), empno__isnull=False)
        if empnox:
            empno = empnox[0].empno_id
            desig = empnox[0].designation_code

        else:
            pass
            # messages.error(request, 'You are not authorize to create DO letters. Please contact to admin')

        if request.method == "GET" and request.is_ajax():
            id=request.GET.get('id') 
            #print(id)   
            x=do_upload.objects.filter(Q(desig_id=desig), Q(id=id)).values('id')[0]
            status=list(do_act.objects.filter(Q(id_upload=x['id'])).values('desig_id__designation','date_of_reply', 'remarks', 'reply_path', 'status_flag'))
            
            for i in range(len(status)):
                    if status[i]['status_flag'] is False:
                        status[i].update({'status_flag':'Pending'}) 
                        status[i].update({'date_of_reply':'NA'}) 
                        status[i].update({'remarks':'NA'}) 
                        status[i].update({'reply_path':'NA'}) 
                    else:
                        date=status[i]['date_of_reply']
                        year=date[0:4]
                        month=date[5:7]
                        day=date[8:10]
                        new_date=day+"/"+month+"/"+year
                        print(new_date)
            #print(status)
            context={'status': status}
            return JsonResponse( context, safe=False)
        return JsonResponse({'sucess':False},status=400)
    except Exception as e: 
        try:
            error_Table.objects.create(fun_name="reply_status",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "doletters_errors.html", {})

def reply_view(request):
    try:
        empnox = Level_Desig.objects.exclude(delete_flag=True).filter(Q(official_email_ID=request.user)| Q(official_email_ID=request.user.guest_email) | Q(official_email_ID=request.user.email), empno__isnull=False)
        if empnox:
            empno = empnox[0].empno_id
            desig = empnox[0].designation_code

        else:
            pass
            # messages.error(request, 'You are not authorize to view DO letters. Please contact to admin')

        if request.method == "GET" and request.is_ajax():
            id=request.GET.get('id') 
            ofc=request.GET.get('ofc')
            remark=do_act.objects.filter(Q(id_upload_id=id), Q(desig_id_id=ofc)).values('remarks')[0]['remarks']
            context={'reply':remark}
            return JsonResponse( {'reply':remark}, safe=False)
        return JsonResponse({'success':False},status=400)
    except Exception as e: 
        try:
            error_Table.objects.create(fun_name="reply_view",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "doletters_errors.html", {})
# def upload_reply(request):
#     if request.method == "POST" and request.is_ajax():
#         pk=request.POST.get('id')
#         print(pk)
#         letter = do_act.objects.filter(id=pk).values('id_upload')
#         print(letter)
#         # empnox = Level_Desig.objects.exclude(delete_flag=True).filter(Q(official_email_ID=request.user) | Q(official_email_ID=request.user.email), empno__isnull=False)
#         # if empnox:
#         #     empno = empnox[0].empno_id
#         #     desig = empnox[0].designation_code

#         # else:
#         #     messages.error(request, 'You are not authorize to view DO letters. Please contact admin')
        
       
#         #if request.method == 'POST':
#         remark=request.POST.get('remarks')
#         #reply_file=request.FILES('reply_file')
#         print(remark)
#         #     x = do_act.objects.filter(Q(id_upload=letter), Q(desig_id=desig)).update(remarks = remark)
#         #     x = do_act.objects.filter(Q(id_upload=letter), Q(desig_id=desig)).update(status_flag = True)
#         #     x = do_act.objects.filter(Q(id_upload=letter), Q(desig_id=desig)).update(date_of_reply = date.today())
#         #     if reply_file:
#         #          x = do_act.objects.filter(Q(id_upload=letter), Q(desig_id=desig)).update(reply_path = reply_file)
#         # values={'remarks':remark, 'reply_file': reply_file}
#         return JsonResponse(values, safe=False)
#     return JsonResponse({'success':False},status=400)


def view_all(request):
    try:
        empnox = Level_Desig.objects.exclude(delete_flag=True).filter(Q(official_email_ID=request.user)| Q(official_email_ID=request.user.guest_email) | Q(official_email_ID=request.user.email), empno__isnull=False)
        if empnox:
            empno = empnox[0].empno_id
            desig = empnox[0].designation_code

        else:
            pass
            # messages.error(request, 'You are not authorize to create DO letters. Please contact to admin')
            
        letters=list(do_upload.objects.filter(Q(desig_id=desig)).values())
        
        officers=Level_Desig.objects.exclude(delete_flag=True).filter().values('designation', 'designation_code') 
        if letters:
            for i in range(len(letters)):
                actions=[]
                x = do_act.objects.filter(id_upload= letters[i]['id']).values('desig_id__designation')
                #print(x)
                if x.count()==0:
                    letters[i].update({'desig_id':'NA'})   
                else:
                    for j in x:
                        actions.append(j['desig_id__designation'])

                    letters[i].update({'desig_id':actions})
                    # letters[i].update({'desig_id':x[0]['desig_id__designation']})
                    # x = do_act.objects.filter(id_upload= letters[i]['id']).values('status_flag')
                    if letters[i]['status_flag'] ==0:
                        letters[i].update({'status_flag':'Pending'})
                        letters[i].update({'date_of_reply':'NA'})
                        letters[i].update({'remarks':'NA'})
                        letters[i].update({'reply_path':'NA'})
                    else:
                        letters[i].update({'status_flag':'Replied'})
                        x = do_act.objects.filter(id_upload= letters[i]['id']).values('date_of_reply')
                        date=x[0]['date_of_reply']
                        year=date.year
                        month=date.month
                        day=date.day
                        new_date=str(day)+"/"+str(month)+"/"+str(year)
                        letters[i].update({'date_of_reply':new_date})
                        x = do_act.objects.filter(id_upload= letters[i]['id']).values('remarks')
                        letters[i].update({'remarks':x[0]['remarks']})
                        x = do_act.objects.filter(id_upload= letters[i]['id']).values('reply_path')
                        letters[i].update({'reply_path':x[0]['reply_path']})
            context={'letters': letters, 'officers': officers}
        else:        
            context={'officers':officers}

            
            #############  MODAL UPLOAD ##################
        
        if request.method == 'POST':  
                do_letter_no=request.POST.get('do_letter_no')
                date=request.POST.get('date')
                subject=request.POST.get('subject')
                action_by= request.POST.get('action_by_test')
                marked_officers=action_by.split(',')
                #print(marked_officers)
                do_file=request.FILES['do_file']
                if len(marked_officers[0])>0:
                    values=do_upload.objects.create( created_by_id = empno, desig_id_id= desig, status_flag=4, do_letter_no = do_letter_no,  do_letter_date=date, subject=subject, do_path= do_file, delete_flag=0 )
                    for i in marked_officers:
                        #print(i)
                        marked_officers_list = Level_Desig.objects.exclude(delete_flag=True).get(designation=i)
                        #print(marked_officers_list)
                        marked_officers_id= empmast.objects.get(empno=(Level_Desig.objects.exclude(delete_flag=True).filter(Q(designation = i)).values('empno'))[0]['empno'])
                        #print(marked_officers_id)
                        action= do_act.objects.create(id_upload=values, desig_id=marked_officers_list, status_flag=False,  emp_no = marked_officers_id )  
                else:
                    pass
                    # messages.error(request,"upload unsuccessful")

                
        return render(request, 'view_all.html', context)
    except Exception as e: 
        try:
            error_Table.objects.create(fun_name="view_all",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "doletters_errors.html", {})

def do_letter_modal_view(request):
    try:
        if request.method == "GET" and request.is_ajax():
            id=request.GET.get('id')
            empnox = Level_Desig.objects.exclude(delete_flag=True).filter(Q(official_email_ID=request.user) | Q(official_email_ID=request.user.guest_email)| Q(official_email_ID=request.user.email), empno__isnull=False)
            if empnox:
                empno = empnox[0].empno_id
                desig = empnox[0].designation_code

            else:
                pass
                # messages.error(request, 'You are not authorize to create DO letters. Please contact to admin')
                
            letters=list(do_upload.objects.filter(Q(desig_id=desig), Q(id=id)).values())

            if letters:
                for i in range(len(letters)):
                    ############date format ################
                    date=letters[i]['do_letter_date']
                    year=date.year
                    month=date.month
                    day=date.day
                    new_date=str(day)+"/"+str(month)+"/"+str(year)
                    letters[i].update({'do_letter_date':new_date})
                    actions=[]
                    x = do_act.objects.filter(id_upload= letters[i]['id']).values('desig_id__designation')
                    #print(x)
                    if x.count()==0:
                        letters[i].update({'desig_id':'NA'})   
                    else:
                        for j in x:
                            actions.append(j['desig_id__designation'])

                    letters[i].update({'desig_id':actions})
                    # letters[i].update({'desig_id':x[0]['desig_id__designation']})

                    # x = do_act.objects.filter(id_upload= letters[i]['id']).values('status_flag')
                    if letters[i]['status_flag'] ==0:
                        letters[i].update({'status_flag':'Pending'}) 
                        letters[i].update({'date_of_reply':'NA'}) 
                        letters[i].update({'remarks':'NA'}) 
                        letters[i].update({'reply_path':'NA'}) 
                    else:
                        letters[i].update({'status_flag':'Replied'}) 
                        x = do_act.objects.filter(id_upload= letters[i]['id']).values('date_of_reply')
                        date=x[0]['date_of_reply']
                        year=date.year
                        month=date.month
                        day=date.day
                        new_date=str(day)+"/"+str(month)+"/"+str(year)
                        letters[i].update({'date_of_reply':new_date})
                        # letters[i].update({'date_of_reply':x[0]['date_of_reply']})
                        x = do_act.objects.filter(id_upload= letters[i]['id']).values('remarks')
                        letters[i].update({'remarks':x[0]['remarks']})
                        x = do_act.objects.filter(id_upload= letters[i]['id']).values('reply_path')
                        letters[i].update({'reply_path':x[0]['reply_path']})
                context={'letters': letters}
            else:         
                context={}
            return JsonResponse(context, safe=False)
        return JsonResponse({'sucess':False},status=400) 
    except Exception as e: 
        try:
            error_Table.objects.create(fun_name="do_letter_modal_view",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "doletters_errors.html", {})

def view_ajax(request):
    try:
        if request.method == "GET" and request.is_ajax():
            id=request.GET.get('id')
            elements=list(do_upload.objects.filter(Q(id=id)).values())
            status=list(do_act.objects.filter(Q(id_upload=id)).values('desig_id__designation','date_of_reply', 'remarks', 'reply_path', 'status_flag'))
            for i in range(len(status)):
                    if status[i]['status_flag'] is False:
                        status[i].update({'status_flag':'Pending'}) 
                        status[i].update({'date_of_reply':'NA'}) 
                        status[i].update({'remarks':'NA'}) 
                        status[i].update({'reply_path':'NA'}) 
            
            #print(elements)
            if elements:
                for i in range(len(elements)):
                    date=elements[i]['do_letter_date']
                    year=date.year
                    month=date.month
                    day=date.day
                    new_date=str(day)+"/"+str(month)+"/"+str(year)
                    elements[i].update({'do_letter_date':new_date})
                    x = do_act.objects.filter(id_upload= elements[i]['id']).values('desig_id__designation')
                    elements[i].update({'desig_id':x[0]['desig_id__designation']})

                    
                    x = do_act.objects.filter(id_upload= elements[i]['id']).values('status_flag')
                    if x[0]['status_flag'] is False:
                        elements[i].update({'status_flag':'Pending'}) 
                        elements[i].update({'date_of_reply':'NA'}) 
                        elements[i].update({'remarks':'NA'}) 
                        elements[i].update({'reply_path':'NA'}) 
                    else:
                        elements[i].update({'status_flag':'Replied'}) 
                        x = do_act.objects.filter(id_upload= elements[i]['id']).values('date_of_reply')
                        date=x[0]['date_of_reply']
                        year=date.year
                        month=date.month
                        day=date.day
                        new_date=str(day)+"/"+str(month)+"/"+str(year)
                    
                        elements[i].update({'date_of_reply':new_date})
                        x = do_act.objects.filter(id_upload= elements[i]['id']).values('remarks')
                        elements[i].update({'remarks':x[0]['remarks']})
                        x = do_act.objects.filter(id_upload= elements[i]['id']).values('reply_path')
                        elements[i].update({'reply_path':x[0]['reply_path']})
                #print(elements)
                xyz=''
                xy = do_copy.objects.filter(do_upload= id).values('desig_id__designation')
                if xy.count()>0:
                    for i in xy:
                        if len(xyz) > 0:
                            xyz += ', '
                        xyz += i['desig_id__designation']

                return JsonResponse({'copyto':xyz, 'id':id, 'do_letter_no': elements[0]['do_letter_no'], 'do_letter_date': elements[0]['do_letter_date'], 'subject': elements[0]['subject'], 'reply_date': elements[0]['date_of_reply'], 'remarks':elements[0]['remarks'], 'attachment':elements[0]['reply_path'], 'do_file':elements[0]['do_path'], 'status':status,'do_text':elements[0]['do_text'] },safe=False)
        return JsonResponse({'sucess':False},status=400)
    except Exception as e: 
        try:
            error_Table.objects.create(fun_name="view_ajax",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "doletters_errors.html", {})


def view_ajax2(request):
    try:
    
        if request.method == "GET" and request.is_ajax():
            id=request.GET.get('id')
            elements=list(do_upload.objects.filter(Q(id=id)).values())
            status=list(do_act.objects.filter(Q(id_upload=id)).values('desig_id__designation','date_of_reply', 'remarks', 'reply_path', 'status_flag'))
            for i in range(len(status)):
                    if status[i]['status_flag'] is False:
                        status[i].update({'status_flag':'Pending'}) 
                        status[i].update({'date_of_reply':'NA'}) 
                        status[i].update({'remarks':'NA'}) 
                        status[i].update({'reply_path':'NA'}) 
                    else:
                        date=status[i]['date_of_reply']
                        year=date.year
                        month=date.month
                        day=date.day
                        new_date=str(day)+"/"+str(month)+"/"+str(year)
                        status[i].update({'date_of_reply': new_date})

            
            #print(status)
            if elements:
                for i in range(len(elements)):
                    date=elements[i]['do_letter_date']
                    year=date.year
                    month=date.month
                    day=date.day
                    new_date=str(day)+"/"+str(month)+"/"+str(year)
                    elements[i].update({'do_letter_date':new_date})
                    x = do_act.objects.filter(id_upload= elements[i]['id']).values('desig_id__designation')
                    elements[i].update({'desig_id':x[0]['desig_id__designation']})
                    x = do_act.objects.filter(id_upload= elements[i]['id']).values('status_flag')
                    if x[0]['status_flag'] is False:
                        elements[i].update({'status_flag':'Pending'}) 
                        elements[i].update({'date_of_reply':'NA'}) 
                        elements[i].update({'remarks':'NA'}) 
                        elements[i].update({'reply_path':'NA'}) 
                    else:
                        elements[i].update({'status_flag':'Replied'}) 
                        x = do_act.objects.filter(id_upload= elements[i]['id']).values('date_of_reply')
                        date=x[0]['date_of_reply']
                        year=date.year
                        month=date.month
                        day=date.day
                        new_date=str(day)+"/"+str(month)+"/"+str(year)
                        elements[i].update({'date_of_reply':new_date})
                        x = do_act.objects.filter(id_upload= elements[i]['id']).values('remarks')
                        elements[i].update({'remarks':x[0]['remarks']})
                        x = do_act.objects.filter(id_upload= elements[i]['id']).values('reply_path')
                        elements[i].update({'reply_path':x[0]['reply_path']})
                #print(elements)
                letters=list(do_upload.objects.filter(id=id).values())
                if letters:
                    for i in range(len(letters)):
                        date=letters[i]['do_letter_date']
                        year=date.year
                        month=date.month
                        day=date.day
                        new_date=str(day)+"/"+str(month)+"/"+str(year)
                        letters[i].update({'do_letter_date':new_date})  
                        #letters[i].update({'created_by_id':letters[i]['desig_id__designation']}) 
                        actions=[]
                        status=[]
                        x = do_act.objects.filter(id_upload= letters[i]['id']).values('desig_id__designation','desig_id')
                        for j in x:
                            y = do_act.objects.filter(id_upload= letters[i]['id'], desig_id=j['desig_id']).values('status_flag','remarks','reply_path','date_of_reply')
                            date=y[0]['date_of_reply']
                            year=date.year
                            month=date.month
                            day=date.day
                            new_date=str(day)+"/"+str(month)+"/"+str(year)
                            status.append({'xyz':j['desig_id__designation'],'abc':y[0]['status_flag'] , 'ofc':j['desig_id'],'remarks':y[0]['remarks'],'reply_path':y[0]['reply_path'],'date':new_date})
                            
                        letters[i].update({'marked_to':status})
                        print(letters)
                return JsonResponse({'do_text':elements[0]['do_text'],'letters':letters,'id':id, 'do_letter_no': elements[0]['do_letter_no'], 'do_letter_date': elements[0]['do_letter_date'], 'subject': elements[0]['subject'], 'reply_date': elements[0]['date_of_reply'], 'remarks':elements[0]['remarks'], 'attachment':elements[0]['reply_path'], 'do_file':elements[0]['do_path'], 'status': status },safe=False)
        return JsonResponse({'sucess':False},status=400)
    except Exception as e: 
        try:
            error_Table.objects.create(fun_name="view_ajax2",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "doletters_errors.html", {})

def view2(request):
    try:
        empnox = Level_Desig.objects.exclude(delete_flag=True).filter(Q(official_email_ID=request.user)| Q(official_email_ID=request.user.guest_email) | Q(official_email_ID=request.user.email), empno__isnull=False)
        if empnox:
            empno = empnox[0].empno_id
            desig = empnox[0].designation_code

        else:
            pass
            # messages.error(request, 'You are not authorize to view DO letters. Please contact admin')

        letters=list(do_upload.objects.filter(Q(desig_id=desig)).values())
        
        
        officers=Level_Desig.objects.exclude(delete_flag=True).filter().values('designation', 'designation_code') 
        
        if letters:
            for i in range(len(letters)):
                date=letters[i]['do_letter_date']
                year=date.year
                month=date.month
                day=date.day
                new_date=str(day)+"/"+str(month)+"/"+str(year)
                letters[i].update({'do_letter_date':new_date})   
                actions=[]
                status=[]
                x = do_act.objects.filter(id_upload= letters[i]['id']).values('desig_id__designation')
                y = do_act.objects.filter(id_upload= letters[i]['id']).values('status_flag')
                if y.count()==0:   
                    letters[i].update({'status_flag':'NA'})
                else:
                    for j in y:     
                        status.append(j['status_flag'])
                f=False
                if f not in status:
                    y=do_upload.objects.filter(id=letters[i]['id']).update(status_flag=1)
                

                if x.count()==0:   
                    letters[i].update({'desig_id':'NA'})
                else:
                    for j in x:     
                        actions.append(j['desig_id__designation'])

                    #letters[i].update({'desig_id':actions})
                    letters[i].update({'desig_id':' '.join(str(x) for x in actions)})
                    # letters[i].update({'desig_id':x[0]['desig_id__designation']})
                    # x = do_act.objects.filter(id_upload= letters[i]['id']).values('status_flag')
                    if letters[i]['status_flag'] == 4:
                        letters[i].update({'status_flag':'Pending'})
                        letters[i].update({'date_of_reply':'NA'})
                        letters[i].update({'remarks':'NA'})
                        letters[i].update({'reply_path':'NA'})
                    else:
                        letters[i].update({'status_flag':'Replied'})
                        x = do_act.objects.filter(id_upload= letters[i]['id']).values('date_of_reply')
                        date=x[0]['date_of_reply']
                        year=date.year
                        month=date.month
                        day=date.day
                        new_date=str(day)+"/"+str(month)+"/"+str(year)
                        letters[i].update({'date_of_reply':new_date})
                        x = do_act.objects.filter(id_upload= letters[i]['id']).values('remarks')
                        letters[i].update({'remarks':x[0]['remarks']})
                        x = do_act.objects.filter(id_upload= letters[i]['id']).values('reply_path')
                        letters[i].update({'reply_path':x[0]['reply_path']})
            context={'letters': letters, 'officers': officers}
        
        else:        
            context={'officers':officers}
            
    
        return render(request, 'view2.html', context)
    except Exception as e: 
        try:
            error_Table.objects.create(fun_name="view2",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "doletters_errors.html", {})


# def letters_marked(request):
#     try:
#         empnox = Level_Desig.objects.exclude(delete_flag=True).filter(Q(official_email_ID=request.user) | Q(official_email_ID=request.user.email), empno__isnull=False)
#         if empnox:
#             empno = empnox[0].empno_id
#             desig = empnox[0].designation_code

#         else:
#             messages.error(request, 'You are not authorize to view DO letters. Please contact admin')

#     ################################################################# UPLOAD REPLY #########################################################################
#         if request.method == 'POST':
            
#             remarks=request.POST.get('remarks')
#             reply_id=request.POST.get('reply_id')
#             filename1=request.POST.get('reply_file')
#             letter = do_act.objects.filter(id=reply_id).values('id_upload')[0]['id_upload']
#             x = do_act.objects.filter(Q(id_upload=letter), Q(desig_id=desig)).update(remarks = remarks)
#             x = do_act.objects.filter(Q(id_upload=letter), Q(desig_id=desig)).update(status_flag = True)
#             x = do_act.objects.filter(Q(id_upload=letter), Q(desig_id=desig)).update(date_of_reply = datetime.today())
#             if filename1!='':
#                 file=request.FILES['reply_file']
#                 x = do_act.objects.filter(Q(id_upload=letter), Q(desig_id=desig))[0]
#                 x.reply_path = file
#                 x.save()
#             #print(remarks, reply_id)

#         letters=list(do_act.objects.filter(Q(desig_id=desig)).values())
    
#         # print(letters)
#         if letters:
#             for i in range(len(letters)):
#                 date=letters[i]['date_of_reply']
#                 year=date.year
#                 month=date.month
#                 day=date.day
#                 new_date=str(day)+"/"+str(month)+"/"+str(year)
#                 letters[i].update({'date_of_reply':new_date})
#                 x=do_upload.objects.filter(id=letters[i]['id_upload_id']).values('desig_id__designation', 'do_letter_no', 'do_letter_date', 'do_path')
#                 letters[i].update({'rcvd_from':x[0]['desig_id__designation']})
#                 letters[i].update({'do_letter_no':x[0]['do_letter_no']})
#                 date=x[0]['do_letter_date']
#                 year=date.year
#                 month=date.month
#                 day=date.day
#                 new_date=str(day)+"/"+str(month)+"/"+str(year)
#                 letters[i].update({'do_letter_date': new_date})
#                 letters[i].update({'do_path':x[0]['do_path']})
#                 #print(letters[i])

#         context={'letters':letters}
#         return render(request, 'letters_marked.html', context)

#     ################################################################# UPLOAD REPLY #########################################################################
#         if request.method == 'POST':
            
#             remarks=request.POST.get('remarks')
#             reply_id=request.POST.get('reply_id')
#             file=request.POST.get('reply_file')
            
#             letter = do_act.objects.filter(id=reply_id).values('id_upload')[0]['id_upload']
#             x = do_act.objects.filter(Q(id_upload=letter), Q(desig_id=desig)).update(remarks = remarks)
#             x = do_act.objects.filter(Q(id_upload=letter), Q(desig_id=desig)).update(status_flag = True)
#             x = do_act.objects.filter(Q(id_upload=letter), Q(desig_id=desig)).update(date_of_reply = datetime.today())
#             if file:
#                 reply_file=request.FILES['reply_file']
#                 x = do_act.objects.filter(Q(id_upload=letter), Q(desig_id=desig)).update(reply_path = reply_file)

#             #print(remarks, reply_id)

#         letters=list(do_act.objects.filter(Q(desig_id=desig)).values())
    
#         # print(letters)
#         if letters:
#             for i in range(len(letters)):
#                 date=letters[i]['date_of_reply']
#                 year=date.year
#                 month=date.month
#                 day=date.day
#                 new_date=str(day)+"/"+str(month)+"/"+str(year)
#                 letters[i].update({'date_of_reply':new_date})
#                 x=do_upload.objects.filter(id=letters[i]['id_upload_id']).values('desig_id__designation', 'do_letter_no', 'do_letter_date', 'do_path')
#                 letters[i].update({'rcvd_from':x[0]['desig_id__designation']})
#                 letters[i].update({'do_letter_no':x[0]['do_letter_no']})
#                 date=x[0]['do_letter_date']
#                 year=date.year
#                 month=date.month
#                 day=date.day
#                 new_date=str(day)+"/"+str(month)+"/"+str(year)
#                 letters[i].update({'do_letter_date': new_date})
#                 letters[i].update({'do_path':x[0]['do_path']})
#                 #print(letters[i])

        
                


#         context={'letters':letters}
#         return render(request, 'letters_marked.html', context)
#     except Exception as e: 
#         try:
#             error_Table.objects.create(fun_name="letters_marked",user_id=request.user,err_details=str(e))
#         except:
#             print("Internal Error!!!")
#         return render(request, "doletters_errors.html", {})


def letters_marked(request):
    try:
        empnox = Level_Desig.objects.exclude(delete_flag=True).filter(Q(official_email_ID=request.user)| Q(official_email_ID=request.user.guest_email) | Q(official_email_ID=request.user.email), empno__isnull=False)
        if empnox:
            empno = empnox[0].empno_id
            desig = empnox[0].designation_code

        else:
            pass
            # messages.error(request, 'You are not authorize to view DO letters. Please contact admin')

    ################################################################# UPLOAD REPLY #########################################################################
        if request.method == 'POST':
            remarks=request.POST.get('remarks')
            reply_id=request.POST.get('reply_id')
            # filename1=request.POST.get('reply_file')
            description=request.POST.get('description')
            print('description',description)
            if description=='Noted':
                filename1=''
            else:
                filename1=request.POST.get('reply_file')  
            letter = do_act.objects.filter(id=reply_id).values('id_upload')[0]['id_upload']
            x = do_act.objects.filter(Q(id_upload=letter), Q(desig_id=desig)).update(remarks = remarks)
            x = do_act.objects.filter(Q(id_upload=letter), Q(desig_id=desig)).update(status_flag = True)
            x = do_act.objects.filter(Q(id_upload=letter), Q(desig_id=desig)).update(date_of_reply = datetime.today())
            if filename1!='':
                file=request.FILES['reply_file']
                x = do_act.objects.filter(Q(id_upload=letter), Q(desig_id=desig))[0]
                x.reply_path = file
                x.save()
            #print(remarks, reply_id)

        letters=list(do_act.objects.filter(Q(desig_id=desig)).values())
    
        # print(letters)
        if letters:
            for i in range(len(letters)):
                date=letters[i]['date_of_reply']
                year=date.year
                month=date.month
                day=date.day
                new_date=str(day)+"/"+str(month)+"/"+str(year)
                letters[i].update({'date_of_reply':new_date})
                x=do_upload.objects.filter(id=letters[i]['id_upload_id']).values('desig_id__designation', 'do_letter_no', 'do_letter_date', 'do_path')
                letters[i].update({'rcvd_from':x[0]['desig_id__designation']})
                letters[i].update({'do_letter_no':x[0]['do_letter_no']})
                date=x[0]['do_letter_date']
                year=date.year
                month=date.month
                day=date.day
                new_date=str(day)+"/"+str(month)+"/"+str(year)
                letters[i].update({'do_letter_date': new_date})
                letters[i].update({'do_path':x[0]['do_path']})
                #print(letters[i])

        context={'letters':letters}
        return render(request, 'letters_marked.html', context)

    ################################################################# UPLOAD REPLY #########################################################################
        if request.method == 'POST':
            remarks=request.POST.get('remarks')
            reply_id=request.POST.get('reply_id')
            description=request.POST.get('description')
            print('description',description)
            if description=='Noted':
                file=''
            else:
                
                file=request.FILES['reply_file']    

            
            letter = do_act.objects.filter(id=reply_id).values('id_upload')[0]['id_upload']
            x = do_act.objects.filter(Q(id_upload=letter), Q(desig_id=desig)).update(remarks = remarks)
            x = do_act.objects.filter(Q(id_upload=letter), Q(desig_id=desig)).update(status_flag = True)
            x = do_act.objects.filter(Q(id_upload=letter), Q(desig_id=desig)).update(date_of_reply = datetime.today())
            if file:
                reply_file=request.FILES['reply_file']
                x = do_act.objects.filter(Q(id_upload=letter), Q(desig_id=desig)).update(reply_path = reply_file)

            #print(remarks, reply_id)

        letters=list(do_act.objects.filter(Q(desig_id=desig)).values())
    
        # print(letters)
        if letters:
            for i in range(len(letters)):
                date=letters[i]['date_of_reply']
                year=date.year
                month=date.month
                day=date.day
                new_date=str(day)+"/"+str(month)+"/"+str(year)
                letters[i].update({'date_of_reply':new_date})
                x=do_upload.objects.filter(id=letters[i]['id_upload_id']).values('desig_id__designation', 'do_letter_no', 'do_letter_date', 'do_path')
                letters[i].update({'rcvd_from':x[0]['desig_id__designation']})
                letters[i].update({'do_letter_no':x[0]['do_letter_no']})
                date=x[0]['do_letter_date']
                year=date.year
                month=date.month
                day=date.day
                new_date=str(day)+"/"+str(month)+"/"+str(year)
                letters[i].update({'do_letter_date': new_date})
                letters[i].update({'do_path':x[0]['do_path']})
                #print(letters[i])

        
                


        context={'letters':letters}
        return render(request, 'letters_marked.html', context)
    except Exception as e: 
        try:
            error_Table.objects.create(fun_name="letters_marked",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "doletters_errors.html", {})






def do_details_ajax(request):
    try:
        if request.method == "GET" and request.is_ajax():
            reply_id=request.GET.get('reply_id')
            upload_id=request.GET.get('upload_id')
            elements=list(do_upload.objects.filter(Q(id=upload_id)).values())
            for i in range (len(elements)):
            # print(elements[i])
                date=elements[i]['do_letter_date']
                year=date.year
                month=date.month
                day=date.day
                new_date=str(day)+"/"+str(month)+"/"+str(year)
                elements[i].update({'do_letter_date': new_date})
            status = list(do_act.objects.filter(Q(id=reply_id, id_upload_id=upload_id)).values())
            #print(status[0]['status_flag'])
            if status[0]['status_flag'] is False:
                status[0]['remarks']='Pending Reply'
                status[0]['date_of_reply']=''
            else:
                date=status[0]['date_of_reply']
                year=date.year
                month=date.month
                day=date.day
                new_date=str(day)+"/"+str(month)+"/"+str(year)
                status[0].update({'date_of_reply': new_date})

            context={'elements' : elements[0], 'status' : status[0]}
            return JsonResponse(context, safe=False)
        return JsonResponse({'sucess':False},status=400)
    except Exception as e: 
        try:
            error_Table.objects.create(fun_name="do_details_ajax",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "doletters_errors.html", {})



from django.views.decorators.clickjacking import xframe_options_exempt

@xframe_options_exempt
def indextest(request):
    try:
        context = {'src':"IMG_0001.pdf"}
        return render(request,'testiframe.html',context)
    except Exception as e: 
        try:
            error_Table.objects.create(fun_name="indextest",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "doletters_errors.html", {})

def view_previous(request):
    try:
        empnox = Level_Desig.objects.exclude(delete_flag=True).filter(Q(official_email_ID=request.user)| Q(official_email_ID=request.user.guest_email) | Q(official_email_ID=request.user.email), empno__isnull=False)
        if empnox:
            empno = empnox[0].empno_id
            desig = empnox[0].designation_code

        else:
            pass
            # messages.error(request, 'You are not authorize to view DO letters. Please contact admin')
        
        officers=Level_Desig.objects.exclude(delete_flag=True).filter().values('designation', 'designation_code') 

        letters=list(do_upload.objects.filter(Q(desig_id=desig)).values().order_by('-do_letter_date'))
        if letters:
            for i in range(len(letters)):
                date=letters[i]['do_letter_date']
                year=date.year
                month=date.month
                day=date.day
                new_date=str(day)+"/"+str(month)+"/"+str(year)
                letters[i].update({'do_letter_date':new_date})   
                actions=[]
                status=[]
                x = do_act.objects.filter(id_upload= letters[i]['id']).values('desig_id__designation','desig_id')
                for j in x:
                    y = do_act.objects.filter(id_upload= letters[i]['id'], desig_id=j['desig_id']).values('status_flag')
                    status.append({'xyz':j['desig_id__designation'],'abc':y[0]['status_flag'] , 'ofc':j['desig_id']})
                    
                letters[i].update({'marked_to':status})
                # print(letters[i])
        

        ########################################################### SEARCH PART ###############################################################################
        if request.method == 'POST':  
                date_range=request.POST.get('date_range')
                subject=request.POST.get('subject')
                action_by= request.POST.get('action_by_test')
                marked_officers=action_by.split(',')
                
                uploads=[]
                subjects=[]

                #marked to filter:
                if action_by:
                    marks=list(do_act.objects.filter(desig_id_id__in=marked_officers).values('id_upload'))
                    for m in marks:
                        uploads.append(m['id_upload'])
                else:
                    marks=list(do_act.objects.filter().values('id_upload'))
                    for m in marks:
                        uploads.append(m['id_upload'])

                #subject filter:
                if subject:
                    # subjects.append(subject)
                    # print(subjects)
                    subject=list(do_upload.objects.filter(subject__icontains=subject).values('subject'))
                    for s in subject:
                        subjects.append(s['subject'])
                else:
                    subject=list(do_upload.objects.filter(Q(desig_id=desig)).values('subject'))
                    for s in subject:
                        subjects.append(s['subject'])
                    print(subjects)

                #date range filter:
                if date_range:
                    sp_date = date_range.split('-')
                    start  = datetime.strptime(sp_date[0].strip(),"%d/%m/%Y").strftime("%Y-%m-%d")
                    end  = datetime.strptime(sp_date[1].strip(),"%d/%m/%Y").strftime("%Y-%m-%d")
                    print(start, end)
                    letters=list(do_upload.objects.filter(Q(desig_id=desig), Q(subject__in=subjects) , Q(do_letter_date__gte=start) , Q(do_letter_date__lte=end) , Q(id__in=uploads)  ).values()) 
                else:
                    letters=list(do_upload.objects.filter(Q(desig_id=desig), Q(id__in=uploads) , Q(subject__in=subjects) ).values())
                    
                if letters:
                    for i in range(len(letters)):
                        date=letters[i]['do_letter_date']
                        year=date.year
                        month=date.month
                        day=date.day
                        new_date=str(day)+"/"+str(month)+"/"+str(year)
                        letters[i].update({'do_letter_date':new_date}) 
                        actions=[]
                        status=[]
                        x = do_act.objects.filter(id_upload= letters[i]['id']).values('desig_id__designation','desig_id')
                        for j in x:
                            y = do_act.objects.filter(id_upload= letters[i]['id'], desig_id=j['desig_id']).values('status_flag')
                            status.append({'xyz':j['desig_id__designation'],'abc':y[0]['status_flag'] , 'ofc':j['desig_id']})
                        letters[i].update({'marked_to':status})
        context={'letters':letters, 'officers':officers}

        return render(request,'view_previous.html', context)
    except Exception as e: 
        try:
            error_Table.objects.create(fun_name="view_previous",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "doletters_errors.html", {})

def do_pdf_create(request,id):
    try:
        data=do_upload.objects.filter(id=id).all()
        name=''
        if data[0].created_by.empname is not None:
            name+=data[0].created_by.empname

        if data[0].created_by.empmname is not None:
            name+=' '+data[0].created_by.empmname

        if data[0].created_by.emplname is not None:
            name+=' '+data[0].created_by.emplname
        desig=data[0].desig_id.designation
        location=data[0].created_by.currentunitdivision
        station=data[0].created_by.station_des

        
        # data1=do_act.objects.filter(id_upload=35).all()
        context={
            'data':data,
            'name':name,
            'desig':desig,
            'data1':data,
            'location':location,
            'station':station,
        }
        return render_to_pdf('do_ReportPdf.html', context)
    except Exception as e: 
        try:
            error_Table.objects.create(fun_name="do_ReportPdf",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "doletters_errors.html", {})

def do_dashboard(request):
    try:
        empnox = Level_Desig.objects.exclude(delete_flag=True).filter(Q(official_email_ID=request.user)| Q(official_email_ID=request.user.guest_email) | Q(official_email_ID=request.user.email), empno__isnull=False)
        if empnox:
            empno = empnox[0].empno_id
            desig = empnox[0].designation_code

        else:
            messages.error(request, 'You are not authorize to view DO letters. Please contact admin')
        
        officers=Level_Desig.objects.exclude(delete_flag=True).filter().values('designation', 'designation_code') 

        letters=list(do_upload.objects.filter(Q(desig_id=desig)).values().order_by('-do_letter_date'))

        # query for date cards
        today=0
        prev11=0
        prev2=0
        prev3=0
        prev4=0
        letter_yesterday= 0
        letter_week = 0
        letter_month = 0
        letter_year = 0
        from datetime import timedelta,date
        from dateutil.relativedelta import relativedelta
        if letters:
            for i in range(len(letters)):
                date=letters[i]['do_letter_date']
                today = date.today()
                prev11 = today - timedelta(days=1)
                prev2 =  today - timedelta(days=7)
                prev3 = today - relativedelta(months=1)
                prev4 = today - relativedelta(year=1)

                if letters[i]['do_letter_date'] == prev11:
                    letter_yesterday+=1
                if letters[i]['do_letter_date'] >= prev2:
                    letter_week+=1
                if letters[i]['do_letter_date'] >= prev3:
                    letter_month+=1
                if letters[i]['do_letter_date'] >= prev4:
                    letter_year+=1

                year=date.year
                month=date.month
                day=date.day
                new_date=str(day)+"/"+str(month)+"/"+str(year)
                letters[i].update({'do_letter_date':new_date})  
                
                    
                actions=[]
                status=[]
                x = do_act.objects.filter(id_upload= letters[i]['id']).values('desig_id__designation','desig_id')
                for j in x:
                    y = do_act.objects.filter(id_upload= letters[i]['id'], desig_id=j['desig_id']).values('status_flag')
                    status.append({'xyz':j['desig_id__designation'],'abc':y[0]['status_flag'] , 'ofc':j['desig_id']})
                    
                letters[i].update({'marked_to':status})
                # print(letters[i])
        

        empnox = Level_Desig.objects.exclude(delete_flag=True).filter(Q(official_email_ID=request.user)| Q(official_email_ID=request.user.guest_email) | Q(official_email_ID=request.user.email), empno__isnull=False)
        if empnox:
            empno = empnox[0].empno_id
            desig = empnox[0].designation_code
    
        else:
            pass
            # messages.error(request, 'You are not authorize to create DO letters. Please contact to admin')
            
        officers=Level_Desig.objects.exclude(delete_flag=True).filter().values('designation', 'designation_code')
    
        if request.method == 'POST':  
            print("inside do")
            do_letter_no=request.POST.get('do_letter_no')
            date111=request.POST.get('date')
            print(do_letter_no,date111)
            if date111:
                new_date = datetime.strptime(date111, '%d-%m-%y').strftime('%Y-%m-%d')
            subject=request.POST.get('subject')
            action_by2= request.POST.get('action_by_test2')
            copy_to= request.POST.get('copy_to_test')
            do_text=request.POST.get('do_text')
            print("copy_to_test",copy_to)
            if action_by2:
                print("action_by",action_by2)
                marked_officers=action_by2.split(',')
                if copy_to:
                    copy_to=copy_to.split(',')
                else:
                    copy_to = []
                if len(do_text)>0:
                    do_file=None
                else:
                    do_text=None
                    do_file=request.FILES['do_file']
                if len(marked_officers[0])>0:
                    print("dfnvjfvb")
                    values=do_upload.objects.create(do_text=do_text, created_by_id = empno, desig_id_id= desig, status_flag=4, do_letter_no = do_letter_no,  do_letter_date=new_date, subject=subject, do_path= do_file, delete_flag=0 )
                    for i in marked_officers:
                        marked_officers_list = Level_Desig.objects.exclude(delete_flag=True).get(designation=i)
                        print("i",i)
                        marked_officers_id= m1.empmast.objects.get(empno=(Level_Desig.objects.exclude(delete_flag=True).filter(Q(designation = i)).values('empno'))[0]['empno'])
                        print("marked_officers_id",marked_officers_id)
                        action= do_act.objects.create(id_upload=values, desig_id=marked_officers_list, status_flag=False,  emp_no = marked_officers_id )  
                        print("succcess")
                    if copy_to != ['']:
                        for i in copy_to:
                            marked_officers_list = Level_Desig.objects.exclude(delete_flag=True).get(designation=i)
                            do_copy.objects.create(do_upload=values, desig_id=marked_officers_list)  
                    else:
                        print("aaaaaaaa")

                else:
                    pass
                    # messages.error(request,"upload unsuccessful")

                
                

        ########################################################### SEARCH PART ###############################################################################
        if request.method == 'POST':  
                date_range=request.POST.get('date_range')
                subject=request.POST.get('subject')
                action_by= request.POST.get('action_by_test')
                if action_by:
                    marked_officers=action_by.split(',')
                else:
                    marked_officers=action_by
                print("ok")
                
                uploads=[]
                subjects=[]

                #marked to filter:
                if action_by:
                    marks=list(do_act.objects.filter(desig_id_id__in=marked_officers).values('id_upload'))
                    for m in marks:
                        uploads.append(m['id_upload'])
                else:
                    marks=list(do_act.objects.filter().values('id_upload'))
                    for m in marks:
                        uploads.append(m['id_upload'])

                #subject filter:
                if subject:
                    # subjects.append(subject)
                    # print(subjects)
                    subject=list(do_upload.objects.filter(subject__icontains=subject).values('subject'))
                    for s in subject:
                        subjects.append(s['subject'])
                else:
                    subject=list(do_upload.objects.filter(Q(desig_id=desig)).values('subject'))
                    for s in subject:
                        subjects.append(s['subject'])
                    print(subjects)

                #date range filter:
                if date_range:
                    sp_date = date_range.split('-')
                    start  = datetime.strptime(sp_date[0].strip(),"%d/%m/%Y").strftime("%Y-%m-%d")
                    end  = datetime.strptime(sp_date[1].strip(),"%d/%m/%Y").strftime("%Y-%m-%d")
                    print(start, end)
                    letters=list(do_upload.objects.filter(Q(desig_id=desig), Q(subject__in=subjects) , Q(do_letter_date__gte=start) , Q(do_letter_date__lte=end) , Q(id__in=uploads)  ).values()) 
                else:
                    letters=list(do_upload.objects.filter(Q(desig_id=desig), Q(id__in=uploads) , Q(subject__in=subjects) ).values())
                    
                if letters:
                    for i in range(len(letters)):
                        date=letters[i]['do_letter_date']
                        year=date.year
                        month=date.month
                        day=date.day
                        new_date=str(day)+"/"+str(month)+"/"+str(year)
                        letters[i].update({'do_letter_date':new_date}) 
                        actions=[]
                        status=[]
                        x = do_act.objects.filter(id_upload= letters[i]['id']).values('desig_id__designation','desig_id')
                        for j in x:
                            y = do_act.objects.filter(id_upload= letters[i]['id'], desig_id=j['desig_id']).values('status_flag')
                            status.append({'xyz':j['desig_id__designation'],'abc':y[0]['status_flag'] , 'ofc':j['desig_id']})
                        letters[i].update({'marked_to':status})
        
        print(today,prev11,prev2)
        context={'letters':letters, 'officers':officers,'letter_yesterday':letter_yesterday,'letter_week':letter_week,'letter_month':letter_month,'letter_year':letter_year,
        'today':today,'prev1':prev11,'prev2':prev2,'prev3':prev3,'prev4':prev4}

        return render(request,'do_dashboard.html', context)
    except Exception as e: 
        print(e)
        try:
            error_Table.objects.create(fun_name="do_dashboard",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "doletters_errors.html", {})
        
    






