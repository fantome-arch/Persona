from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Entry
from .models import  User_Verification
from django.forms import ModelForm
from django.forms.widgets import DateTimeInput

class createaccount(UserCreationForm):
	first_name=forms.CharField(required=True,min_length=2)
	last_name=forms.CharField(required=True)
	def __init__(self,*args,**kwargs):
		super(createaccount,self).__init__(*args,**kwargs)
		self.fields['email'].required=True

	class Meta:
		model=User
		fields=['username','first_name','last_name','email']
		labels={'email':'E-mail','first_name':'First Name','last_name':'Last Name'}


class diaryform(ModelForm):

	def __init__(self,*args,**kwargs):
		super(diaryform,self).__init__(*args,**kwargs)
		self.fields['title' ].widget.attrs['class']='titlefield'
		self.fields['date'].widget.attrs['class']='datefield'



	class Meta:
		model=Entry
		fields=['title','date','content']
		widgets={

				'date':DateTimeInput(attrs={'type':'datetime-local','class':'datetime'})

		}

class verification_input(ModelForm):
	class Meta:
		model= User_Verification
		fields=['verification_code']


class forgotpassform(forms.Form):
	email=forms.EmailField(required=True)
	fields=['mail']
	

class password_reset_form1(forms.Form):
	verification_code=forms.IntegerField(required=True)
	new_password=forms.CharField(widget=forms.PasswordInput(),required=True,min_length=10)
	confirm_password=forms.CharField(widget=forms.PasswordInput(),required=True,min_length=10)
