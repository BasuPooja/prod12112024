from array import array
from datetime import date,datetime,timedelta
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
from home_page import models as m7
from api import models as m9
from django.db.models import Q
from django.db.models import Max, Sum
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.files.storage import FileSystemStorage
import json
from django.db.models import FloatField, IntegerField, CharField
from django.db.models.functions import Cast
from django.db.models import Sum
from decimal import *
from django.db import connections
from dateutil.relativedelta import relativedelta
from django.db.models import Max 
import requests
from requests.auth import HTTPBasicAuth

def vip_references(request):
    try:
        vip_day=m9.LogApi.objects.filter(schedular_name='devinsapi1_vip_zone_dropdown').values('dates').order_by('-dates')[0]['dates']
        vip_time=m9.LogApi.objects.filter(schedular_name='devinsapi1_vip_zone_dropdown',dates=vip_day).values('times').order_by('-times')[0]['times']
        vip_day=vip_day.strftime("%d/%m/%Y")
        viprbdata=list(m7.pendency_status_RB.objects.values('total','withdir','draftreply','withzone'))[0]
    
        vip_zone_pu_div=list(m7.pendency_status_zone_pu_div.objects.values('total','zone','div'))[0]
    
        
        vip_dir=list(m7.pendency_status_DIR.objects.order_by('unitcode').values('unitcode','pendcount12','pendcount6_12','pendcount3_6','pendcount0_3','counttotal','pendcountdir','countdraft','pendcountzone'))
        # pendcount12_sum= sum(l['pendcount12'] for l in list(m7.pendency_status_DIR.objects.filter().values('pendcount12')))
        # pendcount6_12_sum= sum(l['pendcount6_12'] for l in list(m7.pendency_status_DIR.objects.exclude(pendcount6_12__isnull=True).filter().values('pendcount6_12')))
        # pendcount3_6_sum= sum(l['pendcount3_6'] for l in list(m7.pendency_status_DIR.objects.exclude(pendcount3_6__isnull=True).filter().values('pendcount3_6')))
        # pendcount0_3_sum= sum(l['pendcount0_3'] for l in list(m7.pendency_status_DIR.objects.exclude(pendcount0_3__isnull=True).filter().values('pendcount0_3')))
        # counttotal_sum= sum(l['counttotal'] for l in list(m7.pendency_status_DIR.objects.exclude(counttotal__isnull=True).filter().values('counttotal')))
        # pendcountdir_sum= sum(l['pendcountdir'] for l in list(m7.pendency_status_DIR.objects.exclude(pendcountdir__isnull=True).filter().values('pendcountdir')))
        # countdraft_sum= sum(l['countdraft'] for l in list(m7.pendency_status_DIR.objects.exclude(countdraft__isnull=True).filter().values('countdraft')))
        # pendcountzone_sum= sum(l['pendcountzone'] for l in list(m7.pendency_status_DIR.objects.exclude(pendcountzone__isnull=True).filter().values('pendcountzone')))

        # # # print(sum_pendcount12)
        # total_dir=[{'unitcode':'Total','pendcount12':pendcount12_sum,'pendcount6_12':pendcount6_12_sum,
        # 'pendcount3_6':pendcount3_6_sum,'pendcount0_3':pendcount0_3_sum,'counttotal':counttotal_sum,'pendcountdir':pendcountdir_sum,'countdraft':countdraft_sum,'pendcountzone':pendcountzone_sum}]
        # vip_dir.append(total_dir)
        # items = m7.pendency_status_DIR.objects.all().annotate(Sum('countdraft'))
        # # print(vip_dir)
        # recv=sum(l['sint'] for l in list(m9.rail_madad_1.objects.annotate(sint=Cast('recv', IntegerField())).filter(znCode=z,period=1).values('sint')))
        vip_bm=list(m7.pendency_status_BM.objects.order_by('unitcode').values('unitcode','pendcount12','pendcount6_12','pendcount3_6','pendcount0_3','counttotal','pendcountdir','countdraft','pendcountzone'))
        # pendcount12_sum= sum(l['pendcount12'] for l in list(m7.pendency_status_BM.objects.filter().values('pendcount12')))
        # pendcount6_12_sum= sum(l['pendcount6_12'] for l in list(m7.pendency_status_BM.objects.exclude(pendcount6_12__isnull=True).filter().values('pendcount6_12')))
        # pendcount3_6_sum= sum(l['pendcount3_6'] for l in list(m7.pendency_status_BM.objects.exclude(pendcount3_6__isnull=True).filter().values('pendcount3_6')))
        # pendcount0_3_sum= sum(l['pendcount0_3'] for l in list(m7.pendency_status_BM.objects.exclude(pendcount0_3__isnull=True).filter().values('pendcount0_3')))
        # counttotal_sum= sum(l['counttotal'] for l in list(m7.pendency_status_BM.objects.exclude(counttotal__isnull=True).filter().values('counttotal')))
        # pendcountdir_sum= sum(l['pendcountdir'] for l in list(m7.pendency_status_BM.objects.exclude(pendcountdir__isnull=True).filter().values('pendcountdir')))
        # countdraft_sum= sum(l['countdraft'] for l in list(m7.pendency_status_BM.objects.exclude(countdraft__isnull=True).filter().values('countdraft')))
        # pendcountzone_sum= sum(l['pendcountzone'] for l in list(m7.pendency_status_BM.objects.exclude(pendcountzone__isnull=True).filter().values('pendcountzone')))
        # total_bm=[{'unitcode':'Total','pendcount12':pendcount12_sum,'pendcount6_12':pendcount6_12_sum,
        # 'pendcount3_6':pendcount3_6_sum,'pendcount0_3':pendcount0_3_sum,'counttotal':counttotal_sum,'pendcountdir':pendcountdir_sum,'countdraft':countdraft_sum,'pendcountzone':pendcountzone_sum}]


        ############## for graphs ##############
        dir_names=[]
        dir_count=[]
        dir_ford_rlys=[]
        dir_submitted=[]
        for i in range(len(vip_dir)):
            dir_names.append(vip_dir[i]['unitcode'])
            if vip_dir[i]['pendcountdir']:
                dir_count.append(vip_dir[i]['pendcountdir'])
            else:
                dir_count.append(0)

            if vip_dir[i]['pendcountzone']:
                dir_ford_rlys.append(vip_dir[i]['pendcountzone'])
            else:
                dir_ford_rlys.append(0)

            if vip_dir[i]['countdraft']:
                dir_submitted.append(vip_dir[i]['countdraft'])
            else:
                dir_submitted.append(0)

        bm_names=[]
        bm_count=[]
        bm_ford_rlys=[]
        bm_submitted=[]
        for i in range(len(vip_bm)):
            bm_names.append(vip_bm[i]['unitcode'])
            if vip_bm[i]['pendcountdir']:
                bm_count.append(vip_bm[i]['pendcountdir'])
            else:
                bm_count.append(0)

            if vip_bm[i]['pendcountzone']:
                bm_ford_rlys.append(vip_bm[i]['pendcountzone'])
            else:
                bm_ford_rlys.append(0)

            if vip_bm[i]['countdraft']:
                bm_submitted.append(vip_bm[i]['countdraft'])
            else:
                bm_submitted.append(0)


    
        vip_zone_div=list(m7.pendency_status_zone_div.objects.values('zoneunitcode','zonecountpend','divcountpend','pendcount12','pendcount6_12','pendcount3_6','pendcount0_3','zonecountall'))
        zones=list(m7.pendency_status_zone_div.objects.order_by('zoneunitcode').values('zoneunitcode'))
        context={
            'vip_day':vip_day,
            'vip_time':vip_time,
            'viprbdata':viprbdata,
            'vip_zone_pu_div':vip_zone_pu_div,
            'vip_bm':vip_bm,
            # 'total_bm':total_bm,
            'vip_dir':vip_dir,
            # 'total_dir':total_dir,
            'vip_zone_div':vip_zone_div,
            'dir_names':dir_names,
            'dir_count':dir_count,
            'dir_ford_rlys':dir_ford_rlys,
            'dir_submitted':dir_submitted,
            'bm_names':bm_names,
            'bm_count':bm_count,
            'bm_ford_rlys':bm_ford_rlys,
            'bm_submitted':bm_submitted,
            'zones':zones,

        }
        return render(request, 'VIPReference1.html',context)
    except Exception as e: 
        print(e)
        try:
            error_Table.objects.create(fun_name="do_dashboard",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "homepage_errors.html", {})

def getvipdata(request):
    if request.method=='GET':
        y=request.GET.get('dropd1')
        # # print('yy',y)
        if y == 'all':
            finallist=list(m7.pendency_status_zone_div.objects.values('zoneunitcode','zonecountpend','divcountpend','pendcount12','pendcount6_12','pendcount3_6','pendcount0_3','zonecountall'))
        else:
            finallist=list(m7.pendency_status_zone_div_dropdown.objects.filter(zone=y).values('zoneunitcode','zonecountpend','divcountpend','pendcount12','pendcount6_12','pendcount3_6','pendcount0_3','zonecountall'))
            for f in finallist:
                
                if "HQ" in f['zoneunitcode']:
                    # print(f)
                    f['zonecountpend']=f['divcountpend']
                    f['divcountpend']=0
        context={
        'finallist':finallist,
        }  
        return JsonResponse(context, safe=False)
    return JsonResponse({'sucess':False},status=400)

def parliament(request):
    try:
        par_day=m9.LogApi.objects.filter(schedular_name='parliament_countOfficerwiseTotal').values('dates').order_by('-dates')[0]['dates']
        par_time=m9.LogApi.objects.filter(schedular_name='parliament_countOfficerwiseTotal',dates=par_day).values('times').order_by('-times')[0]['times']
        date1 = par_day
        par_day=par_day.strftime("%d/%m/%Y")
        date2 = date1-relativedelta(days=30)
        date1 = datetime.strftime(date1,"%d/%m/%Y")
        date2 = datetime.strftime(date2,"%d/%m/%Y")
        date3 = date1+':'+date2
        # # print(date3)
        parlia_ls_rs=list(m7.parliament_count_LS_RS.objects.values('lscount','rscount','name'))
        assuranceleft,assuranceright, rule377left, rule377right, zerohourleft, zerohourright, petleft, petright, smleft, smright=0,0,0,0,0,0,0,0,0,0
        for i in range(len(parlia_ls_rs)):
            if parlia_ls_rs[i]['name']=='assurance':
                assuranceleft=parlia_ls_rs[i]['lscount']
                assuranceright=parlia_ls_rs[i]['rscount']
            elif parlia_ls_rs[i]['name']=='rule377':
                rule377left=parlia_ls_rs[i]['lscount']
                rule377right=parlia_ls_rs[i]['rscount']
            elif parlia_ls_rs[i]['name']=='zerohour':
                zerohourleft=parlia_ls_rs[i]['lscount']
                zerohourright=parlia_ls_rs[i]['rscount']
            elif parlia_ls_rs[i]['name']=='petition':
                petleft=parlia_ls_rs[i]['lscount']
                petright=parlia_ls_rs[i]['rscount']
            elif parlia_ls_rs[i]['name']=='specialmention':
                smleft=parlia_ls_rs[i]['lscount']
                smright=parlia_ls_rs[i]['rscount']  

        dir_list=list(m7.parliament_mydirectory.objects.filter().order_by('-dir_name').values('myid','dir_name'))
        bm_names_list=list(m7.parliament_myboardmember.objects.filter().order_by('-bm_name').values('bm_name'))
        
        progress_list=list(m7.parliament_progress_count.objects.values('typee','newentry','finalised','total','opnbal'))
        officerwise_dir=list(m7.parliament_officerwise_pendency_DIR.objects.values('specialmentioncount','desigcode','countzerohour','countpetition','countasur','count377')) 
        officerwise_bm=list(m7.parliament_officerwise_pendency_BM.objects.values('specialmentioncount','desigcode','countzerohour','countpetition','countasur','count377')) 
        parlia_dirwise=list(m7.parliament_DIRwise_pendency.objects.values('countspecialmention','countzerohour','countpetition','designame','countrule377','countass'))                     
        dir_names=list(m7.parliament_DIRwise_pendency.objects.filter().order_by('designame').values('designame'))
        d_names=[]
        for d in dir_names:
            if d['designame'] not in d_names:
                d_names.append(d['designame'])
        # # print(d_names)
        for d in dir_list:
            if d['dir_name'] not in d_names:
                parlia_dirwise.append({'countspecialmention':0,'countzerohour':0,'countpetition':0,'designame':d['dir_name'],'countrule377':0,'countass':0})
        parlia_bmwise=list(m7.parliament_BMwise_pendency.objects.values('countspecialmention','countzerohour','countpetition','designame','countrule377','countass'))   
        
    ########### graph of board member
        graph_bm_wise_x=[]
        graph_bm_wise_countass=[]
        graph_bm_wise_countspecialmention=[]
        graph_bm_wise_countzerohour=[]
        graph_bm_wise_countpetition=[]
        graph_bm_wise_countrule377=[]

        bm_wise_x=list(m7.parliament_BMwise_pendency.objects.order_by('designame').values('designame').distinct())
        for b in bm_wise_x:
            graph_bm_wise_x.append(b['designame'])

        bm_wise_countass=list(m7.parliament_BMwise_pendency.objects.order_by('designame').values('countass'))
        for b in bm_wise_countass:
            graph_bm_wise_countass.append(b['countass'])

        bm_wise_countspecialmention=list(m7.parliament_BMwise_pendency.objects.order_by('designame').values('countspecialmention'))
        for b in bm_wise_countspecialmention:
            graph_bm_wise_countspecialmention.append(b['countspecialmention'])
            
        bm_wise_countzerohour=list(m7.parliament_BMwise_pendency.objects.order_by('designame').values('countzerohour'))
        for b in bm_wise_countzerohour:
            graph_bm_wise_countzerohour.append(b['countzerohour'])

        bm_wise_countpetition=list(m7.parliament_BMwise_pendency.objects.order_by('designame').values('countpetition'))
        for b in bm_wise_countpetition:
            graph_bm_wise_countpetition.append(b['countpetition'])

        bm_wise_countrule377=list(m7.parliament_BMwise_pendency.objects.order_by('designame').values('countrule377'))
        for b in bm_wise_countrule377:
            graph_bm_wise_countrule377.append(b['countrule377'])

    ################## graph of directorate
        graph_d_wise_x=[]
        graph_d_wise_countass=[]
        graph_d_wise_countspecialmention=[]
        graph_d_wise_countzerohour=[]
        graph_d_wise_countpetition=[]
        graph_d_wise_countrule377=[]

        d_wise_x=list(m7.parliament_DIRwise_pendency.objects.order_by('designame').values('designame').distinct())
        for b in d_wise_x:
            graph_d_wise_x.append(b['designame'])
            
            d_wise_countass=list(m7.parliament_DIRwise_pendency.objects.order_by('designame').values('countass'))
            for b in d_wise_countass:
                graph_d_wise_countass.append(b['countass'])

            d_wise_countspecialmention=list(m7.parliament_DIRwise_pendency.objects.order_by('designame').values('countspecialmention'))
            for b in d_wise_countspecialmention:
                graph_d_wise_countspecialmention.append(b['countspecialmention'])
                
            d_wise_countzerohour=list(m7.parliament_DIRwise_pendency.objects.order_by('designame').values('countzerohour'))
            for b in d_wise_countzerohour:
                graph_d_wise_countzerohour.append(b['countzerohour'])

            d_wise_countpetition=list(m7.parliament_DIRwise_pendency.objects.order_by('designame').values('countpetition'))
            for b in d_wise_countpetition:
                graph_d_wise_countpetition.append(b['countpetition'])
                
            d_wise_countrule377=list(m7.parliament_DIRwise_pendency.objects.order_by('designame').values('countrule377'))
            for b in d_wise_countrule377:
                graph_d_wise_countrule377.append(b['countrule377'])

        parlia_officer=list(m7.parliament_countOfficerwiseTotal.objects.values())
        bm_list=list(m7.parliament_BMwise_pendency.objects.filter().order_by('designame').values('id','designame'))
    
        # # print('###################################',bm_list)

        context={
            'par_day':par_day,
            'par_time':par_time,
            'graph_bm_wise_x':graph_bm_wise_x,
            'graph_bm_wise_countass':json.dumps(graph_bm_wise_countass),
            'graph_bm_wise_countspecialmention':json.dumps(graph_bm_wise_countspecialmention),
            'graph_bm_wise_countzerohour':json.dumps(graph_bm_wise_countzerohour),
            'graph_bm_wise_countpetition':json.dumps(graph_bm_wise_countpetition),
            'graph_bm_wise_countrule377':json.dumps(graph_bm_wise_countrule377),

            'graph_d_wise_x':graph_d_wise_x,
            'graph_d_wise_countass':json.dumps(graph_d_wise_countass),
            'graph_d_wise_countspecialmention':json.dumps(graph_d_wise_countspecialmention),
            'graph_d_wise_countzerohour':json.dumps(graph_d_wise_countzerohour),
            'graph_d_wise_countpetition':json.dumps(graph_d_wise_countpetition),
            'graph_d_wise_countrule377':json.dumps(graph_d_wise_countrule377),

            'date3':date3,
            'date1':date1,
            'date2':date2,

        'parlia_ls_rs':parlia_ls_rs,
        'assuranceleft':assuranceleft,
        'assuranceright':assuranceright,
        'rule377left':rule377left,
        'rule377right':rule377right,
        'zerohourleft':zerohourleft,
        'zerohourright':zerohourright,
        'petleft':petleft,
        'petright':petright,
        'smleft':smleft,
        'smright':smright,
        'progress_list':progress_list,
        'officerwise_dir':officerwise_dir,
        'parlia_dirwise':parlia_dirwise,
        'officerwise_bm':officerwise_bm,
        'parlia_bmwise':parlia_bmwise,
        #    'directory_names_list':directory_names_list,
        'bm_names_list':bm_names_list,
        'parlia_officer':parlia_officer,
        'bm_list':bm_list,
        'dir_list':dir_list,
        }
        return render(request, 'parliament2.html',context)
    except Exception as e: 
        print(e)
        try:
            error_Table.objects.create(fun_name="do_dashboard",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "homepage_errors.html", {})

def getparliadata(request):
    if request.method == 'POST' and request.is_ajax():
        date_range=request.POST.get('date_range')
        # print('from',date_range)
        sp_date = date_range.split(':')
        start  = datetime.strptime(sp_date[0].strip(),"%d/%m/%Y").strftime("%Y-%m-%d")
        end  = datetime.strptime(sp_date[1].strip(),"%d/%m/%Y").strftime("%Y-%m-%d")
        url='https://morpr.cris.org.in/pat/mu/getProgressCount?&frmdt='+start+'&todt='+end
        data={
        'username':'crismuapi',
        'password':'Crismuapi#1234',
        }
        headers = {"Content-Type": "application/json; charset=utf-8"}
        response = requests.request("GET", url,headers=headers,
        auth = HTTPBasicAuth('crismuapi', 'Crismuapi#1234'))
        progress_list=[]
        l_main=response.json() 
        # Update_count = 0
        # create_count = 0
        # print('lmain',l_main)
        # m7.parliament_progress_count.objects.filter().delete()
        # create_count += 1
        for i in range(len(l_main)):
            # create_count += 1
            progress_list.append({
                'newentry':l_main[i]['newentry'],
                'finalised':l_main[i]['finalised'],
                'typee':l_main[i]['type'],
                'total':l_main[i]['total'],
                'opnbal':l_main[i]['opnbal']})
            # m7.parliament_progress_count.objects.create(newentry=l_main[i]['newentry'],finalised=l_main[i]['finalised'],typee=l_main[i]['type'],total=l_main[i]['total'],opnbal=l_main[i]['opnbal'])
        # m9.LogApi.objects.create(schedular_name = "devinspapiparlia_parlia_progress",dates = date.today(),times = datetime.now().time(),Total_count=create_count+Update_count,Total_update = Update_count,Total_Create = create_count)
        # progress_list=list(m7.parliament_progress_count.objects.values('typee','newentry','finalised','total','opnbal'))

        context={
            'progress_list':progress_list,
        }
        return JsonResponse(context, safe=False)
        # # print(start,end)

    return JsonResponse({'success': False}, status=400)

def getdata1(request):
    if request.method=='GET':
        y=request.GET.get('y')
        x=request.GET.get('x')
        # # print('yy',y)
        # list2=list(m7.parliament_countOfficerwiseTotal.objects.filter(dir_name=y).values('myid'))
        # # print('list2',list2,list2[0]['myid'])
        if y == 'all':
            finallist2= list(m7.parliament_countOfficerwiseTotal.objects.filter(bmid=x).values())
        else:
            finallist2=list(m7.parliament_countOfficerwiseTotal.objects.filter(dircode=y).values())
        # # print('finallist2',finallist2)
     
        context={
        'finallist2':finallist2,
        }  
        return JsonResponse(context, safe=False)
    return JsonResponse({'sucess':False},status=400)

def getdata(request):
    if request.method=='GET':
        x=request.GET.get('x')
        finallist=[]
        if x == 'all':
            finallist= list(m7.parliament_countOfficerwiseTotal.objects.values())
            # officers=list(m7.parliament_DIRwise_pendency.objects.filter().values('id','designame'))
            officers=list(m7.parliament_mydirectory.objects.filter().order_by('-dir_name').values('myid','dir_name'))
        # # print('xx',x)
        # list1=list(m7.parliament_myboardmember.objects.filter(bm_name=x).values('myid'))
        # # print('list1',list1,list1[0]['myid'])
        else:
            filter_off=list(m7.parliament_countOfficerwiseTotal.objects.filter(bmid=x).values('dircode'))
            off=[]
            for i in filter_off:
                off.append(i['dircode'])
            officers=list(m7.parliament_mydirectory.objects.filter(myid__in=off).order_by('-dir_name').values('myid','dir_name'))
            
            finallist=list(m7.parliament_countOfficerwiseTotal.objects.filter(bmid=x).values())

        context={
            'officers':officers,
            'finallist':finallist,
        } 
        return JsonResponse(context, safe=False)
    return JsonResponse({'sucess':False},status=400)

def parlia_pdf(request):
    date1 = date.today()
    par_day=m9.LogApi.objects.filter(schedular_name='parliament_countOfficerwiseTotal').values('dates').order_by('-dates')[0]['dates']
    date1 = datetime.strftime(par_day,"%d/%m/%Y")
    parlia_bmwise=list(m7.parliament_BMwise_pendency.objects.values('countspecialmention','countzerohour','countpetition','designame','countrule377','countass')) 
    sp=0
    zh=0
    cp=0
    ru=0
    au=0
    for p in parlia_bmwise:
        if p['countspecialmention']:
            sp+= int(p['countspecialmention'])
        if p['countzerohour']:
            zh+= int(p['countzerohour'])
        if p['countpetition']:
            cp+= int(p['countpetition'])
        if p['countrule377']:
            ru+= int(p['countrule377'])
        if p['countass']:
            au+= int(p['countass'])
    parlia_bmwise.append({'countspecialmention':sp,'countzerohour':zh,'countpetition':cp,'designame':'Total','countrule377':ru,'countass':au})
    parlia_officer=list(m7.parliament_countOfficerwiseTotal.objects.values())
    total=[{'countspecialmention':sp,'countzerohour':zh,'countpetition':cp,'bm_desig':'Total','designame':'Total','dir_desig':'Total','countrule377':ru,'countass':au}]

    bm = list(m7.parliament_myboardmember.objects.values('myid'))
    officer_list=[]
    xyz=[]
    for p in range(len(parlia_officer)):
        counts=len(list(m7.parliament_countOfficerwiseTotal.objects.filter(bmid=parlia_officer[p]['bmid']).values()))+1
        print(counts)
        bm_desig=list(m7.parliament_BMwise_pendency.objects.filter(id=parlia_officer[p]['bmid']).values('designame'))[0]['designame']
        dir_desig=list(m7.parliament_mydirectory.objects.filter(myid=parlia_officer[p]['dircode']).values('dir_name'))
        if len(dir_desig)>0:
            dir_desig=dir_desig[0]['dir_name']
        else:
            dir_desig=' '

        parlia_officer[p].update({'bm_desig':bm_desig})
        parlia_officer[p].update({'dir_desig':dir_desig})

        if bm_desig not in xyz:
            parlia_officer[p].update({'counts':counts})
            xyz.append(bm_desig)
        else:
            parlia_officer[p].update({'counts':0})
       
        x={'counts':counts,'bm_desig':bm_desig}
        if x not in officer_list:
            officer_list.append(x)
    officer_list=sorted(officer_list,key=lambda d: d['counts'])

    for b in bm:
        sp1= sum(l['countspecialmention'] for l in list(m7.parliament_countOfficerwiseTotal.objects.filter(bmid=b['myid']).exclude(countspecialmention__isnull=True).values('countspecialmention')))
        zh1= sum(l['countzerohour'] for l in list(m7.parliament_countOfficerwiseTotal.objects.filter(bmid=b['myid']).exclude(countzerohour__isnull=True).values('countzerohour')))
        cp1= sum(l['countpetition'] for l in list(m7.parliament_countOfficerwiseTotal.objects.filter(bmid=b['myid']).exclude(countpetition__isnull=True).values('countpetition')))
        ru1= sum(l['countrule377'] for l in list(m7.parliament_countOfficerwiseTotal.objects.filter(bmid=b['myid']).exclude(countrule377__isnull=True).values('countrule377')))
        au1= sum(l['countass'] for l in list(m7.parliament_countOfficerwiseTotal.objects.filter(bmid=b['myid']).exclude(countass__isnull=True).values('countass')))
        bm_desig=list(m7.parliament_BMwise_pendency.objects.filter(id=b['myid']).values('designame'))[0]['designame']
        # print(bm_desig)
        parlia_officer.append({'countspecialmention':sp1,'countzerohour':zh1,'countpetition':cp1,'designame':'Sub Total','countrule377':ru1,'countass':au1, 'bm_desig':bm_desig, 'dir_desig':'NA', 'counts':0})
        # print(len(parlia_officer))
    
    parlia_officer=sorted(parlia_officer,key=lambda d: d['bm_desig'] )
    # print(parlia_officer)
    
    



    context={
        'date1':date1,
        'parlia_bmwise':parlia_bmwise,
        'parlia_officer':parlia_officer,
        'officer_list':officer_list,
        'total':total
    }
    template_src='parlia_pdf.html'
    return render_to_pdf(template_src, context)

# def onfromdate(request):
#     if request.method=='GET':
#         myfrom=request.GET.get('from')
#         # print('from',myfrom)
#         context={

#         }
#         return JsonResponse(context, safe=False)
#     return JsonResponse({'sucess':False},status=400)    


# def ontodate(request):
#     if request.method=='GET':
#         myto=request.GET.get('to')
#         # print('to',myto)
#         context={

#         }
#         return JsonResponse(context, safe=False)
#     return JsonResponse({'sucess':False},status=400)    

   

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def home_page(request):
    
    today=datetime.now()   
    week = datetime.now() - timedelta(days=30)
    lastyear = datetime.now() - timedelta(days=60)
    tempvg=[]
    zone = list(m9.Punctuality_Service_Output.objects.all().values('Zone_Code').distinct())
    tempvg.extend(zone)
    
    o=''
    for i in range(len(tempvg)):
        try:
            o = m9.Punctuality_Service_Output.objects.filter(Zone_Code = tempvg[i]['Zone_Code'] , Scheduled_Date__range = [week,today]).annotate(pp=(Sum('nlt_count')*100.0)/Sum('train_count'))[0]
            tempvg[i].update({"pp":round(o.pp,2)})
        except:
            tempvg[i].update({"pp":0})
    o1 =''
    for i in range(len(tempvg)):
        try:
            o1 = m9.Punctuality_Service_Output.objects.filter(Zone_Code = tempvg[i]['Zone_Code'] , Scheduled_Date__range = [lastyear,week]).annotate(pp1=(Sum('nlt_count')*100.0)/Sum('train_count'))[0]
            tempvg[i].update({"pp1":round(o1.pp1,2)})
        except:
            tempvg[i].update({"pp1":0})
    
    for i in range(len(tempvg)):
        tempvg[i].update({"variation":round((tempvg[i]['pp']-tempvg[i]['pp1']),2)}) 
    punct=sorted(tempvg,key=lambda d: d['variation'])[0]
    punc_zone=punct['Zone_Code']
    punc_val=punct['variation']
    # print(punct)

    load_comd = list(m9.Loading_Commodity.objects.annotate(sint=Cast('Var_Over_Target', FloatField()),mint=Cast('Var_Pctg', FloatField())).order_by('mint').values())[0]
    # print(load_comd)
    load_com=load_comd['PlanHead']
    load_com_val=load_comd['mint']
    load_zone = list(m9.Loading_Zonal.objects.annotate(sint=Cast('Var_Over_Target', FloatField()),mint=Cast('Var_Pctg', FloatField())).order_by('mint').values())[0]
    # print(load_zone)
    load_zon=load_zone['Rly']
    load_zon_val=load_zone['mint']
   

    

    context={
        'punc_zone':punc_zone,
        'punc_val':punc_val,
        'load_com':load_com,
        'load_com_val':load_com_val,
        'load_zon':load_zon,
        'load_zon_val':load_zon_val,
    }
    return render(request, 'home_page3_old.html', context)
    

def view_table(request):
    if request.method == "GET" and request.is_ajax():
        id=int(request.GET.get('id'))

        if id == 1:
            table_data=list(m7.safety.objects.filter().values())

        elif id==2:
            table_data=list(m7.loading.objects.filter().values())
        
        elif id==3:
            table_data=list(m7.punctuality.objects.filter().values())
        
        elif id==4:
            table_data=list(m7.earnings.objects.filter().values())
        
        elif id==5:
            table_data=list(m7.capex.objects.filter().values())

        elif id==6:
            table_data=list(m7.owe.objects.filter().values())
        
        elif id==7:
            table_data=list(m7.pension_bill.objects.filter().values())
        
        elif id==8:
            table_data=list(m7.asset_reliabilty.objects.filter().values())
        
        for s in table_data:
            v=s['cummulative_target']-s['cummulative_actuals']
            s.update({'variation':v})
        
        context={'table_data':table_data}
        return JsonResponse(context, safe=False)
    return JsonResponse({'sucess':False},status=400)

def drishti(request):
    loading=list(m7.punctuality.objects.filter().values())
    punctuality=list(m7.punctuality.objects.filter().values())
    earnings=list(m7.punctuality.objects.filter().values())
    owe=list(m7.punctuality.objects.filter().values())
    capex=list(m7.punctuality.objects.filter().values())
    pension_bill=list(m7.punctuality.objects.filter().values())
    safety=list(m7.punctuality.objects.filter().values())
    asset_reliabilty=list(m7.punctuality.objects.filter().values())
    # wagon_turn_around=list(m7.wagon_turn_around.objects.filter().values())

    for s in loading:
        v=s['cummulative_target']-s['cummulative_actuals']
        s.update({'variation':v})

    for s in punctuality:
        v=s['cummulative_target']-s['cummulative_actuals']
        s.update({'variation':v})
    
    for s in earnings:
        v=s['cummulative_target']-s['cummulative_actuals']
        s.update({'variation':v})
    
    for s in owe:
        v=s['cummulative_target']-s['cummulative_actuals']
        s.update({'variation':v})

    for s in capex:
        v=s['cummulative_target']-s['cummulative_actuals']
        s.update({'variation':v})

    for s in pension_bill:
        v=s['cummulative_target']-s['cummulative_actuals']
        s.update({'variation':v})

    for s in safety:
        v=s['cummulative_target']-s['cummulative_actuals']
        s.update({'variation':v})

    for s in asset_reliabilty:
        v=s['cummulative_target']-s['cummulative_actuals']
        s.update({'variation':v})

    # for s in wagon_turn_around:
    #     v=s['cummulative_target']-s['cummulative_actuals']
    #     s.update({'variation':v})
    
    context={
        'safety':safety,
        'loading':loading,
        'punctuality':punctuality,
        'earnings':earnings,
        'owe':owe,
        'pension_bill':pension_bill,
        'capex':capex,
        'asset_reliabilty':asset_reliabilty,
        }
    return render(request, 'drishti_new.html', context)




def fetchsql(request):
    
    alldata = []
    with connections['users'].cursor() as cursor:
        cursor.execute("SELECT * FROM  mcdo_commodity_wise_mst")
        # alldata = cursor.fetchall()
        alldata = dictfetchall(cursor)
        cursor.close()
    # print('tarun=====', alldata)
    return HttpResponse(alldata)


# def home_page1(request):

#     with connections['users'].cursor() as cursor:
#         ###### vishnu
#         from datetime import date,timedelta
#         dates=datetime.now()
#         y=dates.year
#         m=dates.month
#         lm=dates.month-1
#         # cursor.execute('''SELECT "mou_sub"."name", "mou_sub"."unit", "mou_sub"."id" FROM "mou_sub" WHERE "mou_sub"."main_id" = 4''')
#         cursor.execute('''SELECT name, unit, id FROM `cris-cr`.mou_sub WHERE main_id = 4''')
#         rolling = dictfetchall(cursor)
#         # print("rolling",rolling)
#         for i in range(len(rolling)):
#             # print(rolling[i]['id'])
           
#             if rolling[i]['id'] in [40,41,42,43,44,45, 46,47,48]:
#                 #################### for target ##################
#                 # cursor.execute('''SELECT "mou_sub_target"."target" FROM "mou_sub_target" WHERE ("mou_sub_target"."entry_id" = {target} AND "mou_sub_target"."sub_id" = 4)'''.format(target = rolling[i]['id']))
#                 #cursor.execute('''SELECT target FROM  `cris-cr`.mou_sub_target WHERE (sub_id = {target})'''.format(target = rolling[i]['id']))
#                 #cursor.execute('''SELECT sum(cumm) as unit FROM  `cris-cr`.mou_sub_cumm WHERE (sub_id ={target} and entry_id in (SELECT id FROM `cris-cr`.mou_entry where year={y}) )'''.format(target = rolling[i]['id'],y=y-1))
#                 cursor.execute('''SELECT sum(performance) as unit FROM  `cris-cr`.mou_sub_data WHERE (sub_id ={target} and entry_id in (SELECT id FROM `cris-cr`.mou_entry where year={y}) )'''.format(target = rolling[i]['id'],y=y))

#                 target = dictfetchall(cursor)
#                 if target:
#                     rolling[i].update(target[0])
#                 else:
#                     rolling[i].update({'target':'0'})
                
#                 #################### for performance #############
#                 #cursor.execute('''SELECT "mou_sub_data"."performance" FROM "mou_sub_data" WHERE ("mou_sub_data"."entry_id" = {performance} AND "mou_sub_data"."sub_id" = 4)'''.format(performance = rolling[i]['id']))    
#                 #cursor.execute('''SELECT performance FROM `cris-cr`.mou_sub_data WHERE (sub_id = {performance})'''.format(performance = rolling[i]['id']))    
#                 #cursor.execute('''SELECT sum(cumm) as target FROM  `cris-cr`.mou_sub_cumm WHERE (sub_id ={target} and entry_id in (SELECT id FROM `cris-cr`.mou_entry where year={y}) )'''.format(target = rolling[i]['id'],y=y))
#                 cursor.execute('''SELECT sum(cumm) as target FROM  `cris-cr`.mou_sub_cumm_pre_yr WHERE (sub_id ={target} and entry_id in (SELECT id FROM `cris-cr`.mou_entry where year={y}) )'''.format(target = rolling[i]['id'],y=y))

               
                
#                 performance = dictfetchall(cursor)
#                 if performance:
#                     rolling[i].update(performance[0])
#                 else:
#                     rolling[i].update({'performance':'0'})

#                 #################### for cummn month ############
#                 #cursor.execute('''SELECT "mou_sub_cumm"."cumm" as cumm_month FROM "mou_sub_cumm" WHERE ("mou_sub_cumm"."entry_id" =4 AND "mou_sub_cumm"."sub_id" =  {cumm})'''.format(cumm = rolling[i]['id']))    
#                 # cursor.execute('''SELECT cumm  as cumm_month FROM `cris-cr`.mou_sub_cumm WHERE (sub_id = {cumm})'''.format(cumm = rolling[i]['id']))    
#                 #cursor.execute('''SELECT cumm  as cumm_month FROM `cris-cr`.mou_sub_cumm WHERE (sub_id = {cumm} and entry_id in  (SELECT id FROM `cris-cr`.mou_entry where month={m} and year={y} ))'''.format(cumm = rolling[i]['id'],m=m-1, y=y-1)) 
#                 cursor.execute('''SELECT sum(performance)  as cumm_month FROM `cris-cr`.mou_sub_data WHERE (sub_id = {cumm} and entry_id in  (SELECT id FROM `cris-cr`.mou_entry where month={m} and year={y}))'''.format(cumm = rolling[i]['id'],m=m-2, y=y))    
                
