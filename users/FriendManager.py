from django.db.models.expressions import F
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Profile, UserFriend


class FriendManager():

    def __init__(self, source_user, target_user):
        self.source_user = source_user
        self.target_user = target_user
        self.friendship = None
        self.have_relationship = False
        self.friend_status = None
        self.are_friends = False

        self.update()

    @classmethod
    def for_single_user(cls, source_user):
        return cls(source_user=source_user)

    def run_query(self):
        self.friendship = UserFriend.objects.filter(
            (Q(source_user=self.source_user) & Q(target_user=self.target_user)) |
            (Q(source_user=self.target_user) & Q(target_user=self.source_user))
        ).first()

    def update_attributes(self):
        if self.friendship:
            self.have_relationship = True
            self.friend_status = self.friendship.status
            if self.friendship.status == UserFriend.FriendStatus.ACTIVE:
                self.are_friends = True

    def update(self):
        self.run_query()
        self.update_attributes()