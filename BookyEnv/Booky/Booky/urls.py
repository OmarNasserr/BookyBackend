from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/location/", include("location_app.urls")),
    path("api/v1/playground/", include("playground_app.urls")),
    path("api/v1/user/", include("user_app.urls")),
    path('api/v1/playground/booking/', include('booking_app.urls')),
    path('api/v1/homepage/sliderimages/', include('content_manag_app.urls')),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)   
