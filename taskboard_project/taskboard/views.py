from django.shortcuts import render

# Create your views here.
# taskboard/views.py

from django.shortcuts import render, redirect

from taskboard.forms import CustomAuthenticationForm, CustomUserCreationForm
from .models import User, Task

from django.contrib.auth import authenticate, login

def login(request):
        error_message = ''
        if request.method == 'POST':
            form = CustomAuthenticationForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user = authenticate(request, username=email, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('taskboard:login')  # Redirect to the desired page after successful login
                else:
                    error_message = 'Invalid email or password. Please try again.'
            else:
                error_message = 'Invalid form data. Please check your input.'
        else:
            form = CustomAuthenticationForm()

        return render(request, 'login.html', {'form': form, 'error_message': error_message})


def create_list(request):
    # Your create list logic here
    return redirect('taskboard:task_list')

def task_list(request):
    lists = range(1, 3)  # Assume there are 5 lists
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'lists': lists, 'tasks': tasks})

import random
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm  # Import your actual form

def register(request):
    error_message = ''

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            # Check if the email ends with the allowed domain
            if not email.endswith('@gmail.com'):
                error_message = 'Only @gmail.com email addresses are allowed.'
            else:
                # Save the user without OTP verification
                user = form.save()

                # Redirect to a success page or login page
                return redirect('login')  # Update with the actual URL name or path for login

        else:
            # Form data is not valid, set an error message
            # Check for email and password errors
            email_errors = form.errors.get('username', [])
            password_errors = form.errors.get('password1', [])
            
            if email_errors:
                error_message = email_errors[0]
            elif password_errors:
                error_message = password_errors[0]
            else:
                # If there are no specific errors for email or password, use a general error
                error_message = 'Password should be between 8 to 16 characters long.'

    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form, 'error_message': error_message})



from django.shortcuts import render, redirect
from .models import Task

def add_task(request):
    if request.method == 'POST':
        task_title = request.POST.get('task_title')
        list_id = request.POST.get('list_id')

        # Save the new task to the database
        Task.objects.create(title=task_title, list_id=list_id)

    # Redirect back to the task list page
    return redirect('taskboard:task_list')

# taskboard/views.py

from django.shortcuts import render, redirect
from django.http import Http404
from .models import Task

# Your existing views...

def delete_task(request, task_id):
    if request.method == 'POST':
        try:
            # Get the task by ID and delete it
            task = Task.objects.get(id=task_id)
            task.delete()
        except Task.DoesNotExist:
            raise Http404("Task does not exist.")

    # Redirect back to the task list page
    return redirect('taskboard:task_list')


# taskboard/views.py

from django.shortcuts import render, redirect
from .models import Task

# Your existing views...

def change_status(request, task_id):
    if request.method == 'POST':
        try:
            task = Task.objects.get(id=task_id)
            task.completed = not task.completed  # Toggle the status
            task.save()
        except Task.DoesNotExist:
            # Handle the case where the task does not exist
            pass

    # Redirect back to the task list page
    return redirect('taskboard:task_list')
