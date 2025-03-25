
from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view()),
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('change-password/', ChangePassword.as_view()),
    path('logout/', LogoutView.as_view()),
]
