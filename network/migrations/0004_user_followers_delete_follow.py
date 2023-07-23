# Generated by Django 4.2.2 on 2023-07-20 13:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("network", "0003_alter_post_options_follow_follow_unique_followers"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="followers",
            field=models.ManyToManyField(
                blank=True, related_name="following", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.DeleteModel(
            name="Follow",
        ),
    ]
