from django.db import models
from account.models import User

# Create your models here.


class Task(models.Model):
	title = models.CharField(max_length=200)
	complete = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True)
	employe = models.ForeignKey(User,blank=True,on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return self.title
