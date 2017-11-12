from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import studentForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from time import strftime, localtime
import datetime
import MySQLdb


db = MySQLdb.connect("localhost","root","@mysql12","PHYSICSGRIP" )
cursor = db.cursor()


def save_image(img):
	fs = FileSystemStorage()
	path_to_dp = 'User_dp/'+str('UserDP_')+str(datetime.datetime.now())
	filename = fs.save(path_to_dp, img)
	uploaded_file_url = fs.url(filename)
	return uploaded_file_url

def render_registerForm(request):
	#print ">>> ",request.POST
	request.session['course_selected'] = request.POST['register']
	#print ">>> session data: ",request.session['course_selected']
	user_loggedin = request.user.is_authenticated()
	if user_loggedin:
		extend_page = 'base_login.html'
	else:
		extend_page = 'base.html'
	return render(request, 'accounts/register.html', { 'extend_page' : extend_page})

def register_newuser(request):
	try:
		db = MySQLdb.connect("localhost","root","@mysql12","PHYSICSGRIP" )
		cursor = db.cursor()
	except Exception as e:
		print ">>> ERROR : ",e
		if settings.DEBUG :
			msg = "DATABASE ERROR : Connection not established..."
		else:
			msg = "INTERNAL ERROR : Connection not established..."
		user_loggedin = request.user.is_authenticated()
		if user_loggedin:
			extend_page = 'base_login.html'
		else:
			extend_page = 'base.html'
		return render(request, 'errorpage.html', {'error_msg': msg, 'extend_page' : extend_page})
	if request.method == 'POST':
		#print ">>> ",request.POST
		print ">>> COURSE SELECTED ",request.session['course_selected']
		new_studForm = studentForm(request.POST, request.FILES)
		if new_studForm.is_valid():
			f_name = new_studForm.cleaned_data['f_name']
			l_name = new_studForm.cleaned_data['l_name']
			dob = new_studForm.cleaned_data['dob']
			Fa_name = new_studForm.cleaned_data['Fa_name']
			Mo_name = new_studForm.cleaned_data['Mo_name']
			Mob1 = new_studForm.cleaned_data['Mob1']
			Mob2 = new_studForm.cleaned_data.get('Mob2', None)
			pswd1 = new_studForm.cleaned_data['pswd1']
			pswd2 = new_studForm.cleaned_data['pswd2']
			town_vil = new_studForm.cleaned_data['town_vil']
			zip_code = new_studForm.cleaned_data['zip_code']
			addr = new_studForm.cleaned_data['addr']
			dp = new_studForm.cleaned_data.get('dp', None)
			if pswd1 != pswd2:
				msg = "The password do not match..."
				user_loggedin = request.user.is_authenticated()
				if user_loggedin:
					extend_page = 'base_login.html'
				else:
					extend_page = 'base.html'
				db.close()
				return render(request, 'errorpage.html', {'error_msg': msg, 'extend_page' : extend_page})
			q0 = """ select rollno from STUDENTS where Mob1 = '%s' """%(Mob1)
			cursor.execute(q0)
			duplicate = cursor.fetchone()
			if duplicate :
				error_msg = "Primary mobile no. is allready present. Haven't you registered!"
				user_loggedin = request.user.is_authenticated()
				if user_loggedin:
					extend_page = 'base_login.html'
				else:
					extend_page = 'base.html'
				db.close()
				return render(request, 'errorpage.html', {'error_msg': error_msg, 'extend_page' : extend_page})

			if request.POST['register'] == 'pay_later':

				try:
					q0 = """ SELECT fee from COURSES WHERE courseID = %d """%(int(request.session['course_selected']))
					cursor.execute(q0)
					fee = cursor.fetchone()[0]
					q1 = """ insert into STUDENTS(f_name, l_name, dob, Fa_name, Mo_name, 
						Mob1, pswd, town_vil, zip_code, addr, DUE) VALUES ('%s', '%s', '%s', '%s', '%s', 
						'%s', '%s', '%s', '%s', '%s', %d)
				 		"""%(f_name, l_name, dob, Fa_name, Mo_name, Mob1, pswd1, town_vil, zip_code, addr, fee)
					print ">>> New user registeration begin"
					cursor.execute(q1)
					#db.commit()
				 	print ">>> New user registered"

					q0 = """ select rollno from  STUDENTS where Mob1 = '%s' """%(Mob1)
					cursor.execute(q0)
					data = cursor.fetchone()
				 	
					new_user = User.objects.create_user(username=data[0], password=pswd1)
					new_user.save()
				 	
					print ">>> django User registerd..."
					q_c1 = """ update COURSES set no_of_stud = no_of_stud + 1 where courseID = %d """%(int(request.session['course_selected']))
					cursor.execute(q_c1)
					#db.commit()
				 	print ">>> COURSES table updated..."

					q_c2 = """ select curr_addm_sec from COURSES where courseID = %d """%(int(request.session['course_selected']))
					cursor.execute(q_c2)
					data1 = cursor.fetchone()
					print ">>> CURR SECTION table fetched..."
					if data1[0] == None:
						return render(request, 'errorpage.html', {'error_msg' : "The addmission section is not defined. Contact the administrator."})
					q_s1 = """ update SECTION set no_of_stud = no_of_stud + 1 where sectionID = %d """%(int(data1[0]))
					cursor.execute(q_c1)
					#db.commit()
				 	print ">>> SECTION table updated..."
				 	
					q_r1 = """ insert into REGISTRATIONS(reg_date, reg_time, stud_roll, course_id, section)
				 	VALUES('%s','%s',%d,%d, %d) """ %(strftime('%Y:%m:%d', localtime()),strftime('%H:%M:%S', 
				 		localtime()),data[0], int(request.session['course_selected']),data1[0])
					cursor.execute(q_r1)
					#db.commit()
				 	print ">>> REGISTRATIONS table filled..."
				 	
					if Mob2:
						#print ">>> Mob2 adding begin..."
				 		q3 = """ update STUDENTS set Mob2 = '%s' where Mob1 = '%s' """%(Mob2, Mob1)
						cursor.execute(q3)
						db.commit()
						print ">>> Mob2 added..."
					if dp:
						#print ">>> dp addition begin..."
				 		uploaded_file_url = save_image(dp)
					else:
						uploaded_file_url = settings.DEFAULT_DP
						q4 = """ update STUDENTS set pathofdp = '%s' where Mob1 = '%s' """%(uploaded_file_url, Mob1)
						cursor.execute(q4)
						db.commit()
						print ">>> DP saved at : ",uploaded_file_url
					db.commit()
					user_loggedin = request.user.is_authenticated()
					if user_loggedin:
						extend_page = 'base_login.html'
					else:
						extend_page = 'base.html'
					db.close()
					return render(request, 'custom_page.html',{'title' : "SUCCESS", 'header': "REGISTERED", 'msg' : "You are now successfully registered. Your roll no is : %d..."%(data), 'extend_page' : extend_page})
				except Exception as e:
					db.rollback()
					print ">>> ERROR : ",e
					if settings.DEBUG :
						msg = "DATABASE ERROR : User not registered..."
					else:
						msg = "INTERNAL ERROR : User not registered..."
					user_loggedin = request.user.is_authenticated()
					if user_loggedin:
						extend_page = 'base_login.html'
					else:
						extend_page = 'base.html'
					db.close()
					return render(request, 'errorpage.html', {'error_msg': msg, 'extend_page' : extend_page})
			else:
				try:
					q11 = """ insert into AUX_STUDENTS(f_name, l_name, dob, Fa_name, Mo_name, 
						Mob1, pswd, town_vil, zip_code, addr, adding_time, adding_date) VALUES ('%s', '%s', '%s', '%s', '%s', 
						'%s', '%s', '%s', '%s', '%s', '%s', '%s')
					 """%(f_name, l_name, dob, Fa_name, Mo_name, Mob1, pswd1, town_vil,
					  zip_code, addr, strftime('%H:%M:%S', localtime()), strftime('%Y:%m:%d', localtime()))
					cursor.execute(q11)
					#db.commit()
					request.session['mob'] = Mob1
					q0 = """ select aux_id from  AUX_STUDENTS where Mob1 = '%s' """%(Mob1)
					cursor.execute(q0)
					data = cursor.fetchone()
				 	
					if Mob2:
						#print ">>> Mob2 adding begin..."
				 		q3 = """ update AUX_STUDENTS set Mob2 = '%s' where Mob1 = '%s' """%(Mob2, Mob1)
						cursor.execute(q3)
						#db.commit()
				 		print ">>> Mob2 added..."
					if dp:
						#print ">>> dp addition begin..."
				 		uploaded_file_url = save_image(dp)
						q4 = """ update AUX_STUDENTS set pathofdp = '%s' where Mob1 = '%s' """%(uploaded_file_url, Mob1)
						cursor.execute(q4)
						#db.commit()
				 		print ">>> DP saved at : ",uploaded_file_url
					#print ">>> session data :", request.session['mob'], request.session['course_selected']
					q2 = """ select fee, name from COURSES where courseID = %d """%(int(request.session['course_selected']))
					cursor.execute(q2)
					data = cursor.fetchone()
					fee = data[0]
					course_name = data[1]
					db.commit()
					user_loggedin = request.user.is_authenticated()
					if user_loggedin:
						extend_page = 'base_login.html'
					else:
						extend_page = 'base.html'
					db.close()
					return render(request, 'payment.html', {'course' : course_name,  'fee' : fee, 'extend_page' : extend_page})
				except:
					db.rollback()
					if settings.DEBUG :
						msg = "DATABASE ERROR : User not registered..."
					else:
						msg = "INTERNAL ERROR : User not registered..."
					user_loggedin = request.user.is_authenticated()
					if user_loggedin:
						extend_page = 'base_login.html'
					else:
						extend_page = 'base.html'
					db.close()
					return render(request, 'errorpage.html', {'error_msg': msg, 'extend_page' : extend_page})
		else:
			msg = "Please fill all the required fields."
			user_loggedin = request.user.is_authenticated()
			if user_loggedin:
				extend_page = 'base_login.html'
			else:
				extend_page = 'base.html'
			db.close()
			return render(request, 'errorpage.html',{'error_msg': msg, 'extend_page' : extend_page})
	else:
		user_loggedin = request.user.is_authenticated()
		if user_loggedin:
			extend_page = 'base_login.html'
		else:
			extend_page = 'base.html'
		db.close()
		return render(request, 'errorpage.html', {'error_msg': "Please visit course page...", 'extend_page' : extend_page})

