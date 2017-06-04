from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
# Create your views here.
def index(request):
  return render(request, 'exam_app/index.html')

def register(request):
    postdata= {
    "name": request.POST['name'],
    'alias': request.POST['alias'],
    'email': request.POST['email'],
    'password': request.POST['password'],
    'confirmpassword': request.POST['confirmpassword'],
    'date_birth': request.POST['date_birth']
    }
    # get data from register form, now validate in models.Manager
    # the resultfromvalidation is just a variable store the result from validation in models.Manager
    register_error = User.objects.register(postdata)
    print register_error

    if len(register_error) == 0:
        request.session['id'] = User.objects.filter(alias=postdata['alias'])[0].id
        request.session['name'] = postdata['name']
        return redirect('/next')
    else:
        for error in register_error:
            messages.info(request, error)
    return redirect('/')

def login(request):
    postdata= {
    'email': request.POST['email'],
    'password': request.POST['password'],
    }
    login_error = User.objects.login(postdata)
    if len(login_error) == 0:
        request.session['id'] = User.objects.filter(email=postdata['email'])[0].id
        request.session['name'] = User.objects.filter(email=postdata['email'])[0].alias
        return redirect('/next')
    for error in login_error:
        messages.info(request, error)
    return redirect('/')

def next(request):
  # print User.objects.all()
    return render(request, 'exam_app/next.html')
