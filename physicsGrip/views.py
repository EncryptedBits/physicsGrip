from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import MySQLdb

db = MySQLdb.connect("physicsgrip.mysql.pythonanywhere-services.com","physicsgrip","@mysql12","physicsgrip$default" )
cursor = db.cursor()

def render_home(request):
	user_loggedin = request.user.is_authenticated()
	if user_loggedin:
		return render(request, 'accounts/home_login.html', {})
	else:
		return render(request, 'accounts/home.html', {})

def render_gallery(request):
	db = MySQLdb.connect("physicsgrip.mysql.pythonanywhere-services.com","physicsgrip","@mysql12","physicsgrip$default" )
	cursor = db.cursor()
	q1 = """ select MAX(imageID) from GALLERY """
	cursor.execute(q1)
	print ">>> Query executed"
	max_id_tup = cursor.fetchone()
	#print ">>> ",max_id_tup
	max_id = max_id_tup[0]
	if max_id_tup[0] != None:
		print ">>> image is present"
		id_threshhold = max_id - 40
		q2 = """ delete from GALLERY where imageID < %d """%(id_threshhold)
		cursor.execute(q2)
		db.commit()
	q3 = """ select * from GALLERY order by upload_date DESC """
	cursor.execute(q3)
	print ">>> q3 Query executed"
	data = cursor.fetchall()
	print ">>> All data fetched"
	db.close()
	user_loggedin = request.user.is_authenticated()
	print "user_loggedin", user_loggedin
	if user_loggedin:
		extend_page = 'base_login.html'
	else:
		extend_page = 'base.html'
	return render(request, 'accounts/gallery.html',  {'data' : data, 'extend_page' : extend_page})

def render_courses(request):
	db = MySQLdb.connect("physicsgrip.mysql.pythonanywhere-services.com","physicsgrip","@mysql12","physicsgrip$default" )
	cursor = db.cursor()
	print ">>> connected to db"
	q1 = """ select * from COURSES """
	cursor.execute(q1)
	print ">>> Query executed"
	total_courses = cursor.fetchall()
	user_loggedin = request.user.is_authenticated()
	if user_loggedin:
		extend_page = 'base_login.html'
		loggedin = True
	else:
		extend_page = 'base.html'
		loggedin = False
	return render(request, 'accounts/courses.html', {'total_courses' : total_courses, 'extend_page' : extend_page, 'loggedin':loggedin})

def render_ambassadors(request):
	user_loggedin = request.user.is_authenticated()
	if user_loggedin:
		extend_page = 'base_login.html'
	else:
		extend_page = 'base.html'
	return render(request, 'accounts/ambassador.html', { 'extend_page' : extend_page})
