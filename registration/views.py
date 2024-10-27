from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('index')
    else:
        form = UserRegistrationForm()
    return render(request,'registration/register.html',{'form':form})

# registration/views.py
from django.shortcuts import render

def login_view(request):
    return render(request, 'registration/login.html')

def register_view(request):
    return render(request, 'registration/register.html')

