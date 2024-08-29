"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', UserRegister.as_view()),
    path('login/', UserLogin.as_view()),
    path('logout/', UserLogout.as_view()),
    path('users/', UsersView.as_view()),
    path('users/<str:username>/', UserView.as_view()),
    path('users/<str:username>/profile-pic/', ProfilePicView.as_view()),
    path('users/<str:username>/follows/', FollowView.as_view()),
    path('users/<str:username>/follows/<str:other_username>/', SpecificFollowView.as_view()),
    path('users/<str:username>/followers/', FollowerView.as_view()),
    path('users/<str:username>/followers/<str:other_username>/', SpecificFollowerView.as_view()),
    path('posts/', PostsView.as_view()),
    path('posts/after/<str:latest_datetime>/', PostsView.as_view()),
    path('posts/following/<str:username>/', FollowingPostsView.as_view()),
    path('posts/following/<str:username>/after/<str:latest_datetime>/', FollowingPostsView.as_view()),
    path('posts/<str:post_id>/', PostView.as_view()),
    path('posts/<str:post_id>/replies/', RepliesView.as_view()),
    path('posts/<str:post_id>/replies/after/<str:latest_datetime>/', RepliesView.as_view()),
    path('users/<str:username>/posts/', UserPostView.as_view()),
    path('users/<str:username>/posts/after/<str:latest_datetime>/', UserPostView.as_view()),
    path('posts/<str:parent_post_id>/likes/', PostLikeView.as_view()),
    path('posts/<str:parent_post_id>/likes/<str:username>/', SpecificPostLikeView.as_view()),
    path('posts/<str:parent_post_id>/dislikes/', PostDislikeView.as_view()),
    path('posts/<str:parent_post_id>/dislikes/<str:username>/', SpecificPostDislikeView.as_view()),
    path('search/users/<str:search_term>/', UserSearchView.as_view()),
    path('search/posts/<str:search_term>/', PostSearchView.as_view())
]
