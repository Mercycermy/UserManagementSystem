from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Feedback, Notification, DeletedUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class FeedbackSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Feedback
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class DeletedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeletedUser
        fields = '__all__'
