from django.db import models
from asyncio.windows_events import NULL

# Create your models here.
class capex(models.Model):
    actual_prev_fy = models.CharField(max_length = 20)
    bg_curr = models.CharField(max_length=20)
    month = models.CharField(max_length=20)
    actual_prev_mon = models.CharField(max_length=20)
    planhd = models.CharField(max_length=50)
    serial_no = models.IntegerField()
    exp_curr = models.CharField(max_length=20)
    perc_fy = models.CharField(max_length=20)
    perc_curr = models.CharField(max_length=20)
    bg_mod = models.CharField(max_length=20)
    del_flag = models.IntegerField(default=0)
    class Meta:
        unique_together = (('month','serial_no'))

class Asset_Reliability(models.Model):
    Zone = models.CharField(max_length=4)
    failure_code = models.CharField(max_length=15)
    failure_subcode = models.CharField(max_length=15)
    yearType = models.CharField(max_length=15)
    division = models.CharField(max_length=15)
    classification = models.CharField(max_length=15)
    duration = models.IntegerField(editable=True)
    AF = models.IntegerField(editable=True)
    TD = models.IntegerField(editable=True)
    average_minutes = models.IntegerField(editable=True)
    del_flag = models.IntegerField(default=0)

class safety(models.Model):
    reportDate = models.DateField(default=None,null = True)
    accidentDate = models.DateField(default=None)
    accidentTime = models.DateTimeField(default=None)
    accidentId = models.PositiveBigIntegerField(null=True)
    rlyCode = models.CharField(max_length=10,null=True)
    rlyName = models.CharField(max_length=30,null=True)
    divCode = models.CharField(max_length=10,null=True)
    divName = models.CharField(max_length=50,null=True)
    section = models.CharField(max_length=30,null=True)
    consequentialFlag = models.CharField(max_length=70,null=True)
    accidentCategory = models.CharField(max_length=70,null=True)
    accidentType = models.CharField(max_length=60,null=True)
    location = models.CharField(max_length=80,null=True)
    trainType = models.CharField(max_length=80,null=True)
    trainNo = models.CharField(max_length=80,null=True)
    station = models.CharField(max_length=80,null=True)
    totalCasualities = models.IntegerField(null=True)
    respDept = models.CharField(max_length=200,null=True)
    del_flag = models.IntegerField(default=0)

# class earnings(models.Model):
#     id=models.BigAutoField(primary_key=True)  
#     head=models.CharField(max_length=50, null=True)
#     earn_prev_year=models.CharField(max_length=50, null=True)
#     budget_target_curr_year=models.CharField(max_length=50, null=True)
#     earn_prev_month=models.CharField(max_length=50, null=True)
#     inc_over_prev_yearmonth=models.CharField(max_length=50, null=True)
#     budget_proportion_end_month=models.CharField(max_length=50, null=True)
#     earn_curr_month=models.CharField(max_length=50, null=True)
#     variation_over_bp=models.CharField(max_length=50, null=True)

# class owe(models.Model):
#     id=models.BigAutoField(primary_key=True)  
#     head=models.CharField(max_length=50, null=True)
#     earn_prev_year=models.CharField(max_length=50, null=True)
#     budget_target_curr_year=models.CharField(max_length=50, null=True)
#     earn_prev_month=models.CharField(max_length=50, null=True)
#     inc_over_prev_yearmonth=models.CharField(max_length=50, null=True)
#     budget_proportion_end_month=models.CharField(max_length=50, null=True)
#     earn_curr_month=models.CharField(max_length=50, null=True)
#     variation_over_bp=models.CharField(max_length=50, null=True)

class Asset_Reliability_month(models.Model):
    
    Zone = models.CharField(max_length=4)
    failure_code = models.CharField(max_length=15)
    failure_subcode = models.CharField(max_length=15)
    yearType = models.CharField(max_length=15)
    division = models.CharField(max_length=15)
    classification = models.CharField(max_length=15)
    duration = models.IntegerField(editable=True)
    AF = models.IntegerField(editable=True)
    TD = models.IntegerField(editable=True)
    average_minutes = models.IntegerField(editable=True)
    del_flag = models.IntegerField(default=0)

class LogApi(models.Model):
    schedular_name = models.CharField(max_length = 500)
    dates = models.DateField()
    times = models.TimeField()
    Total_count = models.PositiveBigIntegerField()
    Total_update = models.PositiveIntegerField()
    Total_Create = models.PositiveIntegerField()

