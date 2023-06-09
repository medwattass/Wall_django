from django.shortcuts import render, redirect, HttpResponse
from .models import User
from django.contrib import messages
import bcrypt


def root(request):
    return redirect ('/login')


def login_page(request):
    return render(request, "login.html")


def registration_page(request):
    return render(request, "register.html")


def registration(request):
    if request.method == 'POST':
        errors = User.objects.validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/register')
        else:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            pwd = request.POST.get('password')
            birthday = request.POST.get('birthday')
            pw_hash = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode() 
            user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=pw_hash, birthday=birthday)
            request.session['user_id'] = user.id
            request.session['user_name'] = user.first_name
            return redirect('/wall')
    else:
        return HttpResponse('Method not allowed', status=405)


def loging_in(request):
    if request.method == 'POST':
        errors = User.objects.validator_pwd(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect ('/login')
        else:
            user = User.objects.filter(email=request.POST['email']).first()
            request.session['user_id'] = user.id
            request.session['user_name'] = user.first_name
            return redirect ('/wall')
    else:
        return HttpResponse('Method not allowed', status=405)


def logout(request):
    del request.session['user_name']
    del request.session['user_id']
    return redirect('/login')

