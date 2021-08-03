# Generated by Django 3.2.4 on 2021-08-02 04:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0008_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='c_dislikes',
            field=models.ManyToManyField(blank=True, related_name='c_Dislike', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='c_likes',
            field=models.ManyToManyField(blank=True, related_name='c_like', to=settings.AUTH_USER_MODEL),
        ),
    ]
