from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.

from django.views import View
from django.contrib.auth.models import User, auth
from .models import Feedback, Notification, DeletedUser
from django.utils import timezone
import openpyxl
from django.http import HttpResponse
from django.db.models import Q


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
#Edit Profile
class EditProfile(View):
    def get(self, request):
        return render(request, "edit_profile.html")

    def post(self, request):
        user = request.user
        user.first_name = request.POST.get('firstname')
        user.last_name = request.POST.get('lastname')
        user.email = request.POST.get('email')
        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('/edit-profile')

#Send Feedback
class FeedbackView(View):
    def get(self, request):
        feedbacks = Feedback.objects.filter(user=request.user)
        return render(request, "feedback.html", {"feedbacks": feedbacks})

    def post(self, request):
        msg = request.POST.get('message')
        Feedback.objects.create(user=request.user, message=msg)
        messages.success(request, "Feedback sent.")
        return redirect('/feedback')

# View Notifications
class NotificationView(View):
    def get(self, request):
        notifs = Notification.objects.filter(user=request.user)
        return render(request, "notifications.html", {"notifications": notifs})

# Admin Dashboard
class AdminDashboard(View):
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('/')
        users = User.objects.all()
        feedbacks = Feedback.objects.all()
        deleted = DeletedUser.objects.all()
        return render(request, "admin_dashboard.html", {
            "users": users,
            "feedbacks": feedbacks,
            "deleted": deleted
        })

# Admin Edit/Delete Users
class EditUser(View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        return render(request, "edit_user.html", {"user": user})

    def post(self, request, user_id):
        user = User.objects.get(id=user_id)
        user.first_name = request.POST.get('firstname')
        user.last_name = request.POST.get('lastname')
        user.email = request.POST.get('email')
        user.save()
        messages.success(request, "User updated.")
        return redirect('/admin-dashboard')

class DeleteUser(View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        DeletedUser.objects.create(username=user.username, email=user.email)
        user.delete()
        messages.success(request, "User deleted.")
        return redirect('/admin-dashboard')

# Admin Reply to Feedback
class ReplyFeedback(View):
    def post(self, request, feedback_id):
        feedback = Feedback.objects.get(id=feedback_id)
        feedback.reply = request.POST.get('reply')
        feedback.save()
        messages.success(request, "Replied to feedback.")
        return redirect('/admin-dashboard')

#Export to Excel
class ExportUsers(View):
    def get(self, request):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(["ID", "Username", "Email", "First Name", "Last Name"])
        for user in User.objects.all():
            ws.append([user.id, user.username, user.email, user.first_name, user.last_name])
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=users.xlsx'
        wb.save(response)
        return response

# Search Users or Feedback
class SearchView(View):
    def get(self, request):
        query = request.GET.get('q')
        users = User.objects.filter(
            Q(username__icontains=query) | Q(email__icontains=query)
        )
        feedbacks = Feedback.objects.filter(
            Q(message__icontains=query)
        )
        return render(request, "search.html", {
            "users": users,
            "feedbacks": feedbacks,
            "query": query
        })