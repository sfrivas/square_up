from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile-pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class UserFriend(models.Model):
    # ENUM for friend status
    # See here for more details: 
    # https://docs.djangoproject.com/en/3.2/ref/models/fields/#enumeration-types
    class FriendStatus(models.IntegerChoices):
        NEW = 0
        ACTIVE = 1
        REJECTED = 2

    # DB columns
    source_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='source_user')
    target_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='target_user')
    created_date = models.DateTimeField(auto_now_add=True)
    udpated_date = models.DateTimeField(auto_now=True)
    status = models.PositiveSmallIntegerField(
        choices=FriendStatus.choices,
        default=FriendStatus.NEW)

    def __str__(self):
        return f'{self.FriendStatus(self.status).label} Friendship between: {self.source_user.username} and {self.target_user.username}'