#                 cummn = dictfetchall(cursor)
#                 if cummn:
#                     rolling[i].update(cummn[0])
#                 else:
#                     rolling[i].update({'cumm_month':'0'})
#                 # print("per",cummn)

#                 #################### for cummn Year ##############
#                 # cursor.execute('''SELECT "mou_sub_cumm_pre_yr"."cumm" as cumm_year FROM "mou_sub_cumm_pre_yr" WHERE ("mou_sub_cumm_pre_yr"."entry_id" = 4 AND "mou_sub_cumm_pre_yr"."sub_id" = {cummperyr})'''.format(cummperyr = rolling[i]['id']))    
#                 #cursor.execute('''SELECT cumm as cumm_year FROM `cris-cr`.mou_sub_cumm_pre_yr WHERE (sub_id = {cummperyr})'''.format(cummperyr = rolling[i]['id']))    
#                 #cursor.execute('''SELECT cumm  as cumm_year FROM `cris-cr`.mou_sub_cumm WHERE (sub_id = {cumm} and entry_id in  (SELECT id FROM `cris-cr`.mou_entry where month={m}))'''.format(cumm = rolling[i]['id'],m=m))    
#                 cursor.execute('''SELECT performance  as cumm_year FROM `cris-cr`.mou_sub_data WHERE (sub_id = {cumm} and entry_id in  (SELECT id FROM `cris-cr`.mou_entry where month={m} and year={y}))'''.format(cumm = rolling[i]['id'],m=m-2, y=y))    

#                 cummperyear = dictfetchall(cursor)
#                 # print("cumperyr",cummperyear)
#                 if cummperyear:
#                     rolling[i].update(cummperyear[0])
#                 else:
#                     rolling[i].update({'cumm_year':'0'})
#                 # print("cummperyr",cummperyear)
#             # print('rolling=====', rolling)
    
#     #faisal start \
        
#     with connections['users'].cursor() as cursor:
#         #date for all
#         from datetime import date,timedelta
#         dates=datetime.now()
#         y=dates.year
#         m=dates.month
#         lm=dates.month-1
        
#         # cpy=date.today() - timedelta(days = 365)
#         # # print(cpy)
#         # # print(dates)
#         #cursor.execute('''SELECT "home_page_mousub"."name", "home_page_mousub"."unit", "home_page_mousub"."id" FROM "home_page_mousub" WHERE "home_page_mousub"."main_id" = 6''')
#         cursor.execute('''SELECT name, unit, id FROM `cris-cr`.mou_sub WHERE main_id = 6''')

#         data = dictfetchall(cursor)
#         # print("data1",data)
#         for i in range(len(data)):
#             # print(data[i]['id'])
#             if data[i]['id'] in [56,57,58,59]:
#                 #################### for target ##################
#                 #cursor.execute('''SELECT "home_page_mousubtarget"."target" FROM "home_page_mousubtarget" WHERE ("home_page_mousubtarget"."entry_id" = {target} AND "home_page_mousubtarget"."sub_id" = 6)'''.format(target = data[i]['id']))
#                 #cursor.execute('''SELECT target FROM  `cris-cr`.mou_sub_target WHERE (sub_id ={target}  )'''.format(target = data[i]['id']))
#                 cursor.execute('''SELECT sum(cumm) as unit FROM  `cris-cr`.mou_sub_cumm_pre_yr WHERE (sub_id ={target} and entry_id in (SELECT id FROM `cris-cr`.mou_entry where year={y}) )'''.format(target = data[i]['id'],y=y))

#                 target = dictfetchall(cursor)
#                 if target:
#                     data[i].update(target[0])
#                 else:
#                     data[i].update({'target':'0'})
                
#                 #################### for performance #############
#                 #cursor.execute('''SELECT "home_page_mousubdata"."performance" FROM "home_page_mousubdata" WHERE ("home_page_mousubdata"."entry_id" = {performance} AND "home_page_mousubdata"."sub_id" = 6)'''.format(performance = data[i]['id']))    
#                 #cursor.execute('''SELECT SUM(cumm) FROM `cris-cr`.mou_sub_cumm WHERE (sub_id =  {performance} and entry_id in (SELECT id FROM `cris-cr`.mou_entry where month <= 4  AND month >= {lm}))'''.format(performance = data[i]['id'],lm = lm))    
#                 cursor.execute('''SELECT sum(cumm) as target FROM  `cris-cr`.mou_sub_cumm WHERE (sub_id ={target} and entry_id in (SELECT id FROM `cris-cr`.mou_entry where year={y}) )'''.format(target = data[i]['id'],y=y))

#                 performance = dictfetchall(cursor)
#                 if performance:
#                     data[i].update(performance[0])
#                 else:
#                     data[i].update({'performance':'0'})

#                 #################### for cummn month ############
#                 #cursor.execute('''SELECT "home_page_mousubcumm"."cumm" as cumm_month FROM "home_page_mousubcumm" WHERE ("home_page_mousubcumm"."entry_id" = {cumm} AND "home_page_mousubcumm"."sub_id" = 6)'''.format(cumm = data[i]['id']))    
#                 cursor.execute('''SELECT sum(cumm)  as cumm_month FROM `cris-cr`.mou_sub_cumm_pre_yr WHERE (sub_id = {cumm} and entry_id in  (SELECT id FROM `cris-cr`.mou_entry where month={m} and year={y}))'''.format(cumm = data[i]['id'],m=m-1, y=y))    

#                 cummn = dictfetchall(cursor)
#                 if cummn:
#                     data[i].update(cummn[0])
#                 else:
#                     data[i].update({'cumm_month':'0'})
#                 # print("per",cummn)

#                 #################### for cummn Year ##############
#                 #cursor.execute('''SELECT "home_page_mousubcummpreyr"."cumm" as cumm_year FROM "home_page_mousubcummpreyr" WHERE ("home_page_mousubcummpreyr"."entry_id" = 6 AND "home_page_mousubcummpreyr"."sub_id" = {cummperyr})'''.format(cummperyr = data[i]['id']))    
#                 #cursor.execute('''SELECT cumm as cumm_year FROM `cris-cr`.mou_sub_cumm_pre_yr WHERE (sub_id = {cummperyr})'''.format(cummperyr = data[i]['id']))    
#                 cursor.execute('''SELECT cumm  as cumm_year FROM `cris-cr`.mou_sub_cumm WHERE (sub_id = {cumm} and entry_id in  (SELECT id FROM `cris-cr`.mou_entry where month={m} and year={y}))'''.format(cumm = data[i]['id'],m=m-1, y=y))    

#                 cummperyear = dictfetchall(cursor)
#                 # print("cumperyr",cummperyear)
#                 if cummperyear:
#                     data[i].update(cummperyear[0])
#                 else:
#                     data[i].update({'cumm_year':'0'})
#             elif data[i]['id'] in [55,60,61,62,63,64]:
#                 #################### for target ##################
#                 #cursor.execute('''SELECT "home_page_mousubtarget"."target" FROM "home_page_mousubtarget" WHERE ("home_page_mousubtarget"."entry_id" = {target} AND "home_page_mousubtarget"."sub_id" = 6)'''.format(target = data[i]['id']))
#                 #cursor.execute('''SELECT target FROM  `cris-cr`.mou_sub_target WHERE (sub_id ={target}  )'''.format(target = data[i]['id']))
#                 cursor.execute('''SELECT sum(cumm) as unit FROM  `cris-cr`.mou_sub_cumm_pre_yr WHERE (sub_id ={target} and entry_id in (SELECT id FROM `cris-cr`.mou_entry where year={y}) )'''.format(target = data[i]['id'],y=y))

#                 target = dictfetchall(cursor)
#                 if target:
#                     data[i].update(target[0])
#                 else:
#                     data[i].update({'target':'0'})
                
#                 #################### for performance #############
#                 #cursor.execute('''SELECT "home_page_mousubdata"."performance" FROM "home_page_mousubdata" WHERE ("home_page_mousubdata"."entry_id" = {performance} AND "home_page_mousubdata"."sub_id" = 6)'''.format(performance = data[i]['id']))    
#                 #cursor.execute('''SELECT SUM(cumm) FROM `cris-cr`.mou_sub_cumm WHERE (sub_id =  {performance} and entry_id in (SELECT id FROM `cris-cr`.mou_entry where month <= 4  AND month >= {lm}))'''.format(performance = data[i]['id'],lm = lm))    
#                 cursor.execute('''SELECT sum(performance) as target FROM  `cris-cr`.mou_sub_data WHERE (sub_id ={target} and entry_id in (SELECT id FROM `cris-cr`.mou_entry where year={y}) )'''.format(target = data[i]['id'],y=y))

#                 performance = dictfetchall(cursor)
#                 if performance:
#                     data[i].update(performance[0])
#                 else:
#                     data[i].update({'performance':'0'})

#                 #################### for cummn month ############
#                 #cursor.execute('''SELECT "home_page_mousubcumm"."cumm" as cumm_month FROM "home_page_mousubcumm" WHERE ("home_page_mousubcumm"."entry_id" = {cumm} AND "home_page_mousubcumm"."sub_id" = 6)'''.format(cumm = data[i]['id']))    
#                 cursor.execute('''SELECT sum(cumm)  as cumm_month FROM `cris-cr`.mou_sub_cumm_pre_yr WHERE (sub_id = {cumm} and entry_id in  (SELECT id FROM `cris-cr`.mou_entry where month={m} and year={y}))'''.format(cumm = data[i]['id'],m=m-1, y=y))    

#                 cummn = dictfetchall(cursor)
#                 if cummn:
#                     data[i].update(cummn[0])
#                 else:
#                     data[i].update({'cumm_month':'0'})
#                 # print("per",cummn)

#                 #################### for cummn Year ##############
#                 #cursor.execute('''SELECT "home_page_mousubcummpreyr"."cumm" as cumm_year FROM "home_page_mousubcummpreyr" WHERE ("home_page_mousubcummpreyr"."entry_id" = 6 AND "home_page_mousubcummpreyr"."sub_id" = {cummperyr})'''.format(cummperyr = data[i]['id']))    
#                 #cursor.execute('''SELECT cumm as cumm_year FROM `cris-cr`.mou_sub_cumm_pre_yr WHERE (sub_id = {cummperyr})'''.format(cummperyr = data[i]['id']))    
#                 cursor.execute('''SELECT performance  as cumm_year FROM `cris-cr`.mou_sub_data WHERE (sub_id = {cumm} and entry_id in  (SELECT id FROM `cris-cr`.mou_entry where month={m} and year={y}))'''.format(cumm = data[i]['id'],m=m-1, y=y))    

#                 cummperyear = dictfetchall(cursor)
#                 # print("cumperyr",cummperyear)
#                 if cummperyear:
#                     data[i].update(cummperyear[0])
#                 else:
#                     data[i].update({'cumm_year':'0'})
            
            
#             # # print("cummperyr",cummperyear)
#         # # print(data,'data')
    
#     # Faisal End \
        
#     with connections['users'].cursor() as cursor:
#         # FOR LOADING-COMMODITY 
#         cursor.execute('''SELECT * FROM  mcdo_commodity_wise_mst''')
#         commodity = dictfetchall(cursor)
#         ctar_total,cpre_total,ccur_total=0,0,0
#         commodity1=[]
#         commodity2={}
#         for c in commodity:
#             temp={}
#             cursor.execute('''SELECT sum(target_yr) as a1, sum(previous_yr) as a2, sum(current_yr) as a3, commodity_id,
#                             (sum(current_yr)-sum(previous_yr))/sum(previous_yr)*100 as a4, (sum(current_yr)-sum(target_yr))/sum(target_yr)*100 as a5
#                             FROM mcdo_commodity_wise_data WHERE commodity_id=%s and entry_id in (SELECT id FROM mcdo_commodity_wise_entry where financial_yr=2022)''',[c['id']])
#             dict_data = dictfetchall(cursor)
#             temp['a1']=dict_data[0]['a1']
#             temp['a2']=dict_data[0]['a2']
#             temp['a3']=dict_data[0]['a3']
#             temp['a4']=dict_data[0]['a4']
#             temp['a5']=dict_data[0]['a5']
#             temp['commodity_id']=dict_data[0]['commodity_id']
#             commodity1.append(temp)
#             ctar_total=ctar_total+dict_data[0]['a1']
#             cpre_total=cpre_total+dict_data[0]['a2']
#             ccur_total=ccur_total+dict_data[0]['a3']
#         commodity2['tar_total']=ctar_total
#         commodity2['pre_total']=cpre_total
#         commodity2['cur_total']=ccur_total
#         commodity2['over_lasy']=(ccur_total-cpre_total)/cpre_total*100
#         commodity2['over_targ']=(ccur_total-ctar_total)/ctar_total*100
#     # END LOADING-COMMODITY 

#     # FOR LOADING-ZONE 
#         cursor.execute('''SELECT DISTINCT zone FROM  mcdo_commodity_wise_entry  WHERE zone!='null' order by zone ''')
#         zone = dictfetchall(cursor)
#         ztar_total,zpre_total,zcur_total=0,0,0
#         zone1=[]
#         zone2={}
#         for c in zone:
#             try:
#                 temp={}
#                 cursor.execute('''SELECT sum(target_yr) as a1, sum(previous_yr) as a2, sum(current_yr) as a3, entry_id,
#                                 (sum(current_yr)-sum(previous_yr))/sum(previous_yr)*100 as a4, (sum(current_yr)-sum(target_yr))/sum(target_yr)*100 as a5 
#                                 FROM mcdo_commodity_wise_data where entry_id in (SELECT id FROM mcdo_commodity_wise_entry where financial_yr=2022 and zone=%s)''',[c['zone']])
#                 dict_data = dictfetchall(cursor)
#                 temp['a1']=dict_data[0]['a1']
#                 temp['a2']=dict_data[0]['a2']
#                 temp['a3']=dict_data[0]['a3']
#                 temp['a4']=dict_data[0]['a4']
#                 temp['a5']=dict_data[0]['a5']
#                 temp['entry_id']=dict_data[0]['entry_id']
#                 temp['zone']=c['zone']
#                 zone1.append(temp)
#                 ztar_total=ztar_total+dict_data[0]['a1']
#                 zpre_total=zpre_total+dict_data[0]['a2']
#                 zcur_total=zcur_total+dict_data[0]['a3']
#             except:
#                 temp1=0
#         zone2['tar_total']=ztar_total
#         zone2['pre_total']=zpre_total
#         zone2['cur_total']=zcur_total
#         zone2['over_lasy']=(zcur_total-zpre_total)/zpre_total*100
#         zone2['over_targ']=(zcur_total-ztar_total)/ztar_total*100
#     # END LOADING-ZONE 

#     # FOR FINANCIAL REPORT
#         cursor.execute('''SELECT * FROM  mcdo_financial_mst''')
#         earnings = dictfetchall(cursor)
#         etar_total,epre_total,ecur_total=0,0,0
#         earnings1=[]
#         earnings2={}
#         for c in earnings:
#             temp={}
#             cursor.execute('''SELECT sum(previous_yr) as a1, sum(current_month) as a2, sum(current_yr) as a3, financial_id,
#                             sum(current_yr)-sum(current_month) as a4, sum(current_yr)-sum(previous_yr) as a5
#                             FROM mcdo_financial_data WHERE financial_id=%s and entry_id in (SELECT id FROM mcdo_financial_entry where financial_yr=2022)''',[c['id']])
#             dict_data = dictfetchall(cursor)
#             temp['a1']=dict_data[0]['a1']
#             temp['a2']=dict_data[0]['a2']
#             temp['a3']=dict_data[0]['a3']
#             temp['a4']=dict_data[0]['a4']
#             temp['a5']=dict_data[0]['a5']
#             temp['financial_id']=dict_data[0]['financial_id']
#             earnings1.append(temp)
#             etar_total=etar_total+dict_data[0]['a1']
#             epre_total=epre_total+dict_data[0]['a2']
#             ecur_total=ecur_total+dict_data[0]['a3']
#         earnings2['tar_total']=etar_total
#         earnings2['pre_total']=epre_total
#         earnings2['cur_total']=ecur_total
#         earnings2['over_lasy']=ecur_total-epre_total
#         earnings2['over_targ']=ecur_total-etar_total
#     # END FINANCIAL REPORT
#     #### sidhi
#     with connections['users'].cursor() as cursor:
#         # for cum target column
#         cursor.execute(''' SELECT sum(C_D_Target)+sum(P_D_Target) FROM `cris-cr`.cms_mcdo_crucial_infra_works where year=2022 and month>3''')
#         cumdata=cursor.fetchall()
#         cursor.execute(''' SELECT sum(C_E_Target)+sum(P_E_Target) FROM `cris-cr`.cms_mcdo_crucial_infra_works where year=YEAR(CURDATE()) and month>3''')
#         cumdata1=cursor.fetchall()
#         cursor.execute(''' SELECT sum(C_gc_Target)+sum(P_GC_Target) FROM `cris-cr`.cms_mcdo_crucial_infra_works where year=YEAR(CURDATE()) and month>3''')
#         cumdata2=cursor.fetchall()
#         cursor.execute(''' SELECT sum(C_nl_Target)+sum(P_nl_Target) FROM `cris-cr`.cms_mcdo_crucial_infra_works where year=YEAR(CURDATE()) and month>3''')
#         cumdata3=cursor.fetchall()
#         cursor.execute(''' SELECT sum(C_tr_Target)+sum(P_tr_Target) FROM `cris-cr`.cms_mcdo_crucial_infra_works where year=YEAR(CURDATE()) and month>3''')
#         cumdata4=cursor.fetchall()
        
#         #for cum archived
#         cursor.execute(''' SELECT sum(C_D_Progress)+sum(P_D_Progress) FROM `cris-cr`.cms_mcdo_crucial_infra_works where year=2022 and month>3 and month<=MONTH(CURDATE())''')
#         cum1data=cursor.fetchall()
#         # print(cum1data)
#         cursor.execute(''' SELECT sum(C_e_Progress)+sum(P_e_Progress) FROM `cris-cr`.cms_mcdo_crucial_infra_works where year=2022 and month>3 and month<=MONTH(CURDATE())''')
#         cum1data1=cursor.fetchall()
#         cursor.execute(''' SELECT sum(C_gc_Progress)+sum(P_gc_Progress) FROM `cris-cr`.cms_mcdo_crucial_infra_works where year=2022 and month>3 and month<=MONTH(CURDATE())''')
#         cum1data2=cursor.fetchall()
#         cursor.execute(''' SELECT sum(C_nl_Progress)+sum(P_nl_Progress) FROM `cris-cr`.cms_mcdo_crucial_infra_works where year=2022 and month>3 and month<=MONTH(CURDATE())''')
#         cum1data3=cursor.fetchall()
#         cursor.execute(''' SELECT sum(C_tr_Progress)+sum(P_tr_Progress) FROM `cris-cr`.cms_mcdo_crucial_infra_works where year=2022 and month>3 and month<=MONTH(CURDATE())''')
#         cum1data4=cursor.fetchall()

#         # %var
#         if cumdata!=0:
#             r1=((cum1data[0][0]-cumdata[0][0])/cumdata[0][0])*100
#             # print(type(r1))
#         else:
#             r1=0
#         if cumdata1[0][0]!=0:
#             r2=((cum1data1[0][0]-cumdata1[0][0])/cumdata1[0][0])*100
#         else:
#             r2=0  
#         if cumdata2[0][0]!=0:
#             r3=((cum1data2[0][0]-cumdata2[0][0])/cumdata2[0][0])*100
#         else:
#             r3=0 
#         if cumdata3[0][0]!=0:
#             r4=((cum1data3[0][0]-cumdata3[0][0])/cumdata3[0][0])*100
#         else:
#             r4=0
#         if cumdata2[0][0]!=0:
#             r5=((cum1data4[0][0]-cumdata4[0][0])/cumdata4[0][0])*100
#         else:
#             r5=0    
      
       
#         alldata=2*cumdata[0][0]
#         # print(type(alldata))
#         alldata1=2*cumdata1[0][0]
#         alldata2=2*cumdata2[0][0]
#         alldata3=2*cumdata3[0][0]
#         alldata4=2*cumdata4[0][0]
        
#         infrastructure_creation=[{'h1':"Doubling",'sum':round(alldata,0),'cum':round(cumdata[0][0],0),
#         'cum1':round(cum1data[0][0],0),'res':round(r1,0)},{'h1':"Electrification",'sum':round(alldata1,0),'cum':round(cumdata1[0][0],0),'cum1':round(cum1data1[0][0],0),'res':round(r2,0)},
#         {'h1':"Gauge Conversions",'sum':round(alldata2,0),'cum':round(cumdata2[0][0],0),'cum1':round(cum1data2[0][0],0),
#         'res':round(r3,0)},{'h1':"New Lines",'sum':round(alldata3,0),'cum':round(cumdata3[0][0],0),'cum1':round(cum1data3[0][0],0),
#         'res':round(r4,0)},{'h1':"Track Renewals",'sum':round(alldata4,0),'cum':round(cumdata4[0][0],0),'cum1':round(cum1data4[0][0],0),'res':round(r5,0)}]

#         # infrastructure_creation=[{'h1':"Doubling",'sum':round(alldata,2),'cum':round(cumdata[0][0],2),'cum1':round(cum1data[0][0],2),'res':round(r1,2)},{'h1':"Electrification",'sum':round(alldata1,2),'cum':round(cumdata1[0][0],2),'cum1':round(cum1data1[0][0],2),'res':round(r2,2)},{'h1':"Gauge Conversions",'sum':round(alldata2,2),'cum':round(cumdata2[0][0],2),'cum1':round(cum1data2[0][0],2),'res':round(r3,2)},{'h1':"New Lines",'sum':round(alldata3,2),'cum':round(cumdata3[0][0],2),'cum1':round(cum1data3[0][0],2),'res':round(r4,2)},{'h1':"Track Renewals",'sum':round(alldata4,2),'cum':round(cumdata4[0][0],2),'cum1':round(cum1data4[0][0],2),'res':round(r5,2)}]
    
#     #kritika 
#     with connections['users'].cursor() as cursor:
#         # FOR SAFETY REPORT
#         cursor.execute('''SELECT DISTINCT trainNo1 FROM  safety1 WHERE trainNo1!='' order by trainNo1''')
#         safety = dictfetchall(cursor)
#         safety1=[]
#         safety2={}
#         total1,total2,total3,total4,total5=0,0,0,0,0
#         for s in safety:
#             temp,temp1,temp2,temp3,temp4,temp_change={},{},{},{},{},{}
#             # 2019-2020
#             cursor.execute(''' SELECT sum(current1) as a1 FROM safety1 WHERE trainNo1=%s AND ((year=%s and month>3) OR (year=%s and month<4)) ''',[s['trainNo1'],y-3,y-2])
#             dict_data1 = dictfetchall(cursor)
#             cursor.execute(''' SELECT sum(current2) as a2 FROM safety1 WHERE trainNo2=%s AND ((year=%s and month>3) OR (year=%s and month<4)) ''',[s['trainNo1'],y-3,y-2])
#             dict_data2 = dictfetchall(cursor)
#             cursor.execute(''' SELECT sum(current3) as a3 FROM safety1 WHERE trainNo3=%s AND ((year=%s and month>3) OR (year=%s and month<4)) ''',[s['trainNo1'],y-3,y-2])
#             dict_data3 = dictfetchall(cursor)
#             cursor.execute(''' SELECT sum(current4) as a4 FROM safety1 WHERE trainNo4=%s AND ((year=%s and month>3) OR (year=%s and month<4)) ''',[s['trainNo1'],y-3,y-2])
#             dict_data4 = dictfetchall(cursor)
#             cursor.execute(''' SELECT sum(current5) as a5 FROM safety1 WHERE trainNo5=%s AND ((year=%s and month>3) OR (year=%s and month<4)) ''',[s['trainNo1'],y-3,y-2])
#             dict_data5 = dictfetchall(cursor)
#             if dict_data1[0]['a1']==None:
#                 dict_data1[0]['a1']=0
#             if dict_data2[0]['a2']==None:
#                 dict_data2[0]['a2']=0
#             if dict_data3[0]['a3']==None:
#                 dict_data3[0]['a3']=0
#             if dict_data4[0]['a4']==None:
#                 dict_data4[0]['a4']=0
#             if dict_data5[0]['a5']==None:
#                 dict_data5[0]['a5']=0
#             temp['sum']=dict_data1[0]['a1']+dict_data2[0]['a2']+dict_data3[0]['a3']+dict_data4[0]['a4']+dict_data5[0]['a5']
#             temp['type']=s['trainNo1']
#             temp['year']='2019'
#             total1=total1+temp['sum']
#             safety1.append(temp)

#             # 2020-2021
#             cursor.execute(''' SELECT sum(current1) as a1 FROM safety1 WHERE trainNo1=%s AND ((year=%s and month>3) OR (year=%s and month<4)) ''',[s['trainNo1'],y-2,y-1])
#             dict_data1 = dictfetchall(cursor)
#             cursor.execute(''' SELECT sum(current2) as a2 FROM safety1 WHERE trainNo2=%s AND ((year=%s and month>3) OR (year=%s and month<4)) ''',[s['trainNo1'],y-2,y-1])
#             dict_data2 = dictfetchall(cursor)
#             cursor.execute(''' SELECT sum(current3) as a3 FROM safety1 WHERE trainNo3=%s AND ((year=%s and month>3) OR (year=%s and month<4)) ''',[s['trainNo1'],y-2,y-1])
#             dict_data3 = dictfetchall(cursor)
#             cursor.execute(''' SELECT sum(current4) as a4 FROM safety1 WHERE trainNo4=%s AND ((year=%s and month>3) OR (year=%s and month<4)) ''',[s['trainNo1'],y-2,y-1])
#             dict_data4 = dictfetchall(cursor)
#             cursor.execute(''' SELECT sum(current5) as a5 FROM safety1 WHERE trainNo5=%s AND ((year=%s and month>3) OR (year=%s and month<4)) ''',[s['trainNo1'],y-2,y-1])
#             dict_data5 = dictfetchall(cursor)
#             if dict_data1[0]['a1']==None:
#                 dict_data1[0]['a1']=0
#             if dict_data2[0]['a2']==None:
#                 dict_data2[0]['a2']=0
#             if dict_data3[0]['a3']==None:
#                 dict_data3[0]['a3']=0
#             if dict_data4[0]['a4']==None:
#                 dict_data4[0]['a4']=0
#             if dict_data5[0]['a5']==None:
#                 dict_data5[0]['a5']=0
#             temp1['sum']=dict_data1[0]['a1']+dict_data2[0]['a2']+dict_data3[0]['a3']+dict_data4[0]['a4']+dict_data5[0]['a5']
#             temp1['type']=s['trainNo1']
#             temp1['year']='2020'
#             total2=total2+temp1['sum']
#             safety1.append(temp1)

#             # 2021-2022
#             cursor.execute(''' SELECT sum(current1) as a1 FROM safety1 WHERE trainNo1=%s AND ((year=%s and month>3) OR (year=%s and month<4)) ''',[s['trainNo1'],y-1,y])
#             dict_data1 = dictfetchall(cursor)
#             cursor.execute(''' SELECT sum(current2) as a2 FROM safety1 WHERE trainNo2=%s AND ((year=%s and month>3) OR (year=%s and month<4)) ''',[s['trainNo1'],y-1,y])
#             dict_data2 = dictfetchall(cursor)
#             cursor.execute(''' SELECT sum(current3) as a3 FROM safety1 WHERE trainNo3=%s AND ((year=%s and month>3) OR (year=%s and month<4)) ''',[s['trainNo1'],y-1,y])
#             dict_data3 = dictfetchall(cursor)
#             cursor.execute(''' SELECT sum(current4) as a4 FROM safety1 WHERE trainNo4=%s AND ((year=%s and month>3) OR (year=%s and month<4)) ''',[s['trainNo1'],y-1,y])
#             dict_data4 = dictfetchall(cursor)
#             cursor.execute(''' SELECT sum(current5) as a5 FROM safety1 WHERE trainNo5=%s AND ((year=%s and month>3) OR (year=%s and month<4)) ''',[s['trainNo1'],y-1,y])
#             dict_data5 = dictfetchall(cursor)
#             if dict_data1[0]['a1']==None:
#                 dict_data1[0]['a1']=0
#             if dict_data2[0]['a2']==None:
#                 dict_data2[0]['a2']=0
#             if dict_data3[0]['a3']==None:
#                 dict_data3[0]['a3']=0
#             if dict_data4[0]['a4']==None:
#                 dict_data4[0]['a4']=0
#             if dict_data5[0]['a5']==None:
#                 dict_data5[0]['a5']=0
#             temp2['sum']=dict_data1[0]['a1']+dict_data2[0]['a2']+dict_data3[0]['a3']+dict_data4[0]['a4']+dict_data5[0]['a5']
#             temp2['type']=s['trainNo1']
#             temp2['year']='2021'
#             total3=total3+temp2['sum']
#             safety1.append(temp2)

#             # April,2021 to September,2021
#             cursor.execute(''' SELECT sum(current1) as a1 FROM safety1 WHERE trainNo1=%s AND ((year=%s and month>3) OR (year=%s and month<10)) ''',[s['trainNo1'],y-1,y-1])
#             dict_data1 = dictfetchall(cursor)
#             cursor.execute(''' SELECT sum(current2) as a2 FROM safety1 WHERE trainNo2=%s AND ((year=%s and month>3) OR (year=%s and month<10)) ''',[s['trainNo1'],y-1,y-1])
#             dict_data2 = dictfetchall(cursor)
#             cursor.execute(''' SELECT sum(current3) as a3 FROM safety1 WHERE trainNo3=%s AND ((year=%s and month>3) OR (year=%s and month<10)) ''',[s['trainNo1'],y-1,y-1])
#             dict_data3 = dictfetchall(cursor)
#             cursor.execute(''' SELECT sum(current4) as a4 FROM safety1 WHERE trainNo4=%s AND ((year=%s and month>3) OR (year=%s and month<10)) ''',[s['trainNo1'],y-1,y-1])
#             dict_data4 = dictfetchall(cursor)
#             cursor.execute(''' SELECT sum(current5) as a5 FROM safety1 WHERE trainNo5=%s AND ((year=%s and month>3) OR (year=%s and month<10)) ''',[s['trainNo1'],y-1,y-1])
#             dict_data5 = dictfetchall(cursor)
#             if dict_data1[0]['a1']==None:
#                 dict_data1[0]['a1']=0
#             if dict_data2[0]['a2']==None:
#                 dict_data2[0]['a2']=0
#             if dict_data3[0]['a3']==None:
#                 dict_data3[0]['a3']=0
#             if dict_data4[0]['a4']==None:
#                 dict_data4[0]['a4']=0
#             if dict_data5[0]['a5']==None:
#                 dict_data5[0]['a5']=0
#             temp3['sum']=dict_data1[0]['a1']+dict_data2[0]['a2']+dict_data3[0]['a3']+dict_data4[0]['a4']+dict_data5[0]['a5']
#             temp3['type']=s['trainNo1']
#             temp3['year']='PREVIOUS'
#             total4=total4+temp3['sum']
#             safety1.append(temp3)

#             # April,2022 to September,2022
#             cursor.execute(''' SELECT sum(current1) as a1 FROM safety1 WHERE trainNo1=%s AND ((year=%s and month>3) OR (year=%s and month<10)) ''',[s['trainNo1'],y,y])
#             dict_data1 = dictfetchall(cursor)
#             cursor.execute(''' SELECT sum(current2) as a2 FROM safety1 WHERE trainNo2=%s AND ((year=%s and month>3) OR (year=%s and month<10)) ''',[s['trainNo1'],y,y])
#             dict_data2 = dictfetchall(cursor)
#             cursor.execute(''' SELECT sum(current3) as a3 FROM safety1 WHERE trainNo3=%s AND ((year=%s and month>3) OR (year=%s and month<10)) ''',[s['trainNo1'],y,y])
#             dict_data3 = dictfetchall(cursor)
#             cursor.execute(''' SELECT sum(current4) as a4 FROM safety1 WHERE trainNo4=%s AND ((year=%s and month>3) OR (year=%s and month<10)) ''',[s['trainNo1'],y,y])
#             dict_data4 = dictfetchall(cursor)
#             cursor.execute(''' SELECT sum(current5) as a5 FROM safety1 WHERE trainNo5=%s AND ((year=%s and month>3) OR (year=%s and month<10)) ''',[s['trainNo1'],y,y])
#             dict_data5 = dictfetchall(cursor)
#             if dict_data1[0]['a1']==None:
#                 dict_data1[0]['a1']=0
#             if dict_data2[0]['a2']==None:
#                 dict_data2[0]['a2']=0
#             if dict_data3[0]['a3']==None:
#                 dict_data3[0]['a3']=0
#             if dict_data4[0]['a4']==None:
#                 dict_data4[0]['a4']=0
#             if dict_data5[0]['a5']==None:
#                 dict_data5[0]['a5']=0
#             temp4['sum']=dict_data1[0]['a1']+dict_data2[0]['a2']+dict_data3[0]['a3']+dict_data4[0]['a4']+dict_data5[0]['a5']
#             temp4['type']=s['trainNo1']
#             temp4['year']='CURRENT'
#             total5=total5+temp4['sum']
#             safety1.append(temp4)

#             temp_change['sum_change']=temp4['sum']-temp3['sum']
#             temp_change['type']=s['trainNo1']
#             temp_change['year']='CHANGE'
#             safety1.append(temp_change)
#         safety2['total1']=total1
#         safety2['total2']=total2
#         safety2['total3']=total3
#         safety2['total4']=total4
#         safety2['total5']=total5
#         safety2['change_total']=total5-total4
#     # END SAFETY REPORT

#     context={
#         # 'safety':safety,
#         'infrastructure_creation':infrastructure_creation,
#         'asset_reliabilty':data,
#         'loading_commodity_wise':commodity,
#         'loading_commodity_wise1':commodity1,
#         'loading_commodity_wise2':commodity2,
#         'loading_zone_wise':zone,
#         'loading_zone_wise1':zone1,
#         'loading_zone_wise2':zone2,
#         'earnings':earnings,
#         'earnings1':earnings1,
#         'earnings2':earnings2,
#         'rolling_stock_production':rolling,
#         'safety':safety,
#         'safety1':safety1,
#         'safety2':safety2,
#         # 'punctuality':punctuality,
#     }
#     return render(request, 'home_page3.html', context)

def my_edrishti(request):
    safety=list(m7.safety.objects.filter().order_by('id').values())
    infrastructure_creation=list(m7.infrastructure_creation.objects.annotate(sint=Cast('variation', FloatField())).filter().values())
    loading_commodity_wise=list(m7.loading_commodity_wise.objects.annotate(sint=Cast('var_over_target', FloatField())).filter().values())
    loading_zone_wise=list(m7.loading_zone_wise.objects.annotate(sint=Cast('var_over_target', FloatField())).filter().order_by('id').values())
    loading_b3=list(m7.loading_b3.objects.annotate(sint=Cast('increase', FloatField())).filter().order_by('id').values())
    asset_reliabilty=list(m7.asset_reliabilty.objects.filter().values())
    capex_item_wise=list(m7.capex_item_wise.objects.annotate(sint=Cast('be_mod', FloatField())).order_by('-sint').values())
    capex_head_wise=list(m7.capex_head_wise.objects.annotate(sint=Cast('be_mod', FloatField())).order_by('sint').values())
    capex_resource_wise=list(m7.capex_resource_wise.objects.annotate(sint=Cast('be_mod', FloatField())).order_by('sint').values())
    earnings=list(m7.earnings.objects.annotate(sint=Cast('increase', FloatField())).filter().order_by('id').values())
    owe=list(m7.owe.objects.annotate(sint=Cast('increase', FloatField())).filter().order_by('id').values())
    rolling_stock_production=list(m7.rolling_stock_production.objects.filter().values())   
    punctuality=list(m7.punctuality.objects.filter().values())
    punctuality_dept=list(m7.punctuality_dept.objects.filter().values())

    load=[]
    for l in loading_b3:
        if l['description'] != 'Growth':
            load.append(l)
    loading_b3=load

    cap=[]
    tot={}
    for c in capex_item_wise:
        if c['item'] != 'Total Capex':
            cap.append(c)
        else:
            tot=c
    cap.append(tot)
    capex_item_wise=cap

    current_year=int(datetime.today().strftime("%Y"))
    current_year_short=int(datetime.today().strftime("%y"))
    current_month=datetime.today().strftime("%b")
    current_month_val=int(datetime.today().strftime("%m"))
    prev_month=datetime.strptime(str(current_month_val-1),"%m").strftime("%b")
    day=int(datetime.today().strftime("%d"))
    if day < 7:
        p_month=datetime.strptime(str(current_month_val-2),"%m").strftime("%b")
    else:
        p_month=datetime.strptime(str(current_month_val-1),"%m").strftime("%b")

    safety_heads=[
        {'col1':str(current_year-3)+" - "+ str(current_year_short-2),
         'col2':str(current_year-2)+" - "+ str(current_year_short-1),
          'col3':str(current_year-1)+" - "+ str(current_year_short),
           'col4':"April "+str(current_year_short-1)+" - "+ str(prev_month)+" "+str(current_year_short),
           'col5':"April "+str(current_year_short)+" - "+ str(prev_month)+" "+str(current_year_short)},
    ]
    loading_b3_heads=[{
        'col1':str(current_year-1)+" - "+ str(current_year_short),
        'col2':str(current_year)+" - "+ str(current_year_short+1),
        'col3':prev_month+" "+str(current_year_short-1),
        'col4':prev_month+" "+str(current_year_short),
        'col5':prev_month+" "+str(current_year_short),
    }]
    loading_heads=[{
        'col1':prev_month+" "+str(current_year_short),
        'col2':prev_month+" "+str(current_year_short-1),
        'col3':prev_month+" "+str(current_year_short),
    }]
    
    capex_heads=[{
        'col1':str(current_year-1)+" - "+ str(current_year_short),
        'col2':p_month+" "+str(current_year_short-1),
        'col3':str(current_year)+" - "+ str(current_year_short+1),
        'col4':p_month+" "+str(current_year_short),
    }]
    infrastructure_heads=[{
        'col1':prev_month+" "+str(current_year_short),
    }]
    asset_reliabilty_heads=[{
        'col1':prev_month+" "+str(current_year_short-1),
        'col2':prev_month+" "+str(current_year_short),
    }]
    context={
        'prev_month':prev_month,
        'safety_heads':safety_heads,
        'safety':safety,
        'infrastructure_heads':infrastructure_heads,
        'infrastructure_creation':infrastructure_creation,
        'loading_heads':loading_heads,
        'loading_commodity_wise':loading_commodity_wise,
        'loading_zone_wise':loading_zone_wise,
        'loading_b3_heads':loading_b3_heads,
        'loading_b3':loading_b3,
        'asset_reliabilty_heads':asset_reliabilty_heads,
        'asset_reliabilty':asset_reliabilty,
        'capex_heads':capex_heads,
        'capex_item_wise':capex_item_wise,
        'capex_head_wise':capex_head_wise,
        'capex_resource_wise':capex_resource_wise,
        'earnings':earnings,
        'owe':owe,
        'rolling_stock_production':rolling_stock_production,
        'punctuality':punctuality,
        'punctuality_dept':punctuality_dept,
    }
    return render(request, 'my_edrishti.html', context)
