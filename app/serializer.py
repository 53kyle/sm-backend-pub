from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from . models import *

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SM_User
        fields = ['username', 'email', 'bio', 'password']
    def create(self, clean_data):
        user_obj = SM_User.objects.create_user(username=clean_data['username'], email=clean_data['email'], bio=clean_data['bio'], password=clean_data['password'])
        user_obj.username = clean_data['username']
        user_obj.save()
        return user_obj

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def check_user(self, clean_data):
        user = authenticate(username=clean_data['username'], password=clean_data['password'])
        if not user:
            raise ValueError('user not found')
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SM_User
        fields = ['username', 'email', 'bio']

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['username', 'other_username']

class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Post

class PostSerializer(serializers.ModelSerializer):
    post_id = serializers.UUIDField()
    
    class Meta:
        model = Post
        fields = ['post_id', 'username', 'content', 'datetime_posted', 'reply_to']

class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post_Like
        fields = ['username','parent_post_id']

class PostDislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post_Dislike
        fields = ['username','parent_post_id']

class ProfilePicSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = Profile_Pic
        fields = ['username','image']