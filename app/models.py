from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid

class UserManager(BaseUserManager):
    def create_user(self, username, email, bio="", password=None):
        if not username:
            raise ValueError("Users must have a username")
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            bio=bio
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, bio="", password=None):
        user = self.create_user(
            username=username,
            email=email,
            bio=bio,
            password=password
        )

        user.is_admin = True
        user.save(using=self._db)
        return user

class SM_User(AbstractBaseUser):
    username = models.CharField(max_length = 40, unique = True, primary_key=True)
    email = models.EmailField(max_length = 255, unique = True)
    bio = models.CharField(max_length = 120, null = True, blank = True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ['email']
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
class Profile_Pic(models.Model):
    username = models.ForeignKey(SM_User, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='profile_pics/')

    def delete(self):
        self.image.delete()
        super().delete()

class Follow(models.Model):
    username = models.CharField(max_length = 40)
    other_username = models.CharField(max_length = 40)

class Post(models.Model):
    post_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, blank=True)
    username = models.ForeignKey(SM_User, on_delete=models.CASCADE, blank=True, null=True)
    content = models.CharField(max_length = 140)
    datetime_posted = models.DateTimeField(auto_now_add=True)
    reply_to = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

class Post_Like(models.Model):
    username = models.ForeignKey(SM_User, on_delete=models.CASCADE)
    parent_post_id = models.ForeignKey(Post, on_delete=models.CASCADE)

class Post_Dislike(models.Model):
    username = models.ForeignKey(SM_User, on_delete=models.CASCADE)
    parent_post_id = models.ForeignKey(Post, on_delete=models.CASCADE)