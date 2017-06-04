from django.shortcuts import render, redirect
from .models import User, Appointment
from django.contrib import messages
from django.db.models import Count
from datetime import date
# Create your views here.
def index(request):
  return render(request, 'exam_app/index.html')

def register(request):
    postdata= {
    "name": request.POST['name'],
    'email': request.POST['email'],
    'password': request.POST['password'],
    'confirmpassword': request.POST['confirmpassword'],
    'date_birth': request.POST['date_birth']
    }
    # get data from register form, now validate in models.Manager
    # the resultfromvalidation is just a variable store the result from validation in models.Manager
    register_error = User.objects.register(request.POST)
    print register_error

    if len(register_error) == 0:
        request.session['id'] = User.objects.filter(email=postdata['email'])[0].id
        request.session['name'] = postdata['name']
        return redirect('/appointment')
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
        request.session['name'] = User.objects.filter(email=postdata['email'])[0].email
        return redirect('/appointment')
    for error in login_error:
        messages.info(request, error)
    return redirect('/')

def appointment(request):
    if 'id' not in request.session:
        return redirect ("/")
    appointments= Appointment.objects.filter(user__id=request.session['id']).exclude(date=date.today())
    user= User.objects.get(id=request.session['id'])
    # others = User.objects.all().exclude(appoint__id=request.session['id'])
    context = {
        "user": user,
        'time': date.today(),
        "today_appoint":  Appointment.objects.filter(user__id = request.session['id']).filter(date = date.today()),
        "appointments": appointments
    }
    return render(request, 'exam_app/appointment.html', context)

def add(request):
    if request.method != "POST":
        messages.error(request,"Can't add like that!")
        return redirect('/')
    else:
        add_appoint= Appointment.objects.appointval(request.POST, request.session['id'])
        if add_appoint[0] == False:
            for each in add_appoint[1]:
                messages.error(request, each) #for each error in the list, make a message for each one.
            return redirect('/appointment')
        if add_appoint[0] == True:
            messages.success(request, 'Appointment Successfully Added')
            return redirect('/appointment')

def update(request, appoint_id):
    try:
        appointment= Appointment.objects.get(id=appoint_id)
    except Appointment.DoesNotExist:
        messages.info(request,"appointment Not Found")
        return redirect('/appointment')

    context={
        "appointment": appointment,
        # "others": User.objects.filter(joiner__id=appoint.id).exclude(id=appoint.creator.id),
    }
    return render(request, 'exam_app/update.html', context)

def edit_appoint(request, appoint_id):
    if 'id' not in request.session:
        return redirect ('/')
    if request.method != 'POST':
        messages.info(request, "Cannot edit like this!")
        return redirect('/update'+ appoint_id)

    try:
        print("/"*50)
        update_app = Appointment.objects.edit_appointment(request.POST, appoint_id)
        print "got to edit_appoint Try"
    except Appointment.DoesNotExist:
        messages.info(request,"appointment Not Found")
        return redirect('/update/'+appoint_id)
    if update_app[0]==False:
        messages.info(request, "Please fill in all the spaces and make sure it's valid!")
        return redirect('/update/'+appoint_id)
    else:
        messages.success(request, "successfuly updated information")
        return redirect('/appointment')

def add(request):
    if request.method != "POST":
        messages.error(request,"Can't add like that!")
        return redirect('/')
    else:
        add_appoint= Appointment.objects.appointval(request.POST, request.session['id'])
        if add_appoint[0] == False:
            for each in add_appoint[1]:
                messages.error(request, each) #for each error in the list, make a message for each one.
            return redirect('/appointment')
        if add_appoint[0] == True:
            messages.success(request, 'Appointment Successfully Added')
            return redirect('/appointment')
#
def delete(request, appoint_id):
    try:
        target= Appointment.objects.get(id=appoint_id)
    except Appointment.DoesNotExist:
        messages.info(request,"Message Not Found")
        return redirect('/appointment')
    target.delete()
    return redirect('/appointment')
# #

def logout(request):
    if 'id' not in request.session:
        return redirect('/')
    print "*******"
    print request.session['id']
    del request.session['id']
    return redirect('/')
