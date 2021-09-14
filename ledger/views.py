from ledger.models import Transaction
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView
)
from .models import Transaction

# Create your views here.
class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    fields = ['transaction_date', 'amount']
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)