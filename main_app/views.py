# main_app/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created. Await admin approval.")
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})
from django.shortcuts import render

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_approved:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Account pending approval by admin.")
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, 'login.html')

@login_required
def create_post(request):
    if Post.objects.filter(user=request.user).exists():
        messages.error(request, "You have already posted once.")
        return redirect('home')

    if request.method == "POST":
        content = request.POST['content']
        Post.objects.create(user=request.user, content=content)
        messages.success(request, "Post created successfully.")
        return redirect('home')

    return render(request, 'create_post.html')


from django.core.paginator import Paginator


def post_list_view(request):
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 3)  # 3 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    for post in page_obj:
        post.content_truncated = (post.content[:100] + '...') if len(post.content) > 100 else post.content

    return render(request, 'post_list.html', {'page_obj': page_obj})


# main_app/views.py

from django.http import JsonResponse
from .models import UserPreference


@login_required
def toggle_dark_mode(request):
    preference, created = UserPreference.objects.get_or_create(user=request.user)
    preference.dark_mode = not preference.dark_mode
    preference.save()

    return JsonResponse({'dark_mode': preference.dark_mode})

# main_app/views.py

from django.core.paginator import Paginator

@login_required
def admin_user_approval(request):
    if not request.user.is_superuser:
        return redirect('home')

    users = CustomUser.objects.filter(is_approved=False)
    paginator = Paginator(users, 5)  # 5 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_user_approval.html', {'page_obj': page_obj})

@login_required
def admin_post_management(request):
    if not request.user.is_superuser:
        return redirect('home')

    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 5)  # 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_post_management.html', {'page_obj': page_obj})
# main_app/views.py
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import UserPreference

@login_required
def toggle_dark_mode(request):
    user_preference, created = UserPreference.objects.get_or_create(user=request.user)
    user_preference.dark_mode = not user_preference.dark_mode
    user_preference.save()

    return JsonResponse({'dark_mode': user_preference.dark_mode})

# main_app/views.py
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser

@login_required
def approve_user(request, user_id):
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to approve users.")
        return redirect('home')

    user = get_object_or_404(CustomUser, id=user_id)
    user.is_approved = True
    user.save()

    messages.success(request, f"User {user.username} has been approved.")
    return redirect('admin_user_approval')


# main_app/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Post


@login_required
def create_post(request):
    if Post.objects.filter(user=request.user).exists():
        messages.error(request, "You have already created a post and cannot create another one.")
        return redirect('home')

    if request.method == "POST":
        content = request.POST.get('content')
        if content:
            Post.objects.create(user=request.user, content=content)
            messages.success(request, "Your post has been created successfully.")
            return redirect('home')
        else:
            messages.error(request, "Post content cannot be empty.")

    return render(request, 'create_post.html')

# main_app/views.py

@login_required
def report(request, post_id=None, user_id=None):
    if request.method == "POST":
        message = request.POST.get('message')
        post = Post.objects.get(id=post_id) if post_id else None
        reported_user = CustomUser.objects.get(id=user_id) if user_id else None
        if message:
            Report.objects.create(
                reported_by=request.user,
                post=post,
                reported_user=reported_user,
                message=message
            )
            messages.success(request, "Report submitted successfully.")
            return redirect('home')
    return render(request, 'report.html')


@login_required
def approve_user(request, user_id):
    if not request.user.is_superuser:
        return redirect('home')

    user = CustomUser.objects.get(id=user_id)
    user.is_approved = True
    user.save()

    return redirect('admin_user_approval')

# Create your views here.
