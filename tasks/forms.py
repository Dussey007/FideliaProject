from django import forms
from django.forms import ModelForm


from .models import *




class TaskForm(ModelForm):
    title= forms.CharField(widget= forms.TextInput(attrs={"class":"form-control"}))
	
    class Meta:
        model = Task
        fields = ('title','complete')
        # fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        return super(TaskForm, self).__init__(*args, **kwargs)


    def save(self, *args, **kwargs):
       kwargs['commit']=False
       obj = super(TaskForm, self).save(*args, **kwargs)
       if self.request:
           obj.employe = self.request.user
       obj.save()
       return obj
