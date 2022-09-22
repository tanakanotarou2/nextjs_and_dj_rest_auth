from typing import List

from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.views import LoginView as OrgLoginView
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from drf_spectacular.utils import extend_schema, extend_schema_view, inline_serializer
from rest_framework import serializers
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from prj_auth.serializers import LoginResponseSerializer


@extend_schema_view(
    get=extend_schema(
        responses={200: inline_serializer(name="CSRFResponse", fields={"csrfToken": serializers.CharField()})},
    ),
)
class CSRFView(APIView):
    # authentication_classes = [] #type:None
    permission_classes = [AllowAny]

    # クッキーごとにキャッシュするのはありかもしれない
    @method_decorator(cache_page(10))
    @method_decorator(vary_on_cookie)
    def get(self, request, format=None):
        """CSRFトークンを取得します"""
        return Response({"csrfToken": get_token(request)})


@extend_schema_view(
    get=extend_schema(
        responses={200: inline_serializer(name="PingResponse", fields={"result": serializers.CharField()})},
    ),
)
class PingView(APIView):
    def get(self, request, format=None):
        """認証検証用のエンドポイント"""
        return Response({"result": "ok"})


@extend_schema_view(
    post=extend_schema(
        responses={200: LoginResponseSerializer},
    ),
)
class LoginView(OrgLoginView):
    # クライアントが session に認証情報を持っていても
    # 再度ログインできるように authentication をスキップしています
    authentication_classes: List[BaseAuthentication] = []


# デフォルトのリフレッシュクラスを取得

OrgRefreshViewCls = get_refresh_view()


@extend_schema_view(
    post=extend_schema(
        request=None,
        responses={
            200: inline_serializer(
                name="RefreshTokenResponse",
                fields={"accessTokenExpiration": serializers.DateTimeField(help_text="新しいトークンの有効期限")},
            )
        },
        description="アクセストークンをリフレッシュします",
    ),
)
class RefreshView(OrgRefreshViewCls):  # type: ignore
    # Note: アクセストークンが切れていても、リフレッシュトークンが有効期限内であれば
    # リフレッシュしたいので、authentication をスキップしています
    # 必要な認証があれば追加してください
    authentication_classes: List[BaseAuthentication] = []

    def finalize_response(self, request, response, *args, **kwargs):
        res = super().finalize_response(request, response, *args, **kwargs)
        if res.status_code != 200:
            return res

        # drop tokens
        for key in ["access", "refresh"]:
            if key in res.data:
                del res.data[key]

        return res
