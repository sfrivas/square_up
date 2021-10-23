from .models import User, UserFriend
from rest_framework import serializers


class UserFriendSerializer(serializers.HyperlinkedModelSerializer):
    
    source_user = serializers.CharField(
        read_only=True,
        source = 'source_user.username'
        )

    target_user = serializers.CharField(
        read_only=True,
        source = 'target_user.username'
        )

    source_user_url = serializers.HyperlinkedRelatedField(
        read_only=True,
        source = 'source_user',
        view_name='user-detail'
        )

    target_user_url = serializers.HyperlinkedRelatedField(
        read_only=True,
        source = 'target_user',
        view_name='user-detail'
        )


    
    class Meta:
        model = UserFriend
        fields = [
            'source_user',
            'source_user_url',
            'target_user',
            'target_user_url',
            'created_date',
            'status'
        ]

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']