# end

def my_edrishti1(request):
    # try:
        dates=datetime.now()
        y=dates.year
        m=dates.month
        yflag=0
        if m<4:
            yflag=1
        lm=dates.month-1
     
    # FOR PUNCTUALITY VIA API
        today= m9.LogApi.objects.filter(schedular_name='devinsapi_punctuality_service').values('dates').order_by('-dates')[0]['dates']
        today= today-relativedelta(days=1)
        punc_today=today.strftime("%d/%m/%Y")
        # print(punc_today)
        punc_lastyear = (today - relativedelta(months=12)).strftime("%d/%m/%Y")
        punc_week= (today - relativedelta(days=6)).strftime("%d/%m/%Y")
        punc_month=(today - relativedelta(days=29)).strftime("%d/%m/%Y")
        
        week = today - relativedelta(days=29)
        lastyear = today - relativedelta(months=12)
        lastweek= lastyear - relativedelta(days=29)
        # print(today,"today")
        # print(week,"week")
        # print(lastyear,"lastyear")
        # print(lastweek,"lastweek")
        
        tempvg=[]
        causecodes = ['PATH','INC','ENG','TFC','ORL','CNST','RUNO','ACC','LC','DCW']
        others =['LO','WEA','DELC','ACP','ST','PBC','RE','DDSL','ELEC','PBOL','OHE','OPLNI','CONNI','ICW','MA','COM','IDSL','IELC','AGT','PRONI']
        zone = list(m9.Punctuality_Service_Output.objects.all().values('Zone_Code').distinct())
    
        new=[{'department_code' : 'ELEC'},{'department_code' : 'RPF'},{'department_code' : 'TFC'},{'department_code' : 'COM'},{'department_code' : 'CNST'},{'department_code' : 'ST'},{'department_code' : 'MECH'},{'department_code' : 'ENG'},{'department_code': 'Others' }]
        xyz=['ELEC','RPF', 'TFC','COM','CNST','ST', 'MECH', 'ENG']
        # ['RE','INC','OPLNI','RUNO','WEA','PATH','ACC','ORL','ACP','AGT','PRONI']
        tempvg.extend(zone)
        
        o=''
        for i in range(len(tempvg)):
            try:
                nlt=0
                tc=0
                o = list(m9.Punctuality_Service_Output.objects.filter(Zone_Code = tempvg[i]['Zone_Code'],train_group ='M' , Scheduled_Date__range = [week,today]).values())
                for o_v in o:
                        # print('in',o)
                        nlt+=o_v['nlt_count']
                        tc+=o_v['train_count']
                pp=(nlt*100.0)/tc
                tempvg[i].update({"pp":round(pp,2)})
            except:
                tempvg[i].update({"pp":0})
                
        o1 =''
        for i in range(len(tempvg)):
            try:
                nlt=0
                tc=0
                o1 = list(m9.Punctuality_Service_Output.objects.filter(Zone_Code = tempvg[i]['Zone_Code'],train_group ='M' , Scheduled_Date__range = [lastweek,lastyear]).values())
                for o_v in o1:
                        # print('in',o)
                        nlt+=o_v['nlt_count']
                        tc+=o_v['train_count']
                pp=(nlt*100.0)/tc
                tempvg[i].update({"pp1":round(pp,2)})
            except:
                tempvg[i].update({"pp1":0})
        
        for i in range(len(tempvg)):
            tempvg[i].update({"variation":round((tempvg[i]['pp']-tempvg[i]['pp1']),2)}) 
        
        for i in range(len(tempvg)):
            listt=[]
            for j in range(len(causecodes)):
                try:
                    duration = list(m9.Cause_Service_Output.objects.filter(Scheduled_Date__range = [week,today],Zone_Code = tempvg[i]['Zone_Code'],cause_code = causecodes[j],train_group='M').values_list('duration',flat=True))
                    durationsum = sum(duration)
                    listt.append(durationsum)
                except:
                    listt.append(0)
            tempvg[i].update({"sumofcause":listt})
            
        for i in range(len(tempvg)):
            litt=[]
            for j in range(len(others)):
                try:
                    duration1 = list(m9.Cause_Service_Output.objects.filter(Scheduled_Date__range = [week,today],Zone_Code = tempvg[i]['Zone_Code'],cause_code = others[j],train_group='M').values_list('duration',flat=True))
                    durationsum1 = sum(duration1)
                    litt.append(durationsum1)
                except:
                    litt.append(0)
            summm = sum(litt)
            tempvg[i].update({"others":summm})
            
        for i in range(len(new)):
            newlist=[]
            if new[i]['department_code'] != "Others":
                for j in range(len(causecodes)):
                    try:
                        duration2 = list(m9.Cause_Service_Output.objects.filter(Scheduled_Date__range = [week,today],department_code = new[i]['department_code'],cause_code = causecodes[j],train_group='M').values_list('duration',flat=True))
                        durationsum2 = sum(duration2)
                        newlist.append(durationsum2)
                    except:
                        newlist.append(0)
                new[i].update({"sumofcause1":newlist})
            else:
                for j in range(len(causecodes)):
                    try:
                        duration2 = list(m9.Cause_Service_Output.objects.exclude(department_code__in=new).filter(Scheduled_Date__range = [week,today],cause_code = causecodes[j],train_group='M').values_list('duration',flat=True))
                        durationsum2 = sum(duration2)
                        newlist.append(durationsum2)
                    except:
                        newlist.append(0)
                new[i].update({"sumofcause1":newlist})
            
            
        for i in range(len(new)):
            departlistothers=[]
            if new[i]['department_code'] != "Others":
                for j in range(len(others)):
                    try:
                        durationdepart = list(m9.Cause_Service_Output.objects.filter(Scheduled_Date__range = [week,today],department_code = new[i]['department_code'],cause_code = others[j],train_group='M').values_list('duration',flat=True))
                        departdurationsum1 = sum(durationdepart)
                        departlistothers.append(departdurationsum1)
                    except:
                        departlistothers.append(0)
                summ = sum(departlistothers)
                new[i].update({"others":summ})
            else:
                for j in range(len(others)):
                    try:
                        durationdepart = list(m9.Cause_Service_Output.objects.exclude(department_code__in=xyz).filter(Scheduled_Date__range = [week,today],cause_code = others[j],train_group='M').values_list('duration',flat=True))
                        departdurationsum1 = sum(durationdepart)
                        departlistothers.append(departdurationsum1)
                    except:
                        departlistothers.append(0)
                summ5 = sum(departlistothers)
                new[i].update({"others":summ5})

        dept_punctuality={}
        dept_wise = list(m9.Cause_Service_Output.objects.values('department_code').distinct('department_code'))
        # # print("dept_wise",dept_wise)
        for i in range(len(dept_wise)):
            cnt = m9.Cause_Service_Output.objects.filter(Scheduled_Date__range = [week,today],department_code=dept_wise[i]['department_code']).count()
            dept_code = dept_wise[i]['department_code']
            # # print("dept_code",dept_code)
            # print('cnt',cnt)
            dept_punctuality.update({dept_code:{'cnt':cnt}})
        # print("dept_punctuality",dept_punctuality)
        tempvg=sorted(tempvg,key=lambda d: d['Zone_Code'] )

    # GUNJAN START LOADING
        # with connections['users'].cursor() as cursor:
        
        # FOR LOADING-COMMODITY 
            # cursor.execute('''SELECT * FROM  mcdo_commodity_wise_mst''')
            # commodity = dictfetchall(cursor)
            # ctar_total,cpre_total,ccur_total=0,0,0
            # commodity1=[]
            # commodity2={}
            # for c in commodity:
            #     temp={}
            #     cursor.execute('''SELECT sum(target_yr) as a1, sum(previous_yr) as a2, sum(current_yr) as a3, commodity_id,
            #                     (sum(current_yr)-sum(previous_yr))/sum(previous_yr)*100 as a4, (sum(current_yr)-sum(target_yr))/sum(target_yr)*100 as a5
            #                     FROM mcdo_commodity_wise_data WHERE commodity_id=%s and entry_id in (SELECT id FROM mcdo_commodity_wise_entry where financial_yr=%s)''',[c['id'],y])
            #     dict_data = dictfetchall(cursor)
            #     temp['a1']=dict_data[0]['a1']
            #     temp['a2']=dict_data[0]['a2']
            #     temp['a3']=dict_data[0]['a3']
            #     temp['a4']=dict_data[0]['a4']
            #     temp['a5']=dict_data[0]['a5']
            #     temp['commodity_id']=dict_data[0]['commodity_id']
            #     commodity1.append(temp)
            #     ctar_total=ctar_total+dict_data[0]['a1']
            #     cpre_total=cpre_total+dict_data[0]['a2']
            #     ccur_total=ccur_total+dict_data[0]['a3']
            # commodity2['tar_total']=ctar_total
            # commodity2['pre_total']=cpre_total
            # commodity2['cur_total']=ccur_total
            # commodity2['over_lasy']=(ccur_total-cpre_total)/cpre_total*100
            # commodity2['over_targ']=(ccur_total-ctar_total)/ctar_total*100
        # END LOADING-COMMODITY 

        # FOR LOADING-ZONE 
            # cursor.execute('''SELECT DISTINCT zone FROM  mcdo_commodity_wise_entry  WHERE zone!='null' ''')
            # zone = dictfetchall(cursor)
            # ztar_total,zpre_total,zcur_total=0,0,0
            # zone1=[]
            # zone2={}
            # for c in zone:
            #     try:
            #         temp={}
            #         cursor.execute('''SELECT sum(target_yr) as a1, sum(previous_yr) as a2, sum(current_yr) as a3, entry_id,
            #                         (sum(current_yr)-sum(previous_yr))/sum(previous_yr)*100 as a4, (sum(current_yr)-sum(target_yr))/sum(target_yr)*100 as a5 
            #                         FROM mcdo_commodity_wise_data where entry_id in (SELECT id FROM mcdo_commodity_wise_entry where financial_yr=%s and zone=%s)''',[y,c['zone']])
            #         dict_data = dictfetchall(cursor)
            #         temp['a1']=dict_data[0]['a1']
            #         temp['a2']=dict_data[0]['a2']
            #         temp['a3']=dict_data[0]['a3']
            #         temp['a4']=dict_data[0]['a4']
            #         temp['a5']=dict_data[0]['a5']
            #         temp['entry_id']=dict_data[0]['entry_id']
            #         temp['zone']=c['zone']
            #         zone1.append(temp)
            #         ztar_total=ztar_total+dict_data[0]['a1']
            #         zpre_total=zpre_total+dict_data[0]['a2']
            #         zcur_total=zcur_total+dict_data[0]['a3']
            #     except:
            #         temp1=0
            # zone2['tar_total']=ztar_total
            # zone2['pre_total']=zpre_total
            # zone2['cur_total']=zcur_total
            # zone2['over_lasy']=(zcur_total-zpre_total)/zpre_total*100
            # zone2['over_targ']=(zcur_total-ztar_total)/ztar_total*100
        # END LOADING-ZONE 

        # FOR FINANCIAL REPORT
            # cursor.execute('''SELECT * FROM  mcdo_financial_mst''')
            # earnings = dictfetchall(cursor)
            # etar_total,epre_total,ecur_total=0,0,0
            # earnings1=[]
            # earnings2={}
            # for c in earnings:
            #     temp={}
            #     cursor.execute('''SELECT sum(previous_yr) as a1, sum(current_month) as a2, sum(current_yr) as a3, financial_id,
            #                     sum(current_yr)-sum(current_month) as a4, sum(current_yr)-sum(previous_yr) as a5
            #                     FROM mcdo_financial_data WHERE financial_id=%s and entry_id in (SELECT id FROM mcdo_financial_entry where financial_yr=%s)''',[c['id'],y])
            #     dict_data = dictfetchall(cursor)
            #     temp['a1']=dict_data[0]['a1']
            #     temp['a2']=dict_data[0]['a2']
            #     temp['a3']=dict_data[0]['a3']
            #     temp['a4']=dict_data[0]['a4']
            #     temp['a5']=dict_data[0]['a5']
            #     temp['financial_id']=dict_data[0]['financial_id']
            #     earnings1.append(temp)
            #     etar_total=etar_total+dict_data[0]['a1']
            #     epre_total=epre_total+dict_data[0]['a2']
            #     ecur_total=ecur_total+dict_data[0]['a3']
            # earnings2['tar_total']=etar_total
            # earnings2['pre_total']=epre_total
            # earnings2['cur_total']=ecur_total
            # earnings2['over_lasy']=ecur_total-epre_total
            # earnings2['over_targ']=ecur_total-etar_total
        # END FINANCIAL REPORT
        
    # FOR SAFETY REPORT VIA SQL
            # cursor.execute('''SELECT month FROM safety1 order by month desc, year desc limit 1''')
            # mnth=cursor.fetchall()
            # month=mnth[0][0]
            # safety_month=datetime.strptime(str(int(month)),"%m").strftime("%b")
            # cursor.execute('''SELECT year FROM safety1 order by month desc, year desc limit 1''')
            # yr=cursor.fetchall()
            # year=yr[0][0]

            # cursor.execute('''SELECT DISTINCT trainNo1 FROM  safety1 WHERE trainNo1!='' order by trainNo1''')
            # safety = dictfetchall(cursor)
            # safety1=[]
            # safety2={}
            # total1,total2,total3,total4,total5=0,0,0,0,0
            # for s in safety:
            #     temp,temp1,temp2,temp3,temp4,temp_change={},{},{},{},{},{}
            #     # 2019-2020
            #     cursor.execute(''' SELECT FORMAT(ROUND(sum(current1)),'NO') as a1 FROM safety1 WHERE trainNo1=%s AND ((year=%s and month>3) OR (year=%s and month<4)) ''',[s['trainNo1'],y-3,y-2])
            #     dict_data1 = dictfetchall(cursor)
            #     cursor.execute(''' SELECT FORMAT(ROUND(sum(current2)),'NO') as a2 FROM safety1 WHERE trainNo2=%s AND ((year=%s and month>3) OR (year=%s and month<4)) ''',[s['trainNo1'],y-3,y-2])
            #     dict_data2 = dictfetchall(cursor)
            #     cursor.execute(''' SELECT FORMAT(ROUND(sum(current3)),'NO') as a3 FROM safety1 WHERE trainNo3=%s AND ((year=%s and month>3) OR (year=%s and month<4)) ''',[s['trainNo1'],y-3,y-2])
            #     dict_data3 = dictfetchall(cursor)
            #     cursor.execute(''' SELECT FORMAT(ROUND(sum(current4)),'NO') as a4 FROM safety1 WHERE trainNo4=%s AND ((year=%s and month>3) OR (year=%s and month<4)) ''',[s['trainNo1'],y-3,y-2])
            #     dict_data4 = dictfetchall(cursor)
            #     cursor.execute(''' SELECT FORMAT(ROUND(sum(current5)),'NO') as a5 FROM safety1 WHERE trainNo5=%s AND ((year=%s and month>3) OR (year=%s and month<4)) ''',[s['trainNo1'],y-3,y-2])
            #     dict_data5 = dictfetchall(cursor)
            #     if dict_data1[0]['a1']==None:
            #         dict_data1[0]['a1']=0
            #     if dict_data2[0]['a2']==None:
            #         dict_data2[0]['a2']=0
            #     if dict_data3[0]['a3']==None:
            #         dict_data3[0]['a3']=0
            #     if dict_data4[0]['a4']==None:
            #         dict_data4[0]['a4']=0
            #     if dict_data5[0]['a5']==None:
            #         dict_data5[0]['a5']=0
            #     temp['sum']=int(dict_data1[0]['a1'])+int(dict_data2[0]['a2'])+int(dict_data3[0]['a3'])+int(dict_data4[0]['a4'])+int(dict_data5[0]['a5'])
            #     temp['type']=s['trainNo1']
            #     temp['year']='2019'
            #     total1=total1+temp['sum']
            #     safety1.append(temp)

            #     # 2020-2021
            #     cursor.execute(''' SELECT FORMAT(ROUND(sum(current1)),'NO') as a1 FROM safety1 WHERE trainNo1=%s AND ((year=%s and month>3) OR (year=%s and month<4)) ''',[s['trainNo1'],y-2,y-1])
            #     dict_data1 = dictfetchall(cursor)
            #     cursor.execute(''' SELECT FORMAT(ROUND(sum(current2)),'NO') as a2 FROM safety1 WHERE trainNo2=%s AND ((year=%s and month>3) OR (year=%s and month<4)) ''',[s['trainNo1'],y-2,y-1])
            #     dict_data2 = dictfetchall(cursor)
            #     cursor.execute(''' SELECT FORMAT(ROUND(sum(current3)),'NO') as a3 FROM safety1 WHERE trainNo3=%s AND ((year=%s and month>3) OR (year=%s and month<4)) ''',[s['trainNo1'],y-2,y-1])
            #     dict_data3 = dictfetchall(cursor)
            #     cursor.execute(''' SELECT FORMAT(ROUND(sum(current4)),'NO') as a4 FROM safety1 WHERE trainNo4=%s AND ((year=%s and month>3) OR (year=%s and month<4)) ''',[s['trainNo1'],y-2,y-1])
            #     dict_data4 = dictfetchall(cursor)
            #     cursor.execute(''' SELECT FORMAT(ROUND(sum(current5)),'NO') as a5 FROM safety1 WHERE trainNo5=%s AND ((year=%s and month>3) OR (year=%s and month<4)) ''',[s['trainNo1'],y-2,y-1])
            #     dict_data5 = dictfetchall(cursor)
            #     if dict_data1[0]['a1']==None:
            #         dict_data1[0]['a1']=0
            #     if dict_data2[0]['a2']==None:
            #         dict_data2[0]['a2']=0
            #     if dict_data3[0]['a3']==None:
            #         dict_data3[0]['a3']=0
            #     if dict_data4[0]['a4']==None:
            #         dict_data4[0]['a4']=0
            #     if dict_data5[0]['a5']==None:
            #         dict_data5[0]['a5']=0
            #     temp1['sum']=int(dict_data1[0]['a1'])+int(dict_data2[0]['a2'])+int(dict_data3[0]['a3'])+int(dict_data4[0]['a4'])+int(dict_data5[0]['a5'])
            #     temp1['type']=s['trainNo1']
            #     temp1['year']='2020'
            #     total2=total2+temp1['sum']
            #     safety1.append(temp1)

            #     # 2021-2022
            #     cursor.execute(''' SELECT FORMAT(ROUND(sum(current1)),'NO') as a1 FROM safety1 WHERE trainNo1=%s AND ((year=%s and month>3) OR (year=%s and month<4)) ''',[s['trainNo1'],y-1,y])
            #     dict_data1 = dictfetchall(cursor)
            #     cursor.execute(''' SELECT FORMAT(ROUND(sum(current2)),'NO') as a2 FROM safety1 WHERE trainNo2=%s AND ((year=%s and month>3) OR (year=%s and month<4)) ''',[s['trainNo1'],y-1,y])
            #     dict_data2 = dictfetchall(cursor)
            #     cursor.execute(''' SELECT FORMAT(ROUND(sum(current3)),'NO') as a3 FROM safety1 WHERE trainNo3=%s AND ((year=%s and month>3) OR (year=%s and month<4)) ''',[s['trainNo1'],y-1,y])
            #     dict_data3 = dictfetchall(cursor)
            #     cursor.execute(''' SELECT FORMAT(ROUND(sum(current4)),'NO') as a4 FROM safety1 WHERE trainNo4=%s AND ((year=%s and month>3) OR (year=%s and month<4)) ''',[s['trainNo1'],y-1,y])
            #     dict_data4 = dictfetchall(cursor)
            #     cursor.execute(''' SELECT FORMAT(ROUND(sum(current5)),'NO') as a5 FROM safety1 WHERE trainNo5=%s AND ((year=%s and month>3) OR (year=%s and month<4)) ''',[s['trainNo1'],y-1,y])
            #     dict_data5 = dictfetchall(cursor)
            #     if dict_data1[0]['a1']==None:
            #         dict_data1[0]['a1']=0
            #     if dict_data2[0]['a2']==None:
            #         dict_data2[0]['a2']=0
            #     if dict_data3[0]['a3']==None:
            #         dict_data3[0]['a3']=0
            #     if dict_data4[0]['a4']==None:
            #         dict_data4[0]['a4']=0
            #     if dict_data5[0]['a5']==None:
            #         dict_data5[0]['a5']=0
            #     temp2['sum']=int(dict_data1[0]['a1'])+int(dict_data2[0]['a2'])+int(dict_data3[0]['a3'])+int(dict_data4[0]['a4'])+int(dict_data5[0]['a5'])
            #     temp2['type']=s['trainNo1']
            #     temp2['year']='2021'
            #     total3=total3+temp2['sum']
            #     safety1.append(temp2)

            #     # April,2021 to September,2021
            #     if yflag==0:
            #         cursor.execute(''' SELECT FORMAT(ROUND(sum(current1)),'NO') as a1 FROM safety1 WHERE trainNo1=%s AND ((year=%s and month>3) and (year=%s and month<=%s)) ''',[s['trainNo1'],y-1,y-1,month])
            #         dict_data1 = dictfetchall(cursor)
            #         cursor.execute(''' SELECT FORMAT(ROUND(sum(current2)),'NO') as a2 FROM safety1 WHERE trainNo2=%s AND ((year=%s and month>3) and (year=%s and month<=%s)) ''',[s['trainNo1'],y-1,y-1,month])
            #         dict_data2 = dictfetchall(cursor)
            #         cursor.execute(''' SELECT FORMAT(ROUND(sum(current3)),'NO') as a3 FROM safety1 WHERE trainNo3=%s AND ((year=%s and month>3) and (year=%s and month<=%s)) ''',[s['trainNo1'],y-1,y-1,month])
            #         dict_data3 = dictfetchall(cursor)
            #         cursor.execute(''' SELECT FORMAT(ROUND(sum(current4)),'NO') as a4 FROM safety1 WHERE trainNo4=%s AND ((year=%s and month>3) and (year=%s and month<=%s)) ''',[s['trainNo1'],y-1,y-1,month])
            #         dict_data4 = dictfetchall(cursor)
            #         cursor.execute(''' SELECT FORMAT(ROUND(sum(current5)),'NO') as a5 FROM safety1 WHERE trainNo5=%s AND ((year=%s and month>3) and (year=%s and month<=%s)) ''',[s['trainNo1'],y-1,y-1,month])
            #         dict_data5 = dictfetchall(cursor)
            #     else:
            #         cursor.execute(''' SELECT FORMAT(ROUND(sum(current1)),'NO') as a1 FROM safety1 WHERE trainNo1=%s AND ((year=%s and month>3) or (year=%s and month<=%s)) ''',[s['trainNo1'],y-2,y-1,month])
            #         dict_data1 = dictfetchall(cursor)
            #         cursor.execute(''' SELECT FORMAT(ROUND(sum(current2)),'NO') as a2 FROM safety1 WHERE trainNo2=%s AND ((year=%s and month>3) or (year=%s and month<=%s)) ''',[s['trainNo1'],y-2,y-1,month])
            #         dict_data2 = dictfetchall(cursor)
            #         cursor.execute(''' SELECT FORMAT(ROUND(sum(current3)),'NO') as a3 FROM safety1 WHERE trainNo3=%s AND ((year=%s and month>3) or (year=%s and month<=%s)) ''',[s['trainNo1'],y-2,y-1,month])
            #         dict_data3 = dictfetchall(cursor)
            #         cursor.execute(''' SELECT FORMAT(ROUND(sum(current4)),'NO') as a4 FROM safety1 WHERE trainNo4=%s AND ((year=%s and month>3) or (year=%s and month<=%s)) ''',[s['trainNo1'],y-2,y-1,month])
            #         dict_data4 = dictfetchall(cursor)
            #         cursor.execute(''' SELECT FORMAT(ROUND(sum(current5)),'NO') as a5 FROM safety1 WHERE trainNo5=%s AND ((year=%s and month>3) or (year=%s and month<=%s)) ''',[s['trainNo1'],y-2,y-1,month])
            #         dict_data5 = dictfetchall(cursor)

            #     if dict_data1[0]['a1']==None:
            #         dict_data1[0]['a1']=0
            #     if dict_data2[0]['a2']==None:
            #         dict_data2[0]['a2']=0
            #     if dict_data3[0]['a3']==None:
            #         dict_data3[0]['a3']=0
            #     if dict_data4[0]['a4']==None:
            #         dict_data4[0]['a4']=0
            #     if dict_data5[0]['a5']==None:
            #         dict_data5[0]['a5']=0
            #     temp3['sum']=int(dict_data1[0]['a1'])+int(dict_data2[0]['a2'])+int(dict_data3[0]['a3'])+int(dict_data4[0]['a4'])+int(dict_data5[0]['a5'])
            #     temp3['type']=s['trainNo1']
            #     temp3['year']='PREVIOUS'
            #     total4=total4+temp3['sum']
            #     safety1.append(temp3)

            #     # April,2022 to September,2022
            #     if yflag==0:
                    
            #         cursor.execute(''' SELECT FORMAT(ROUND(sum(current1)),'NO') as a1 FROM safety1 WHERE trainNo1=%s AND ((year=%s and month>3) and (year=%s and month<=%s)) ''',[s['trainNo1'],y,y,month])
            #         dict_data1 = dictfetchall(cursor)
            #         cursor.execute(''' SELECT FORMAT(ROUND(sum(current2)),'NO') as a2 FROM safety1 WHERE trainNo2=%s AND ((year=%s and month>3) and (year=%s and month<=%s)) ''',[s['trainNo1'],y,y,month])
            #         dict_data2 = dictfetchall(cursor)
            #         cursor.execute(''' SELECT FORMAT(ROUND(sum(current3)),'NO') as a3 FROM safety1 WHERE trainNo3=%s AND ((year=%s and month>3) and (year=%s and month<=%s)) ''',[s['trainNo1'],y,y,month])
            #         dict_data3 = dictfetchall(cursor)
            #         cursor.execute(''' SELECT FORMAT(ROUND(sum(current4)),'NO') as a4 FROM safety1 WHERE trainNo4=%s AND ((year=%s and month>3) and (year=%s and month<=%s)) ''',[s['trainNo1'],y,y,month])
            #         dict_data4 = dictfetchall(cursor)
            #         cursor.execute(''' SELECT FORMAT(ROUND(sum(current5)),'NO') as a5 FROM safety1 WHERE trainNo5=%s AND ((year=%s and month>3) and (year=%s and month<=%s)) ''',[s['trainNo1'],y,y,month])
            #         dict_data5 = dictfetchall(cursor)
            #     else:
            #         cursor.execute(''' SELECT FORMAT(ROUND(sum(current1)),'NO') as a1 FROM safety1 WHERE trainNo1=%s AND ((year=%s and month>3) or (year=%s and month<=%s)) ''',[s['trainNo1'],y-1,y,month])
            #         dict_data1 = dictfetchall(cursor)
            #         cursor.execute(''' SELECT FORMAT(ROUND(sum(current2)),'NO') as a2 FROM safety1 WHERE trainNo2=%s AND ((year=%s and month>3) or (year=%s and month<=%s)) ''',[s['trainNo1'],y-1,y,month])
            #         dict_data2 = dictfetchall(cursor)
            #         cursor.execute(''' SELECT FORMAT(ROUND(sum(current3)),'NO') as a3 FROM safety1 WHERE trainNo3=%s AND ((year=%s and month>3) or (year=%s and month<=%s)) ''',[s['trainNo1'],y-1,y,month])
            #         dict_data3 = dictfetchall(cursor)
            #         cursor.execute(''' SELECT FORMAT(ROUND(sum(current4)),'NO') as a4 FROM safety1 WHERE trainNo4=%s AND ((year=%s and month>3) or (year=%s and month<=%s)) ''',[s['trainNo1'],y-1,y,month])
            #         dict_data4 = dictfetchall(cursor)
            #         cursor.execute(''' SELECT FORMAT(ROUND(sum(current5)),'NO') as a5 FROM safety1 WHERE trainNo5=%s AND ((year=%s and month>3) or (year=%s and month<=%s)) ''',[s['trainNo1'],y-1,y,month])
            #         dict_data5 = dictfetchall(cursor)            
            #     if dict_data1[0]['a1']==None:
            #         dict_data1[0]['a1']=0
            #     if dict_data2[0]['a2']==None:
            #         dict_data2[0]['a2']=0
            #     if dict_data3[0]['a3']==None:
            #         dict_data3[0]['a3']=0
            #     if dict_data4[0]['a4']==None:
            #         dict_data4[0]['a4']=0
            #     if dict_data5[0]['a5']==None:
            #         dict_data5[0]['a5']=0
            #     temp4['sum']=int(dict_data1[0]['a1'])+int(dict_data2[0]['a2'])+int(dict_data3[0]['a3'])+int(dict_data4[0]['a4'])+int(dict_data5[0]['a5'])
            #     temp4['type']=s['trainNo1']
            #     temp4['year']='CURRENT'
            #     total5=total5+temp4['sum']
            #     safety1.append(temp4)

            #     temp_change['sum_change']=temp4['sum']-temp3['sum']
            #     temp_change['type']=s['trainNo1']
            #     temp_change['year']='CHANGE'
            #     safety1.append(temp_change)
            # safety2['total1']=total1
            # safety2['total2']=total2
            # safety2['total3']=total3
            # safety2['total4']=total4
            # safety2['total5']=total5
            # safety2['change_total']=total5-total4
        # END SAFETY REPORT

    # FOR INFRASTRUCTURE
        with connections['users'].cursor() as cursor:
            cursor.execute('''SELECT  distinct zone FROM cms_mcdo_crucial_infra_works WHERE zone!=%s''',['CORE'])
            infra_zone=dictfetchall(cursor)
            double,electric,gauge,lines,track=0,0,0,0,0
            double1,electric1,gauge1,lines1,track1=0,0,0,0,0
            double2,electric2,gauge2,lines2,track2=0,0,0,0,0
            double3,electric3,gauge3,lines3,track3=0,0,0,0,0
            cursor.execute('''SELECT  MAX(year) FROM cms_mcdo_crucial_infra_works''')
            infra_year=int(dictfetchall(cursor)[0]['MAX(year)'])
            cursor.execute('''SELECT   MAX(cast(month AS DECIMAL(2,0))) as 'MAX(month)' FROM cms_mcdo_crucial_infra_works WHERE year=%s''',[infra_year])
            month=int(dictfetchall(cursor)[0]['MAX(month)'])
            infra_month=datetime.strptime(str(month),"%m").strftime("%b")
            financial_year=infra_year
            if month<4:
                financial_year=infra_year-1

            print(financial_year,infra_year, "infra yay")


            # for i in infra_zone:
            #     cursor.execute('''SELECT sum(C_D_target)+sum(P_D_target) as a1, count(C_D_target) as a2 FROM cms_mcdo_crucial_infra_works 
            #             WHERE year=%s AND zone=%s AND month=4 AND month<%s AND C_D_target!=0 ''',[y,i['zone'],m])
            #     infra_list=dictfetchall(cursor)                                                                                                                                                                                                             
            #     if infra_list[0]['a1']!=None and infra_list[0]['a2']!=None:
            #         double=double+(infra_list[0]['a1']/infra_list[0]['a2'])
            #         double1=double*(month-4)/12

            #     cursor.execute('''SELECT sum(C_E_target)+sum(P_E_target) as a3, count(C_E_target) as a4 FROM cms_mcdo_crucial_infra_works 
            #             WHERE year=%s AND zone=%s AND month=4 AND month<%s AND C_E_target!=0 ''',[y,i['zone'],m]) 
            #     infra_list=dictfetchall(cursor)
            #     if infra_list[0]['a3']!=None and infra_list[0]['a4']!=None:
            #         electric=electric+(infra_list[0]['a3']/infra_list[0]['a4'])
            #         electric1=electric*(month-4)/12
                
            #     cursor.execute('''SELECT sum(C_GC_target)+sum(P_GC_target) as a5, count(C_GC_target) as a6 FROM cms_mcdo_crucial_infra_works 
            #             WHERE year=%s AND zone=%s AND month=4 AND month<%s AND C_GC_target!=0 ''',[y,i['zone'],m])
            #     infra_list=dictfetchall(cursor)
            #     if infra_list[0]['a5']!=None and infra_list[0]['a6']!=None:
            #         gauge=gauge+(infra_list[0]['a5']/infra_list[0]['a6'])
            #         gauge1=gauge*(month-4)/12
                
            #     cursor.execute('''SELECT sum(C_NL_target)+sum(P_NL_target) as a7, count(C_NL_target) as a8 FROM cms_mcdo_crucial_infra_works 
            #             WHERE year=%s AND zone=%s AND month=4 AND month<%s AND C_NL_target!=0 ''',[y,i['zone'],m])
            #     infra_list=dictfetchall(cursor)
            #     if infra_list[0]['a7']!=None and infra_list[0]['a8']!=None:
            #         lines=lines+(infra_list[0]['a7']/infra_list[0]['a8'])
            #         lines1=lines*(month-4)/12
                
            #     cursor.execute('''SELECT sum(C_TR_target)+sum(P_TR_target) as a9, count(C_TR_target) as a10 FROM cms_mcdo_crucial_infra_works 
            #             WHERE year=%s AND zone=%s AND month=4 AND month<%s AND C_TR_target!=0 ''',[y,i['zone'],m])
            #     infra_list=dictfetchall(cursor)
            #     if infra_list[0]['a9']!=None and infra_list[0]['a10']!=None:
            #         track=track+(infra_list[0]['a9']/infra_list[0]['a10'])
            #         track1=track*(month-4)/12

            #     cursor.execute(''' SELECT sum(C_D_Progress)+sum(P_D_Progress) as a1, 
            #                     sum(C_E_Progress)+sum(P_E_Progress) as a2,
            #                     sum(C_GC_Progress)+sum(P_GC_Progress) as a3,
            #                     sum(C_NL_Progress)+sum(P_NL_Progress) as a4,
            #                     sum(C_TR_Progress)+sum(P_TR_Progress) as a5
            #                     FROM cms_mcdo_crucial_infra_works WHERE year=%s AND (month>3 AND month<%s) AND zone!=%s''',[y,month,'CORE'])
            #     infra_list1=dictfetchall(cursor)
                
            #     if infra_list1[0]['a1']!=None:
            #         double2=infra_list1[0]['a1']
            #         if double1!=0:
            #             double3=(double2-double1)/double1*100

            #     if infra_list1[0]['a2']!=None:
            #         electric2=infra_list1[0]['a2']
            #         if electric1!=0:
            #             electric3=(electric2-electric1)/electric1*100

            #     if infra_list1[0]['a3']!=None:
            #         gauge2=infra_list1[0]['a3']
            #         if gauge1!=0:
            #             gauge3=(gauge2-gauge1)/gauge1*100

            #     if infra_list1[0]['a4']!=None:
            #         lines2=infra_list1[0]['a4']
            #         if lines1!=0:
            #             lines3=(lines2-lines1)/lines1*100

            #     if infra_list1[0]['a5']!=None:
            #         track2=infra_list1[0]['a5']
            #         if track1!=0:
            #             track3=(track2-track1)/track1*100
            
            # cursor.execute(''' SELECT sum(C_D_target)+sum(P_D_target) as a1,
            #                   sum(C_E_target)+sum(P_E_target) as a3,
            #                   sum(C_GC_target)+sum(P_GC_target) as a5,
            #                   sum(C_NL_target)+sum(P_NL_target) as a7,
            #                   sum(C_TR_target)+sum(P_TR_target) as a9
            #                   FROM cms_mcdo_crucial_infra_works 
            #                   WHERE year=%s AND zone!=%s AND month>3 ''',[y,'CORE'])


            if financial_year==infra_year:
                cursor.execute(''' SELECT sum(C_D_target)+sum(P_D_target) as a1,
                                sum(C_E_target)+sum(P_E_target) as a3,
                                sum(C_GC_target)+sum(P_GC_target) as a5,
                                sum(C_NL_target)+sum(P_NL_target) as a7,
                                sum(C_TR_target)+sum(P_TR_target) as a9 
                                FROM(SELECT zone,
                                max(cast(C_D_Target AS DECIMAL(8,2)))as C_D_target,max(cast(P_D_Target AS DECIMAL(8,2)))as P_D_target,
                                max(cast(C_E_Target AS DECIMAL(8,2)))as C_E_target,max(cast(P_E_Target AS DECIMAL(8,2)))as P_E_target,
                                max(cast(C_gc_Target AS DECIMAL(8,2)))as C_gc_target,max(cast(P_gc_Target AS DECIMAL(8,2)))as P_gc_target,
                                max(cast(C_nl_Target AS DECIMAL(8,2)))as C_nl_target,max(cast(P_nl_Target AS DECIMAL(8,2)))as P_nl_target,
                                max(cast(C_Tr_Target AS DECIMAL(8,2)))as C_Tr_target,max(cast(P_Tr_Target AS DECIMAL(8,2)))as P_Tr_target
                                FROM `cris-cr`.cms_mcdo_crucial_infra_works where year=%s and month>3 and zone!=%s and zone!=%s group by zone) as table1 ''',[financial_year,'CORE','MTP'])
            else:
                cursor.execute(''' SELECT sum(C_D_target)+sum(P_D_target) as a1,
                                sum(C_E_target)+sum(P_E_target) as a3,
                                sum(C_GC_target)+sum(P_GC_target) as a5,
                                sum(C_NL_target)+sum(P_NL_target) as a7,
                                sum(C_TR_target)+sum(P_TR_target) as a9 
                                FROM(SELECT zone,
                                max(cast(C_D_Target AS DECIMAL(8,2)))as C_D_target,max(cast(P_D_Target AS DECIMAL(8,2)))as P_D_target,
                                max(cast(C_E_Target AS DECIMAL(8,2)))as C_E_target,max(cast(P_E_Target AS DECIMAL(8,2)))as P_E_target,
                                max(cast(C_gc_Target AS DECIMAL(8,2)))as C_gc_target,max(cast(P_gc_Target AS DECIMAL(8,2)))as P_gc_target,
                                max(cast(C_nl_Target AS DECIMAL(8,2)))as C_nl_target,max(cast(P_nl_Target AS DECIMAL(8,2)))as P_nl_target,
                                max(cast(C_Tr_Target AS DECIMAL(8,2)))as C_Tr_target,max(cast(P_Tr_Target AS DECIMAL(8,2)))as P_Tr_target
                                FROM `cris-cr`.cms_mcdo_crucial_infra_works where ((year=%s and month>3) or (year=%s and month<4)) and zone!=%s and zone!=%s group by zone) as table1 ''',[financial_year,infra_year,'CORE','MTP'])


            infra_list=dictfetchall(cursor)
            if month<4:
                mon=month+13
            else:
                mon=month+1
            if infra_list[0]['a1']!=None:
                    # print(type(infra_list[0]['a1']))
                    double=double+(infra_list[0]['a1'])
                    double1=double*(mon-4)/12

            if infra_list[0]['a3']!=None:
                    electric=electric+(infra_list[0]['a3'])
                    electric1=electric*(mon-4)/12

            if infra_list[0]['a5']!=None:
                    gauge=gauge+(infra_list[0]['a5'])
                    gauge1=gauge*(mon-4)/12

            if infra_list[0]['a7']!=None:
                    lines=lines+(infra_list[0]['a7'])
                    lines1=lines*(mon-4)/12

            if infra_list[0]['a9']!=None:
                    track=track+(infra_list[0]['a9'])
                    track1=track*(mon-4)/12

            # cursor.execute(''' SELECT sum(C_D_Progress)+sum(P_D_Progress) as a1, 
            #                     sum(C_E_Progress)+sum(P_E_Progress) as a2,
            #                     sum(C_GC_Progress)+sum(P_GC_Progress) as a3,
            #                     sum(C_NL_Progress)+sum(P_NL_Progress) as a4,
            #                     sum(C_TR_Progress)+sum(P_TR_Progress) as a5,
            #                      FROM (select cast(C_D_Progress AS DECIMAL(8,2))as C_D_Progress, cast(P_D_Progress AS DECIMAL(8,2)) as P_D_Progress,
            #                      cast(C_E_Progress AS DECIMAL(8,2))as C_E_Progress,cast(P_E_Progress AS DECIMAL(8,2))as P_E_Progress,
            #                      cast(C_gc_Progress  AS DECIMAL(8,2))as C_gc_Progress,cast(P_gc_Progress  AS DECIMAL(8,2))as P_gc_Progress,
            #                      cast(C_nl_Progress  AS DECIMAL(8,2))as C_nl_Progress,cast(P_nl_Progress  AS DECIMAL(8,2))as P_nl_Progress,
            #                      cast(C_Tr_Progress  AS DECIMAL(8,2))as C_Tr_Progress,cast(P_Tr_Progress  AS DECIMAL(8,2))as P_Tr_Progress
            #                      FROM `cris-cr`.cms_mcdo_crucial_infra_works where year=%s AND (month>3 AND month<%s) AND zone!=%s) as table2 ''',[y,month,'CORE'])
        
            if financial_year==infra_year:
                cursor.execute(''' SELECT sum(C_D_Progress)+sum(P_D_Progress) as a1, 
                                    sum(C_E_Progress)+sum(P_E_Progress) as a2,
                                    sum(C_GC_Progress)+sum(P_GC_Progress) as a3,
                                    sum(C_NL_Progress)+sum(P_NL_Progress) as a4,
                                    sum(C_TR_Progress)+sum(P_TR_Progress) as a5
                                    FROM `cris-cr`.cms_mcdo_crucial_infra_works where year=%s AND (month>3 AND month<=%s) AND (zone!=%s and zone!=%s) ''',[financial_year,month,'CORE','MTP'])

            else:
                cursor.execute(''' SELECT sum(C_D_Progress)+sum(P_D_Progress) as a1, 
                                    sum(C_E_Progress)+sum(P_E_Progress) as a2,
                                    sum(C_GC_Progress)+sum(P_GC_Progress) as a3,
                                    sum(C_NL_Progress)+sum(P_NL_Progress) as a4,
                                    sum(C_TR_Progress)+sum(P_TR_Progress) as a5
                                    FROM `cris-cr`.cms_mcdo_crucial_infra_works where (year=%s AND (month>3 AND month<%s)) or (year=%s AND month<%s) AND (zone!=%s and zone!=%s) ''',[financial_year,13,infra_year,month,'CORE','MTP'])

            infra_list1=dictfetchall(cursor)
            cursor.close()   
            if infra_list1[0]['a1']!=None:
                    double2=Decimal(infra_list1[0]['a1'])
                    # print(type(double2))
                    if double1!=0:
                        double3=(double2-double1)/double1*100

            if infra_list1[0]['a2']!=None:
                    electric2=Decimal(infra_list1[0]['a2'])
                    if electric1!=0:
                        electric3=(electric2-electric1)/electric1*100

            if infra_list1[0]['a3']!=None:
                    gauge2=Decimal(infra_list1[0]['a3'])
                    if gauge1!=0:
                        gauge3=(gauge2-gauge1)/gauge1*100

            if infra_list1[0]['a4']!=None:
                    lines2=Decimal(infra_list1[0]['a4'])
                    if lines1!=0:
                        lines3=(lines2-lines1)/lines1*100

            if infra_list1[0]['a5']!=None:
                    track2=Decimal(infra_list1[0]['a5'])
                    if track1!=0:
                        track3=(track2-track1)/track1*100

            infrastructure=[{'h1':"Doubling",'target':round(double,2),'cumm':round(double1,2),'achieve':round(double2,2),'variation':round(double3,2)},
                            {'h1':"Electrification",'target':round(electric,2),'cumm':round(electric1,2),'achieve':round(electric2,2),'variation':round(electric3,2)},
                            {'h1':"Gauge Conversions",'target':round(gauge,2),'cumm':round(gauge1,2),'achieve':round(gauge2,2),'variation':round(gauge3,2)},
                            {'h1':"New Lines",'target':round(lines,2),'cumm':round(lines1,2),'achieve':round(lines2,2),'variation':round(lines3,2)},
                            {'h1':"Track Renewals",'target':round(track,2),'cumm':round(track1,2),'achieve':round(track2,2),'variation':round(track3,2)}]

    # FOR COAL & PORT DATA VIA ESB (irpsm_workplan_mstr)  
        from django.db.models import Max 
        # coal and port
            # max_updatedate = m1.irpsm_workplan_mstr.objects.aggregate(Max('updatedate'))['updatedate__max']
        max_updatedate = m1.irpsm_workplan_mstr.objects.filter(work_category__contains='Coal').aggregate(Max('receiving_time'))['receiving_time__max']
        # # print("66666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666",max_updatedate)
        coal=list(m1.irpsm_workplan_mstr.objects.filter(work_category__contains='Coal',receiving_time=max_updatedate).values())
        # # print(len(coal))
        max_updatedate = m1.irpsm_workplan_mstr.objects.filter(work_category__contains='Port').aggregate(Max('receiving_time'))['receiving_time__max']
        # # print(max_updatedate)
        port=list(m1.irpsm_workplan_mstr.objects.filter(work_category__contains='Port',receiving_time=max_updatedate).values())
        # port=list(m1.irpsm_workplan_mstr.objects.filter(work_category__contains='Port').values())

    # FOR CAPEX
        # capex_item_wise=[]
        # cap=[]
        # tot={}
        # for c in capex_item_wise:
        #     if c['item'] != 'Total Capex':
        #         cap.append(c)
        #     else:
        #         tot=c
        # cap.append(tot)
        # capex_item_wise=cap

        

        # safety_heads=[
        #     {'col1':str(current_year-3)+" - "+ str(current_year_short-2),
        #      'col2':str(current_year-2)+" - "+ str(current_year_short-1),
        #       'col3':str(current_year-1)+" - "+ str(current_year_short),
        #        'col4':"April "+str(current_year_short-1)+" - "+ str(safety_month)+" "+str(current_year_short-1),
        #        'col5':"April "+str(current_year_short)+" - "+ str(safety_month)+" "+str(current_year_short)},
        # ]

        # loading_heads=[{
        #     'col1':prev_month+" "+str(current_year_short),
        #     'col2':prev_month+" "+str(current_year_short-1),
        #     'col3':prev_month+" "+str(current_year_short),
        # }]

        # infrastructure_heads=[{
        #     'col1':infra_month+" "+str(current_year_short),
        # }]

        # asset_reliabilty_heads=[{
        #     'col1':prev_month+" "+str(current_year_short-1),
        #     'col2':prev_month+" "+str(current_year_short),
        # }]
   
    # FOR ROLLING STOCK BY VISHNU SIR
        # with connections['users'].cursor() as cursor:
        #     # cursor.execute('''SELECT "mou_sub"."name", "mou_sub"."unit", "mou_sub"."id" FROM "mou_sub" WHERE "mou_sub"."main_id" = 4''')
        #     cursor.execute('''SELECT name, unit, id FROM `cris-cr`.mou_sub WHERE main_id = 4''')
        #     rolling = dictfetchall(cursor)
        #     for i in range(len(rolling)):
        #         if rolling[i]['id'] in [40,41,42,43,44,45, 46,47,48]:
        #             #################### for target ##################
        #             # cursor.execute('''SELECT "mou_sub_target"."target" FROM "mou_sub_target" WHERE ("mou_sub_target"."entry_id" = {target} AND "mou_sub_target"."sub_id" = 4)'''.format(target = rolling[i]['id']))
        #             #cursor.execute('''SELECT target FROM  `cris-cr`.mou_sub_target WHERE (sub_id = {target})'''.format(target = rolling[i]['id']))
        #             #cursor.execute('''SELECT sum(cumm) as unit FROM  `cris-cr`.mou_sub_cumm WHERE (sub_id ={target} and entry_id in (SELECT id FROM `cris-cr`.mou_entry where year={y}) )'''.format(target = rolling[i]['id'],y=y-1))
        #             cursor.execute('''SELECT sum(performance) as unit FROM  `cris-cr`.mou_sub_data WHERE (sub_id ={target} and entry_id in (SELECT id FROM `cris-cr`.mou_entry where year={y}) )'''.format(target = rolling[i]['id'],y=y))
        #             target = dictfetchall(cursor)
        #             if target:
        #                 rolling[i].update(target[0])
        #             else:
        #                 rolling[i].update({'target':'0'}) 
        #             #################### for performance #############
        #             #cursor.execute('''SELECT "mou_sub_data"."performance" FROM "mou_sub_data" WHERE ("mou_sub_data"."entry_id" = {performance} AND "mou_sub_data"."sub_id" = 4)'''.format(performance = rolling[i]['id']))    
        #             #cursor.execute('''SELECT performance FROM `cris-cr`.mou_sub_data WHERE (sub_id = {performance})'''.format(performance = rolling[i]['id']))    
        #             #cursor.execute('''SELECT sum(cumm) as target FROM  `cris-cr`.mou_sub_cumm WHERE (sub_id ={target} and entry_id in (SELECT id FROM `cris-cr`.mou_entry where year={y}) )'''.format(target = rolling[i]['id'],y=y))
        #             cursor.execute('''SELECT sum(cumm) as target FROM  `cris-cr`.mou_sub_cumm_pre_yr WHERE (sub_id ={target} and entry_id in (SELECT id FROM `cris-cr`.mou_entry where year={y}) )'''.format(target = rolling[i]['id'],y=y))
        #             performance = dictfetchall(cursor)
        #             if performance:
        #                 rolling[i].update(performance[0])
        #             else:
        #                 rolling[i].update({'performance':'0'})
        #             #################### for cummn month ############
        #             #cursor.execute('''SELECT "mou_sub_cumm"."cumm" as cumm_month FROM "mou_sub_cumm" WHERE ("mou_sub_cumm"."entry_id" =4 AND "mou_sub_cumm"."sub_id" =  {cumm})'''.format(cumm = rolling[i]['id']))    
        #             # cursor.execute('''SELECT cumm  as cumm_month FROM `cris-cr`.mou_sub_cumm WHERE (sub_id = {cumm})'''.format(cumm = rolling[i]['id']))    
        #             #cursor.execute('''SELECT cumm  as cumm_month FROM `cris-cr`.mou_sub_cumm WHERE (sub_id = {cumm} and entry_id in  (SELECT id FROM `cris-cr`.mou_entry where month={m} and year={y} ))'''.format(cumm = rolling[i]['id'],m=m-1, y=y-1)) 
                
                
        #             cursor.execute('''SELECT sum(performance)  as cumm_month FROM `cris-cr`.mou_sub_data WHERE (sub_id = {cumm} and entry_id in  (SELECT id FROM `cris-cr`.mou_entry where month={m} and year={y}))'''.format(cumm = rolling[i]['id'],m=m-2, y=y))    
        #             cummn = dictfetchall(cursor)
        #             if cummn:
        #                 rolling[i].update(cummn[0])
        #             else:
        #                 rolling[i].update({'cumm_month':'0'})

                        
        #             #################### for cummn Year ##############
        #             # cursor.execute('''SELECT "mou_sub_cumm_pre_yr"."cumm" as cumm_year FROM "mou_sub_cumm_pre_yr" WHERE ("mou_sub_cumm_pre_yr"."entry_id" = 4 AND "mou_sub_cumm_pre_yr"."sub_id" = {cummperyr})'''.format(cummperyr = rolling[i]['id']))    
        #             #cursor.execute('''SELECT cumm as cumm_year FROM `cris-cr`.mou_sub_cumm_pre_yr WHERE (sub_id = {cummperyr})'''.format(cummperyr = rolling[i]['id']))    
        #             #cursor.execute('''SELECT cumm  as cumm_year FROM `cris-cr`.mou_sub_cumm WHERE (sub_id = {cumm} and entry_id in  (SELECT id FROM `cris-cr`.mou_entry where month={m}))'''.format(cumm = rolling[i]['id'],m=m))    
        #             cursor.execute('''SELECT performance  as cumm_year FROM `cris-cr`.mou_sub_data WHERE (sub_id = {cumm} and entry_id in  (SELECT id FROM `cris-cr`.mou_entry where month={m} and year={y}))'''.format(cumm = rolling[i]['id'],m=m-2, y=y))    
        #             cummperyear = dictfetchall(cursor)
        #             if cummperyear:
        #                 rolling[i].update(cummperyear[0])
        #             else:
        #                 rolling[i].update({'cumm_year':'0'})
        # VISHNU END

    # FAISAL START FOR ASSET RELIABILITY VIA SQL
        # with connections['users'].cursor() as cursor:
        #     #cursor.execute('''SELECT "home_page_mousub"."name", "home_page_mousub"."unit", "home_page_mousub"."id" FROM "home_page_mousub" WHERE "home_page_mousub"."main_id" = 6''')
        #     cursor.execute('''SELECT name, unit, id FROM `cris-cr`.mou_sub WHERE main_id = 6''')
        #     data = dictfetchall(cursor)
        #     for i in range(len(data)):
        #         if data[i]['id'] in [56,57,58,59]:
        #             #################### for target ##################
        #             #cursor.execute('''SELECT "home_page_mousubtarget"."target" FROM "home_page_mousubtarget" WHERE ("home_page_mousubtarget"."entry_id" = {target} AND "home_page_mousubtarget"."sub_id" = 6)'''.format(target = data[i]['id']))
        #             #cursor.execute('''SELECT target FROM  `cris-cr`.mou_sub_target WHERE (sub_id ={target}  )'''.format(target = data[i]['id']))
        #             cursor.execute('''SELECT sum(cumm) as unit FROM  `cris-cr`.mou_sub_cumm_pre_yr WHERE (sub_id ={target} and entry_id in (SELECT id FROM `cris-cr`.mou_entry where year={y}) )'''.format(target = data[i]['id'],y=y))
        #             target = dictfetchall(cursor)
        #             if target:
        #                 data[i].update(target[0])
        #             else:
        #                 data[i].update({'target':'0'})              
        #             #################### for performance #############
        #             #cursor.execute('''SELECT "home_page_mousubdata"."performance" FROM "home_page_mousubdata" WHERE ("home_page_mousubdata"."entry_id" = {performance} AND "home_page_mousubdata"."sub_id" = 6)'''.format(performance = data[i]['id']))    
        #             #cursor.execute('''SELECT SUM(cumm) FROM `cris-cr`.mou_sub_cumm WHERE (sub_id =  {performance} and entry_id in (SELECT id FROM `cris-cr`.mou_entry where month <= 4  AND month >= {lm}))'''.format(performance = data[i]['id'],lm = lm))    
        #             cursor.execute('''SELECT sum(cumm) as target FROM  `cris-cr`.mou_sub_cumm WHERE (sub_id ={target} and entry_id in (SELECT id FROM `cris-cr`.mou_entry where year={y}) )'''.format(target = data[i]['id'],y=y))
        #             performance = dictfetchall(cursor)
        #             if performance:
        #                 data[i].update(performance[0])
        #             else:
        #                 data[i].update({'performance':'0'})
        #             #################### for cummn month ############
        #             #cursor.execute('''SELECT "home_page_mousubcumm"."cumm" as cumm_month FROM "home_page_mousubcumm" WHERE ("home_page_mousubcumm"."entry_id" = {cumm} AND "home_page_mousubcumm"."sub_id" = 6)'''.format(cumm = data[i]['id']))    
        #             cursor.execute('''SELECT sum(cumm)  as cumm_month FROM `cris-cr`.mou_sub_cumm_pre_yr WHERE (sub_id = {cumm} and entry_id in  (SELECT id FROM `cris-cr`.mou_entry where month={m} and year={y}))'''.format(cumm = data[i]['id'],m=m-2, y=y))    
        #             cummn = dictfetchall(cursor)
        #             if cummn:
        #                 data[i].update(cummn[0])
        #             else:
        #                 data[i].update({'cumm_month':'0'})
        #             #################### for cummn Year ##############
        #             #cursor.execute('''SELECT "home_page_mousubcummpreyr"."cumm" as cumm_year FROM "home_page_mousubcummpreyr" WHERE ("home_page_mousubcummpreyr"."entry_id" = 6 AND "home_page_mousubcummpreyr"."sub_id" = {cummperyr})'''.format(cummperyr = data[i]['id']))    
        #             #cursor.execute('''SELECT cumm as cumm_year FROM `cris-cr`.mou_sub_cumm_pre_yr WHERE (sub_id = {cummperyr})'''.format(cummperyr = data[i]['id']))    
        #             cursor.execute('''SELECT cumm  as cumm_year FROM `cris-cr`.mou_sub_cumm WHERE (sub_id = {cumm} and entry_id in  (SELECT id FROM `cris-cr`.mou_entry where month={m} and year={y}))'''.format(cumm = data[i]['id'],m=m-2, y=y))    
        #             cummperyear = dictfetchall(cursor)
        #             if cummperyear:
        #                 data[i].update(cummperyear[0])
        #             else:
        #                 data[i].update({'cumm_year':'0'})
        #         elif data[i]['id'] in [55,60,61,62,63,64]:
        #             #################### for target ##################
        #             #cursor.execute('''SELECT "home_page_mousubtarget"."target" FROM "home_page_mousubtarget" WHERE ("home_page_mousubtarget"."entry_id" = {target} AND "home_page_mousubtarget"."sub_id" = 6)'''.format(target = data[i]['id']))
        #             #cursor.execute('''SELECT target FROM  `cris-cr`.mou_sub_target WHERE (sub_id ={target}  )'''.format(target = data[i]['id']))
        #             cursor.execute('''SELECT sum(cumm) as unit FROM  `cris-cr`.mou_sub_cumm_pre_yr WHERE (sub_id ={target} and entry_id in (SELECT id FROM `cris-cr`.mou_entry where year={y}) )'''.format(target = data[i]['id'],y=y))
        #             target = dictfetchall(cursor)
        #             if target:
        #                 data[i].update(target[0])
        #             else:
        #                 data[i].update({'target':'0'})
        #             #################### for performance #############
        #             #cursor.execute('''SELECT "home_page_mousubdata"."performance" FROM "home_page_mousubdata" WHERE ("home_page_mousubdata"."entry_id" = {performance} AND "home_page_mousubdata"."sub_id" = 6)'''.format(performance = data[i]['id']))    
        #             #cursor.execute('''SELECT SUM(cumm) FROM `cris-cr`.mou_sub_cumm WHERE (sub_id =  {performance} and entry_id in (SELECT id FROM `cris-cr`.mou_entry where month <= 4  AND month >= {lm}))'''.format(performance = data[i]['id'],lm = lm))    
        #             cursor.execute('''SELECT sum(performance) as target FROM  `cris-cr`.mou_sub_data WHERE (sub_id ={target} and entry_id in (SELECT id FROM `cris-cr`.mou_entry where year={y}) )'''.format(target = data[i]['id'],y=y))
        #             performance = dictfetchall(cursor)
        #             if performance:
        #                 data[i].update(performance[0])
        #             else:
        #                 data[i].update({'performance':'0'})
        #             #################### for cummn month ############
        #             #cursor.execute('''SELECT "home_page_mousubcumm"."cumm" as cumm_month FROM "home_page_mousubcumm" WHERE ("home_page_mousubcumm"."entry_id" = {cumm} AND "home_page_mousubcumm"."sub_id" = 6)'''.format(cumm = data[i]['id']))    
        #             cursor.execute('''SELECT sum(cumm)  as cumm_month FROM `cris-cr`.mou_sub_cumm_pre_yr WHERE (sub_id = {cumm} and entry_id in  (SELECT id FROM `cris-cr`.mou_entry where month={m} and year={y}))'''.format(cumm = data[i]['id'],m=m-2, y=y))    
        #             cummn = dictfetchall(cursor)
        #             if cummn:
        #                 data[i].update(cummn[0])
        #             else:
        #                 data[i].update({'cumm_month':'0'})
        #             #################### for cummn Year ##############
        #             #cursor.execute('''SELECT "home_page_mousubcummpreyr"."cumm" as cumm_year FROM "home_page_mousubcummpreyr" WHERE ("home_page_mousubcummpreyr"."entry_id" = 6 AND "home_page_mousubcummpreyr"."sub_id" = {cummperyr})'''.format(cummperyr = data[i]['id']))    
        #             #cursor.execute('''SELECT cumm as cumm_year FROM `cris-cr`.mou_sub_cumm_pre_yr WHERE (sub_id = {cummperyr})'''.format(cummperyr = data[i]['id']))    
        #             cursor.execute('''SELECT performance  as cumm_year FROM `cris-cr`.mou_sub_data WHERE (sub_id = {cumm} and entry_id in  (SELECT id FROM `cris-cr`.mou_entry where month={m} and year={y}))'''.format(cumm = data[i]['id'],m=m-2, y=y))    
        #             cummperyear = dictfetchall(cursor)
        #             if cummperyear:
        #                 data[i].update(cummperyear[0])
        #             else:
        #                 data[i].update({'cumm_year':'0'})
        # FAISAL END

    # FOR DYNAMIC HEADINGS
        current_year=int(datetime.today().strftime("%Y"))
        current_year_short=int(datetime.today().strftime("%y"))
        current_month=datetime.today().strftime("%b")
        current_month_val=int(datetime.today().strftime("%m"))
        # print(current_month_val)
        prev_month=datetime.now() - relativedelta(months=1)
        prev_month=int(prev_month.strftime("%m"))
        prev_month=datetime.strptime(str(prev_month),"%m").strftime("%b")
        
        back_month=datetime.now() - relativedelta(months=2)
        back_month=int(back_month.strftime("%m"))
        day=int(datetime.today().strftime("%d"))
        if day < 7:
            p_month=datetime.strptime(str(back_month),"%m").strftime("%b")
        else:
            p_month=prev_month

        loading_b3_heads=[{
            'col1':str(current_year-1)+" - "+ str(current_year_short),
            'col2':str(current_year)+" - "+ str(current_year_short+1),
            'col3':prev_month+" "+str(current_year_short-1),
            'col4':prev_month+" "+str(current_year_short),
            'col5':prev_month+" "+str(current_year_short),
        }]

        capex_heads1=[{
            'col1':str(current_year-1)+" - "+ str(current_year_short),
            'col2':p_month+" "+str(current_year_short-1),
            'col3':str(current_year)+" - "+ str(current_year_short+1),
            'col4':p_month+" "+str(current_year_short),
        }]

        current_year=datetime.today().strftime("%Y")
        current_month=datetime.today()
        prev_month=current_month-relativedelta(days=30)
        month=datetime.strftime(prev_month,"%m")

    # FOR CAPEX VIA API
        date_capex = datetime.today()
        date_capex = date_capex - relativedelta(months=1)
        year_capex = date_capex.year
        month_capex = date_capex.month
        month_capex1 = datetime.strftime(date_capex,'%b')
        if month_capex < 10:
            month_capex = str(0)+str(month_capex)
        # # print(month_capex)
        data_capex = str(year_capex)+str(month_capex)
        # print(data_capex)
        capex_heads = list(m9.capex.objects.filter(month = data_capex).values())
        # print("capex",len(capex_heads),capex_heads)
        
        stop_year = datetime.today() - relativedelta(months=24)
        stop_year = stop_year.year

        while len(capex_heads) == 0 and year_capex > stop_year:
            date_capex = date_capex - relativedelta(months=1)
            year_capex = date_capex.year
            month_capex = date_capex.month
            month_capex1 = datetime.strftime(date_capex,'%b')
            if month_capex < 10:
                month_capex = str(0)+str(month_capex)
            data_capex = str(year_capex)+str(month_capex)
            # print(data_capex)
            capex_heads = list(m9.capex.objects.filter(month = data_capex).values())

        # print(capex_heads)
        print(month_capex,"oye",year_capex)
        if int(month_capex)>3:
            year_capex2 = date_capex - relativedelta(months=12)
            year_capex2 = year_capex2.year
            year_capex1 = year_capex
            year_capex1_short=date_capex.strftime("%y")
            year_capex2_short=int(year_capex1_short)+1
            pymonth_capex=year_capex2
            cymonth_capex=year_capex1
        else:
            year_capex2 = date_capex - relativedelta(months=24)
            year_capex2 = year_capex2.year
            year_capex1 = (date_capex - relativedelta(months=12)).year
            year_capex1_short=(date_capex - relativedelta(months=12)).strftime("%y")
            year_capex2_short=int(year_capex1_short)+1
            pymonth_capex=year_capex1
            cymonth_capex=year_capex
            
        
        # current_year=datetime.today().strftime("%Y")
        # current_month=datetime.today()
        # prev_month=current_month-relativedelta(days=30)
        # month=datetime.strftime(prev_month,"%m")

        # date_capex = datetime.today()
        # date_capex = date_capex - relativedelta(months=1)
        # year_capex = date_capex.year
        # month_capex = date_capex.month
        # month_capex1 = datetime.strftime(date_capex,'%b')
        # if month_capex < 10:
        #     month_capex = str(0)+str(month_capex)
        # # # print(month_capex)
        # data_capex = str(year_capex)+str(month_capex)
        # # print(data_capex)
        # capex_heads = list(m9.capex.objects.filter(month = data_capex).values())
        # # # print("capex",len(capex_heads),capex_heads)
        
        # while len(capex_heads) == 0:
        #     date_capex = date_capex - relativedelta(months=1)
        #     year_capex = date_capex.year
        #     month_capex = date_capex.month
        #     month_capex1 = datetime.strftime(date_capex,'%b')
        #     if month_capex < 10:
        #         month_capex = str(0)+str(month_capex)
        #     data_capex = str(year_capex)+str(month_capex)
        #     # print(data_capex)
        #     capex_heads = list(m9.capex.objects.filter(month = data_capex).values())
        # # capex_heads = list(m9.capex.objects.filter(month=current_year+month).values())

        # # print(capex_heads)
        # # print(month_capex1)
        # year_capex1 = year_capex
        # year_capex2 = date_capex - relativedelta(months=12)
        # year_capex2 = year_capex2.year

    # FOR LOADING VIA API BY PARIDHI
        zone_names_load={'CR':'CR',
            'ECO':'ECOR',
            'EC':'ECR',
            'ER':'ER',
            'KR':'KR',
            'NC':'NCR',
            'NE':'NER',
            'NF':'NFR',
            'NR':'NR',
            'NW':'NWR',
            'SEC':'SECR',
            'SC':'SCR',
            'SE':'SER',
            'SR':'SR',
            'SW':'SWR',
            'WC':'WCR',
            'WR':'WR',
            'Total':'Total'}

        load_com_today= m9.LogApi.objects.filter(schedular_name='devinsapi_loading_commodity').values('dates').order_by('-dates')[0]['dates']
        load_com_prev=(load_com_today-relativedelta(months=12)).strftime("%d/%m/%Y")
        load_com_today=load_com_today.strftime("%d/%m/%Y")

        load_zon_today= m9.LogApi.objects.filter(schedular_name='devinsapi_loading_zonal').values('dates').order_by('-dates')[0]['dates']
        load_zon_prev=(load_zon_today-relativedelta(months=12)).strftime("%d/%m/%Y")
        load_zon_today=load_zon_today.strftime("%d/%m/%Y")

        load_ovr_today= m9.LogApi.objects.filter(schedular_name='devinsapi_loading_overall').values('dates').order_by('-dates')[0]['dates']
        load_ovr_prev=(load_ovr_today-relativedelta(months=12)).strftime("%d/%m/%Y")
        load_ovr_today=load_ovr_today.strftime("%d/%m/%Y")

        load_comd = list(m9.Loading_Commodity.objects.annotate(sint=Cast('Var_Over_Target', FloatField()),mint=Cast('Var_Pctg', FloatField())).values())
        load_zone = list(m9.Loading_Zonal.objects.annotate(sint=Cast('Var_Over_Target', FloatField()),mint=Cast('Var_Pctg', FloatField())).values())
        # print(load_zone,"load_zone")
        for l in load_zone:
            l['Rly']=zone_names_load[l['Rly']]
        # print(load_zone,"load_zone")
        load_overall11 = list(m9.Loading_Overall.objects.values())
        load_overall = {}


        load_overall.update({'Freight Loading (MT)': {'prev':"{:.2f}".format(float(load_overall11[0]['Loading_Upto_Month_LY'])),'se_dte':"{:.2f}".format(float(load_overall11[0]['Loading_LFY'])), 'cur':"{:.2f}".format(float(load_overall11[0]['Loading_Upto_Month_CY'])),'change':float("{:.2f}".format((float(load_overall11[0]['Loading_Upto_Month_CY']))-(float(load_overall11[0]['Loading_Upto_Month_LY']))))}})
        load_overall.update({'Average Lead (Km)': {'prev':"{:.2f}".format(float(load_overall11[0]['Lead_Upto_Month_LY'])),'se_dte':"{:.2f}".format(float(load_overall11[0]['Lead_LFY'])), 'cur':"{:.2f}".format(float(load_overall11[0]['Lead_Upto_Month_CY'])),'change':float("{:.2f}".format((float(load_overall11[0]['Lead_Upto_Month_CY']))-(float(load_overall11[0]['Lead_Upto_Month_LY']))))}})
        load_overall.update({'NTKMs (Billion)': {'prev':"{:.2f}".format(float(load_overall11[0]['NTKM_Upto_Month_LY'])/1000),'se_dte':"{:.2f}".format(float(load_overall11[0]['NTKM_LFY'])/1000), 'cur':"{:.2f}".format(float(load_overall11[0]['NTKM_Upto_Month_CY'])/1000),'change':float("{:.2f}".format((float(load_overall11[0]['NTKM_Upto_Month_CY']))/1000 -(float(load_overall11[0]['NTKM_Upto_Month_LY']))/1000))}})
        load_overall.update({'Yield per NTKM (in paise)': {'prev':"{:.2f}".format(float(load_overall11[0]['Yield_NTKM_Upto_Month_LY'])),'se_dte':"{:.2f}".format(float(load_overall11[0]['Yield_NTKM_LFY'])), 'cur':"{:.2f}".format(float(load_overall11[0]['Yield_NTKM_Upto_Month_CY'])),'change':float("{:.2f}".format((float(load_overall11[0]['Yield_NTKM_Upto_Month_CY'])) - (float(load_overall11[0]['Yield_NTKM_Upto_Month_LY']))))}})
        load_overall.update({'Yield per MT (Rs in Cr)': {'prev':"{:.2f}".format(float(load_overall11[0]['Yield_MT_Upto_Month_LY'])),'se_dte':"{:.2f}".format(float(load_overall11[0]['Yield_MT_LFY'])), 'cur':"{:.2f}".format(float(load_overall11[0]['Yield_MT_Upto_Month_CY'])),'change':float("{:.2f}".format((float(load_overall11[0]['Yield_MT_Upto_Month_CY']))-(float(load_overall11[0]['Yield_MT_Upto_Month_LY']))))}})

    # FOR ASSET RELIABILITY VIA API BY PARIDHI
        assets = {}
        asset_day=m9.LogApi.objects.filter(schedular_name='devinsapi_punctuality_mrafdashboard').values('dates').order_by('-dates')[0]['dates']
        asset_day=datetime.strftime(asset_day,"%d/%m/%Y")

        asset_month=m9.LogApi.objects.filter(schedular_name='devinsapi_punctuality_mrafdashboard').values('dates').order_by('-dates')[0]['dates']
        pre_month=asset_month - relativedelta(months=12)
        asset_prev_yr=datetime.strftime(pre_month,"%d/%m/%Y")
        pre_month=datetime.strftime(pre_month,"%b %Y")
        asset_month=datetime.strftime(asset_month,"%b %Y")
        
        # print(asset_month)
        # fcodes = list(m2.Asset_Reliability.objects.values('failure_code').distinct('failure_code'))
        l1 = m9.Asset_Reliability.objects.filter(yearType='2',failure_code__in=['ELEC_LOCO','DSL_LOCO','ST','OHE','CW','ENGG']).values('failure_code',"yearType").order_by('failure_code').annotate(sum1=Sum('AF'))
        l3 = m9.Asset_Reliability_month.objects.filter(yearType='2',failure_code__in=['ELEC_LOCO','DSL_LOCO','ST','OHE','CW','ENGG']).values('failure_code',"yearType").order_by('failure_code').annotate(sum1=Sum('AF'))
        # l2 = m9.Asset_Reliability.objects.filter(yearType='1',failure_code__in=['ELEC_LOCO','DSL_LOCO','ST','OHE','CW','ENGG']).values('failure_code',"yearType").order_by('failure_code').annotate(sum1=Sum('AF'))
        # l4 = m9.Asset_Reliability_month.objects.filter(yearType='1',failure_code__in=['ELEC_LOCO','DSL_LOCO','ST','OHE','CW','ENGG']).values('failure_code',"yearType").order_by('failure_code').annotate(sum1=Sum('AF'))
        l2 = m9.Asset_Reliability.objects.filter(yearType='1',failure_code__in=['ELEC_LOCO','DSL_LOCO','ST','OHE','COACH','WAGON','ENGG']).values('failure_code',"yearType").order_by('failure_code').annotate(sum1=Sum('AF'))
        l4 = m9.Asset_Reliability_month.objects.filter(yearType='1',failure_code__in=['ELEC_LOCO','DSL_LOCO','ST','OHE','COACH','WAGON','ENGG']).values('failure_code',"yearType").order_by('failure_code').annotate(sum1=Sum('AF'))
        
        for i in range(len(l1)):
            # # print(l1[i]['failure_code'],l2[i]['failure_code'])
            if l1[i]['failure_code']=='ST':
                fcode = 'Signal and Telecom'
            elif l1[i]['failure_code']=='ELEC_LOCO':
                fcode = 'Electric Loco'
            elif l1[i]['failure_code']=='DSL_LOCO':
                fcode = 'Diesel Loco'
            elif l1[i]['failure_code']=='OHE':
                fcode = 'OHE/GRID Failure'
            elif l1[i]['failure_code']=='CW':
                fcode = 'Carriage and Wagon'
            elif l1[i]['failure_code']=='ENGG':
                fcode = 'Track'
            year_diff=round(((l2[i]['sum1']-l1[i]['sum1'])/l1[i]['sum1'])*100,2)
            month_diff=round(((l4[i]['sum1']-l3[i]['sum1'])/l3[i]['sum1'])*100,2)
            # print(year_diff)
            assets.update({fcode:{'prev':l1[i]['sum1'],'cur':l2[i]['sum1'],'year_diff':year_diff,'prev_mnth':l3[i]['sum1'],'cur_mnth':l4[i]['sum1'],'month_diff':month_diff}})
        
    # FOR ASSET FAILURE ZONE WISE  
        assets_zones_data=[] 
        assets_zones_data_month=[]
        fail_codes=['ELEC_LOCO','OHE','ENGG','CW','DSL_LOCO','ST']
        assets_zones=["CR","ECOR","ECR","ER","NCR","NER","NFR","NR","NWR","SCR","SECR","SER","SR","SWR","WCR","WR","total"]
        fail_sub_code_cw=[['CDTCH'],['HAP','HEG'],['TPG','TPP'],['WDTCH']]
        fail_sub_code_eng=['RF','WF']
        fail_sub_code_elec=['ELFG','ELTG','ELTP','EPFMID','EPFSTN','EPOTH','EPS']
        fail_sub_code_dsl=['DLFG','DLTG','DLTP','DPFMID','DPFSTN','DOTH','DPS']
        fail_sub_code_ohe=['ATF','BBOHE','ETFB','GRID','OHE','OHEOTH']
        fail_sub_code_sig=['ASF','AUTSF','AXCF','BBST','BIF','GSF','HSF','IBSF','LCCNS','LCGNC',
                        'OSF','PANF','PTF','SPEF','SSIF','STCC','TCF']
        
        codes={'ELEC_LOCO':fail_sub_code_elec,'DSL_LOCO':fail_sub_code_dsl,'OHE':fail_sub_code_ohe,'ST':fail_sub_code_sig}
        
        i=1
        for f in fail_codes:
            cy=[]
            py=[]
            diff=[]
            cm=[]
            pm=[]
            diffm=[]


            if f=='ST':
                fcode = 'Signal and Telecom'
            elif f=='ELEC_LOCO':
                fcode = 'Electric Loco'
            elif f=='DSL_LOCO':
                fcode = 'Diesel Loco'
            elif f=='OHE':
                fcode = 'OHE/GRID Failure'
            elif f=='CW':
                fcode = 'Carriage and Wagon'
            elif f=='ENGG':
                fcode = 'Engineering'
            
            if f == 'ENGG':
                assets_zones_data.append({'code':fcode,'val':i,'head':0})
                assets_zones_data_month.append({'code':fcode,'val':i,'head':0})
                for fs in fail_sub_code_eng:
                    cy=[]
                    py=[]
                    diff=[]
                    cm=[]
                    pm=[]
                    diffm=[]
                    for z in assets_zones:
                        if z == 'total':
                            f1 = list(m9.Asset_Reliability.objects.filter(yearType='2',failure_code=f,failure_subcode=fs,Zone__in=assets_zones).values('failure_code',"yearType").order_by('failure_code').annotate(sum1=Sum('AF')))
                            f2 = list(m9.Asset_Reliability.objects.filter(yearType='1',failure_code=f,failure_subcode=fs,Zone__in=assets_zones).values('failure_code',"yearType").order_by('failure_code').annotate(sum1=Sum('AF')))
                            if len(f1)==0:
                                f1.append({'sum1':0})
                            if len(f2)==0:
                                f2.append({'sum1':0})

                            if f1[0]['sum1']==0:
                                    per_diff=100
                            else:
                                per_diff=round(((f2[0]['sum1']-f1[0]['sum1'])/f1[0]['sum1'])*100,2)
                            cy.append(f2[0]['sum1'])
                            py.append(f1[0]['sum1'])
                            diff.append(per_diff)

                            f3 = list(m9.Asset_Reliability_month.objects.filter(yearType='2',failure_code=f,failure_subcode=fs,Zone__in=assets_zones).values('failure_code',"yearType").order_by('failure_code').annotate(sum1=Sum('AF')))
                            f4 = list(m9.Asset_Reliability_month.objects.filter(yearType='1',failure_code=f,failure_subcode=fs,Zone__in=assets_zones).values('failure_code',"yearType").order_by('failure_code').annotate(sum1=Sum('AF')))
                            if len(f3)==0:
                                f3.append({'sum1':0})
                            if len(f4)==0:
                                f4.append({'sum1':0})
                            if f3[0]['sum1']==0:
                                    per_diffm=100
                            else:
                                per_diffm=round(((f4[0]['sum1']-f3[0]['sum1'])/f3[0]['sum1'])*100,2)
                            cm.append(f4[0]['sum1'])
                            pm.append(f3[0]['sum1'])
                            diffm.append(per_diffm)

                        else:
                            f1 = list(m9.Asset_Reliability.objects.filter(yearType='2',failure_code=f,Zone=z,failure_subcode=fs).values('failure_code',"yearType","Zone").order_by('failure_code').annotate(sum1=Sum('AF')))
                            f2 = list(m9.Asset_Reliability.objects.filter(yearType='1',failure_code=f,Zone=z,failure_subcode=fs).values('failure_code',"yearType",'Zone').order_by('failure_code').annotate(sum1=Sum('AF')))
                            if len(f1)==0:
                                f1.append({'sum1':0})
                            if len(f2)==0:
                                f2.append({'sum1':0})
                            if f1[0]['sum1']==0:
                                per_diff=100
                            else:
                                per_diff=round(((f2[0]['sum1']-f1[0]['sum1'])/f1[0]['sum1'])*100,2)
                            
                            cy.append(f2[0]['sum1'])
                            py.append(f1[0]['sum1'])
                            diff.append(per_diff)

                            f3 = list(m9.Asset_Reliability_month.objects.filter(yearType='2',failure_code=f,Zone=z,failure_subcode=fs).values('failure_code',"yearType","Zone").order_by('failure_code').annotate(sum1=Sum('AF')))
                            f4 = list(m9.Asset_Reliability_month.objects.filter(yearType='1',failure_code=f,Zone=z,failure_subcode=fs).values('failure_code',"yearType","Zone").order_by('failure_code').annotate(sum1=Sum('AF')))
                            if len(f3)==0:
                                f3.append({'sum1':0})
                            if len(f4)==0:
                                f4.append({'sum1':0})
                            if f3[0]['sum1']==0:
                                per_diff_m=100
                            else:
                                per_diff_m=round(((f4[0]['sum1']-f3[0]['sum1'])/f3[0]['sum1'])*100,2)

                            cm.append(f4[0]['sum1'])
                            pm.append(f3[0]['sum1'])
                            diffm.append(per_diff_m)

                    if fs=='RF':
                        assets_zones_data.append({'code':'Rail Fracture Reported in ICMS upto '+asset_month, 'val':cy,'head':2,'sr_no':'(i)','color':1})
                        assets_zones_data.append({'code':'Rail Fracture Reported in ICMS upto '+pre_month, 'val':py,'head':2,'sr_no':'','color':2})
                        assets_zones_data_month.append({'code':'Rail Fracture Reported in ICMS for '+asset_month, 'val':cm,'head':2,'sr_no':'(i)','color':1})
                        assets_zones_data_month.append({'code':'Rail Fracture Reported in ICMS for '+pre_month, 'val':pm,'head':2,'sr_no':'','color':2})
                    else:
                        assets_zones_data.append({'code':'Weld Failure Reported in ICMS upto '+asset_month, 'val':cy,'head':2,'sr_no':'(ii)','color':11})
                        assets_zones_data.append({'code':'Weld Failure Reported in ICMS upto '+pre_month, 'val':py,'head':2,'sr_no':'','color':21})
                        assets_zones_data_month.append({'code':'Weld Failure Reported in ICMS for '+asset_month, 'val':cm,'head':2,'sr_no':'(ii)','color':11})
                        assets_zones_data_month.append({'code':'Weld Failure Reported in ICMS for '+pre_month, 'val':pm,'head':2,'sr_no':'','color':21})
                    
                    diff_colors=[]
                    diff_max=sorted(diff)[0:5]
                    diff_min=sorted(diff, reverse=True)[0:5]
                    # print(diff_max,diff_min)
                    for d in diff:
                        if d in diff_max:
                            diff_colors.append({'point':d,'col':1})#green
                        elif d in diff_min:
                            diff_colors.append({'point':d,'col':2})#red
                        else:
                            diff_colors.append({'point':d,'col':0})#white

                    assets_zones_data.append({'code':'% Improvement/Deterioration', 'val':diff_colors,'head':1,'color':3})

                    diff_colors=[]
                    diff_max=sorted(diffm)[0:5]
                    diff_min=sorted(diffm, reverse=True)[0:5]
                    # print(diff_max,diff_min)
                    for d in diffm:
                        if d in diff_max:
                            diff_colors.append({'point':d,'col':1})#green
                        elif d in diff_min:
                            diff_colors.append({'point':d,'col':2})#red
                        else:
                            diff_colors.append({'point':d,'col':0})#white

                    assets_zones_data_month.append({'code':'% Improvement/Deterioration', 'val':diff_colors,'head':1,'color':3})
                    # assets_zones_data.append({'code':'% Improvement/Deterioration', 'val':diff,'head':2,'sr_no':'','color':3})
                    # assets_zones_data_month.append({'code':'% Improvement/Deterioration', 'val':diff,'head':2,'sr_no':'','color':3})

            
            elif f == 'CW':
                fix=['COACH','WAGON']
                assets_zones_data.append({'code':fcode,'val':i,'head':0})
                assets_zones_data_month.append({'code':fcode,'val':i,'head':0})
                for fs in fail_sub_code_cw:
                    # print(fs)
                    cy=[]
                    py=[]
                    diff=[]
                    cm=[]
                    pm=[]
                    diffm=[]
                    for z in assets_zones:
                        if z == 'total':
                            f1 = list(m9.Asset_Reliability.objects.filter(yearType='2',failure_code=f,failure_subcode__in=fs,Zone__in=assets_zones).values('failure_code',"yearType").order_by('failure_code').annotate(sum1=Sum('AF')))
                            # f2 = list(m9.Asset_Reliability.objects.filter(yearType='1',failure_code=f,failure_subcode__in=fs,Zone__in=assets_zones).values('failure_code',"yearType").order_by('failure_code').annotate(sum1=Sum('AF')))
                            f2 = list(m9.Asset_Reliability.objects.filter(yearType='1',failure_code__in=fix,failure_subcode__in=fs,Zone__in=assets_zones).values('failure_code',"yearType").order_by('failure_code').annotate(sum1=Sum('AF')))
                            if len(f1)==0:
                                f1.append({'sum1':0})
                            if len(f2)==0:
                                f2.append({'sum1':0})
                            if f1[0]['sum1']==0:
                                    per_diff=100
                            else:
                                per_diff=round(((f2[0]['sum1']-f1[0]['sum1'])/f1[0]['sum1'])*100,2)
                            cy.append(f2[0]['sum1'])
                            py.append(f1[0]['sum1'])
                            diff.append(per_diff)

                            f3 = list(m9.Asset_Reliability_month.objects.filter(yearType='2',failure_code=f,failure_subcode__in=fs).values('failure_code',"yearType").order_by('failure_code').annotate(sum1=Sum('AF')))
                            # f4 = list(m9.Asset_Reliability_month.objects.filter(yearType='1',failure_code=f,failure_subcode__in=fs).values('failure_code',"yearType").order_by('failure_code').annotate(sum1=Sum('AF')))
                            f4 = list(m9.Asset_Reliability_month.objects.filter(yearType='1',failure_code__in=fix,failure_subcode__in=fs).values('failure_code',"yearType").order_by('failure_code').annotate(sum1=Sum('AF')))
                            if len(f3)==0:
                                f3.append({'sum1':0})
                            if len(f4)==0:
                                f4.append({'sum1':0})
                            if f3[0]['sum1']==0:
                                    per_diffm=100
                            else:
                                per_diffm=round(((f4[0]['sum1']-f3[0]['sum1'])/f3[0]['sum1'])*100,2)
                            cm.append(f4[0]['sum1'])
                            pm.append(f3[0]['sum1'])
                            diffm.append(per_diffm)

                        else:
                            f1 = list(m9.Asset_Reliability.objects.filter(yearType='2',failure_code=f,Zone=z,failure_subcode__in=fs).values('failure_code',"yearType","Zone").order_by('failure_code').annotate(sum1=Sum('AF')))
                            # f2 = list(m9.Asset_Reliability.objects.filter(yearType='1',failure_code=f,Zone=z,failure_subcode__in=fs).values('failure_code',"yearType",'Zone').order_by('failure_code').annotate(sum1=Sum('AF')))
                            f2 = list(m9.Asset_Reliability.objects.filter(yearType='1',failure_code__in=fix,Zone=z,failure_subcode__in=fs).values('failure_code',"yearType",'Zone').order_by('failure_code').annotate(sum1=Sum('AF')))    
                            if len(f1)==0:
                                f1.append({'sum1':0})
                            if len(f2)==0:
                                f2.append({'sum1':0})                   
                            if f1[0]['sum1']==0:
                                per_diff=100
                            else:
                                per_diff=round(((f2[0]['sum1']-f1[0]['sum1'])/f1[0]['sum1'])*100,2)
                            cy.append(f2[0]['sum1'])
                            py.append(f1[0]['sum1'])
                            diff.append(per_diff)

                            f3 = list(m9.Asset_Reliability_month.objects.filter(yearType='2',failure_code=f,Zone=z,failure_subcode__in=fs).values('failure_code',"yearType","Zone").order_by('failure_code').annotate(sum1=Sum('AF')))
                            # f4 = list(m9.Asset_Reliability_month.objects.filter(yearType='1',failure_code=f,Zone=z,failure_subcode__in=fs).values('failure_code',"yearType",'Zone').order_by('failure_code').annotate(sum1=Sum('AF')))
                            f4 = list(m9.Asset_Reliability_month.objects.filter(yearType='1',failure_code__in=fix,Zone=z,failure_subcode__in=fs).values('failure_code',"yearType",'Zone').order_by('failure_code').annotate(sum1=Sum('AF')))
                            if len(f3)==0:
                                f3.append({'sum1':0})
                            if len(f4)==0:
                                f4.append({'sum1':0})
                            if f3[0]['sum1']==0:
                                per_diffm=100
                            else:
                                per_diffm=round(((f4[0]['sum1']-f3[0]['sum1'])/f3[0]['sum1'])*100,2)
                            cm.append(f4[0]['sum1'])
                            pm.append(f3[0]['sum1'])
                            diffm.append(per_diffm)
                        

                    if fs in [['CDTCH']]:
                        assets_zones_data.append({'code':'Coach Detachment Reported in ICMS upto '+asset_month, 'val':cy,'head':2,'sr_no':'(i)','color':1})
                        assets_zones_data.append({'code':'Coach Detachment Reported in ICMS upto '+pre_month, 'val':py,'head':2,'sr_no':'','color':2})
                        assets_zones_data_month.append({'code':'Coach Detachment Reported in ICMS for '+asset_month, 'val':cm,'head':2,'sr_no':'(i)','color':1})
                        assets_zones_data_month.append({'code':'Coach Detachment Reported in ICMS for '+pre_month, 'val':pm,'head':2,'sr_no':'','color':2})
                    elif fs in [['HAP','HEG']]:
                        assets_zones_data.append({'code':'Hot Axel Reported in ICMS upto '+asset_month, 'val':cy,'head':2,'sr_no':'(ii)', 'color':11})
                        assets_zones_data.append({'code':'Hot Axel Reported in ICMS upto '+pre_month, 'val':py,'head':2,'sr_no':'', 'color':21})
                        assets_zones_data_month.append({'code':'Hot Axel Reported in ICMS for '+asset_month, 'val':cm,'head':2,'sr_no':'(ii)', 'color':11})
                        assets_zones_data_month.append({'code':'Hot Axel Reported in ICMS for '+pre_month, 'val':pm,'head':2,'sr_no':'', 'color':21})
                    elif fs in [['TPG','TPP']]:
                        assets_zones_data.append({'code':'Train Parting Reported in ICMS upto '+asset_month, 'val':cy,'head':2,'sr_no':'(iii)', 'color':1})
                        assets_zones_data.append({'code':'Train Parting Reported in ICMS upto '+pre_month, 'val':py,'head':2,'sr_no':'', 'color':2})
                        assets_zones_data_month.append({'code':'Train Parting Reported in ICMS for '+asset_month, 'val':cm,'head':2,'sr_no':'(iii)', 'color':1})
                        assets_zones_data_month.append({'code':'Train Parting Reported in ICMS for '+pre_month, 'val':pm,'head':2,'sr_no':'', 'color':2})
                    elif fs in [['WDTCH']]:
                        assets_zones_data.append({'code':'Wagon Detachment Reported in ICMS upto '+asset_month, 'val':cy,'head':2,'sr_no':'(iv)', 'color':11})
                        assets_zones_data.append({'code':'Wagon Detachment Reported in ICMS upto '+pre_month, 'val':py,'head':2,'sr_no':'', 'color':21})
                        assets_zones_data_month.append({'code':'Wagon Detachment Reported in ICMS for '+asset_month, 'val':cm,'head':2,'sr_no':'(iv)', 'color':11})
                        assets_zones_data_month.append({'code':'Wagon Detachment Reported in ICMS for '+pre_month, 'val':pm,'head':2,'sr_no':'', 'color':21})
                    
                    diff_colors=[]
                    diff_max=sorted(diff)[0:5]
                    diff_min=sorted(diff, reverse=True)[0:5]
                    # print(diff_max,diff_min)
                    for d in diff:
                        if d in diff_max:
                            diff_colors.append({'point':d,'col':1})#green
                        elif d in diff_min:
                            diff_colors.append({'point':d,'col':2})#red
                        else:
                            diff_colors.append({'point':d,'col':0})#white

                    assets_zones_data.append({'code':'% Improvement/Deterioration', 'val':diff_colors,'head':1,'color':3})

                    diff_colors=[]
                    diff_max=sorted(diffm)[0:5]
                    diff_min=sorted(diffm, reverse=True)[0:5]
                    # print(diff_max,diff_min)
                    for d in diffm:
                        if d in diff_max:
                            diff_colors.append({'point':d,'col':1})#green
                        elif d in diff_min:
                            diff_colors.append({'point':d,'col':2})#red
                        else:
                            diff_colors.append({'point':d,'col':0})#white

                    assets_zones_data_month.append({'code':'% Improvement/Deterioration', 'val':diff_colors,'head':1,'color':3})

                    # assets_zones_data.append({'code':'% Improvement/Deterioration', 'val':diff,'head':2,'sr_no':'', 'color':3})
                    # assets_zones_data_month.append({'code':'% Improvement/Deterioration', 'val':diffm,'head':2,'sr_no':'', 'color':3})

        

            else:
                for z in assets_zones:
                    if z == 'total':
                        f1 = list(m9.Asset_Reliability.objects.filter(yearType='2',failure_code=f,failure_subcode__in=codes[f],Zone__in=assets_zones).values('failure_code',"yearType").order_by('failure_code').annotate(sum1=Sum('AF')))
                        f2 = list(m9.Asset_Reliability.objects.filter(yearType='1',failure_code=f,failure_subcode__in=codes[f],Zone__in=assets_zones).values('failure_code',"yearType").order_by('failure_code').annotate(sum1=Sum('AF')))
                        if len(f1)==0:
                            f1.append({'sum1':0})
                        if len(f2)==0:
                            f2.append({'sum1':0})
                        if f1[0]['sum1']==0:
                                per_diff=100
                        else:
                            per_diff=round(((f2[0]['sum1']-f1[0]['sum1'])/f1[0]['sum1'])*100,2)
                        cy.append(f2[0]['sum1'])
                        py.append(f1[0]['sum1'])
                        diff.append(per_diff)

                        f3 = list(m9.Asset_Reliability_month.objects.filter(yearType='2',failure_code=f,failure_subcode__in=codes[f],Zone__in=assets_zones).values('failure_code',"yearType").order_by('failure_code').annotate(sum1=Sum('AF')))
                        f4 = list(m9.Asset_Reliability_month.objects.filter(yearType='1',failure_code=f,failure_subcode__in=codes[f],Zone__in=assets_zones).values('failure_code',"yearType").order_by('failure_code').annotate(sum1=Sum('AF')))
                        if len(f3)==0:
                            f3.append({'sum1':0})
                        if len(f4)==0:
                            f4.append({'sum1':0})
                        if f3[0]['sum1']==0:
                                per_diffm=100
                        else:
                            per_diffm=round(((f4[0]['sum1']-f3[0]['sum1'])/f3[0]['sum1'])*100,2)
                        cm.append(f4[0]['sum1'])
                        pm.append(f3[0]['sum1'])
                        diffm.append(per_diffm)

                    else:

                        #year wise
                        f1 = list(m9.Asset_Reliability.objects.filter(yearType='2',failure_code=f,failure_subcode__in=codes[f],Zone=z).values('failure_code',"yearType","Zone").order_by('failure_code').annotate(sum1=Sum('AF')))
                        f2 = list(m9.Asset_Reliability.objects.filter(yearType='1',failure_code=f,failure_subcode__in=codes[f],Zone=z).values('failure_code',"yearType",'Zone').order_by('failure_code').annotate(sum1=Sum('AF')))
                        # print(f1)
                        if len(f1)==0:
                            f1.append({'sum1':0})
                        if len(f2)==0:
                            f2.append({'sum1':0})

                        if f1[0]['sum1']==0:
                                per_diff=100
                        else:
                            per_diff=round(((f2[0]['sum1']-f1[0]['sum1'])/f1[0]['sum1'])*100,2)
                        cy.append(f2[0]['sum1'])
                        py.append(f1[0]['sum1'])
                        diff.append(per_diff)

                        #month wise
                        f3 = list(m9.Asset_Reliability_month.objects.filter(yearType='2',failure_code=f,failure_subcode__in=codes[f],Zone=z).values('failure_code',"yearType","Zone").order_by('failure_code').annotate(sum1=Sum('AF')))
                        f4 = list(m9.Asset_Reliability_month.objects.filter(yearType='1',failure_code=f,failure_subcode__in=codes[f],Zone=z).values('failure_code',"yearType",'Zone').order_by('failure_code').annotate(sum1=Sum('AF')))
                        if len(f3)==0:
                            f3.append({'sum1':0})
                        if len(f4)==0:
                            f4.append({'sum1':0})

                        if f3[0]['sum1']==0:
                                per_diffm=100
                        else:
                            per_diffm=round(((f4[0]['sum1']-f3[0]['sum1'])/f3[0]['sum1'])*100,2)
                        cm.append(f4[0]['sum1'])
                        pm.append(f3[0]['sum1'])
                        diffm.append(per_diffm)

                assets_zones_data.append({'code':fcode,'val':i,'head':0})
                assets_zones_data.append({'code':'Reported in ICMS upto '+asset_month, 'val':cy,'head':1,'color':1})
                assets_zones_data.append({'code':'Reported in ICMS upto '+pre_month, 'val':py,'head':1,'color':2})
            
                diff_colors=[]
                diff_max=sorted(diff)[0:5]
                diff_min=sorted(diff, reverse=True)[0:5]
                # print(diff_max,diff_min)
                for d in diff:
                    if d in diff_max:
                        diff_colors.append({'point':d,'col':1})#green
                    elif d in diff_min:
                        diff_colors.append({'point':d,'col':2})#red
                    else:
                        diff_colors.append({'point':d,'col':0})#white

                assets_zones_data.append({'code':'% Improvement/Deterioration', 'val':diff_colors,'head':1,'color':3})

                assets_zones_data_month.append({'code':fcode,'val':i,'head':0})
                assets_zones_data_month.append({'code':'Reported in ICMS for '+asset_month, 'val':cm,'head':1,'color':1 })
                assets_zones_data_month.append({'code':'Reported in ICMS for '+pre_month, 'val':pm,'head':1,'color':2})
                
                diff_colors=[]
                diff_max=sorted(diffm)[0:5]
                diff_min=sorted(diffm, reverse=True)[0:5]
                # print(diff_max,diff_min)
                for d in diffm:
                    if d in diff_max:
                        diff_colors.append({'point':d,'col':1})#green
                    elif d in diff_min:
                        diff_colors.append({'point':d,'col':2})#red
                    else:
                        diff_colors.append({'point':d,'col':0})#white

                assets_zones_data_month.append({'code':'% Improvement/Deterioration', 'val':diff_colors,'head':1,'color':3})
                # assets_zones_data_month.append({'code':'% Improvement/Deterioration', 'val':diffm,'head':1,'color':3})
            i+=1
            # print(assets_zones_data)

    # FOR SAFETY VIA API BY PARIDHI
        curdate = date.today()
        curdate = datetime.strftime(curdate,'%b-%y')
        prevyear = curdate.split('-')[1]
        prevyear = int(prevyear)-1
        mnth=curdate.split('-')[0]
        
        # print(mnth,"apeksha")
        curdate = date.today()
        curdate = datetime.strftime(curdate,'%b-%Y')
        curyear = curdate.split('-')[1]
        prevyear = int(curyear)-1
        secprevyear = int(prevyear)-1
        thirdprevyear = int(secprevyear)-1
        thirdprevfromdate = str(thirdprevyear)+"-04-01"
        thirdprevtodate = str(secprevyear)+"-03-31"
        secprevfromdate = str(secprevyear)+"-04-01"
        secprevtodate = str(prevyear)+"-03-31"
        prevfromdate = str(prevyear)+"-04-01"
        prevtodate = str(curyear)+"-03-31"

        acci_date=m9.LogApi.objects.filter(schedular_name='accident_data').values('dates').order_by('-dates')[0]['dates']
        pre_acci_date=acci_date-relativedelta(months=12)
        acci_date=datetime.strftime(acci_date,"%d/%m/%Y")
        pre_acci_date=datetime.strftime(pre_acci_date,"%d/%m/%Y")
        safety1 = {}
        accitypes = list(m9.safety.objects.values('accidentType').distinct('accidentType'))
        for i in range(len(accitypes)):
            last3rdyear = m9.safety.objects.filter(accidentType=accitypes[i]['accidentType'],accidentDate__range=[thirdprevfromdate,thirdprevtodate],consequentialFlag='Y').exclude(rlyCode='DFC').distinct('accidentId').count()
            last2ndyear = m9.safety.objects.filter(accidentType=accitypes[i]['accidentType'],accidentDate__range=[secprevfromdate,secprevtodate],consequentialFlag='Y').exclude(rlyCode='DFC').distinct('accidentId').count()
            lastyear = m9.safety.objects.filter(accidentType=accitypes[i]['accidentType'],accidentDate__range=[prevfromdate,prevtodate],consequentialFlag='Y').exclude(rlyCode='DFC').distinct('accidentId').count()
            month1 = datetime.today().month
            if(month1 <= 3):
                curdate1 = date.today()
                curdate2 = curdate1-relativedelta(months=12)
                curdate1 = datetime.strftime(curdate1,"%Y-%m-%d")
                curdate2 = datetime.strftime(curdate2,"%Y-%m-%d")
                finlastyear = m9.safety.objects.filter(accidentType=accitypes[i]['accidentType'],accidentDate__range=[secprevfromdate,curdate2],consequentialFlag='Y').exclude(rlyCode='DFC').distinct('accidentId').count()
                finyear = m9.safety.objects.filter(accidentType=accitypes[i]['accidentType'],accidentDate__range=[prevfromdate,curdate1],consequentialFlag='Y').exclude(rlyCode='DFC').distinct('accidentId').count()
            else:
                curdate1 = date.today()
                curdate2 = curdate1-relativedelta(months=12)
                curdate2 = datetime.strftime(curdate2,"%Y-%m-%d")
                curdate1 = datetime.strftime(curdate1,"%Y-%m-%d")
                date1 = str(curyear)+"-04-01"
                finlastyear = m9.safety.objects.filter(accidentType=accitypes[i]['accidentType'],accidentDate__range=[prevfromdate,curdate2],consequentialFlag='Y').exclude(rlyCode='DFC').distinct('accidentId').count()
                finyear = m9.safety.objects.filter(accidentType=accitypes[i]['accidentType'],accidentDate__range=[date1,curdate1],consequentialFlag='Y').exclude(rlyCode='DFC').distinct('accidentId').count()
            if accitypes[i]['accidentType']=='Collision':
                accitypes[i]['accidentType']='Collisions'
            elif accitypes[i]['accidentType']=='Derailment':
                accitypes[i]['accidentType']='Derailments'
            elif accitypes[i]['accidentType']=='Fire':
                accitypes[i]['accidentType']='Fire'
            elif accitypes[i]['accidentType']=='Miscellaneous Accident':
                accitypes[i]['accidentType']='Misc.'
            elif accitypes[i]['accidentType']=='MLC Accident':
                accitypes[i]['accidentType']='MLC'
            elif accitypes[i]['accidentType']=='UMLC Accident':
                accitypes[i]['accidentType']='UMLC'
            else:
                continue
            safety1.update({accitypes[i]['accidentType']:{'finlastyear':finlastyear,'finyear':finyear,'lastyear':lastyear,'last2ndyear':last2ndyear,'last3rdyear':last3rdyear,'change':finyear-finlastyear}})
    
        # # print("Paridhi",safety1)

    # FOR SAFETY ZONE WISE
        zone_names={'CR':'CR',
            'ECo':'ECOR',
            'EC':'ECR',
            'ER':'ER',
            'DFC':'DFC',
            'MR':'MR',
            'KR':'KR',
            'NC':'NCR',
            'NE':'NER',
            'NF':'NFR',
            'NR':'NR',
            'NW':'NWR',
            'SEC':'SECR',
            'SC':'SCR',
            'SE':'SER',
            'SR':'SR',
            'SW':'SWR',
            'WC':'WCR',
            'WR':'WR'}

        safety_zone = {}
        rlyCodes = list(m9.safety.objects.values('rlyCode').exclude(rlyCode='DFC').distinct('rlyCode'))
        for i in range(len(rlyCodes)):
            last3rdyear = m9.safety.objects.filter(rlyCode=rlyCodes[i]['rlyCode'],accidentDate__range=[thirdprevfromdate,thirdprevtodate],consequentialFlag='Y').distinct('accidentId').count()
            last2ndyear = m9.safety.objects.filter(rlyCode=rlyCodes[i]['rlyCode'],accidentDate__range=[secprevfromdate,secprevtodate],consequentialFlag='Y').distinct('accidentId').count()
            lastyear = m9.safety.objects.filter(rlyCode=rlyCodes[i]['rlyCode'],accidentDate__range=[prevfromdate,prevtodate],consequentialFlag='Y').distinct('accidentId').count()
            month1 = datetime.today().month
            if(month1 <= 3):
                curdate1 = date.today()
                curdate2 = curdate1-relativedelta(months=12)
                curdate1 = datetime.strftime(curdate1,"%Y-%m-%d")
                curdate2 = datetime.strftime(curdate2,"%Y-%m-%d")
                finlastyear = m9.safety.objects.filter(rlyCode=rlyCodes[i]['rlyCode'],accidentDate__range=[secprevfromdate,curdate2],consequentialFlag='Y').distinct('accidentId').count()
                finyear = m9.safety.objects.filter(rlyCode=rlyCodes[i]['rlyCode'],accidentDate__range=[prevfromdate,curdate1],consequentialFlag='Y').distinct('accidentId').count()
            else:
                curdate1 = date.today()
                curdate2 = curdate1-relativedelta(months=12)
                curdate2 = datetime.strftime(curdate2,"%Y-%m-%d")
                curdate1 = datetime.strftime(curdate1,"%Y-%m-%d")
                date1 = str(curyear)+"-04-01"
                finlastyear = m9.safety.objects.filter(rlyCode=rlyCodes[i]['rlyCode'],accidentDate__range=[prevfromdate,curdate2],consequentialFlag='Y').distinct('accidentId').count()
                finyear = m9.safety.objects.filter(rlyCode=rlyCodes[i]['rlyCode'],accidentDate__range=[date1,curdate1],consequentialFlag='Y').distinct('accidentId').count()
            safety_zone.update({rlyCodes[i]['rlyCode']:{'rly':zone_names[rlyCodes[i]['rlyCode']],'finlastyear':finlastyear,'finyear':finyear,'lastyear':lastyear,'last2ndyear':last2ndyear,'last3rdyear':last3rdyear,'change':finyear-finlastyear}})
        # print(safety_zone,"wow")

    # FOR EARNINGS & OWE VIA API BY PARIDHI
        secprevyear1 = str(secprevyear)[2:4]
        prevyear1 = str(prevyear)[2:4]
        curyear1 = str(curyear)[2:4]
        # print(secprevyear1,curyear1)
        date11 = date.today()
        date11=date11-relativedelta(days=1)
        date12 = date11 - relativedelta(months=12)
        date111 = datetime.strftime(date11,"%Y-%m-%d")
        date112 = datetime.strftime(date12,"%Y-%m-%d")
        date12 = datetime.strftime(date12,"%d/%m/%Y")
        date11 = datetime.strftime(date11,"%d/%m/%Y")
        

        curyear123 = date.today().year
        date123 = date.today() - relativedelta(days=30)
        month123 = date123.month
        # print(str(curyear123)+str(month123))
        

        date_earnings = datetime.today()
        date_earnings = date_earnings - relativedelta(months=1)
        year_earnings = date_earnings.year
        month_earnings = date_earnings.month
        month_earnings1 = datetime.strftime(date_earnings,'%b')
        print(date_earnings,' dd ',month_earnings1)
        if month_earnings < 10:
            month_earnings = str(0)+str(month_earnings)
        data_earnings = str(year_earnings)+str(month_earnings)
        earnings1 = list(m9.earnings.objects.filter(MONTH=data_earnings).values().annotate(sint=Cast('INCREASE_OVER_PREV', FloatField())).order_by('id'))
        for e in earnings1:
                inc=round(float(e['ACTUALS_CURR_MONTH'])-float(e['PREV_ACTUALS_MONTH']),2)
                if e['HEAD']=='Growth':
                    e.update({'sint':inc})
        # print(data_earnings)
        while len(earnings1)==0:
            date_earnings = date_earnings - relativedelta(months=1)
            year_earnings= date_earnings.year
            month_earnings = date_earnings.month
            month_earnings1 = datetime.strftime(date_earnings,'%b')
            print(date_earnings,' while ',month_earnings1)
            if month_earnings < 10:
                month_earnings = str(0)+str(month_earnings)
            data_earnings = str(year_earnings)+str(month_earnings)
            # print(data_earnings)
            earnings1 = list(m9.earnings.objects.filter(MONTH=data_earnings).values().annotate(sint=Cast('INCREASE_OVER_PREV', FloatField())).order_by('id'))
            for e in earnings1:
                inc=round(float(e['ACTUALS_CURR_MONTH'])-float(e['PREV_ACTUALS_MONTH']),2)
                if e['HEAD']=='Growth':
                    e.update({'sint':inc})
        # print(earnings1,"hhwvbebvvvvvvvvvvvvvv")
        # print(month_earnings1)
        year_earnings1 = year_earnings
        year_earnings2 = date_earnings - relativedelta(months=12)
        year_earnings2 = year_earnings2.year  



        
        # earnings1 = list(m9.earnings.objects.filter(MONTH=str(curyear123)+str(month123)).values().annotate(sint=Cast('INCREASE_OVER_PREV', FloatField())).order_by('id'))

    # FOR ROLLING STOCK (WAGONS) VIA API BY PARIDHI
        
        
        # wagons ={}
        # # print("lst1",str(prevyear)+"-01-01",str(prevyear)+"-12-31")
        # lst1 = m9.wagon.objects.filter(dm_date__range=[str(prevyear)+"-01-01",str(prevyear)+"-12-31"]).count()
        # month1 = datetime.today().month
        # if month1 <= 3:
        #     # print("lst2",str(prevyear)+"-04-01",date111)
        #     lst2 = m9.wagon.objects.filter(dm_date__range=[str(prevyear)+"-04-01",date111]).count()
        # else:
        #     # print("lst2",str(curyear)+"-04-01",date111)
        #     lst2 = m9.wagon.objects.filter(dm_date__range=[str(curyear)+"-04-01",date111]).count()
        # # print("lst3",str(prevyear)+"-"+str(month1)+"-01",date112)
        # lst3 = m9.wagon.objects.filter(dm_date__range=[str(prevyear)+"-"+str(month1)+"-01",date112]).count()
        # # print("lst4",str(curyear)+"-"+str(month1)+"-01",date111)
        # lst4 = m9.wagon.objects.filter(dm_date__range=[str(curyear)+"-"+str(month1)+"-01",date111]).count()
        # wagons.update({'Wagon Included' : {'prev_year' : lst1, 'cur_year' : lst2, 'prev_mnth': lst3, 'cur_mnth': lst4}})
        # # print("Wagons",wagons)
        

    # FOR ROLLING STOCK VIA SQL BY NEILOTPAL
        rolling_stock=[]
        # rollimg stock date part:
        with connections['users'].cursor() as cursor:
            cursor.execute('''SELECT MAX(CAST(year as DECIMAL(8))) as year FROM `cris-cr`.pu_category_monthly_entry''')
            y1=dictfetchall(cursor)[0]['year']
            print("rssssssssssssssssssss", y1)
            if y1:
                rs_year=int(y1)
            else:
                rs_year=date.today().year

            cursor.execute('''SELECT  MAX(CAST(month as DECIMAL(8))) as month FROM `cris-cr`.pu_category_monthly_entry WHERE year=%s''',[rs_year])
            mnth=dictfetchall(cursor)[0]['month']
            if mnth:
                rsp_month=int(mnth)+1
            else:
                rsp_month=date.today().month +1

            rs_month=datetime.strptime(str(rsp_month-1),"%m").strftime("%b")
            rs_financial_year=rs_year
        
            if rsp_month <= 4:
                rs_financial_year=rs_year-1

            rs_year_short=str(rs_financial_year)[2:4]
            rs_year_short_next=int(rs_year_short)+1
            rs_prev_year=rs_financial_year-1
            rs_prev_year_short=str(rs_prev_year)[2:4]

            # rolling stock select button part:
            cursor.execute('''SELECT username,railway FROM `cris-cr`.users_details where username in ('blw@pu','clw@pu','dmw@pu','icf@pu','mcf@pu','rcf@pu')''')
            users = dictfetchall(cursor)
            # print("########################",users)

            # for i in range(len(users)):
            #     pu=users[i]['username']
            #     pu_name=users[i]['railway']
            #     x = pu.split("@")
            #     users[i]['username']=x[0]

        
            cursor.execute('''SELECT id, asset FROM `cris-cr`.assets where asset LIKE '%Loco%' or asset LIKE '%Coach%' ''')
            rs = dictfetchall(cursor)
            # print(rs)
            pu_list=[]

            # for i in range(len(rs)):
            #     cursor.execute('''SELECT distinct(added_by) FROM `cris-cr`.assets_sub_category where main_asset=%s''',[rs[i]['id']])
            #     pu=dictfetchall(cursor)
            #     # print(pu)
            #     pu_list.extend(pu)
            # # print(pu_list)

            print(rs_financial_year,rs_year)
            if rs_financial_year == rs_year:
                for i in range (len(rs)):
                    cursor.execute('''SELECT category_id,sum(outturn) FROM `cris-cr`.pu_category_monthly_outturn where category_id in 
                    (Select id from `cris-cr`.assets_sub_category where main_asset=%s) and entry_id in 
                    (SELECT id FROM `cris-cr`.pu_category_monthly_entry where ((year=%s and month>3) or (year=%s and month<4)) and active=1)''',[rs[i]['id'],rs_prev_year,rs_financial_year])
                    s0 = dictfetchall(cursor)
                    if s0[0]['sum(outturn)']:
                        s0=s0[0]['sum(outturn)']
                    else:
                        s0=0
                
                    # # print(s0)

                    cursor.execute('''SELECT category_id,sum(target) FROM `cris-cr`.pu_category_monthly_target where category_id in 
                    (Select id from `cris-cr`.assets_sub_category where main_asset=%s) and entry_id in 
                    (SELECT id FROM `cris-cr`.pu_category_target_entry where year=%s and active=1 and id>83)''',[rs[i]['id'], rs_year])
                    s1 = dictfetchall(cursor)[0]['sum(target)']
                    if s1:
                        s1=s1
                    else:
                        s1=0
                    # s1=int(s1)
                    # s1=int((s1/12)*(rsp_month-4))
                    # ask sir about decimal
                    # print(s1)
                    # # print('rsp_month',rsp_month)

                    cursor.execute('''SELECT category_id,CEILING(sum(outturn)) as outturn1
                    FROM `cris-cr`.pu_category_monthly_outturn where entry_id in 
                    (SELECT id FROM `cris-cr`.pu_category_monthly_entry where month=%s and year=%s and active=1) and  
                    category_id in (Select id from `cris-cr`.assets_sub_category where main_asset=%s)''',[rsp_month-1,rs_year,rs[i]['id']])
                    s2 = dictfetchall(cursor)
                    if s2[0]['outturn1']:
                        s2=s2[0]['outturn1']
                    else:
                        s2=0
                    # if s2:
                    #     c2=s2[0]['outturn1']
                    # else:
                    #     c2='NA'
                    # # print(c2)
                    # # print(s2)
                    # if s2:
                    #     c2=s2[0]['outturn1']
                    #     c2=int(c2)
                    # else:
                    #     c2='NA'

                    # # print(c2)
                    # # print(s2)

                    cursor.execute('''SELECT category_id,CEILING(sum(outturn)) as outturn1
                    FROM `cris-cr`.pu_category_monthly_outturn where 
                    entry_id in (SELECT id FROM `cris-cr`.pu_category_monthly_entry where month=%s and year=%s and active=1) and  
                    category_id in (Select id from `cris-cr`.assets_sub_category where main_asset=%s)''',[rsp_month-1,rs_prev_year,rs[i]['id']])
                    s5 = dictfetchall(cursor)
                    if s5[0]['outturn1']:
                        s5=s5[0]['outturn1']
                    else:
                        s5=0
                    # # print(s5)

                    cursor.execute('''SELECT category_id,sum(outturn) as outturn1
                    FROM `cris-cr`.pu_category_monthly_outturn where entry_id in (SELECT id FROM `cris-cr`.pu_category_monthly_entry where month>3 and year=%s and active=1)
                    and category_id in (Select id from `cris-cr`.assets_sub_category where main_asset=%s)''',[rs_year,rs[i]['id']])
                    s3 = dictfetchall(cursor)
                    if s3[0]['outturn1']:
                        s3=s3[0]['outturn1']
                    else:
                        s3=0
                    # # print(s3)
                    
                    rolling_stock.append({'id':rs[i]['asset'],'cum_prev':int(s0),'target':int(s1),'monthly_achvd':int(s2),'cum_achvd':int(s3),'same_month_of_previous_year':int(s5)})
                    
            else:
                for i in range (len(rs)):
                    cursor.execute('''SELECT category_id,sum(outturn) FROM `cris-cr`.pu_category_monthly_outturn where category_id in 
                    (Select id from `cris-cr`.assets_sub_category where main_asset=%s) and entry_id in 
                    (SELECT id FROM `cris-cr`.pu_category_monthly_entry where ((year=%s and month>3) or (year=%s and month<4)) and active=1)''',
                    [rs[i]['id'],rs_prev_year,rs_financial_year])
                    # print(rs_prev_year,rs_financial_year,"wow")
                    s0 = dictfetchall(cursor)
                    if s0:
                        s0=s0[0]['sum(outturn)']
                    else:
                        s0='0'
                    print(s0, type(s0))

                    cursor.execute('''SELECT category_id,sum(target) FROM `cris-cr`.pu_category_monthly_target where category_id in 
                    (Select id from `cris-cr`.assets_sub_category where main_asset=%s) and entry_id in 
                    (SELECT id FROM `cris-cr`.pu_category_target_entry where year=%s  and active=1 and id>83)''',
                    [rs[i]['id'],rs_financial_year])
                    s1 = dictfetchall(cursor)[0]['sum(target)']
                    # print(s1,"wow")
                    if s1:
                        s1=s1
                    else:
                        cursor.execute('''SELECT category_id,sum(target) FROM `cris-cr`.pu_category_monthly_target where category_id in 
                        (Select id from `cris-cr`.assets_sub_category where main_asset=%s) and entry_id in 
                        (SELECT id FROM `cris-cr`.pu_category_target_entry where year=%s  and active=1 and id>83)''',
                        [rs[i]['id'],rs_year])
                        s1 = dictfetchall(cursor)[0]['sum(target)']
                        if s1:
                            s1=s1
                        else:
                            s1=0
                    # s1=int(s1)
                    # s1=int((s1/12)*(rsp_month+9))
                    print(s1)
                    print('rsp_month',rsp_month)

                    cursor.execute('''SELECT category_id,CEILING(sum(outturn)) as outturn1
                    FROM `cris-cr`.pu_category_monthly_outturn where entry_id in 
                    (SELECT id FROM `cris-cr`.pu_category_monthly_entry where month=%s and year=%s and active=1) and  category_id in 
                    (Select id from `cris-cr`.assets_sub_category where main_asset=%s)''',[rsp_month-1,rs_year,rs[i]['id']])
                    s2 = dictfetchall(cursor)
                    if s2:
                        s2=s2[0]['outturn1']
                    else:
                        s2=0
                    # # print(s2)
    
                    cursor.execute('''SELECT category_id,CEILING(sum(outturn)) as outturn1
                    FROM `cris-cr`.pu_category_monthly_outturn where entry_id in 
                    (SELECT id FROM `cris-cr`.pu_category_monthly_entry where month=%s and year=%s and active=1) and  category_id in 
                    (Select id from `cris-cr`.assets_sub_category where main_asset=%s)''',[rsp_month-1,rs_financial_year,rs[i]['id']])
                    s5 = dictfetchall(cursor)
                    if s5:
                        s5=s5[0]['outturn1']
                    else:
                        s5=0
                    # # print(s5)

                    cursor.execute('''SELECT category_id,sum(outturn) as outturn1
                    FROM `cris-cr`.pu_category_monthly_outturn where entry_id in 
                    (SELECT id FROM `cris-cr`.pu_category_monthly_entry where active=1 and ((month>3 and year=%s) or (month<4 and year=%s)))
                    and  category_id in (Select id from `cris-cr`.assets_sub_category where main_asset=%s)''',[rs_financial_year,rs_year,rs[i]['id']])
                    # pu_user=('blw@pu','clw@pu','dmw@pu','icf@pu','mcf@pu','rcf@pu')
                    # cursor.execute('''SELECT category_id,sum(outturn) as outturn1
                    #     FROM `cris-cr`.pu_category_monthly_outturn where entry_id in 
                    #     (SELECT id FROM `cris-cr`.pu_category_monthly_entry where (month>3 and year=%s) or (month<4 and year=%s) and active=1 and pu in %s)
                    #     and  category_id in (Select id from `cris-cr`.assets_sub_category where main_asset=%s)''',[rs_financial_year,rs_year,pu_user,rs[i]['id']])
                    s3 = dictfetchall(cursor)
                    if s3:
                        s3=s3[0]['outturn1']
                    else:
                        s3=0
                    cursor.close()
                    rolling_stock.append({'id':rs[i]['asset'],'cum_prev':int(s0),'target': s1,'monthly_achvd':s2,'cum_achvd':s3,'same_month_of_previous_year':s5})
                    
        # # print(rolling_stock)
        if len(rolling_stock)==0:
            rolling_stock.append({'id':'Loco'})
            rolling_stock.append({'id':'Coach'})

    # FOR ROLLING STOCK (WAGONS) VIA ESB BY APEKSHA
        wagons ={}
        today=datetime.today()
        curr_yr=today.year
        fin_year=curr_yr
        curr_mon=today.month
        
        if curr_mon<4:
            fin_year=(today - relativedelta(months=12)).year
        
        if fin_year==curr_yr:
            prev_year=(today - relativedelta(months=12)).year
            next_year=(today + relativedelta(months=12)).year
        else:
            prev_year=(today - relativedelta(months=24)).year
            next_year=(today - relativedelta(months=12)).year


        # print("lst1",str(prev_year)+"-04-01",str(next_year)+"-03-31")
        lst1 = models.wagon_master.objects.filter(manufacture_date__range=[str(prev_year)+"-04-01",str(next_year)+"-03-31"]).count()
        month1 = rsp_month
        if month1!=1:
            month1-=1
        # if month1 <= 3:
        #     # print("lst2",str(prevyear)+"-04-01",date111)
        #     lst2 = models.wagon_master.objects.filter(manufacture_date__range=[str(prevyear)+"-04-01",date111]).count()
        # else:
        # print("lst2",str(fin_year)+"-04-01",str(curr_yr)+"-"+str(month1)+"-31")
        if month1==2:
            day="-28"
        elif month1==1 or month1==3 or month1==5 or month1==7 or month1==8 or month1==10 or month1==12:
            day="-31"
        else:
            day="-30"
        lst2 = models.wagon_master.objects.filter(manufacture_date__range=[str(fin_year)+"-04-01",str(curr_yr)+"-"+str(month1)+day]).count()
        
        
        # print("lst3",str(prev_year)+"-"+str(month1)+"-01",str(prev_year)+"-"+str(month1)+"-31")
        if month1>4:
            lst3 = models.wagon_master.objects.filter(manufacture_date__range=[str(prev_year)+"-"+str(month1)+"-01",str(prev_year)+"-"+str(month1)+day]).count()
        else:
            # print("lst3",str(fin_year)+"-"+str(month1)+"-01",str(fin_year)+"-"+str(month1)+"-31")
            lst3 = models.wagon_master.objects.filter(manufacture_date__range=[str(fin_year)+"-"+str(month1)+"-01",str(fin_year)+"-"+str(month1)+day]).count()


        # print("lst4",str(curr_yr)+"-"+str(month1)+"-01",str(curr_yr)+"-"+str(month1)+"-31")
        lst4 = models.wagon_master.objects.filter(manufacture_date__range=[str(curr_yr)+"-"+str(month1)+"-01",str(curr_yr)+"-"+str(month1)+day]).count()
        wagons.update({'Wagon Included' : {'prev_year' : lst1, 'cur_year' : lst2, 'prev_mnth': lst3, 'cur_mnth': lst4}})
        # print("Wagons",wagons) 

    ###################### CONTEXT 
        acci_date1=m9.LogApi.objects.filter(schedular_name='accident_data').values('dates').order_by('-dates')[0]['dates']
        acci_time=m9.LogApi.objects.filter(schedular_name='accident_data',dates=acci_date1).values('times').order_by('-times')[0]['times']
        load_com_today1=m9.LogApi.objects.filter(schedular_name='devinsapi_loading_commodity').values('dates').order_by('-dates')[0]['dates']
        load_com_time=m9.LogApi.objects.filter(schedular_name='devinsapi_loading_commodity',dates=load_com_today1).values('times').order_by('-times')[0]['times']
        load_zon_today1= m9.LogApi.objects.filter(schedular_name='devinsapi_loading_zonal').values('dates').order_by('-dates')[0]['dates']
        load_zon_time=m9.LogApi.objects.filter(schedular_name='devinsapi_loading_zonal',dates=load_zon_today1).values('times').order_by('-times')[0]['times']
        load_ovr_today1= m9.LogApi.objects.filter(schedular_name='devinsapi_loading_overall').values('dates').order_by('-dates')[0]['dates']
        load_ovr_time=m9.LogApi.objects.filter(schedular_name='devinsapi_loading_overall',dates=load_ovr_today1).values('times').order_by('-times')[0]['times']
        punc_today1= m9.LogApi.objects.filter(schedular_name='devinsapi_punctuality_service').values('dates').order_by('-dates')[0]['dates']
        punc_time=m9.LogApi.objects.filter(schedular_name='devinsapi_punctuality_service',dates=punc_today1).values('times').order_by('-times')[0]['times']
        punc_today1=punc_today1.strftime("%d/%m/%Y")
        earn_today1= m9.LogApi.objects.filter(schedular_name='earnings_data').values('dates').order_by('-dates')[0]['dates']
        earn_time=m9.LogApi.objects.filter(schedular_name='earnings_data',dates=earn_today1).values('times').order_by('-times')[0]['times']
        earn_today1=earn_today1.strftime("%d/%m/%Y")
        cap_today1= m9.LogApi.objects.filter(schedular_name='capex_data').values('dates').order_by('-dates')[0]['dates']
        cap_time=m9.LogApi.objects.filter(schedular_name='capex_data',dates=cap_today1).values('times').order_by('-times')[0]['times']
        cap_today1=cap_today1.strftime("%d/%m/%Y")
        ast_today1= m9.LogApi.objects.filter(schedular_name='devinsapi_punctuality_mrafdashboard').values('dates').order_by('-dates')[0]['dates']
        ast_time=m9.LogApi.objects.filter(schedular_name='devinsapi_punctuality_mrafdashboard',dates=ast_today1).values('times').order_by('-times')[0]['times']
        
        # print("hello")
        context={
            'assets_zones_data_month':assets_zones_data_month,
            'assets_zones_data':assets_zones_data,
            'assets_zones':assets_zones,
            'safety_zone':safety_zone,
            'acci_time':acci_time,
            'load_com_time':load_com_time,
            'load_zon_time':load_zon_time,
            'load_ovr_time':load_ovr_time,
            'punc_today1':punc_today1,
            'punc_time':punc_time,
            'earn_time':earn_time,
            'earn_today1':earn_today1,
            'cap_today1':cap_today1,
            'cap_time':cap_time,
            'ast_time':ast_time,

            'load_com_today':load_com_today,
            'load_zon_today':load_zon_today,
            'load_ovr_today':load_ovr_today,
            'load_com_prev':load_com_prev,
            'load_zon_prev':load_zon_prev,
            'load_ovr_prev':load_ovr_prev,
            'punc_today':punc_today,
            'punc_lastyear' :punc_lastyear,
            'punc_week':punc_week,
            'punc_month':punc_month,
            'rs_year':rs_financial_year,
            'rs_current_year':rs_year,
            'infra_year':infra_year,
            'year_capex1_short':year_capex1_short,
            'year_capex2_short':year_capex2_short,
            'acci_date':acci_date,
            'pre_acci_date':pre_acci_date,
            'asset_month':asset_month,
            'pre_month':pre_month,
            'max_updatedate':max_updatedate,
            'infra_month':infra_month,
            'rolling_stock':rolling_stock,
            'rs_month':rs_month,
            'rs_year_short':rs_year_short,
            'rs_financial_year':rs_financial_year,
            'rs_year_short_next':rs_year_short_next,
            'rs_prev_year':rs_prev_year,
            'rs_prev_year_short':rs_prev_year_short,
            'wagons':wagons,
            'load_comd':load_comd,
            'load_zone':load_zone,
            'load_overall':load_overall,
            'infrastructure':infrastructure,
            # 'loading_commodity_wise':commodity,
            # 'loading_commodity_wise1':commodity1,
            # 'loading_commodity_wise2':commodity2,
            'loading_zone_wise':zone,
            # 'loading_zone_wise1':zone1,
            # 'loading_zone_wise2':zone2,
            # 'earnings':earnings,
            'earnings1':earnings1,
            # 'earnings2':earnings2,
            'month_earnings1':month_earnings1,
            'year_earnings2':year_earnings2,
            'year_earnings1':year_earnings1,
            'month_capex1':month_capex1,
            'year_capex2':year_capex2,
            'year_capex1':year_capex1,
            'cymonth_capex':cymonth_capex,
            'pymonth_capex':pymonth_capex,
            'safety12':safety1,
            # 'safety':safety,
            # 'safety2':safety2,
            # 'safety_heads':safety_heads,
            # 'infrastructure_heads':infrastructure_heads,
            # 'loading_heads':loading_heads,
            'loading_b3_heads':loading_b3_heads,
            # 'asset_reliabilty_heads':asset_reliabilty_heads,
            'capex_heads':capex_heads,
            'capex_heads1':capex_heads1,
            # 'asset_reliabilty':data,
            # 'rolling_stock_production':rolling,
            # 'earnings_ap':earnings_ap,
            # 'owe_ap':owe_ap,
            # 'loading_b3_ap':loading_b3_ap,
            # 'punctuality_ap':punctuality_ap,
            # 'punctuality_dept_ap':punctuality_dept_ap,
            # 'rolling_stock_production_ap':rolling_stock_production_ap,
            'prev_month':prev_month,
            'assets':assets,
            'curdate':curdate,
            'prevyear':prevyear,
            'mnth':mnth,
            'safety1':safety1,
            'prevyear1':prevyear1,
            'prevyear':prevyear,
            'curyear':curyear,
            'curyear1':curyear1,
            'secprevyear1':secprevyear1,
            'secprevyear':secprevyear,
            'thirdprevyear':thirdprevyear,
            'date11':date11,
            'date12':date12,
            'earnings1':earnings1,
            'o':o,
            'temp':tempvg,
            'new':new,
            'dept_punctuality':dept_punctuality,
            'pu':users,
            'coal':coal,
            'port':port,
            'asset_day':asset_day,
            'asset_prev_yr':asset_prev_yr,
            
        }
        return render(request, 'my_edrishti1.html', context)

    # except Exception as e: 
    #         print(e)
    #         try:
    #             error_Table.objects.create(fun_name="do_dashboard",user_id=request.user,err_details=str(e))
    #         except:
    #             print("Internal Error!!!")
    #         return render(request, "homepage_errors.html", {})


