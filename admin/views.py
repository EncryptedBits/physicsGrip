from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from .forms import galleryForm, ambForm, subjectForm, courseForm, secForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from time import strftime, localtime
import datetime
import MySQLdb

def save_image(img,folder,prefix):
	fs = FileSystemStorage()
	path_to_dp = folder+'/'+str(prefix)+str(datetime.datetime.now())
	filename = fs.save(path_to_dp, img)
	uploaded_file_url = fs.url(filename)
	return uploaded_file_url


def check_admin(user):
	return user.is_staff


def render_adminlogin(request):
	return render(request, 'admin/adminlogin.html', {})


def adminloginrequest(request):
	try:
		db = MySQLdb.connect("physicsgrip.mysql.pythonanywhere-services.com","physicsgrip","@mysql12","physicsgrip$default" )
		cursor = db.cursor()
	except Exception as e:
		print ">>> ERROR : ", e
		if settings.DEBUG:
			msg = "DATABASE ERROR : Connection not established..."
		else:
			msg = "INTERNAL ERROR : Connection not established..."
		return render(request, 'admin/errorpage.html', {'error_msg': msg})
	if request.method == 'POST':
		print request.POST
		username = request.POST['admin_name']
		password = request.POST['admin_pswd']
		print username, password
		usr = User.objects.get(username=username)
		if not usr or not usr.is_staff:
			db.close()
			return render(request, 'admin/errorpage.html', {'error_msg': "User does not exists..."})
		else:
			user = authenticate(username=username, password=password)
			if user is not None and user.is_staff:
				login(request, user)
				print ">>> User logined..."
				request.session['username'] = username
				db.close()
				return redirect('/admin/')
			else:
				return render(request, 'admin/errorpage.html', {'error_msg': "Password Incorrect..."})
	else:
		return render(request, 'admin/errorpage.html', {'error_msg': "Login from login page..."})

@user_passes_test(check_admin,login_url='/admin/login/')
def adminlogoutrequest(request):
	try:
		db = MySQLdb.connect("physicsgrip.mysql.pythonanywhere-services.com","physicsgrip","@mysql12","physicsgrip$default" )
		cursor = db.cursor()
	except Exception as e:
		print ">>> ERROR : ", e
		if settings.DEBUG:
			msg = "DATABASE ERROR : Connection not established..."
		else:
			msg = "INTERNAL ERROR : Connection not established..."

		return render(request, 'admin/errorpage.html', {'error_msg': msg})
	try:
		logout(request)
		del request.session['username']
		print ">>> ADMIN LOGOUT..."
		return render(request, 'custom_page.html', {'title': "SUCCESS", 'header': "LOGOUT", 'msg': "LOGOUT SUCCESSFUL. SIGN IN FOR MORE..."})
	except Exception as e:
		print ">>> ERROR :",e
		return render(request, 'admin/errorpage.html',{'error_msg': "LOGOUT UNSUCCESSFULL..."})


@user_passes_test(check_admin,login_url='/admin/login/')
def render_adminhome(request):
	try:
		db = MySQLdb.connect("physicsgrip.mysql.pythonanywhere-services.com","physicsgrip","@mysql12","physicsgrip$default" )
		cursor = db.cursor()
	except Exception as e:
		print ">>> ERROR : ",e
		if settings.DEBUG :
			msg = "DATABASE ERROR : Connection not established..."
		else:
			msg = "INTERNAL ERROR : Connection not established..."
		return render(request, 'admin/errorpage.html', {'error_msg': msg})
	try:
		context = {}
		q_c = """ SELECT COUNT(*) FROM COURSES """
		cursor.execute(q_c)
		no_of_courses = cursor.fetchone()[0]
		print ">>> COURSE DATA RETRIEVED"
		context['no_of_courses'] = no_of_courses

		q_s = " SELECT COUNT(*) FROM SECTION " 
		cursor.execute(q_s)
		no_of_sections = cursor.fetchone()[0]
		print ">>> SECTION DATA RETRIEVED"
		context['no_of_sections'] = no_of_sections

		q_stud = """ SELECT COUNT(*) FROM STUDENTS"""
		cursor.execute(q_stud)
		no_of_students = cursor.fetchone()[0]
		print ">>> STUDENTS DATA RETRIEVED"
		context['no_of_students'] = no_of_students

		q_due = """ SELECT SUM(DUE) FROM STUDENTS"""
		cursor.execute(q_due)
		total_due = cursor.fetchone()[0]
		print ">>> STUDENTS DATA RETRIEVED"
		context['total_due'] = total_due

		q_rcnt_reg = """SELECT s.f_name, s.l_name, s.rollno, s.pathofdp, r.course_id from STUDENTS AS s INNER JOIN REGISTRATIONS AS r ON s.rollno = r.stud_roll ORDER BY r.reg_date DESC, r.reg_time DESC LIMIT 20 """
		cursor.execute(q_rcnt_reg)
		reg_data = cursor.fetchall()
		print ">>> RECENT REGISTRATIONS DATA RETRIEVED"
		context['reg_data'] = reg_data

		q_due_reg = """ SELECT s.f_name, s.l_name, s.rollno, s.pathofdp, r.course_id from STUDENTS AS s INNER JOIN REGISTRATIONS AS r ON s.rollno = r.stud_roll WHERE s.DUE > 0 """
		cursor.execute(q_due_reg)
		due_data = cursor.fetchall()
		print ">>> DUE REGISTRATIONS DATA RETRIEVED"
		context['due_data'] = due_data
		#print context
		db.close()
		return render(request, 'admin/adminhome.html', context)
	except Exception as e:
		print ">>> ERROR : ",e
		if settings.DEBUG :
			msg = "DATABASE ERROR : Data not retrieved..."
		else:
			msg = "INTERNAL ERROR : Data not retrieved..."
		db.close()
		return render(request, 'admin/errorpage.html', {'error_msg': msg})

