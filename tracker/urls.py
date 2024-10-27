from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from . import views, views as reg_views
from .views import  add_topic, edit_topic, delete_topic,mark_completed


urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('add/',views.add_topic,name='add_topic'),
    path('edit/<int:topic_id>/', edit_topic, name='edit_topic'),
    path('delete/<int:topic_id>/', delete_topic, name='delete_topic'),
    path('login/', auth_views.LoginView.as_view(template_name='tracker/login.html'), name='login'),
    path('mark_completed/<int:topic_id>/', mark_completed, name='mark_completed'),
    path('progress/', views.progress, name='progress'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register, name='register'),
]