def show_breakup(request):
    if request.method == "GET":
        rsname = request.GET.get('id')
        pu_user = request.GET.get('pu')
           
        # # print(rsname)
        rolling_stock=[]

        with connections['users'].cursor() as cursor:
            cursor.execute('''SELECT MAX(CAST(year as DECIMAL(8))) as year FROM `cris-cr`.pu_category_monthly_entry''')
            y1=dictfetchall(cursor)[0]['year']
            if y1:
                rs_year=int(y1)
            else:
                rs_year=date.today().year
            # # print('rs year',rs_year)
            cursor.execute('''SELECT  MAX(CAST(month as DECIMAL(8))) as month FROM `cris-cr`.pu_category_monthly_entry WHERE year=%s''',[rs_year])
            m1=dictfetchall(cursor)[0]['month']
            # print(m1)
            if m1:
                rsp_month=int(m1)+1
            else:
                rsp_month=date.today().month +1
            # print(rsp_month)
            rs_month=datetime.strptime(str(rsp_month-1),"%m").strftime("%b")
            
            rs_financial_year=rs_year
        
            if rsp_month <= 4:
                rs_financial_year=rs_year-1
            print(rs_financial_year,rs_year)
           
            rs_year_short=str(rs_financial_year)[2:4]

            cursor.execute('''SELECT id, asset FROM `cris-cr`.assets where asset LIKE '%Loco%' or asset LIKE '%Coach%' ''')
            rs1 = dictfetchall(cursor)

            if(rsname=='Wagon'):
                wagons=list(m9.wagon_breakup.objects.filter().values('id','cum_prev','target','monthly_achvd','cum_achvd','same_month_of_previous_year')) 
                print(wagons)
                context={'rs': wagons,}
                return JsonResponse(context,safe=False)

                # today=datetime.today()
                # date111=today
                # curr_yr=today.year
                # fin_year=curr_yr
                # curr_mon=today.month
                # if curr_mon<4:
                #     fin_year=(today - relativedelta(months=12)).year
                
                # if fin_year==curr_yr:
                #     prev_year=(today - relativedelta(months=12)).year
                #     next_year=(today + relativedelta(months=12)).year
                # else:
                #     prev_year=(today - relativedelta(months=24)).year
                #     next_year=(today - relativedelta(months=12)).year

                # wagons ={}
                # items=list(models.wagon_master.objects.filter().values('wagon_type').distinct())
                # # print(len(items))
                # for i in items:

                #     # print("lst1",str(prev_year)+"-04-01",str(next_year)+"-03-31")
                #     lst1 = models.wagon_master.objects.filter(manufacture_date__range=[str(prev_year)+"-04-01",str(next_year)+"-03-31"], wagon_type=i['wagon_type']).count()
                #     month1 = rsp_month
                #     if month1!=1:
                #         month1-=1
                        
                #     # print("lst2",str(fin_year)+"-04-01",date111)
                #     lst2 = models.wagon_master.objects.filter(manufacture_date__range=[str(fin_year)+"-04-01",str(curr_yr)+"-"+str(month1)+"-31"],wagon_type=i['wagon_type']).count()
                    
                    
                #     # print("lst3",str(prev_year)+"-"+str(month1)+"-01",str(prev_year)+"-"+str(month1)+"-31")
                #     if month1>3:
                #         lst3 = models.wagon_master.objects.filter(manufacture_date__range=[str(prev_year)+"-"+str(month1)+"-01",str(prev_year)+"-"+str(month1)+"-31"],wagon_type=i['wagon_type']).count()
                #     else:
                #         lst3 = models.wagon_master.objects.filter(manufacture_date__range=[str(fin_year)+"-"+str(month1)+"-01",str(fin_year)+"-"+str(month1)+"-31"],wagon_type=i['wagon_type']).count()

                #     # print("lst4",str(fin_year)+"-"+str(month1)+"-01",date111)
                #     lst4 = models.wagon_master.objects.filter(manufacture_date__range=[str(curr_yr)+"-"+str(month1)+"-01",str(curr_yr)+"-"+str(month1)+"-31"],wagon_type=i['wagon_type']).count()
                #     # wagons.update({'Wagon Included' : {'prev_year' : lst1, 'cur_year' : lst2, 'prev_mnth': lst3, 'cur_mnth': lst4}})

                #     rolling_stock.append({'id':i['wagon_type'],'cum_prev':lst1,'target':'NA','monthly_achvd':lst4,'cum_achvd':lst2,'same_month_of_previous_year':lst3})

                #     # # print("Wagons",wagons)   
                
                

        
            
            cursor.execute('''SELECT id, asset FROM `cris-cr`.assets where asset=%s''',[rsname])
            rs = dictfetchall(cursor)

            if(pu_user=='All'):
                # cursor.execute('''SELECT id,category from `cris-cr`.assets_sub_category where main_asset=%s''',[rs[0]['id']])
                # subrs = dictfetchall(cursor)
                cursor.execute('''SELECT id,category from `cris-cr`.assets_sub_category where id in
                (SELECT selected_category_id FROM `cris-cr`.pu_category_selected where entry_id in 
                (SELECT id FROM `cris-cr`.pu_category_select_entry where active=1)   
                ) and  main_asset=%s''',[rs[0]['id']])
                subrs = dictfetchall(cursor)
                # cursor.execute('''SELECT added_by FROM `cris-cr`.assets where asset LIKE '%Loco%' or asset LIKE '%Coach%' ''')
                # pu_user = dictfetchall(cursor)
                # cursor.execute('''SELECT username FROM `cris-cr`.users_details where username in ('blw@pu','clw@pu','dmw@pu','icf@pu','mcf@pu','rcf@pu')''')
                # pu_user = dictfetchall(cursor)
                pu_user=('blw@pu','clw@pu','dmw@pu','icf@pu','mcf@pu','rcf@pu')
                # print("hellooooooooooooooooooooooooo+++++++++++++++++++++++++++++++++++++++",pu_user)

            
            else:
                cursor.execute('''SELECT id,category from `cris-cr`.assets_sub_category where id in
                (SELECT selected_category_id FROM `cris-cr`.pu_category_selected where entry_id in 
                (SELECT id FROM `cris-cr`.pu_category_select_entry where pu_user_id=%s and active=1)   
                ) and  main_asset=%s''',[pu_user,rs[0]['id']])
                
                subrs = dictfetchall(cursor)
                pu_tup = ()
                pu_list=[]
                pu_list.append(pu_user)
                pu_tup = pu_tup + tuple(pu_list)
                pu_user = pu_tup
                # # print("hellooooooooooooooooooooooooo",type(pu_user), pu_user)

            len1=[]

            for i in range(len(rs1)):
                cursor.execute('''SELECT id,category from `cris-cr`.assets_sub_category where main_asset=%s''',[rs1[i]['id']])
                subrs1 = dictfetchall(cursor)
                # # print(len(subrs1))
                len1.append({rs1[i]['asset']:len(subrs1)})
            # # print(len1)

            rs_prev_year=rs_financial_year-1
            rs_prev_year_short=str(rs_prev_year)[2:4]
            # print(rs_financial_year,rs_year,rs_prev_year,"hello")
            
            if rs_financial_year == rs_year:
                for i in range(len(subrs)):
                    # # print(subrs[i])
                    cursor.execute('''
                    SELECT category_id,sum(outturn) FROM `cris-cr`.pu_category_monthly_outturn where category_id=%s and entry_id in 
                    (SELECT id FROM `cris-cr`.pu_category_monthly_entry where 
                    ((year=%s and month>3) or (year=%s and month<4)) and active=1 and pu in %s) 
                    group by category_id''',[subrs[i]['id'],rs_prev_year,rs_financial_year,pu_user])

                    s0 = dictfetchall(cursor)
                    # print(s0)
                    if s0:
                        c0= s0[0]['sum(outturn)']
                    else:
                        c0= '0'

                    cursor.execute('''SELECT category_id, sum(target) as target FROM `cris-cr`.pu_category_monthly_target where entry_id in 
                    (SELECT id FROM `cris-cr`.pu_category_target_entry where year=%s and active=1 and id>83 and pu in %s) 
                    and  category_id=%s group by category_id''',[rs_year,pu_user,subrs[i]['id']])
                    # latest_entry= dictfetchall(cursor)
                    # # print(latest_entry)

                    # cursor.execute('''SELECT * FROM `cris-cr`.pu_category_monthly_target where category_id=%s 
                    # order by entry_id desc''',[subrs[i]['id']])
                    s1 = dictfetchall(cursor)
                    # # print(s1)
                    if s1:
                        c1=s1[0]['target']
                        # c1=int(c1)
                        # c1=int((c1/12)*(rsp_month-4))
                    else:
                        c1='0'
            
                    cursor.execute('''SELECT category_id,CEILING(sum(outturn)) as outturn1
                    FROM `cris-cr`.pu_category_monthly_outturn where entry_id in 
                    (SELECT id FROM `cris-cr`.pu_category_monthly_entry where month=%s and year=%s and active=1 and pu in %s) 
                    and  category_id=%s group by category_id''',[rsp_month-1,rs_year,pu_user,subrs[i]['id']])
                    s2 = dictfetchall(cursor)
                    if s2:
                        c2=s2[0]['outturn1']
                    else:
                        c2='0'

                    cursor.execute('''SELECT category_id,CEILING(sum(outturn)) as outturn1
                    FROM `cris-cr`.pu_category_monthly_outturn where entry_id in 
                    (SELECT id FROM `cris-cr`.pu_category_monthly_entry where month=%s and year=%s and active=1 and pu in %s) 
                    and  category_id=%s group by category_id''',[rsp_month-1,rs_prev_year,pu_user,subrs[i]['id']])
                    s5 = dictfetchall(cursor)
                    if s5:
                        c5=s5[0]['outturn1']
                    else:
                        c5='0'
                    

                    cursor.execute('''SELECT category_id,sum(outturn) as outturn1
                    FROM `cris-cr`.pu_category_monthly_outturn where entry_id in 
                    (SELECT id FROM `cris-cr`.pu_category_monthly_entry where month>3 and year=%s and active=1 and pu in %s)
                    and category_id=%s group by category_id''',[rs_year,pu_user,subrs[i]['id']])
                    s3 = dictfetchall(cursor)
                    if s3:
                        c3=s3[0]['outturn1']
                    else:
                        c3='0'

                    rolling_stock.append({'id':subrs[i]['category'],'cum_prev':c0,'target':c1,'monthly_achvd':c2,'cum_achvd':c3,'same_month_of_previous_year':c5})
                # # print(rolling_stock)
            
           
            else:
                
                for i in range(len(subrs)):
                    cursor.execute('''SELECT category_id,sum(outturn) FROM `cris-cr`.pu_category_monthly_outturn where category_id=%s and entry_id in 
                    (SELECT id FROM `cris-cr`.pu_category_monthly_entry where 
                    ((year=%s and month>3) or (year=%s and month<4)) and active=1 and pu in %s) group by category_id''',
                    [subrs[i]['id'],rs_prev_year,rs_financial_year,pu_user])
                    s0 = dictfetchall(cursor)
                    if s0:
                        c0= s0[0]['sum(outturn)']
                    else:
                        c0= '0'

                    cursor.execute('''SELECT category_id, sum(target) as target FROM `cris-cr`.pu_category_monthly_target where entry_id in 
                    (SELECT id FROM `cris-cr`.pu_category_target_entry where year=%s and active=1 and id>83 and pu in %s) 
                    and  category_id=%s group by category_id''',[rs_financial_year,pu_user,subrs[i]['id']])
                    # cursor.execute('''SELECT * FROM `cris-cr`.pu_category_monthly_target where category_id=%s order by entry_id desc''',[subrs[i]['id'], rs_financial_year,rs_year])
                    s1 = dictfetchall(cursor)
                    if s1:
                        c1=s1[0]['target']
                        # c1=int(c1)
                        # c1=int((c1/12)*(rsp_month-4))
                    else:
                        cursor.execute('''SELECT category_id, sum(target) as target FROM `cris-cr`.pu_category_monthly_target where entry_id in 
                        (SELECT id FROM `cris-cr`.pu_category_target_entry where year=%s and active=1 and id>83 and pu in %s) 
                        and  category_id=%s group by category_id''',[rs_year,pu_user,subrs[i]['id']])
                        s1 = dictfetchall(cursor)
                        if s1:
                            c1=s1[0]['target']
                        else:
                            c1='0'

                    cursor.execute('''SELECT category_id,CEILING(sum(outturn)) as outturn1
                    FROM `cris-cr`.pu_category_monthly_outturn where entry_id in 
                    (SELECT id FROM `cris-cr`.pu_category_monthly_entry where month=%s and year=%s and active=1 and pu in %s) 
                    and  category_id=%s group by category_id''',[rsp_month-1,rs_year,pu_user,subrs[i]['id']])
                    s2 = dictfetchall(cursor)
                    if s2:
                        c2=s2[0]['outturn1']
                    else:
                        c2='0'

                    cursor.execute('''SELECT category_id,CEILING(sum(outturn)) as outturn1
                    FROM `cris-cr`.pu_category_monthly_outturn where entry_id in 
                    (SELECT id FROM `cris-cr`.pu_category_monthly_entry where month=%s and year=%s and active=1 and pu in %s) 
                    and  category_id=%s group by category_id''',[rsp_month-1,rs_financial_year,pu_user,subrs[i]['id']])
                    s5 = dictfetchall(cursor)
                    if s5:
                        c5=s5[0]['outturn1']
                    else:
                        c5='0'

                    cursor.execute('''SELECT category_id,sum(outturn) as outturn1
                    FROM `cris-cr`.pu_category_monthly_outturn where entry_id in 
                    (SELECT id FROM `cris-cr`.pu_category_monthly_entry where active=1 and pu in %s and ((month>3 and year=%s) or (month<4 and year=%s)))
                    and  category_id=%s group by category_id''',[pu_user,rs_financial_year,rs_year,subrs[i]['id']])
                    s3 = dictfetchall(cursor)
                    # print(s3,"apeksha")
                    if s3:
                        c3=s3[0]['outturn1']
                    else:
                        c3='0'
                    rolling_stock.append({'id':subrs[i]['category'],'cum_prev':c0,'target': c1,'monthly_achvd':c2,'cum_achvd':c3,'same_month_of_previous_year':c5})
            cursor.close()
        context={
            'rs': rolling_stock,
            'len1':len1,
        }
    return JsonResponse(context,safe=False)