def register_payment(request):
	try:
		db = MySQLdb.connect("localhost","root","@mysql12","PHYSICSGRIP" )
		cursor = db.cursor()
	except Exception as e:
		print ">>> ERROR : ",e
		if settings.DEBUG :
			msg = "DATABASE ERROR : Connection not established..."
		else:
			msg = "INTERNAL ERROR : Connection not established..."
		user_loggedin = request.user.is_authenticated()
		if user_loggedin:
			extend_page = 'base_login.html'
		else:
			extend_page = 'base.html'
		return render(request, 'errorpage.html', {'error_msg': msg, 'extend_page' : extend_page})
	if request.POST['pay_mode'] == 'cancel' :
		q1 = """ delete from AUX_STUDENTS where Mob1 = '%s' """%(request.session['mob'])
		del request.session['course_selected']
		del request.session['mob']
		db.close()
		return redirect('/courses/')
	else:
		print ">>> session Mob data", request.session['mob']
		Mob1 = request.session['mob']
		del request.session['mob']
		try:
			q2 = """ select * from AUX_STUDENTS where Mob1 = '%s' """%(Mob1)
			cursor.execute(q2)
			d = cursor.fetchone()
			q3 = """ insert into STUDENTS(f_name, l_name, dob, Fa_name, Mo_name, 
					Mob1, Mob2, pswd, town_vil, zip_code, addr, pathofdp, fee) VALUES ('%s', '%s', '%s', '%s', '%s', 
					'%s', '%s', '%s', '%s', '%s','%s','%s' %d)
					 """ %(d[1],d[2],d[3],d[4],d[5],d[6],d[7],d[8],d[9],d[10],d[11],d[12], 0)
			cursor.execute(q3)
			#db.commit()
			print ">>> User registered permanently..."

			q4 = """ select rollno, pswd from STUDENTS where Mob1 = '%s' """%(d[6])
			cursor.execute(q4)
			data = cursor.fetchone()
			new_user = User.objects.create_user(username=data[0], password=d[1])
			new_user.save()
			print ">>> Django User registered..."
			q_c1 = """ update COURSES set no_of_stud = no_of_stud + 1 where courseID = %d """%(int(request.session['course_selected']))
			cursor.execute(q_c1)
			#db.commit()
			print ">>> COURSES table updated..."

			q_c2 = """ select curr_addm_sec from COURSES where courseID = %d """%(int(request.session['course_selected']))
			cursor.execute(q_c2)
			data1 = cursor.fetchone()

			q_s1 = """ update SECTION set no_of_stud = no_of_stud + 1 where sectionID = %d """%(data1[0])
			cursor.execute(q_c1)
			#db.commit()
		 	print ">>> SECTION table updated..."

			q_r1 = """ insert into REGISTRATIONS(reg_date, reg_time, stud_roll, course_id)
			VALUES('%s','%s',%d,%d) """ %(strftime('%Y:%m:%d', localtime()),strftime('%H:%M:%S', 
			localtime()),data[0], request.session['course_selected'])
			cursor.execute(q_r1)

			print ">>> REGISTRATIONS table filled..."

			db.commit()
			del request.session['course_selected']
			user_loggedin = request.user.is_authenticated()
			if user_loggedin:
				extend_page = 'base_login.html'
			else:
				extend_page = 'base.html'
			db.close()
			return render(request, 'custom_page.html',{'title' : "SUCCESS", 'header': "REGISTERED", 'msg' : "You are now successfully registered. Login to continue...", 'extend_page' : extend_page})
		except:
			db.rollback()
			del request.session['course_selected']
			if settings.DEBUG :
				msg = "DATABASE ERROR : User not registered..."
			else:
				msg = "INTERNAL ERROR : User not registered..."
			user_loggedin = request.user.is_authenticated()
			if user_loggedin:
				extend_page = 'base_login.html'
			else:
				extend_page = 'base.html'
			db.close()
			return render(request, 'errorpage.html', {'error_msg': msg, 'extend_page' : extend_page})