@user_passes_test(check_admin,login_url='/admin/login/')
def view_or_delete_due(request):
	print ">>> POST : ",request.POST
	try:
		db = MySQLdb.connect("physicsgrip.mysql.pythonanywhere-services.com","physicsgrip","@mysql12","physicsgrip$default" )
		cursor = db.cursor()
	except Exception as e:
		print ">>> ERROR : ",e
		if settings.DEBUG :
			msg = "DATABASE ERROR : Connection not established..."
		else:
			msg = "INTERNAL ERROR : Connection not established..."
		return render(request, 'admin/errorpage.html', {'error_msg': msg})
	if request.method == 'POST':
		print ">>> CHECK : ", str(request.POST['submt'])
		if str(request.POST.get('submt')) == str("delete") :
			print "Entered in 1st..."
			try:
				q_due_reg = """ SELECT rollno from STUDENTS WHERE DUE > 0 """
				cursor.execute(q_due_reg)
				due_studs = cursor.fetchall()
				due_studs_str = []
				for s in due_studs:
					due_studs_str.append(str(s[0]))
				roll_to_del = []
				for roll in due_studs_str:
					if request.POST.get(roll, None):
						roll_to_del.append(int(roll))
				if roll_to_del:
					for roll in roll_to_del:
						q = " UPDATE STUDENTS SET DUE = %d WHERE rollno = %d "%(0, int(roll))
						cursor.execute(q)
						print "DUE OF ROLL",roll," updated to 0."
					db.commit()
				print "redirected"
				db.close()
				return redirect('/admin/')
			except Exception as e:
				db.rollback()
				print ">>> ERROR : ",e
				msg = "DATABASE ERROR : Paid students not updated. Try again."
				db.close()
				return render(request, 'admin/errorpage.html', {'error_msg' : msg})

		else:
			print "2nd Entered"
			roll_to_display = int(request.POST.get('submt').split(':')[-1].strip())
			q1 = "select * from STUDENTS where rollno = %d "%(roll_to_display)
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
			q2 = " select course_id, section, reg_no from REGISTRATIONS where stud_roll = %d " %(roll_to_display)
			cursor.execute(q2)
			stud_data = cursor.fetchone()
			context['course_id'] = stud_data[0]
			context['section_id'] = stud_data[1]
			context['registration_no'] = stud_data[2]
			q3 =  "select name from COURSES where courseID = %d" %(stud_data[0])
			cursor.execute(q3)
			crs = cursor.fetchone()
			context['course'] = crs[0]
			context['extend_page'] = 'admin/base.html'

			q4 =  "select name from SECTION where sectionID = %d" %(stud_data[1])
			cursor.execute(q4)
			sec = cursor.fetchone()
			context['section'] = sec[0]
			db.close()
			return render(request, 'accounts/student_profile.html', context)