def change_table(request):
    if request.method == "GET":
        puname = request.GET.get('pu')
        if puname == 'All':
            ################################################# rolling stock neilotpal #########################################
            rolling_stock=[]
            # rollimg stock date part:
            with connections['users'].cursor() as cursor:
                cursor.execute('''SELECT MAX(CAST(year as DECIMAL(8))) as year FROM `cris-cr`.pu_category_monthly_entry''')
                y1=dictfetchall(cursor)[0]['year']
                if y1:
                    rs_year=int(y1)
                else:
                    rs_year=date.today().year

                cursor.execute('''SELECT  MAX(CAST(month as DECIMAL(8))) as month FROM `cris-cr`.pu_category_monthly_entry WHERE year=%s''',[rs_year])
                mnth=dictfetchall(cursor)[0]['month']
                if mnth:
                    rsp_month=int(mnth)+1
                else:
                    rsp_month=date.today().month +1

                rs_month=datetime.strptime(str(rsp_month-1),"%m").strftime("%b")
                rs_financial_year=rs_year
            
                if rsp_month <= 4:
                    rs_financial_year=rs_year-1

                rs_year_short=str(rs_financial_year)[2:4]
                rs_year_short_next=int(rs_year_short)+1
                rs_prev_year=rs_financial_year-1
                rs_prev_year_short=str(rs_prev_year)[2:4]

                # rolling stock select button part:
                # cursor.execute('''SELECT username FROM `cris-cr`.users where username in ('blw@pu','clw@pu','dmw@pu','icf@pu','mcf@pu','rcf@pu')''')
                # users = dictfetchall(cursor)
                # # print("########################",users)

                # for i in range(len(users)):
                #     pu=users[i]['username']
                #     x = pu.split("@")
                #     users[i]['username']=x[0]

            
                cursor.execute('''SELECT id, asset FROM `cris-cr`.assets where asset LIKE '%Loco%' or asset LIKE '%Coach%' ''')
                rs = dictfetchall(cursor)
                # print(rs)
                cursor.execute('''SELECT added_by FROM `cris-cr`.assets where asset LIKE '%Loco%' or asset LIKE '%Coach%' ''')
                pu_user = dictfetchall(cursor)
                # pu_list=[]

                # for i in range(len(rs)):
                #     cursor.execute('''SELECT distinct(added_by) FROM `cris-cr`.assets_sub_category where main_asset=%s''',[rs[i]['id']])
                #     pu=dictfetchall(cursor)
                #     # print(pu)
                #     pu_list.extend(pu)
                # # print(pu_list)

                # stocks=[]
                if rs_financial_year == rs_year:
                    for i in range (len(rs)):
                        cursor.execute('''SELECT category_id,sum(outturn) FROM `cris-cr`.pu_category_monthly_outturn where category_id in 
                        (Select id from `cris-cr`.assets_sub_category where main_asset=%s) and entry_id in 
                        (SELECT id FROM `cris-cr`.pu_category_monthly_entry where ((year=%s and month>3) or (year=%s and month<4)) 
                        and active=1)''',[rs[i]['id'],rs_prev_year,rs_financial_year])
                        s0 = dictfetchall(cursor)
                    
                        # # print(s0)

                        cursor.execute('''SELECT category_id,sum(target) FROM `cris-cr`.pu_category_monthly_target where category_id in 
                                (Select id from `cris-cr`.assets_sub_category where main_asset=%s) and entry_id in 
                                (SELECT id FROM `cris-cr`.pu_category_target_entry where year=%s and active=1 and id>83)''',[rs[i]['id'], rs_year])
                        s1 = dictfetchall(cursor)[0]['sum(target)']
                        # s1=int(s1)
                        # s1=int((s1/12)*(rsp_month-4))
                        # ask sir about decimal
                        # # print(s1)
                        # # print('rsp_month',rsp_month)

                        cursor.execute('''SELECT category_id,CEILING(sum(outturn)) as outturn1
                        FROM `cris-cr`.pu_category_monthly_outturn where entry_id in 
                        (SELECT id FROM `cris-cr`.pu_category_monthly_entry where month=%s and year=%s and active=1) and  
                        category_id in (Select id from `cris-cr`.assets_sub_category where main_asset=%s)''',[rsp_month-1,rs_year,rs[i]['id']])
                        s2 = dictfetchall(cursor)
                        # if s2:
                        #     c2=s2[0]['outturn1']
                        # else:
                        #     c2='NA'
                        # # print(c2)
                        # # print(s2)
                        # if s2:
                        #     c2=s2[0]['outturn1']
                        #     c2=int(c2)
                        # else:
                        #     c2='NA'

                        # # print(c2)
                        # # print(s2)

                        cursor.execute('''SELECT category_id,CEILING(sum(outturn)) as outturn1
                        FROM `cris-cr`.pu_category_monthly_outturn where 
                        entry_id in (SELECT id FROM `cris-cr`.pu_category_monthly_entry where month=%s and year=%s and active=1) and  
                        category_id in (Select id from `cris-cr`.assets_sub_category where main_asset=%s)''',[rsp_month-1,rs_prev_year,rs[i]['id']])
                        s5 = dictfetchall(cursor)
                        # # print(s5)

                        cursor.execute('''SELECT category_id,sum(outturn) as outturn1
                        FROM `cris-cr`.pu_category_monthly_outturn where entry_id in (SELECT id FROM `cris-cr`.pu_category_monthly_entry where month>3 and year=%s and active=1)
                        and category_id in (Select id from `cris-cr`.assets_sub_category where main_asset=%s)''',[rs_year,rs[i]['id']])
                        s3 = dictfetchall(cursor)
                        # # print(s3)
                        
                        rolling_stock.append({'id':rs[i]['asset'],'cum_prev':s0[0]['sum(outturn)'],'target':s1,'monthly_achvd':s2[0]['outturn1'],'cum_achvd':s3[0]['outturn1'],'same_month_of_previous_year':s5[0]['outturn1']})
                        # stocks.append(rs[i]['asset'])
                else:
                    for i in range (len(rs)):
                        cursor.execute('''SELECT category_id,sum(outturn) FROM `cris-cr`.pu_category_monthly_outturn where category_id in 
                        (Select id from `cris-cr`.assets_sub_category where main_asset=%s) and entry_id in 
                        (SELECT id FROM `cris-cr`.pu_category_monthly_entry where ((year=%s and month>3) or (year=%s and month<4)) and active=1)''',
                        [rs[i]['id'],rs_prev_year,rs_financial_year])
                        s0 = dictfetchall(cursor)
                        # print(s0,"ok")
                        if s0:
                            s0=s0[0]['sum(outturn)']
                        else:
                            s0=0
                        # # print(s0)

                        cursor.execute('''SELECT category_id,sum(target) FROM `cris-cr`.pu_category_monthly_target where category_id in 
                        (Select id from `cris-cr`.assets_sub_category where main_asset=%s) and entry_id in 
                        (SELECT id FROM `cris-cr`.pu_category_target_entry where year=%s and active=1 and id>83  )''',
                        [rs[i]['id'],rs_year])
                        s1 = dictfetchall(cursor)
                        
                        if s1[0]['sum(target)']:
                            s1=s1[0]['sum(target)']
                        else:
                            cursor.execute('''SELECT category_id,sum(target) FROM `cris-cr`.pu_category_monthly_target where category_id in 
                            (Select id from `cris-cr`.assets_sub_category where main_asset=%s) and entry_id in 
                            (SELECT id FROM `cris-cr`.pu_category_target_entry where year=%s and active=1 and id>83 )''',
                            [rs[i]['id'],rs_financial_year])
                            s1 = dictfetchall(cursor)
                            # print(s1,"hellos")
                            if s1[0]['sum(target)']:
                                s1=s1[0]['sum(target)']
                            else:
                                s1=0


                        cursor.execute('''SELECT category_id,CEILING(sum(outturn)) as outturn1
                        FROM `cris-cr`.pu_category_monthly_outturn where entry_id in 
                        (SELECT id FROM `cris-cr`.pu_category_monthly_entry where month=%s and year=%s and active=1 ) and  category_id in 
                        (Select id from `cris-cr`.assets_sub_category where main_asset=%s)''',
                        [rsp_month-1,rs_year,rs[i]['id']])
                        s2 = dictfetchall(cursor)
                        if s2:
                            s2=s2[0]['outturn1']
                        else:
                            s2=0
                        # # print(s2)
        
                        cursor.execute('''SELECT category_id,CEILING(sum(outturn)) as outturn1
                        FROM `cris-cr`.pu_category_monthly_outturn where entry_id in 
                        (SELECT id FROM `cris-cr`.pu_category_monthly_entry where month=%s and year=%s and active=1) and  category_id in 
                        (Select id from `cris-cr`.assets_sub_category where main_asset=%s)''',
                        [rsp_month-1,rs_financial_year,rs[i]['id']])
                        s5 = dictfetchall(cursor)
                        if s5:
                            s5=s5[0]['outturn1']
                        else:
                            s5=0
                        # # print(s5)

                        cursor.execute('''SELECT category_id,sum(outturn) as outturn1
                        FROM `cris-cr`.pu_category_monthly_outturn where entry_id in 
                        (SELECT id FROM `cris-cr`.pu_category_monthly_entry where  active=1 and ((month>3 and year=%s) or (month<4 and year=%s)))
                        and  category_id in (Select id from `cris-cr`.assets_sub_category where main_asset=%s)''',
                        [rs_financial_year,rs_year,rs[i]['id']])
                        s3 = dictfetchall(cursor)
                        if s3:
                            s3=s3[0]['outturn1']
                        else:
                            s3=0

                        rolling_stock.append({'id':rs[i]['asset'],'cum_prev':s0,'target': s1,'monthly_achvd':s2,'cum_achvd':s3,'same_month_of_previous_year':s5})
                cursor.close()
                        # stocks.append(rs[i]['asset'])
            # # print(rolling_stock)
            if len(rolling_stock)==0:
                rolling_stock.append({'id':'Loco'})
                rolling_stock.append({'id':'Coach'})
        
        else:

            pu_user = puname
            
            rolling_stock=[]
            with connections['users'].cursor() as cursor:
                    
            # rollimg stock date part:
                    cursor.execute('''SELECT MAX(CAST(year as DECIMAL(8))) as year FROM `cris-cr`.pu_category_monthly_entry''')
                    y1=dictfetchall(cursor)[0]['year']
                    if y1:
                        rs_year=int(y1)
                    else:
                        rs_year=date.today().year

                    cursor.execute('''SELECT  MAX(CAST(month as DECIMAL(8))) as month FROM `cris-cr`.pu_category_monthly_entry WHERE year=%s''',[rs_year])
                    m1=dictfetchall(cursor)[0]['month']
                    if m1:
                        rsp_month=int(m1)+1
                    else:
                        rsp_month=date.today().month +1

                    rs_month=datetime.strptime(str(rsp_month-1),"%m").strftime("%b")
                    rs_financial_year=rs_year
                
                    if rsp_month <= 4:
                        rs_financial_year=rs_year-1

                    rs_year_short=str(rs_financial_year)[2:4]
                    rs_year_short_next=int(rs_year_short)+1
                    rs_prev_year=rs_financial_year-1
                    rs_prev_year_short=str(rs_prev_year)[2:4]

                    # cursor.execute('''SELECT id, asset FROM `cris-cr`.assets where added_by=%s''',[pu_user])
                    # rs = dictfetchall(cursor) 
                    
                    if pu_user in ['blw@pu','dmw@pu']:
                        cursor.execute('''SELECT id, asset FROM `cris-cr`.assets where asset LIKE '%Loco%'  ''')
                        rs = dictfetchall(cursor)
                    elif pu_user in ['clw@pu']:
                        cursor.execute('''SELECT id, asset FROM `cris-cr`.assets where asset LIKE '%Electric Loco%'  ''')
                        rs = dictfetchall(cursor)
                    elif pu_user in ['icf@pu','mcf@pu','rcf@pu']:
                        cursor.execute('''SELECT id, asset FROM `cris-cr`.assets where asset LIKE '%Coach%'  ''')
                        rs = dictfetchall(cursor)

                    # print("heyy",rs)
                    
                    if rs_financial_year == rs_year:
                        for i in range (len(rs)):
                            cursor.execute('''SELECT category_id,sum(outturn) FROM `cris-cr`.pu_category_monthly_outturn where category_id in 
                            (Select id from `cris-cr`.assets_sub_category where main_asset=%s) and entry_id in 
                            (SELECT id FROM `cris-cr`.pu_category_monthly_entry where ((year=%s and month>3) or (year=%s and month<4)) and active=1 and pu=%s)''',[rs[i]['id'],rs_prev_year,rs_financial_year,pu_user])
                            s0 = dictfetchall(cursor)
                        
                            # print(rs[i]['id'], rs_year,pu_user)
                            # cursor.execute('''SELECT category_id, sum(target) as target FROM `cris-cr`.pu_category_monthly_target where entry_id in 
                            # (SELECT id FROM `cris-cr`.pu_category_target_entry where year=%s and active=1 and id>83 and pu in %s) 
                            # and  category_id=%s group by category_id''',[rs_financial_year,pu_user,subrs[i]['id']])

                            cursor.execute('''SELECT category_id,sum(target) FROM `cris-cr`.pu_category_monthly_target where category_id in 
                            (Select id from `cris-cr`.assets_sub_category where main_asset=%s) and entry_id in 
                            (SELECT id FROM `cris-cr`.pu_category_target_entry where year=%s and active=1 and id>83 and pu = %s)''',[rs[i]['id'], rs_year,pu_user])
                            s1 = dictfetchall(cursor)[0]['sum(target)']
                            # print(s1)

                            cursor.execute('''SELECT category_id,CEILING(sum(outturn)) as outturn1
                            FROM `cris-cr`.pu_category_monthly_outturn where entry_id in 
                            (SELECT id FROM `cris-cr`.pu_category_monthly_entry where month=%s and year=%s and active=1 and pu=%s) and  category_id in 
                            (Select id from `cris-cr`.assets_sub_category where main_asset=%s)''',[rsp_month-1,rs_year,pu_user,rs[i]['id']])
                            s2 = dictfetchall(cursor)

                            cursor.execute('''SELECT category_id,sum(outturn) as outturn1
                            FROM `cris-cr`.pu_category_monthly_outturn where entry_id in 
                            (SELECT id FROM `cris-cr`.pu_category_monthly_entry where month>3 and year=%s and active=1 and pu=%s)
                            and category_id in (Select id from `cris-cr`.assets_sub_category where main_asset=%s)''',[rs_year,pu_user,rs[i]['id']])
                            s3 = dictfetchall(cursor)
                            # # print(s3)

                            cursor.execute('''SELECT category_id,CEILING(sum(outturn)) as outturn1
                            FROM `cris-cr`.pu_category_monthly_outturn where entry_id in 
                            (SELECT id FROM `cris-cr`.pu_category_monthly_entry where month=%s and year=%s and active=1 and pu=%s) and  category_id in 
                            (Select id from `cris-cr`.assets_sub_category where main_asset=%s)''',[rsp_month-1,rs_prev_year,pu_user,rs[i]['id']])
                            s5 = dictfetchall(cursor)

                            rolling_stock.append({'id':rs[i]['asset'],'cum_prev':s0[0]['sum(outturn)'],'target':s1,'monthly_achvd':s2[0]['outturn1'],'cum_achvd':s3[0]['outturn1'],'same_month_of_previous_year':s5[0]['outturn1']})
                            # stocks.append(rs[i]['asset'])
                    else:
                        for i in range (len(rs)):
                            cursor.execute('''SELECT category_id,sum(outturn) FROM `cris-cr`.pu_category_monthly_outturn 
                            where category_id in (Select id from `cris-cr`.assets_sub_category where main_asset=%s) and 
                            entry_id in (SELECT id FROM `cris-cr`.pu_category_monthly_entry 
                            where ((year=%s and month>3) or (year=%s and month<4)) and active=1 and pu=%s)''',
                            [rs[i]['id'],rs_prev_year,rs_financial_year,pu_user])
                            s0 = dictfetchall(cursor)
                            if s0:
                                s0=s0[0]['sum(outturn)']
                            else:
                                s0=0

                            cursor.execute('''SELECT category_id, sum(target) FROM `cris-cr`.pu_category_monthly_target 
                            where category_id in (Select id from `cris-cr`.assets_sub_category where main_asset=%s) 
                            and entry_id in (SELECT id FROM `cris-cr`.pu_category_target_entry where year=%s and active=1 and id>83 and pu = %s)''',
                            [rs[i]['id'],rs_year,pu_user])
                            s1 = dictfetchall(cursor)
                            print(s1,"hello")
                            if s1[0]['sum(target)']:
                                s1=s1[0]['sum(target)']
                            else:
                                cursor.execute('''SELECT category_id, sum(target) FROM `cris-cr`.pu_category_monthly_target 
                                where category_id in (Select id from `cris-cr`.assets_sub_category where main_asset=%s) 
                                and entry_id in (SELECT id FROM `cris-cr`.pu_category_target_entry where year=%s and active=1 and id>83 and pu = %s)''',
                                [rs[i]['id'],rs_financial_year,pu_user])
                                s1 = dictfetchall(cursor)
                                if s1:
                                    s1=s1[0]['sum(target)']
                                else:
                                    s1=0



                            cursor.execute('''SELECT category_id,CEILING(sum(outturn)) as outturn1
                            FROM `cris-cr`.pu_category_monthly_outturn where entry_id in 
                            (SELECT id FROM `cris-cr`.pu_category_monthly_entry where month=%s and year=%s and active=1 and pu=%s) 
                            and  category_id in (Select id from `cris-cr`.assets_sub_category where main_asset=%s)''',
                            [rsp_month-1,rs_year,pu_user,rs[i]['id']])
                            s2 = dictfetchall(cursor)
                            if s2:
                                s2=s2[0]['outturn1']
                            else:
                                s2=0
                            # # print(s2)
            
                            cursor.execute('''SELECT category_id,CEILING(sum(outturn)) as outturn1
                            FROM `cris-cr`.pu_category_monthly_outturn where entry_id in 
                            (SELECT id FROM `cris-cr`.pu_category_monthly_entry where month=%s and year=%s and active=1 and pu=%s) 
                            and  category_id in (Select id from `cris-cr`.assets_sub_category where main_asset=%s)''',
                            [rsp_month-1,rs_financial_year,pu_user,rs[i]['id']])
                            s5 = dictfetchall(cursor)
                            if s5:
                                s5=s5[0]['outturn1']
                            else:
                                s5=0
                            # # print(s5)

                            cursor.execute('''SELECT category_id,sum(outturn) as outturn1
                            FROM `cris-cr`.pu_category_monthly_outturn where entry_id in 
                            (SELECT id FROM `cris-cr`.pu_category_monthly_entry where active=1 and pu=%s and ((month>3 and year=%s) or (month<4 and year=%s)))
                            and  category_id in (Select id from `cris-cr`.assets_sub_category where main_asset=%s)''',
                            [pu_user,rs_financial_year,rs_year,rs[i]['id']])
                            # print(pu_user)
                            s3 = dictfetchall(cursor)
                            if s3:
                                s3=s3[0]['outturn1']
                            else:
                                s3=0

                            rolling_stock.append({'id':rs[i]['asset'],'cum_prev':s0,'target': s1,'monthly_achvd':s2,'cum_achvd':s3,'same_month_of_previous_year':s5})
                            # stocks.append(rs[i]['asset'])
                    cursor.close()
        context={
            'rs': rolling_stock,
            # 'stock' :stocks,
        }
    return JsonResponse(context,safe=False)            