def render_studenthome(request):
	try:
		db = MySQLdb.connect("localhost","root","@mysql12","PHYSICSGRIP")
		cursor = db.cursor()
	except Exception as e:
		print ">>> ERROR : ",e
		if settings.DEBUG :
			msg = "DATABASE ERROR : Connection not established..."
		else:
			msg = "INTERNAL ERROR : Connection not established..."
		user_loggedin = request.user.is_authenticated()
		if user_loggedin:
			extend_page = 'base_login.html'
		else:
			extend_page = 'base.html'
		return render(request, 'errorpage.html', {'error_msg': msg, 'extend_page' : extend_page})
	try:
		q1 = """ select * from STUDENTS where rollno = %d """ % (int(request.session['username']))
		cursor.execute(q1)
		print ">>> STUDENTs' details retrieved..."
		result = cursor.fetchone()
		#for i in result:
		#	print i, type(i)
		context = {}
		context['f_name'] = result[0]
		context['l_name'] = result[1]
		context['dob'] = result[2]
		context['Fa_name'] = result[3]
		context['Mo_name'] = result[4]
		context['Mob1'] = result[5]
		context['Mob2'] = result[6]
		context['pswd'] = result[7]
		context['town_vil'] = result[8]
		context['zip_code'] = result[9]
		context['addr'] = result[10]
		context['pathofdp'] = result[11]
		context['rollno'] = result[12]
		context['DUE'] = result[13]
		print ">>> 1"
		q2 = """ select course_id, section, reg_no from REGISTRATIONS where stud_roll = %d """ % (int(request.session['username']))
		cursor.execute(q2)
		stud_data = cursor.fetchone()
		print ">>> 1"
		print ">>> 2"
		q3 = """ select name from COURSES where courseID = %d """ % (stud_data[0])
		cursor.execute(q3)
		crs = cursor.fetchone()
		print ">>> 2"
		context['course'] = crs[0]
		print ">>> 3"
		q4 = """ select name from SECTION where sectionID = %d """ % (stud_data[1])
		cursor.execute(q4)
		sec = cursor.fetchone()
		print ">>> 3"
		context['section'] = sec[0]
		context['registration_no'] = stud_data[2]
		user_loggedin = request.user.is_authenticated()
		if user_loggedin:
			extend_page = 'base_login.html'
		else:
			extend_page = 'base.html'
		context['extend_page'] = extend_page
		db.close()
		return render(request, 'accounts/student_profile.html', context)
	except:
		if settings.DEBUG:
			msg = "DATABASE ERROR : Query not executed..."
		else:
			msg = "INTERNAL ERROR : Some problem Occured..."
		user_loggedin = request.user.is_authenticated()
		if user_loggedin:
			extend_page = 'base_login.html'
		else:
			extend_page = 'base.html'
		db.close()
		return render(request, 'errorpage.html', {'error_msg': msg, 'extend_page': extend_page})