@user_passes_test(check_admin,login_url='/admin/login/')
def courses_render(request):
	try:
		db = MySQLdb.connect("physicsgrip.mysql.pythonanywhere-services.com","physicsgrip","@mysql12","physicsgrip$default" )
		cursor = db.cursor()
	except Exception as e:
		print ">>> ERROR : ",e
		if settings.DEBUG :
			msg = "DATABASE ERROR : Connection not established..."
		else:
			msg = "INTERNAL ERROR : Connection not established..."
		return render(request, 'admin/errorpage.html', {'error_msg': msg})
	try:
		q = """ SELECT name, fee, no_of_stud, pre_req, course_beg, course_end,
		 admsn_beg, admsn_end, curr_addm_sec, courseID, class FROM COURSES """
		cursor.execute(q)
		course_data = cursor.fetchall()
		course_ids = []
		for c in course_data:
			course_ids.append(c[9])
		sections_for_each_course = []
		for c_id in course_ids:
			qq = """ SELECT sectionID, name FROM SECTION WHERE course = %d """%(c_id)
			cursor.execute(qq)
			sections_for_each_course.append(cursor.fetchall())
		course_sec = zip(course_data, sections_for_each_course)
		#q3 = "select name from SECTION where sectionID = %d"%()
		q2 = """ SELECT subjectID, name FROM SUBJECTS """
		cursor.execute(q2)
		subjects = cursor.fetchall()
		db.close()
		return render(request, 'admin/createcourse.html', {'course_sec' : course_sec, 'subjects' : subjects, 'sec':sections_for_each_course})
	except Exception as e:
		print ">>> ERROR : ", e
		if settings.DEBUG:
			msg = "DATABASE ERROR : COURSES DATA NOT RETRIEVED..."
		else:
			msg = "INTERNAL ERROR : COURSES DATA NOT FOUND..."
		db.close()
		return render(request, 'admin/errorpage.html', {'error_msg': msg})

@user_passes_test(check_admin,login_url='/admin/login/')
def create_course(request):
	try:
		db = MySQLdb.connect("physicsgrip.mysql.pythonanywhere-services.com","physicsgrip","@mysql12","physicsgrip$default" )
		cursor = db.cursor()
	except Exception as e:
		print ">>> ERROR : ",e
		if settings.DEBUG :
			msg = "DATABASE ERROR : Connection not established..."
		else:
			msg = "INTERNAL ERROR : Connection not established..."
		return render(request, 'admin/errorpage.html', {'error_msg': msg})
	if request.method == 'POST':
		course_form = courseForm(request.POST)
		if course_form.is_valid():
			c_name = course_form.cleaned_data['c_name']
			classs = course_form.cleaned_data['classs']
			fee = course_form.cleaned_data['fee']
			pre_req = course_form.cleaned_data['pre_req']
			adm_beg = course_form.cleaned_data['adm_beg']
			adm_end = course_form.cleaned_data['adm_end']
			c_beg = course_form.cleaned_data['c_beg']
			c_end = course_form.cleaned_data['c_end']
			sub1 = course_form.cleaned_data.get('sub1', None)
			sub2 = course_form.cleaned_data.get('sub2', None)
			sub3 = course_form.cleaned_data.get('sub3', None)
			sub4 = course_form.cleaned_data.get('sub4', None)
			sub5 = course_form.cleaned_data.get('sub5', None)
			sub6 = course_form.cleaned_data.get('sub6', None)

			try:
				q = """ INSERT INTO COURSES(name,fee,no_of_stud,pre_req,course_beg,course_end,
				admsn_beg, admsn_end, class) VALUES ('%s', %d, %d, '%s','%s','%s','%s','%s', %d) 
				"""%(c_name, fee,0, pre_req,c_beg, c_end,adm_beg, adm_end, classs)
				cursor.execute(q)
				print "passed"
				q1 = """ SELECT courseID from COURSES WHERE name = '%s' """%(c_name)
				cursor.execute(q1)
				c_id = cursor.fetchone()[0]
				if sub1 != 'not_selected':
					q0 = """ INSERT INTO COURSE_SUBJECT VALUES (%d, %d) """%(c_id, int(sub1))
					cursor.execute(q0)
				if sub2 != 'not_selected':
					q0 = """ INSERT INTO COURSE_SUBJECT VALUES (%d, %d) """%(c_id, int(sub2))
					cursor.execute(q0)
				if sub3 != 'not_selected':
					q0 = """ INSERT INTO COURSE_SUBJECT VALUES (%d, %d) """%(c_id, int(sub3))
					cursor.execute(q0)
				if sub4 != 'not_selected':
					q0 = """ INSERT INTO COURSE_SUBJECT VALUES (%d, %d) """%(c_id, int(sub4))
					cursor.execute(q0)
				if sub5 != 'not_selected':
					q0 = """ INSERT INTO COURSE_SUBJECT VALUES (%d, %d) """%(c_id, int(sub5))
					cursor.execute(q0)
				if sub6 != 'not_selected':
					q0 = """ INSERT INTO COURSE_SUBJECT VALUES (%d, %d) """%(c_id, int(sub6))
					cursor.execute(q0)
				db.commit()
				db.close()
				return redirect('/admin/course/')
				#return render(request, 'custom_page.html', {'header': "SUCCESS", 'msg' : "COURSE CREATED SUCCESSFULLY"})
			except Exception as e:
				print ">>> ERROR", e
				db.rollback()
				if settings.DEBUG:
					msg = "DATABASE ERROR : COURSE NOT CREATED PROPERLY..."
				else:
					msg = "INTERNAL ERROR : COURSE NOT CREATED PROPERLY..."
				db.close()
				return render(request, 'admin/errorpage.html', {'error_msg': msg})
		else:
			msg = "INPUT DATA IS INVALID..."
			db.close()
			return render(request, 'admin/errorpage.html', {'error_msg' : msg})
	else:
		msg = "PROCEED PROPERLY USING GIVEN LINKS, NOT BY ENTERING URLS..."
		db.close()
		return render(request, 'admin/errorpage.html', {'error_msg': msg})

