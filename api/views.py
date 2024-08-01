#api/views.py

from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer, UserProfileSerializer, UserDashboardSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q
from .models import Message
from .serializers import MessageSerializer
from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
import logging

logger = logging.getLogger(__name__)



# Serve React App
index = never_cache(TemplateView.as_view(template_name='index.html'))

User = get_user_model()

@api_view(['POST'])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        logger.debug(f'User registered: {user}')
        logger.debug(f'Access token: {str(refresh.access_token)}')
        logger.debug(f'Refresh token: {str(refresh)}')
        return Response({
            'user': serializer.data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)
    logger.error(f'Errors during registration: {serializer.errors}')
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserDashboardView(generics.RetrieveAPIView):
    serializer_class = UserDashboardSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

@api_view(['GET'])
@permission_classes([AllowAny])
def featured_users(request):
    featured_users = User.objects.filter(featured=True)[:3]
    serializer = UserProfileSerializer(featured_users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bookmark_user(request):
    user_id = request.data.get('user_id')
    try:
        user_to_bookmark = User.objects.get(id=user_id)
        if user_to_bookmark in request.user.bookmarked_users.all():
            request.user.bookmarked_users.remove(user_to_bookmark)
            message = 'User unbookmarked successfully'
        else:
            request.user.bookmarked_users.add(user_to_bookmark)
            message = 'User bookmarked successfully'
        return Response({'message': message}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_bookmarked_users(request):
    bookmarked_users = request.user.bookmarked_users.all()
    serializer = UserProfileSerializer(bookmarked_users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def list_users(request):
    search_query = request.GET.get('search', '')
    filter_query = request.GET.get('filter', 'all')

    users = User.objects.all()

    if search_query:
        users = users.filter(name__icontains=search_query)

    if filter_query != 'all':
        if filter_query == 'developer':
            users = users.filter(is_developer=True)
        elif filter_query == 'marketer':
            users = users.filter(is_developer=False)

    serializer = UserProfileSerializer(users, many=True)
    return Response(serializer.data)

class MessageListCreate(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        other_user_id = self.request.query_params.get('user_id')
        if other_user_id:
            return Message.objects.filter(
                (Q(sender=user) & Q(receiver_id=other_user_id)) |
                (Q(sender_id=other_user_id) & Q(receiver=user))
            ).order_by('created_at')
        return Message.objects.filter(Q(sender=user) | Q(receiver=user)).order_by('created_at')

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_conversation_list(request):
    user = request.user
    conversations = Message.objects.filter(Q(sender=user) | Q(receiver=user)) \
        .values('sender', 'receiver') \
        .distinct() \
        .order_by('-created_at')
    
    conversation_list = []
    for conv in conversations:
        other_user = User.objects.get(id=conv['sender'] if conv['sender'] != user.id else conv['receiver'])
        conversation_list.append({
            'user_id': other_user.id,
            'username': other_user.username,
            'name': other_user.name
        })
    
    return Response(conversation_list)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_conversation_partners(request):
    user = request.user
    conversation_partner_ids = Message.objects.filter(
        Q(sender=user) | Q(receiver=user)
    ).values_list('sender', 'receiver').distinct()
    
    unique_partner_ids = set()
    for sender_id, receiver_id in conversation_partner_ids:
        if sender_id != user.id:
            unique_partner_ids.add(sender_id)
        if receiver_id != user.id:
            unique_partner_ids.add(receiver_id)
    
    conversation_partners = User.objects.filter(id__in=unique_partner_ids)
    serializer = UserProfileSerializer(conversation_partners, many=True)
    return Response(serializer.data)