from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib import messages


# Create your views here.
def home(request):
    # context = {
    #     'posts': Post.objects.all()
    # }
    return render(request, 'home.html')