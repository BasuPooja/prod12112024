from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from api import models as m1
from datetime import date,datetime,timedelta
from dateutil.relativedelta import relativedelta
import requests
from requests.auth import HTTPBasicAuth
import json
from home_page import models as m7
from myadmin import models
from apscheduler.schedulers.background import BackgroundScheduler
from django.db.models import Max



# RAIL MADAD 
def rail_madad_bottomReports():
    Update_count = 0
    create_count = 0
    # m1.railmadad_cause_graph.objects.filter().delete()
    names=['division','train','zone']
    today=date.today()
    todays = datetime.datetime.strftime(today,"%Y-%m-%d")
    yesterday = today - relativedelta(days = 1)
    yesterday = datetime.datetime.strftime(yesterday,"%Y-%m-%d")
    last_month=today - relativedelta(days = 30)
    last_month = datetime.datetime.strftime(last_month,"%Y-%m-%d")
    last_week=today - relativedelta(days = 7)
    last_week = datetime.datetime.strftime(last_week,"%Y-%m-%d")
    period=[yesterday,last_month,last_week]

    for p in period:
        for n in names:
            count=1
            # print(n,"hello rail madad")
            var_suc = True
            while var_suc and count<=20:
                count+=1
                # print(n,count)
                try:
                    url='https://railmadad.indianrailways.gov.in/rmmis/rmmisapi/reportapi/BottomReport'
                    data={
                            
                            "fromInput":p,
                            "toInput":yesterday,
                            "viewType":n,
                            "limit":"5"
                            }
                
                    auth1=HTTPBasicAuth('externaluser' ,'m@d@dadm1n')
                    headers = {"Content-Type": "application/json; charset=utf-8"}
                    response = requests.request("POST", url,headers=headers,json=data,auth=auth1)
                    l_main=response.json()
                    var_suc = False
                except Exception as e:
                    pass
            
            if var_suc is False:
                data = l_main['arr']
                cause_types=data[0]
                values=data[1:6]
                

                if n=='zone':
                    types=0
                elif n=='division':
                    types=1
                else:
                    types=2

                if p==yesterday:
                    per=1
                elif p==last_month:
                    per=30
                else:
                    per=7
                m1.railmadad_cause_graph.objects.filter(period=per,type=types).delete()
                
                for i in range(1,len(data)):
                    
                    # if types==2:
                    #     n=list(models.train_master.objects.filter(train_no=data[i][0]).values('train_name'))[0]['train_name']
                    #     if len(n)==0:
                    #         name=data[i][0].split('-')[0]
                    #     else:
                    #         name=n+"-"+data[i][0].split('-')[0]
                    # else:
                    #     name=data[i][0].split('-')[0]
                    
                    sums=sum( i for i in data[i][1:len(data[i])])

                    ####STATION#####
                    if 'Cleanliness-S' in cause_types:
                        cleanliness=data[i][cause_types.index('Cleanliness-S')]
                    else:
                        cleanliness=0
                    if 'Water Availability-S' in cause_types:
                        water=data[i][cause_types.index('Water Availability-S')]
                    else:
                        water=0
                    if 'Electrical Equipment-S' in cause_types:
                        electrical=data[i][cause_types.index('Electrical Equipment-S')]
                    else:
                        electrical=0
                    if 'Catering & Vending Services-S' in cause_types:
                        catering=data[i][cause_types.index('Catering & Vending Services-S')]
                    else:
                        catering=0
                    if 'Security-S' in cause_types:
                        security=data[i][cause_types.index('Security-S')]
                    else:
                        security=0
                    if 'Reserved Ticketing-S' in cause_types:
                        r_ticketing=data[i][cause_types.index('Reserved Ticketing-S')]
                    else:
                        r_ticketing=0
                    if 'Unreserved Ticketing-S' in cause_types:
                        u_ticketing=data[i][cause_types.index('Unreserved Ticketing-S')]
                    else:
                        u_ticketing=0
                    if 'Refund of Tickets-S' in cause_types:
                        refund_ticket=data[i][cause_types.index('Refund of Tickets-S')]
                    else:
                        refund_ticket=0
                    if 'Passenger Amenities-S' in cause_types:
                        pssngr_amenities=data[i][cause_types.index('Passenger Amenities-S')]
                    else:
                        pssngr_amenities=0
                    if 'Luggage / Parcels -S' in cause_types:
                        luggage=data[i][cause_types.index('Luggage / Parcels -S')]
                    else:
                        luggage=0
                    if 'Goods-S' in cause_types:
                        goods=data[i][cause_types.index('Goods-S')]
                    else:
                        goods=0
                    if 'Punctuality-S' in cause_types:
                        punctuality=data[i][cause_types.index('Punctuality-S')]
                    else:
                        punctuality=0
                    if 'Medical Assistance-S' in cause_types:
                        medical=data[i][cause_types.index('Medical Assistance-S')]
                    else:
                        medical=0
                    if 'Divyangjan Facilities-S' in cause_types:
                        divyangjan=data[i][cause_types.index('Divyangjan Facilities-S')]
                    else:
                        divyangjan=0
                    if 'Facilities for Women with Special needs-S' in cause_types:
                        woman=data[i][cause_types.index('Facilities for Women with Special needs-S')]
                    else:
                        woman=0
                    if 'Corruption / Bribery-S' in cause_types:
                        corruption=data[i][cause_types.index('Corruption / Bribery-S')]
                    else:
                        corruption=0
                    if 'Staff Behaviour-S' in cause_types:
                        staff=data[i][cause_types.index('Staff Behaviour-S')]
                    else:
                        staff=0
                    if 'Coach - Cleanliness-S' in cause_types:
                        coach_clean=data[i][cause_types.index('Coach - Cleanliness-S')]
                    else:
                        coach_clean=0
                    if 'Coach - Maintenance-S' in cause_types:
                        coach_main=data[i][cause_types.index('Coach - Maintenance-S')]
                    else:
                        coach_main=0
                    if 'Bed Roll-S' in cause_types:
                        bed=data[i][cause_types.index('Bed Roll-S')]
                    else:
                        bed=0 
                    ####TRAIN########
                    if 'Cleanliness-T' in cause_types:
                        cleanliness+=data[i][cause_types.index('Cleanliness-T')]
                    else:
                        cleanliness+=0
                    if 'Water Availability-T' in cause_types:
                        water+=data[i][cause_types.index('Water Availability-T')]
                    else:
                        water+=0
                    if 'Electrical Equipment-T' in cause_types:
                        electrical+=data[i][cause_types.index('Electrical Equipment-T')]
                    else:
                        electrical+=0
                    if 'Catering & Vending Services-T' in cause_types:
                        catering+=data[i][cause_types.index('Catering & Vending Services-T')]
                    else:
                        catering+=0
                    if 'Security-T' in cause_types:
                        security+=data[i][cause_types.index('Security-T')]
                    else:
                        security+=0
                    if 'Reserved Ticketing-T' in cause_types:
                        r_ticketing+=data[i][cause_types.index('Reserved Ticketing-T')]
                    else:
                        r_ticketing+=0
                    if 'Unreserved Ticketing-T' in cause_types:
                        u_ticketing+=data[i][cause_types.index('Unreserved Ticketing-T')]
                    else:
                        u_ticketing+=0
                    if 'Refund of Tickets-T' in cause_types:
                        refund_ticket+=data[i][cause_types.index('Refund of Tickets-T')]
                    else:
                        refund_ticket+=0
                    if 'Passenger Amenities-T' in cause_types:
                        pssngr_amenities+=data[i][cause_types.index('Passenger Amenities-T')]
                    else:
                        pssngr_amenities+=0
                    if 'Luggage / Parcels -T' in cause_types:
                        luggage+=data[i][cause_types.index('Luggage / Parcels -T')]
                    else:
                        luggage+=0
                    if 'Goods-T' in cause_types:
                        goods+=data[i][cause_types.index('Goods-T')]
                    else:
                        goods+=0
                    if 'Punctuality-T' in cause_types:
                        punctuality+=data[i][cause_types.index('Punctuality-T')]
                    else:
                        punctuality+=0
                    if 'Medical Assistance-T' in cause_types:
                        medical+=data[i][cause_types.index('Medical Assistance-T')]
                    else:
                        medical+=0
                    if 'Divyangjan Facilities-T' in cause_types:
                        divyangjan+=data[i][cause_types.index('Divyangjan Facilities-T')]
                    else:
                        divyangjan+=0
                    if 'Facilities for Women with Special needs-T' in cause_types:
                        woman+=data[i][cause_types.index('Facilities for Women with Special needs-T')]
                    else:
                        woman+=0
                    if 'Corruption / Bribery-T' in cause_types:
                        corruption+=data[i][cause_types.index('Corruption / Bribery-T')]
                    else:
                        corruption+=0
                    if 'Staff Behaviour-T' in cause_types:
                        staff+=data[i][cause_types.index('Staff Behaviour-T')]
                    else:
                        staff+=0
                    if 'Coach - Cleanliness-T' in cause_types:
                        coach_clean+=data[i][cause_types.index('Coach - Cleanliness-T')]
                    else:
                        coach_clean+=0
                    if 'Coach - Maintenance-T' in cause_types:
                        coach_main+=data[i][cause_types.index('Coach - Maintenance-T')]
                    else:
                        coach_main+=0
                    if 'Bed Roll-T' in cause_types:
                        bed+=data[i][cause_types.index('Bed Roll-T')]
                    else:
                        bed+=0 
                    
                    ########### SAVE
                    other=sums-(
                        cleanliness+water+electrical+catering+security+
                        r_ticketing+u_ticketing+refund_ticket+pssngr_amenities+
                        luggage+goods+punctuality+medical+divyangjan+woman+
                        corruption+staff+coach_clean+coach_main+bed)
                    # print(p)
                    m1.railmadad_cause_graph.objects.create(
                        name=data[i][0].split('-')[0],
                        cleanliness=cleanliness,
                        water=water,
                        electrical=electrical,
                        catering=catering,
                        security=security,
                        r_ticketing=r_ticketing,
                        u_ticketing=u_ticketing,
                        refund_ticket=refund_ticket,
                        pssngr_amenities=pssngr_amenities,
                        luggage=luggage,
                        goods=goods,
                        punctuality=punctuality,

                        medical=medical,
                        divyangjan=divyangjan,
                        woman=woman,
                        corruption=corruption,
                        staff=staff,
                        coach_clean=coach_clean,
                        coach_main=coach_main,
                        bed=bed,

                        other=other,
                        type=types,
                        period=per,
                        todate=yesterday,
                        fromdate=p,
                    )
                    create_count+=1


                # for i in range(1,len(data)):
                #     # print(data[i])
                #     sums=sum( i for i in data[i][1:len(data[i])])
                #     if n=='zone':
                #         types=0
                #     elif n=='division':
                #         types=1
                #     else:
                #         types=2
                    
                #     if p==yesterday:
                #         per=1
                #     elif p==last_month:
                #         per=30
                #     else:
                #         per=7

                #     m1.railmadad_bottom_reports.objects.create(
                #         name=data[i][0].split('-')[0],
                #         total=sums,
                #         type=types,
                #         period=per,
                #     )
                #     create_count += 1
        
    m1.LogApi.objects.create(schedular_name = "rail_madad_bottomReports",dates = date.today(),times = datetime.datetime.now().time(),Total_count=create_count+Update_count,Total_update = Update_count,Total_Create = create_count)
    print("-----------------------------------------out of api rail_madad_bottomReports---------------------------------", data)
    return data

scheduler = BackgroundScheduler()
scheduler.start()
ob = scheduler.add_job(rail_madad_bottomReports, 'cron', year='*', month='*', day='*', hour=21, minute=20, second=0)
# ob = scheduler.add_job(rail_madad_bottomReports, 'cron', year='*', month='*', day='*', hour=14, minute=30, second=0)
#ob = scheduler.add_job(rail_madad_bottomReports, 'cron', year='*', month='*', day='*', hour=13, minute=24, second=50)

