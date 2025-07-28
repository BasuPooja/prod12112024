from django.urls import path, re_path
from django.conf import settings
from einspect.models import *
from myadmin.models import *
from django.conf.urls.static import static
from django.conf import settings
from einspect import views as v2
from inspects import views as v1
from myadmin import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.messages import constants as messages

urlpatterns=[
    # master form
    path('masterTable/', v2.masterTable, name='masterTable'),

    path('inspection_view/', v2.inspection_view, name='inspection_view'),
    path('inspection_add/', v2.inspection_add, name='inspection_add'),
    
    path('viewInspect/', v2.viewInspect, name='viewInspect'),
    path('updateI/',v2.updateI,name='updateI'),
    path('delInspect/',v2.delInspect,name='delInspect'),
    path('upInspect/',v2.upInspect,name='upInspect'),
    
    path('viewProfile/', v1.viewProfile, name='viewProfile'),

    path('viewQuest/', v2.viewQuest, name='viewQuest'),
    path('updateQ/', v2.updateQ, name='updateQ'),
    path('upQuest/', v2.upQuest, name='upQuest'),
    path('delQuest/', v2.delQuest, name='delQuest'),

    path('getQuestion/', v2.getQuestion, name='getQuestion'),
    path('viewQuest3/', v2.viewQuest3, name='viewQuest3'),
    path('updateQ3/', v2.updateQ3, name='updateQ3'),
    path('upQuest3/', v2.upQuest3, name='upQuest3'),
    path('delQuest3/', v2.delQuest3, name='delQuest3'),
    path('user/', v2.user, name='user'),
    path('train_repo/', v2.train_repo, name='train_repo'),
    path('dependent_question/', v2.dependent_question, name='dependent_question'),
    path('dependColumn/', v2.dependColumn, name='dependColumn'),
    #dashboard(user form)
    path('mydashboard/', v2.mydashboard, name='mydashboard'),
    path('myfun/', v2.myfun, name='myfun'),
    path('showMenu/', v2.showMenu, name='showMenu'),
    # path('showquestions/', v2.showquestions, name='showquestions'),
    path('addQ145/', v2.addQ145, name='addQ145'),
    path('drop_option/', v2.drop_option, name='drop_option'),
    path('endStation/', v2.endStation, name='endStation'),
    path('getDataEntity/', v2.getDataEntity, name='getDataEntity'),
    path('getStationSectionWise/', v2.getStationSectionWise, name='getStationSectionWise'),
    path('getSectionDash/', v2.getSectionDash, name='getSectionDash'),
    path('palyResponse/', v2.palyResponse, name='palyResponse'),
    path('eInspectionUserForm/',v2.eInspectionUserForm,name='eInspectionUserForm'),
    path('changeEntityData/',v2.changeEntityData,name='changeEntityData'),
    path('checkFillofDepartment/', v2.checkFillofDepartment, name='checkFillofDepartment'),
    path('getDependentData/', v2.getDependentData, name='getDependentData'),

    # frontpage 26/08/2022
    path('frontpage/',v2.frontpage,name='frontpage'),

    #siri Form
    path('siriForm/',v2.siriForm, name="siriForm"),   
    path('showData/',v2.showData, name="showData"),
    path('showMenu/siriForm',v2.siriForm, name="siriForm"),   
    path('showMenu/showData',v2.showData, name="showData"),
    path('division_wise',v2.division_wise, name="division_wise"),
    #path('saveData',v2.saveData, name="saveData"),    
    path('showUserData',v2.showUserData, name="showUserData"),    
    path('saveRemarks',v2.saveRemarks, name="saveRemarks"),    
    path('department_wise',v2.department_wise, name="department_wise"),    
    path('remarks',v2.remarks, name="remarks"),
    path('DataShowing',v2.DataShowing, name="DataShowing"),
    path('getZoneEinsp/', v2.getZoneEinsp, name='getZoneEinsp'),
    path('AddIssue',v2.AddIssue, name="AddIssue"),
    path('saveIssue',v2.saveIssue, name="saveIssue"),
    path('validatSearch',v2.validatSearch, name="validatSearch"),
    path('showUserData',v2.showUserData, name="showUserData"),    
    path('showUserComaplaints',v2.showUserComaplaints, name="showUserComaplaints"),
    
    path('getSectionCode1',v2.getSectionCode1, name="getSectionCode1"),
    path('getStationCode1',v2.getStationCode1, name="getStationCode1"),
    path('updateUser',v2.updateUser, name="updateUser"),
    path('getdescripwise',v2.getdescripwise, name="getdescripwise"), 
    path('getForwardOfficer',v2.getForwardOfficer, name="getForwardOfficer"), 
    path('forwardToNext',v2.forwardToNext, name="forwardToNext"), 
    path('modalInfo',v2.modalInfo, name="modalInfo"),
    # path('show_siri_data',v1.show_siri_data, name="show_siri_data"), 

    # Roster
    path('saveDraft',v2.saveDraft,name='saveDraft'),
    path('roster_draft/',v2.roster_draft,name='roster_draft'),
    path('roster_draft_list/',v2.roster_draft_list,name='roster_draft_list'),
    path('showDraftData1',v2.showDraftData1,name='showDraftData1'),
    path('showUserDataDraft',v2.showUserDataDraft,name='showUserDataDraft'),
    path('edit_details',v2.edit_details,name='edit_details'),
    path('update_m1',v2.update_m1,name='update_m1'),
    path('update_m2',v2.update_m2,name='update_m2'),
    path('roster_details2/', v2.roster_details2, name='roster_details2'),
    path('roster/', v2.roster, name='roster'),
    path('view_roster/',v2.view_roster,name='view_roster'),
    path('roster_list/',v2.roster_list,name='roster_list'),
    
    # path('duration',v2.duration,name='duration'),
    path('showUserDataa',v2.showUserDataa,name='showUserDataa'),
    path('roster_schedule',v2.roster_schedule,name='roster_schedule'),
    path('delet',v2.delet,name='delet'),
    path('delet1',v2.delet1,name='delet1'),
    path('saveDuration',v2.saveDuration,name='saveDuration'),
    path('saveDurationUpdate',v2.saveDurationUpdate,name='saveDurationUpdate'),
    path('DurationFinal',v2.DurationFinal,name='DurationFinal'),
    path('DurationFinal_id',v2.DurationFinal_id,name='DurationFinal_id'),
    path('DurationUpDraft',v2.DurationUpDraft,name='DurationUpDraft'),
    
    path('DurationUp_id',v2.DurationUp_id,name='DurationUp_id'),
    path('edit_details_draft/',v2.edit_details_draft,name='edit_details_draft'),
    path('getFilterValueDraft',v2.getFilterValueDraft,name='getFilterValueDraft'),
    path('saveDataa',v2.saveDataa,name='saveDataa'),
    path('showUserData1',v2.showUserData1,name='showUserData1'),
    path('train_details',v2.train_details,name='train_details'),
    path('name_wise',v2.name_wise,name='name_wise'),
    path('getFilterValue',v2.getFilterValue,name='getFilterValue'),
    # path('roster_view',v2.roster_view,name='roster_view'),
    path('update_m',v2.update_m,name='update_m'),
    path('name_wise_m',v2.name_wise_m,name='name_wise_m'),
    # end roster
     path('UNDERDEV/', v2.UNDERDEV, name='UNDERDEV'),
    #report Inspection_conducted
    path('inspection_conducted',v2.inspection_conducted,name='inspection_conducted'),
    path('searchInspect',v2.searchInspect,name='searchInspect'),
    path('showInspect',v2.showInspect,name='showInspect'),
    path('inspectionConductedexcel/',v2.inspectionConductedexcel,name='inspectionConductedexcel'),
    #linen report   
    path('trainReport/',v2.trainReport,name='trainReport'),
    path('trainInspect/',v2.trainInspect,name='trainInspect'),
    path('trainInspectpdf/',v2.trainInspectpdf,name='trainInspectpdf'),

    # Report Paridhi
    path('footPlate_report/',v2.footPlate_report,name='footPlate_report'),
    path('showDetails/',v2.showDetails,name='showDetails'),
    path('searchDetails/',v2.searchDetails,name='searchDetails'),
    path('viewDetails/',v2.viewDetails,name='viewDetails'),
    path('pdfDetails/',v2.pdfDetails,name='pdfDetails'),
    path('getValues/',v2.getValues,name='getValues'),
    path('checkFillofStation/', v2.checkFillofStation, name='checkFillofStation'),   
    path('getstations',v2.getstations,name='getstations'),
    path('ValidateDateOfInsp',v2.ValidateDateOfInsp,name='ValidateDateOfInsp'),
    path('getConcernedOfficer/', v2.getConcernedOfficer, name='getConcernedOfficer'),
    path('getSectionCode',v2.getSectionCode, name="getSectionCode"),
    path('getStationCode',v2.getStationCode, name="getStationCode"),
    path('showInspect',v2.showInspect,name='showInspect'),
    path('stationInsp/',v2.stationInsp,name='stationInsp'),
    path('showDet/',v2.showDet,name='showDet'),
    path('searchDet/',v2.searchDet,name='searchDet'),
    path('complienceForm/',v2.complienceForm,name='complienceForm'),
    path('showCompliance/',v2.showCompliance,name='showCompliance'),
    path('searchCompliance/',v2.searchCompliance,name='searchCompliance'),
    path('updateEinspUser/',v2.updateEinspUser,name='updateEinspUser'),
    path('updateSiriUser/',v2.updateSiriUser,name='updateSiriUser'),
    path('actionEinsp/',v2.actionEinsp,name='actionEinsp'),
    path('actionSiri/',v2.actionSiri,name='actionSiri'),
    path('stationReviewpdf/',v2.stationReviewpdf,name='stationReviewpdf'),
    path('DeficiencyReportpdf/',v2.DeficiencyReportpdf,name='DeficiencyReportpdf'),

    
# swasti  start


    path('cardsCategories/',v2.cardsCategories,name='cardsCategories'),   
    path('adminCards/',v2.adminCards,name='adminCards'),

    path('viewStation/',v2.viewStation,name='viewStation'),
    path('saveStation1/',v2.saveStation1,name='saveStation1'),
    path('UpdateStation/',v2.UpdateStation,name='UpdateStation'),
    path('delStation/',v2.delStation,name='delStation'),
    path('zoneChangeStation/',v2.zoneChangeStation,name='zoneChangeStation'),


    path('zoneChangeTrain/',v2.zoneChangeTrain,name='zoneChangeTrain'),
    path('viewTrain/',v2.viewTrain,name='viewTrain'),
    path('saveTrain/',v2.saveTrain,name='saveTrain'),
    path('updateTrain/',v2.updateTrain,name='updateTrain'),
    path('delTrain/',v2.delTrain,name='delTrain'),
    

    path('zoneChangeSection/',v2.zoneChangeSection,name='zoneChangeSection'),
    path('viewSection/',v2.viewSection,name='viewSection'),
    path('saveSection/',v2.saveSection,name='saveSection'),
    path('updateSection/',v2.updateSection,name='updateSection'),
    path('delSection/',v2.delSection,name='delSection'),
    path('sectionStartChange',v2.sectionStartChange,name='sectionStartChange'),
    path('getSectionCodeName',v2.getSectionCodeName,name='getSectionCodeName'),
    path('ssName/',v2.ssName,name='ssName'),


    path('zoneChangeRr/',v2.zoneChangeRr,name='zoneChangeRr'),
    path('viewRunningRoom/',v2.viewRunningRoom,name='viewRunningRoom'),
    path('saveRr/',v2.saveRr,name='saveRr'),
    path('updateRr/',v2.updateRr,name='updateRr'),
    path('delRr/',v2.delRr,name='delRr'),
    path('viewquestions/',v2.viewquestions,name='viewquestions'),
    
    path('stationReport/',v2.stationReport,name='stationReport'),
    path('stationInspect/',v2.stationInspect,name='stationInspect'),
    path('stationReportPdf/',v2.stationReportPdf,name='stationReportPdf'),


    # swasti end
    ####     neilotpal
     path('analysis_report/',v2.analysis_report,name='analysis_report'),
     path('searchEInspectDetails/',v2.searchEInspectDetails,name='searchEInspectDetails'),
     path('AnalysisReportpdf/',v2.AnalysisReportpdf,name='AnalysisReportpdf'),

    # Supriya (Report)
    path('InspectionSummary_report/',v2.InspectionSummary_report,name='InspectionSummary_report'),
    path('searchdetailsISR/',v2.searchdetailsISR,name='searchdetailsISR'),
    path('showdetailsISR/',v2.showdetailsISR,name='showdetailsISR'),
    path('inspectionsummaryReportPdf/',v2.inspectionsummaryReportPdf,name='inspectionsummaryReportPdf'),

    #report Train review
    path('Train_inspection/',v2.Train_inspection,name='Train_inspection'),
    path('searchTrain',v2.searchTrain,name='searchTrain'),
    path('showTrain',v2.showTrain,name='showTrain'),
    path('trainReviewpdf/',v2.trainReviewpdf,name='trainReviewpdf'),


    ##### OBHS report Swasti/Parul
    path('OBHS_report/',v2.OBHS_report,name='OBHS_report'),
    path('searchOBHS',v2.searchOBHS,name='searchOBHS'),

######### Apeksha URLs: 
    path('disableQuest/', v2.disableQuest, name='disableQuest'),
    path('enableQuest/', v2.enableQuest, name='enableQuest'),
    path('disableinspect/', v2.disableinspect, name='disableinspect'),
    path('enableinspect/', v2.enableinspect, name='enableinspect'),
    path('disbalequest3/', v2.disbalequest3, name='disbalequest3'),
    path('enablequest3/', v2.enablequest3, name='enablequest3'),
    path('filter_masterform/', v2.filter_masterform, name='filter_masterform'),   



    path('setAllDepartment/', v2.setAllDepartment, name='setAllDepartment'),   
    path('showMenuEdit/', v2.showMenuEdit, name='showMenuEdit'),  
    path('showMenuFinal/', v2.showMenuFinal, name='showMenuFinal'),   

    path('actionEinspByMe/', v2.actionEinspByMe, name='actionEinspByMe'),  
    path('updateForwarded/', v2.updateForwarded, name='updateForwarded'),  
    path('actionEinspForByMe/', v2.actionEinspForByMe, name='actionEinspForByMe'),  
    path('actionEinspForToMe/', v2.actionEinspForToMe, name='actionEinspForToMe'),  

    path('updateForwardToMeData/', v2.updateForwardToMeData, name='updateForwardToMeData'),

    path('getAllDepartment/', v2.getAllDepartment, name='getAllDepartment'),

    path('performanceRating/', v2.performanceRating, name='performanceRating'),

    path('actorForm/', v2.actorForm, name='actorForm'),
    
    path('openAllPerformance/<str:insp>/<str:actor>',v2.openAllPerformance,name='openAllPerformance'),

    path('fiStartPage/', v2.fiStartPage, name='fiStartPage'),

    path('openAllQuestions/<str:actor>/<str:insp>',v2.openAllQuestions,name='openAllQuestions'),   
    path('openActorDetails/<str:actor>/<str:val>',v2.openActorDetails,name='openActorDetails'),

    #URLs APEKSHA
    path('compliance_phase2/', v1.compliance_phase2, name='compliance_phase2'),

    path('api/getConcernedOfficerList/', v2.getConcernedOfficerList, name='getConcernedOfficerList'),
    path('forwardInfo',v2.forwardInfo, name="forwardInfo"),


    # CIRI saving in Phase1
    path('siriForm1/',v2.siriForm1, name="siriForm1"),
    path('showUserDataa1',v2.showUserDataa1,name='showUserDataa1'),
    path('showData1/',v2.showData1, name="showData1"),
    path('showUserComaplaints1',v2.showUserComaplaints1, name="showUserComaplaints1"),
    path('updateUser1',v2.updateUser1, name="updateUser1"),
    path('forwardToNext1',v2.forwardToNext1, name="forwardToNext1"), 
    path('forwardInfo1',v2.forwardInfo1, name="forwardInfo1"),
    path('modalInfo1',v2.modalInfo1, name="modalInfo1"),



    ############  api @api_view(['GET'])


    path('api/siriForm_api/',v2.siriForm_api,name='siriForm_api'),
    path('api/getUserRailwayDivision/',v2.getUserRailwayDivision,name='getUserRailwayDivision'),
    # path('api/getRailways/',v2.getRailways,name='getRailways'),
    path('api/getRailways_ciri/',v2.getRailways_ciri,name='getRailways_ciri'),
    path('api/getDivision/',v2.getDivision,name='getDivision'),
    path('api/getSection/',v2.getSection,name='getSection'),
    path('api/getStation/',v2.getStation,name='getStation'),
    path('api/getTrain/',v2.getTrain,name='getTrain'),
    path('api/getDepartment/',v2.getDepartment,name='getDepartment'),
    path('api/issue_category/',v2.issue_category,name='issue_category'),
    path('api/ConcernedOfficer/', v2.ConcernedOfficer, name='ConcernedOfficer'),
    path('api/upload_img_api/', v2.upload_img_api, name='upload_img_api'),


    ###################app android api phase1 start ##################
    path('api/save_inspection_details/', v2.save_inspection_details, name='save_inspection_details'),
    path('api/get_marked_officers/', v2.get_marked_officers, name='get_marked_officers'),
    path('api/getRailways/',v2.getRailways,name='getRailways'),
    path('api/getDivisions/',v2.getDivisions,name='getDivisions'),  #Aryma
    path('api/generate_title/', v2.generate_title, name='generate_title'),
    # path('api/getUserRailwayDivision/',v2.getUserRailwayDivision,name='getUserRailwayDivision'),
    path('api/AccompaniedByList/', v2.AccompaniedByList, name='AccompaniedByList'),
    path('api/chooseLocation/', v2.chooseLocation, name='chooseLocation'),
    # path('api/upload_img_api/', v2.upload_img_api, name='upload_img_api'),


     ###################app android api phase1 end##################
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)