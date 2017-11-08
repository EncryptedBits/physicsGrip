from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [

	url(r'^register/$', views.render_registerForm),
	url(r'^newuser/$', views.register_newuser),
	url(r'^login/$', views.user_login),
	url(r'^logout/$', views.user_logout),
	url(r'^paymentedregistration/$', views.register_payment),
	

#    url(r'^$', views.render_home),
#    url(r'^gallery/$', views.render_gallery),
#    url(r'^courses/$', views.render_courses),
#    url(r'^ambassadors/$', views.render_ambassadors),
#    url(r'^admin/', admin.site.urls),
#    url(r'^accounts/', include('accounts.urls')),
]