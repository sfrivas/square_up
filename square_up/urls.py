"""square_up URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from square_up import views as app_views
from users import views as user_views
from ledger.views import (
    TransactionCreateView
)

# Django REST framework
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', user_views.UserViewSet)
router.register(r'userfriends', user_views.UserFriendViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', app_views.home, name='home'),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('transaction/new', TransactionCreateView.as_view(), name='transaction-create'),
    path('profile/', user_views.profile, name='profile'),
    path('user/<slug:username>', user_views.UserProfileView.as_view(), name='user-profiles'),
    path('user/<slug:username>/addfriend/', user_views.AddFriendView.as_view(), name='add-friend'),
    path('friendrequests/', user_views.FriendRequestsView.as_view(), name='friend-requests'),
    path('friendrequests/<slug:friend_username>/', user_views.friend_request_action, name='friend-request-action'),
    path('friends/', user_views.FriendsView.as_view(), name='friends'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
