

from django.urls import path
from . import views

urlpatterns = [
    path('',views.homepage),
    path('register',views.register),
    path('login',views.login),
    path('logout',views.logout),
    path('update',views.update),
    path('updateResume',views.updateResume),
    path('changeProfile',views.changeProfile),
    path('updateHeadline',views.updateHeadline),
    path('keySkills',views.keySkills),
    path('personal',views.personal),
    path('personal1',views.personalinfo),
    path('userExp',views.userExp),
    path('useredu',views.useredu),
    path('editEdu/<id>',views.editEdu),
    path('delete',views.delete),
    path('editExp/<id>',views.editExp),
    path('deleteExp/<id>',views.deleteExp),
    path('searchJob',views.searchJob),
    # company
    path('RecruitSignup',views.rcruitSignup),
    path('RecruitLogin',views.rcruitLogin),
    path('payment',views.payment),
    path('subscribe',views.subscribe),
    path('ChangePass',views.ChangePass),
    path('EditData',views.EditData),
    path('addJob',views.addJob),
    path('sub',views.sub),
    path('records',views.records),
    path('editjob/<id>',views.editjob),
    path('jobcat/<id>',views.jobcat),
    path('jobdetails/<id>',views.jobdetails),
    path('loginone/<id>',views.loginone),
    path('apply/<id>',views.apply),
    path('history/<id>',views.history),
    path('resp/<id>',views.resp),
    path('viewprofile/<id>',views.viewprofile),
    path('deletejob/<id>',views.deletejob),
    path('msgresp/<id>',views.sendmsg),
    path('openmsg/<id>',views.openmsg),
    path('inbox',views.inbox), 
    path('send/<id>',views.send),
    path('forget',views.forget),
    path('aboutus',views.aboutus),
    path('contact',views.contact),
    path('resetpass',views.resetpass),
    path('newpass',views.newpass),
    path('userpass',views.userpass)

 


]