def rail_madad_complaint():
    Update_count = 0
    create_count = 0
    # m1.rail_madad_1.objects.filter().delete()
    today=date.today()
    todays = datetime.datetime.strftime(today,"%Y-%m-%d")
    yesterday = today - relativedelta(days = 1)
    yesterday = datetime.datetime.strftime(yesterday,"%Y-%m-%d")
    last_month=today - relativedelta(days = 30)
    last_month = datetime.datetime.strftime(last_month,"%Y-%m-%d")
    last_week=today - relativedelta(days = 7)
    last_week = datetime.datetime.strftime(last_week,"%Y-%m-%d")
    period=[yesterday,last_month,last_week]
    zones=['CR','EO','EC','ER','IRC','KM','KR','NC','NE','NF','NR','NW','SB','SC','SE','SR','SW','WC','WR']
    count=1
    for p in period:
        for z in zones:
            count=1
            var_suc = True
            while var_suc and count<=20:
                count+=1
                #print(p,z,count)
                try:
                    url='https://railmadad.indianrailways.gov.in/rmmis/rmmisapi/reportapi/Report1FetchData'
                    data={
                            
                            "fromInput":p,
                            "toInput":yesterday,
                            "viewType":"",
                            "flag":"N",
                            "flag1":"N",
                            "complaintZoneInput":z
                            }
                
                    auth1=HTTPBasicAuth('externaluser' ,'m@d@dadm1n')
                    headers = {"Content-Type": "application/json; charset=utf-8"}
                    response = requests.request("POST", url,headers=headers,json=data,auth=auth1)
                    l_main=response.json()
                    #print('',l_main)
                    var_suc = False
                except Exception as e:
                    print(e)
                    pass
            
            if var_suc is False :
                data = l_main
                
                # print(data)
                if len(data)>0 and len(data['report1ResponseModel'])>0:
                    data=data['report1ResponseModel']
                    if p==yesterday:
                        per=1
                    elif p==last_month:
                        per=30
                    else:
                        per=7
                    
                    m1.rail_madad_1.objects.filter(period=per,znCode=data[0]['znCode']).delete()
                    # print(data)
                    for i in range(len(data)-1):
                        if data[i]['avgPendencyDiffName'] == '-':
                            data[i]['avgPendencyDiffName']='0:0'
                        # print(data[i])
                        # print("hello",data[i]['pid'])
                        try:
                            m1.rail_madad_1.objects.create(
                                # avgDiff= data[i]['avgDiff'],
                                # avgDiffName= data[i]['avgDiffName'],
                                # avgFrtDiffName=data[i]['avgFrtDiffName'] ,
                                avgPendencyDiff= data[i]['avgPendencyDiffName'].split(":")[0],
                                avgPendencyDiffName= data[i]['avgPendencyDiffName'].split(":")[1],
                                # avgRating= data[i]['avgRating'],
                                # cb= data[i]['cb'],
                                # compmode= data[i]['compmode'],
                                # deptCode= data[i]['deptCode'],
                                # deptName= data[i]['deptName'],
                                # divCode= data[i]['divCode'],
                                # divName= data[i]['divName'],
                                # mainClosure= data[i]['mainClosure'],
                                # ob= data[i]['ob'],
                                # org= data[i]['org'],
                                # pendencyDiffCount= data[i]['pendencyDiffCount'],
                                # perDisposal= data[i]['perDisposal'],
                                # perShare= data[i]['perShare'],
                                # pid= data[i]['pid'],
                                pname= data[i]['pname'],
                                # ratingName= data[i]['ratingName'],
                                recv= data[i]['recv'],
                                settled= data[i]['settled'],
                                # sname= data[i]['sname'],
                                znCode= z,
                                znName= data[i]['znName'],
                                period=per,
                            )
                            create_count+=1
                        except Exception as e:
                            try:
                                m1.error_log.objects.create(pid=data[i]['pid'],err_details=str(e),fun_name='Report1FetchData')
                            except:
                                    pass

    m1.LogApi.objects.create(schedular_name = "rail_madad_complaint",dates = date.today(),times = datetime.datetime.now().time(),Total_count=create_count+Update_count,Total_update = Update_count,Total_Create = create_count)
    #print("----------------------------------out of api rail_madad_complaint--------------------------------")
    return data



scheduler = BackgroundScheduler()
scheduler.start()
# ob = scheduler.add_job(rail_madad_complaint, 'cron', year='*', month='*', day='*', hour=8, minute=00, second=0)
ob = scheduler.add_job(rail_madad_complaint, 'cron', year='*', month='*', day='*', hour=21, minute=10, second=0)

# Punctuality
def devinsapi_punctuality_cause():
    curdate = date.today()
    prevdate = curdate-relativedelta(months=24)
    mnth = curdate.month
    
    # print(mnth)
    curdate = datetime.datetime.strftime(curdate,'%d-%b-%Y')
    prevdate = datetime.datetime.strftime(prevdate,'%d-%b-%Y')

    url='https://icms.indianrail.gov.in/reports/Report?reportType=RailwayWisePunctualityCauseService'
    data = {"userName": "RailwayWisePunctualityCauses",
            "password":"icmsReport@20221",
            "fromDate":prevdate,
            "toDate":curdate,
            "gauge":"BG",
            "trainTypeGroup":"M",
            "reportLevel":"ZN"}
    headers = {"Content-Type": "application/json; charset=utf-8"}
    response = requests.request("POST", url,headers=headers,json=data)

    l_main=response.json() 
    data = l_main['records']
    if l_main['successFlag']:
        # m1.Cause_Service_Output.objects.filter().delete()
        m1.Cause_Service_Output.objects.filter().update(del_flag=1)
    Update_count = 0
    create_count = 0
    # from datetime import datetime 
    for i in range(len(data)):
        # print(mylist1['records'][i]['scheduleDate'])
        try:
            dates = data[i]['scheduleDate']
            dates = datetime.datetime.strptime(dates,'%d-%b-%Y')
            if m1.Cause_Service_Output.objects.filter(del_flag=0,Scheduled_Date=dates,Zone_Code=data[i]['zoneCode'],cause_code=data[i]['causeCode'],train_group=data[i]['trainTypeGroup']).exists():
                m1.Cause_Service_Output.objects.update(department_code=data[i]['departmentCode'],duration=data[i]['duration'])
                Update_count+=1
            else:
                create_count+=1
                m1.Cause_Service_Output.objects.create(Scheduled_Date=dates,Zone_Code=data[i]['zoneCode'],cause_code=data[i]['causeCode'],department_code=data[i]['departmentCode'],duration=data[i]['duration'],train_group=data[i]['trainTypeGroup'])
        except Exception as e:
                    print(e)
                    pass
    m1.Cause_Service_Output.objects.filter(del_flag=1).delete()
    m1.LogApi.objects.create(schedular_name = "devinsapi_punctuality_cause",dates = date.today(),times = datetime.datetime.now().time(),Total_count=create_count+Update_count,Total_update = Update_count,Total_Create = create_count)
    #print('------------- out of api devinsapi_punctuality_cause--------------------')
    return data

scheduler = BackgroundScheduler()
scheduler.start()
# ob = scheduler.add_job(devinsapi_punctuality_cause, 'cron', year='*', month='*', day='*', hour=8, minute=00, second=0)
ob = scheduler.add_job(devinsapi_punctuality_cause, 'cron', year='*', month='*', day='*', hour=23, minute=00, second=0)

def devinsapi_punctuality_service():
    # m1.Punctuality_Service_Output.objects.filter().delete()
    curdate = date.today()
    prevdate = curdate-relativedelta(months=24)
    mnth = curdate.month
    # print(mnth)
    curdate = datetime.datetime.strftime(curdate,'%d-%b-%Y')
    prevdate = datetime.datetime.strftime(prevdate,'%d-%b-%Y')

    #print(curdate)
    url='https://icms.indianrail.gov.in/reports/Report?reportType=RailwayWisePunctualityService'
    data = {"userName": "RailwayWisePunctualityService",
                "password":"icmsReport@20221",
                "fromDate":prevdate,
                "toDate":curdate,
                "gauge":"BG",
                "trainTypeGroup":"M",
                "reportLevel":"ZN"}
    headers = {"Content-Type": "application/json; charset=utf-8"}
    response = requests.request("POST", url,headers=headers,json=data)
    l_main=response.json() 
    data = l_main['records']
    # if data:
    #   m1.Punctuality_Service_Output.objects.filter().delete()
    Update_count = 0
    create_count = 0
    # from datetime import datetime 
    for i in range(len(data)):
        # print(mylist1['records'][i]['scheduleDate'])
        try:
            dates = data[i]['scheduleDate']
            dates = datetime.datetime.strptime(dates,'%d-%b-%Y')
            if m1.Punctuality_Service_Output.objects.filter(Scheduled_Date=dates,Zone_Code=data[i]['zoneCode'],train_group=data[i]['trainTypeGroup']).exists():
                m1.Punctuality_Service_Output.objects.filter(Scheduled_Date=dates,Zone_Code=data[i]['zoneCode'],train_group=data[i]['trainTypeGroup']).update(train_count=data[i]['trainCount'],nlt_count=data[i]['nltCount'])
                Update_count+=1
            else:
                create_count+=1
                m1.Punctuality_Service_Output.objects.create(Scheduled_Date=dates,Zone_Code=data[i]['zoneCode'],train_count=data[i]['trainCount'],nlt_count=data[i]['nltCount'],train_group=data[i]['trainTypeGroup'])
        except Exception as e:
                    print(e)
                    pass
    # print("count",len(data))
    m1.LogApi.objects.create(schedular_name = "devinsapi_punctuality_service",dates = date.today(),times = datetime.datetime.now().time(),Total_count=create_count+Update_count,Total_update = Update_count,Total_Create = create_count)
    return data


scheduler = BackgroundScheduler()
scheduler.start()
# ob = scheduler.add_job(devinsapi_punctuality_service, 'cron', year='*', month='*', day='*', hour=8, minute=0, second=0)
ob = scheduler.add_job(devinsapi_punctuality_service, 'cron', year='*', month='*', day='*', hour=23, minute=0, second=0)



#E-DRISHTI (Asset Reliabilty)

def devinsapi_punctuality_mrafdashboard():
    # print("inside")
    # m1.Asset_Reliability.objects.filter().delete()
    m1.Asset_Reliability.objects.filter().update(del_flag=1)
    curdate = date.today()
    curdate=curdate-relativedelta(days=1)
    mnth = curdate.month
    # print(mnth)
    curdate = datetime.datetime.strftime(curdate,'%d-%b-%Y')
    curyear = date.today().year
    if mnth <= 3:
        curyear = curyear-1
    # print("Hello",curyear)
    # print(curdate)
    import json
    url='https://icms.indianrail.gov.in/reports/Report?reportType=MRAfDashboard'
    data = {"fromDate":"1-Apr-"+str(curyear),
            "toDate":curdate}
    headers = {"Content-Type": "application/json; charset=utf-8"}
    # print(data,"----------",headers)
    response = requests.request("POST", url,headers=headers,json=data)
    # res = response.raw
    # data = res.read()
    # print('hhhh',data)
    # print('hhhh',response)
    import json
    l_main=response.json() 
    data = l_main['vRecordList']
    Update_count = 0
    create_count = 0
    for i in range(len(data)):
        try:
            m1.Asset_Reliability.objects.create(Zone=data[i]['zone'],classification=data[i]['classification'],failure_code=data[i]['failureCode'],failure_subcode=data[i]['failureSubCode'],duration=data[i]['duration'],division=data[i]['division'],AF=data[i]['AF'],TD=data[i]['TD'],yearType=data[i]['yearType'],average_minutes=data[i]['averageMinutes'])
            create_count+=1
        except:
            pass
    if create_count:
        m1.Asset_Reliability.objects.filter(del_flag=1).delete()
    m1.LogApi.objects.create(schedular_name = "devinsapi_punctuality_mrafdashboard",dates = date.today(),times = datetime.datetime.now().time(),Total_count=create_count+Update_count,Total_update = Update_count,Total_Create = create_count)

    return data