def selectPeriod123(request):
    today= m9.LogApi.objects.filter(schedular_name='devinsapi_punctuality_service').values('dates').order_by('-dates')[0]['dates']
    today= today-relativedelta(days=1)
    lastyear = today - relativedelta(months=12)
    

    if request.method == "GET":
        data = request.GET.get('str')
        # print(data)
        if data == 'week':
            enddate = today
            startdate = today - relativedelta(days=6)
            lastdate = lastyear - relativedelta(days=6)
        elif data == 'month':
            enddate = today
            startdate = today - relativedelta(days=29)
            lastdate = lastyear - relativedelta(days=29)
        elif data == 'year':
            enddate = today
            startdate = today - relativedelta(months=12)
            lastdate = lastyear - relativedelta(months=12)

        # print(enddate,"today")
        # print(startdate,"week")
        # print(lastyear,"lastyear")
        # print(lastdate,"lastweek")
        
        # print("startdate",startdate,"enddate",enddate,'lastyear',lastyear,'lastdate',lastdate)
        temp_vga=[]
        causecodes_vga = ['PATH','INC','ENG','TFC','ORL','CNST','RUNO','ACC','LC','DCW']
        others_vga =['LO','WEA','DELC','ACP','ST','PBC','RE','DDSL','ELEC','PBOL','OHE','OPLNI','CONNI','ICW','MA','COM','IDSL','IELC','AGT','PRONI']
        zone_vga = list(m9.Punctuality_Service_Output.objects.all().values('Zone_Code').distinct())
    
        new_vga=list([{'department_code' : 'ELEC'},{'department_code' : 'RPF'},{'department_code' : 'TFC'},{'department_code' : 'COM'},{'department_code' : 'CNST'},{'department_code' : 'ST'},{'department_code' : 'MECH'},{'department_code' : 'ENG'},{'department_code': 'Others' }])
        xyz_vga=['ELEC','RPF', 'TFC','COM','CNST','ST', 'MECH', 'ENG']
        # ['RE','INC','OPLNI','RUNO','WEA','PATH','ACC','ORL','ACP','AGT','PRONI']
        temp_vga.extend(zone_vga)
        # print(temp_vga)
        o_vga=''
        for i in range(len(temp_vga)):
            try:
                nlt=0
                tc=0
                # print(temp_vga[i]['Zone_Code'])
                o_vga = list(m9.Punctuality_Service_Output.objects.filter(Zone_Code = temp_vga[i]['Zone_Code'] ,train_group ='M', Scheduled_Date__range = [startdate,enddate]).values())
                # print(o_vga)
                for o in o_vga:
                    # print('in',o)
                    nlt+=o['nlt_count']
                    tc+=o['train_count']
                pp=(nlt*100.0)/tc
                # print('out',pp)
                temp_vga[i].update({"pp":round(pp,2)})
            except:
                temp_vga[i].update({"pp":0})

        o1_vga =''
        for i in range(len(temp_vga)):
            try:
                nlt=0
                tc=0
                o1_vga = list(m9.Punctuality_Service_Output.objects.filter(Zone_Code = temp_vga[i]['Zone_Code'],train_group ='M' , Scheduled_Date__range = [lastdate,lastyear]).values())
                for o in o1_vga:
                    # print('in',o)
                    nlt+=o['nlt_count']
                    tc+=o['train_count']
                pp1=(nlt*100.0)/tc
                temp_vga[i].update({"pp1":round(pp1,2)})
            except:
                temp_vga[i].update({"pp1":0})

        for i in range(len(temp_vga)):
            temp_vga[i].update({"variation":round((temp_vga[i]['pp']-temp_vga[i]['pp1']),2)}) 

        for i in range(len(temp_vga)):
            listt_vga=[]
            for j in range(len(causecodes_vga)):
                try:
                    duration_vga = list(m9.Cause_Service_Output.objects.filter(Scheduled_Date__range = [startdate,enddate],Zone_Code = temp_vga[i]['Zone_Code'],cause_code = causecodes_vga[j],train_group='M').values_list('duration',flat=True))
                    durationsum_vga = sum(duration_vga)
                    listt_vga.append(durationsum_vga)
                except:
                    listt_vga.append(0)
            temp_vga[i].update({"sumofcause":listt_vga})

        for i in range(len(temp_vga)):
            litt_vga=[]
            for j in range(len(others_vga)):
                try:
                    duration1_vga = list(m9.Cause_Service_Output.objects.filter(Scheduled_Date__range = [startdate,enddate],Zone_Code = temp_vga[i]['Zone_Code'],cause_code = others_vga[j],train_group='M').values_list('duration',flat=True))
                    durationsum1_vga = sum(duration1_vga)
                    litt_vga.append(durationsum1_vga)
                except:
                    litt_vga.append(0)
            summm_vga = sum(litt_vga)
            temp_vga[i].update({"others":summm_vga})

        for i in range(len(new_vga)):
            newlist_vga=[]
            if new_vga[i]['department_code'] != "Others":
                for j in range(len(causecodes_vga)):
                    try:
                        duration2_vga = list(m9.Cause_Service_Output.objects.filter(Scheduled_Date__range = [startdate,enddate],department_code = new_vga[i]['department_code'],cause_code = causecodes_vga[j],train_group='M').values_list('duration',flat=True))
                        durationsum2_vga = sum(duration2_vga)
                        newlist_vga.append(durationsum2_vga)
                    except:
                        newlist_vga.append(0)
                new_vga[i].update({"sumofcause1":newlist_vga})
            else:
                for j in range(len(causecodes_vga)):
                    try:
                        duration2_vga = list(m9.Cause_Service_Output.objects.exclude(department_code__in=new_vga).filter(Scheduled_Date__range = [startdate,enddate],cause_code = causecodes_vga[j],train_group='M').values_list('duration',flat=True))
                        durationsum2_vga = sum(duration2_vga)
                        newlist_vga.append(durationsum2_vga)
                    except:
                        newlist_vga.append(0)
                new_vga[i].update({"sumofcause1":newlist_vga})


        for i in range(len(new_vga)):
            departlistothers_vga=[]
            if new_vga[i]['department_code'] != "Others":
                for j in range(len(others_vga)):
                    try:
                        durationdepart_vga = list(m9.Cause_Service_Output.objects.filter(Scheduled_Date__range = [startdate,enddate],department_code = new_vga[i]['department_code'],cause_code = others_vga[j],train_group='M').values_list('duration',flat=True))
                        departdurationsum1_vga = sum(durationdepart_vga)
                        departlistothers_vga.append(departdurationsum1_vga)
                    except:
                        departlistothers_vga.append(0)
                summ_vga = sum(departlistothers_vga)
                new_vga[i].update({"others":summ_vga})
            else:
                for j in range(len(others_vga)):
                    try:
                        durationdepart_vga = list(m9.Cause_Service_Output.objects.exclude(department_code__in=xyz_vga).filter(Scheduled_Date__range = [startdate,enddate],cause_code = others_vga[j],train_group='M').values_list('duration',flat=True))
                        departdurationsum1_vga = sum(durationdepart_vga)
                        departlistothers_vga.append(departdurationsum1_vga)
                    except:
                        departlistothers_vga.append(0)
                summ5_vga = sum(departlistothers_vga)
                new_vga[i].update({"others":summ5_vga})

        dept_punctuality={}
        dept_wise = list(m9.Cause_Service_Output.objects.values('department_code').distinct('department_code'))
        # print("dept_wise",dept_wise)
        for i in range(len(dept_wise)):
            cnt = m9.Cause_Service_Output.objects.filter(Scheduled_Date__range = [startdate,enddate],department_code=dept_wise[i]['department_code']).count()
            dept_code = dept_wise[i]['department_code']
            # print("dept_code",dept_code)
            # print('cnt',cnt)
            dept_punctuality.update({dept_code:cnt})
        # print("dept_punctuality11",dept_punctuality)

        temp_vga=sorted(temp_vga,key=lambda d: d['Zone_Code'] )
        context={
        'temp_vga':temp_vga,
        'new_vga':new_vga,
        'dept_punctuality':dept_punctuality
        }
    return JsonResponse(context,safe=False)  
    
