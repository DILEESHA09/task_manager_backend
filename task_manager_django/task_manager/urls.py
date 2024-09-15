from django.urls import path
from . import views

urlpatterns = [
        path('create-task/',views.CreateTaskView.as_view() ,name='create-task' ),
        path('tasks/', views.TaskListView.as_view(), name='task-list'),
        path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
        path('register/',views.RegisterView.as_view(),name='register'),
        path('login/',views.LoginView.as_view(),name='login'),
        path('logout/',views.LogoutView.as_view(),name='logout'),

       
        ]