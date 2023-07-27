from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import *
from .forms import *

# Create your views here.

def index(request):
	tasks = Task.objects.filter( employe_id = request.user.pk).all()

	form = TaskForm()

	if request.method =='POST':
		form = TaskForm(request.POST)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.employe = request.user
			obj.save()
		return redirect('lisT')


	context = {'tasks':tasks, 'form':form}
	return render(request, 'tasks/list.html', context)

def updateTask(request, pk):
	task = Task.objects.filter( employe_id = request.user.pk).get(id=pk)

	form = TaskForm(instance=task)

	if request.method == 'POST':
		form = TaskForm(request.POST, instance=task)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.employe = request.user
			obj.save()
			return redirect('lisT')

	context = {'form':form}

	return render(request, 'tasks/update_task.html', context)

def deleteTask(request, pk):
	item = Task.objects.filter( employe_id = request.user.pk).get(id=pk)

	if request.method == 'POST':
		item.delete()
		return redirect('lisT')

	context = {'item':item}
	return render(request, 'tasks/delete.html', context)



