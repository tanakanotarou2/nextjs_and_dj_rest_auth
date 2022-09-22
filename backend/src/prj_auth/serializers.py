from dj_rest_auth.serializers import (
    JWTSerializerWithExpiration as OrgJWTSerializerWithExpiration,
)
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from accounts.serializers import UserDetailSerializer


class LoginResponseSerializer(OrgJWTSerializerWithExpiration):
    """ログインレスポンス"""

    # drop token
    access_token = None
    refresh_token = None

    access_token_expiration = serializers.DateTimeField(read_only=True, help_text="アクセストークンの有効期限")
    refresh_token_expiration = serializers.DateTimeField(read_only=True, help_text="リフレッシュトークンの有効期限")

    # 行儀良くないが、schema 生成のためだけに継承
    @extend_schema_field(UserDetailSerializer)
    def get_user(self, obj):
        return super(LoginResponseSerializer, self).get_user(obj)
