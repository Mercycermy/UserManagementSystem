from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),  
    path('register/', RegisterView.as_view(), name='register'),  
    path('change-password/', ChangePassword.as_view(), name='change-password'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
