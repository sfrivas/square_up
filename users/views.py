from django.db.models.query import QuerySet
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.defaults import page_not_found, bad_request
from django.core.exceptions import SuspiciousOperation
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    DetailView,
    ListView
)
from django.views import View
from django.db.models import Q
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile, UserFriend
from .FriendManager import FriendManager

# Django REST framework
from rest_framework import viewsets, permissions
from .serializers import UserFriendSerializer, UserSerializer

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created. You are now able to log in.')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
        messages.success(request, f'Your account has been updated.')
        return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)

@login_required
def friend_request_action(request, friend_username):
    action_string = request.GET.get('approve').lower()
    approved = None
    if action_string == 'true' or action_string == 'false':
        approved = action_string == 'true'
        print(f'Action string from url: {action_string}.')
    else:
        return bad_request(request, SuspiciousOperation)
    
    friend = User.objects.filter(username=friend_username).first()
    fm = FriendManager(request.user, friend)
    

    if approved:
        # User accepted request
        result = fm.approve(request.user)
    else:
        # User rejected request
        result = fm.reject(request.user)

    print(reverse('friend-requests'))

    return redirect('friend-requests')


class AddFriendView(LoginRequiredMixin, View):

    def get(self, request, username):
        requesting_user = request.user
        # If object does not exist for below query, Django will throw User.DoesNotExist exception.
        # See link below for more details: 
        # https://docs.djangoproject.com/en/3.2/topics/db/queries/#retrieving-a-single-object-with-get
        requested_user = User.objects.get(username=username)

        friendship = UserFriend.objects.filter(
            (Q(source_user=requesting_user) & Q(target_user=requested_user)) |
            (Q(source_user=requested_user) & Q(target_user=requesting_user))
        ).first()

        fm = FriendManager(requesting_user, requested_user)

        if friendship:
            context = {
                'relationship': '(Class based View) Relationship exists: ' + str(friendship),
                'source_user': requesting_user.username,
                'target_user': requested_user.username,
                'fm': fm
            }
        else:
            friendship = UserFriend(
                source_user=requesting_user,
                target_user=requested_user,
            )

            friendship.save()

            context = {
                'relationship': '(Class based View) Relationship DOES NOT exist. New friendship created.',
                'source_user': requesting_user.username,
                'target_user': requested_user.username,
                'fm': fm
            }

        return render(request, 'users/after_add_friend.html', context)

class FriendsView(LoginRequiredMixin, ListView):
    model = UserFriend
    ordering = ['-created_date']
    template_name = 'users/friends.html'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user.username)
        fm = FriendManager(user, None)
        friends = fm.get_all_friends()
        print(list(friends))
        return friends

class FriendRequestsView(LoginRequiredMixin, ListView):
    model = UserFriend
    ordering = ['created_date']
    template_name = 'users/friend_requests.html'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user.username)
        fm = FriendManager(user, None)
        incoming_requests = fm.get_incoming_requests()
        print(list(incoming_requests))
        return incoming_requests


class UserProfileView(DetailView):
    model = User
    template_name = 'users/view_profile.html'
    slug_url_kwarg = 'username'
    slug_field = 'username'

    def get(self, request, username):
        if request.user.is_authenticated:

            friend = self.get_object()

            friendship = FriendManager(request.user, friend)

            context = {
                'user': request.user,
                'friend': self.get_object(),
                'friendship': friendship
            }
        
        return render(request, self.template_name, context)

class UserFriendViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows UserFriends to be viewed or edited.
    """
    queryset = UserFriend.objects.all()
    serializer_class = UserFriendSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]