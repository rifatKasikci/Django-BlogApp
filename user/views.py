from email import message
from django.shortcuts import render,redirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import login as django_login
from django.contrib.auth import authenticate
from django.contrib.auth import logout as django_logout
from django.contrib import messages


# Create your views here.
def register(request):
    
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        inserted_user = User(username=username)
        inserted_user.set_password(password)
        inserted_user.save()
        django_login(request,inserted_user)
        messages.success(request,"Başarıyla kayıt oldunuz!")
        return redirect("index")
    
    context = {
       "form":form
       }
    return render(request,"register.html",context)    

    
    

def login(request):
    form = LoginForm(request.POST or None)
    context = {
        "form":form
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        
        user = authenticate(username=username,password=password)

        if user is None:
            messages.info(request,"Kullanıcı bulunamadı!")
            return render(request,"login.html",context)
        messages.success(request,"Başarıyla giriş yaptınız!")
        django_login(request,user)
        return redirect("index")   
    return render(request,"login.html",context)

def logout(request):
    django_logout(request)
    messages.success(request,"Başarıyla çıkış yaptınız!")
    return redirect("index")

