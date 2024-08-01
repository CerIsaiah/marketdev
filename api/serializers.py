from rest_framework import serializers
from .models import User, Message

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'is_developer', 'is_marketer', 'skills', 'bio', 
                  'featured', 'profile_views', 'subscription_status', 'date_joined']
        read_only_fields = ['id', 'username', 'email', 'profile_views', 'subscription_status', 'date_joined']

class UserDashboardSerializer(serializers.ModelSerializer):
    connections = serializers.SerializerMethodField()
    active_projects = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'is_developer', 'is_marketer', 'skills', 'bio', 
                  'featured', 'profile_views', 'subscription_status', 'date_joined', 'connections', 'active_projects']

    def get_connections(self, obj):
        return obj.bookmarked_users.count()

    def get_active_projects(self, obj):
        # Implement this if you have a Project model
        return 0
    
class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.ReadOnlyField(source='sender.username')
    receiver_name = serializers.ReadOnlyField(source='receiver.username')

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'sender_name', 'receiver_name', 'content', 'created_at']
        read_only_fields = ['sender', 'created_at']