def homepage(request):
    return render(request,"homepage.html")

def rail_madad(request):
    try:
        rail_today=(list(m9.railmadad_cause_graph.objects.filter(period=1).values('todate'))[0]['todate']).strftime("%d/%m/%Y")
        rail_yest=(list(m9.railmadad_cause_graph.objects.filter(period=1).values('fromdate'))[0]['fromdate']).strftime("%d/%m/%Y")
        rail_week=(list(m9.railmadad_cause_graph.objects.filter(period=7).values('fromdate'))[0]['fromdate']).strftime("%d/%m/%Y")
        rail_mon=(list(m9.railmadad_cause_graph.objects.filter(period=30).values('fromdate'))[0]['fromdate']).strftime("%d/%m/%Y")
        rail_day=m9.LogApi.objects.filter(schedular_name='rail_madad_bottomReports').values('dates').order_by('-dates')[0]['dates']
        rail_time=m9.LogApi.objects.filter(schedular_name='rail_madad_bottomReports',dates=rail_day).values('times').order_by('-times')[0]['times']
        rail_day=rail_day.strftime("%d/%m/%Y")
        # print(rail_today)
        complaint=[]
        zones=['CR','EO','EC','ER','IRC','KM','KR','NC','NE','NF','NR','NW','SB','SC','SE','SR','SW','WC','WR']
        zone_names={'CR':'CR','EO':'EOCR','EC':'ECR','ER':'ER','IRC':'IRCTC','KM':'KM','KR':'KR','NC':'NCR','NE':'NER','NF':'NFR','NR':'NR','NW':'NWR','SB':'SECR','SC':'SCR','SE':'SER','SR':'SR','SW':'SWR','WC':'WCR','WR':'WR'}
        zone_cause=[]
        complaints=['Cleanliness','Water Availability','Electrical Equipment','Catering & Vending Services','Security','Reserved Ticketing',
        'Unreserved Ticketing','Refund of Tickets','Passenger Amenities','Luggage / Parcels ','Goods','Punctuality']
        for z in zones:
            cause=[]
            cause1=[]
            recv1=sum(l['sint'] for l in list(m9.rail_madad_1.objects.annotate(sint=Cast('recv', IntegerField())).filter(znCode=z,period=1).values('sint')))
            settled=sum(l['sint'] for l in list(m9.rail_madad_1.objects.annotate(sint=Cast('settled', IntegerField())).filter(znCode=z,period=1).values('sint')))
            avg_pend_m=sum(l['sint'] for l in list(m9.rail_madad_1.objects.annotate(sint=Cast('avgPendencyDiffName', IntegerField())).filter(znCode=z,period=1).values('sint')))
            avg_pend_hr=sum(l['sint'] for l in list(m9.rail_madad_1.objects.annotate(sint=Cast('avgPendencyDiff', IntegerField())).filter(znCode=z,period=1).values('sint')))


            # zone_name=list(m9.rail_madad_1.objects.filter(znCode=z).values('znName'))
            # # print("zone name",zone_names[0][z])
            for c in complaints:
                    recv=sum(l['sint'] for l in list(m9.rail_madad_1.objects.annotate(sint=Cast('recv', IntegerField())).filter(znCode=z,pname=c,period=1).values('sint')))
                    # print( recv)
                    cause.append({str(c).split(' ')[0]+"recv":recv})
                    cause1.append(recv)
            recv=sum(l['sint'] for l in list(m9.rail_madad_1.objects.annotate(sint=Cast('recv', IntegerField())).filter(znCode=z,period=1).exclude(pname__in=complaints).values('sint')))
            cause1.append(recv)
            
            # zname=zone_name[0]
            avg_pend=avg_pend_hr*60+avg_pend_m
            zone_cause.append({'zone':zone_names[z],'values':cause1,'com_rcvd':recv1,'com_closed':settled,'avg_pend':avg_pend})
            # print(zone_cause)
        
    ######################## zone graph for yesterday#########################################

        zone_graphs_y= list(m9.railmadad_cause_graph.objects.filter(type=0,period=1).values())
        zone_list_y=[]
        cleanliness_zone_y=[]
        water_zone_y=[]
        electrical_zone_y=[]
        catering_zone_y=[]
        security_zone_y=[]
        r_ticketing_zone_y=[]
        u_ticketing_zone_y=[]
        refund_ticket_zone_y=[]
        pssngr_amenities_zone_y=[]
        luggage_zone_y=[]
        goods_zone_y=[]
        punctuality_zone_y=[]

        medical_zone_y=[]
        divyangjan_zone_y=[]
        woman_zone_y=[]
        corruption_zone_y=[]
        staff_zone_y=[]
        coach_clean_zone_y=[]
        coach_main_zone_y=[]
        bed_zone_y=[]

        other_zone_y=[]
        for b in zone_graphs_y:
            zone_list_y.append(b['name'])
            cleanliness_zone_y.append(b['cleanliness'])
            water_zone_y.append(b['water'])
            electrical_zone_y.append(b['electrical'])
            catering_zone_y.append(b['catering'])
            security_zone_y.append(b['security'])
            r_ticketing_zone_y.append(b['r_ticketing'])
            u_ticketing_zone_y.append(b['u_ticketing'])
            refund_ticket_zone_y.append(b['refund_ticket'])
            pssngr_amenities_zone_y.append(b['pssngr_amenities'])
            luggage_zone_y.append(b['luggage'])
            goods_zone_y.append(b['goods'])
            punctuality_zone_y.append(b['punctuality'])

            medical_zone_y.append(b['medical'])
            divyangjan_zone_y.append(b['divyangjan'])
            woman_zone_y.append(b['woman'])
            corruption_zone_y.append(b['corruption'])
            staff_zone_y.append(b['staff'])
            coach_clean_zone_y.append(b['coach_clean'])
            coach_main_zone_y.append(b['coach_main'])
            bed_zone_y.append(b['bed'])

            other_zone_y.append(b['other'])

    ######################## zone graph for 7 days#########################################
        zone_graphs_w= list(m9.railmadad_cause_graph.objects.filter(type=0,period=7).values())
        zone_list_w=[]
        cleanliness_zone_w=[]
        water_zone_w=[]
        electrical_zone_w=[]
        catering_zone_w=[]
        security_zone_w=[]
        r_ticketing_zone_w=[]
        u_ticketing_zone_w=[]
        refund_ticket_zone_w=[]
        pssngr_amenities_zone_w=[]
        luggage_zone_w=[]
        goods_zone_w=[]
        punctuality_zone_w=[]

        medical_zone_w=[]
        divyangjan_zone_w=[]
        woman_zone_w=[]
        corruption_zone_w=[]
        staff_zone_w=[]
        coach_clean_zone_w=[]
        coach_main_zone_w=[]
        bed_zone_w=[]

        other_zone_w=[]
        for b in zone_graphs_w:
            zone_list_w.append(b['name'])
            cleanliness_zone_w.append(b['cleanliness'])
            water_zone_w.append(b['water'])
            electrical_zone_w.append(b['electrical'])
            catering_zone_w.append(b['catering'])
            security_zone_w.append(b['security'])
            r_ticketing_zone_w.append(b['r_ticketing'])
            u_ticketing_zone_w.append(b['u_ticketing'])
            refund_ticket_zone_w.append(b['refund_ticket'])
            pssngr_amenities_zone_w.append(b['pssngr_amenities'])
            luggage_zone_w.append(b['luggage'])
            goods_zone_w.append(b['goods'])
            punctuality_zone_w.append(b['punctuality'])

            medical_zone_w.append(b['medical'])
            divyangjan_zone_w.append(b['divyangjan'])
            woman_zone_w.append(b['woman'])
            corruption_zone_w.append(b['corruption'])
            staff_zone_w.append(b['staff'])
            coach_clean_zone_w.append(b['coach_clean'])
            coach_main_zone_w.append(b['coach_main'])
            bed_zone_w.append(b['bed'])

            other_zone_w.append(b['other'])

    ######################## zone graph for 30 days#########################################
        zone_graphs_m= list(m9.railmadad_cause_graph.objects.filter(type=0,period=30).values())
        zone_list_m=[]
        cleanliness_zone_m=[]
        water_zone_m=[]
        electrical_zone_m=[]
        catering_zone_m=[]
        security_zone_m=[]
        r_ticketing_zone_m=[]
        u_ticketing_zone_m=[]
        refund_ticket_zone_m=[]
        pssngr_amenities_zone_m=[]
        luggage_zone_m=[]
        goods_zone_m=[]
        punctuality_zone_m=[]

        medical_zone_m=[]
        divyangjan_zone_m=[]
        woman_zone_m=[]
        corruption_zone_m=[]
        staff_zone_m=[]
        coach_clean_zone_m=[]
        coach_main_zone_m=[]
        bed_zone_m=[]

        other_zone_m=[]
        for b in zone_graphs_m:
            zone_list_m.append(b['name'])
            cleanliness_zone_m.append(b['cleanliness'])
            water_zone_m.append(b['water'])
            electrical_zone_m.append(b['electrical'])
            catering_zone_m.append(b['catering'])
            security_zone_m.append(b['security'])
            r_ticketing_zone_m.append(b['r_ticketing'])
            u_ticketing_zone_m.append(b['u_ticketing'])
            refund_ticket_zone_m.append(b['refund_ticket'])
            pssngr_amenities_zone_m.append(b['pssngr_amenities'])
            luggage_zone_m.append(b['luggage'])
            goods_zone_m.append(b['goods'])
            punctuality_zone_m.append(b['punctuality'])

            medical_zone_m.append(b['medical'])
            divyangjan_zone_m.append(b['divyangjan'])
            woman_zone_m.append(b['woman'])
            corruption_zone_m.append(b['corruption'])
            staff_zone_m.append(b['staff'])
            coach_clean_zone_m.append(b['coach_clean'])
            coach_main_zone_m.append(b['coach_main'])
            bed_zone_m.append(b['bed'])

            other_zone_m.append(b['other'])

    ######################## division graph for yesterday#########################################
        div_graphs_y= list(m9.railmadad_cause_graph.objects.filter(type=1,period=1).values())
        div_list_y=[]
        cleanliness_div_y=[]
        water_div_y=[]
        electrical_div_y=[]
        catering_div_y=[]
        security_div_y=[]
        r_ticketing_div_y=[]
        u_ticketing_div_y=[]
        refund_ticket_div_y=[]
        pssngr_amenities_div_y=[]
        luggage_div_y=[]
        goods_div_y=[]
        punctuality_div_y=[]

        medical_div_y=[]
        divyangjan_div_y=[]
        woman_div_y=[]
        corruption_div_y=[]
        staff_div_y=[]
        coach_clean_div_y=[]
        coach_main_div_y=[]
        bed_div_y=[]

        other_div_y=[]
        for b in div_graphs_y:
            div_list_y.append(b['name'])
            cleanliness_div_y.append(b['cleanliness'])
            water_div_y.append(b['water'])
            electrical_div_y.append(b['electrical'])
            catering_div_y.append(b['catering'])
            security_div_y.append(b['security'])
            r_ticketing_div_y.append(b['r_ticketing'])
            u_ticketing_div_y.append(b['u_ticketing'])
            refund_ticket_div_y.append(b['refund_ticket'])
            pssngr_amenities_div_y.append(b['pssngr_amenities'])
            luggage_div_y.append(b['luggage'])
            goods_div_y.append(b['goods'])
            punctuality_div_y.append(b['punctuality'])

            medical_div_y.append(b['medical'])
            divyangjan_div_y.append(b['divyangjan'])
            woman_div_y.append(b['woman'])
            corruption_div_y.append(b['corruption'])
            staff_div_y.append(b['staff'])
            coach_clean_div_y.append(b['coach_clean'])
            coach_main_div_y.append(b['coach_main'])
            bed_div_y.append(b['bed'])

            other_div_y.append(b['other'])

    ######################## div graph for 7 days#########################################
        div_graphs_w= list(m9.railmadad_cause_graph.objects.filter(type=1,period=7).values())
        div_list_w=[]
        cleanliness_div_w=[]
        water_div_w=[]
        electrical_div_w=[]
        catering_div_w=[]
        security_div_w=[]
        r_ticketing_div_w=[]
        u_ticketing_div_w=[]
        refund_ticket_div_w=[]
        pssngr_amenities_div_w=[]
        luggage_div_w=[]
        goods_div_w=[]
        punctuality_div_w=[]

        medical_div_w=[]
        divyangjan_div_w=[]
        woman_div_w=[]
        corruption_div_w=[]
        staff_div_w=[]
        coach_clean_div_w=[]
        coach_main_div_w=[]
        bed_div_w=[]

        other_div_w=[]
        for b in div_graphs_w:
            div_list_w.append(b['name'])
            cleanliness_div_w.append(b['cleanliness'])
            water_div_w.append(b['water'])
            electrical_div_w.append(b['electrical'])
            catering_div_w.append(b['catering'])
            security_div_w.append(b['security'])
            r_ticketing_div_w.append(b['r_ticketing'])
            u_ticketing_div_w.append(b['u_ticketing'])
            refund_ticket_div_w.append(b['refund_ticket'])
            pssngr_amenities_div_w.append(b['pssngr_amenities'])
            luggage_div_w.append(b['luggage'])
            goods_div_w.append(b['goods'])
            punctuality_div_w.append(b['punctuality'])

            medical_div_w.append(b['medical'])
            divyangjan_div_w.append(b['divyangjan'])
            woman_div_w.append(b['woman'])
            corruption_div_w.append(b['corruption'])
            staff_div_w.append(b['staff'])
            coach_clean_div_w.append(b['coach_clean'])
            coach_main_div_w.append(b['coach_main'])
            bed_div_w.append(b['bed'])

            other_div_w.append(b['other'])

    ######################## div graph for 30 days#########################################
        div_graphs_m= list(m9.railmadad_cause_graph.objects.filter(type=1,period=30).values())
        div_list_m=[]
        cleanliness_div_m=[]
        water_div_m=[]
        electrical_div_m=[]
        catering_div_m=[]
        security_div_m=[]
        r_ticketing_div_m=[]
        u_ticketing_div_m=[]
        refund_ticket_div_m=[]
        pssngr_amenities_div_m=[]
        luggage_div_m=[]
        goods_div_m=[]
        punctuality_div_m=[]

        medical_div_m=[]
        divyangjan_div_m=[]
        woman_div_m=[]
        corruption_div_m=[]
        staff_div_m=[]
        coach_clean_div_m=[]
        coach_main_div_m=[]
        bed_div_m=[]

        other_div_m=[]
        for b in div_graphs_m:
            div_list_m.append(b['name'])
            cleanliness_div_m.append(b['cleanliness'])
            water_div_m.append(b['water'])
            electrical_div_m.append(b['electrical'])
            catering_div_m.append(b['catering'])
            security_div_m.append(b['security'])
            r_ticketing_div_m.append(b['r_ticketing'])
            u_ticketing_div_m.append(b['u_ticketing'])
            refund_ticket_div_m.append(b['refund_ticket'])
            pssngr_amenities_div_m.append(b['pssngr_amenities'])
            luggage_div_m.append(b['luggage'])
            goods_div_m.append(b['goods'])
            punctuality_div_m.append(b['punctuality'])

            medical_div_m.append(b['medical'])
            divyangjan_div_m.append(b['divyangjan'])
            woman_div_m.append(b['woman'])
            corruption_div_m.append(b['corruption'])
            staff_div_m.append(b['staff'])
            coach_clean_div_m.append(b['coach_clean'])
            coach_main_div_m.append(b['coach_main'])
            bed_div_m.append(b['bed'])

            other_div_m.append(b['other'])

    ######################## train graph for yesterday#########################################
        train_graphs_y= list(m9.railmadad_cause_graph.objects.filter(type=2,period=1).values())
        train_list_y=[]
        train_names_y=[]
        cleanliness_train_y=[]
        water_train_y=[]
        electrical_train_y=[]
        catering_train_y=[]
        security_train_y=[]
        r_ticketing_train_y=[]
        u_ticketing_train_y=[]
        refund_ticket_train_y=[]
        pssngr_amenities_train_y=[]
        luggage_train_y=[]
        goods_train_y=[]
        punctuality_train_y=[]

        medical_train_y=[]
        divyangjan_train_y=[]
        woman_train_y=[]
        corruption_train_y=[]
        staff_train_y=[]
        coach_clean_train_y=[]
        coach_main_train_y=[]
        bed_train_y=[]

        other_train_y=[]
        for b in train_graphs_y:
            train_list_y.append(b['name'])
            n=list(models.train_master.objects.filter(train_no=b['name']).values('train_name'))
            # print(n)
            if n:
                train_names_y.append(n[0]['train_name'])
            else:
                train_names_y.append(b['name'])
            cleanliness_train_y.append(b['cleanliness'])
            water_train_y.append(b['water'])
            electrical_train_y.append(b['electrical'])
            catering_train_y.append(b['catering'])
            security_train_y.append(b['security'])
            r_ticketing_train_y.append(b['r_ticketing'])
            u_ticketing_train_y.append(b['u_ticketing'])
            refund_ticket_train_y.append(b['refund_ticket'])
            pssngr_amenities_train_y.append(b['pssngr_amenities'])
            luggage_train_y.append(b['luggage'])
            goods_train_y.append(b['goods'])
            punctuality_train_y.append(b['punctuality'])

            medical_train_y.append(b['medical'])
            divyangjan_train_y.append(b['divyangjan'])
            woman_train_y.append(b['woman'])
            corruption_train_y.append(b['corruption'])
            staff_train_y.append(b['staff'])
            coach_clean_train_y.append(b['coach_clean'])
            coach_main_train_y.append(b['coach_main'])
            bed_train_y.append(b['bed'])

            other_train_y.append(b['other'])

    ######################## train graph for 7 days#########################################
        train_graphs_w= list(m9.railmadad_cause_graph.objects.filter(type=2,period=7).values())
        train_list_w=[]
        train_names_w=[]
        cleanliness_train_w=[]
        water_train_w=[]
        electrical_train_w=[]
        catering_train_w=[]
        security_train_w=[]
        r_ticketing_train_w=[]
        u_ticketing_train_w=[]
        refund_ticket_train_w=[]
        pssngr_amenities_train_w=[]
        luggage_train_w=[]
        goods_train_w=[]
        punctuality_train_w=[]

        medical_train_w=[]
        divyangjan_train_w=[]
        woman_train_w=[]
        corruption_train_w=[]
        staff_train_w=[]
        coach_clean_train_w=[]
        coach_main_train_w=[]
        bed_train_w=[]

        other_train_w=[]
        for b in train_graphs_w:
            train_list_w.append(b['name'])
            n=list(models.train_master.objects.filter(train_no=b['name']).values('train_name'))
            # print(n)
            if n:
                train_names_w.append(n[0]['train_name'])
            else:
                train_names_w.append(b['name'])
            cleanliness_train_w.append(b['cleanliness'])
            water_train_w.append(b['water'])
            electrical_train_w.append(b['electrical'])
            catering_train_w.append(b['catering'])
            security_train_w.append(b['security'])
            r_ticketing_train_w.append(b['r_ticketing'])
            u_ticketing_train_w.append(b['u_ticketing'])
            refund_ticket_train_w.append(b['refund_ticket'])
            pssngr_amenities_train_w.append(b['pssngr_amenities'])
            luggage_train_w.append(b['luggage'])
            goods_train_w.append(b['goods'])
            punctuality_train_w.append(b['punctuality'])

            medical_train_w.append(b['medical'])
            divyangjan_train_w.append(b['divyangjan'])
            woman_train_w.append(b['woman'])
            corruption_train_w.append(b['corruption'])
            staff_train_w.append(b['staff'])
            coach_clean_train_w.append(b['coach_clean'])
            coach_main_train_w.append(b['coach_main'])
            bed_train_w.append(b['bed'])

            other_train_w.append(b['other'])

    ######################## train graph for 30 days#########################################
        train_graphs_m= list(m9.railmadad_cause_graph.objects.filter(type=2,period=30).values())
        train_list_m=[]
        train_names_m=[]
        cleanliness_train_m=[]
        water_train_m=[]
        electrical_train_m=[]
        catering_train_m=[]
        security_train_m=[]
        r_ticketing_train_m=[]
        u_ticketing_train_m=[]
        refund_ticket_train_m=[]
        pssngr_amenities_train_m=[]
        luggage_train_m=[]
        goods_train_m=[]
        punctuality_train_m=[]

        medical_train_m=[]
        divyangjan_train_m=[]
        woman_train_m=[]
        corruption_train_m=[]
        staff_train_m=[]
        coach_clean_train_m=[]
        coach_main_train_m=[]
        bed_train_m=[]

        other_train_m=[]
        for b in train_graphs_m:
            train_list_m.append(b['name'])
            n=list(models.train_master.objects.filter(train_no=b['name']).values('train_name'))
            # print(n)
            if n:
                train_names_m.append(n[0]['train_name'])
            else:
                train_names_m.append(b['name'])
            cleanliness_train_m.append(b['cleanliness'])
            water_train_m.append(b['water'])
            electrical_train_m.append(b['electrical'])
            catering_train_m.append(b['catering'])
            security_train_m.append(b['security'])
            r_ticketing_train_m.append(b['r_ticketing'])
            u_ticketing_train_m.append(b['u_ticketing'])
            refund_ticket_train_m.append(b['refund_ticket'])
            pssngr_amenities_train_m.append(b['pssngr_amenities'])
            luggage_train_m.append(b['luggage'])
            goods_train_m.append(b['goods'])
            punctuality_train_m.append(b['punctuality'])

            medical_train_m.append(b['medical'])
            divyangjan_train_m.append(b['divyangjan'])
            woman_train_m.append(b['woman'])
            corruption_train_m.append(b['corruption'])
            staff_train_m.append(b['staff'])
            coach_clean_train_m.append(b['coach_clean'])
            coach_main_train_m.append(b['coach_main'])
            bed_train_m.append(b['bed'])

            other_train_m.append(b['other'])

    ################## OLD GRAPH #################
        # zone_list_y=[]
        # zone_values_y=[]
        # bottom_zones=list(m9.railmadad_bottom_reports.objects.filter(type=0,period=1).values('name','total'))
        # for b in bottom_zones:
        #     zone_list_y.append(b['name'])
        #     zone_values_y.append(b['total'])
        # # # print(bottom_zones)
        # div_list_y=[]
        # div_values_y=[]
        # bottom_zones=list(m9.railmadad_bottom_reports.objects.filter(type=1,period=1).values('name','total'))
        # for b in bottom_zones:
        #     div_list_y.append(b['name'])
        #     div_values_y.append(b['total'])
        # # # print(div_values_y,div_list_y)
        # train_list_y=[]
        # train_values_y=[]
        # bottom_zones=list(m9.railmadad_bottom_reports.objects.filter(type=2,period=1).values('name','total'))
        # for b in bottom_zones:
        #     train_list_y.append(b['name'])
        #     train_values_y.append(b['total'])

        # zone_list_w=[]
        # zone_values_w=[]
        # bottom_zones=list(m9.railmadad_bottom_reports.objects.filter(type=0,period=7).values('name','total'))
        # for b in bottom_zones:
        #     zone_list_w.append(b['name'])
        #     zone_values_w.append(b['total'])
        # # # print(bottom_zones)
        # div_list_w=[]
        # div_values_w=[]
        # bottom_zones=list(m9.railmadad_bottom_reports.objects.filter(type=1,period=7).values('name','total'))
        # for b in bottom_zones:
        #     div_list_w.append(b['name'])
        #     div_values_w.append(b['total'])
        # train_list_w=[]
        # train_values_w=[]
        # bottom_zones=list(m9.railmadad_bottom_reports.objects.filter(type=2,period=7).values('name','total'))
        # for b in bottom_zones:
        #     train_list_w.append(b['name'])
        #     train_values_w.append(b['total'])

        # zone_list_m=[]
        # zone_values_m=[]
        # bottom_zones=list(m9.railmadad_bottom_reports.objects.filter(type=0,period=30).values('name','total'))
        # for b in bottom_zones:
        #     zone_list_m.append(b['name'])
        #     zone_values_m.append(b['total'])
        # # # print(bottom_zones)
        # div_list_m=[]
        # div_values_m=[]
        # bottom_zones=list(m9.railmadad_bottom_reports.objects.filter(type=1,period=30).values('name','total'))
        # for b in bottom_zones:
        #     div_list_m.append(b['name'])
        #     div_values_m.append(b['total'])
        # train_list_m=[]
        # train_values_m=[]
        # bottom_zones=list(m9.railmadad_bottom_reports.objects.filter(type=2,period=30).values('name','total'))
        # for b in bottom_zones:
        #     train_list_m.append(b['name'])
        #     train_values_m.append(b['total'])

    ##### CONTEXT RAILMADAD
        periods=[{'key':7,'value':'Last 7 days', 'fromdate':rail_week},{'key':30,'value':'Last 30 days','fromdate':rail_mon}]

    
        context={
            'rail_day':rail_day,
            'rail_time':rail_time,
            'rail_today':rail_today,
            'rail_yest':rail_yest,
            'rail_week':rail_week,
            'rail_mon':rail_mon,
            'periods':periods,
            'complaint':complaint,
            # 'bottom_zones':bottom_zones,
            'zone_cause':zone_cause,

            # 'zone_list_y':zone_list_y,
            # 'zone_values_y':zone_values_y,
            # 'train_list_y':train_list_y,
            # 'train_values_y':train_values_y,
            # 'div_list_y':div_list_y,
            # 'div_values_y':div_values_y,

            # 'zone_list_w':zone_list_w,
            # 'zone_values_w':zone_values_w,
            # 'train_list_w':train_list_w,
            # 'train_values_w':train_values_w,
            # 'div_list_w':div_list_w,
            # 'div_values_w':div_values_w,

            # 'zone_list_m':zone_list_m,
            # 'zone_values_m':zone_values_m,
            # 'train_list_m':train_list_m,
            # 'train_values_m':train_values_m,
            # 'div_list_m':div_list_m,
            # 'div_values_m':div_values_m,

            'div_list_y':div_list_y,
            'cleanliness_div_y':cleanliness_div_y,
            'water_div_y':water_div_y,
            'electrical_div_y':electrical_div_y,
            'catering_div_y':catering_div_y,
            'security_div_y':security_div_y,
            'r_ticketing_div_y':r_ticketing_div_y,
            'u_ticketing_div_y':u_ticketing_div_y,
            'refund_ticket_div_y':refund_ticket_div_y,
            'pssngr_amenities_div_y':pssngr_amenities_div_y,
            'luggage_div_y':luggage_div_y,
            'goods_div_y':goods_div_y,
            'punctuality_div_y':punctuality_div_y,
            'medical_div_y':medical_div_y,
            'divyangjan_div_y':divyangjan_div_y,
            'woman_div_y':woman_div_y,
            'corruption_div_y':corruption_div_y,
            'staff_div_y':staff_div_y,
            'coach_clean_div_y':coach_clean_div_y,
            'coach_main_div_y':coach_main_div_y,
            'bed_div_y':bed_div_y,
            'other_div_y':other_div_y,

            'div_list_w'               :div_list_w,
            'cleanliness_div_w'        :cleanliness_div_w,
            'water_div_w'              :water_div_w,
            'electrical_div_w'         :electrical_div_w,
            'catering_div_w'           :catering_div_w,
            'security_div_w'           :security_div_w,
            'r_ticketing_div_w'        :r_ticketing_div_w,
            'u_ticketing_div_w'        :u_ticketing_div_w,
            'refund_ticket_div_w'      :refund_ticket_div_w,
            'pssngr_amenities_div_w'   :pssngr_amenities_div_w,
            'luggage_div_w'            :luggage_div_w,
            'goods_div_w'              :goods_div_w,
            'punctuality_div_w'        :punctuality_div_w,
            'medical_div_w':medical_div_w,
            'divyangjan_div_w':divyangjan_div_w,
            'woman_div_w':woman_div_w,
            'corruption_div_w':corruption_div_w,
            'staff_div_w':staff_div_w,
            'coach_clean_div_w':coach_clean_div_w,
            'coach_main_div_w':coach_main_div_w,
            'bed_div_w':bed_div_w,
            'other_div_w'              :other_div_w,

            'div_list_m'               :div_list_m,
            'cleanliness_div_m'        :cleanliness_div_m,
            'water_div_m'              :water_div_m,
            'electrical_div_m'         :electrical_div_m,
            'catering_div_m'           :catering_div_m,
            'security_div_m'           :security_div_m,
            'r_ticketing_div_m'        :r_ticketing_div_m,
            'u_ticketing_div_m'        :u_ticketing_div_m,
            'refund_ticket_div_m'      :refund_ticket_div_m,
            'pssngr_amenities_div_m'   :pssngr_amenities_div_m,
            'luggage_div_m'            :luggage_div_m,
            'goods_div_m'              :goods_div_m,
            'punctuality_div_m'        :punctuality_div_m,
            'medical_div_m':medical_div_m,
            'divyangjan_div_m':divyangjan_div_m,
            'woman_div_m':woman_div_m,
            'corruption_div_m':corruption_div_m,
            'staff_div_m':staff_div_m,
            'coach_clean_div_m':coach_clean_div_m,
            'coach_main_div_m':coach_main_div_m,
            'bed_div_m':bed_div_m,
            'other_div_m'              :other_div_m,

            'zone_list_y':zone_list_y,
            'cleanliness_zone_y':cleanliness_zone_y,
            'water_zone_y':water_zone_y,
            'electrical_zone_y':electrical_zone_y,
            'catering_zone_y':catering_zone_y,
            'security_zone_y':security_zone_y,
            'r_ticketing_zone_y':r_ticketing_zone_y,
            'u_ticketing_zone_y':u_ticketing_zone_y,
            'refund_ticket_zone_y':refund_ticket_zone_y,
            'pssngr_amenities_zone_y':pssngr_amenities_zone_y,
            'luggage_zone_y':luggage_zone_y,
            'goods_zone_y':goods_zone_y,
            'punctuality_zone_y':punctuality_zone_y,
            'medical_zone_y':medical_zone_y,
            'divyangjan_zone_y':divyangjan_zone_y,
            'woman_zone_y':woman_zone_y,
            'corruption_zone_y':corruption_zone_y,
            'staff_zone_y':staff_zone_y,
            'coach_clean_zone_y':coach_clean_zone_y,
            'coach_main_zone_y':coach_main_zone_y,
            'bed_zone_y':bed_zone_y,
            'other_zone_y':other_zone_y,

            'zone_list_w'               :zone_list_w,
            'cleanliness_zone_w'        :cleanliness_zone_w,
            'water_zone_w'              :water_zone_w,
            'electrical_zone_w'         :electrical_zone_w,
            'catering_zone_w'           :catering_zone_w,
            'security_zone_w'           :security_zone_w,
            'r_ticketing_zone_w'        :r_ticketing_zone_w,
            'u_ticketing_zone_w'        :u_ticketing_zone_w,
            'refund_ticket_zone_w'      :refund_ticket_zone_w,
            'pssngr_amenities_zone_w'   :pssngr_amenities_zone_w,
            'luggage_zone_w'            :luggage_zone_w,
            'goods_zone_w'              :goods_zone_w,
            'punctuality_zone_w'        :punctuality_zone_w,
            'medical_zone_w':medical_zone_w,
            'divyangjan_zone_w':divyangjan_zone_w,
            'woman_zone_w':woman_zone_w,
            'corruption_zone_w':corruption_zone_w,
            'staff_zone_w':staff_zone_w,
            'coach_clean_zone_w':coach_clean_zone_w,
            'coach_main_zone_w':coach_main_zone_w,
            'bed_zone_w':bed_zone_w,
            'other_zone_w'              :other_zone_w,

            'zone_list_m'               :zone_list_m,
            'cleanliness_zone_m'        :cleanliness_zone_m,
            'water_zone_m'              :water_zone_m,
            'electrical_zone_m'         :electrical_zone_m,
            'catering_zone_m'           :catering_zone_m,
            'security_zone_m'           :security_zone_m,
            'r_ticketing_zone_m'        :r_ticketing_zone_m,
            'u_ticketing_zone_m'        :u_ticketing_zone_m,
            'refund_ticket_zone_m'      :refund_ticket_zone_m,
            'pssngr_amenities_zone_m'   :pssngr_amenities_zone_m,
            'luggage_zone_m'            :luggage_zone_m,
            'goods_zone_m'              :goods_zone_m,
            'punctuality_zone_m'        :punctuality_zone_m,
            'medical_zone_m':medical_zone_m,
            'divyangjan_zone_m':divyangjan_zone_m,
            'woman_zone_m':woman_zone_m,
            'corruption_zone_m':corruption_zone_m,
            'staff_zone_m':staff_zone_m,
            'coach_clean_zone_m':coach_clean_zone_m,
            'coach_main_zone_m':coach_main_zone_m,
            'bed_zone_m':bed_zone_m,
            'other_zone_m'              :other_zone_m,

            'train_list_y':train_list_y,
            'train_names_y':train_names_y,
            'cleanliness_train_y':cleanliness_train_y,
            'water_train_y':water_train_y,
            'electrical_train_y':electrical_train_y,
            'catering_train_y':catering_train_y,
            'security_train_y':security_train_y,
            'r_ticketing_train_y':r_ticketing_train_y,
            'u_ticketing_train_y':u_ticketing_train_y,
            'refund_ticket_train_y':refund_ticket_train_y,
            'pssngr_amenities_train_y':pssngr_amenities_train_y,
            'luggage_train_y':luggage_train_y,
            'goods_train_y':goods_train_y,
            'punctuality_train_y':punctuality_train_y,
            'medical_train_y':medical_train_y,
            'divyangjan_train_y':divyangjan_train_y,
            'woman_train_y':woman_train_y,
            'corruption_train_y':corruption_train_y,
            'staff_train_y':staff_train_y,
            'coach_clean_train_y':coach_clean_train_y,
            'coach_main_train_y':coach_main_train_y,
            'bed_train_y':bed_train_y,
            'other_train_y':other_train_y,

            'train_list_w'               :train_list_w,
            'train_names_w'              :train_names_w,
            'cleanliness_train_w'        :cleanliness_train_w,
            'water_train_w'              :water_train_w,
            'electrical_train_w'         :electrical_train_w,
            'catering_train_w'           :catering_train_w,
            'security_train_w'           :security_train_w,
            'r_ticketing_train_w'        :r_ticketing_train_w,
            'u_ticketing_train_w'        :u_ticketing_train_w,
            'refund_ticket_train_w'      :refund_ticket_train_w,
            'pssngr_amenities_train_w'   :pssngr_amenities_train_w,
            'luggage_train_w'            :luggage_train_w,
            'goods_train_w'              :goods_train_w,
            'punctuality_train_w'        :punctuality_train_w,
            'medical_train_w':medical_train_w,
            'divyangjan_train_w':divyangjan_train_w,
            'woman_train_w':woman_train_w,
            'corruption_train_w':corruption_train_w,
            'staff_train_w':staff_train_w,
            'coach_clean_train_w':coach_clean_train_w,
            'coach_main_train_w':coach_main_train_w,
            'bed_train_w':bed_train_w,
            'other_train_w'              :other_train_w,

            'train_list_m'               :train_list_m,
            'train_names_m'              :train_names_m,
            'cleanliness_train_m'        :cleanliness_train_m,
            'water_train_m'              :water_train_m,
            'electrical_train_m'         :electrical_train_m,
            'catering_train_m'           :catering_train_m,
            'security_train_m'           :security_train_m,
            'r_ticketing_train_m'        :r_ticketing_train_m,
            'u_ticketing_train_m'        :u_ticketing_train_m,
            'refund_ticket_train_m'      :refund_ticket_train_m,
            'pssngr_amenities_train_m'   :pssngr_amenities_train_m,
            'luggage_train_m'            :luggage_train_m,
            'goods_train_m'              :goods_train_m,
            'punctuality_train_m'        :punctuality_train_m,
            'medical_train_m':medical_train_m,
            'divyangjan_train_m':divyangjan_train_m,
            'woman_train_m':woman_train_m,
            'corruption_train_m':corruption_train_m,
            'staff_train_m':staff_train_m,
            'coach_clean_train_m':coach_clean_train_m,
            'coach_main_train_m':coach_main_train_m,
            'bed_train_m':bed_train_m,
            'other_train_m'              :other_train_m,
    
        }
        return render(request,'railmadad.html',context)
    except Exception as e: 
        print(e)
        try:
            error_Table.objects.create(fun_name="do_dashboard",user_id=request.user,err_details=str(e))
        except:
            print("Internal Error!!!")
        return render(request, "homepage_errors.html", {})

