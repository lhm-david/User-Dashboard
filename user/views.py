from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt


def index(request):
    return render (request, 'index.html')

def registerpage (request):
    return render (request, 'register.html')

def loginpage (request):
    return render (request, 'login.html')

def register (request):
    if request.method != 'POST':
        return redirect ('/register')
    else: 
        errors = User.objects.reg_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect ('/register')
        else:
            new_user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            )
            request.session['user_id'] = new_user.id
            request.session['greeting'] = new_user.first_name
            first_user = User.objects.get(id = 1)
            if new_user.id == first_user.id:
                new_user.userlevel = 'Admin'
                new_user.save()
            else:
                new_user.userlevel = 'Normal'
                new_user.save()
            return redirect('/success')

def login(request):
    if request.method != 'POST':
        return redirect ('/login')
    else:
        errors = User.objects.login_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/login')
        else:
            loginuser = User.objects.get(email=request.POST['email'])
            request.session['user_id'] = loginuser.id
            request.session['greeting'] = loginuser.first_name
            return redirect('/success')

def inpage(request):
    if 'user_id' not in request.session:
        return redirect('/login')
    else:
        users = User.objects.all()
        loginuser = User.objects.get(id = request.session['user_id'])
        context = {
            'all_users': users,
            'loginuser':loginuser
        }
        return render (request, 'maindashboard.html', context)

def addnewpage(request):
    return render (request, 'addnew.html')

def addnewuser(request):
    if request.method != 'POST':
        return redirect ('/addnew')
    else: 
        errors = User.objects.reg_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect ('/addnew')
        else:
            User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            )
            return redirect('/success')

def userpage(request, user_id):
    this_user = User.objects.get(id = request.session['user_id'])
    user = User.objects.get(id = user_id)
    messages = Message.objects.filter(created_for = user.id)
    context = {
        'user':user,
        'login_user':this_user,
        'all_messages':messages,
    }
    return render (request,'userprofile.html', context)

def addmessage (request, user_id):
    if request.method == 'POST':
        user = User.objects.get(id = user_id)
        loginuser = User.objects.get(id = request.session['user_id'])
        errors = Message.objects.message_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                    messages.error(request, value)
        else:
            Message.objects.create(message_content = request.POST['message'], poster = loginuser, created_for = user.id)
        return redirect (f'/userprofile/{user.id}')

def addcomment (request, user_id,message_id):
    user = User.objects.get(id = user_id)
    if request.method == 'POST':
        this_user = User.objects.get(id = request.session['user_id'])
        this_message = Message.objects.get(id = message_id)
        errors = Comment.objects.comment_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                    messages.error(request, value)
        Comment.objects.create(comment_content = request.POST['comment'], formessage = this_message, poster = this_user)
    return redirect (f'/userprofile/{user.id}')


def edituserpage(request, user_id):
    loginuser = User.objects.get(id = request.session['user_id'])
    if loginuser.userlevel == 'Normal':
        context = {
            'user': loginuser
        }
    else:
        user = User.objects.get(id = user_id)
        context = {
            'user':user,
            'loginuser':loginuser
        }
    return render (request, 'editprofile.html', context)

def edituser (request, user_id):
    if request.method == 'POST':
        user = User.objects.get(id = user_id)
        errors = User.objects.update_user(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect (f'/edituser/{user.id}')
        else:    
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.save()
            return redirect(f'/userprofile/{user.id}')

def userlevel (request, user_id):
    user = User.objects.get(id = user_id)
    user.userlevel = request.POST['user_level']
    user.save()
    return redirect ('/success')

def editpassword (request):
    user = User.objects.get(id = request.session['user_id'])
    if request.method == 'POST':
        
        errors = User.objects.password_change(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect ('/edituser')
        else:
            newpassword = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            user.password = newpassword
            user.save()
            return redirect ('/logout')

def logout(request):
    request.session.flush()
    return redirect('/')

def deleteMessage (request, id):
    remove = Message.objects.get(id = id)
    remove.delete()
    return redirect('/success')

def deleteUser (request, user_id):
    if user_id != request.session['user_id']:
        remove = User.objects.get(id = user_id)
        remove.delete()
    return redirect('/success')

