from django.contrib import admin
from .models import Post, Comment, Profile, Notification, Message_Model, Thread_Model

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(Notification)
admin.site.register(Message_Model)
admin.site.register(Thread_Model)