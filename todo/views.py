from django.shortcuts import render, redirect
from .models import Todo
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

@login_required
def todo_list(request):
    todos = Todo.objects.filter(user=request.user)
    return render(request, 'todo/index.html', {'todos': todos})

@login_required
def create_todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        if title and description:  # prevent empty records
            Todo.objects.create(user=request.user, title=title, description=description)
    return redirect('todo_list')  # ✅ use URL name instead of '/'

'''
def complete_todo(request, todo_id):
    todo = Todo.objects.get(Todo, id=todo_id)
    todo.completed = True
    todo.save()
    return redirect('todo_list')


def complete_todo(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    todo.progress = not todo.progress  # switch between True/False
    todo.save()
    return redirect('todo_list')
'''

@login_required
def complete_todo(request, todo_id):
    todo = Todo.objects.get(id=todo_id, user=request.user)
    todo.progress = not todo.progress  # switch between True/False
    todo.save()
    return redirect('todo_list')

def delete_todo(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    todo.delete()
    return redirect('todo_list')

# ✅ Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('todo_list')
        else:
            return render(request, 'todo/login.html', {'error': 'Invalid credentials'})
    return render(request, 'todo/login.html')

# ✅ Logout view
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# ✅ Signup (optional)
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('todo_list')
        else:
            return render(request, 'todo/signup.html', {'error': 'Username already exists'})
    return render(request, 'todo/signup.html')