def change_period(request):
    if request.method == "GET":
        p = request.GET.get('period')
        complaint=[]
        zones=['CR','EO','EC','ER','IRC','KM','KR','NC','NE','NF','NR','NW','SB','SC','SE','SR','SW','WC','WR']
        zone_names={'CR':'CR','EO':'EOCR','EC':'ECR','ER':'ER','IRC':'IRCTC','KM':'KM','KR':'KR','NC':'NCR','NE':'NER','NF':'NFR','NR':'NR','NW':'NWR','SB':'SECR','SC':'SCR','SE':'SER','SR':'SR','SW':'SWR','WC':'WCR','WR':'WR'}

        # for z in zones:

        #     recv1=sum(l['sint'] for l in list(m9.rail_madad_1.objects.annotate(sint=Cast('recv', FloatField())).filter(znCode=z,period=p).values('sint')))
        #     # # print( recv)
        #     settled=sum(l['sint'] for l in list(m9.rail_madad_1.objects.annotate(sint=Cast('settled', FloatField())).filter(znCode=z,period=p).values('sint')))
        #     # # print( recv)
        #     avg_pend=sum(l['sint'] for l in list(m9.rail_madad_1.objects.annotate(sint=Cast('avgPendencyDiffName', FloatField())).filter(znCode=z,period=p).values('sint')))
        #     # # print( recv)
        #     complaint.append({'zone':zone_names[z],'com_rcvd':recv,'com_closed':settled,'avg_pend':avg_pend})

        zone_cause=[]
        complaints=['Cleanliness','Water Availability','Electrical Equipment','Catering & Vending Services','Security','Reserved Ticketing',
            'Unreserved Ticketing','Refund of Tickets','Passenger Amenities','Luggage / Parcels','Goods','Punctuality']
        for z in zones:
                cause=[]
                cause1=[]
                recv1=sum(l['sint'] for l in list(m9.rail_madad_1.objects.annotate(sint=Cast('recv', FloatField())).filter(znCode=z,period=p).values('sint')))
                settled=sum(l['sint'] for l in list(m9.rail_madad_1.objects.annotate(sint=Cast('settled', FloatField())).filter(znCode=z,period=p).values('sint')))
                avg_pend_m=sum(l['sint'] for l in list(m9.rail_madad_1.objects.annotate(sint=Cast('avgPendencyDiffName', FloatField())).filter(znCode=z,period=p).values('sint')))
                avg_pend_hr=sum(l['sint'] for l in list(m9.rail_madad_1.objects.annotate(sint=Cast('avgPendencyDiff', FloatField())).filter(znCode=z,period=p).values('sint')))

                for c in complaints:
                        recv=sum(l['sint'] for l in list(m9.rail_madad_1.objects.annotate(sint=Cast('recv', FloatField())).filter(znCode=z,pname=c,period=p).values('sint')))
                        # print( recv)
                        cause.append({str(c).split(' ')[0]+"recv":recv})
                        cause1.append(recv)
                recv=sum(l['sint'] for l in list(m9.rail_madad_1.objects.annotate(sint=Cast('recv', FloatField())).filter(znCode=z,period=p).exclude(pname__in=complaints).values('sint')))
                cause1.append(recv)
                avg_pend=avg_pend_hr*60+avg_pend_m
                zone_cause.append({'zone':zone_names[z],'values':cause1,'com_rcvd':recv1,'com_closed':settled,'avg_pend':avg_pend})
    
    context={
            # 'complaint':complaint,
            'zone_cause':zone_cause
        }
    return JsonResponse(context,safe=False)

from django.db.models import Max
 
def irpsm(request):
    # max_updatedate = m1.irpsm_workplan_mstr.objects.aggregate(Max('updatedate'))['updatedate__max']
    max_updatedate = m1.irpsm_workplan_mstr.objects.filter(work_category__contains='Coal').aggregate(Max('receiving_time'))['receiving_time__max']
    # print(max_updatedate)
    coal=list(m1.irpsm_workplan_mstr.objects.filter(work_category__contains='Coal',receiving_time=max_updatedate).values())
    # print(len(coal))
    max_updatedate = m1.irpsm_workplan_mstr.objects.filter(work_category__contains='Port').aggregate(Max('receiving_time'))['receiving_time__max']
    # print(max_updatedate)
    port=list(m1.irpsm_workplan_mstr.objects.filter(work_category__contains='Port',receiving_time=max_updatedate).values())
    # port=list(m1.irpsm_workplan_mstr.objects.filter(work_category__contains='Port').values())
 
    # print(len(port))
    context={
        'coal':coal,
        'port':port,
    }
    return render(request,'irpsm.html',context)

def  vip_reference_zpd_pdf(request):
    vip_zone_div=list(m7.pendency_status_zone_div.objects.values('zoneunitcode','zonecountpend','divcountpend','pendcount12','pendcount6_12','pendcount3_6','pendcount0_3','zonecountall'))
    sp=0
    zh=0
    cp=0
    ru=0
    au=0
    gh=0
    bd=0

    for p in vip_zone_div:
        if p['zonecountpend']:
            sp+= int(p['zonecountpend'])
        if p['divcountpend']:
            zh+= int(p['divcountpend'])
        if p['pendcount12']:
            cp+= int(p['pendcount12'])
        if p['pendcount6_12']:
            ru+= int(p['pendcount6_12'])
        if p['pendcount3_6']:
            au+= int(p['pendcount3_6'])
        if p['pendcount0_3']:
            gh+= int(p['pendcount0_3'])
        if p['zonecountall']:
            bd+= int(p['zonecountall'])
    
    vip_zone_div.append({'zonecountpend':sp,'divcountpend':zh,'pendcount12':cp,'pendcount6_12':ru,'zoneunitcode':'Total','pendcount3_6':au,'pendcount0_3':gh,'zonecountall':bd})

    context={
       'vip_zone_div':vip_zone_div,
    }
    print("parker",vip_zone_div)
    pdf= render_to_pdf('vip_reference_zpd_pdf.html',context)
    return HttpResponse(pdf,content_type='application/pdf')

def vip_reference_bm_pdf(request):
        
    vip_bm=list(m7.pendency_status_BM.objects.order_by('unitcode').values('unitcode','pendcount12','pendcount6_12','pendcount3_6','pendcount0_3','counttotal','pendcountdir','countdraft','pendcountzone'))
    sp=0
    zh=0
    cp=0
    ru=0
    au=0
    gh=0
    bd=0
    fd=0
    for p in vip_bm:
        if p['pendcount12']:
            sp+= int(p['pendcount12'])
        if p['pendcount6_12']:
            zh+= int(p['pendcount6_12'])
        if p['pendcount3_6']:
            cp+= int(p['pendcount3_6'])
        if p['pendcount0_3']:
            ru+= int(p['pendcount0_3'])
        if p['counttotal']:
            au+= int(p['counttotal'])
        if p['pendcountdir']:
            gh+= int(p['pendcountdir'])
        if p['countdraft']:
            bd+= int(p['countdraft'])
        if p['pendcountzone']:
            fd+= int(p['pendcountzone'])
    vip_bm.append({'pendcount12':sp,'pendcount6_12':zh,'pendcount3_6':cp,'pendcount0_3':ru,'unitcode':'Total','counttotal':au,'pendcountdir':gh,'countdraft':bd,'pendcountzone':fd})

    context={
        'vip_bm':vip_bm,
    }
    print("vikash",vip_bm)

    pdf= render_to_pdf('vip_reference_bm_pdf.html',context)
    return HttpResponse(pdf,content_type='application/pdf')

def vip_reference_dir_pdf(request):
  
    vip_dir=list(m7.pendency_status_DIR.objects.order_by('unitcode').values('unitcode','pendcount12','pendcount6_12','pendcount3_6','pendcount0_3','counttotal','pendcountdir','countdraft','pendcountzone'))
    sp=0
    zh=0
    cp=0
    ru=0
    au=0
    gh=0
    bd=0
    fd=0
    for p in vip_dir:
        if p['pendcount12']:
            sp+= int(p['pendcount12'])
        if p['pendcount6_12']:
            zh+= int(p['pendcount6_12'])
        if p['pendcount3_6']:
            cp+= int(p['pendcount3_6'])
        if p['pendcount0_3']:
            ru+= int(p['pendcount0_3'])
        if p['counttotal']:
            au+= int(p['counttotal'])
        if p['pendcountdir']:
            gh+= int(p['pendcountdir'])
        if p['countdraft']:
            bd+= int(p['countdraft'])
        if p['pendcountzone']:
            fd+= int(p['pendcountzone'])
    vip_dir.append({'pendcount12':sp,'pendcount6_12':zh,'pendcount3_6':cp,'pendcount0_3':ru,'unitcode':'Total','counttotal':au,'pendcountdir':gh,'countdraft':bd,'pendcountzone':fd})
    print('kkkkk',vip_dir)
    
        #@vikash_parker
    for i in vip_dir:
        # print('kkkkk',i['countdraft'])
        if i['countdraft'] is None:
            i['countdraft']=0
        print('lllll######',vip_dir)
        context={
            'vip_dir':vip_dir,
        
        }
    pdf= render_to_pdf('vip_reference_dir_pdf.html',context)
    return HttpResponse(pdf,content_type='application/pdf')