scheduler = BackgroundScheduler()
scheduler.start()
ob = scheduler.add_job(devinsapi_punctuality_mrafdashboard, 'cron', year='*', month='*', day='*', hour=23, minute=00, second=0)


def devinsapi_punctuality_mrafdashboard_monthly():
    # m1.Asset_Reliability_month.objects.filter().delete()
    m1.Asset_Reliability_month.objects.filter().update(del_flag=1)
    curdate = date.today()
    curdate = curdate - relativedelta(days=1)
    prevdate = datetime.datetime.strftime(curdate,'%b-%Y')
    curdate = datetime.datetime.strftime(curdate,'%d-%b-%Y')
    # print(curdate,prevdate)
    url='https://icms.indianrail.gov.in/reports/Report?reportType=MRAfDashboard'
    data = {"fromDate":"1-"+prevdate,
            "toDate":curdate}
    headers = {"Content-Type": "application/json; charset=utf-8"}
    response = requests.request("POST", url,headers=headers,json=data)
    l_main=response.json()
    data = l_main['vRecordList']
    Update_count = 0
    create_count = 0
    # print(data)
    # print('hhhh',len(data))
    # print("Heyyy",data)
    for i in range(len(data)):
        try:
            m1.Asset_Reliability_month.objects.create(Zone=data[i]['zone'],classification=data[i]['classification'],failure_code=data[i]['failureCode'],failure_subcode=data[i]['failureSubCode'],duration=data[i]['duration'],division=data[i]['division'],AF=data[i]['AF'],TD=data[i]['TD'],yearType=data[i]['yearType'],average_minutes=data[i]['averageMinutes'])
            create_count += 1
        except:
            pass
    if create_count:
        m1.Asset_Reliability_month.objects.filter(del_flag=1).delete()
    m1.LogApi.objects.create(schedular_name = "devinsapi_punctuality_mrafdashboard_monthly",dates = date.today(),times = datetime.datetime.now().time(),Total_count=create_count+Update_count,Total_update = Update_count,Total_Create = create_count)
    # print("Heyyy")
    return data

scheduler = BackgroundScheduler()
scheduler.start()
ob = scheduler.add_job(devinsapi_punctuality_mrafdashboard_monthly, 'cron', year='*', month='*', day='*', hour=23, minute=0, second=0)

#E-DRISHTI (Others)

def accident_data():
    
    date11 = m1.LogApi.objects.filter(schedular_name='accident_data').values('dates').order_by('-dates')[0]['dates']
    startdate=date11
    presentdate = datetime.datetime.now().date()
    
    Update_count = 0
    create_count = 0
    data=[]
    while startdate < presentdate:
        ### api code
        try:
            startdate = startdate + timedelta(days = 1)
            acci = datetime.datetime.strftime(startdate,"%d/%m/%Y")
            url="http://10.64.1.211:7003/simsws/rest/SIMS_eDristi/accidentfedristi"
            data1 = {"userId":"EDRISTISIMS2","password":"EDRISTI@SIMS2021","acciDate":str(acci)}
            # data1 = {"userId":"EDRISTISIMS2","password":"EDRISTI@SIMS2021","acciDate":"22/12/2022"}
            headers = {"Content-Type": "application/json; charset=utf-8"}
            response = requests.request("POST", url,headers=headers,json=data1)
            # print(response.raise_for_status())
            data=response.json() 
            
            if data:
                for i in range(len(data)):
                    create_count += 1
                    m1.safety.objects.create(reportDate=data[i]['reportDate'],accidentDate=data[i]['accidentDate'],accidentTime=datetime.datetime.strptime(data[i]['accidentTime'],"%d-%m-%Y %H:%M"),accidentId=data[i]['accidentId'],rlyCode = data[i]['rlyCode'],rlyName = data[i]['rlyName'],divCode = data[i]['divCode'],divName = data[i]['divName'],section = data[i]['section'],consequentialFlag = data[i]['consequentialFlag'],accidentCategory = data[i]['accidentCategory'],accidentType = data[i]['accidentType'],location = data[i]['location'],trainType = data[i]['trainType'],trainNo = data[i]['trainNo'],station = data[i]['station'],totalCasualities = data[i]['totalCasualities'],respDept = data[i]['respDept'])
        except:
            pass
     
    m1.LogApi.objects.create(schedular_name = "accident_data",dates = date.today(),times = datetime.datetime.now().time(),Total_count=create_count+Update_count,Total_update = Update_count,Total_Create = create_count)
    return data

scheduler = BackgroundScheduler()
scheduler.start()
ob = scheduler.add_job(accident_data, 'cron', year='*', month='*', day='*', hour=21, minute=55, second=0)


def devinsapi_loading_commodity():
    date1 = date.today()
    date1 = datetime.datetime.strftime(date1,"%d-%m-%Y")
    url='https://www.fois.indianrail.gov.in/foisweb/FOISLdngMU?Qry=CMDT_STATS&Date='+date1
    headers = {"Content-Type": "application/json; charset=utf-8"}
    response = requests.request("GET", url,headers=headers)
    l_main=response.json() 
    if l_main['Stts'] == 'Failed':
        pass
    data = l_main['Data']
    Update_count = 0
    create_count = 0
    # m1.Loading_Commodity.objects.filter().delete()
    m1.Loading_Commodity.objects.filter().update(del_flag=1)
    # print(len(data))
    for i in range(len(data)):
        try:
            if data[i]['PlanHead']=='':
                data[i]['PlanHead']='Total'
            m1.Loading_Commodity.objects.create(PlanHead=data[i]['PlanHead'],Yearly_Target=data[i]['Yearly_Target'],Actual_Upto_Month_LY=data[i]['Actual_Upto_Month_LY'],Actual_Upto_Month_CY=data[i]['Actual_Upto_Month_CY'],Var_Pctg=data[i]['Var_Pctg'],Var_Over_Target=data[i]['Var_Over_Target'])
            create_count += 1
        except:
            pass
    if create_count:
        m1.Loading_Commodity.objects.filter(del_flag=1).delete()
    m1.LogApi.objects.create(schedular_name = "devinsapi_loading_commodity",dates = date.today(),times = datetime.datetime.now().time(),Total_count=create_count+Update_count,Total_update = Update_count,Total_Create = create_count)
    return data

scheduler = BackgroundScheduler()
scheduler.start()
ob = scheduler.add_job(devinsapi_loading_commodity, 'cron', year='*', month='*', day='*', hour=23, minute=0, second=0)

def devinsapi_loading_zonal():
    date1 = date.today()
    date1 = datetime.datetime.strftime(date1,"%d-%m-%Y")
    url='https://www.fois.indianrail.gov.in/foisweb/FOISLdngMU?Qry=ZONAL_STATS&Date='+date1
    headers = {"Content-Type": "application/json; charset=utf-8"}
    response = requests.request("GET", url,headers=headers)
    l_main=response.json()
    if l_main['Stts'] == 'Failed':
        pass
    data = l_main['Data']
    Update_count = 0
    create_count = 0
    # m1.Loading_Zonal.objects.filter().delete()
    m1.Loading_Zonal.objects.filter().update(del_flag=1)
    # print(len(data))
    for i in range(len(data)):
        try:
            if data[i]['Rly']=='':
                data[i]['Rly']='Total'
            m1.Loading_Zonal.objects.create(Rly=data[i]['Rly'],Yearly_Target=data[i]['Yearly_Target'],Actual_Upto_Month_LY=data[i]['Actual_Upto_Month_LY'],Actual_Upto_Month_CY=data[i]['Actual_Upto_Month_CY'],Var_Pctg=data[i]['Var_Pctg'],Var_Over_Target=data[i]['Var_Over_Target'])
            create_count += 1
        except:
            pass

    if create_count:
        m1.Loading_Zonal.objects.filter(del_flag=1).delete()
    m1.LogApi.objects.create(schedular_name = "devinsapi_loading_zonal",dates = date.today(),times = datetime.datetime.now().time(),Total_count=create_count+Update_count,Total_update = Update_count,Total_Create = create_count)
    # print("count",len(data))
    return data

scheduler = BackgroundScheduler()
scheduler.start()
ob = scheduler.add_job(devinsapi_loading_zonal, 'cron', year='*', month='*', day='*', hour=23, minute=0, second=0)

def devinsapi_loading_overall():
    date1 = date.today()
    date1 = datetime.datetime.strftime(date1,"%d-%m-%Y")
    url='https://www.fois.indianrail.gov.in/foisweb/FOISLdngMU?Qry=YEARLY_STATS&Date='+date1
    headers = {"Content-Type": "application/json; charset=utf-8"}
    response = requests.request("GET", url,headers=headers)
    l_main=response.json() 
    if l_main['Stts'] == 'Failed':
        pass
    data = l_main['Data']
    Update_count = 0
    create_count = 0
    # m1.Loading_Overall.objects.filter().delete()
    m1.Loading_Overall.objects.filter().update(del_flag=1)
    # print(len(data))
    for i in range(len(data)):
        try:
            m1.Loading_Overall.objects.create(Loading_Upto_Month_LY=data[i]['Loading_Upto_Month_LY'],NTKM_Upto_Month_LY=data[i]['NTKM_Upto_Month_LY'],Earning_Upto_Month_LY=data[i]['Earning_Upto_Month_LY'],Lead_Upto_Month_LY=data[i]['Lead_Upto_Month_LY'],Yield_NTKM_Upto_Month_LY=data[i]['Yield_NTKM_Upto_Month_LY'],Yield_MT_Upto_Month_LY=data[i]['Yield_MT_Upto_Month_LY'],Loading_Upto_Month_CY=data[i]['Loading_Upto_Month_CY'],NTKM_Upto_Month_CY=data[i]['NTKM_Upto_Month_CY'],Earning_Upto_Month_CY=data[i]['Earning_Upto_Month_CY'],Lead_Upto_Month_CY=data[i]['Lead_Upto_Month_CY'],Yield_NTKM_Upto_Month_CY=data[i]['Yield_NTKM_Upto_Month_CY'],Yield_MT_Upto_Month_CY=data[i]['Yield_MT_Upto_Month_CY'],Loading_LFY=data[i]['Loading_LFY'],NTKM_LFY=data[i]['NTKM_LFY'],Earning_LFY=data[i]['Earning_LFY'],Lead_LFY=data[i]['Lead_LFY'],Yield_NTKM_LFY=data[i]['Yield_NTKM_LFY'],Yield_MT_LFY=data[i]['Yield_MT_LFY'])
            create_count += 1
        except:
            pass
    if create_count:
        m1.Loading_Overall.objects.filter(del_flag=1).delete()
    m1.LogApi.objects.create(schedular_name = "devinsapi_loading_overall",dates = date.today(),times = datetime.datetime.now().time(),Total_count=create_count+Update_count,Total_update = Update_count,Total_Create = create_count)
    return data

scheduler = BackgroundScheduler()
scheduler.start()
ob = scheduler.add_job(devinsapi_loading_overall, 'cron', year='*', month='*', day='*', hour=23, minute=0, second=0)



