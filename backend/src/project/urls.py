from django.contrib import admin
from django.urls import include, path

from project import api_urls

urlpatterns = [
    path("admin/", admin.site.urls),
]

# api urls
urlpatterns += [
    path("api/", include(api_urls)),
]
