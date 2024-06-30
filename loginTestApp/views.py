from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm
from .CustomUserCreationForm import myUserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html',{
            'form': myUserCreationForm()
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            user= User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
            user.save()
            return HttpResponse('User Created')
        else: 
            return HttpResponse('Wrong Password')
        
        
@login_required
def some_protected_view(request):
    return HttpResponse('This is a protected view')




def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('rtplot')  # o a donde quieras redirigir después de iniciar sesión
        else:
            return HttpResponse('Invalid login')
    else:
        return render(request, 'login.html')