from django.db import models

from django.contrib.auth.models import User
from django.db.models import base
from django.db.models.expressions import F
from django.db.models.fields import DateTimeField

from django.db.models.signals import post_save
from django.dispatch import receiver

class Post(models.Model):
    title = models.CharField(max_length=50, verbose_name="Titulo")
    content = models.TextField()
    picture = models.ImageField(upload_to='uploads/post_picture/', blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    #likes and dislikes
    likes = models.ManyToManyField(User, blank=True, related_name="like")
    dislikes = models.ManyToManyField(User, blank=True, related_name="Dislike")
    
class Comment(models.Model):
    content = models.CharField(max_length=200, verbose_name="comment")
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    c_likes = models.ManyToManyField(User, blank=True, related_name="c_like")
    c_dislikes = models.ManyToManyField(User, blank=True, related_name="c_Dislike")

    

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, null=True, verbose_name="Nombre")
    location = models.CharField(max_length=100, null=True)
    web =  models.CharField(max_length=200, null=True, verbose_name="WEBSITE")
    picture = models.ImageField(upload_to='uploads/profile_pictures/', default='uploads/profile_pictures/default.png', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True),

    #Followers
    followers = models.ManyToManyField(User, related_name="followers", blank=True)

    

#For Message i will need to models..one will handle all the massage between te user 
#The Second one is message model has well

class Thread_Model(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    has_unread = models.BooleanField(default=False)


class Message_Model(models.Model):

    thread = models.ForeignKey('Thread_Model', related_name='+', on_delete=models.CASCADE, blank=True, null=True)
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    content = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='uploads/messages/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


class Notification(models.Model):
    # 1 = like 
    # 2 = comment
    # 3 = Follow 

    notification_type = models.IntegerField()
    to_user = models.ForeignKey(User, related_name="notification_to", on_delete=models.CASCADE, null=True)
    from_user = models.ForeignKey(User, related_name="notification_from", on_delete=models.CASCADE, null=True)
    
    #i will use a post and a comment field to have a way to link to the especific post and comment
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name="+", blank=True, null=True)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name="+", blank=True, null=True)
    
    date = models.DateTimeField(auto_now_add=True)
    user_has_seen = models.BooleanField(default=False)
