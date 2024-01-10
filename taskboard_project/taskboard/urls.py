# taskboard/urls.py

from django.urls import path
from . import views

app_name = 'taskboard'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('create_list/', views.create_list, name='create_list'),
    path('task_list/', views.task_list, name='task_list'),
    path('', views.register, name='register'),
    path('add_task/', views.add_task, name='add_task'),  # Add this line for adding tasks
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),  # Add this line for deleting tasks
    path('change_status/<int:task_id>/', views.change_status, name='change_status'),  # Add this line for changing status
    # Add other URLs as needed
]
