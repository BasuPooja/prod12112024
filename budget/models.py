from email.policy import default
from re import S
from django.db import models


# Create your models here.
class budget_para(models.Model):
    budget_id = models.AutoField(primary_key=True)
    para_no = models.CharField(max_length=10, null=False)
    financial_year = models.CharField(max_length=10, null=False)
    title = models.CharField(max_length=200, null=False)
    action = models.CharField(max_length=50, null=False, default='Action Not Initiated')
    # marked_officer = models.CharField(max_length=50, null=True)
    # target_date = models.DateField(max_length=8, null=True)
    created_by = models.CharField(max_length=50, null=True)
    modified_by = models.CharField(max_length=50, null=True)
    created_on = models.DateField(null=True)
    modified_on = models.DateField(null=True)
    delete_flag = models.BooleanField(default=False)
    status_flag = models.IntegerField(max_length=7, null=True)
    overall_status = models.CharField(max_length=50, null=True)
    compliance = models.TextField(null=True)

class budget_specific_actions(models.Model):
    specific_action_id = models.AutoField(primary_key=True)
    budget_id = models.ForeignKey('budget_para', on_delete=models.CASCADE, null=True)
    specific_action = models.CharField(max_length=500, null=True)
    sub_specific_action = models.CharField(max_length=500, null=True)
    physical_target_given = models.CharField(max_length=100, null=True)
    financial_target_sanctioned = models.CharField(max_length=100, null=True)
    intended_outcome = models.CharField(max_length=100, null=True)
    physical_target_achieved = models.CharField(max_length=100, null=True)
    financial_target_achieved = models.CharField(max_length=100, null=True)
    intended_outcome_achieved = models.CharField(max_length=100, null=True)
    created_by = models.CharField(max_length=50, null=True)
    modified_by = models.CharField(max_length=50, null=True)
    created_on = models.DateField(null=True)
    modified_on = models.DateField(null=True)
    target_date = models.DateField(max_length=8, null=True)
    data_id = models.CharField(max_length=10, null=True)
    data_type = models.CharField(max_length=10, null=True)



class budget_marked_officers(models.Model):
    budget_marked_officers_id = models.AutoField(primary_key=True)
    specific_action_id = models.ForeignKey('budget_specific_actions', on_delete=models.CASCADE, null=True)
    marked_officer = models.ForeignKey('myadmin.Level_Desig', on_delete=models.CASCADE, null=True)
    # marked_officer = models.CharField(max_length=50, null=True)
    status_flag = models.IntegerField(max_length=7, null=True)



class budget_updates(models.Model):
    updates_id = models.AutoField(primary_key=True)
    budget_marked_officers_id = models.ForeignKey('budget_marked_officers', on_delete=models.CASCADE, null=True)
    type_of_update_flag = models.IntegerField(max_length=3, null=True)
    status_flag = models.IntegerField(max_length=7, null=True)
    overall_status = models.IntegerField(max_length=7, null=True)


class budget_otp(models.Model):
    otp_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('myadmin.Level_Desig', on_delete=models.CASCADE, null=True)
    otp = models.PositiveIntegerField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=False)
    
