from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime

from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.conf import settings
import os


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="profile")
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='default_profile.jpg')
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user_profile.user.username

@receiver(pre_delete, sender=Post)
def delete_image(sender, instance, **kwargs):
        # Delete the associated image when the model instance is deleted
    if instance.image:
        try:
            os.remove(instance.image.path)
        except Exception as e:
            pass

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username

    

class FollowersCount(models.Model):
    follower=models.CharField(max_length=100)
    user=models.CharField(max_length=100)

    def __str__(self):
        return self.user
    
