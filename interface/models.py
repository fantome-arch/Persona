from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor.fields import RichTextField

class Entry(models.Model):
	title=models.CharField(max_length=100)
	content=RichTextField(blank=True,null=True)
	date=models.DateTimeField(default=timezone.now)
	user=models.ForeignKey(User,on_delete=models.CASCADE)


class User_Verification(models.Model):
	user=models.ForeignKey(User,unique=True,on_delete=models.CASCADE)
	date_time=models.DateTimeField(auto_now=True)
	verification_code=models.IntegerField(max_length=6)
	is_verified=models.BooleanField(default=False)
