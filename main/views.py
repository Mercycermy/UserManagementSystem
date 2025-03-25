from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.

from django.views import View
from django.contrib.auth.models import User, auth


class IndexView(View):
    def get(self, request):
        if(not request.user.is_authenticated):
            return redirect('/login')
        users = User.objects.all()
        return render(request, "index.html", {"users": users})


class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        return redirect('/')


class LoginView(View):
    def get(self, request):
        if(request.user.is_authenticated):
            return redirect('/')
        return render(request, "login.html")

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        error = 0
        if(username == ""):
            messages.add_message(request, messages.ERROR,
                                 "Username can't be empty.")
            error += 1
        if(password == ""):
            messages.add_message(request, messages.ERROR,
                                 "Password can't be empty.")
            error += 1

        if(not error):
            user = auth.authenticate(
                request, username=username, password=password)

            if(user is not None):
                auth.login(request, user)
                return redirect('/')
            else:
                messages.add_message(request, messages.ERROR,
                                     "Username or Password was wrong")

        return redirect('/login')


class RegisterView(View):
    def get(self, request):
        return render(request, "register.html")

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        error = 0
        if(email == ""):
            messages.add_message(request, messages.ERROR,
                                 "Email can't be empty.")
            error += 1
        if(password == ""):
            messages.add_message(request, messages.ERROR,
                                 "Password can't be empty.")
            error += 1
        if(User.objects.filter(username=email).exists()):
            messages.add_message(request, messages.ERROR,
                                 "Email already registered.")
            error += 1

        if(not error):
            user = User.objects.create_user(
                username=email, password=password, email=email, first_name=first_name, last_name=last_name,)
            if user is not None:
                user.set_password(password)
                user = auth.authenticate(
                    request, username=email, password=password)
                auth.login(request, user)
                return redirect('/')

        return redirect('/register')




class ChangePassword(View):
    def get(self, request):
        if not request.user.is_authenticated:
            messages.add_message(request, messages.ERROR,
                                 "You aren't loged in.")
            return redirect('/')

        return render(request, "changepassword.html")

    def post(self, request):
        if not request.user.is_authenticated:
            messages.add_message(request, messages.ERROR,
                                 "You aren't loged in.")
            return redirect("/")
        oldpass = request.POST.get('oldpass')
        newpass = request.POST.get('newpass')

        user = User.objects.get(id=request.user.id)
        error = 0

        if(len(newpass) < 8):
            messages.add_message(request, messages.ERROR,
                                 "New password cant be less than 8 charecture.")
            error += 1

        if error:
            return redirect('/change-password')

        if(user.check_password(oldpass)):
            user.set_password(newpass)
            user.save()
            auth.login(request, user)
            messages.add_message(request, messages.SUCCESS,
                                 "Password updated.")
        else:
            messages.add_message(request, messages.ERROR,
                                 "Old Password doesn't match.")

        return redirect('/change-password')
