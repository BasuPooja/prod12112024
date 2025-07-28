from misiProject.Imports.url_imports import  *

urlpatterns = [
    path('create_budget_form/',m5.create_budget_form,name="create_budget_form"),
    path('create_budget_details/',m5.create_budget_details,name="create_budget_details"),
    # path('summary_budget/',m5.summary_budget,name="summary_budget"),
    path('budget_implementation/',m5.budget_implementation,name="budget_implementation"),
    path('budget_dashboard/',m5.budget_dashboard,name="budget_dashboard"),
    path('UpdateBudget/',m5.UpdateBudget,name="UpdateBudget"),
    path('getPara/',m5.getPara,name="getPara"),
    path('getOfficer/',m5.getOfficer,name="getOfficer"),
    path('create_budget_draft_details/',m5.create_budget_draft_details,name="create_budget_draft_details"),
    path('validatePara_ajax/',m5.validatePara_ajax,name="validatePara_ajax"),
    path('budgetReportPdf/',m5.budgetReportPdf,name="budgetReportPdf"),
    path('budgetReportExcel/',m5.budgetReportExcel,name="budgetReportExcel"),

    path('updateStatus_budget_ajax/',m5.updateStatus_budget_ajax,name="updateStatus_budget_ajax"),
    path('updateCompliance_ajax/',m5.updateCompliance_ajax,name="updateCompliance_ajax"),
    path('updateCompliance_ajax1/',m5.updateCompliance_ajax1,name="updateCompliance_ajax1"),
    path('draftCompliance_ajax/',m5.draftCompliance_ajax,name="draftCompliance_ajax"),
    path('budgetReportPPT/',m5.budgetReportPPT,name="budgetReportPPT"),
    path('budgetSaveOtp_ajax/',m5.budgetSaveOtp_ajax,name="budgetSaveOtp_ajax"),
    path('budget_verify_my_otp_ajax/',m5.budget_verify_my_otp_ajax,name="budget_verify_my_otp_ajax"),

    path('budget_draft/',m5.budget_draft,name="budget_draft"),
    path('delete_budget_fun/',m5.delete_budget_fun,name="delete_budget_fun"),
    path('budget_draft_submission/',m5.budget_draft_submission,name="budget_draft_submission"),
    path('create_budget_draft_details/',m5.create_budget_draft_details,name="create_budget_draft_details"),
]