@user_passes_test(check_admin,login_url='/admin/login/')
def process_course(request):
	try:
		db = MySQLdb.connect("physicsgrip.mysql.pythonanywhere-services.com","physicsgrip","@mysql12","physicsgrip$default" )
		cursor = db.cursor()
	except Exception as e:
		print ">>> ERROR : ", e
		if settings.DEBUG:
			msg = "DATABASE ERROR : Connection not established..."
		else:
			msg = "INTERNAL ERROR : Connection not established..."
		return render(request, 'admin/errorpage.html', {'error_msg': msg})
	if request.method == 'POST':
		print request.POST
		if request.POST.get('submit1', None):
			new_curr_sec = int(request.POST['new_curr_sec'])
			curr_course = int(request.POST['submit1'])
			try:
				q = """ UPDATE COURSES SET curr_addm_sec = %d where courseID = %d """%(new_curr_sec, curr_course)
				cursor.execute(q)
				db.commit()
				db.close()
				return redirect('/admin/course/')
			except Exception as e:
				db.rollback()
				print ">>> ERROR",e
				if settings.DEBUG:
					msg = "DATABASE ERROR : CURR SECTION NOT UPDATED..."
				else:
					msg = "INTERNAL ERROR : CURR SECTION NOT UPDATED..."
				db.close()
				return render(request, 'admin/errorpage.html', {'error_msg': msg})
		elif request.POST.get('submit2', None) :
			curr_course = int(request.POST['submit2'])
			print ">>> CURR COURSE",curr_course
			try:
				q = """ DELETE FROM COURSES where courseID = %d """%(curr_course)
				cursor.execute(q)
				db.commit()
				return redirect('/admin/course/')
			except Exception as e:
				db.rollback()
				print ">>> ERROR",e
				if settings.DEBUG:
					msg = "DATABASE ERROR : COURSE NOT DELETED..."
				else:
					msg = "INTERNAL ERROR : COURSE NOT DELETED..."
				db.close()
				return render(request, 'admin/errorpage.html', {'error_msg': msg})
		elif request.POST.get('submit3', None) :
			curr_course = int(request.POST['submit3'])
			try:
				q = """ SELECT * FROM SECTION WHERE course = %d """%(curr_course)
				cursor.execute(q)
				sec_data = cursor.fetchall()
				course = int(request.POST['submit3'])
				db.close()
				return render(request, 'admin/createsection.html', {'sec_data': sec_data, 'course':course})
			except Exception as e:
				db.rollback()
				print ">>> ERROR",e
				if settings.DEBUG:
					msg = "DATABASE ERROR : SECTION NOT RETRIEVED..."
				else:
					msg = "INTERNAL ERROR : SECTION NOT RETRIEVED..."
				db.close()
				return render(request, 'admin/errorpage.html', {'error_msg': msg})

@user_passes_test(check_admin,login_url='/admin/login/')
def gallery_render(request):
	return render(request, 'admin/uploadgallery.html', {})

