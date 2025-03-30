
from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view()),
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('change-password/', ChangePassword.as_view()),
    path('logout/', LogoutView.as_view()),
    path('edit-profile/', EditProfile.as_view()),
    path('feedback/', FeedbackView.as_view()),
    path('notifications/', NotificationView.as_view()),
    path('admin-dashboard/', AdminDashboard.as_view()),
    path('admin/edit-user/<int:user_id>/', EditUser.as_view()),
    path('admin/delete-user/<int:user_id>/', DeleteUser.as_view()),
    path('admin/reply-feedback/<int:feedback_id>/', ReplyFeedback.as_view()),
    path('admin/export-users/', ExportUsers.as_view()),
    path('search/', SearchView.as_view()),
]
