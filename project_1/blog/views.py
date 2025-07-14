from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import Post, PostImage, PostFile, Profile
from .forms import postform, CustomPasswordChangeForm
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, PostForm, ProfileUpdateForm
from django.contrib.auth.models import User


def home(request):
    posts = Post.objects.select_related('author').prefetch_related('images', 'files').order_by('-created_at')
    return render(request, 'blog/home.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            post.author = request.user
            post.save()
            images = form.cleaned_data.get('images')
            if images:
                if isinstance(images, list):
                    for image in images:
                        PostImage.objects.create(post=post, image=image)
                else:
                    PostImage.objects.create(post=post, image=images)
            
            files = form.cleaned_data.get('files')
            if files:
                if isinstance(files, list):
                    for file in files:
                        PostFile.objects.create(
                            post=post, 
                            file=file, 
                            filename=file.name
                        )
                else:
                    PostFile.objects.create(
                        post=post, 
                        file=files, 
                        filename=files.name
                    )
            
            messages.success(request, 'Post created successfully!')
            return redirect('/', pk=post.pk)
    else:
        form = PostForm()
    
    return render(request, 'blog/create_post.html', {'form': form})

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, PostImage, PostFile
from .forms import PostForm

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if post.author != request.user:
        messages.error(request, "You are not allowed to edit this post.")
        return redirect('home')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            post = form.save()

            for img in request.FILES.getlist('images'):
                PostImage.objects.create(post=post, image=img)

            for f in request.FILES.getlist('files'):
                PostFile.objects.create(post=post, file=f, filename=f.name)

            messages.success(request, "Post updated successfully!")
            return redirect('/', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/edit_post.html', {
        'form': form,
        'post': post,
        'existing_images': post.images.all(),
        'existing_files': post.files.all(),
    })

@login_required
def delete_post(request, post_id):
    current_post = get_object_or_404(Post, id=post_id)
    if current_post.author != request.user:
        return redirect('home')  # or show a 403 page
    if request.method == 'POST':
        current_post.delete()
        return redirect('/')
    return render(request, 'blog/delete_post.html', {'current_post': current_post})


def custom_logout(request):
    logout(request)
    return redirect('custom_login')

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'blog/login.html', {'error': 'Invalid username or password'})
    return render(request, 'blog/login.html')

def custom_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'blog/signup.html', {'form': form})

@login_required
def dashboard(request):
    user_posts = Post.objects.filter(author=request.user)
    return render(request, 'blog/dashboard.html', {'user_posts': user_posts})

def edit_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)

        if user_form.is_valid() and password_form.is_valid():
            user_form.save()
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            return redirect('dashboard')
    else:
        user_form = UserUpdateForm(instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'blog/edit_profile.html', {
        'user_form': user_form,
        'password_form':password_form,
        })

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    images = post.images.all()
    files = post.files.all()
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'images': images,
        'files': files,
    })

@login_required
def profile_detail(request):
    """User's own profile page"""
    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'blog/profile_detail.html', {
        'profile_user': request.user,
        'user_posts': user_posts
    })

def public_profile(request, username):
    """Public profile page for any user"""
    profile_user = get_object_or_404(User, username=username)
    user_posts = Post.objects.filter(author=profile_user).order_by('-created_at')
    return render(request, 'blog/public_profile.html', {
        'profile_user': profile_user,
        'user_posts': user_posts
    })

@login_required
def edit_profile_extended(request):
    """Extended profile editing with all profile fields"""
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile_detail')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    return render(request, 'blog/edit_profile_extended.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })
