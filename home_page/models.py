from unittest.util import _MAX_LENGTH
from django.db import models
from asyncio.windows_events import NULL

class safety(models.Model):
    id=models.BigAutoField(primary_key=True)  
    type_of_accident=models.CharField(max_length=50)
    col1=models.IntegerField(null=True)
    col2=models.IntegerField(null=True)
    col3=models.IntegerField(null=True)
    col4=models.IntegerField(null=True)
    col5=models.IntegerField(null=True)
    change=models.CharField(max_length=50, null=True)

class loading_commodity_wise(models.Model):
    id=models.BigAutoField(primary_key=True)  
    commodity=models.CharField(max_length=50, null=True)
    targets=models.CharField(max_length=50, null=True)
    actuals=models.CharField(max_length=50, null=True)
    actuals_current_month=models.CharField(max_length=50, null=True)
    var_over_ly=models.CharField(max_length=50, null=True)
    var_over_target=models.CharField(max_length=50, null=True)

class loading_zone_wise(models.Model):
    id=models.BigAutoField(primary_key=True)  
    zone=models.CharField(max_length=50, null=True)
    targets=models.CharField(max_length=50, null=True)
    actuals=models.CharField(max_length=50, null=True)
    actuals_current_month=models.CharField(max_length=50, null=True)
    var_over_ly=models.CharField(max_length=50, null=True)
    var_over_target=models.CharField(max_length=50, null=True)

class loading_b3(models.Model):
    id=models.BigAutoField(primary_key=True)  
    description=models.CharField(max_length=50, null=True)
    se_dte=models.CharField(max_length=50, null=True)
    budget_targets=models.CharField(max_length=50, null=True)
    actuals=models.CharField(max_length=50, null=True)
    bp=models.CharField(max_length=50, null=True)
    approx=models.CharField(max_length=50, null=True)
    variation=models.CharField(max_length=50, null=True)
    increase=models.CharField(max_length=50, null=True)


class punctuality(models.Model):
    id=models.BigAutoField(primary_key=True)  
    zone=models.CharField(max_length=50, null=True)
    train_count=models.CharField(max_length=50, null=True)
    pp=models.CharField(max_length=50, null=True)
    total_delay=models.CharField(max_length=50, null=True)
    delay_per_train=models.CharField(max_length=50, null=True)
    cause1=models.CharField(max_length=50, null=True)
    cause2=models.CharField(max_length=50, null=True)
    cause3=models.CharField(max_length=50, null=True)
    cause4=models.CharField(max_length=50, null=True)
    cause5=models.CharField(max_length=50, null=True)
    cause6=models.CharField(max_length=50, null=True)
    cause7=models.CharField(max_length=50, null=True)
    cause8=models.CharField(max_length=50, null=True)
    cause9=models.CharField(max_length=50, null=True)
    cause10=models.CharField(max_length=50, null=True)
    cause11=models.CharField(max_length=50, null=True)
    cause12=models.CharField(max_length=50, null=True)
    cause13=models.CharField(max_length=50, null=True)
    cause14=models.CharField(max_length=50, null=True)
    cause15=models.CharField(max_length=50, null=True)
    cause16=models.CharField(max_length=50, null=True)
    others=models.CharField(max_length=50, null=True)

class punctuality_dept(models.Model):
    id=models.BigAutoField(primary_key=True)  
    dept=models.CharField(max_length=50, null=True)
    train_count=models.CharField(max_length=50, null=True)
    pp=models.CharField(max_length=50, null=True)
    total_delay=models.CharField(max_length=50, null=True)
    delay_per_train=models.CharField(max_length=50, null=True)
    cause1=models.CharField(max_length=50, null=True)
    cause2=models.CharField(max_length=50, null=True)
    cause3=models.CharField(max_length=50, null=True)
    cause4=models.CharField(max_length=50, null=True)
    cause5=models.CharField(max_length=50, null=True)
    cause6=models.CharField(max_length=50, null=True)
    cause7=models.CharField(max_length=50, null=True)
    cause8=models.CharField(max_length=50, null=True)
    cause9=models.CharField(max_length=50, null=True)
    cause10=models.CharField(max_length=50, null=True)
    cause11=models.CharField(max_length=50, null=True)
    cause12=models.CharField(max_length=50, null=True)
    cause13=models.CharField(max_length=50, null=True)
    cause14=models.CharField(max_length=50, null=True)
    cause15=models.CharField(max_length=50, null=True)
    cause16=models.CharField(max_length=50, null=True)
    others=models.CharField(max_length=50, null=True)



class earnings(models.Model):
    id=models.BigAutoField(primary_key=True)  
    description=models.CharField(max_length=50, null=True)
    year=models.CharField(max_length=50, null=True)
    budget_targets=models.CharField(max_length=50, null=True)
    actuals=models.CharField(max_length=50, null=True)
    bp=models.CharField(max_length=50, null=True)
    approx=models.CharField(max_length=50, null=True)
    variation=models.CharField(max_length=50, null=True)
    increase=models.CharField(max_length=50, null=True)

class owe(models.Model):
    id=models.BigAutoField(primary_key=True)  
    description=models.CharField(max_length=50, null=True)
    year=models.CharField(max_length=50, null=True)
    budget_targets=models.CharField(max_length=50, null=True)
    actuals=models.CharField(max_length=50, null=True)
    bp=models.CharField(max_length=50, null=True)
    approx=models.CharField(max_length=50, null=True)
    variation=models.CharField(max_length=50, null=True)
    increase=models.CharField(max_length=50, null=True)

class capex_item_wise(models.Model):
    id=models.BigAutoField(primary_key=True)  
    item=models.CharField(max_length=50, null=True)
    actual_exp=models.CharField(max_length=50, null=True)
    exp_sept_2021=models.CharField(max_length=50, null=True)
    utilization=models.CharField(max_length=50, null=True)
    be=models.CharField(max_length=50, null=True)
    be_mod=models.CharField(max_length=50, null=True)
    exp_sept_2022=models.CharField(max_length=50, null=True)
    utilization_be_mod=models.CharField(max_length=50, null=True)

class capex_head_wise(models.Model):
    id=models.BigAutoField(primary_key=True)  
    item=models.CharField(max_length=50, null=True)
    actual_exp=models.CharField(max_length=50, null=True)
    exp_sept_2021=models.CharField(max_length=50, null=True)
    utilization=models.CharField(max_length=50, null=True)
    be=models.CharField(max_length=50, null=True)
    be_mod=models.CharField(max_length=50, null=True)
    exp_sept_2022=models.CharField(max_length=50, null=True)
    utilization_be_mod=models.CharField(max_length=50, null=True)

class capex_resource_wise(models.Model):
    id=models.BigAutoField(primary_key=True)  
    item=models.CharField(max_length=50, null=True)
    actual_exp=models.CharField(max_length=50, null=True)
    exp_sept_2021=models.CharField(max_length=50, null=True)
    utilization=models.CharField(max_length=50, null=True)
    be=models.CharField(max_length=50, null=True)
    be_mod=models.CharField(max_length=50, null=True)
    exp_sept_2022=models.CharField(max_length=50, null=True)
    utilization_be_mod=models.CharField(max_length=50, null=True)

class infrastructure_creation(models.Model):
    id=models.BigAutoField(primary_key=True)  
    infrastructure_works=models.CharField(max_length=50, null=True)
    annual_target=models.CharField(max_length=50, null=True)
    cum_targets=models.CharField(max_length=50, null=True)
    cummulative_achieved=models.CharField(max_length=50, null=True)
    variation=models.CharField(max_length=50, null=True)

class rolling_stock_production(models.Model):
    id=models.BigAutoField(primary_key=True)  
    item=models.CharField(max_length=50, null=True)
    total_previous_year=models.IntegerField( null=True)
    progressive_current_year=models.IntegerField( null=True)
    same_month_of_previous_year=models.IntegerField( null=True)
    progressive_current_month=models.IntegerField( null=True)

class asset_reliabilty(models.Model):
    id=models.BigAutoField(primary_key=True)  
    item=models.CharField(max_length=50, null=True)
    targets=models.CharField(max_length=50, null=True)
    actuals=models.CharField(max_length=50, null=True)
    targets_current_month=models.CharField(max_length=50, null=True)
    progressive_current_month=models.CharField(max_length=50, null=True)
    y_day_actual=models.CharField(max_length=50, null=True)
    today_forecast=models.CharField(max_length=50, null=True)

class division_performa(models.Model):
    id=models.BigAutoField(primary_key=True)  
    month=models.CharField(max_length=50, null=True)
    cummulative=models.CharField(max_length=50, null=True)
    current_month_py=models.CharField(max_length=50, null=True)
    current_month=models.CharField(max_length=50, null=True)
    current_month_variation=models.CharField(max_length=50, null=True)
    current_year_py=models.CharField(max_length=50, null=True)
    current_year=models.CharField(max_length=50, null=True)
    current_year_variation=models.CharField(max_length=50, null=True)

######## vip references ############## 


class pendency_status_RB(models.Model):
    withdir=models.IntegerField(null=True)
    withzone=models.IntegerField(null=True)
    total=models.IntegerField(null=True) 
    draftreply=models.IntegerField(null=True)  
    datecreatedon=models.DateField(auto_now_add=True)

class pendency_status_zone_pu_div(models.Model):
    total=models.IntegerField(null=True)
    zone=models.IntegerField(null=True)
    div=models.IntegerField(null=True)
    refrb=models.IntegerField(null=True)
    deptcnt=models.IntegerField(null=True)
    datecreatedon=models.DateField(auto_now_add=True)

class pendency_status_DIR(models.Model):
    id=models.IntegerField(primary_key=True)
    vipid4zone=models.IntegerField(null=True)
    pendcountdir=models.IntegerField(null=True)
    vipid4dir=models.IntegerField(null=True)
    pendcountzone=models.IntegerField(null=True)
    unitcode=models.CharField(max_length=50, null=True)
    id3_6=models.IntegerField(null=True)
    id0_3=models.IntegerField(null=True)
    pendcount0_3=models.IntegerField(null=True)
    countdraft=models.IntegerField(null=True)
    id6_12=models.IntegerField(null=True)
    vipid4total=models.IntegerField(null=True)
    id12=models.IntegerField(null=True)
    pendcount6_12=models.IntegerField(null=True)
    pendcount3_6=models.IntegerField(null=True)
    counttotal=models.IntegerField(null=True)
    pendcount12=models.IntegerField(null=True)
    datecreatedon=models.DateField(auto_now_add=True)


class pendency_status_BM(models.Model):
    id=models.IntegerField(primary_key=True)
    vipid4zone=models.IntegerField(null=True)
    pendcountdir=models.IntegerField(null=True)
    vipid4dir=models.IntegerField(null=True)
    pendcountzone=models.IntegerField(null=True)
    unitcode=models.CharField(max_length=50, null=True)
    id3_6=models.IntegerField(null=True)
    id0_3=models.IntegerField(null=True)
    pendcount0_3=models.IntegerField(null=True)
    countdraft=models.IntegerField(null=True)
    id6_12=models.IntegerField(null=True)
    vipid4total=models.IntegerField(null=True)
    id12=models.IntegerField(null=True)
    pendcount6_12=models.IntegerField(null=True)
    pendcount3_6=models.IntegerField(null=True)
    counttotal=models.IntegerField(null=True)
    pendcount12=models.IntegerField(null=True)
    datecreatedon=models.DateField(auto_now_add=True)


class pendency_status_zone_div(models.Model):
    pendcountzone=models.IntegerField(null=True)
    id3_6=models.IntegerField(null=True)
    allid=models.IntegerField(null=True)
    divpendid=models.IntegerField(null=True)
    id0_3=models.IntegerField(null=True)
    pendcount0_3=models.IntegerField(null=True)
    id6_12=models.IntegerField(null=True)
    zonecountpend=models.IntegerField(null=True)
    zonecountall=models.IntegerField(null=True)
    id12=models.IntegerField(null=True)
    pendcount6_12=models.IntegerField(null=True)
    pendcount3_6=models.IntegerField(null=True)
    zonependid=models.IntegerField(null=True)
    pendcount12=models.IntegerField(null=True)
    divcountpend=models.IntegerField(null=True)
    zoneunitcode=models.CharField(max_length=50, null=True)
    datecreatedon=models.DateField(auto_now_add=True)


################ parliament #############

# first card
class parliament_count_LS_RS(models.Model): 
    lscount=models.IntegerField(null=True)   
    rscount=models.IntegerField(null=True)
    total=models.IntegerField(null=True)
    name=models.CharField(max_length=50, null=True)
    datecreatedon=models.DateField(auto_now_add=True)

# fourth card

class parliament_officerwise_pendency_DIR(models.Model):
    id=models.IntegerField(primary_key=True)
    specialmentioncount=models.IntegerField(null=True)
    countzerohour=models.IntegerField(null=True)
    desigcode=models.CharField(max_length=50, null=True)   
    dircode=models.IntegerField(null=True)
    bmid=models.IntegerField(null=True)
    countpetition=models.IntegerField(null=True)
    count377=models.IntegerField(null=True)
    countasur=models.IntegerField(null=True)
    datecreatedon=models.DateField(auto_now_add=True)


class parliament_officerwise_pendency_BM(models.Model):
    id=models.IntegerField(primary_key=True)
    specialmentioncount=models.IntegerField(null=True)
    countzerohour=models.IntegerField(null=True)
    desigcode=models.CharField(max_length=50, null=True)   
    dircode=models.IntegerField(null=True)
    bmid=models.IntegerField(null=True)
    countpetition=models.IntegerField(null=True)
    count377=models.IntegerField(null=True)
    countasur=models.IntegerField(null=True)
    datecreatedon=models.DateField(auto_now_add=True)


# third card
class parliament_DIRwise_pendency(models.Model):
    id=models.IntegerField(primary_key=True)
    countspecialmention=models.IntegerField(null=True)
    countzerohour=models.IntegerField(null=True)
    countpetition=models.IntegerField(null=True)
    designame=models.CharField(max_length=50, null=True) 
    countrule377=models.IntegerField(null=True)
    countass=models.IntegerField(null=True)
    datecreatedon=models.DateField(auto_now_add=True)

class parliament_BMwise_pendency(models.Model):
    id=models.IntegerField(primary_key=True)
    countspecialmention=models.IntegerField(null=True)
    countzerohour=models.IntegerField(null=True)
    countpetition=models.IntegerField(null=True)
    designame=models.CharField(max_length=50, null=True) 
    countrule377=models.IntegerField(null=True)
    countass=models.IntegerField(null=True)
    datecreatedon=models.DateField(auto_now_add=True)


# second card
class parliament_progress_count(models.Model):
    newentry=models.IntegerField(null=True)
    finalised=models.IntegerField(null=True)
    typee=models.CharField(max_length=50, null=True) 
    total=models.IntegerField(null=True)
    opnbal=models.IntegerField(null=True)
    datecreatedon=models.DateField(auto_now_add=True)

# parliament names for board member and directory    

class parliament_mydirectory(models.Model):
    myid=models.IntegerField(null=True)
    dir_name=models.CharField(max_length=50, null=True) 

class parliament_myboardmember(models.Model):
    myid=models.IntegerField(null=True)
    bm_name=models.CharField(max_length=50, null=True)        

class parliament_countOfficerwiseTotal(models.Model):
    id=models.IntegerField(primary_key=True)
    dircode=models.IntegerField(null=True)
    bmid=models.IntegerField(null=True)
    countspecialmention=models.IntegerField(null=True)
    countzerohour=models.IntegerField(null=True)
    countpetition=models.IntegerField(null=True)
    designame=models.CharField(max_length=50, null=True) 
    countrule377=models.IntegerField(null=True)
    countass=models.IntegerField(null=True)
    datecreatedon=models.DateField(auto_now_add=True)

class pendency_status_zone_div_dropdown(models.Model):
    zone=models.CharField(max_length=50, null=True)
    pendcountzone=models.IntegerField(null=True)
    id3_6=models.IntegerField(null=True)
    allid=models.IntegerField(null=True)
    divpendid=models.IntegerField(null=True)
    id0_3=models.IntegerField(null=True)
    pendcount0_3=models.IntegerField(null=True)
    id6_12=models.IntegerField(null=True)
    zonecountpend=models.IntegerField(null=True)
    zonecountall=models.IntegerField(null=True)
    id12=models.IntegerField(null=True)
    pendcount6_12=models.IntegerField(null=True)
    pendcount3_6=models.IntegerField(null=True)
    zonependid=models.IntegerField(null=True)
    pendcount12=models.IntegerField(null=True)
    divcountpend=models.IntegerField(null=True)
    zoneunitcode=models.CharField(max_length=50, null=True)
    datecreatedon=models.DateField(auto_now_add=True)
    
