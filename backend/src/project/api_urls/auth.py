from dj_rest_auth.views import LogoutView, UserDetailsView
from django.urls import path

from prj_auth import views as prj_auth_views

urlpatterns = [
    path("auth/login/", prj_auth_views.LoginView.as_view(), name="rest_login"),
    path("auth/logout/", LogoutView.as_view(), name="rest_logout"),
    path("auth/token/refresh/", prj_auth_views.RefreshView.as_view(), name="token_refresh"),
    path("auth/csrf/", prj_auth_views.CSRFView.as_view(), name="csrf_token"),
    path("auth/ping/", prj_auth_views.PingView.as_view(), name="ping"),
    path("auth/login_user/", UserDetailsView.as_view(), name="rest_user_details"),
]
