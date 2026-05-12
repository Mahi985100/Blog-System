
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from .models import Blog, Comment, Category
from .forms import RegisterForm, BlogForm, CommentForm

def home(request):
    search = request.GET.get('search')
    category_id = request.GET.get('category')
    
    blogs = Blog.objects.all().order_by('-created_at')
    categories = Category.objects.all()

    if search:
        blogs = blogs.filter(title__icontains=search)
    
    if category_id:
        blogs = blogs.filter(category_id=category_id)

    paginator = Paginator(blogs, 6) # Increased to 6 for better grid
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home.html', {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None
    })

def detail(request, id):
    blog = get_object_or_404(Blog, id=id)
    comments = Comment.objects.filter(blog=blog)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.user = request.user
            comment.save()
            return redirect('detail', id=id)
    else:
        form = CommentForm()

    return render(request, 'detail.html', {
        'blog': blog,
        'comments': comments,
        'form': form
    })

def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('home')
    return render(request, 'register.html', {'form': form})

def user_login(request):
    form = AuthenticationForm(data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        if user.is_staff:
            return redirect('admin_dashboard')
        return redirect('home')
    return render(request, 'login.html', {'form': form})

@staff_member_required
def admin_dashboard(request):
    blog_count = Blog.objects.count()
    category_count = Category.objects.count()
    comment_count = Comment.objects.count()
    user_count = User.objects.count()
    
    recent_blogs = Blog.objects.order_by('-created_at')[:5]
    recent_users = User.objects.order_by('-date_joined')[:5]
    recent_comments = Comment.objects.order_by('-created_at')[:5]
    
    context = {
        'blog_count': blog_count,
        'category_count': category_count,
        'comment_count': comment_count,
        'user_count': user_count,
        'recent_blogs': recent_blogs,
        'recent_users': recent_users,
        'recent_comments': recent_comments,
    }
    return render(request, 'dashboard.html', context)

@staff_member_required
def blog_manage(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'blog_manage.html', {'blogs': blogs})

@staff_member_required
def blog_add(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('blog_manage')
    else:
        form = BlogForm()
    return render(request, 'blog_form.html', {'form': form, 'title': 'Add Blog'})

@staff_member_required
def blog_edit(request, id):
    blog = get_object_or_404(Blog, id=id)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog_manage')
    else:
        form = BlogForm(instance=blog)
    return render(request, 'blog_form.html', {'form': form, 'title': 'Edit Blog'})

@staff_member_required
def blog_delete(request, id):
    blog = get_object_or_404(Blog, id=id)
    if request.method == 'POST':
        blog.delete()
        return redirect('blog_manage')
    return render(request, 'blog_confirm_delete.html', {'blog': blog})

def user_logout(request):
    logout(request)
    return redirect('home')