@user_passes_test(check_admin,login_url='/admin/login/')
def upload_gallery(request):
	try:
		db = MySQLdb.connect("physicsgrip.mysql.pythonanywhere-services.com","physicsgrip","@mysql12","physicsgrip$default" )
		cursor = db.cursor()
	except Exception as e:
		print ">>> ERROR : ",e
		if settings.DEBUG :
			msg = "DATABASE ERROR : Connection not established..."
		else:
			msg = "INTERNAL ERROR : Connection not established..."
		return render(request, 'admin/errorpage.html', {'error_msg': msg})

	if request.method == 'POST' :
		gallery_form = galleryForm(request.POST, request.FILES)
		if gallery_form.is_valid():
			try:
				title = gallery_form.cleaned_data['title']
				caption = gallery_form.cleaned_data['caption']
				gallery_photo = gallery_form.cleaned_data['gallery_photo']
				image_url = save_image(gallery_photo,"gallery_pic","gallery_")
				q = """ INSERT INTO GALLERY VALUES (NULL, '%s', '%s', '%s', '%s')
				 """ %(title, strftime('%Y:%m:%d', localtime()), image_url, caption)
				cursor.execute(q)
				db.commit()
				db.close()
				return render(request, 'admin/custom_page.html',{'header': "SUCCESS" ,'msg': "PHOTO SUCCESSFULLY UPLOADED..."})
			except Exception as e:
				print ">>> ERROR : ", e
				if settings.DEBUG:
					msg = "DATABASE ERROR : GALLERY PHOTO NOT UPLOADED..."
				else:
					msg = "INTERNAL ERROR : GALLERY PHOTO NOT UPLOADED..."
				db.close()
				return render(request, 'admin/errorpage.html', {'error_msg': msg})
		else:
			db.close()
			return render(request, 'admin/errorpage.html',{'error_msg': "The entered data is invalid..."})


@user_passes_test(check_admin,login_url='/admin/login/')
def ambassadors_render(request):
	return render(request, 'admin/uploadamb.html',{})

@user_passes_test(check_admin,login_url='/admin/login/')
def upload_ambassadors(request):
	try:
		db = MySQLdb.connect("physicsgrip.mysql.pythonanywhere-services.com","physicsgrip","@mysql12","physicsgrip$default" )
		cursor = db.cursor()
	except Exception as e:
		print ">>> ERROR : ",e
		if settings.DEBUG :
			msg = "DATABASE ERROR : Connection not established..."
		else:
			msg = "INTERNAL ERROR : Connection not established..."
		return render(request, 'admin/errorpage.html', {'error_msg': msg})

	if request.method == 'POST' :
		amb_form = ambForm(request.POST, request.FILES)
		if amb_form.is_valid():
			try:
				amb_name = amb_form.cleaned_data['amb_name']
				achievement = amb_form.cleaned_data['achievement']
				amb_photo = amb_form.cleaned_data['amb_photo']
				amb_words = amb_form.cleaned_data['amb_words']
				image_url = save_image(amb_photo,"amb_pic","amb_")
				q = """ INSERT INTO AMBASSADORS VALUES (NULL, '%s', '%s', '%s', '%s')
				 """ %(amb_name, achievement, amb_words, image_url)
				cursor.execute(q)
				db.commit()
				db.close()
				return render(request, 'admin/custom_page.html',{'header': "SUCCESS" ,'msg': "AMBASSADOR SUCCESSFULLY UPLOADED..."})
			except Exception as e:
				print ">>> ERROR : ", e
				if settings.DEBUG:
					msg = "DATABASE ERROR : AMBASSADOR NOT UPLOADED..."
				else:
					msg = "INTERNAL ERROR : AMBASSADOR NOT UPLOADED..."
				db.close()
				return render(request, 'admin/errorpage.html', {'error_msg': msg})
		else:
			db.close()
			return render(request, 'admin/errorpage.html',{'error_msg': "The entered data is invalid..."})

@user_passes_test(check_admin,login_url='/admin/login/')
def subject_render(request):
	try:
		db = MySQLdb.connect("physicsgrip.mysql.pythonanywhere-services.com","physicsgrip","@mysql12","physicsgrip$default" )
		cursor = db.cursor()
	except Exception as e:
		print ">>> ERROR : ",e
		if settings.DEBUG :
			msg = "DATABASE ERROR : Connection not established..."
		else:
			msg = "INTERNAL ERROR : Connection not established..."
		return render(request, 'admin/errorpage.html', {'error_msg': msg})
	try:
		q = """ SELECT * FROM SUBJECTS """
		cursor.execute(q)
		subject_data = cursor.fetchall()
		db.close()
		return render(request, 'admin/createsubject.html', {'subject_data' : subject_data })
	except Exception as e:
		print ">>> ERROR : ", e
		if settings.DEBUG:
			msg = "DATABASE ERROR : SUBJECTS DATA NOT RETRIEVED..."
		else:
			msg = "INTERNAL ERROR : SUBJECTS DATA NOT FOUND..."
		db.close()
		return render(request, 'admin/errorpage.html', {'error_msg': msg})

