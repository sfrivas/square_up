from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.views import View
from django.db.models import Q
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile, UserFriend
from .FriendManager import FriendManager

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


class UserProfileView(DetailView):
    model = User
    template_name = 'users/view_profile.html'
    slug_url_kwarg = 'username'
    slug_field = 'username'