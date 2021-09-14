from decimal import *
from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    transaction_date = models.DateField()
    created_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
        )

    def __str__(self):
        return (self.user.username + str(self.transaction_date))

    # def get_absolute_url(self):
    #     return reverse('home', kwargs={"pk": self.pk})
    