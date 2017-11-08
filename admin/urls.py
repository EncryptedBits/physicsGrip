from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.render_adminhome),
    url(r'^login/$', views.render_adminlogin),
    url(r'^adminloginrequest/$', views.adminloginrequest),
    url(r'^adminlogoutrequest/$', views.adminlogoutrequest),
    url(r'^gallery/$', views.gallery_render),
    url(r'^course/$', views.courses_render),
    url(r'^ambassador/$', views.ambassadors_render),
    url(r'^section/$', views.sections_render),
    url(r'^subject/$', views.subject_render),
    url(r'^search/$', views.search_render),
    url(r'^createordeletesubject/$', views.create_subject),
    url(r'^gallerypicupload/$', views.upload_gallery),
    url(r'^requeststudentordeletedue/$', views.view_or_delete_due),
    url(r'^uploadnewamb/$', views.upload_ambassadors),
    url(r'^addnewcourse/$', views.create_course),
    url(r'^processcourse/$', views.process_course),
    url(r'^createordeletesection/$', views.process_section),
    url(r'^returncourses/$', views.return_courses),
    url(r'^returnsections/$', views.return_sections),
    url(r'^searchresult/$', views.search_result),
    url(r'^returnnamesearch/$', views.searchbyname_result),
    

]