@user_passes_test(check_admin,login_url='/admin/login/')
def create_subject(request):
	try:
		db = MySQLdb.connect("physicsgrip.mysql.pythonanywhere-services.com","physicsgrip","@mysql12","physicsgrip$default" )
		cursor = db.cursor()
	except Exception as e:
		print ">>> ERROR : ",e
		if settings.DEBUG :
			msg = "DATABASE ERROR : Connection not established..."
		else:
			msg = "INTERNAL ERROR : Connection not established..."
		return render(request, 'admin/errorpage.html', {'error_msg': msg})
	if request.method == 'POST':
		if request.POST.get('add',None):
			sub_form = subjectForm(request.POST)
			if sub_form.is_valid():
				s_name = sub_form.cleaned_data['s_name']
				no_of_lectures = sub_form.cleaned_data['no_of_lectures']
				th_marks = sub_form.cleaned_data['th_marks']
				prac_marks = sub_form.cleaned_data['prac_marks']
				no_of_midtests = sub_form.cleaned_data['no_of_midtests']
				try:
					q = """ INSERT INTO SUBJECTS VALUES (NULL, '%s', %d, %d, %d, %d, %d) """%(s_name, no_of_lectures,th_marks,prac_marks,0, no_of_midtests)
					cursor.execute(q)
					db.commit()
					db.close()
					#return render(request, 'custom_page.html', {'header': "SUCCESS", 'msg' : "SUBJECT CREATED SUCCESSFULLY"})
					return redirect('/admin/subject/')
				except Exception as e:
					print ">>> ERROR", e
					db.rollback()
					if settings.DEBUG:
						msg = "DATABASE ERROR : SUBJECT NOT CREATED..."
					else:
						msg = "INTERNAL ERROR : SUBJECT NOT CREATED..."
					db.close()
					return render(request, 'admin/errorpage.html', {'error_msg': msg})

			else:
				msg = "INPUT DATA IS INVALID..."
				db.close()
				return render(request, 'admin/errorpage.html', {'error_msg' : msg})
		else:
			try:
				print ">>> ---",request.POST.get('delete')
				sub_id = int(request.POST.get('delete'))
				print "subid",sub_id
				q2 = """ DELETE FROM SUBJECTS WHERE subjectID = %d """%(sub_id)
				print "delete query executed..."
				cursor.execute(q2)
				db.commit()
				db.close()
				return render(request, 'admin/custom_page.html',{'heading' : "SUCCESS", 'msg' : "SUBJECT DELETED SUCCESSFULLY"})
			except Exception as e:
				db.rollback()
				print ">>> ERROR",e
				if settings.DEBUG:
					msg = "DATABASE ERROR : SUBJECTS NOT DELETED..."
				else:
					msg = "INTERNAL ERROR : SUBJECTS NOT DELETED..."
				db.close()
				return render(request, 'admin/errorpage.html', {'error_msg': msg})
	else:
		msg = "PROCEED PROPERLY USING GIVEN LINKS, NOT BY ENTERING URLS..."
		db.close()
		return render(request, 'admin/errorpage.html', {'error_msg': msg})


@user_passes_test(check_admin,login_url='/admin/login/')
def sections_render(request):
	return render(request, 'admin/createsection.html',{})

