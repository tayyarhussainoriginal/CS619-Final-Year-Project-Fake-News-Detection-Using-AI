from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Admin FIRST
    path("admin/", admin.site.urls),

    # App routes
    path("", include("detector.urls")),
]

# allow uploaded files to be accessed during development 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)