def earnings_data():
    curyear = date.today().year
    date1 = date.today() - relativedelta(days=30)
    month = datetime.datetime.strftime(date1,"%m")
    curyear = date1.year
    url="https://aims.indianrailways.gov.in/IPASWebService/rest/WebService/getEarningFR"
    data = {
        
        "month":str(curyear)+str(month),
        "userId":"AMEY",
        "userPwd":"AMEY"
        
    }
    headers = {"Content-Type": "application/json; charset=utf-8"}
    response = requests.request("POST", url,headers=headers,json=data)
    l_main=response.json() 
    data = l_main['data']
    Update_count = 0
    create_count = 0
    for i in range(len(data)):
        if m1.earnings.objects.filter(MONTH=data[i]['MONTH'],S_NO=int(data[i]['S_NO'])).exists():
            if data[i]['INCREASE_OVER_PREV']=="":
                data[i]['INCREASE_OVER_PREV'] = "0"
            m1.earnings.objects.filter(MONTH=data[i]['MONTH'],S_NO=int(data[i]['S_NO'])).update(HEAD=data[i]['HEAD'],INCREASE_OVER_PREV=data[i]['INCREASE_OVER_PREV'],VARIATION_BP=data[i]['VARIATION_BP'],PREV_ACTUALS_MONTH=data[i]['PREV_ACTUALS_MONTH'],BUDGET_TARGET=data[i]['BUDGET_TARGET'],BP_CURR_MONTH=data[i]['BP_CURR_MONTH'],ACTUALS_CURR_MONTH=data[i]['ACTUALS_CURR_MONTH'],PREV_YEAR=data[i]['PREV_YEAR'])
            Update_count += 1
        else:
            if data[i]['INCREASE_OVER_PREV']=="":
                data[i]['INCREASE_OVER_PREV'] = "0"
            m1.earnings.objects.create(MONTH=data[i]['MONTH'],S_NO=int(data[i]['S_NO']),HEAD=data[i]['HEAD'],INCREASE_OVER_PREV=data[i]['INCREASE_OVER_PREV'],VARIATION_BP=data[i]['VARIATION_BP'],PREV_ACTUALS_MONTH=data[i]['PREV_ACTUALS_MONTH'],BUDGET_TARGET=data[i]['BUDGET_TARGET'],BP_CURR_MONTH=data[i]['BP_CURR_MONTH'],ACTUALS_CURR_MONTH=data[i]['ACTUALS_CURR_MONTH'],PREV_YEAR=data[i]['PREV_YEAR'])
            create_count += 1
    m1.LogApi.objects.create(schedular_name = "earnings_data",dates = date.today(),times = datetime.datetime.now().time(),Total_count=create_count+Update_count,Total_update = Update_count,Total_Create = create_count)
    return data

scheduler = BackgroundScheduler()
scheduler.start()
ob = scheduler.add_job(earnings_data, 'cron', year='*', month='*', day='*', hour=21, minute=40, second=0)

def capex_data():
    # current_year=datetime.today().strftime("%Y")
    # cm=int(datetime.today().strftime("%m"))
    current_month=datetime.datetime.today()
    # if cm<4:
    #     current_year=current_month-relativedelta(months=12)
    #     current_year=datetime.strftime(current_year,"%Y")
    
    day=int(datetime.datetime.today().strftime("%d"))
    # print(day)
    if day<8:
        prev_month=current_month-relativedelta(days=60)
    else:
        # print("else")
        prev_month=current_month-relativedelta(days=31)

    month=datetime.datetime.strftime(prev_month,"%m")
    current_year=datetime.datetime.strftime(prev_month,"%Y")
    # print(current_year+month)
    # m1.capex.objects.filter().delete()
    url="https://aims.indianrailways.gov.in/IPASWebService/rest/WebService/getACPJFRCAPEX"
    data = {
        "month":current_year+month,
        # "month":"202310",
        "userId":"AMEY",
        "userPwd":"AMEY"
        }
    headers = {"Content-Type": "application/json; charset=utf-8"}
    # headers = {"Content-Type": "application/json; charset=utf-8"}
    # response = requests.request("POST", url,headers=headers,json=data)
    response = requests.request("POST", url,headers=headers,json=data)
    l_main=response.json() 
    data = l_main['data']
    Update_count = 0
    create_count = 0
    for i in range(len(data)):
        try:
            if m1.capex.objects.filter(month=data[i]['MONTH'],serial_no=int(data[i]['SRNO'])).exists():
                m1.capex.objects.filter(month=data[i]['MONTH'],serial_no=int(data[i]['SRNO'])).update(actual_prev_fy=data[i]['ACTUAL_PREV_FY'],bg_curr=data[i]['BG_CURR'],actual_prev_mon=data[i]['ACTUAL_PREV_MON'],planhd=data[i]['PLANHD'],exp_curr=data[i]['EXP_CURR'],perc_fy=data[i]['PERC_FY'],perc_curr=data[i]['PERC_CURR'],bg_mod=data[i]['BG_MOD'])
                Update_count+=1
            else:
                create_count+=1
                m1.capex.objects.create(actual_prev_fy=data[i]['ACTUAL_PREV_FY'],bg_curr=data[i]['BG_CURR'],month=data[i]['MONTH'],actual_prev_mon=data[i]['ACTUAL_PREV_MON'],planhd=data[i]['PLANHD'],serial_no=int(data[i]['SRNO']),exp_curr=data[i]['EXP_CURR'],perc_fy=data[i]['PERC_FY'],perc_curr=data[i]['PERC_CURR'],bg_mod=data[i]['BG_MOD'])
        except:
            pass
        # m1.capex.objects.create(actual_prev_fy=data[i]['ACTUAL_PREV_FY'],bg_curr=data[i]['BG_CURR'],month=data[i]['MONTH'],actual_prev_mon=data[i]['ACTUAL_PREV_MON'],planhd=data[i]['PLANHD'],serial_no=data[i]['SRNO'],exp_curr=data[i]['EXP_CURR'],perc_fy=data[i]['PERC_FY'],perc_curr=data[i]['PERC_CURR'],bg_mod=data[i]['BG_MOD'])
    m1.LogApi.objects.create(schedular_name = "capex_data",dates = date.today(),times = datetime.datetime.now().time(),Total_count=create_count+Update_count,Total_update = Update_count,Total_Create = create_count)
    # print("Done", data)
    return data

scheduler = BackgroundScheduler()
scheduler.start()
ob = scheduler.add_job(capex_data, 'cron', year='*', month='*', day="*", hour=21, minute=25, second=0)




######### parliament ap1 ####################


def devinspapiparlia_parliament_LS_RS():
    m7.parliament_count_LS_RS.objects.filter().delete()
    url='https://morpr.cris.org.in/pat/mu/getPendingCount'
    data={
    'username':'crismuapi',
    'password':'Crismuapi#1234',
    }
    headers = {"Content-Type": "application/json; charset=utf-8"}
    response = requests.request("GET", url,headers=headers,
    auth = HTTPBasicAuth('crismuapi', 'Crismuapi#1234'))
    
    l_main=response.json() 
    data = []
    Update_count = 0
    create_count = 0
    create_count += 1
    for key, value in l_main.items():
        try:
            myname=key
            m7.parliament_count_LS_RS.objects.create(lscount=l_main[key]['lscount'],rscount=l_main[key]['rscount'],total=l_main[key]['total'],name=myname)
        except:
            pass
    m1.LogApi.objects.create(schedular_name = "devinspapiparlia_parliament_LS_RS",dates = date.today(),times = datetime.datetime.now().time(),Total_count=create_count+Update_count,Total_update = Update_count,Total_Create = create_count)
    return data



scheduler = BackgroundScheduler()
scheduler.start()
# ob = scheduler.add_job(devinspapiparlia_parliament_LS_RS, 'cron', year='*', month='*', day='*', hour=8, minute=0, second=0)
ob = scheduler.add_job(devinspapiparlia_parliament_LS_RS, 'cron', year='*', month='*', day='*', hour=20, minute=55, second=0)

def devinspapiparlia_parlia_progress():
    m7.parliament_progress_count.objects.filter().delete()
    date1 = date.today()
    date2 = date1-relativedelta(days=30)
    date1 = datetime.datetime.strftime(date1,"%Y-%m-%d")
    date2 = datetime.datetime.strftime(date2,"%Y-%m-%d")
    # print(date1)
    # requests.get('https://files.explosm.net/comics/Rob/chainsaw.png')
    # url='https://morpr.cris.org.in/pat/mu/getProgressCount?&frmdt=2021-11-06&todt=2021-11-06'
    url='https://morpr.cris.org.in/pat/mu/getProgressCount?&frmdt='+date2+'&todt='+date1
    data={
    'username':'crismuapi',
    'password':'Crismuapi#1234',
    }
    headers = {"Content-Type": "application/json; charset=utf-8"}
    response = requests.request("GET", url,headers=headers,
    auth = HTTPBasicAuth('crismuapi', 'Crismuapi#1234'))
    
    l_main=response.json() 
    data = []
    Update_count = 0
    create_count = 0
    # print('lmain',l_main)
    create_count += 1
    for i in range(len(l_main)):
        try:
            m7.parliament_progress_count.objects.create(newentry=l_main[i]['newentry'],finalised=l_main[i]['finalised'],typee=l_main[i]['type'],total=l_main[i]['total'],opnbal=l_main[i]['opnbal'])
            create_count += 1
        except:
            pass
    m1.LogApi.objects.create(schedular_name = "devinspapiparlia_parlia_progress",dates = date.today(),times = datetime.datetime.now().time(),Total_count=create_count+Update_count,Total_update = Update_count,Total_Create = create_count)
    return data    
 

scheduler = BackgroundScheduler()
scheduler.start()
# ob = scheduler.add_job(devinspapiparlia_parlia_progress, 'cron', year='*', month='*', day='*', hour=8, minute=0, second=40)
ob = scheduler.add_job(devinspapiparlia_parlia_progress, 'cron', year='*', month='*', day='*', hour=20, minute=15, second=0)    

def devinspapiparlia_parlia_bmwise():
    m7.parliament_BMwise_pendency.objects.filter().delete()
    # requests.get('https://files.explosm.net/comics/Rob/chainsaw.png')
    url='https://morpr.cris.org.in/pat/mu/getPendCountBM'
    data={
    'username':'crismuapi',
    'password':'Crismuapi#1234',
    }
    headers = {"Content-Type": "application/json; charset=utf-8"}
    response = requests.request("GET", url,headers=headers,
    auth = HTTPBasicAuth('crismuapi', 'Crismuapi#1234'))
    
    l_main=response.json() 
    data = []
    Update_count = 0
    create_count = 0
    # print('lmain',l_main)
    create_count += 1
    for i in range(len(l_main)):
        try:
            m7.parliament_BMwise_pendency.objects.create(id=l_main[i]['id'],countspecialmention=l_main[i]['countspecialmention'],countzerohour=l_main[i]['countzerohour'],countpetition=l_main[i]['countpetition'],designame=l_main[i]['designame'],countrule377=l_main[i]['countrule377'],countass=l_main[i]['countass'])
            create_count += 1
        except:
            pass
    m1.LogApi.objects.create(schedular_name = "devinspapiparlia_parlia_bmwise",dates = date.today(),times = datetime.datetime.now().time(),Total_count=create_count+Update_count,Total_update = Update_count,Total_Create = create_count)
    return data 
    
scheduler = BackgroundScheduler()
scheduler.start()
# ob = scheduler.add_job(devinspapiparlia_parlia_bmwise, 'cron', year='*', month='*', day='*', hour=8, minute=00, second=40)
ob = scheduler.add_job(devinspapiparlia_parlia_bmwise, 'cron', year='*', month='*', day='*', hour=20, minute=50, second=0)     

def devinspapiparlia_parlia_dirwise():
    m7.parliament_DIRwise_pendency.objects.filter().delete()
    # requests.get('https://files.explosm.net/comics/Rob/chainsaw.png')
    url='https://morpr.cris.org.in/pat/mu/getPendCountDirectorate'
    data={
    'username':'crismuapi',
    'password':'Crismuapi#1234',
    }
    headers = {"Content-Type": "application/json; charset=utf-8"}
    response = requests.request("GET", url,headers=headers,
    auth = HTTPBasicAuth('crismuapi', 'Crismuapi#1234'))
    
    l_main=response.json() 
    data = []
    Update_count = 0
    create_count = 0
    # print('lmain',l_main)
    create_count += 1
    for i in range(len(l_main)):
        try:
            m7.parliament_DIRwise_pendency.objects.create(id=l_main[i]['id'],countspecialmention=l_main[i]['countspecialmention'],countzerohour=l_main[i]['countzerohour'],countpetition=l_main[i]['countpetition'],designame=l_main[i]['designame'],countrule377=l_main[i]['countrule377'],countass=l_main[i]['countass'])
            create_count += 1

        except:
            pass
    m1.LogApi.objects.create(schedular_name = "devinspapiparlia_parlia_dirwise",dates = date.today(),times = datetime.datetime.now().time(),Total_count=create_count+Update_count,Total_update = Update_count,Total_Create = create_count)
    return data 