@user_passes_test(check_admin,login_url='/admin/login/')
def process_section(request):
	try:
		db = MySQLdb.connect("physicsgrip.mysql.pythonanywhere-services.com","physicsgrip","@mysql12","physicsgrip$default" )
		cursor = db.cursor()
	except Exception as e:
		print ">>> ERROR : ", e
		if settings.DEBUG:
			msg = "DATABASE ERROR : Connection not established..."
		else:
			msg = "INTERNAL ERROR : Connection not established..."
		return render(request, 'admin/errorpage.html', {'error_msg': msg})
	if request.method == 'POST':
		print ">>> SECTION", request.POST
		if request.POST.get('add',None):
			new_sec = secForm(request.POST)
			if new_sec.is_valid():
				sec_name = new_sec.cleaned_data['sec_name']
				std = new_sec.cleaned_data['std']
				curr_year = new_sec.cleaned_data['curr_year']
				course = int(request.POST['add'])
				try:
					q = """ INSERT INTO SECTION(name, class, current_year, no_of_stud, course) VALUES( '%s', '%s', '%s', %d , %d)
					 """%(sec_name,std, curr_year, 0, course )
					cursor.execute(q)
					db.commit()
					db.close()
					return render(request, 'admin/custom_page.html', {'header':"SUCCESS", 'msg':"SECTION SUCCESSFULLY ADDED..."})
				except Exception as e:
					db.rollback()
					print ">>> ERROR", e
					if settings.DEBUG:
						msg = "DATABASE ERROR : SECTION NOT ADDED..."
					else:
						msg = "INTERNAL ERROR : SECTION NOT ADDED..."
					db.close()
					return render(request, 'admin/errorpage.html', {'error_msg': msg})
			else:
				if settings.DEBUG:
					msg = "ERROR : INVALID DATA..."
				else:
					msg = "ERROR : INVALID DATA..."
				db.close()
				return render(request, 'admin/errorpage.html', {'error_msg': msg})
		else:
			s_c = request.POST['delete']
			sid, cid = map(int, s_c.split('-'))
			try:
				q = """ DELETE FROM SECTION WHERE course = %d AND sectionID = %d """%(cid, sid)
				cursor.execute(q)
				db.commit()
				db.close()
				return render(request, 'admin/custom_page.html', {'header': "SUCCESS", 'msg': "SUCCESSFULLY DELETED..."})
			except Exception as e:
				db.rollback()
				print  e
				if settings.DEBUG:
					msg = "DATABASE ERROR : SECTION NOT DELETED..."
				else:
					msg = "INTERNAL ERROR : SECTION NOT DELETED..."
				db.close()
				return render(request, 'admin/errorpage.html', {'error_msg': msg})

def search_render(request):
	return render(request, 'admin/search.html',{})

def return_courses(request):
	try:
		db = MySQLdb.connect("physicsgrip.mysql.pythonanywhere-services.com","physicsgrip","@mysql12","physicsgrip$default" )
		cursor = db.cursor()
	except Exception as e:
		print ">>> ERROR : ", e
		if settings.DEBUG:
			msg = "DATABASE ERROR : Connection not established..."
		else:
			msg = "INTERNAL ERROR : Connection not established..."
		return render(request, 'admin/errorpage.html', {'error_msg': msg})
	std = request.POST.get('class', None)
	print "CLASS: ",std
	if int(std) != 0:
		q = " SELECT courseID, name FROM COURSES WHERE class = %d"%(int(std))
		cursor.execute(q)
		data = {}
		for section in cursor.fetchall():
			data[str(section[0])] = section[1]
		db.close()
		return JsonResponse(data)
	else:
		return HttpResponse("Class not selected")




def return_sections(request):
	try:
		db = MySQLdb.connect("physicsgrip.mysql.pythonanywhere-services.com","physicsgrip","@mysql12","physicsgrip$default" )
		cursor = db.cursor()
	except Exception as e:
		print ">>> ERROR : ", e
		if settings.DEBUG:
			msg = "DATABASE ERROR : Connection not established..."
		else:
			msg = "INTERNAL ERROR : Connection not established..."
		return render(request, 'admin/errorpage.html', {'error_msg': msg})
	course = request.POST.get('course', None)
	print "COURSE: ",course
	if int(course) != 0:
		q = " SELECT sectionID, name FROM SECTION WHERE course = %d"%(int(course))
		cursor.execute(q)
		data = {}
		for section in cursor.fetchall():
			data[str(section[0])] = section[1]
		db.close()
		return JsonResponse(data)
	else:
		return HttpResponse("Class not selected")



def search_result(request):
	try:
		db = MySQLdb.connect("physicsgrip.mysql.pythonanywhere-services.com","physicsgrip","@mysql12","physicsgrip$default" )
		cursor = db.cursor()
	except Exception as e:
		print ">>> ERROR : ", e
		if settings.DEBUG:
			msg = "DATABASE ERROR : Connection not established..."
		else:
			msg = "INTERNAL ERROR : Connection not established..."
		return render(request, 'admin/errorpage.html', {'error_msg': msg})

	classs = request.POST.get('class', None)
	course = request.POST.get('course', None)
	section = request.POST.get('section', None)
	due = request.POST.get('due', None)
	q = """ SELECT  """
	if int(classs) != 0:
		q = " SELECT sectionID, name FROM SECTION WHERE course = %d"%(int(course))
		cursor.execute(q)
		data = {}
		for section in cursor.fetchall():
			data[str(section[0])] = section[1]
		db.close()
		return JsonResponse(data)



