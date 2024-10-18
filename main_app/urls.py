# main_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Your homepage
    path('admin/user-approval/', views.admin_user_approval, name='admin_user_approval'),
    path('report/', views.report, name='report'),
]