scheduler = BackgroundScheduler()
scheduler.start()
# ob = scheduler.add_job(devinspapiparlia_parlia_dirwise, 'cron', year='*', month='*', day='*', hour=8, minute=0, second=0)   
ob = scheduler.add_job(devinspapiparlia_parlia_dirwise, 'cron', year='*', month='*', day='*', hour=20, minute=25, second=0) 
   

def devinspapiparlia_parlia_officerwise_DIR():
    m7.parliament_officerwise_pendency_DIR.objects.filter().delete()
    # requests.get('https://files.explosm.net/comics/Rob/chainsaw.png')
    url='https://morpr.cris.org.in/pat/mu/getCountOfficerwise'
    data={
    'username':'crismuapi',
    'password':'Crismuapi#1234',
    }
    headers = {"Content-Type": "application/json; charset=utf-8"}
    response = requests.request("GET", url,headers=headers,
    auth = HTTPBasicAuth('crismuapi', 'Crismuapi#1234'))
    
    l_main=response.json() 
    data = []
    Update_count = 0
    create_count = 0
    # print('lmain',l_main)
    create_count += 1
    
    for i in range(len(l_main)):
        try:
            m7.parliament_officerwise_pendency_DIR.objects.create(id=l_main[i]['id'],specialmentioncount=l_main[i]['specialmentioncount'],countzerohour=l_main[i]['countzerohour'],desigcode=l_main[i]['desigcode'],dircode=l_main[i]['dircode'],bmid=l_main[i]['bmid'],countpetition=l_main[i]['countpetition'],count377=l_main[i]['count377'],countasur=l_main[i]['countasur'])
            create_count += 1
        except:
                pass
    m1.LogApi.objects.create(schedular_name = "devinspapiparlia_parlia_officerwise_DIR",dates = date.today(),times = datetime.datetime.now().time(),Total_count=create_count+Update_count,Total_update = Update_count,Total_Create = create_count)
    return data  

scheduler = BackgroundScheduler()
scheduler.start()
# ob = scheduler.add_job(devinspapiparlia_parlia_officerwise_DIR, 'cron', year='*', month='*', day='*', hour=8, minute=00, second=40)
ob = scheduler.add_job(devinspapiparlia_parlia_officerwise_DIR, 'cron', year='*', month='*', day='*', hour=20, minute=35, second=0)       


def parliament_countOfficerwiseTotal():
    m7.parliament_countOfficerwiseTotal.objects.filter().delete()
    officers=list(m7.parliament_BMwise_pendency.objects.filter().values('id'))
    Update_count = 0
    create_count = 0
    for o in officers:
        # print(o)
        url='https://morpr.cris.org.in/pat/mu/getCountOfficerwiseTotal?bmid='+str(o['id'])
        data={
        'username':'crismuapi',
        'password':'Crismuapi#1234',
        }
        headers = {"Content-Type": "application/json; charset=utf-8"}
        response = requests.request("GET", url,headers=headers,
        auth = HTTPBasicAuth('crismuapi', 'Crismuapi#1234'))
        l_main=response.json() 
        Update_count = 0
        create_count = 0
        data = []
        # print('lmain',l_main)
        create_count += 1
        for i in range(len(l_main)):
            try:
                m7.parliament_countOfficerwiseTotal.objects.create(
                    countspecialmention=l_main[i]['specialmentioncount'],
                    countzerohour=l_main[i]['countzerohour'],
                    countpetition=l_main[i]['countpetition'],
                    designame=l_main[i]['desigcode'],
                    countrule377=l_main[i]['count377'],
                    countass=l_main[i]['countasur'],
                    dircode=l_main[i]['dircode'],
                    bmid=l_main[i]['bmid'],
                    id=l_main[i]['id'])
                create_count += 1
            except:
                pass

    m1.LogApi.objects.create(schedular_name = "parliament_countOfficerwiseTotal",dates = date.today(),times = datetime.datetime.now().time(),Total_count=create_count+Update_count,Total_update = Update_count,Total_Create = create_count)
    return data
scheduler = BackgroundScheduler()
scheduler.start()
# ob = scheduler.add_job(parliament_countOfficerwiseTotal, 'cron', year='*', month='*', day='*', hour=8, minute=00, second=40)
ob = scheduler.add_job(parliament_countOfficerwiseTotal, 'cron', year='*', month='*', day='*', hour=20, minute=20, second=0)



  

####### vip starts #################

def devinsapi1_pendency_status_zone_pu_div():
    m7.pendency_status_zone_pu_div.objects.filter().delete()
    # requests.get('https://files.explosm.net/comics/Rob/chainsaw.png')
    url='https://morpr.cris.org.in/pat/mu/getZoneDivCount'
    data={
    'username':'crismuapi',
    'password':'Crismuapi#1234',
    }
    headers = {"Content-Type": "application/json; charset=utf-8"}
    response = requests.request("GET", url,headers=headers,
    auth = HTTPBasicAuth('crismuapi', 'Crismuapi#1234'))
    
    l_main=response.json() 
    data = []
    Update_count = 0
    create_count = 0
    # print('lmain',l_main)
    create_count += 1
    m7.pendency_status_zone_pu_div.objects.create(total=l_main['total'],zone=l_main['zone'],div=l_main['div'],refrb=l_main['refrb'],deptcnt=l_main['deptcnt'])
    m1.LogApi.objects.create(schedular_name = "devinsapi1_pendency_status_zone_pu_div",dates = date.today(),times = datetime.datetime.now().time(),Total_count=create_count+Update_count,Total_update = Update_count,Total_Create = create_count)
    return data

scheduler = BackgroundScheduler()
scheduler.start()
# ob = scheduler.add_job(devinsapi1_pendency_status_zone_pu_div, 'cron', year='*', month='*', day='*', hour=8, minute=00, second=40)  
ob = scheduler.add_job(devinsapi1_pendency_status_zone_pu_div, 'cron', year='*', month='*', day='*', hour=21, minute=0, second=0)    

    

def devinsapi1_vip_rbwise():
    m7.pendency_status_RB.objects.filter().delete()
    # requests.get('https://files.explosm.net/comics/Rob/chainsaw.png')
    url='https://morpr.cris.org.in/pat/mu/getMarkedToCountDraft'
    data={
    'username':'crismuapi',
    'password':'Crismuapi#1234',
    }
    headers = {"Content-Type": "application/json; charset=utf-8"}
    response = requests.request("GET", url,headers=headers,
    auth = HTTPBasicAuth('crismuapi', 'Crismuapi#1234'))
    
    l_main=response.json() 
    Update_count = 0
    create_count = 0
    data = []
    # print('lmain',l_main)
    create_count += 1
    m7.pendency_status_RB.objects.create(withdir=l_main['withdir'],withzone=l_main['withzone'],total=l_main['total'],draftreply=l_main['draftreply'])
    m1.LogApi.objects.create(schedular_name = "devinsapi1_vip_rbwise",dates = date.today(),times = datetime.datetime.now().time(),Total_count=create_count+Update_count,Total_update = Update_count,Total_Create = create_count)
    return data

scheduler = BackgroundScheduler()
scheduler.start()
# ob = scheduler.add_job(devinsapi1_vip_rbwise, 'cron', year='*', month='*', day='*', hour=8, minute=0, second=40)    
ob = scheduler.add_job(devinsapi1_vip_rbwise, 'cron', year='*', month='*', day='*', hour=20, minute=45, second=0)  
  



def devinsapi1_vip_zonewise():
    m7.pendency_status_zone_div.objects.filter().delete()
    # requests.get('https://files.explosm.net/comics/Rob/chainsaw.png')
    url='https://morpr.cris.org.in/pat/mu/dashzonedata'
    data={
    'username':'crismuapi',
    'password':'Crismuapi#1234',
    }
    headers = {"Content-Type": "application/json; charset=utf-8"}
    response = requests.request("GET", url,headers=headers,
    auth = HTTPBasicAuth('crismuapi', 'Crismuapi#1234'))
    
    l_main=response.json() 
    Update_count = 0
    create_count = 0
    data = []
    create_count += 1
    for i in range(len(l_main)):
        try:
            
            m7.pendency_status_zone_div.objects.create(
            pendcountzone=l_main[i]['pendcountzone'],
            pendcount0_3=l_main[i]['pendcount0_3'],
            zonecountpend=l_main[i]['zonecountpend'],
            pendcount6_12=l_main[i]['pendcount6_12'],
            pendcount3_6=l_main[i]['pendcount3_6'],
            pendcount12=l_main[i]['pendcount12'],
            divcountpend=l_main[i]['divcountpend'],
            zonecountall=l_main[i]['zonecountall'],
            zoneunitcode=l_main[i]['zoneunitcode'])
            create_count += 1
        except:
            pass
    m1.LogApi.objects.create(schedular_name = "devinsapi1_vip_zonewise",dates = date.today(),times = datetime.datetime.now().time(),Total_count=create_count+Update_count,Total_update = Update_count,Total_Create = create_count)
    return data

scheduler = BackgroundScheduler()
scheduler.start()
# ob = scheduler.add_job(devinsapi1_vip_zonewise, 'cron', year='*', month='*', day='*', hour=8, minute=00, second=10)    
ob = scheduler.add_job(devinsapi1_vip_zonewise, 'cron', year='*', month='*', day='*', hour=20, minute=30, second=0)  

def devinsapi1_vip_zone_dropdown():
    m7.pendency_status_zone_div_dropdown.objects.filter().delete()
    zones=m7.pendency_status_zone_div.objects.filter().values('zoneunitcode')
    Update_count = 0
    create_count = 0
    for z in zones:
        url='https://morpr.cris.org.in/pat/mu/dashdivdata?zone='+z['zoneunitcode']
        data={
        'username':'crismuapi',
        'password':'Crismuapi#1234',
        }
        headers = {"Content-Type": "application/json; charset=utf-8"}
        response = requests.request("GET", url,headers=headers,
        auth = HTTPBasicAuth('crismuapi', 'Crismuapi#1234'))
        
        l_main=response.json() 
        Update_count = 0
        create_count = 0
        data = []
        # print('lmain',l_main)
        create_count += 1
        for i in range(len(l_main)):
            try:
                m7.pendency_status_zone_div_dropdown.objects.create(
                zone=z['zoneunitcode'],
                pendcountzone=l_main[i]['pendcountzone'],
                pendcount0_3=l_main[i]['pendcount0_3'],
                zonecountpend=l_main[i]['zonecountpend'],
                pendcount6_12=l_main[i]['pendcount6_12'],
                pendcount3_6=l_main[i]['pendcount3_6'],
                pendcount12=l_main[i]['pendcount12'],
                divcountpend=l_main[i]['divcountpend'],
                zoneunitcode=l_main[i]['zoneunitcode'])
                create_count += 1
            except:
                pass
    m1.LogApi.objects.create(schedular_name = "devinsapi1_vip_zone_dropdown",dates = date.today(),times = datetime.datetime.now().time(),Total_count=create_count+Update_count,Total_update = Update_count,Total_Create = create_count)
   

scheduler = BackgroundScheduler()
scheduler.start()
# ob = scheduler.add_job(devinsapi1_vip_zone_dropdown, 'cron', year='*', month='*', day='*', hour=8, minute=00, second=40)   
ob = scheduler.add_job(devinsapi1_vip_zone_dropdown, 'cron', year='*', month='*', day='*', hour=20, minute=25, second=0)      


