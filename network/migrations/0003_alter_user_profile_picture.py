# Generated by Django 4.2.1 on 2023-05-07 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0002_user_bio_user_profile_picture_post_like_follow"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="profile_picture",
            field=models.ImageField(
                blank=True, default=None, null=True, upload_to="network/static/network"
            ),
        ),
    ]
