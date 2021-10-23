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

    def __str__(self):
        return f'Friend Manager between: {self.source_user.username} {self.target_user.username}'

    @classmethod
    def for_single_user(cls, source_user):
        return cls(source_user=source_user, target_user=None)

    def run_query(self):
        self.friendship = UserFriend.objects.filter(
            (Q(source_user=self.source_user) & Q(target_user=self.target_user)) |
            (Q(source_user=self.target_user) & Q(target_user=self.source_user))
        ).first()

    def update_attributes(self):
        if self.friendship:
            self.source_user = self.friendship.source_user
            self.target_user = self.friendship.target_user
            self.have_relationship = True
            self.friend_status = self.friendship.status
            if self.friendship.status == UserFriend.FriendStatus.ACTIVE:
                self.are_friends = True

    def update(self):
        self.run_query()
        self.update_attributes()

    def get_all_friend_relationships(self):
        if self.source_user and not self.target_user:
            friends = UserFriend.objects.filter(
                Q(source_user=self.source_user) |
                Q(target_user=self.source_user)
            )
            return friends
        else:
            print('Source_user is not populated or target_user is populated.')
            return None

    def get_all_friends(self):
        if self.source_user and not self.target_user:
            friend_relationships = UserFriend.objects.filter(
                Q(source_user=self.source_user) |
                Q(target_user=self.source_user)
            )
            ids = set()
            for relationship in friend_relationships:
                if relationship.source_user == self.source_user:
                    ids.add(relationship.target_user.username)
                else:
                    ids.add(relationship.source_user.username)
            friends = User.objects.filter(username__in = ids)
            return friends
        else:
            print('Source_user is not populated or target_user is populated.')
            return None

    def get_incoming_requests(self):
        if self.source_user and not self.target_user:
            friends = UserFriend.objects.filter(
                target_user=self.source_user,
                status=UserFriend.FriendStatus.NEW
            )
            return friends
        else:
            print('Source_user is not populated or target_user is populated.')
            return None

    def user_can_approve(self, user):
        print('FriendManager.user_can_approve() method called.')
        print(f'target_user: {self.target_user.username}.')
        print(f'User can approve: {self.target_user == user}')
        return self.target_user == user
    
    def user_can_reject(self, user):
        return (self.source_user == user or self.target_user == user)

    def approve(self, approver):
        print('FriendManager.approve() method called.')
        print(f'Logged in user: {approver.username}')
        if self.user_can_approve(approver):
            print(f'{approver} can approve.')
            # Approver is the person who rec'd request
            if (self.have_relationship and not self.are_friends):
                # if not yet friends, update the relationship to friendship
                self.friendship.status = UserFriend.FriendStatus.ACTIVE
                self.friendship.save()
                print(f'{approver} updated and saved the relationship to {self.friendship.status}.')
                return True
            else:
                return False
        else:
            # Approver is not authorized to approve the request
            return False

    def reject(self, rejecter):
        if self.user_can_reject(rejecter):
            print(f'{rejecter} can reject.')
            # Approver is the person who rec'd request
            if (self.have_relationship):
                # if not yet friends, update the relationship to friendship
                self.friendship.status = UserFriend.FriendStatus.REJECTED
                self.friendship.save()
                print(f'{rejecter} updated and saved the relationship to {self.friendship.status}.')
                return True
            else:
                return False
        else:
            # Approver is not authorized to approve the request
            return False
