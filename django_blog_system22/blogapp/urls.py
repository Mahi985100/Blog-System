
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('blog/<int:id>/', views.detail, name='detail'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Admin Dashboard Routes
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/blogs/', views.blog_manage, name='blog_manage'),
    path('dashboard/blogs/add/', views.blog_add, name='blog_add'),
    path('dashboard/blogs/edit/<int:id>/', views.blog_edit, name='blog_edit'),
    path('dashboard/blogs/delete/<int:id>/', views.blog_delete, name='blog_delete'),
]
