from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

def index(request):
    return render(request, 'login_reg/index.html')

def home(request):
    if 'user_id' in request.session:
        user = User.objects.get(id = request.session['user_id'])
        context = {
            'user': user
        }
        return render(request, 'login_reg/home.html', context)
    return redirect('/')

def login(request):
    if request.method == "POST":
        result = User.objects.login(request.POST)
        return processLogin(request, result)
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def register(request):
    if request.method == "POST":
        result = User.objects.registerUser(request.POST)
        return processLogin(request, result)
    return redirect('/join')

def processLogin(request, result):
    if result['status']:
        request.session['user_id'] = result['user_id']
        return redirect('/home')

    for error in result['errors']:
        messages.error(request, error['message'], extra_tags = error['tag'])
    return redirect('/')
