from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('users/register/', views.register_user, name='register-user'),
    path('users/profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('users/dashboard/', views.UserDashboardView.as_view(), name='user-dashboard'),
    path('users/featured/', views.featured_users, name='featured-users'),
    path('users/bookmark/', views.bookmark_user, name='bookmark-user'),
    path('users/bookmarked/', views.get_bookmarked_users, name='bookmarked-users'),
    path('users/list/', views.list_users, name='list-users'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('messages/', views.MessageListCreate.as_view(), name='message-list-create'),
    path('conversations/', views.get_conversation_list, name='conversation-list'),
    path('conversation-partners/', views.get_conversation_partners, name='conversation-partners'),
]