def devinsapi1_vip_dirwise():
    m7.pendency_status_DIR.objects.filter().delete()
 
    url='https://morpr.cris.org.in/pat/mu/getDirBmZoneCountDraft?type=DIR'
    data={
    'username':'crismuapi',
    'password':'Crismuapi#1234',
    }
    headers = {"Content-Type": "application/json; charset=utf-8"}
    response = requests.request("GET", url,headers=headers,
    auth = HTTPBasicAuth('crismuapi', 'Crismuapi#1234'))
    
    l_main=response.json() 
    Update_count = 0
    create_count = 0
    data = []
    # print('lmain',l_main)
    create_count += 1
    for i in range(len(l_main)):
        if l_main[i]['id']:
            try:
                m7.pendency_status_DIR.objects.create(pendcountdir=l_main[i]['pendcountdir'],pendcountzone=l_main[i]['pendcountzone'],pendcount0_3=l_main[i]['pendcount0_3'],countdraft=l_main[i]['countdraft'],pendcount6_12=l_main[i]['pendcount6_12'],pendcount3_6=l_main[i]['pendcount3_6'],counttotal=l_main[i]['counttotal'],pendcount12=l_main[i]['pendcount12'],unitcode=l_main[i]['unitcode'],id=l_main[i]['id'])
                create_count += 1
            except:
                pass
    m1.LogApi.objects.create(schedular_name = "devinsapi1_vip_dirwise",dates = date.today(),times = datetime.datetime.now().time(),Total_count=create_count+Update_count,Total_update = Update_count,Total_Create = create_count)
    return data

scheduler = BackgroundScheduler()
scheduler.start()
# ob = scheduler.add_job(devinsapi1_vip_dirwise, 'cron', year='*', month='*', day='*', hour=8, minute=00, second=40)   
ob = scheduler.add_job(devinsapi1_vip_dirwise, 'cron', year='*', month='*', day='*', hour=20, minute=5, second=40)

# def devinsapi1_vip_zone_dropdown():
#     m7.pendency_status_zone_div_dropdown.objects.filter().delete()
#     zones=m7.pendency_status_zone_div.objects.filter().values('zoneunitcode')
#     Update_count = 0
#     create_count = 0
#     for z in zones:

#         url='https://morpr.cris.org.in/pat/mu/dashdivdata?zone='+z['zoneunitcode']
#         data={
#         'username':'crismuapi',
#         'password':'Crismuapi#1234',
#         }
#         headers = {"Content-Type": "application/json; charset=utf-8"}
#         response = requests.request("GET", url,headers=headers,
#         auth = HTTPBasicAuth('crismuapi', 'Crismuapi#1234'))
        
#         l_main=response.json() 
#         Update_count = 0
#         create_count = 0
#         data = []
#         # print('lmain',l_main)
#         create_count += 1
#         for i in range(len(l_main)):
#             try:
#                 m7.pendency_status_zone_div_dropdown.objects.create(
#                 zone=z['zoneunitcode'],
#                 pendcountzone=l_main[i]['pendcountzone'],
#                 pendcount0_3=l_main[i]['pendcount0_3'],
#                 zonecountpend=l_main[i]['zonecountpend'],
#                 pendcount6_12=l_main[i]['pendcount6_12'],
#                 pendcount3_6=l_main[i]['pendcount3_6'],
#                 pendcount12=l_main[i]['pendcount12'],
#                 divcountpend=l_main[i]['divcountpend'],
#                 zoneunitcode=l_main[i]['zoneunitcode'])
#                 create_count += 1
#             except:
#                 pass
#     m1.LogApi.objects.create(schedular_name = "devinsapi1_vip_zone_dropdown",dates = date.today(),times = datetime.datetime.now().time(),Total_count=create_count+Update_count,Total_update = Update_count,Total_Create = create_count)
#     return data

# scheduler = BackgroundScheduler()
# scheduler.start()
# ob = scheduler.add_job(devinsapi1_vip_zone_dropdown, 'cron', year='*', month='*', day='*', hour=10, minute=55, second=40) 
# ob = scheduler.add_job(devinsapi1_vip_zone_dropdown, 'cron', year='*', month='*', day='*', hour=14, minute=55, second=40) 

 
def devinsapi1_vip_bmwise():
    m7.pendency_status_BM.objects.filter().delete()

    url='https://morpr.cris.org.in/pat/mu/getDirBmZoneCountDraft?type=BM'
    data={
    'username':'crismuapi',
    'password':'Crismuapi#1234',
    }
    headers = {"Content-Type": "application/json; charset=utf-8"}
    response = requests.request("GET", url,headers=headers,
    auth = HTTPBasicAuth('crismuapi', 'Crismuapi#1234'))
    
    l_main=response.json() 
    Update_count = 0
    create_count = 0
    data = []
    # print('lmain',l_main)
    create_count += 1
    for i in range(len(l_main)):
        try:
            m7.pendency_status_BM.objects.create(
            pendcountdir=l_main[i]['pendcountdir'],
            pendcountzone=l_main[i]['pendcountzone'],
            pendcount0_3=l_main[i]['pendcount0_3'],
            countdraft=l_main[i]['countdraft'],
            pendcount6_12=l_main[i]['pendcount6_12'],
            pendcount3_6=l_main[i]['pendcount3_6'],
            counttotal=l_main[i]['counttotal'],
            pendcount12=l_main[i]['pendcount12'],
            unitcode=l_main[i]['unitcode'],
            id=l_main[i]['id'])
            create_count += 1
        except:
            pass
    m1.LogApi.objects.create(schedular_name = "devinsapi1_vip_bmwise",dates = date.today(),times = datetime.datetime.now().time(),Total_count=create_count+Update_count,Total_update = Update_count,Total_Create = create_count)
    return data

scheduler = BackgroundScheduler()
scheduler.start()
# ob = scheduler.add_job(devinsapi1_vip_bmwise, 'cron', year='*', month='*', day='*', hour=8, minute=0, second=40)
ob = scheduler.add_job(devinsapi1_vip_bmwise, 'cron', year='*', month='*', day='*', hour=20, minute=40, second=0) 




def all_function():
    accident_data()
    devinsapi_loading_commodity()
    devinsapi_loading_zonal()
    devinsapi_loading_overall()
    earnings_data()
    capex_data()
    devinsapi_punctuality_mrafdashboard()
    devinsapi_punctuality_mrafdashboard_monthly()
    devinsapi_punctuality_service()
    devinsapi_punctuality_cause()
    rail_madad_bottomReports()
    rail_madad_complaint()
    devinspapiparlia_parliament_LS_RS()
    devinspapiparlia_parlia_progress()
    devinspapiparlia_parlia_bmwise()
    devinspapiparlia_parlia_dirwise()
    devinspapiparlia_parlia_officerwise_DIR()
    parliament_countOfficerwiseTotal()
    devinsapi1_pendency_status_zone_pu_div()
    devinsapi1_vip_rbwise()
    devinsapi1_vip_zonewise()
    devinsapi1_vip_zone_dropdown()
    devinsapi1_vip_dirwise()
    devinsapi1_vip_zone_dropdown()
    devinsapi1_vip_bmwise()
   

scheduler = BackgroundScheduler()
scheduler.start()
ob = scheduler.add_job(all_function, 'cron', year='*', month='*', day='*', hour=23, minute=0, second=0)


def wagon_breakup():
    m1.wagon_breakup.objects.filter().delete()
    today=datetime.datetime.today()
    date111=today
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

    wagons ={}
    items=list(models.wagon_master.objects.filter().values('wagon_type').distinct())
    for i in items:
        # print("lst1",str(prev_year)+"-04-01",str(next_year)+"-03-31")
        lst1 = models.wagon_master.objects.filter(manufacture_date__range=[str(prev_year)+"-04-01",str(next_year)+"-03-31"], wagon_type=i['wagon_type']).count()
        month1 = curr_mon
        if month1!=1:
            month1-=1
        if month1 in [1,3,5,7,8,10,12]:
            day='-31'
        elif month1 == 2:
            day='-28'
        else:
            day='-30'
        # print("lst2",str(fin_year)+"-04-01",date111)
        lst2 = models.wagon_master.objects.filter(manufacture_date__range=[str(fin_year)+"-04-01",str(curr_yr)+"-"+str(month1)+day],wagon_type=i['wagon_type']).count()
        # print("lst3",str(prev_year)+"-"+str(month1)+"-01",str(prev_year)+"-"+str(month1)+day)
        if month1>3:
            lst3 = models.wagon_master.objects.filter(manufacture_date__range=[str(prev_year)+"-"+str(month1)+"-01",str(prev_year)+"-"+str(month1)+day],wagon_type=i['wagon_type']).count()
        else:
            lst3 = models.wagon_master.objects.filter(manufacture_date__range=[str(fin_year)+"-"+str(month1)+"-01",str(fin_year)+"-"+str(month1)+day],wagon_type=i['wagon_type']).count()
        # print("lst4",str(fin_year)+"-"+str(month1)+"-01",date111)
        lst4 = models.wagon_master.objects.filter(manufacture_date__range=[str(curr_yr)+"-"+str(month1)+"-01",str(curr_yr)+"-"+str(month1)+day],wagon_type=i['wagon_type']).count()
        m1.wagon_breakup.objects.create(id=i['wagon_type'],cum_prev=lst1,target='NA',monthly_achvd=lst4,cum_achvd=lst2,same_month_of_previous_year=lst3)

scheduler = BackgroundScheduler()
scheduler.start()
ob = scheduler.add_job(wagon_breakup, 'cron', year='*', month='*', day='*', hour=23, minute=0, second=0)
# ob = scheduler.add_job(wagon_breakup, 'cron', year='*', month='*', day='*', hour=8, minute=44, second=0)

