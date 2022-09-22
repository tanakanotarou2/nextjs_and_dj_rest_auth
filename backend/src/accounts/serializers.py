from rest_framework.serializers import ModelSerializer

from accounts.models import User


class UserSerializer(ModelSerializer):
    """ユーザー情報。ログインユーザー全体に公開できる情報です"""

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "profile_icon"]
        read_only_fields = ["id"]


class UserDetailSerializer(ModelSerializer):
    """ユーザー情報。ユーザー本人及び上位権限者のみ参照できる情報です"""

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "profile_icon"]
        read_only_fields = ["id", "username"]
