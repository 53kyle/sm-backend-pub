from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime, UTC, timezone

from django.contrib.auth import get_user_model, login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework import permissions, status

from django.db.models import Q

from . models import *
from . serializer import *

class UserRegister(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(request.data)
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(status=status.HTTP_400_BAD_REQUEST)

class UserLogin(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(request.data)
            login(request, user)
            return Response(serializer.data, status=status.HTTP_200_OK)
                

class UserLogout(APIView):
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)

class UserView(APIView):
    def get(self, request, username):
        output = [{"username": output.username,
                   "bio": output.bio,
                   "email": output.email,
                   "password": output.password}
                for output in SM_User.objects.filter(username__exact=username)]
        return Response(output)
        
class UsersView(APIView):
    def get(self, request):
        output = [{"username": output.username,
                   "bio": output.bio,
                   "email": output.email,
                   "password": output.password}
                for output in SM_User.objects.all()]
        return Response(output)
        
class UserSearchView(APIView):
    def get(self, request, search_term):
        output = [{"username": output.username,
                   "bio": output.bio,
                   "email": output.email,
                   "password": output.password}
                for output in SM_User.objects.filter(username__contains=search_term)]
        return Response(output)
        
class FollowView(APIView):
    def get(self, request, username):
        output = [{"username": output.username,
                   "other_username": output.other_username}
                for output in Follow.objects.filter(username__exact=username)]
        return Response(output)
    def post(self, request, username):
        criterion1 = Q(username__exact=request.data['username'])
        criterion2 = Q(other_username__exact=request.data['other_username'])
        existingFollows = Follow.objects.filter(criterion1 & criterion2)
        if len(existingFollows) > 0:
            Follow.objects.filter(criterion1 & criterion2).delete()
            return Response(status=status.HTTP_200_OK)
        else:
            serializer = FollowSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        
class SpecificFollowView(APIView):
    def get(self, request, username, other_username):
        criterion1 = Q(username__exact=username)
        criterion2 = Q(other_username__exact=other_username)
        output = [{"username": output.username,
                   "other_username": output.other_username}
                for output in Follow.objects.filter(criterion1 & criterion2)]
        return Response(output)

class FollowerView(APIView):
    def get(self, request, username):
        output = [{"username": output.username,
                   "other_username": output.other_username}
                for output in Follow.objects.filter(other_username__exact=username)]
        return Response(output)
    def post(self, request, username):
        serializer = FollowSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
class SpecificFollowerView(APIView):
    def get(self, request, username, other_username):
        criterion1 = Q(username__exact=other_username)
        criterion2 = Q(other_username__exact=username)
        output = [{"username": UserSerializer(output.username).data['username'],
                   "other_username": UserSerializer(output.other_username).data['username']}
                for output in Follow.objects.filter(criterion1 & criterion2)]
        return Response(output)
    
class PostView(APIView):
    def get(self, request, post_id):
        output = [{"post_id": output.post_id,
                   "username": UserSerializer(output.username).data['username'],
                   "content": output.content,
                   "datetime_posted": output.datetime_posted,
                   "reply_to": PostSerializer(output.reply_to).data['post_id']}
                for output in Post.objects.filter(post_id__exact=post_id)]
        return Response(output)

class PostsView(APIView):
    def get(self, request, latest_datetime="2031-12-31T23:59:59.000000Z"):
        latest_datetime_obj = datetime.strptime(latest_datetime, '%Y-%m-%dT%H:%M:%S.%fZ')
        print(latest_datetime_obj)
        output = [{"post_id": output.post_id,
                   "username": UserSerializer(output.username).data['username'],
                   "content": output.content,
                   "datetime_posted": output.datetime_posted,
                   "reply_to": PostSerializer(output.reply_to).data['post_id']}
                for output in Post.objects.filter(datetime_posted__lt=latest_datetime_obj).order_by('-datetime_posted')[:10]]
        return Response(output)
    def post(self, request, latest_datetime="2031-12-31T23:59:59.000000Z"):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
class FollowingPostsView(APIView):
    def get(self, request, username, latest_datetime="2031-12-31T23:59:59.000000Z"):
        follows = set(Follow.objects.filter(username__exact=username).values_list('other_username', flat=True))
        latest_datetime_obj = datetime.strptime(latest_datetime, '%Y-%m-%dT%H:%M:%S.%fZ')
        criterion1 = Q(username__in=follows)
        criterion2 = Q(datetime_posted__lt=latest_datetime_obj)
        print(follows)
        output = [{"post_id": output.post_id,
                   "username": UserSerializer(output.username).data['username'],
                   "content": output.content,
                   "datetime_posted": output.datetime_posted,
                   "reply_to": PostSerializer(output.reply_to).data['post_id']}
                for output in Post.objects.filter(criterion1 & criterion2).order_by('-datetime_posted')[:10]]
        return Response(output)
        
class RepliesView(APIView):
    def get(self, request, post_id, latest_datetime="2031-12-31T23:59:59.000000Z"):
        latest_datetime_obj = datetime.strptime(latest_datetime, '%Y-%m-%dT%H:%M:%S.%fZ')
        criterion1 = Q(reply_to__exact=post_id)
        criterion2 = Q(datetime_posted__lt=latest_datetime_obj)
        output = [{"post_id": output.post_id,
                   "username": UserSerializer(output.username).data['username'],
                   "content": output.content,
                   "datetime_posted": output.datetime_posted,
                   "reply_to": PostSerializer(output.reply_to).data['post_id']}
                for output in Post.objects.filter(criterion1 & criterion2).order_by('-datetime_posted')[:10]]
        return Response(output)
        
class UserPostView(APIView):
    def get(self, request, username, latest_datetime="2031-12-31T23:59:59.000000Z"):
        latest_datetime_obj = datetime.strptime(latest_datetime, '%Y-%m-%dT%H:%M:%S.%fZ')
        criterion1 = Q(username__exact=username)
        criterion2 = Q(datetime_posted__lt=latest_datetime_obj)
        output = [{"post_id": output.post_id,
                   "username": UserSerializer(output.username).data['username'],
                   "content": output.content,
                   "datetime_posted": output.datetime_posted,
                   "reply_to": PostSerializer(output.reply_to).data['post_id']}
                for output in Post.objects.filter(criterion1 & criterion2).order_by('-datetime_posted')[:10]]
        return Response(output)
        
class PostSearchView(APIView):
    def get(self, request, search_term):
        output = [{"post_id": output.post_id,
                   "username": UserSerializer(output.username).data['username'],
                   "content": output.content,
                   "datetime_posted": output.datetime_posted}
                for output in Post.objects.filter(username__contains=search_term)]
        return Response(output)
    
class PostLikeView(APIView):
    def get(self, request, parent_post_id):
        output = [{"username": UserSerializer(output.username).data['username'],
            "parent_post_id": PostSerializer(output.parent_post_id).data['post_id']}
                for output in Post_Like.objects.filter(parent_post_id__exact=parent_post_id)]
        return Response(len(output))
    def post(self, request, parent_post_id):
        criterion1 = Q(parent_post_id__exact=request.data['parent_post_id'])
        criterion2 = Q(username__exact=request.data['username'])
        Post_Dislike.objects.filter(criterion1 & criterion2).delete()

        existingLikes = Post_Like.objects.filter(criterion1 & criterion2)
        if len(existingLikes) > 0:
            Post_Like.objects.filter(criterion1 & criterion2).delete()
            return Response(status=status.HTTP_200_OK)
        else:
            serializer = PostLikeSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        
class SpecificPostLikeView(APIView):
    def get(self, request, parent_post_id, username):
        criterion1 = Q(parent_post_id__exact=parent_post_id)
        criterion2 = Q(username__exact=username)
        output = [{"username": UserSerializer(output.username).data['username'],
            "parent_post_id": PostSerializer(output.parent_post_id).data['post_id']}
                for output in Post_Like.objects.filter(criterion1, criterion2)]
        return Response(output)
    
class PostDislikeView(APIView):
    def get(self, request, parent_post_id):
        output = [{"username": UserSerializer(output.username).data['username'],
            "parent_post_id": PostSerializer(output.parent_post_id).data['post_id']}
                for output in Post_Dislike.objects.filter(parent_post_id__exact=parent_post_id)]
        return Response(len(output))
    def post(self, request, parent_post_id):
        criterion1 = Q(parent_post_id__exact=request.data['parent_post_id'])
        criterion2 = Q(username__exact=request.data['username'])
        Post_Like.objects.filter(criterion1 & criterion2).delete()

        existingDislikes = Post_Dislike.objects.filter(criterion1 & criterion2)
        if len(existingDislikes) > 0:
            Post_Dislike.objects.filter(criterion1 & criterion2).delete()
            return Response(status=status.HTTP_200_OK)
        else:
            serializer = PostDislikeSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        
class SpecificPostDislikeView(APIView):
    def get(self, request, parent_post_id, username):
        criterion1 = Q(parent_post_id__exact=parent_post_id)
        criterion2 = Q(username__exact=username)
        output = [{"username": UserSerializer(output.username).data['username'],
            "parent_post_id": PostSerializer(output.parent_post_id).data['post_id']}
                for output in Post_Dislike.objects.filter(criterion1, criterion2)]
        return Response(output)
    
class ProfilePicView(APIView):
    def get(self, request, username):
        output = [{"username": UserSerializer(output.username).data['username'],
                   "image": output.image.url}
                   for output in Profile_Pic.objects.filter(username__exact=username)]
        return Response(output)
    def post(self, request, username):
        print(request.data)
        existingProfilePic = Profile_Pic.objects.filter(username__exact=username)
        if len(existingProfilePic) > 0:
            Profile_Pic.objects.filter(username__exact=username).delete()
        serializer = ProfilePicSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)