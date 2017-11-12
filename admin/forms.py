from django import forms

class galleryForm(forms.Form):
    title = forms.CharField(max_length=50)
    caption = forms.CharField(max_length=200)
    gallery_photo = forms.ImageField(required=True)

class ambForm(forms.Form):
    amb_name = forms.CharField(max_length=40)
    achievement = forms.CharField(max_length=60)
    amb_photo = forms.ImageField(required=False)
    amb_words = forms.CharField(max_length=1000)

class courseForm(forms.Form):
    c_name = forms.CharField(max_length=30)
    classs = forms.IntegerField()
    fee = forms.IntegerField()
    pre_req = forms.CharField(max_length=30)
    adm_beg = forms.DateField()
    adm_end = forms.DateField()
    c_beg = forms.DateField()
    c_end = forms.DateField()
    sub1 = forms.CharField(max_length=30, required=False)
    sub2 = forms.CharField(max_length=30, required=False)
    sub3 = forms.CharField(max_length=30, required=False)
    sub4 = forms.CharField(max_length=30, required=False)
    sub5 = forms.CharField(max_length=30, required=False)
    sub6 = forms.CharField(max_length=30, required=False)

class subjectForm(forms.Form):
    s_name = forms.CharField(max_length=50)
    no_of_lectures = forms.IntegerField()
    th_marks = forms.IntegerField()
    prac_marks = forms.IntegerField()
    no_of_midtests = forms.IntegerField()

class secForm(forms.Form):
    sec_name = forms.CharField(max_length=10)
    std = forms.CharField(max_length=10)
    curr_year = forms.CharField(max_length=10)