def train_schedule_update():

    date1 = date.today()
    # date2 = date1-relativedelta(days=1)
    date2 =list(m1.LogApi.objects.filter(schedular_name='train_schedule_update').values('dates').order_by('dates'))[0]['dates']
    scrapOfDate = date1-relativedelta(days=1)
    old_ids=list(models.iem_tranprofmstr.objects.filter(iadvaldto__lte=scrapOfDate).values_list('iaitranid', flat=True))
    models.iem_tranprofmstr.objects.filter(iaitranid__in=old_ids).delete()
    models.iem_transch.objects.filter(iaitranid__in=old_ids).delete()
    todays = date.today()
    proxy = {
    'http': 'http://172.16.1.61:8080',
    'https': 'https://172.16.1.61:8080'
    }

    while(date2<=todays):
        date2 = date2+relativedelta(days=1)
        date1 = datetime.datetime.strftime(date2,"%d/%m/%Y")
        Update_count = 0
        create_count = 0

        url='https://www.satsweb.indianrail.gov.in/GetChangeinTrainProfile_RestApi?icmssyncdate='+date1
        headers = {"Content-Type": "application/json; charset=utf-8"}
        response = requests.request("GET", url,headers=headers,proxies=proxy)
        l_main=response.json() 
        # print(l_main)
        data = l_main
        new_trains=[]
        existing_trains=[]
        
        for t in data:
            try:
                if t['trainflag']=='E':
                    existing_trains.append({'trainid':t['trainid'],'trainnumber':t['trainnumber'],'oldtrainid':t['oldtrainid']})
                else:
                    new_trains.append({'trainid':t['trainid'],'trainnumber':t['trainnumber']})
            except:
                pass 

        for e in existing_trains:
            try:
                if e['oldtrainid']!=e['trainid']:
                    #CREATING NEW TRAIN  PROFILE
                    url='https://www.satsweb.indianrail.gov.in/GetCurrentProfileByTrainIDPublish_RestApi?Trainid='+e['trainid']
                    headers = {"Content-Type": "application/json; charset=utf-8"}
                    response = requests.request("GET", url,headers=headers,proxies=proxy)
                    l_main=response.json()
                    if l_main!=[]:
                        l_main=l_main[0]
                        iadvaldfrom=datetime.strptime(l_main['validfrom'],"%d-%m-%Y")
                        iadvaldto=datetime.strptime(l_main['validto'],"%d-%m-%Y")
                        create_count+=1
                        max_id=models.iem_tranprofmstr.objects.filter().aggregate(Max('id'))
                        max_id=int(max_id['id__max']) +1
                        models.iem_tranprofmstr.objects.create(
                            id=max_id,
                            iaitranid = l_main['trainid'],
                            iavtranowngrly = l_main['trainowngrly'],
                            iavtrannumb = l_main['trainnumber'],
                            iavtranname = l_main['trainname'],
                            mavtrantype = l_main['traintype'],
                            iavtranstyp = l_main['trainsubtype'],
                            iadvaldfrom =iadvaldfrom,
                            iadvaldto =iadvaldto,
                            iavdaysofsrvc = l_main['daysofsrvc'],
                            iavorgn = l_main['orig'],
                            iavdstn = l_main['dstn'],
                            iaideptime = l_main['dprttime'],
                            iaiarvltime = l_main['arvltime'],
                            iacgaug = l_main['gauge'],
                            iacuknwvldty = l_main['unknownvldty'],
                            iacirctcflag = l_main['irctcflag'],
                            iavsrcstt = l_main['srcstate'],
                            iavdstnstt = l_main['dstnstate'],
                            iairsrvflag = l_main['reserveflag'],
                            iavhdayctgy = l_main['holidaycategory'],
                            iavresncode = l_main['reasoncode'],
                            iacsrctrcn = l_main['sourcetraction'],
                            iacsliptranflag = l_main['sliptrainflag'],
                            iacsliptype = l_main['sliptype'],
                            iainrmlload = l_main['normalload'],
                            iaimaxload = l_main['maxload'],
                            # iaiintlflag =l_main['mansoon'], 
                            iaiftrbokgflag = l_main['ftrbookingflag'],
                            iavmaintrannumb =l_main['maintrainnumber'], 
                            iavsliptrannumb = l_main['sliptrainnumber'],
                            iainewtrannumb = l_main['newtrainnumber'],
                            iavnewtranname = l_main['newtrainname'],
                        )
                    #CREATING NEW TRAIN  SCHEDULE
                    url='https://www.satsweb.indianrail.gov.in/GetScheduleByTrainIDPublish_RestApi?Trainid='+e['trainid']
                    headers = {"Content-Type": "application/json; charset=utf-8"}
                    response = requests.request("GET", url,headers=headers,proxies=proxy)
                    l_main=response.json()
                    if l_main!=[]:
                        l_main=l_main[0]
                        for l in l_main:
                            create_count+=1
                            max_id=models.iem_transch.objects.aggregate(Max('id'))
                            # print(max_id)
                            max_id=int(max_id['id__max']) +1
                            models.iem_transch.objects.create(
                                    id=max_id,
                                    iaitranid = l_main['trainid'],
                                    iavtrannumb = l_main['trainnumber'],
                                    iaisqncnumb = l_main['seqnumber'],
                                    iavzonecode = l_main['zonecode'],
                                    iavdvsncode = l_main['dvsncode'],
                                    iavsttncode = l_main['sttncode'],
                                    iacclsflag = l_main['classflag'],
                                    iaiwttarvl = l_main['wttarvl'],
                                    iaiwttdprt = l_main['wttdprt'],
                                    iachaltflag = l_main['haltflag'],
                                    iaiwttdayofrun = l_main['dayofrun'],
                                    iaipttdprt = l_main['pttdprt'],
                                    # iaipttarvl = l_main[''],
                                    iairuntime = l_main['runtime'],
                                    iaiacctime = l_main['acctime'],
                                    iaidectime = l_main['dectime'],
                                    iaitrfcalwc = l_main['trfcalwc'],
                                    iaienggalwc = l_main['enggalwc'],
                                    iaicstrtime = l_main['constrainttime'],
                                    iavcstrresn = l_main['constraintreason'],
                                    iacxingflag = l_main['crossingflag'],
                                    iavxingtran = l_main['crossingtrain'],
                                    iavxingtime = l_main['crossingtime'],
                                    iaiintrdist = l_main['intrdist'],
                                    iavpltfnumb =l_main['platformnumber'],
                                    iaccrewchng = l_main['crewchng'],
                                    iaclocochng = l_main['locochange'],
                                    iacrvslsttn = l_main['reversal_STATION'],
                                    iavtrcncode = l_main['trtncode'],
                                    iavcrewchngcode = l_main['crewchngcode'],
                                    iacgarbg = l_main['garbg'],
                                    iacwater = l_main['water']
                            )


                    #UPDATING OLD TRAIN PROFILE
                    url='https://www.satsweb.indianrail.gov.in/GetCurrentProfileByTrainIDPublish_RestApi?Trainid='+e['oldtrainid']
                    headers = {"Content-Type": "application/json; charset=utf-8"}
                    response = requests.request("GET", url,headers=headers,proxies=proxy)
                    l_main=response.json()
                    if l_main!=[]:
                        l_main=l_main[0] 
                        Update_count+=1
                        iadvaldfrom=datetime.datetime.strptime(l_main['validfrom'],"%d-%m-%Y")
                        iadvaldto=datetime.datetime.strptime(l_main['validto'],"%d-%m-%Y")
                        models.iem_tranprofmstr.objects.filter(iaitranid=l_main['trainid']).update(
                            iaitranid = l_main['trainid'],
                            iavtranowngrly = l_main['trainowngrly'],
                            iavtrannumb = l_main['trainnumber'],
                            iavtranname = l_main['trainname'],
                            mavtrantype = l_main['traintype'],
                            iavtranstyp = l_main['trainsubtype'],
                            iadvaldfrom =iadvaldfrom,
                            iadvaldto =iadvaldto,
                            iavdaysofsrvc = l_main['daysofsrvc'],
                            iavorgn = l_main['orig'],
                            iavdstn = l_main['dstn'],
                            iaideptime = l_main['dprttime'],
                            iaiarvltime = l_main['arvltime'],
                            iacgaug = l_main['gauge'],
                            iacuknwvldty = l_main['unknownvldty'],
                            iacirctcflag = l_main['irctcflag'],
                            iavsrcstt = l_main['srcstate'],
                            iavdstnstt = l_main['dstnstate'],
                            iairsrvflag = l_main['reserveflag'],
                            iavhdayctgy = l_main['holidaycategory'],
                            iavresncode = l_main['reasoncode'],
                            iacsrctrcn = l_main['sourcetraction'],
                            iacsliptranflag = l_main['sliptrainflag'],
                            iacsliptype = l_main['sliptype'],
                            iainrmlload = l_main['normalload'],
                            iaimaxload = l_main['maxload'],
                            # iaiintlflag =l_main['mansoon'], 
                            iaiftrbokgflag = l_main['ftrbookingflag'],
                            iavmaintrannumb =l_main['maintrainnumber'], 
                            iavsliptrannumb = l_main['sliptrainnumber'],
                            iainewtrannumb = l_main['newtrainnumber'],
                            iavnewtranname = l_main['newtrainname'],
                        )
                    #UPDATING OLD TRAIN SCHEDULE
                    url='https://www.satsweb.indianrail.gov.in/GetScheduleByTrainIDPublish_RestApi?Trainid='+e['oldtrainid']
                    headers = {"Content-Type": "application/json; charset=utf-8"}
                    response = requests.request("GET", url,headers=headers,proxies=proxy)
                    l_main=response.json()
                    if l_main!=[]:
                        l_main=l_main[0] 
                        for l in l_main:
                            Update_count+=1
                            models.iem_transch.objects.filter(iaitranid=l_main['trainid']).update(
                                    iaitranid = l_main['trainid'],
                                    iavtrannumb = l_main['trainnumber'],
                                    iaisqncnumb = l_main['seqnumber'],
                                    iavzonecode = l_main['zonecode'],
                                    iavdvsncode = l_main['dvsncode'],
                                    iavsttncode = l_main['sttncode'],
                                    iacclsflag = l_main['classflag'],
                                    iaiwttarvl = l_main['wttarvl'],
                                    iaiwttdprt = l_main['wttdprt'],
                                    iachaltflag = l_main['haltflag'],
                                    iaiwttdayofrun = l_main['dayofrun'],
                                    iaipttdprt = l_main['pttdprt'],
                                    # iaipttarvl = l_main[''],
                                    iairuntime = l_main['runtime'],
                                    iaiacctime = l_main['acctime'],
                                    iaidectime = l_main['dectime'],
                                    iaitrfcalwc = l_main['trfcalwc'],
                                    iaienggalwc = l_main['enggalwc'],
                                    iaicstrtime = l_main['constrainttime'],
                                    iavcstrresn = l_main['constraintreason'],
                                    iacxingflag = l_main['crossingflag'],
                                    iavxingtran = l_main['crossingtrain'],
                                    iavxingtime = l_main['crossingtime'],
                                    iaiintrdist = l_main['intrdist'],
                                    iavpltfnumb =l_main['platformnumber'],
                                    iaccrewchng = l_main['crewchng'],
                                    iaclocochng = l_main['locochange'],
                                    iacrvslsttn = l_main['reversal_STATION'],
                                    iavtrcncode = l_main['trtncode'],
                                    iavcrewchngcode = l_main['crewchngcode'],
                                    iacgarbg = l_main['garbg'],
                                    iacwater = l_main['water']
                            )

                else:
                #UPDATING OLD TRAIN PROFILE
                    url='https://www.satsweb.indianrail.gov.in/GetCurrentProfileByTrainIDPublish_RestApi?Trainid='+e['trainid']
                    headers = {"Content-Type": "application/json; charset=utf-8"}
                    response = requests.request("GET", url,headers=headers,proxies=proxy)
                    l_main=response.json()
                    if l_main!=[]:
                        l_main=l_main[0]
                        Update_count+=1
                        iadvaldfrom=datetime.datetime.strptime(l_main['validfrom'],"%d-%m-%Y")
                        iadvaldto=datetime.datetime.strptime(l_main['validto'],"%d-%m-%Y")
                        models.iem_tranprofmstr.objects.filter(iaitranid=l_main['trainid']).update(
                            iaitranid = l_main['trainid'],
                            iavtranowngrly = l_main['trainowngrly'],
                            iavtrannumb = l_main['trainnumber'],
                            iavtranname = l_main['trainname'],
                            mavtrantype = l_main['traintype'],
                            iavtranstyp = l_main['trainsubtype'],
                            iadvaldfrom =iadvaldfrom,
                            iadvaldto =iadvaldto,
                            iavdaysofsrvc = l_main['daysofsrvc'],
                            iavorgn = l_main['orig'],
                            iavdstn = l_main['dstn'],
                            iaideptime = l_main['dprttime'],
                            iaiarvltime = l_main['arvltime'],
                            iacgaug = l_main['gauge'],
                            iacuknwvldty = l_main['unknownvldty'],
                            iacirctcflag = l_main['irctcflag'],
                            iavsrcstt = l_main['srcstate'],
                            iavdstnstt = l_main['dstnstate'],
                            iairsrvflag = l_main['reserveflag'],
                            iavhdayctgy = l_main['holidaycategory'],
                            iavresncode = l_main['reasoncode'],
                            iacsrctrcn = l_main['sourcetraction'],
                            iacsliptranflag = l_main['sliptrainflag'],
                            iacsliptype = l_main['sliptype'],
                            iainrmlload = l_main['normalload'],
                            iaimaxload = l_main['maxload'],
                            # iaiintlflag =l_main['mansoon'], 
                            iaiftrbokgflag = l_main['ftrbookingflag'],
                            iavmaintrannumb =l_main['maintrainnumber'], 
                            iavsliptrannumb = l_main['sliptrainnumber'],
                            iainewtrannumb = l_main['newtrainnumber'],
                            iavnewtranname = l_main['newtrainname'],
                        )
                    #UPDATING OLD TRAIN SCHEDULE
                    url='https://www.satsweb.indianrail.gov.in/GetScheduleByTrainIDPublish_RestApi?Trainid='+e['oldtrainid']
                    headers = {"Content-Type": "application/json; charset=utf-8"}
                    response = requests.request("GET", url,headers=headers,proxies=proxy)
                    l_main=response.json()
                    if l_main!=[]:
                        l_main=l_main[0]
                        for l in l_main:
                            Update_count+=1
                            models.iem_transch.objects.filter(iaitranid=l_main['trainid']).update(
                                    iaitranid = l_main['trainid'],
                                    iavtrannumb = l_main['trainnumber'],
                                    iaisqncnumb = l_main['seqnumber'],
                                    iavzonecode = l_main['zonecode'],
                                    iavdvsncode = l_main['dvsncode'],
                                    iavsttncode = l_main['sttncode'],
                                    iacclsflag = l_main['classflag'],
                                    iaiwttarvl = l_main['wttarvl'],
                                    iaiwttdprt = l_main['wttdprt'],
                                    iachaltflag = l_main['haltflag'],
                                    iaiwttdayofrun = l_main['dayofrun'],
                                    iaipttdprt = l_main['pttdprt'],
                                    # iaipttarvl = l_main[''],
                                    iairuntime = l_main['runtime'],
                                    iaiacctime = l_main['acctime'],
                                    iaidectime = l_main['dectime'],
                                    iaitrfcalwc = l_main['trfcalwc'],
                                    iaienggalwc = l_main['enggalwc'],
                                    iaicstrtime = l_main['constrainttime'],
                                    iavcstrresn = l_main['constraintreason'],
                                    iacxingflag = l_main['crossingflag'],
                                    iavxingtran = l_main['crossingtrain'],
                                    iavxingtime = l_main['crossingtime'],
                                    iaiintrdist = l_main['intrdist'],
                                    iavpltfnumb =l_main['platformnumber'],
                                    iaccrewchng = l_main['crewchng'],
                                    iaclocochng = l_main['locochange'],
                                    iacrvslsttn = l_main['reversal_STATION'],
                                    iavtrcncode = l_main['trtncode'],
                                    iavcrewchngcode = l_main['crewchngcode'],
                                    iacgarbg = l_main['garbg'],
                                    iacwater = l_main['water']
                            )
            except:
                pass 

        for n in new_trains:
            #CREATING NEW TRAIN  PROFILE
            try:
                url='https://www.satsweb.indianrail.gov.in/GetCurrentProfileByTrainIDPublish_RestApi?Trainid='+n['trainid']
                headers = {"Content-Type": "application/json; charset=utf-8"}
                response = requests.request("GET", url,headers=headers,proxies=proxy)
                l_main=response.json()
                print(l_main)
                if l_main!=[]:
                    l_main=l_main[0]
                
                    create_count+=1
                    iadvaldfrom=datetime.datetime.strptime(l_main['validfrom'],"%d-%m-%Y")
                    iadvaldto=datetime.datetime.strptime(l_main['validto'],"%d-%m-%Y")
                    max_id=models.iem_tranprofmstr.objects.filter().aggregate(Max('id'))
                    max_id=int(max_id['id__max']) +1
                    models.iem_tranprofmstr.objects.create(
                        id=max_id,
                        iaitranid = l_main['trainid'],
                        iavtranowngrly = l_main['trainowngrly'],
                        iavtrannumb = l_main['trainnumber'],
                        iavtranname = l_main['trainname'],
                        mavtrantype = l_main['traintype'],
                        iavtranstyp = l_main['trainsubtype'],
                        iadvaldfrom =iadvaldfrom,
                        iadvaldto =iadvaldto,
                        iavdaysofsrvc = l_main['daysofsrvc'],
                        iavorgn = l_main['orig'],
                        iavdstn = l_main['dstn'],
                        iaideptime = l_main['dprttime'],
                        iaiarvltime = l_main['arvltime'],
                        iacgaug = l_main['gauge'],
                        iacuknwvldty = l_main['unknownvldty'],
                        iacirctcflag = l_main['irctcflag'],
                        iavsrcstt = l_main['srcstate'],
                        iavdstnstt = l_main['dstnstate'],
                        iairsrvflag = l_main['reserveflag'],
                        iavhdayctgy = l_main['holidaycategory'],
                        iavresncode = l_main['reasoncode'],
                        iacsrctrcn = l_main['sourcetraction'],
                        iacsliptranflag = l_main['sliptrainflag'],
                        iacsliptype = l_main['sliptype'],
                        iainrmlload = l_main['normalload'],
                        iaimaxload = l_main['maxload'],
                        # iaiintlflag =l_main['mansoon'], 
                        iaiftrbokgflag = l_main['ftrbookingflag'],
                        iavmaintrannumb =l_main['maintrainnumber'], 
                        iavsliptrannumb = l_main['sliptrainnumber'],
                        iainewtrannumb = l_main['newtrainnumber'],
                        iavnewtranname = l_main['newtrainname'],
                    )   
                #CREATING NEW TRAIN  SCHEDULE
                url='https://www.satsweb.indianrail.gov.in/GetScheduleByTrainIDPublish_RestApi?Trainid='+n['trainid']
                headers = {"Content-Type": "application/json; charset=utf-8"}
                response = requests.request("GET", url,headers=headers,proxies=proxy)
                l_main=response.json()
                if l_main!=[]:
                    l_main=l_main[0]
                    for l in l_main:
                        create_count+=1
                        max_id=models.iem_transch.objects.filter().aggregate(Max('id'))
                        max_id=int(max_id['id__max']) +1
                        models.iem_transch.objects.create(
                                id=max_id,
                                iaitranid = l_main['trainid'],
                                iavtrannumb = l_main['trainnumber'],
                                iaisqncnumb = l_main['seqnumber'],
                                iavzonecode = l_main['zonecode'],
                                iavdvsncode = l_main['dvsncode'],
                                iavsttncode = l_main['sttncode'],
                                iacclsflag = l_main['classflag'],
                                iaiwttarvl = l_main['wttarvl'],
                                iaiwttdprt = l_main['wttdprt'],
                                iachaltflag = l_main['haltflag'],
                                iaiwttdayofrun = l_main['dayofrun'],
                                iaipttdprt = l_main['pttdprt'],
                                # iaipttarvl = l_main[''],
                                iairuntime = l_main['runtime'],
                                iaiacctime = l_main['acctime'],
                                iaidectime = l_main['dectime'],
                                iaitrfcalwc = l_main['trfcalwc'],
                                iaienggalwc = l_main['enggalwc'],
                                iaicstrtime = l_main['constrainttime'],
                                iavcstrresn = l_main['constraintreason'],
                                iacxingflag = l_main['crossingflag'],
                                iavxingtran = l_main['crossingtrain'],
                                iavxingtime = l_main['crossingtime'],
                                iaiintrdist = l_main['intrdist'],
                                iavpltfnumb =l_main['platformnumber'],
                                iaccrewchng = l_main['crewchng'],
                                iaclocochng = l_main['locochange'],
                                iacrvslsttn = l_main['reversal_STATION'],
                                iavtrcncode = l_main['trtncode'],
                                iavcrewchngcode = l_main['crewchngcode'],
                                iacgarbg = l_main['garbg'],
                                iacwater = l_main['water']
                        )
            except:
                pass    
        
    m1.LogApi.objects.create(schedular_name = "train_schedule_update",dates = date.today(),times = datetime.datetime.now().time(),Total_count=create_count+Update_count,Total_update = Update_count,Total_Create = create_count)
    train_master_update()
    return data

