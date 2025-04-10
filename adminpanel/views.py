from django.contrib import admin, messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

def adminlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        admin_user = authenticate(username = username, password = password)
        if admin_user is not None:
            admin_user_details = User.objects.get(username=username)
            if admin_user_details.is_superuser:

                login(request,admin_user)

                return redirect(admin_homepage)
            else:
                messages.error(request,'Enter correct admin details..')
                return render(request,'adminlogin.html')
        else:
            messages.error(request,'Enter correct admin details..')
            return render(request,'adminlogin.html')
    return render(request,'adminlogin.html')

@login_required(login_url='/')
def admin_homepage(request):
        admin_details = User.objects.all() 
        return render(request,'adminhome.html',{ 'user' : admin_details})

@login_required(login_url='/')
def user_edit( request ):
        id = request.GET.get( 'id' )
        user = User.objects.filter( id = id )
        if user:
            user_details = User.objects.get( id = id )
            return render(request,'admin_userinfo.html',{ 'user':user_details })
        return redirect(admin_homepage)


@login_required(login_url='/')
def user_update(request):
        if request.method == 'POST':
            id = request.POST[ 'id' ]
            username = request.POST[ 'username' ]
            email = request.POST[ 'email' ]
            check = User.objects.filter(username=username).exists()
            if check == False:
                User.objects.filter( id = id ).update( username = username, email = email)
        return redirect(admin_homepage)

def user_block(request):
        id = request.GET.get('id')
        user = User.objects.get( id = id )
        if user.is_staff == 0:
            User.objects.filter(id=id).update(is_staff = 1)
        else:
            User.objects.filter(id=id).update(is_staff=0)

        return redirect(admin_homepage)


def user_delete(request):
        id = request.GET.get('id')
        User.objects.filter(id = id).delete()
        return redirect(admin_homepage)


from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required(login_url='/')
def user_add(request):
    if request.method == 'POST':
        # Get data 
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')

    
        if not username or not email or not password:
            messages.error(request, 'Username, email, and password are required.')
            return render(request, 'admin_adduser.html')

        # Create a new user
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = firstname
            user.last_name = lastname
            user.save()
            messages.success(request, 'User added successfully!')
            return redirect('admin_homepage')
        except Exception as e:
            messages.error(request, f'Error adding user: {str(e)}')

    return render(request, 'admin_adduser.html')


@login_required(login_url='adminpanel')
def admin_logout(request):
        logout(request)
        print('ok')
        return redirect(adminlogin)

def searched(request):
    if request.method == 'POST':
        val = request.POST['searched']
        admin_details = User.objects.filter(username__contains=val)
        return render(request,'adminhome.html',{ 'user' : admin_details})
  