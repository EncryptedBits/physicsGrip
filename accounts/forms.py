from django import forms

class studentForm(forms.Form):
	f_name = forms.CharField(max_length=30)
	l_name = forms.CharField(max_length=30)
	dob = forms.DateField()
	Fa_name = forms.CharField(max_length=40)
	Mo_name = forms.CharField(max_length=40)
	Mob1 = forms.IntegerField()
	Mob2 = forms.IntegerField(required=False)
	pswd1 = forms.CharField(widget=forms.PasswordInput())
	pswd2 = forms.CharField(widget=forms.PasswordInput())
	town_vil = forms.CharField(max_length=40)
	zip_code = forms.IntegerField()
	addr = forms.CharField(max_length=100)
	dp = forms.ImageField(required=False)