#punctuality
class Punctuality_Service_Output(models.Model):
    class Meta:
        unique_together = (('Scheduled_Date','Zone_Code','train_group'))
    Scheduled_Date = models.DateField(default=NULL)
    Zone_Code = models.CharField(max_length=4)
    train_count = models.IntegerField(editable=True)
    nlt_count = models.IntegerField(editable=True)
    train_group = models.CharField(max_length=5)
    del_flag = models.IntegerField(default=0)

class Cause_Service_Output(models.Model):
    class Meta:
        unique_together = (('Scheduled_Date','Zone_Code','train_group','cause_code'))
    Scheduled_Date = models.DateField(default=NULL)
    Zone_Code = models.CharField(max_length=4)
    cause_code = models.CharField(max_length=15)
    department_code = models.CharField(max_length=15)
    duration = models.IntegerField(editable=True)
    train_group = models.CharField(max_length=5) 
    del_flag = models.IntegerField(default=0)

class Loading_Commodity(models.Model):
    PlanHead = models.CharField(max_length=100,null=True)
    Yearly_Target = models.CharField(max_length=15)
    Actual_Upto_Month_LY = models.CharField(max_length=50)
    Actual_Upto_Month_CY = models.CharField(max_length=50)
    Var_Pctg = models.CharField(max_length=20)
    Var_Over_Target = models.CharField(max_length=50)
    del_flag = models.IntegerField(default=0)
    
class Loading_Zonal(models.Model):
    Rly = models.CharField(max_length=100,null=True)
    Yearly_Target = models.CharField(max_length=15)
    Actual_Upto_Month_LY = models.CharField(max_length=50)
    Actual_Upto_Month_CY = models.CharField(max_length=50)
    Var_Pctg = models.CharField(max_length=20)
    Var_Over_Target = models.CharField(max_length=50)
    del_flag = models.IntegerField(default=0)
    
class Loading_Overall(models.Model):
    Loading_Upto_Month_LY = models.CharField(max_length=50,default=NULL)
    NTKM_Upto_Month_LY = models.CharField(max_length=50,default=NULL)
    Earning_Upto_Month_LY = models.CharField(max_length=50,default=NULL)
    Lead_Upto_Month_LY = models.CharField(max_length=50,default=NULL)
    Yield_NTKM_Upto_Month_LY = models.CharField(max_length=50,default=NULL)
    Yield_MT_Upto_Month_LY = models.CharField(max_length=50,default=NULL)
    Loading_Upto_Month_CY = models.CharField(max_length=50,default=NULL)
    NTKM_Upto_Month_CY = models.CharField(max_length=50,default=NULL)
    Earning_Upto_Month_CY = models.CharField(max_length=50,default=NULL)
    Lead_Upto_Month_CY = models.CharField(max_length=50,default=NULL)
    Yield_NTKM_Upto_Month_CY = models.CharField(max_length=50,default=NULL)
    Yield_MT_Upto_Month_CY = models.CharField(max_length=50,default=NULL)
    Loading_LFY = models.CharField(max_length=50,default=NULL)
    NTKM_LFY = models.CharField(max_length=50,default=NULL)
    Earning_LFY = models.CharField(max_length=50,default=NULL)
    Lead_LFY = models.CharField(max_length=50,default=NULL)
    Yield_NTKM_LFY = models.CharField(max_length=50,default=NULL)
    Yield_MT_LFY = models.CharField(max_length=50,default=NULL)
    del_flag = models.IntegerField(default=0)

class earnings(models.Model):
    HEAD = models.CharField(max_length=40,null=True)
    MONTH = models.CharField(max_length=40,null=True)
    INCREASE_OVER_PREV = models.CharField(max_length=60,null=True)
    S_NO = models.IntegerField(null=True)
    VARIATION_BP = models.CharField(max_length=40,null=True)
    PREV_ACTUALS_MONTH = models.CharField(max_length=40,null=True)
    BUDGET_TARGET = models.CharField(max_length=40,null=True)
    BP_CURR_MONTH = models.CharField(max_length=40,null=True)
    ACTUALS_CURR_MONTH = models.CharField(max_length=40,null=True)
    PREV_YEAR = models.CharField(max_length=40,null=True)
    del_flag = models.IntegerField(default=0)
    class Meta:
        unique_together = (('MONTH','S_NO'))

class wagon(models.Model):
    id=models.AutoField(primary_key=True, editable=False, unique=True)
    wagon_type = models.CharField(max_length=50,null=True)
    wagon_no = models.PositiveBigIntegerField(null=True)
    owner_id = models.CharField(max_length=40,null=True)
    type = models.CharField(max_length=40,null=True)
    dm_date = models.DateField(null=True)
    ic_date = models.DateField(null=True)
    mf_id = models.CharField(max_length=40,null=True)
    manufacturer_date = models.DateField(null=True)
    del_flag = models.IntegerField(default=0)

