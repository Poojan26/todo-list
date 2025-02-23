from django.shortcuts import render,redirect
from django.http import HttpResponse
from todolist_app.models import TaskList
from todolist_app.forms import Taskform
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required 

# Create your views here.

@login_required
def todolist(request):
    
    if request.method == "POST":
        form = Taskform(request.POST or None)
        if form.is_valid:
            instance = form.save(commit=False)
            instance.manage = request.user
            instance.save()
        messages.success(request,("Task added successfully!"))    
        return redirect('todolist')
        
    else:   
        all_tasks = TaskList.objects.filter(manage = request.user )
        paginator = Paginator(all_tasks, 5)
        page = request.GET.get('pg')
        all_tasks = paginator.get_page(page)
        
        return render(request,'todolist.html',{'all_tasks':all_tasks})


def delete_task(request,task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.manage == request.user:
        task.delete()
    else:
        messages.error(request,("Access denied- You cannot delete any info provided by another user"))
    return redirect('todolist')

def edit_task(request,task_id):
    
    if request.method == "POST":
        task = TaskList.objects.get(pk=task_id)
        form = Taskform(request.POST or None, instance=task)
        if form.is_valid:
            form.save()
        
        messages.success(request,("Task updated successfully!"))    
        return redirect('todolist')
        
    else:   
        task_obj = TaskList.objects.get(pk=task_id)
        return render(request,'edit.html',{'task_obj':task_obj})

@login_required
def complete_task(request,task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.manage == request.user:
        task.done = True
        task.save()
        return redirect(request.META['HTTP_REFERER'])
    else:
        messages.error(request,("Access Denied- You are not authorized to access this page"))
        return redirect('todolist')
        
    

def pending_task(request,task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.manage == request.user:
        task.done = False
        task.save()
        return redirect(request.META['HTTP_REFERER'])
    else:
        messages.error(request,("Access Denied- You are not authorized to access this page"))
        return redirect('todolist')
        

def index(request):
    context = {
                'index_text':"Welcome from Index page"
               }
    
    return render(request,'index.html',context)

        
    
    
def contact(request):
    context = {
                'contact_text':"Welcome from Contact Us page"
               }
    
    return render(request,'contact.html',context)

def about(request):
    context = {
                'about_text':"Welcome from About us page"
               }
    
    return render(request,'about.html',context)