# main_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page at /
    path('report/', views.report, name='report'),  # Report page at /report/
    path('admin/user-approval/', views.admin_user_approval, name='admin_user_approval'),
    path('login/', views.login_view, name='login'),# Admin user approval page
]
