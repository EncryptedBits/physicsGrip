create table STUDENTS (
	f_name VARCHAR(30) NOT NULL,
	l_name VARCHAR(30),
	dob DATE NOT NULL,
	Fa_name VARCHAR(40) NOT NULL,
	Mo_name VARCHAR(40) NOT NULL,
	Mob1 VARCHAR(10) NOT NULL,
	Mob2 VARCHAR(10) ,
	pswd VARCHAR(64) NOT NULL,
	town_vil VARCHAR(40) NOT NULL,
	zip_code VARCHAR(10) NOT NULL,
	addr VARCHAR(100) NOT NULL,
	pathofdp VARCHAR(200),
	rollno INT NOT NULL AUTO_INCREMENT,
	DUE INT DEFAULT -500,
	PRIMARY KEY (rollno)
);

create table COURSES (
	courseID INT NOT NULL AUTO_INCREMENT,
	name VARCHAR(30) NOT NULL,
	fee INT,
	no_of_stud INT,
	pre_req VARCHAR(20),
	course_beg DATE,
	course_end DATE,
	admsn_beg DATE,
	admsn_end DATE,
	curr_addm_sec INT DEFAULT 1,
	class INT NOT NULL,
	FOREIGN KEY (curr_addm_sec) REFERENCES SECTION(sectionID) ON DELETE SET NULL ON UPDATE CASCADE,
	PRIMARY KEY (courseID)
);

create table SCHEDULE(
    scheduleID INT NOT NULL AUTO_INCREMENT,
    mon_beg VARCHAR(20),
    mon_end VARCHAR(20),
    tue_beg VARCHAR(20),
    tue_end VARCHAR(20),
    wed_beg VARCHAR(20),
    wed_end VARCHAR(20),
    thu_beg VARCHAR(20),
    thu_end VARCHAR(20),
    fri_beg VARCHAR(20),
    fri_end VARCHAR(20),
    sat_beg VARCHAR(20),
    sat_end VARCHAR(20),
    PRIMARY KEY (scheduleID)
);

create table SECTION(
	sectionID INT NOT NULL AUTO_INCREMENT,
	name VARCHAR(20),
	class VARCHAR(15),
	current_year VARCHAR(20),
	no_of_stud INT,
	course INT,
	schedule INT,
	FOREIGN KEY	(schedule) REFERENCES SCHEDULE (scheduleID) ON DELETE SET NULL,
	FOREIGN KEY	(course) REFERENCES COURSES (courseID) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (sectionID, course)
);

create table REGISTRATIONS (
	reg_no INT NOT NULL AUTO_INCREMENT,
	reg_date DATE NOT NULL,
	reg_time TIME,
	stud_roll INT,
	course_id INT,
	section INT,
	FOREIGN KEY (section) REFERENCES SECTION(sectionID) ON DELETE SET NULL ON UPDATE CASCADE,
	FOREIGN KEY (stud_roll) REFERENCES STUDENTS(rollno)  ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (course_id) REFERENCES COURSES(courseID)  ON DELETE SET NULL ON UPDATE CASCADE,
	PRIMARY KEY (reg_no)
);

create table SUBJECTS (
	subjectID INT NOT NULL AUTO_INCREMENT,
	name VARCHAR(30) NOT NULL,
	no_of_lectures INT,
	theory_marks INT,
	prac_marks INT,
	no_of_stud INT,
	no_of_midtests INT,
	PRIMARY KEY	(subjectID)
);


create table TRANSACTIONS (
	transactionID INT NOT NULL AUTO_INCREMENT,
	trans_date DATE,
	tran_time TIME,
	amount DECIMAL(7,2),
	bank_name VARCHAR(30),
	account_no VARCHAR(15),
	studID INT,
	PRIMARY KEY (transactionID),
	FOREIGN KEY (studID) REFERENCES STUDENTS (rollno) ON DELETE SET NULL ON UPDATE CASCADE
);

create table INSTRUCTORS (
	instructorID INT NOT NULL AUTO_INCREMENT,
	name VARCHAR(30),
	dob DATE,
	age INT,
	Mob VARCHAR(10),
	salary INT,
	account_no VARCHAR(15),
	ifsc_code VARCHAR(15),
	addr VARCHAR(100),
	pin_code INT,
	subject INT,
	PRIMARY KEY (instructorID),
	FOREIGN KEY (subject) REFERENCES SUBJECTS(subjectID) ON DELETE SET NULL ON UPDATE CASCADE
);


create table COURSE_SUBJECT(
	course_id INT,
	subject_id INT,
	PRIMARY KEY (course_id, subject_id),
	FOREIGN KEY (course_id) REFERENCES COURSES (courseID) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (subject_id) REFERENCES SUBJECTS (subjectID) ON DELETE CASCADE ON UPDATE CASCADE
);

create table GALLERY(
	imageID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
	title VARCHAR(25) NOT NULL,
	upload_date DATE NOT NULL,
	pathofimage VARCHAR(200) NOT NULL,
	caption VARCHAR(100)
);

create table AMBASSADORS(
	amb_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(30) NOT NULL,
	achievement VARCHAR(50) NOT NULL,
	description VARCHAR(1000),
	pathofimage varchar(200)
);

create table AUX_STUDENTS (
	aux_id INT NOT NULL AUTO_INCREMENT,
	f_name VARCHAR(30) NOT NULL,
	l_name VARCHAR(30),
	dob DATE NOT NULL,
	Fa_name VARCHAR(40) NOT NULL,
	Mo_name VARCHAR(40) NOT NULL,
	Mob1 VARCHAR(10) NOT NULL,
	Mob2 VARCHAR(10) ,
	pswd VARCHAR(64) NOT NULL,
	town_vil VARCHAR(40) NOT NULL,
	zip_code VARCHAR(10) NOT NULL,
	addr VARCHAR(100) NOT NULL,
	pathofdp VARCHAR(200),
	adding_time TIME NOT NULL,
	adding_date DATE NOT NULL,
	PRIMARY KEY (aux_id)
);

ALTER TABLE STUDENTS AUTO_INCREMENT = 1001;
ALTER TABLE COURSES AUTO_INCREMENT = 101;
ALTER TABLE REGISTRATIONS AUTO_INCREMENT = 100001;
ALTER TABLE SUBJECTS AUTO_INCREMENT = 11;
ALTER TABLE TRANSACTIONS AUTO_INCREMENT = 1000001;


#subjects, no. of lectures in course