def searchbyname_result(request):
	try:
		db = MySQLdb.connect("physicsgrip.mysql.pythonanywhere-services.com","physicsgrip","@mysql12","physicsgrip$default" )
		cursor = db.cursor()
	except Exception as e:
		print ">>> ERROR : ", e
		if settings.DEBUG:
			msg = "DATABASE ERROR : Connection not established..."
		else:
			msg = "INTERNAL ERROR : Connection not established..."
		return render(request, 'admin/errorpage.html', {'error_msg': msg})

	qname = request.POST.get('search_name', None)
	q = """ SELECT s.f_name, s.l_name, s.rollno, s.pathofdp, r.course_id from STUDENTS AS s INNER JOIN REGISTRATIONS AS r ON s.rollno = r.stud_roll WHERE s.f_name LIKE '%s%s%s' OR s.l_name LIKE '%s%s%s'  """%("%",qname,"%","%",qname,"%")
	try:
		cursor.execute(q)
		students = cursor.fetchall()
		context = {}
		context['students'] = students
		context['name'] = qname
		context['total'] = len(students)
		db.close()
		return render(request, 'admin/search.html', context)
	except Exception as e:
		print ">>> ERROR",e
		db.close()
		if settings.DEBUG:
			msg = "DATABASE ERROR : Students retrieval problem..."
		else:
			msg = "INTERNAL ERROR : Students retrieval problem..."
		return render(request, 'admin/errorpage.html', {'error_msg': msg})

@user_passes_test(check_admin,login_url='/admin/login/')
def view_or_delete_student(request):
	print ">>> POST : ",request.POST
	try:
		db = MySQLdb.connect("physicsgrip.mysql.pythonanywhere-services.com","physicsgrip","@mysql12","physicsgrip$default" )
		cursor = db.cursor()
	except Exception as e:
		print ">>> ERROR : ",e
		if settings.DEBUG :
			msg = "DATABASE ERROR : Connection not established..."
		else:
			msg = "INTERNAL ERROR : Connection not established..."
		return render(request, 'admin/errorpage.html', {'error_msg': msg})
	if request.method == 'POST':
		print ">>> CHECK : ", str(request.POST['submt'])
		if str(request.POST.get('submt')) == str("delete") :
			print "Entered in 1st..."
			try:
				q_due_reg = """ SELECT rollno from STUDENTS """
				cursor.execute(q_due_reg)
				due_studs = cursor.fetchall()
				due_studs_str = []
				for s in due_studs:
					due_studs_str.append(str(s[0]))
				roll_to_del = []
				for roll in due_studs_str:
					if request.POST.get(roll, None):
						roll_to_del.append(int(roll))
				if roll_to_del:
					for roll in roll_to_del:
						q = " DELETE FROM STUDENTS WHERE rollno = %d "%(int(roll))
						cursor.execute(q)
					db.commit()
				print "redirected"
				db.close()
				return render(request, 'admin/custom_page.html', {'header' : "SUCCESS", 'msg' : "SUCCESSFULLY DELETED"})
			except Exception as e:
				db.rollback()
				print ">>> ERROR : ",e
				msg = "DATABASE ERROR : Students not deleted. Try again."
				db.close()
				return render(request, 'admin/errorpage.html', {'error_msg' : msg})

		else:
			print "2nd Entered"
			roll_to_display = int(request.POST.get('submt').split(':')[-1].strip())
			q1 = "select * from STUDENTS where rollno = %d "%(roll_to_display)
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
			q2 = " select course_id, section, reg_no from REGISTRATIONS where stud_roll = %d " %(roll_to_display)
			cursor.execute(q2)
			stud_data = cursor.fetchone()
			context['course_id'] = stud_data[0]
			context['section_id'] = stud_data[1]
			context['registration_no'] = stud_data[2]
			q3 =  "select name from COURSES where courseID = %d" %(stud_data[0])
			cursor.execute(q3)
			crs = cursor.fetchone()
			context['course'] = crs[0]
			context['extend_page'] = 'admin/base.html'

			q4 =  "select name from SECTION where sectionID = %d" %(stud_data[1])
			cursor.execute(q4)
			sec = cursor.fetchone()
			context['section'] = sec[0]
			db.close()
			return render(request, 'accounts/student_profile.html', context)
