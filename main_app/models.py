# main_app/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=15, unique=True)
    is_approved = models.BooleanField(default=False)  # Admin approval flag

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'contact_number']

    def __str__(self):
        return self.email
# main_app/models.py
class Post(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)  # One post per user
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.user.username}"

class Report(models.Model):
    reported_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return f"Report by {self.reported_by.username}"

# Register models in admin
from django.contrib import admin
from .models import CustomUser, Post, Report

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'is_approved']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Post)
admin.site.register(Report)

# main_app/models.py

class UserPreference(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    dark_mode = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s preferences"

# main_app/models.py

class Report(models.Model):
    reported_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE)
    reported_user = models.ForeignKey(CustomUser, null=True, blank=True, related_name='reported_user', on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return f"Report by {self.reported_by.username}"