def user_login(request):
	try:
		db = MySQLdb.connect("localhost","root","@mysql12","PHYSICSGRIP" )
		cursor = db.cursor()
	except Exception as e:
		print ">>> ERROR : ",e
		if settings.DEBUG :
			msg = "DATABASE ERROR : Connection not established..."
		else:
			msg = "INTERNAL ERROR : Connection not established..."
		user_loggedin = request.user.is_authenticated()
		if user_loggedin:
			extend_page = 'base_login.html'
		else:
			extend_page = 'base.html'
		return render(request, 'errorpage.html', {'error_msg': msg, 'extend_page' : extend_page})
	if request.method == 'POST':
		username = int((request.POST['user_name']).strip())
		password = request.POST['pswd']
		if not User.objects.get(username=username):
			user_loggedin = request.user.is_authenticated()
			if user_loggedin:
				extend_page = 'base_login.html'
			else:
				extend_page = 'base.html'
			db.close()
			return render(request, 'errorpage.html', {'error_msg' : "User does not exists...", 'extend_page' : extend_page})
		else:
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				print ">>> User logined..."
				print ">>> LOGIN USER",request.user
				request.session['username'] = username
				try:
					q1 = """ select * from STUDENTS where rollno = %d """%(int(request.session['username']))
					cursor.execute(q1)
					print ">>> STUDENTs' details retrieved..."
					result = cursor.fetchone()
					context = {}
					context['f_name'] = result[0]
					context['l_name'] = result[1]
					context['dob'] = result[2]
					context['Fa_name'] = result[3]
					context['Mo_name'] = result[4]
					context['Mob1'] = result[5]
					context['Mob2'] = result[6]
					context['pswd'] = result[7]
					context['town_vil'] = result[8]
					context['zip_code'] = result[9]
					context['addr'] = result[10]
					context['pathofdp'] = result[11]
					context['rollno'] = result[12]
					context['DUE'] = result[13]
					q2 = """ select course_id, section, reg_no from REGISTRATIONS where stud_roll = %d """%(int(username))
					cursor.execute(q2)
					stud_data = cursor.fetchone()
					q3 = """ select name from COURSES where courseID = %d """%(stud_data[0])
					cursor.execute(q3)
					crs = cursor.fetchone()
					context['course'] = crs[0]

					q4 = """ select name from SECTION where sectionID = %d """%(stud_data[1])
					cursor.execute(q4)
					sec = cursor.fetchone()
					context['section'] = sec[0]
					context['registration_no'] = stud_data[2]
					user_loggedin = request.user.is_authenticated()
					if user_loggedin:
						extend_page = 'base_login.html'
					else:
						extend_page = 'base.html'
					context['extend_page'] = extend_page
					db.close()
					return render(request, 'accounts/student_profile.html', context)
				except:
					if settings.DEBUG:
						msg = "DATABASE ERROR : User not registered..."
					else:
						msg = "INTERNAL ERROR : User not registered..."
					user_loggedin = request.user.is_authenticated()
					if user_loggedin:
						extend_page = 'base_login.html'
					else:
						extend_page = 'base.html'
					db.close()
					return render(request, 'errorpage.html', {'error_msg': msg, 'extend_page' : extend_page})
			else:
				user_loggedin = request.user.is_authenticated()
				if user_loggedin:
					extend_page = 'base_login.html'
				else:
					extend_page = 'base.html'
				db.close()
				return render(request, 'errorpage.html', {'error_msg' : "Password is incorrect..." , 'extend_page' : extend_page})
	user_loggedin = request.user.is_authenticated()
	if user_loggedin:
		extend_page = 'base_login.html'
	else:
		extend_page = 'base.html'
	db.close()
	return render(request, 'errorpage.html', {'error_msg': "Login from login window...", 'extend_page' : extend_page})

def render_schedule(request):
	pass


def user_logout(request):
	logout(request)
	user_loggedin = request.user.is_authenticated()
	if user_loggedin:
		extend_page = 'base_login.html'
	else:
		extend_page = 'base.html'
	return render(request, 'custom_page.html',{'title' : "SUCCESS", 'header': "LOGOUT", 'msg' : "LOGOUT SUCCESSFUL. SIGN IN FOR MORE...", 'extend_page' : extend_page})