scheduler = BackgroundScheduler()
scheduler.start()
ob = scheduler.add_job(train_schedule_update, 'cron', year='*', month='*', day='*', hour=23, minute=0, second=0)


def train_master_update():
    train_ids=list(models.iem_tranprofmstr.objects.filter().distinct('iaitranid').values_list('iaitranid', flat=True))
    Update_count = 0
    create_count = 0
    for t in train_ids:
        try:
            profiles=list(models.iem_tranprofmstr.objects.filter(iaitranid=t).values())[0]
            passing_rly=list(models.iem_transch.objects.filter(iaitranid=t).distinct('iavzonecode').values_list('iavzonecode', flat=True))
            passing_division=list(models.iem_transch.objects.filter(iaitranid=t).distinct('iavdvsncode').values_list('iavdvsncode', flat=True))
            rly=models.railwayLocationMaster.objects.get(location_code=profiles['iavtranowngrly'].upper())
                
            if models.trainMaster.objects.filter(trainid=t).exists():
                models.trainMaster.objects.filter(trainid=t).update(
                    trainid=t,
                    train_no=profiles['iavtrannumb'],
                    train_name=profiles['iavtranname'],
                    org_rly_id=rly,
                    org_railway_code=profiles['iavtranowngrly'],
                    lastmodified_on=datetime.datetime.now(),
                    passing_rly=passing_rly,
                    passing_division=passing_division
                )
                Update_count+=1
            else:
                
                models.trainMaster.objects.create(
                    trainid=t,
                    train_no=profiles['iavtrannumb'],
                    train_name=profiles['iavtranname'],
                    org_rly_id=rly,
                    org_railway_code=profiles['iavtranowngrly'],
                    created_on=datetime.datetime.now(),
                    passing_rly=passing_rly,
                    passing_division=passing_division
                )
                create_count+=1
        except:
            pass
    m1.LogApi.objects.create(schedular_name = "train_master_update",dates = date.today(),times = datetime.datetime.now().time(),Total_count=create_count+Update_count,Total_update = Update_count,Total_Create = create_count)
   
    return True


scheduler = BackgroundScheduler()
scheduler.start()
ob = scheduler.add_job(train_master_update, 'cron', year='*', month='*', day='*', hour=23, minute=0, second=0)




from rest_framework.decorators import api_view
from django.db import connection

@api_view(['GET'])
def pddashboardAPI(request):
    if request.method == 'GET': 
        try:
            # Execute a raw SQL query to select all data from the table
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM insp_marked_sumry")
                columns = [col[0] for col in cursor.description]  # Get column names
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]  # Fetch data
            cursor.close()
            return JsonResponse(data, safe=False)  # Return data as JSON
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)



from rest_framework.views import APIView
from rest_framework.response import Response

import jwt
import datetime
from django.conf import settings

SECRET_KEY = settings.SECRET_KEY




from functools import wraps




def create_jwt(id, issuer, subject, secret_key, ttl_seconds):
    try:
        now = datetime.datetime.utcnow()
        payload = {
            'id': id,
            'iat': now,
            'sub': subject,
            'iss': issuer,
        }
        from django.utils import timezone
        if ttl_seconds > 0:
            payload['exp'] = datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(seconds=3600)
        token = jwt.encode(payload, secret_key, algorithm='HS256')
        return token
    except Exception as e:
        return str(e)


def verify_jwt(jwt_token, secret_key):
    try:
        decoded_payload = jwt.decode(jwt_token, secret_key, algorithms=['HS256'])
        return "Token is valid"
    except jwt.ExpiredSignatureError:
        return "Token expired"
    except jwt.InvalidTokenError:
        return "Invalid token"
    except Exception as e:
        return str(e)


class GenerateToken(APIView):
    def post(self, request, format=None):
        data = request.data
        id = data.get('id')
        issuer = data.get('issuer')
        subject = data.get('subject')
        ttl_seconds = data.get('ttl_seconds', 3600)


        jwt_token = create_jwt(id, issuer, subject, SECRET_KEY, ttl_seconds)
        return Response({"jwt_token": jwt_token})


class VerifyToken(APIView):
    def post(self, request, format=None):
        data = request.data
        jwt_token = data.get('jwt_token')


        verification_status = verify_jwt(jwt_token, SECRET_KEY)
        return Response({"verification_status": verification_status})


def token_authentication_required(view_func):
    @authentication_classes([TokenAuthentication])
    @permission_classes([IsAuthenticated])
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return _wrapped_view




from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


#################################
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
#@token_authentication_required
@api_view(['GET'])
# @authentication_classes([TokenAuthentication])  # Use Token Authentication
# @permission_classes([IsAuthenticated])  # Require authentication
def pendency_dashboardAPI(request):
    if request.method == 'GET':
        try:
            # Execute a raw SQL query to select all data from the table
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM insp_marked_sumry")
                columns = [col[0] for col in cursor.description]  # Get column names
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]  # Fetch data
            cursor.close()

            return JsonResponse(data, safe=False)  # Return data as JSON
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
#################################



