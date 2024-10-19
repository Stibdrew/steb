from django.contrib import admin
from django.urls import path, include  # Import 'include' to include app's URLs

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel route
    path('', include('main_app.urls')),  # Include your app's URLs for the home page and others
]