# class complaint(models.Model):
#     id=models.BigAutoField(primary_key=True)
#     zone=models.CharField(max_length=15, null=True)
#     com_rcvd=models.IntegerField(null=True)
#     com_closed=models.IntegerField(null=True)
#     avg_pend=models.CharField(max_length=25,null=True)
 
class railmadad_cause_graph(models.Model):
    id=models.BigAutoField(primary_key=True)
    # name111=models.CharField(max_length=50, null=True)
    name=models.CharField(max_length=50, null=True)
    cleanliness=models.IntegerField(null=True)
    water=models.IntegerField(null=True)
    electrical=models.IntegerField(null=True)
    catering=models.IntegerField(null=True)
    security=models.IntegerField(null=True)
    r_ticketing=models.IntegerField(null=True)
    u_ticketing=models.IntegerField(null=True)
    refund_ticket=models.IntegerField(null=True)
    pssngr_amenities=models.IntegerField(null=True)
    luggage=models.IntegerField(null=True)
    goods=models.IntegerField(null=True)
    punctuality=models.IntegerField(null=True)
    
    medical=models.IntegerField(null=True)
    divyangjan=models.IntegerField(null=True)
    woman=models.IntegerField(null=True)
    corruption=models.IntegerField(null=True)
    staff=models.IntegerField(null=True)
    coach_clean=models.IntegerField(null=True)
    coach_main=models.IntegerField(null=True)
    bed=models.IntegerField(null=True)
    other=models.IntegerField(null=True)

    type=models.IntegerField(null=True, default=0)
    period=models.IntegerField(null=True, default=0)
    fromdate=models.DateField(null=True)
    todate=models.DateField(null=True)


class railmadad_bottom_reports(models.Model):
    name=models.CharField(max_length=50, null=True) 
    total=models.IntegerField(null=True, default=0)
    type=models.IntegerField(null=True, default=0)
    period=models.IntegerField(null=True, default=0)
    created_on=models.DateTimeField(auto_now=True, null=True)
# code used in bottom_reports
# for column: 'type'
# 0=zone
# 1=division
# 2=train

class rail_madad_1(models.Model):
    avgDiff=models.CharField(max_length=50, null=True) 
    avgDiffName=models.CharField(max_length=50, null=True) 
    avgFrtDiffName=models.CharField(max_length=50, null=True) 
    avgPendencyDiff=models.CharField(max_length=50, null=True) 
    avgPendencyDiffName=models.CharField(max_length=50, null=True) 
    avgRating=models.CharField(max_length=50, null=True) 
    cb=models.CharField(max_length=50, null=True) 
    compmode=models.CharField(max_length=50, null=True) 
    deptCode=models.CharField(max_length=50, null=True) 
    deptName=models.CharField(max_length=50, null=True) 
    divCode=models.CharField(max_length=50, null=True) 
    divName=models.CharField(max_length=50, null=True) 
    mainClosure=models.CharField(max_length=50, null=True) 
    ob=models.CharField(max_length=50, null=True) 
    org=models.CharField(max_length=50, null=True) 
    pendencyDiffCount=models.CharField(max_length=50, null=True) 
    perDisposal=models.CharField(max_length=50, null=True) 
    perShare=models.CharField(max_length=50, null=True) 
    pid=models.CharField(max_length=50, null=True) 
    pname=models.CharField(max_length=100, null=True) 
    ratingName=models.CharField(max_length=50, null=True) 
    recv=models.CharField(max_length=50, null=True) 
    settled=models.CharField(max_length=50, null=True) 
    sname=models.CharField(max_length=100, null=True) 
    znCode=models.CharField(max_length=50, null=True) 
    znName=models.CharField(max_length=50, null=True) 
    period=models.IntegerField(null=True, default=0)
    created_on=models.DateTimeField(auto_now=True, null=True)

class error_log(models.Model):
    pid=models.CharField(max_length=50, null=True) 
    fun_name=models.CharField(max_length=255,null=True,blank=True)
    err_details=models.TextField(null=True,blank=True)
    err_date=models.DateField(auto_now_add=True)



class wagon_breakup(models.Model):
    id=models.CharField(max_length=10,primary_key=True) 
    cum_prev=models.IntegerField(null=True, default=0)
    target=models.CharField(null=True, default='NA',max_length=10)
    monthly_achvd=models.IntegerField(null=True, default=0)
    cum_achvd=models.IntegerField(null=True, default=0)
    same_month_of_previous_year=models.IntegerField(null=True, default=0)